from typing import Set, TYPE_CHECKING

if TYPE_CHECKING:
    from models import Task
    from models import TaskList

dict_tasks: dict[int, "Task"] = {}
dict_tasks_lists :dict[str, "TaskList"] = {}
set_completed_tasks : Set[int] = set()
set_ongoing_tasks : Set[int] = set()

next_id = 0
def get_new_id() -> int:
    global next_id
    next_id+= 1
    return next_id