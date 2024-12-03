from dataclasses import dataclass

@dataclass(frozen=True)
class Task:
    id: int
    name: str
    description: str
    deadline: str
    assigned: list
    todo: bool

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


@dataclass(frozen=True)
class TaskWithGroup:
    group_id: int
    task_id: int
    name: str
    description: str
    deadline: str
    assigned: list
    todo: bool

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

@dataclass(frozen=True)
class Group:
    id: int
    name: str