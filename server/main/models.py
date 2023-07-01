import logging
from django.db import models
from django.utils import timezone

logging.basicConfig(level=logging.INFO)


class Job(models.Model):

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    # TODO: # rename file name on creation to be unique
    job_file = models.FileField(upload_to='jobs/')
    nbr_tasks = models.IntegerField()
    status = models.CharField(max_length=100, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):

    runner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    task_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending')
    result = models.TextField(null=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.job.name} - {self.task_id}'

    def save(self, *args, **kwargs):

        if self.status == 'pending':
            last_task = Task.objects.filter(job=self.job).last()
            print("last_task", last_task)

            self.task_id = last_task.task_id + 1 if last_task else 1

            if self.task_id > self.job.nbr_tasks:
                logging.warning("No more tasks available")
                return

        elif self.status == 'running':
            self.started_at = timezone.now()
        elif self.status == 'finished':
            self.finished_at = timezone.now()
            logging.info(
                f'Task {self.task_id} finished, with result: {self.result}')

        if self.job.task_set.filter(status='finished').count() == self.job.nbr_tasks:
            self.job.status = 'finished'
            self.job.save()

        if self.task_id == self.job.nbr_tasks:
            self.job.status = 'no-pending-tasks'
            self.job.save()

        return super(Task, self).save(*args, **kwargs)
