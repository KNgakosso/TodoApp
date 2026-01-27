from backend.models import Task, TaskModel, TaskList, TaskListModel
import datetime
import pytest
from backend.utils import get_new_id

# TEST TASKMODEL
#########################

def test_init_taskmodel():
    task_model = TaskModel(
        name= "Manger",
        description= "Manger des fruits et légumes.",
        deadline= datetime.date(2025, 10, 1),
        priority= 1
    )
    assert task_model.name == "Manger"
    assert task_model.description == "Manger des fruits et légumes."
    assert task_model.deadline == datetime.date(2025, 10, 1)
    assert task_model.priority == 1

def test_init_taskmodel_default_values():
    task_model = TaskModel(
        name= "Boire"
    )
    assert task_model.name == "Boire"
    assert task_model.description is None
    assert task_model.deadline is None
    assert task_model.priority == 0

@pytest.mark.parametrize("kwargs", [{},
                            {"name" : 10},
                            {"name" : "Tâche", "description" : False},
                            {"name" : "Tâche", "priority" : "Erreur"},
                                {"name" : "Tâche", "deadline" : 10}
                            ]
            )
def test_init_taskmodel_invalid_params_type(kwargs):
    with pytest.raises(ValueError):
        task_model = TaskModel(**kwargs)

#########################
# TEST TASK
#########################

# get_new_id
################
def test_get_new_id():
    id_1 = get_new_id()
    id_2 = get_new_id()
    assert id_1!= id_2
    assert isinstance(id_1, int)
    assert isinstance(id_2, int)

# task.__init__
##############
def test_init_task():
    task = Task(
        name= "Test",
        description= "Initialisation de la tâche.",
        deadline= datetime.date(2025, 10, 8),
        priority= 1,
        completed = True,
        list_name = "ToDoList"
    )
    assert isinstance(task.id, int)
    assert task.name == "Test"
    assert task.description == "Initialisation de la tâche."
    assert task.deadline == datetime.date(2025, 10, 8)
    assert task.priority == 1
    assert task.completed == True
    assert task.list_name == "ToDoList"

def test_init_task_default_values():
    task = Task(
        name= "Boire"
    )
    assert isinstance(task.id, int)
    assert task.name == "Boire"
    assert task.description is None
    assert task.deadline is None
    assert task.priority == 0
    assert task.completed == False
    assert task.list_name is None

"""
@pytest.mark.parametrize("kwargs", [{},
                            {"name" : 10},
                            {"name" : "Tâche", "description" : False},
                            {"name" : "Tâche", "deadline" : 10},
                            {"name" : "Tâche", "priority" : "Erreur"},
                            {"name" : "Tâche", "completed" : 10},
                            {"name" : "Tâche", "list_name" : 10},
                            ]
            )
def test_init_task_invalid_params_type(kwargs):
    with pytest.raises(ValueError):
        task = Task(**kwargs)
"""
def test_init_multiple_tasks_different_ids():
    task_1 = Task(name= "Tâche seule")
    task_2 = Task(name= "Tâche double")
    task_3 = Task(name= "Tâche double")

    assert task_1.id != task_2.id
    assert task_1.id != task_3.id
    assert task_2.id != task_3.id

# task.from_model
################

def test_init_task_from_model(sample_task_model_basic):
    task = Task.from_model(sample_task_model_basic)
    assert isinstance(task.id, int) 
    assert task.name == "Tâche"
    assert task.description == "Description"
    assert task.deadline == datetime.date(2025, 10, 5)
    assert task.priority == 100
    assert task.completed == False
    assert task.list_name is None

def test_init_task_from_model_default_values(sample_task_model):
    task = Task.from_model(sample_task_model(name= "Tâche"))
    assert isinstance(task.id, int)
    assert task.name == "Tâche"
    assert task.description is None
    assert task.deadline is None
    assert task.priority == 0
    assert task.completed == False
    assert task.list_name is None


def test_init_task_from_model_invalid_params_type():
    with pytest.raises(ValueError):
        task = Task.from_model(7)

def test_init_multiple_tasks_from_model(sample_task_model, sample_task_model_basic):
    task_1 = Task.from_model(sample_task_model(name= "Tâche 1"))
    task_2 = Task.from_model(sample_task_model_basic)
    task_3 = Task.from_model(sample_task_model_basic)

    assert task_1.id != task_2.id
    assert task_1.id != task_3.id
    assert task_2.id != task_3.id

#########################
# TESTS TASKLIST
#########################

# Tasklist.__init__
#########################
def test_init_tasklist():
    task_list = TaskList(name= "Liste", 
                         tasks= {1,2,3},
    )
    assert task_list.name == "Liste"
    assert task_list.tasks == {1,2,3}

def test_init_tasklist_default_values():
    task_list = TaskList(
        name= "Todo"
    )
    assert task_list.name == "Todo"
    assert isinstance(task_list.tasks, set)
    assert len(task_list.tasks) == 0

# Tasklist.from_model
#########################
def test_init_task_list_from_model():
    task_list = TaskList.from_model(TaskListModel(name= "Projets"))
    assert task_list.name == "Projets"
    assert isinstance(task_list.tasks, set)
    assert len(task_list.tasks) == 0

def test_init_task_list_from_model_invalid_param_type():
    with pytest.raises(ValueError):
        task = TaskList.from_model(7)