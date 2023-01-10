from sqlalchemy.orm import Session

from . import models

# Job CRUD
def create_job(db: Session, job):

    db_job = models.Job(object_id = job["object_id"])
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job(db: Session, job_id, data):
    db.query(models.Job).filter(models.Job.id == job_id).update(data)
    db.commit()
    
def get_job_by_id(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_last_job_by_object_id(db: Session, object_id: int):
    return db.query(models.Job).filter(models.Job.object_id == object_id).order_by(models.Job.timestamp.desc()).first()
