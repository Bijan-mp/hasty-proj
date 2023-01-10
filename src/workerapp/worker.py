import os
import time
import random

from celery import Celery
from sqlalchemy.orm import Session

from db import crud
from db.database import engine

TASK_TIME_LIMIT = int(os.environ.get("TASK_TIME_LIMIT",60))

# Celery
celery = Celery("job_worker")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")

@celery.task(time_limit=TASK_TIME_LIMIT)
def job(rate_limiting_delay, job_data):
    
    # Wait until the end of time window
    time.sleep(rate_limiting_delay)

    # Update job status in DB
    with Session(engine) as session:
        job_update_obj = {"status": "PROCESSING"}
        crud.update_job(session, job_data["job_id"], job_update_obj)

    try:
        job_duration = random.randint(15, 45) 
        time.sleep(job_duration)
        status = "SUCCESS"
    except Exception as e:
        status = "FAILED"
        
    # Update job status and duration in DB
    with Session(engine) as session:
        job_update_obj = {
            "duration":job_duration,
            "status": status
        }
        crud.update_job(session, job_data["job_id"], job_update_obj)

    return True

@celery.task(name='startJob')
def start_job(rate_limiting_delay, job_data):
    job.apply_async((rate_limiting_delay, job_data))
    return True

   
   