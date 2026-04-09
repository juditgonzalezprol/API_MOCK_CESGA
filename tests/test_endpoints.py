"""Basic API tests using pytest."""
import json
import time
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.db_models import Job, JobStatus

# Create test client
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Setup and teardown test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "submit_job" in data["endpoints"]


class TestJobSubmission:
    """Test job submission endpoint."""
    
    def test_submit_valid_job(self, setup_database):
        """Test submitting a valid job."""
        payload = {
            "fasta_sequence": ">seq1\nMKFSMVQVS",
            "fasta_filename": "test.fasta",
            "gpus": 1,
            "cpus": 8,
            "memory_gb": 32.0,
            "max_runtime_seconds": 3600,
        }
        
        response = client.post("/jobs/submit", json=payload)
        assert response.status_code == 201
        
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "PENDING"
        assert data["message"]
    
    def test_submit_job_invalid_fasta_no_header(self, setup_database):
        """Test submitting job with invalid FASTA (no header)."""
        payload = {
            "fasta_sequence": "MKFSM",  # No '>' header
            "fasta_filename": "test.fasta",
        }
        
        response = client.post("/jobs/submit", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_submit_job_gpus_exceed_limit(self, setup_database):
        """Test submitting job with too many GPUs."""
        payload = {
            "fasta_sequence": ">seq1\nMKFSMVQVS",
            "fasta_filename": "test.fasta",
            "gpus": 10,  # Exceeds MAX_GPUS_PER_JOB (4)
        }
        
        response = client.post("/jobs/submit", json=payload)
        assert response.status_code == 422


class TestJobStatus:
    """Test job status endpoint."""
    
    def test_get_pending_job_status(self, setup_database):
        """Test retrieving status of a pending job."""
        # Submit a job
        submit_response = client.post(
            "/jobs/submit",
            json={
                "fasta_sequence": ">seq1\nMKFSMVQVS",
                "fasta_filename": "test.fasta",
            }
        )
        job_id = submit_response.json()["job_id"]
        
        # Get status
        status_response = client.get(f"/jobs/{job_id}/status")
        assert status_response.status_code == 200
        
        data = status_response.json()
        assert data["job_id"] == job_id
        assert data["status"] == "PENDING"
        assert data["fasta_filename"] == "test.fasta"
    
    def test_get_nonexistent_job(self, setup_database):
        """Test retrieving status of non-existent job."""
        response = client.get("/jobs/nonexistent_id/status")
        assert response.status_code == 404


class TestJobOutputs:
    """Test job outputs endpoint."""
    
    def test_get_pending_job_outputs_fails(self, setup_database):
        """Test that outputs are not available for pending jobs."""
        submit_response = client.post(
            "/jobs/submit",
            json={
                "fasta_sequence": ">seq1\nMKFSMVQVS",
                "fasta_filename": "test.fasta",
            }
        )
        job_id = submit_response.json()["job_id"]
        
        # Try to get outputs (should fail for pending job)
        response = client.get(f"/jobs/{job_id}/outputs")
        assert response.status_code == 400


class TestListJobs:
    """Test listing jobs."""
    
    def test_list_jobs_empty(self, setup_database):
        """Test listing jobs when database is empty."""
        response = client.get("/jobs/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_jobs_multiple(self, setup_database):
        """Test listing multiple jobs."""
        # Submit 3 jobs
        job_ids = []
        for i in range(3):
            submit_response = client.post(
                "/jobs/submit",
                json={
                    "fasta_sequence": f">seq{i}\nMKFSMVQVS",
                    "fasta_filename": f"test{i}.fasta",
                }
            )
            job_ids.append(submit_response.json()["job_id"])
        
        # List jobs
        response = client.get("/jobs/")
        assert response.status_code == 200
        
        jobs = response.json()
        assert len(jobs) == 3
        for job in jobs:
            assert job["job_id"] in job_ids
            assert job["status"] == "PENDING"


class TestStateTransitions:
    """Test job state transitions (requires timing)."""
    
    def test_job_state_progression(self, setup_database):
        """Test that job progresses through states over time.
        
        Note: This test depends on PENDING_TO_RUNNING_DELAY 
        and RUNNING_TO_COMPLETED_DELAY configuration.
        """
        # Submit job
        submit_response = client.post(
            "/jobs/submit",
            json={
                "fasta_sequence": ">seq1\nMKFSMVQVS",
                "fasta_filename": "test.fasta",
            }
        )
        job_id = submit_response.json()["job_id"]
        
        # Check initial status (should be PENDING)
        response = client.get(f"/jobs/{job_id}/status")
        assert response.json()["status"] == "PENDING"
        
        # Note: Full state progression testing would require
        # waiting for configured delays or mocking time
        # This is a skeleton for integration testing


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
