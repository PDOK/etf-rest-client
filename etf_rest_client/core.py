import json
import os
import time
import uuid
from datetime import datetime

import requests

BASE_URL = "http://inspire.ec.europa.eu/validator"


POLLING_WAIT_TIME = 2
TESTS = {"ATOM": {
            "id": "EID11571c92-3940-4f42-a6cd-5e2b1c6f4d93",
            "title": " Conformance Class: Download Service - Pre-defined Atom"
            },
         "ISO19139": {
             "id": "EID59692c11-df86-49ad-be7f-94a1e1ddd8da",
             "title": "Common Requirements for ISO/TC 19139:2007 \
             based INSPIRE metadata records"
            },
         "WMS": {
             "id":  "EIDeec9d674-d94b-4d8d-b744-1309c6cae1d2",
             "title": "Conformance Class: View Service - WMS"
            }}


def create_test_run(test_type, payload):
    test_uuid = TESTS[test_type]["id"]
    uuid_string = str(uuid.uuid4())
    timestamp = str(datetime.now()).split('.')[0]
    body = {}
    body = {
        "label": f"PDOK - {uuid_string} - {timestamp}",
        "executableTestSuiteIds": [test_uuid],
        "arguments": {
            "files_to_test": ".*",
            "tests_to_execute": ".*"
        },
        "testObject": {
            "resources": {
            }
        }
    }
    body["testObject"]["resources"] = payload
    url = f"{BASE_URL}/v2/TestRuns"
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
    return bool(data["max"] == data["val"])


def get_resource(path):
    url = f"{BASE_URL}/{path}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"FAILED TO GET RESOURCE: {url}")
    data = response.content
    return data


def validate_atom(url, output_folder, validator_url=""):
    if validator_url:
        global BASE_URL
        BASE_URL = validator_url
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
    result_html = get_resource(f"/v2/TestRuns/{test_run_id}.html").\
        decode("utf-8")
    status = result_json["EtfItemCollection"]["testRuns"]["TestRun"]["status"]
    valid = bool(status == "PASSED")
    html_path = os.path.join(output_folder, f"{test_run_id}.html")

    with open(html_path, "w") as html_file:
        html_file.write(result_html)
    result = {}
    result["valid"] = valid
    result["html_path"] = html_path
    result["etf_test_id"] = TESTS["ATOM"]["id"]
    result["etf_test_label"] = TESTS["ATOM"]["title"]
    return result
