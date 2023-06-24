#%%
import base64
import requests 

#%%

client_id = "iYEN4kSTupiZ6vFzjef7tFCrGOBqlRTwJ4k9k9Ze"
secret = "Ri9kOUAAdYMzp4uDlmuh6X3S2QmQLaHgefOLhudmbL4BBelDqh630Hugf9ddF5FNWjKpBZ3oZxYbO8Hz61ZPHF9bCB2yztlhMH0ervalG7KppKbafblAmFgA4brouFkw"
credential = "{0}:{1}".format(client_id, secret)
credential = base64.b64encode(credential.encode("utf-8"))
#%%

url = "http://127.0.0.1:8000/o/token/"
headers = {
    "Authorization": b"Basic " + credential,
    "Cache-Control": "no-cache",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials"
}
#%

response = requests.post(url, headers=headers, data=data)
#%%

response_data = response.json()
response_data
#%%

# get jobs
endpoint = "http://localhost:8000"
access_token = response_data["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json"
}
url = f"{endpoint}/jobs"
response = requests.get(url, headers=headers)
#%%
response.json()

#%%

url = f"{endpoint}/api/hello"
response = requests.get(url, headers=headers)
response.content

#%%
# # request task from a pending job

url = f"{endpoint}/tasks/request_task/"
response = requests.get(url, headers=headers)
response.json()

# import the main function from the job and run it passing the task id

# post the result to the server

# %%
