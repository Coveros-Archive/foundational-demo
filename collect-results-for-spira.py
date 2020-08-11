import requests
import json
import datetime
import os
import argparse

parser = argparse.ArgumentParser(description='Give build status')
parser.add_argument('-s', '--status', type=int, help="the build status. 1=failure, 2=success")
parser.add_argument('-m', '--message', type=str, help="any relevant message")

args = parser.parse_args()

message = args.message
status = args.status

CREATE_HOST = False

api_base = "https://coveros.spiraservice.net/services/v5_0/RestService.svc"
api_key = os.environ['API_TOKEN']
api_user = os.environ['API_USER']
# test_status = os.environ['TEST_STATUS']
# consider a switch for different tests

headers = {"username": api_user, "api-key": api_key}
# r = requests.get(url=f"{api_base}/projects?username=matthew.taylor", headers=headers)
# print(r.json())

#"starting_row": 1, "number_of_rows": 1
# params = {"TestCaseId": 35, "TestCaseStatusId": 0, "OwnerId": "matthew.taylor", "TestCaseTypeId": 0}
# r = requests.post(url = f"{api_base}/projects/10/test-cases", headers=headers, params=params)
# # print(r.request.headers)
# print(r.text)

# hits projects/{project_id}/test-runs/create?release_id={release_id}
# "Creates a new test run shell from the provided test case(s)"
# params = {"TestCaseId": 35, "TestCaseStatusId": 0, "OwnerId": "matthew.taylor", "TestCaseTypeId": 0}
# r = requests.post(url = f"{api_base}projects/10/test-runs/create?release_id=1.0.0.0", headers=headers)
# print(r.request.headers)
# print(r.text)

if CREATE_HOST:
# create an automation host. Onetime thing.
    payload = {"AutomationHostId": None, 
            "Name": "Jenkins",
            "Token": "jenkins",
            "Description": "test",
            "Active":"true"} 
    r2 = requests.post(url = f"{api_base}/projects/10/automation-hosts", headers=headers, json=payload)
    print(r2.text)

# payload = {"ConsiderTimes":"false",
#         "EndDate":None,
#         "StartDate":None}

# allegedly create a test run "shell" using provided host
# r3 = requests.post(url=f"{api_base}/projects/10/test-runs/create/automation_host/jenkins", headers=headers, json=payload)
# print(r3.text)
# print(r3.raw)
# print(r3.request.body)

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
r4 = requests.post(url=f"{api_base}/projects/10/test-runs/record", headers=headers, json=payload)
print(r4.text)
print(r4.request.body)
print(r4.raw)
# r4.