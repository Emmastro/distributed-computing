import json
import requests
import importlib
import time
import logging

logging.basicConfig(level=logging.INFO)

endpoint = "http://127.0.0.1:8000"
# test access token
access_token = "f0e1df66ee254bc5bb141e8033bf6e82687554ed"

HEADERS = {
    "Authorization": f"Token {access_token}",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json"
}


def request_pending_task():
    url = f"{endpoint}/tasks/request_task/"
    response = requests.get(url, headers=HEADERS)
    new_task = response.json()
    return new_task


def get_job_file(new_task):

    headers = {
        **HEADERS,
        "Content-Type": "text/plain"
    }
    url = f"{endpoint}/jobs/{new_task['job']}/get_job_file/"
    response = requests.get(url, headers=headers)
    filename = f"job_{new_task['job']}_{new_task['task_id']}"

    open(f"jobs/{filename}.py", "wb").write(response.content)
    return filename


def run_job(filename, new_task):

    module = importlib.import_module(f"jobs.{filename}")

    # update task to started
    url = f"{endpoint}/tasks/{new_task['id']}/"
    data = {
        "status": "running"
    }
    response = requests.patch(url, headers=HEADERS, data=json.dumps(data))

    try:
        result = module.main(new_task['task_id'])
        data = {
            "result": str(result),
            "status": "finished"
        }
        logging.info(f"Task {new_task['task_id']} finished")
    except Exception as e:
        data = {
            "result": str(e),
            "status": "failed"
        }
        logging.error(f"Task {new_task['task_id']} failed")

    response = requests.patch(url, headers=HEADERS, data=json.dumps(data))

    return response.json()


def mainloop():

    while 1:
        new_task = request_pending_task()

        if new_task.get("message", False) == 'no jobs available':
            logging.info("No new tasks, sleeping for 5 seconds")
            time.sleep(5)
        else:
            filename = get_job_file(new_task)
            run_job(filename, new_task)


if __name__ == "__main__":
    mainloop()
