from typing import List, Dict, Optional, Any
from dataclasses import dataclass

@dataclass
class IbpmResponse:
    result: str
    message: Optional[str]


@dataclass
class CreateNewProcessResponse(IbpmResponse):
    documentName: str
    instanceId: str


@dataclass
class User:
    userName: str

    def __str__(self):
        return self.userName

@dataclass
class Task:
    activity: str
    activityDescription: str
    userName: str
    assignedUsers: Optional[List[User]]
    
    def __str__(self):
        return self.activityDescription


@dataclass
class LinkedProcess:
    model: str
    documentName: str
    documentDescription: str
    instanceId: str

    def __str__(self):
        return f"{self.model}:{self.documentName}"


@dataclass
class Process(IbpmResponse):
    #def __init__(self, result, message, model, documentName, documentDescription, instanceId, activeTasks: Optional[List[Task]], links: Optional[List[LinkedProcess]], variables, state, graph):
        
    model: str
    documentName: str
    documentDescription: str
    instanceId: str
    activeTasks: Optional[List[Task]]
    links: Optional[List[LinkedProcess]]
    variables: Optional[Dict]
    state = str
    graph: Any

    def __str__(self):
        return f"{self.model}:{self.documentName} @ {self.activeTasks[0].activityDescription}"


def boolNull(x) -> bool:
    if x is None:
        return False
    else:
        return x

@dataclass
class VariableBase:
    availableValues: Optional[List]
    propertyName: str
    propertyType: str
    variableType: Optional[str]
    description: str
    required: Optional[bool]
    readOnly: Optional[bool]
    hasDefault: Optional[bool]

    def __str__(self):
        return f'{self.propertyName}: {self.propertyType}'

        
@dataclass
class Variable(VariableBase):
    subProperties: Optional[List[VariableBase]]


@dataclass
class Schema(IbpmResponse):
    activity: str
    properties: Optional[List[Variable]]
