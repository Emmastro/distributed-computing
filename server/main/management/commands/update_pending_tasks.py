from django.core.management.base import BaseCommand
import logging
from main.models import Job, Task

# TODO: schedule this function to run periodically. Alternatively, set an event that's trigger once a 
# task isn't finished by a certain time, or haven't received signal from the client in a certain time

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        print("test")
        logging.info("Updating jobs with status `no-pending-tasks`")
        jobs = Job.objects.filter(status='no-pending-tasks')

        for job in jobs:
            tasks = Task.objects.filter(status='running', job=job)
            print(tasks)
            for task in tasks:
                task.status = 'cancelled'
                task.save()
            job.status = 'pending'
            job.save()
        logging.info("Done")
