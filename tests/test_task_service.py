import src.task_service as ts
import src.storage as st
import pytest
import datetime

# TEST CREATE TASK
######################

def test_create_task(sample_task_model_basic):
    task_model = sample_task_model_basic
    task = ts.create_task(task_model= task_model,
                          list_name= None)
    assert len(st.dict_tasks) == 1
    assert task.id in st.dict_tasks.keys()
    assert task == st.dict_tasks[task.id]

    assert len(st.set_ongoing_tasks) == 1
    assert task.id in st.set_ongoing_tasks

    assert not task.id in st.set_completed_tasks

    assert len(st.dict_tasks_lists) == 0


def test_create_task_with_non_existing_list_name(sample_task_model_basic):
    task = ts.create_task(task_model= sample_task_model_basic,
                        list_name= "Liste")
    assert len(st.dict_tasks) == 1
    assert task.id in st.dict_tasks.keys()
    assert st.dict_tasks[task.id] == task
    
    assert task.list_name == "Liste"
    assert "Liste" in st.dict_tasks_lists
    assert st.dict_tasks_lists["Liste"].name == "Liste"
    assert len(st.dict_tasks_lists["Liste"].tasks) == 1
    assert task.id in st.dict_tasks_lists["Liste"].tasks

    assert len(st.set_ongoing_tasks) == 1
    assert task.id in st.set_ongoing_tasks

    assert len(st.set_completed_tasks) == 0

def test_create_task_with_existing_list_name(sample_task_list, sample_task_model_basic):
    task_list = sample_task_list("Liste")
    task = ts.create_task(task_model= sample_task_model_basic,
                          list_name= "Liste")
    assert len(st.dict_tasks) == 1
    assert task.id in st.dict_tasks.keys()
    assert st.dict_tasks[task.id] == task
    
    assert task.list_name == "Liste"
    assert "Liste" in st.dict_tasks_lists
    assert st.dict_tasks_lists["Liste"].name == "Liste"
    assert len(st.dict_tasks_lists["Liste"].tasks) == 1
    assert task.id in st.dict_tasks_lists["Liste"].tasks

    assert len(st.set_ongoing_tasks) == 1
    assert task.id in st.set_ongoing_tasks

    assert len(st.set_completed_tasks) == 0

def test_create_multiple_tasks(sample_task_model):
    task_1 = ts.create_task(task_model= sample_task_model("Tâche 1"),
                          list_name= "Liste A")
    task_2 = ts.create_task(task_model= sample_task_model("Tâche 2", description= "Description_2"),
                          list_name= "Liste B")
    task_3 = ts.create_task(task_model= sample_task_model("Tâche 3", priority= 3),
                          list_name= None)
    task_4 = ts.create_task(task_model= sample_task_model("Tâche 4", deadline= datetime.date(2027,4,4)),
                          list_name= "Liste A")

    assert len(st.dict_tasks) == 4
    assert task_1.id in st.dict_tasks.keys()
    assert task_2.id in st.dict_tasks.keys()
    assert task_3.id in st.dict_tasks.keys()
    assert task_4.id in st.dict_tasks.keys()
    assert task_1 == st.dict_tasks[task_1.id]
    assert task_2 == st.dict_tasks[task_2.id]
    assert task_3 == st.dict_tasks[task_3.id]
    assert task_4 == st.dict_tasks[task_4.id]

    assert task_1.list_name == "Liste A"
    assert task_2.list_name == "Liste B"
    assert task_3.list_name is None
    assert task_4.list_name == "Liste A"
    assert len(st.dict_tasks_lists) == 2
    assert task_1.id in st.dict_tasks_lists["Liste A"].tasks
    assert task_4.id in st.dict_tasks_lists["Liste A"].tasks
    assert task_2.id in st.dict_tasks_lists["Liste B"].tasks

    assert len(st.set_ongoing_tasks) == 4
    assert task_1.id in st.set_ongoing_tasks
    assert task_2.id in st.set_ongoing_tasks
    assert task_3.id in st.set_ongoing_tasks
    assert task_4.id in st.set_ongoing_tasks

    assert len(st.set_completed_tasks) == 0

def test_create_task_with_invalid_task_model():
    with pytest.raises(ValueError):
        task = ts.create_task(task_model=7, list_name= None)

def test_create_task_with_invalid_list_name(sample_task_model_basic):
    with pytest.raises(ValueError):
        task = ts.create_task(task_model=sample_task_model_basic, list_name= 7)


# TEST GET TASK
###################
def test_get_task_correct_id(sample_basic_tasks):
    sample = sample_basic_tasks
    task = ts.get_task(1)
    assert task.id == 1
    assert task.name == "Tâche 1"
    assert task == st.dict_tasks[1]

def test_get_task_correct_id_on_list(sample_task):
    task = sample_task(name="Tâche 1", list_name = "Liste A")
    task = ts.get_task(1)
    assert task.id == 1
    assert task.name == "Tâche 1"
    assert task == st.dict_tasks[1]

def test_get_task_correct_id_completed(sample_task):
    task = sample_task(name="Tâche 1", completed = True)
    task = ts.get_task(1)
    assert task.id == 1
    assert task.name == "Tâche 1"
    assert task == st.dict_tasks[1]

def test_get_task_incorrect_id(sample_basic_tasks):
    sample = sample_basic_tasks
    with pytest.raises(ValueError):
        task = ts.get_task(10)

def test_get_task_empty_dataset():
    with pytest.raises(ValueError):
        task = ts.get_task(1)

def test_get_task_deleted(sample_basic_tasks):
    sample = sample_basic_tasks
    ts.delete_task(1)
    with pytest.raises(ValueError):
        task = ts.get_task(1)

def test_get_task_invalid_parameter(sample_basic_tasks):
    sample = sample_basic_tasks
    with pytest.raises(ValueError):
        task = ts.get_task("1")

# TEST GET TASKS
#######################
def test_get_tasks(sample_basic_tasks):
    sample = sample_basic_tasks
    result = ts.get_tasks()
    assert result == st.dict_tasks

def test_get_tasks_with_deleted_tasks(sample_basic_tasks_2):
    sample = sample_basic_tasks_2
    result = ts.get_tasks()
    assert result == st.dict_tasks

def test_get_tasks_empty():
    result = ts.get_tasks()
    assert result == st.dict_tasks

# TEST GET ONGOING TASKS
#################################

def test_get_ongoing_tasks(sample_basic_tasks):
    sample = sample_basic_tasks
    result = ts.get_ongoing_tasks()
    for task_id, task in result.items():
        assert task_id in st.set_ongoing_tasks
        assert not task.completed
        assert task == st.dict_tasks[task_id]
    assert len(result) == len(st.set_ongoing_tasks)

def test_get_ongoing_tasks_empty(sample_task):
    task_1 = sample_task("Tâche finie 1", completed = True)
    task_2 = sample_task("Tâche finie 2", completed = True)
    result = ts.get_ongoing_tasks()
    assert len(result) == 0

# TEST GET COMPLETED TASKS
#################################
def test_get_completed_tasks(sample_basic_tasks):
    sample = sample_basic_tasks
    result = ts.get_completed_tasks()
    for task_id, task in result.items():
        assert task_id in st.set_completed_tasks
        assert task.completed
        assert task == st.dict_tasks[task_id]
    assert len(result) == len(st.set_completed_tasks)

def test_get_completed_tasks_empty(sample_task):
    task_1 = sample_task("Tâche non finie 1")
    task_2 = sample_task("Tâche non finie 2")
    result = ts.get_completed_tasks()
    assert len(result) == 0

# TEST TOGGLE TASK
#######################
def test_toggle_task_complete_the_task(sample_task):
    task = sample_task(name="Tâche à finir")
    task_id = task.id
    task = ts.toggle_task(task.id)
    assert st.dict_tasks[task_id].completed
    assert st.dict_tasks[task_id] == task
    assert len(st.set_ongoing_tasks) == 0
    assert task_id in st.set_completed_tasks
    assert len(st.set_completed_tasks) == 1

def test_toggle_task_restart_the_task(sample_task):
    task = sample_task(name="Tâche à reprendre", completed = True, list_name = "Liste")
    task_id = task.id
    task = ts.toggle_task(task_id)
    assert not st.dict_tasks[task_id].completed
    assert st.dict_tasks[task_id] == task
    assert len(st.set_completed_tasks) == 0
    assert task_id in st.set_ongoing_tasks
    assert len(st.set_ongoing_tasks) == 1

def test_toggle_task_complete_and_restart_task(sample_task):
    task = sample_task(name="Tâche en cours", completed = False, list_name = "Liste")
    task_id = task.id
    task = ts.toggle_task(task_id)
    task = ts.toggle_task(task_id)
    assert not st.dict_tasks[task_id].completed
    assert st.dict_tasks[task_id] == task
    assert len(st.set_completed_tasks) == 0
    assert task_id in st.set_ongoing_tasks
    assert len(st.set_ongoing_tasks) == 1

def test_toggle_task_restart_and_complete_task(sample_task):
    task = sample_task(name="Tâche finie", completed = True, list_name = "Liste")
    task_id = task.id
    task = ts.toggle_task(task_id)
    task = ts.toggle_task(task_id)
    assert st.dict_tasks[task_id].completed
    assert st.dict_tasks[task_id] == task
    assert len(st.set_ongoing_tasks) == 0
    assert task_id in st.set_completed_tasks
    assert len(st.set_completed_tasks) == 1

def test_toggle_task_non_exsiting(sample_basic_tasks):
    sample = sample_basic_tasks
    with pytest.raises(ValueError):
        task = ts.toggle_task(10)

def test_toggle_task_invalid_param(sample_basic_tasks):
    sample = sample_basic_tasks
    with pytest.raises(ValueError):
        task = ts.toggle_task("invalid_id")


# TEST DELELTE TASK
#########################

def test_delete_task_simple(sample_task):
    task = sample_task()
    task = ts.delete_task(task.id)

    assert len(st.dict_tasks) == 0
    assert len(st.set_ongoing_tasks) == 0
    assert len(st.set_completed_tasks) == 0

def test_delete_task_in_list(sample_task):
    task = sample_task(list_name = "Liste.")
    task = ts.delete_task(task.id)

    assert len(st.dict_tasks) == 0
    assert len(st.set_ongoing_tasks) == 0
    assert len(st.set_completed_tasks) == 0

    assert len(st.dict_tasks_lists) == 1
    assert "Liste." in st.dict_tasks_lists
    assert len(st.dict_tasks_lists["Liste."].tasks) == 0

def test_delete_task_completed_task(sample_basic_tasks_2):
    sample = sample_basic_tasks_2
    task = ts.delete_task(6)

    assert len(st.dict_tasks) == 8
    assert not 6 in st.dict_tasks.keys()
    assert not 6 in st.set_ongoing_tasks
    assert len(st.set_completed_tasks) == 3

def test_delete_multiple_tasks(sample_basic_tasks_2):
    sample = sample_basic_tasks_2
    task_1 = ts.delete_task(1)
    task_2 = ts.delete_task(2)
    task_3 = ts.delete_task(3)
    task_4 = ts.delete_task(4)

    assert len(st.dict_tasks) == 5
    assert len(st.set_completed_tasks) == 3
    assert len(st.set_ongoing_tasks) == 2
    assert len(st.dict_tasks_lists) == 3

def test_delete_task_non_existing(sample_basic_tasks):
    sample = sample_basic_tasks
    with pytest.raises(ValueError):
        task = ts.delete_task(10)

def test_delete_task_invalid_param(sample_basic_tasks):
    sample = sample_basic_tasks
    with pytest.raises(ValueError):
        task = ts.delete_task("Error")

# TEST UPDATE TASK
######################

@pytest.mark.parametrize("list_name", ["Liste", None])
@pytest.mark.parametrize("completed", [True, False])
def test_update_task_all_attributes(sample_task, sample_task_model, list_name, completed):
    task_prev = sample_task(name= "Task name before",
                            description = "Description before",
                            deadline = datetime.date(2025,10,10),
                            priority = 0,
                            list_name = list_name,
                            completed= completed
                        )
    task_id_prev = task_prev.id
    task_model = sample_task_model(name= "Task name after",
                            description = "Description after",
                            deadline = datetime.date(2026,11,11),
                            priority = 1,
                        )
    task_updated = ts.update_task(task_prev.id, task_model)
    assert task_updated.id == task_id_prev
    assert task_updated.name == "Task name after"
    assert task_updated.description == "Description after"
    assert task_updated.deadline == datetime.date(2026,11,11)
    assert task_updated.priority == 1
    assert task_updated.list_name == list_name
    assert task_updated.completed == completed
    assert task_updated == st.dict_tasks[task_prev.id]

@pytest.mark.parametrize("expected_data", [
                                    {"deadline": datetime.date(2000,1,1)},
                                    {"deadline" : None},       
                                    {"priority": 100},
                                    {"description": "new decription"},
                                    {"description": None}
                                    ])
def test_update_task_1_attribute(expected_data, sample_task_model):
    task_model_prv = sample_task_model(name= "Task name before",
                                    description = "Description before",
                                    deadline = datetime.date(2025,10,10),
                                    priority = 0,
                                )
    task = ts.create_task(task_model_prv, list_name = None)
    task_aft = ts.update_task(task_id=task.id,
                                    task_model = sample_task_model(name = "Task name before", **expected_data))
    non_tested_attr = {"name", "description", "deadline", "priority"}
    for attr, value in expected_data.items():
        assert getattr(task_aft, attr) == value
        non_tested_attr.remove(attr)
    
    for attr in non_tested_attr:
        assert getattr(task_aft, attr) == getattr(task_model_prv, attr)
    

def test_update_task_non_existing_task_id(sample_task, sample_task_model_basic):
    task = sample_task("Tâche")
    task_model = sample_task_model_basic
    with pytest.raises(ValueError):
        ts.update_task(task_id=10, task_model=task_model)

def test_update_task_invalid_task_id(sample_task, sample_task_model_basic):
    task = sample_task("Tâche")
    task_model = sample_task_model_basic
    with pytest.raises(ValueError):
        ts.update_task(task_id="wrong_task_id", task_model=task_model)

def test_update_task_invalid_task_model(sample_task, sample_task_model_basic):
    task = sample_task("Tâche")
    task_model = sample_task_model_basic
    with pytest.raises(ValueError):
        ts.update_task(task_id=task.id, task_model=7)
