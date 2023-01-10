import json
import time
import random
from fastapi.testclient import TestClient
from webapp.main import app


client = TestClient(app)


def test_post():
    response = client.post(
        "/jobs",
        data=json.dumps({"object_id": 1}) 
    )
    assert response.status_code == 200
    content = response.json()
    assert content["job_id"]
    assert isinstance(content["job_id"], int)
    # get job from db by id and assert


def test_create_and_get_job():
    object_id = random.randint(1,1000)
    
    # Create a job for a special object_id
    response = client.post(
        "/jobs",
        data=json.dumps({"object_id": object_id})
    )
    assert response.status_code == 200
    content = response.json()
    job_id = content["job_id"]
    assert job_id
    assert isinstance(content["job_id"], int)
    
    # Get job from end point
    response = client.get(f"jobs/{job_id}")
    content = response.json()
    assert response.status_code == 200
    assert content["id"] == job_id
    assert content["object_id"] == object_id
    assert (content["status"] == "PENDDING" or content["status"] == "PROCESSING" )

    time.sleep(45)
    response = client.get(f"jobs/{job_id}")
    content = response.json()
    assert response.status_code == 200
    assert content["status"] == "SUCCESS"

def test_time_limit_window_for_creae_jobs_with_same_object_id():
    object_id = -999
    
    # Create Job 1
    response = client.post(
        "/jobs",
        data=json.dumps({"object_id": object_id})
    )
    assert response.status_code == 200
    job_1 = response.json()
    job_1_id = job_1["job_id"]
    assert job_1_id
    
    # Create Job 2
    response = client.post(
        "/jobs",
        data=json.dumps({"object_id": object_id})
    )
    assert response.status_code == 200
    job_2 = response.json()
    job_2_id = job_2["job_id"]
    assert job_2_id
    
    # Get Job 1
    response = client.get(f"jobs/{job_1_id}")
    content = response.json()
    assert response.status_code == 200
    assert content["id"] == job_1_id
    assert content["object_id"] == object_id
    assert (content["status"] == "PENDDING" or content["status"] == "PROCESSING" )


    # Get Job 2
    response = client.get(f"jobs/{job_2_id}")
    content = response.json()
    assert response.status_code == 200
    assert content["id"] == job_2_id
    assert content["object_id"] == object_id
    assert content["status"] == "PENDDING"

    time.sleep(5*60+1)
    # Get Job 2 after time window
    response = client.get(f"jobs/{job_2_id}")
    content = response.json()
    assert response.status_code == 200
    assert (content["status"] == "SUCCESS" or content["status"] == "PROCESSING" )

    time.sleep(45)
    # Get Job 2 after it is finished
    response = client.get(f"jobs/{job_2_id}")
    content = response.json()
    assert response.status_code == 200
    assert content["status"] == "SUCCESS"