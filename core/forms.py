from django import forms
from .models import Project, Evaluation, CustomUser

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'presentation_time', 'location']
        widgets = {
            'presentation_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['rating', 'comments']  # Changed from 'score' to 'rating'
        widgets = {
            'rating': forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'comments': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'rating': 'التقييم',
            'comments': 'التعليقات',
        }

class StudentAssignmentForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='S', project__isnull=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="الطلاب المتاحون"
    )

class VisitorEvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['evaluator_name', 'evaluator_email', 'rating', 'comments']
        widgets = {
            'rating': forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'comments': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'evaluator_name': 'الاسم (اختياري)',
            'evaluator_email': 'البريد الإلكتروني (اختياري)',
            'rating': 'التقييم',
            'comments': 'التعليقات',
        }

class AnonymousEvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['evaluator_name', 'evaluator_email', 'rating', 'comments']
        widgets = {
            'rating': forms.RadioSelect(),
            'comments': forms.Textarea(attrs={'rows': 4}),
        }

