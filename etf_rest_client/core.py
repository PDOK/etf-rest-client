import os
import json
import requests
import io
import uuid
import time
from datetime import datetime

BASE_URL = "http://inspire.ec.europa.eu/validator"
POLLING_WAIT_TIME = 2

def create_test_run(test_type, payload):
    types = {"ATOM": "EID11571c92-3940-4f42-a6cd-5e2b1c6f4d93", "ISO19139": "EID59692c11-df86-49ad-be7f-94a1e1ddd8da", "WMS": "EIDeec9d674-d94b-4d8d-b744-1309c6cae1d2"}
    test_uuid = types[test_type]
    uuid_string = str(uuid.uuid4())
    timestamp = str(datetime.now()).split('.')[0]
    body = {
        "label": f"PDOK - {uuid_string} - {timestamp}",
        "executableTestSuiteIds": [test_uuid],
        "arguments": {
            "files_to_test": ".*",
            "tests_to_execute": ".*"
        },
        "testObject": {
            "resources":{
            }
        }
    }
    body["testObject"]["resources"] = payload
    print(json.dumps(body, indent=4))

    url = f"{BASE_URL}/v2/TestRuns"
    print(url)
    response = requests.post(url, json=body)
    if response.status_code != 201:
        raise Exception("FAILED TO CREATE TESTRUN")
    return response.json()

def test_run_completed(testrun_id):
    url = f"{BASE_URL}/v2/TestRuns/{testrun_id}/progress"
    response = requests.get(url)
    if response.status_code != 200: 
        raise Exception("FAILED TO CREATE TESTRUN")
    data = response.json()
    if data["max"] == data["val"]:
        return True
    else:
        return False

def get_resource(path):
    url = f"{BASE_URL}/{path}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"FAILED TO GET RESOURCE: {path}")
    data = response.content
    return data

def validate_atom(url, html_path):
    payload = {"serviceEndpoint": url}
    data = create_test_run("ATOM", payload)
    test_run_id = data["EtfItemCollection"]["testRuns"]["TestRun"]["id"]
    while True:
        if test_run_completed(test_run_id):
            break
        time.sleep(POLLING_WAIT_TIME)
    # retrieve json
    result_json = json.loads(get_resource(f"/v2/TestRuns/{test_run_id}.json"))
    # retrieve html
    result_html = get_resource(f"/v2/TestRuns/{test_run_id}.html").decode("utf-8")
    valid = result_json["EtfItemCollection"]["testRuns"]["TestRun"]["status"] == "PASSED"
    with open(f"{html_path}/{test_run_id}.html", "w") as html_file:
        html_file.write(result_html)
    with open(f"{html_path}/{test_run_id}.json", "w") as json_file:
        json_file.write(json.dumps(result_json, indent=4))
    return valid