from typing import List

from mp3monitoring.core.job import Job, JobConfig


class Manager:
    """
    Management object to manage multiple job objects.
    :ivar jobs: We could use a dictionary here, but it is easier to use a List and find a specific Job in it. Also it is not expected to have a lot of jobs.
    """

    def __init__(self):
        self.jobs: List[Job] = []

    def __len__(self):
        return len(self.jobs)

    def add(self, job: Job):
        self.jobs.append(job)

    def get_configurations(self) -> List[JobConfig]:
        """
        Get configurations from every job.
        """
        return [job.config for job in self.jobs]

    def remove_by_index(self, index: int):
        """
        Removes and stops a job by it's index.
        """
        job = self.jobs.pop(index)
        job.stop()

    def start(self):
        """
        Attempt to start all jobs.
        """
        for job in self.jobs:
            if job.config.run_at_startup:
                job.start()

    def stop(self, join=True):
        """
        Stop all jobs.

        :param join: join the threads
        """
        for job in self.jobs:
            job.stop(join)

    def join(self):
        """
        Manually join the job threads.
        """
        for job in self.jobs:
            job.join()
