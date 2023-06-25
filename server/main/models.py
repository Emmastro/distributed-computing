from django.db import models


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
            last_running_task = Task.objects.filter(
                status='pending', job=self.job).last()
            print("last_running_task", last_running_task)

            self.task_id = last_running_task.task_id + 1 if last_running_task else 1
            print(self.task_id, self.runner)
        elif self.status == 'running':
            self.started_at = datetime.now()
        elif self.status == 'finished':
            self.finished_at = datetime.now()
        
        super(Task, self).save(*args, **kwargs)

        if self.job.task_set.filter(status='finished').count() == self.job.nbr_tasks:
            self.job.status = 'finished'
            self.job.save()
        if self.task_id == self.job.nbr_tasks:
            self.job.status = 'no-pending-tasks'
            self.job.save() 