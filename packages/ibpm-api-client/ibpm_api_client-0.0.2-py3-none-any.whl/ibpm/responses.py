
class ibpmResponse:
    def __init__(self, result, message):
        self.result = result
        self.message = message


class createNewProcessResponse(ibpmResponse):
    def __init__(self, result, message, documentName, instanceId):
        super().__init__(result, message)
        self.documentName = documentName
        self.instanceId = instanceId

class getProcessResponse(ibpmResponse):
    def __init__(self, result, message, model, documentName, documentDescription, instanceId, activeTasks, links, variables, state, graph):
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