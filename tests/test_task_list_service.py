import src.task_service as ts
import src.storage as st
import pytest
import datetime

# TEST CREATE TASKLIST
############################
def test_create_task_list_basic(sample_task_list_model):
    task_list = ts.create_task_list(task_list_model=sample_task_list_model("Liste"))
    
    assert len(st.dict_tasks_lists) == 1
    assert "Liste" in st.dict_tasks_lists.keys()
    assert st.dict_tasks_lists["Liste"] == task_list
    assert len(st.dict_tasks_lists["Liste"].tasks) == 0

def test_create_task_list_already_created(sample_task_list_model):
    task_list_1 = ts.create_task_list(task_list_model=sample_task_list_model("Liste"))
    
    with pytest.raises(ValueError):   
        task_list_2 = ts.create_task_list(task_list_model=sample_task_list_model("Liste"))

    assert len(st.dict_tasks_lists) == 1

def test_create_task_list_with_invalid_tasklist_model():
    with pytest.raises(ValueError):
        task_list = ts.create_task_list(task_list_model=7)

# TEST GET TASK LIST
#########################

def test_get_task_list_empty_list(sample_task_list):
    task_list = sample_task_list("Empty List")
    task_list = ts.get_task_list("Empty List")

    assert task_list.name == "Empty List"
    assert task_list == st.dict_tasks_lists["Empty List"]

def test_get_task_list_success(sample_basic_tasks_2):
    sample = sample_basic_tasks_2
    task_list = ts.get_task_list("Sport")

    assert task_list.name == "Sport"
    assert task_list == st.dict_tasks_lists["Sport"]

def test_get_task_list_non_existing(sample_basic_tasks_2):
    sample = sample_basic_tasks_2
    with pytest.raises(ValueError):
        task_list = ts.get_task_list("Projets")

def test_get_task_list_invalid_param(sample_basic_tasks_2):
    sample = sample_basic_tasks_2
    with pytest.raises(ValueError):
        task_list = ts.get_task_list(True)


# TEST GET TASK LISTS
##########################

def test_get_task_lists(sample_basic_tasks_2):
    sample = sample_basic_tasks_2
    result = ts.get_task_lists()
    assert result == st.dict_tasks_lists


def test_get_task_lists_no_lists(sample_task):
    task = sample_task("Tâche_1", description="Tâche sans liste", completed = True)
    task = sample_task("Tâche_2", description="Tâche sans liste")
    result = ts.get_task_lists()
    assert len(result) == 0

def test_get_task_lists_empty_dataset():
    result = ts.get_task_lists()
    assert result == st.dict_tasks


# TEST DELETE TASK LIST
###############################
def test_delete_task_list_no_tasks(sample_task_list):
    task_list_created = sample_task_list("Empty List")
    task_list_deleted = ts.delete_task_list("Empty List")

    assert len(st.dict_tasks) == 0
    assert len(st.dict_tasks_lists) == 0
    assert len(st.set_completed_tasks) == 0
    assert len(st.set_ongoing_tasks) == 0

    assert task_list_deleted == task_list_created

def test_delete_task_list_empty_list(sample_basic_tasks):
    sample = sample_basic_tasks
    task_list = ts.delete_task_list("Liste C")

    assert len(st.dict_tasks_lists) == 2
    assert not "Liste C" in st.dict_tasks_lists

    assert task_list.name == "Liste C"
    assert task_list.tasks == set()

def test_delete_task_lists_non_empty(sample_basic_tasks_2):
    sample = sample_basic_tasks_2
    task_list = ts.delete_task_list("Sport")

    assert len(st.dict_tasks_lists) == 2
    assert not "Sport" in st.dict_tasks_lists
    assert st.dict_tasks[1].list_name is None
    assert st.dict_tasks[2].list_name is None
    assert st.dict_tasks[3].list_name is None
    assert st.dict_tasks[4].list_name is None

    assert task_list.name == "Sport"
    assert task_list.tasks == {1, 2, 3, 4}

def test_delete_task_lists_non_existing(sample_basic_tasks_2):
    a = sample_basic_tasks_2
    with pytest.raises(ValueError):
        task_list = ts.delete_task_list("Projets")
    assert len(st.dict_tasks_lists) == 3