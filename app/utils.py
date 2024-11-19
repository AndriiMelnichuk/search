import requests as req
from .models import Task, Group
from itertools import product

task_url = 'http://user-service:5001/'
task_url = 'http://localhost:5001/'

def get_tasks4group(id, jwt):
    data = {
        'type': 'get_tasks_for_group',
        'group_id': id,
        'jwt': jwt
    }
    head = {
        'Content-Type': 'application/json'
    }
    response = req.post(task_url, 
                        json=data, 
                        headers=head).json()
    
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
    head = {
        'Content-Type': 'application/json'
    }
    response = req.post(task_url, 
                        json=data, 
                        headers=head).json()
    group_count = len(response['group_id'])
    group_list = [Group(
                      response['group_id'][i],
                      response['group'][i],
                      )
    for i in range(group_count)]
    return group_list
    

def filter_groups(group_list: list, text:str):
    return [group for group in group_list if text.lower() in group.name.lower()]


def filter_tasks(task_list: list, text: str, assigned_to: list, complete_before: str, todo, is_date) -> list:
    result = task_list.copy()
    if text != '':
        result = union(filter_by_title(result, text), filter_by_description(result, text))
    if assigned_to != []:
        result = filter_by_assigned(result, assigned_to)
    if is_date:
        result = filter_by_deadline(result, complete_before)
    if todo != '':
        result = filter_by_todo(result, todo)

    return result


def union(list1, list2):
    return list1 + [item for item in list2 if item not in list1]


def intersection(a: list, b: list) -> list:
    return [elem for elem in a if elem in b]


def filter_by_title(task_list: list, search_name: str) -> list:
    return [task for task in task_list if search_name.lower() in task.name.lower()]


def filter_by_description(task_list: list, search_name: str) -> list:
    return [task for task in task_list if search_name.lower() in task.description.lower()]


def filter_by_deadline(task_list: list, deadline: str) -> list:
    return [task for task in task_list if deadline == task.deadline]


def filter_by_assigned(task_list: list, assigned: list) -> list:
    ans = []
    for task in task_list:
        for user in task.assigned:
            if user in assigned:
                ans.append(task)            
    return list(set(ans))


def filter_by_todo(task_list: list, todo) -> list:
    return [task for task in task_list if todo == task.todo]

