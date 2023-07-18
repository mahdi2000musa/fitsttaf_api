from django.db import models
from staff.models import Profile

# Create your models here.


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        waiting = 'W','waiting'
        done = 'D', 'done'
        pending = 'P', 'pending'
        assigned = 'A', 'assigned'

    subject = models.CharField(max_length=200, null=False, blank=False)
    participant = models.ForeignKey(Profile, related_name="participant", on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True)
    file = models.FileField(upload_to='task_file/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=TaskStatus.choices, null=False, blank=False, default=TaskStatus.assigned)
    assigner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assigner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} that status {self.status}"

class Comment(models.Model):
    text = models.TextField(max_length=1000)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='comment_file/', blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.task.subject} , {self.profile.user.username}'
