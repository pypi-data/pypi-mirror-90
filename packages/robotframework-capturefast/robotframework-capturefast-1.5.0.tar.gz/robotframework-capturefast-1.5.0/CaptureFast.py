import requests
import base64
import json
import time
import ntpath
import os
from RPA.Robocloud.Secrets import Secrets


class CaptureFastBase:
    accesstoken: str = None

    def _init_client(self):
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        secrets = Secrets()
        USER_NAME = secrets.get_secret("credentials")["username"]
        PASSWORD = secrets.get_secret("credentials")["password"]

        authRequest = {
            "username": USER_NAME,
            "password": PASSWORD,
            "grant_type": "password"
        }

        response = requests.request(
            "POST", "https://api.capturefast.com/token",
            headers=headers,
            data=authRequest
        )

        self.accesstoken = response.json().get('access_token')
        return self.accesstoken

    def GetAccessToken(self):
        return self.accesstoken
        
    def CaptureFastTest(self):
        return "CaptureFast is running..."

    def UploadDocument(self, filePath, documentTypeId):
        fileContent = ''
        with open(filePath, "rb") as f:
            fileContent = base64.b64encode(f.read()).decode('ascii')

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.accesstoken 
        }

        secrets = Secrets()
        teamid = secrets.get_secret("credentials")["teamid"]

        document = {
            'TeamId': teamid,
            'DocumentTypeId': documentTypeId,
            'Files': [{'FileName': os.path.basename(filePath),
                       'Content': fileContent}]
        }

        response = requests.request("POST",
                                    "https://api.capturefast.com/api/Upload/Document",
                                    headers=headers,
                                    data=json.dumps(document))

        return response.json().get('DocumentId')

    def GetDocumentData(self, documentId, timeoutInSeconds=100):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.accesstoken
        }

        jsonDoc = {}

        while(timeoutInSeconds > 0):
            timeoutInSeconds -= 5

            if(timeoutInSeconds < 0):
                raise Exception("Sorry, data is not available")
            
            response = requests.request("GET", "https://api.capturefast.com/api/Download/Data?documentId=" + str(documentId), headers= headers)

            jsonDoc = response.json()

            resultCode = jsonDoc['ResultCode']

            if(resultCode == 0):
                break
            elif(resultCode == 100):
                continue
            else:
                time.sleep(5)
                jsonDoc = self.GetDocumentData(documentId, timeoutInSeconds)
                break

        return jsonDoc


class DocService(CaptureFastBase):
    def __init__(self) -> None:
        self._init_client()


class CaptureFast(DocService):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "REST"

    def __init__(self):
        DocService.__init__(self)




