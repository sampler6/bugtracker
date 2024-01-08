from enum import Enum


class TaskType(str, Enum):
    Bug = "Bug"
    Task = "Task"


class Status(str, Enum):
    """Statuses of tasks"""
    To_do = 'To do'
    In_progress = 'In progress'
    Code_review = 'Code review'
    Dev_test = 'Dev test'
    Testing = 'Testing'
    Done = 'Done'
    Wontfix = 'Wontfix'


next_status_dict = {
    Status.To_do: Status.In_progress,
    Status.In_progress: Status.Code_review,
    Status.Code_review: Status.Dev_test,
    Status.Dev_test: Status.Testing,
    Status.Testing: Status.Done,
    Status.Done: Status.Done,
    Status.Wontfix: Status.Done
}


class StatusNext(str, Enum):
    """Used for changing the status in order"""
    Next = "Next"
    To_do = "To_Do"
    Wontfix = "Wontfix"


class Roles(str, Enum):
    Manager = "Manager"
    Team_lead = "Team lead"
    Developer = "Developer"
    QA = "QA Engineer"


class Priority(str, Enum):
    Critical = "Critical"
    High = "High"
    Medium = "Medium"
    Low = "Low"


class TaskFields(str, Enum):
    type = "type"
    priority = "priority"
    status = "status"
    header = "header"
    description = "description"
    executor = "executor"
    creator = "creator"
