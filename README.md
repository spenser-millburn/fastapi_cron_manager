# Cron Manager

This project provides a command-line interface (CLI) and a REST API to manage cron jobs on a Linux/Ubuntu system.

## Requirements

- Python 3.7+
- FastAPI
- Typer
- Uvicorn

## Installation

1. Clone the repository:
   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### CLI

- Start the server:
  ```
  python cli.py start
  ```

- Create a cron job:
  ```
  python cli.py create --command "<command>" --schedule "<schedule>"
  ```

- Delete a cron job:
  ```
  python cli.py delete --command "<command>"
  ```

- List all cron jobs:
  ```
  python cli.py list
  ```

### API

- Start the server:
  ```
  uvicorn app:app --reload
  ```

- Create a cron job:
  ```
  POST /create_cron
  {
    "minute": "*",
    "hour": "*",
    "day_of_month": "*",
    "month": "*",
    "day_of_week": "*",
    "command": "<command>"
  }
  ```

- Delete a cron job:
  ```
  DELETE /delete_cron?command=<command>
  ```

- List all cron jobs:
  ```
  GET /list_crons
  ```
