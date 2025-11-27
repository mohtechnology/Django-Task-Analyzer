from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.TextField(max_length=100)
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.FloatField(default=1)
    importance = models.IntegerField(default=1)
    dependencies = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="blocked_by")
    score = models.FloatField(default=0)

    def __str__(self):
        return self.title 