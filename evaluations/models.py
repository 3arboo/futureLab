from django.db import models
from django.conf import settings
from core.models import Project

class Criteria(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    max_score = models.IntegerField()

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='visitor_evaluations'
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    comments = models.TextField(blank=True)  # Added comments field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation for {self.student.username} by {self.evaluator.username}"

class Score(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        unique_together = ['evaluation', 'criteria']
