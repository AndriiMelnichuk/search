from .models import Task, Group, TaskWithGroup
from .rpcClient import RpcClient
from .filter import filter_tasks, filter_groups
USER_SERVICE_QUEUE = 'user_service_queue'

def get_tasks4group(id, jwt):
    data = {
        'type': 'get_tasks_for_group',
        'group_id': id,
        'jwt': jwt
    }
    client = RpcClient()
    response = client.call(data, USER_SERVICE_QUEUE)
    # response2Task
    task_count = len(response['task_id'])
    task_list = [Task(
                      response['task_id'][i],
                      response['task_name'][i],
                      response['description'][i],
                      response['deadline'][i],
                      response['members'][i],
                      response['todo_task'][i]
                      )
    for i in range(task_count)]
    return task_list
    

def get_groups(jwt):
    data = {
        'type': 'get_groups',
        'jwt': jwt
    }
    client = RpcClient()
    response = client.call(data, USER_SERVICE_QUEUE)
    group_count = len(response['group_id'])
    group_list = [Group(
                      response['group_id'][i],
                      response['group'][i],
                      )
    for i in range(group_count)]
    return group_list


def get_all_tasks(jwt):
    data = {
        'type': 'get_tasks_for_user',
        'jwt': jwt
    }
    client = RpcClient()
    response = client.call(data, USER_SERVICE_QUEUE)
    task_count = len(response['task_id'])
    task_list = [TaskWithGroup(
                      response['group_id'][i],
                      response['task_id'][i],
                      response['task_name'][i],
                      response['description'][i],
                      response['deadline'][i],
                      response['members'][i],
                      response['todo_task'][i]
                      )
    for i in range(task_count)]
    return task_list


def on_task(message):
    jwt = message.get('jwt')
    group_id = message.get('group_id')
    text = message.get('text')
    assigned_to = message.get('assigned_to')
    complete_before = message.get('complete_before')
    todo = message.get('status')
    is_date = message.get('is_date')
    task_list = get_tasks4group(group_id, jwt)
    filtered_task_list = filter_tasks(task_list, text, assigned_to, complete_before, todo, is_date)  
    response = {
        'id': [t.id for t in filtered_task_list],
        'title': [t.name for t in filtered_task_list],
        'description': [t.description for t in filtered_task_list],
        'deadline': [t.deadline for t in filtered_task_list],
        'assigned': [t.assigned for t in filtered_task_list],
        'status': [t.todo for t in filtered_task_list],
        }
    return response

def on_group(message):
        jwt = message.get('jwt')
        text = message.get('text')
        group_list = get_groups(jwt)
        filtered_group_list = filter_groups(group_list, text)
        response = {
            "id": [group.id for group in filtered_group_list],
            "group": [group.name for group in filtered_group_list],
        }
        return response

def on_task_date(message):
    jwt = message['jwt']
    date = message['date'] 
    
    task_list = get_all_tasks(jwt)
    filtered_task_list = list(filter(lambda x: date in x.date, task_list))
    
    response = {
        'group_id': [t.group_id for t in filtered_task_list],
        'task_id': [t.task_id for t in filtered_task_list],
        'title': [t.name for t in filtered_task_list],
        'description': [t.description for t in filtered_task_list],
        'deadline': [t.deadline for t in filtered_task_list],
        'assigned': [t.assigned for t in filtered_task_list],
        'status': [t.todo for t in filtered_task_list],
        }
    return response