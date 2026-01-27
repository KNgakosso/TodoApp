import pytest
import datetime
from models import Task, TaskModel, TaskList, TaskListModel
import storage as storage
import backend.utils
import backend.task_service as ts
from typing import Callable

@pytest.fixture
def sample_task_model_basic() -> TaskModel:
    return TaskModel(
        name="Tâche",
        description="Description",
        priority=100,
        deadline = datetime.date(2025, 10, 5)
    )

@pytest.fixture
def sample_task_model() -> Callable[[str], TaskModel]:
    def task_model_factory(name : str = "Tâche", **kwargs ) -> TaskModel:
        return TaskModel(name=name,  **kwargs)
    return task_model_factory


@pytest.fixture
def sample_task() -> Callable[[str], Task]:
    def task_factory(name : str = "Tâche", list_name : str | None = None, completed : bool = False,  **kwargs) -> Task:
        task = ts.create_task(TaskModel(name=name, **kwargs),
                                 list_name=list_name)
        if completed:
            ts.toggle_task(task.id)
        return task
    return task_factory

@pytest.fixture
def sample_task_list_model() -> Callable[[str], TaskListModel]:
    def task_list_model_factory(name : str = "Liste") -> TaskListModel:
        return TaskListModel(name = name)
    return task_list_model_factory

@pytest.fixture
def sample_task_list() -> Callable[[str], TaskList]:
    def task_list_factory(name : str = "Liste") -> TaskList:
        task_list = ts.create_task_list(TaskListModel(name=name))
        return task_list
    return task_list_factory

# EXEMPLES DATASETS
@pytest.fixture
def sample_basic_tasks() -> dict[str, dict]:
    task_1 = ts.create_task(TaskModel(name= "Tâche 1"), list_name=None)
    task_2 = ts.create_task(TaskModel(name= "Tâche 2"), list_name="Liste A")
    task_3 = ts.create_task(TaskModel(name= "Tâche 3"), list_name="Liste B")
    task_4 = ts.create_task(TaskModel(name= "Tâche 4"), list_name= "Liste A")

    task_list_c = ts.create_task_list(TaskListModel(name = "Liste C"))

    return {
        "tasks" : storage.dict_tasks,
        "task_lists" : storage.dict_tasks_lists
    }


@pytest.fixture
def sample_basic_tasks_2() -> dict:
    task_list_1 = ts.create_task_list(TaskListModel(name= "Sport"))
    task_list_2 = ts.create_task_list(TaskListModel(name= "Courses"))
    task_list_3 = ts.create_task_list(TaskListModel(name= "Tâches ménagères"))
    task_1 = ts.create_task(TaskModel(name= "Footing", description= "Courir 5km.", priority= 2), list_name= "Sport")  #completed - Sport
    task_2 = ts.create_task(TaskModel(name= "Étirements", priority= 2), list_name= "Sport")  #ongoing - Sport
    task_3 = ts.create_task(TaskModel(name= "Musculation", description= "Haut du corps", priority= 1), list_name= "Sport")  #ongoing - Sport
    task_4 = ts.create_task(TaskModel(name= "Basket"), list_name= "Sport")  #ongoing - Sport

    task_5 = ts.create_task(TaskModel(name= "Légumes", description="Poireaux, Carottes, Oignons."), list_name= "Courses")  #completed - Courses
    task_6 = ts.create_task(TaskModel(name= "Lait"), list_name= "Courses")   #completed - Courses
    task_7 = ts.create_task(TaskModel(name= "Fromage"), list_name= "Courses")   #completed - Courses

    task_8 = ts.create_task(TaskModel(name= "Lave vaisselle", priority= 5), list_name= "Tâches ménagères") #ongoing - Tâches ménagères
    task_9 = ts.create_task(TaskModel(name= "Aspirateur", priority = 5), list_name= "Tâches ménagères")  #ongoing - Tâches ménagères

    task_1 = ts.toggle_task(task_1.id)
    task_5 = ts.toggle_task(task_5.id)
    task_6 = ts.toggle_task(task_6.id)
    task_7 = ts.toggle_task(task_7.id)
    return {
        "tasks" : storage.dict_tasks,
        "task_lists" : storage.dict_tasks_lists
    }

def sample_basic_tasks_3() -> dict[str, dict]:
    task_list_a = ts.create_task_list(TaskListModel(name="Liste A"))   #tâche 2
    task_list_b = ts.create_task_list(TaskListModel(name="Liste B"))   #deleted
    task_list_c = ts.create_task_list(TaskListModel(name="Liste C"))   #vide
    task_1 = ts.create_task(TaskModel(name= "Tâche 1"), list_name="Liste A")  #deleted
    task_2 = ts.create_task(TaskModel(name= "Tâche 2"), list_name="Liste A")  #completed - List A
    task_3 = ts.create_task(TaskModel(name= "Tâche 3"), list_name="Liste B")  #deleted
    task_4 = ts.create_task(TaskModel(name= "Tâche 4"), list_name="Liste B")  #ongoing

    task_1 = ts.delete_task(task_1.id)
    task_3 = ts.delete_task(task_3.id)
    task_2 = ts.toggle_task(task_2.id)
    task_list_b = ts.delete_task_list("Liste B") 
    return {
        "tasks" : storage.dict_tasks,
        "task_lists" : storage.dict_tasks_lists
    }

@pytest.fixture(autouse=True)
def clear_sotrage():
    storage.dict_tasks.clear()
    storage.dict_tasks_lists.clear()
    storage.set_ongoing_tasks.clear()
    storage.set_completed_tasks.clear()
    src.utils.next_id = 0