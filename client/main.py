#%%
import requests 
import importlib

endpoint = "http://localhost:8000"
access_token = "f0e1df66ee254bc5bb141e8033bf6e82687554ed"
headers = {
    "Authorization": f"Token {access_token}",
    # "Cache-Control": "no-cache",
    # "Content-Type": "application/json"
}
url = f"{endpoint}/jobs"
response = requests.get(url, headers=headers)
#%%
response.json()
#%%
# # request task from a pending job

url = f"{endpoint}/tasks/request_task/"
response = requests.get(url, headers=headers)
new_task = response.json()

#%%
# get job file for the task
headers = {
    "Authorization": f"Token {access_token}",
    "Cache-Control": "no-cache",
    "Content-Type": "text/plain"
}
url = f"{endpoint}/jobs/{new_task['job']}/get_job_file/"
response = requests.get(url, headers=headers)
filename = f"job_{new_task['job']}_{new_task['task_id']}"

open(f"jobs/{filename}.py", "wb").write(response.content)

# import the main function from the job and run it passing the task id

module = importlib.import_module(f"jobs.{filename}")
print(module)
result = module.main(new_task['task_id'])
result
# post the result to the server

# %%
