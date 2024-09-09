from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

class CronJob(BaseModel):
    minute: str
    hour: str
    day_of_month: str
    month: str
    day_of_week: str
    command: str

def create_cron(job: CronJob) -> dict:
    cron_command = f"{job.minute} {job.hour} {job.day_of_month} {job.month} {job.day_of_week} {job.command}"
    try:
        subprocess.run(f'(crontab -l; echo "{cron_command}") | crontab -', shell=True, check=True)
        return {"status": "success", "message": "Cron job created successfully"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to create cron job: {e}")

def delete_cron(command: str) -> dict:
    try:
        cron_jobs = subprocess.check_output('crontab -l', shell=True).decode().splitlines()
        new_cron_jobs = [job for job in cron_jobs if command not in job]
        subprocess.run('crontab -r', shell=True, check=True)
        for job in new_cron_jobs:
            subprocess.run(f'(crontab -l; echo "{job}") | crontab -', shell=True, check=True)
        return {"status": "success", "message": "Cron job deleted successfully"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete cron job: {e}")

def list_crons() -> list:
    try:
        cron_jobs = subprocess.check_output('crontab -l', shell=True).decode().splitlines()
        return cron_jobs
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Failed to list cron jobs: {e}")

@app.post("/create_cron")
def create_cron_endpoint(job: CronJob):
    return create_cron(job)

@app.delete("/delete_cron")
def delete_cron_endpoint(command: str):
    return delete_cron(command)

@app.get("/list_crons")
def list_crons_endpoint():
    return list_crons()
