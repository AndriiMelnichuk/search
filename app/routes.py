from flask import Blueprint, request, jsonify
from .utils import get_tasks4group, filter_tasks, get_groups, filter_groups

main = Blueprint('main', __name__)

@main.route('/task', methods=['POST'])
def task_search():
    data = request.get_json()
    jwt = data.get('jwt')
    group_id = data.get('group_id')
    text = data.get('text')
    assigned_to = data.get('assigned_to')
    complete_before = data.get('complete_before')
    todo = data.get('status')
    is_date = data.get('is_date')

    task_list = get_tasks4group(group_id, jwt)
    filtered_task_list = filter_tasks(task_list, text, assigned_to, complete_before, todo, is_date)  
    return {
        'id': [t.id for t in filtered_task_list],
        'title': [t.name for t in filtered_task_list],
        'description': [t.description for t in filtered_task_list],
        'deadline': [t.deadline for t in filtered_task_list],
        'assigned': [t.assigned for t in filtered_task_list],
        'status': [t.todo for t in filtered_task_list],
    }



@main.route('/group', methods=['POST'])
def group_search():
    data = request.get_json()
    jwt = data.get('jwt')
    text = data.get('text')

    group_list = get_groups(jwt)
    filtered_group_list = filter_groups(group_list, text)
    return{
        "id": [group.id for group in filtered_group_list],
        "group": [group.name for group in filtered_group_list],
    }
