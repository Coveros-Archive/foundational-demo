import requests
import json
import datetime
import os
import argparse

parser = argparse.ArgumentParser(description='Give build status')
parser.add_argument('-s', '--status', type=int, help="the build status. 1=failure, 2=success")
parser.add_argument('-m', '--message', type=str, help="any relevant message")
parser.add_argument('-t', '--token', type=str, help="SpiraPlan API token")
parser.add_argument('-u', '--user', type=str, help="SpiraPlan API user")
args = parser.parse_args()

message = args.message
status = args.status
api_key = args.token
api_user = args.user

CREATE_HOST = False

api_base = "https://coveros.spiraservice.net/services/v5_0/RestService.svc"

headers = {"username": api_user, "api-key": api_key}

if CREATE_HOST:
# create an automation host. Onetime thing.
    payload = {"AutomationHostId": None, 
            "Name": "Jenkins",
            "Token": "jenkins",
            "Description": "test",
            "Active":"true"} 
    r2 = requests.post(url = f"{api_base}/projects/10/automation-hosts", headers=headers, json=payload)
    print(r2.text)

# several of these fields seem like they must be set to 1 to avoid the notorious:
# "EntityForeignKeyException: Database foreign key violation occurred"
payload = {
    "ArtifactTypeId":1,
    "ConcurrencyDate":"/Date({})/".format(round(datetime.datetime.now().timestamp())),
    "ExecutionStatusId":status, # 1 = fail, 2 = pass, 0 = BREAKS IT
    "StartDate":"/Date({})/".format(round(datetime.datetime.now().timestamp())),
    "TestCaseId":35,
    "TestRunTypeId":1,
    "TestRunFormatId":0,
    "RunnerName":"jenkins",
    "AutomationHostId": 7, # set equal to ID found for jenkins under 'Automation Hosts' in Spira instance
    "RunnerStackTrace": "Foo",
    "RunnerTestName": "Bar",
    "RunnerMessage": message}

# hit projects/{project_id}/test-runs/record
# "Records the results of executing an automated test"
r = requests.post(url=f"{api_base}/projects/10/test-runs/record", headers=headers, json=payload)
print(r.text)
print(r.request.body)
print(r.raw)