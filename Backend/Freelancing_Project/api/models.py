from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_freelancer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    department=models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.client.username) +" | "+ str(self.title)

class Proposal(models.Model):
    project = models.ForeignKey(Project, related_name='proposals', on_delete=models.CASCADE, null=True, blank=True)
    freelancer = models.ForeignKey(User, related_name='freelancer_proposals', on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(User, related_name='client_projects', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self) -> str:
        return str(self.freelancer.username) + str(self.project.client.username)