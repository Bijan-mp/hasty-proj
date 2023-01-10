# Table of Content
---
- [Table of Content](#table-of-content)
- [TL;DR](#tldr)
- [Project Parts and Services](#project-parts-and-services)
- [Build and Deploy in Development](#build-and-deploy-in-development)
  - [Build The Project](#build-the-project)
  - [Run The Project](#run-the-project)
  - [Build and run The Project](#build-and-run-the-project)
  - [Stop The Running Project](#stop-the-running-project)
  - [Stop The Running Project and remove containers volumes](#stop-the-running-project-and-remove-containers-volumes)
  - [Test The Project](#test-the-project)
- [Web Application EndPoints](#web-application-endpoints)
- [Database explenation](#database-explenation)
    - [Schema](#schema)
      - [Job](#job)
- [The Logic Behind the Service](#the-logic-behind-the-service)
    - [Steps](#steps)
    - [Rate limiter logic](#rate-limiter-logic)
- [Test](#test)

# TL;DR
---
1. Go to the project folder using command line and run below command.
> **NOTE** It takes about 30 seconds for the services to be ready.
```
make build-run
```
2. Go to `http://127.0.0.1:8080/` in your browser to send jobs to the service and get jobs details.
3. Go to `http://127.0.0.1:8899/` in your browser to see Celery task monitoring dashboard.

# Project Parts and Services
---
The project has these separated parts:
- `webapp` server
- `workerapp` server (That is a Celery instance)
- `Redis` server
- `Postgresql` server
- `Flower` server (As a dashboard for monitoring the Celery server)
> **NOTE** As each part of the application is a separate service we can scale each out separately easily.

# Build and Deploy in Development
---
## Build The Project
```
make build
```

## Run The Project
```
make run
```

## Build and run The Project
```
make build-run
```

## Stop The Running Project
```
make stop
```

## Stop The Running Project and remove containers volumes
```
make stop-and-remove-volumes:
```

## Test The Project
```
make build-and-test
```


# Web Application EndPoints
---
```
/               
    - Description:      Webbapp user dashboard address to add new job and get jobs by id.
    - HTTP Methd:       GET

/jobs        
    - Description:      To send an object id and start a new job.
    - HTTP Methd:       POST
    - content-type:     application/json

/jobs/{job_id}  
    - Description:      To get details of a job by its id.
    - HTTP Methd:       GET

```

# Database explenation
---
This project uses PostgreSQL as its database and SQLalchemy as ORM.
> **NOTE:** Based on the challenge document to avoid complexity, the project just has one table that stores the jobs data.

### Schema
#### Job
The `jobs` table holds data about the jobs.
* `id`: Integer Primary key 
* `object_id`:  Integer
* `duration`:   Integer (Duration of job processing)
* `timestamp`:  Integet (UNIX base timestamp that fill automatically at inserting record)
* `status`:     String  



# The Logic Behind the Service
### Steps
1. The user sends an object id using the HTTP post method to the web application
2. The endpoint gets the last job that has the same object id.
3. If there is any job, the system calculates the delay number for the new task based on the length of the time window and the last job timestamp.
4. The endpoint inserts a job record into the `'jobs'` table and set its status to `'PENDING'`.
5. The endpoint sends a task and its delay number to a Cellery task using (In the backend the job data send to the celery message broker that is Redis in this project)
6. The endpoint sends the created job data back to the user.
7. The message broker publishes the task to the worker
8. The worker receives the task and waits for the received delay number second. The worker updates the status of the task to the `'PROCESSING'` and processes the task after the delay time is finished.
9. The worker updates the status of the task to `'SUCCESS'` or `'FAILED'` based on the process result.

### Rate limiter logic
In this project, the rate-limiting logic is implemented in these steps:
1. Get the last job with the same object id
2. If the difference between the last job time stamp and now is more than 5 minutes the job runs immediately.
3. If the difference between the last job time stamp  and now is less than 5 minutes, the job waits until the end of the time window and runs immediately after it.

> **_NOTE:_**  Also we can send warning to the user if the last job creation is less that 5 minutes ago, and pass the responsibility of handling it to the user.

# Test 
The tests are in `webapp/main_test.py`