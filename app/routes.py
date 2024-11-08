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

    task_list = get_tasks4group(group_id, jwt)
    filtered_task_list = filter_tasks(task_list, text, assigned_to, complete_before, todo)  
    return jsonify([{
        'id': t.id,
        'title': t.name,
        'description': t.description,
        'deadline': t.deadline,
        'assigned': t.assigned,
        'status': t.todo
    } for t in filtered_task_list])


@main.route('/group', methods=['POST'])
def group_search():
    data = request.get_json()
    jwt = data.get('jwt')
    text = data.get('text')

    group_list = get_groups(jwt)
    filtered_group_list = filter_groups(group_list, text)
    return jsonify([{
        'id': group.id,
        'name': group.name
    } for group in filtered_group_list])