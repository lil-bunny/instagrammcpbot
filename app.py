


from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

from cronjob import MyScheduler
from bottask import get_comments, get_post_data

from helper import  do_task_exist, get_task_history, reset_task, set_post_url, set_task
import os

from fastapi.middleware.cors import CORSMiddleware




app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


myscheduler=MyScheduler()





class TaskRequest(BaseModel):
    post_url:str
    time: int  # time in minutes


class UserDetails(BaseModel):
    username:str
    password:str
    
@app.post("/connect_instagram")
def connect_instagram(payload: UserDetails):
    env_path = Path("./.env")

    # Check if .env exists, create if not
    if not env_path.exists():
        env_path.touch()
        print(".env file created.")

    # Basic checks
    if not payload.username or not payload.password:
        return {"status": False, "message": "Username and password cannot be empty"}

    # Write or update the .env file
    def update_env_file(key: str, value: str):
        lines = []
        if env_path.exists():
            with open(env_path, "r") as file:
                lines = file.readlines()

        found = False
        for i, line in enumerate(lines):
            if line.startswith(key + "="):
                lines[i] = f"{key}={value}\n"
                found = True
                break
        if not found:
            lines.append(f"{key}={value}\n")

        with open(env_path, "w") as file:
            file.writelines(lines)

    # Update environment file and current process env
    update_env_file("INSTAGRAM_USERNAME", payload.username)
    update_env_file("INSTAGRAM_PASSWORD", payload.password)
    os.environ["INSTAGRAM_USERNAME"] = payload.username
    os.environ["INSTAGRAM_PASSWORD"] = payload.password

    return {"status": True, "message": "Instagram account connected"}
    



@app.post('/pause_task')
def pause_task():
    myscheduler.pause_job()
    print("task paused")

@app.post('/get_work_history')
def get_work_history():
    return get_task_history()

@app.post('/stop_task')
def stoptask():
  
    reset_task()
    myscheduler.stop_scheduler()
    return {"status":1,"message":"Task stopped"}
@app.post('/start_task')
async def create_task(payload: TaskRequest):
    set_post_url(post_url= payload.post_url)
    if not do_task_exist():
        set_task(task_id="mytask")
        await get_post_data()
        # Correct: pass function + kwargs
        myscheduler.add_job(
            task=get_comments,
            
            
            job_id="mytask_job",
           
        )
    
        
  
        
        return {"status": 1, "message": "Task created"}
    else:
        return {"status": 0, "message": "Task already present"}
    

@app.on_event("startup")
async def start_scheduler():
    myscheduler.start_job()














