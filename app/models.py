from dataclasses import dataclass

@dataclass
class Task:
    id: int
    name: str
    description: str
    deadline: str
    assigned: list[str]
    todo: bool


@dataclass
class Group:
    id: int
    name: str