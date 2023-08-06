from typing import List

class IbpmResponse:
    def __init__(self, result, message):
        self.result = result
        self.message = message


class CreateNewProcessResponse(IbpmResponse):
    def __init__(self, result, message, documentName, instanceId):
        super().__init__(result, message)
        self.documentName = documentName
        self.instanceId = instanceId

class User:
    def __init__(self, userName):
        self.userName = userName

    def __str__(self):
        return self.userName

class Task:
    def __init__(self, activity, activityDescription, userName, assignedUsers: List[User]):
        self.activity = activity
        self.activityDescription = activityDescription
        self.userName = userName
        self.assignedUsers = assignedUsers

    def __str__(self):
        return self.activityDescription

class LinkedProcess:
    def __init__(self, model, documentName, documentDescription, instanceId):
        self.model = model
        self.documentName = documentName
        self.documentDescription = documentDescription
        self.instanceId = instanceId

    def __str__(self):
        return f"{self.model}:{self.documentName}"

class GetProcessResponse(IbpmResponse):
    def __init__(self, result, message, model, documentName, documentDescription, instanceId, activeTasks: List[Task], links: List[LinkedProcess], variables, state, graph):
        super().__init__(result, message)
        self.model = model
        self.documentName = documentName
        self.documentDescription = documentDescription
        self.instanceId = instanceId
        self.activeTasks = activeTasks
        self.links = links
        self.variables = variables
        self.state = state
        self.graph = graph

    def __str__(self):
        return f"{self.model}:{self.documentName} @ {self.activeTasks[0].activityDescription}"