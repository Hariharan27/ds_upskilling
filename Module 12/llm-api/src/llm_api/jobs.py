from datetime import datetime
from uuid import uuid4


class JobManager:
    """Stores the state of background jobs."""

    def __init__(self):
        self.jobs = {}

    def create_job(self) -> str:
        """Create a new pending job."""

        job_id = str(uuid4())

        self.jobs[job_id] = {
            "job_id": job_id,
            "status": "pending",
            "created_at": datetime.now(),
            "result": None,
        }

        return job_id

    def update_job(
        self,
        job_id: str,
        status: str,
        result: str | None = None,
    ) -> None:
        """Update the state of a job."""

        if job_id not in self.jobs:
            return

        self.jobs[job_id]["status"] = status
        self.jobs[job_id]["result"] = result

    def get_job(self, job_id: str):
        """Return job information."""

        return self.jobs.get(job_id)