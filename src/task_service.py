import src.storage as st
from src.models import Task, TaskModel, TaskListModel, TaskList

def create_task(task_model : TaskModel, list_name : str | None) -> Task:
    if not isinstance(task_model, TaskModel):
        raise ValueError
    if not isinstance(list_name, str) and not list_name is None:
        raise ValueError
    task = Task.from_model(task_model)
    st.set_ongoing_tasks.add(task.id)
    st.dict_tasks[task.id] = task
    if list_name:
        add_task_to_task_list(task.id, list_name)
    return task

def create_task_list(task_list_model : TaskListModel) -> TaskList:
    if not isinstance(task_list_model, TaskListModel):
        raise ValueError
    if task_list_model.name in st.dict_tasks_lists.keys():
        raise ValueError("La liste existe déjà.")
    list_tasks = TaskList.from_model(task_list_model)
    st.dict_tasks_lists[task_list_model.name] = list_tasks
    return list_tasks

def get_task(task_id : int) -> Task:
    if not isinstance(task_id, int):
        raise ValueError
    if not task_id in st.dict_tasks.keys():
        raise ValueError("La tâche n'existe pas",) 
    return st.dict_tasks[task_id]

def get_tasks() -> dict[int, Task]:
    return st.dict_tasks

def get_completed_tasks() -> dict[int, Task]:
    return {task_id : st.dict_tasks[task_id] for task_id in st.set_completed_tasks}

def get_ongoing_tasks() -> dict[int, Task]:
    return {task_id : st.dict_tasks[task_id] for task_id in st.set_ongoing_tasks}

def update_task(task_id : int, task_model : TaskModel) -> Task:
    if not isinstance(task_id, int):
        raise ValueError
    if not isinstance(task_model, TaskModel):
        raise ValueError
    if not task_id in st.dict_tasks.keys():
        raise ValueError("La tâche n'existe pas")
    updates = task_model.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(st.dict_tasks[task_id], key, value )
    return st.dict_tasks[task_id]

def delete_task(task_id : int) -> Task:
    if not isinstance(task_id, int):
        raise ValueError
    if not task_id in st.dict_tasks.keys():
        raise ValueError("La tâche n'existe pas")
    st.set_completed_tasks.discard(task_id)
    st.set_ongoing_tasks.discard(task_id)
    list_name = st.dict_tasks[task_id].list_name
    if not list_name is None:
        st.dict_tasks_lists[list_name].tasks.remove(task_id)
    return st.dict_tasks.pop(task_id)

def get_task_list(task_list_name : str) -> TaskList:
    if not isinstance(task_list_name, str):
        raise ValueError
    if not task_list_name in st.dict_tasks_lists.keys():
        raise ValueError("La liste n'existe pas") 
    return st.dict_tasks_lists[task_list_name]

def get_task_lists() -> dict[str, TaskList]:
    return st.dict_tasks_lists


def delete_task_list(task_list_name : str) -> TaskList:
    if not task_list_name in st.dict_tasks_lists:
        raise ValueError("La liste n'existe pas.")
    for task_id in st.dict_tasks_lists[task_list_name].tasks:
        st.dict_tasks[task_id].list_name = None
    return st.dict_tasks_lists.pop(task_list_name)

def toggle_task(task_id : int):
    if not isinstance(task_id, int):
        raise ValueError
    if not task_id in st.dict_tasks.keys():
        raise ValueError
    st.dict_tasks[task_id].completed = not st.dict_tasks[task_id].completed
    st.set_ongoing_tasks.symmetric_difference_update({task_id})
    st.set_completed_tasks.symmetric_difference_update({task_id})
    return st.dict_tasks[task_id]

def add_task_to_task_list(task_id, list_name):
    st.dict_tasks[task_id].list_name = list_name
    st.dict_tasks_lists.setdefault(list_name, TaskList(name = list_name)).tasks.add(task_id)
        