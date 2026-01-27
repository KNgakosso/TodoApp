from dataclasses import dataclass, field
import datetime
from pydantic import BaseModel
from backend.utils import get_new_id

class TaskModel(BaseModel):
    name : str
    description : str | None = None
    deadline : datetime.date | None = None
    priority : int = 0

@dataclass
class Task:
    id : int = field(default_factory=get_new_id, init=False)
    name : str
    description : str | None = None
    deadline : datetime.date | None = None
    priority : int = 0
    completed : bool = False
    list_name : str | None = None

    @classmethod
    def from_model(cls, task_model : TaskModel):
        if not isinstance(task_model, TaskModel):
            raise ValueError
        return cls(
            name = task_model.name,
            description = task_model.description,
            deadline = task_model.deadline,
            priority = task_model.priority
        )

class TaskListModel(BaseModel):
    name : str

@dataclass
class TaskList:
    name : str
    tasks : set = field(default_factory=set)
    @classmethod
    def from_model(cls, task_list_model : TaskListModel):
        if not isinstance(task_list_model, TaskListModel):
            raise ValueError
        return cls(
            name = task_list_model.name
        )