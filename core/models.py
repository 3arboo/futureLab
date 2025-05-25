from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta
import os
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

def project_file_path(instance, filename):
    # Generate file path: projects/project_title/filename
    return os.path.join('projects', str(instance.title), filename)

class CustomUser(models.Model):
    ROLES = (
        ('A', 'Admin'),
        ('E', 'Evaluator'),
        ('S', 'Student'),
        ('V', 'Visitor'),
    )
    id_student = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="Student ID",
        help_text="Student ID must be unique"
    )
    full_name = models.CharField(max_length=100, verbose_name="Full Name")
    role = models.CharField(max_length=1, choices=ROLES, default='S')
    phone = PhoneNumberField(blank=True, verbose_name="Phone Number")
    project = models.ForeignKey(
        'Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name="Project"
    )

    def clean(self):
        if self.role == 'S' and self.project and self.project.students.exclude(id=self.id).exists():
            raise ValidationError("This project is already assigned to another student")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['full_name']

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Project Title")
    description = models.TextField(verbose_name="Description")
    presentation_time = models.DateTimeField(
        verbose_name="Presentation Time",
        default=timezone.now() + timedelta(days=7)
    )
    location = models.CharField(
        max_length=100, 
        verbose_name="Location",
        default="Presentation Hall"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(
        upload_to='project_pdfs/',
        validators=[FileExtensionValidator(['pdf'])],
        verbose_name="Project PDF",
        null=True,
        blank=True
    )

    def get_pdf_url(self):
        if self.pdf_file:
            return self.pdf_file.url
        return None

    def get_evaluations(self):
        return self.evaluation_set.all()  # Using default related name

    @property
    def average_rating(self):
        evaluations = self.evaluations.all()  # Changed from evaluation_set
        if evaluations:
            return sum(e.rating for e in evaluations) / len(evaluations)
        return 0

class Evaluation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='evaluations')
    evaluator_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="اسم المقيّم")
    evaluator_email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم"
    )
    comments = models.TextField(blank=True, verbose_name="التعليقات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"

    def __str__(self):
        return f"{self.evaluator_name or 'Anonymous'} - {self.project.title}"

class StudentAssignment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='assignments/')
    comments = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'project']

    def __str__(self):
        return f"{self.student.username} - {self.project.title}"


