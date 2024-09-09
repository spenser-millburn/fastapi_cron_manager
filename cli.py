import typer
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
cli = typer.Typer()

class CronJob(BaseModel):
    minute: str
    hour: str
    day_of_month: str
    month: str
    day_of_week: str
    command: str

def start_server() -> None:
    subprocess.run(["uvicorn", "app:app", "--reload"])

def create_cron(command: str, schedule: str) -> None:
    cron_command = f"{schedule} {command}"
    try:
        subprocess.run(f'(crontab -l; echo "{cron_command}") | crontab -', shell=True, check=True)
        print("Cron job created successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create cron job: {e}")

def delete_cron(command: str) -> None:
    try:
        cron_jobs = subprocess.check_output('crontab -l', shell=True).decode().splitlines()
        new_cron_jobs = [job for job in cron_jobs if command not in job]
        subprocess.run('crontab -r', shell=True, check=True)
        for job in new_cron_jobs:
            subprocess.run(f'(crontab -l; echo "{job}") | crontab -', shell=True, check=True)
        print("Cron job deleted successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to delete cron job: {e}")

def list_crons() -> None:
    try:
        cron_jobs = subprocess.check_output('crontab -l', shell=True).decode().splitlines()
        for job in cron_jobs:
            print(job)
    except subprocess.CalledProcessError as e:
        print(f"Failed to list cron jobs: {e}")

@cli.command()
def start() -> None:
    start_server()

@cli.command()
def create(command: str, schedule: str) -> None:
    create_cron(command, schedule)

@cli.command()
def delete(command: str) -> None:
    delete_cron(command)

@cli.command()
def list() -> None:
    list_crons()

if __name__ == "__main__":
    cli()

@app.post("/create_cron")
def create_cron_endpoint(job: CronJob):
    return create_cron(job.command, f"{job.minute} {job.hour} {job.day_of_month} {job.month} {job.day_of_week}")

@app.delete("/delete_cron")
def delete_cron_endpoint(command: str):
    return delete_cron(command)

@app.get("/list_crons")
def list_crons_endpoint():
    return list_crons()
