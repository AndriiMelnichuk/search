
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
    todo = 'true' == todo
    return [task for task in task_list if todo == task.todo]

