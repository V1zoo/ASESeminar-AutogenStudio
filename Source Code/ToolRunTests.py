import requests
import json
import os
import subprocess
import sys

def run_tests(index: int) -> str:
    API_URL = "http://localhost:8081/task/index/"
    try:
        tokens= -1
        api_url = f"{API_URL}{index}"
        start_dir = os.getcwd()
        repo_dir = os.path.join(start_dir, f"repos\\repo_{index}")
        LOG_FILE = start_dir + "\\AGSLog.txt"
        responseJSON = requests.get(api_url,timeout=10).json()
        taskNumber = responseJSON['taskNumber']
        instance_id = responseJSON['instance_id']
        prompt = responseJSON["Problem_statement"]
        git_clone = responseJSON["git_clone"]
        fail_to_pass = json.loads(responseJSON.get("FAIL_TO_PASS","[]"))
        pass_to_pass = json.loads(responseJSON.get("PASS_TO_PASS","[]"))
        test_payload = {
            "instance_id": instance_id, # type: ignore
            "repoDir" : f"/repos/repo_{index}",
            "FAIL_TO_PASS" : fail_to_pass, # type: ignore
            "PASS_TO_PASS" : pass_to_pass, # type: ignore
            }
        result = requests.post("http://localhost:8082/test", json=test_payload)
        result.raise_for_status()
        if len(result.json()) == 1:
            os.chdir(start_dir)
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"\n---< TESTCASE {index} >------------")
                log.write(f"\nFailed to make any changes to the repository or")
                log.write("\nencountered errors during evaluation")
                log.write(f"\nTotal Tokens used: {tokens}")
            print(f"Test case {index} unchanged and logged")
        else:
            result_raw = result.json().get("harnessOutput", "{}")
            result_json = json.loads(result_raw)
            if not result_json:
                print(f"BenchResponseError: {result.json().get("error")}")
                raise ValueError(f"No data in harnessOutput - possible evaluation error\nTotal Tokens used: {tokens}")
            print(result_json)
            instance_id = next(iter(result_json))
            tests_status = result_json[instance_id]["tests_status"]
            fail_pass_results = tests_status["FAIL_TO_PASS"]
            fail_pass_passed = len(fail_pass_results["success"])
            fail_pass_total = fail_pass_passed + len(fail_pass_results["failure"])
            pass_pass_results = tests_status["PASS_TO_PASS"]
            pass_pass_passed = len(pass_pass_results["success"])
            pass_pass_total = pass_pass_passed + len(pass_pass_results["failure"])

                # log results
            os.chdir(start_dir)
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"\n---< TESTCASE {index} >------------")
                log.write(f"\nFAIL_TO_PASS passed: {fail_pass_passed}/{fail_pass_total}")
                log.write(f"\nPASS_TO_PASS passed: {pass_pass_passed}/{pass_pass_total}")
                log.write(f"\nTotal Tokens used: {tokens}")
            print(f"Test case {index} completed and logged")
        return "TERMINATE"
    except Exception as e:
        os.chdir(start_dir)
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"\n---< TESTCASE {index} >------------")
            log.write(f"\nError: {e}")
        print(f"Error in test case {index}: {e}")
        return f"Error: {str(e)}"
