import os
import time
import traceback
from fastapi import FastAPI, Body, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from celery import Celery

from db.database import SessionLocal, engine
from db import crud, models


RATE_LIMIT_TIME_WINDOW = int(os.environ.get("rate_limit_time_window", 5*60))

# Database & ORM
models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Fast API
app = FastAPI()
app.mount("/static", StaticFiles(directory="src/webapp/static"), name="static")
templates = Jinja2Templates(directory="src/webapp/templates")

# Celery
celery = Celery("job_worker")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.get("/jobs/{job_id}")
def get_status(job_id, db: Session = Depends(get_db)):
    try:
        job = crud.get_job_by_id(db, int(job_id))
        job = {
            "id": job.id,
            "object_id": job.object_id,
            "duration": job.duration,
            "timestamp": job.timestamp,
            "status": job.status,
        }
        return JSONResponse(job)
    except Exception:
        print(f"ERROR: {traceback.format_exc()}")
        return HTTPException(status_code=500)


@app.post("/jobs", status_code=201)
def post_job(payload=Body(...), db: Session = Depends(get_db)):
    try:
        last_job = crud.get_last_job_by_object_id(db, payload["object_id"])

        # The rait limiter delay calculation
        rate_limiter_delay = 0
        if last_job:
            now = round(time.time())
            time_delta = RATE_LIMIT_TIME_WINDOW - (now - last_job.timestamp)
            rate_limiter_delay = max(time_delta, 0)

        # Create Job in DB
        job_data = {
            "object_id": payload["object_id"],
            "timestamp": round(time.time()),
        }
        job = crud.create_job(db, job_data)

        # Send Job to the Celery
        celery.send_task('startJob', (rate_limiter_delay, {"job_id": job.id}))

        return JSONResponse({"job_id": job.id})

    except Exception as e:
        print(f"ERROR: {traceback.format_exc()}")
        return HTTPException(status_code=500)
