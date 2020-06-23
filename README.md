# Task Executor Service

Task Executor Service for ROSA system.

Master status: ![](https://github.com/RSOA-WEITI-2020/TaskExecutor/workflows/Tests/badge.svg?branch=master)  
Develop status: ![](https://github.com/RSOA-WEITI-2020/TaskExecutor/workflows/Tests/badge.svg?branch=develop)

To start app locally:

- run `poetry install`
- run `poetry shell`
- run `cd app && python main.py`

## Available endpoints

### `/v1/register`

Used to register

Params (`x-www-form-url-encoded`):

- `username`
- `password`
- `email`
