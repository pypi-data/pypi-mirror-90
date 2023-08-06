import requests
import jsons
import base64
import io
from PIL import Image
from .responses import *

class IbpmClient:

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.apiUrl = baseUrl + '/api/ext/'
        self.authorizationToken = ""
        self.userName = ""

    def _req(self, method, **kwargs):
        data = {
            "authenticationToken": self.authorizationToken,
            "userName": self.userName
        }
        
        for k,v in kwargs.items():
            if v != None:
                data[k]=v
        
        resp = requests.post(self.apiUrl + method, json = data)
        return resp.json()


    def createNewProcess(self, model, variables, startObject=None) -> CreateNewProcessResponse:
        resp = self._req("createNewProcess", model=model, variables=variables, startObject=startObject)
        return jsons.load(resp, CreateNewProcessResponse)

    def execTask(self, model=None, documentName=None, instanceId=None, activity=None, comments=None) -> IbpmResponse:
        resp = self._req("execTask", model=model, documentName=documentName, instanceId=instanceId, activity=activity, comments=comments)
        return jsons.load(resp, IbpmResponse)

    def updateProcess(self, model=None, documentName=None, instanceId=None, variables=None, resetGroups=None, state=None) -> IbpmResponse:
        resp = self._req("updateProcess", model=model, documentName=documentName, instanceId=instanceId, variables=variables, resetGroups=resetGroups, state=state)
        return jsons.load(resp, IbpmResponse)

    def getProcess(self, model=None, documentName=None, instanceId=None, includeVariables=None, includeGraph=None) -> Process:
        resp = self._req("getProcess", model=model, documentName=documentName, instanceId=instanceId, includeVariables=includeVariables, includeGraph=includeGraph)
        proc = jsons.load(resp, Process)

        #decode graph from png/base64 into PIL image
        if proc.graph != "" and proc.graph != None:
            img_bytes = base64.b64decode(proc.graph)
            img_buf = io.BytesIO(img_bytes)
            proc.graph = Image.open(img_buf)
        return proc

    def getSchema(self, modelName=None, activityName=None) -> Schema:
        resp = self._req("getSchema", modelName=modelName, activityName=activityName)
        schema = jsons.load(resp, Schema)
        return schema

    def getVersion(self):
        resp = self._req("getVersion") 
        return resp
        
