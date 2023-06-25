import requests 
import importlib
import time

endpoint = "http://localhost:8000"
access_token = "f0e1df66ee254bc5bb141e8033bf6e82687554ed"
headers = {
    "Authorization": f"Token {access_token}",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json"
}

def request_pending_task():
    url = f"{endpoint}/tasks/request_task/"
    response = requests.get(url, headers=headers)
    new_task = response.json()
    return new_task

def get_job_file(new_task):
    headers = {
    "Authorization": f"Token {access_token}",
    "Cache-Control": "no-cache",
    "Content-Type": "text/plain"
    }
    url = f"{endpoint}/jobs/{new_task['job']}/get_job_file/"
    response = requests.get(url, headers=headers)
    filename = f"job_{new_task['job']}_{new_task['task_id']}"

    open(f"jobs/{filename}.py", "wb").write(response.content)
    return filename


def run_job(filename, new_task):
    # import the main function from the job and run it passing the task id
    module = importlib.import_module(f"jobs.{filename}")
    print(module)

    # update task to started
    url = f"{endpoint}/tasks/{new_task['id']}/"
    data = {
        "status": "started"
    }
    response = requests.patch(url, headers=headers, data=data)
    
    try:
        result = module.main(new_task['task_id'])
        data = {
        "result": result,
        "status": "finished"
        }
    except Exception as e:
        data = {
        "result": str(e),
        "status": "failed"
        }

    response = requests.post(url, headers=headers, data=data)

    return response.json()

JOB_FOUND_STATUS_CODE = 1

def mainloop():
    while 1:
        new_task = request_pending_task()
        # TODO: add status code on task response
        if hasattr(new_task, "message") and new_task['message'] == 'no jobs available':
            filename = get_job_file(new_task)
            run_job(filename, new_task)
        else:
            print("No new tasks, sleeping for 5 seconds")
            time.sleep(5)


if __name__ == "__main__":
    mainloop()