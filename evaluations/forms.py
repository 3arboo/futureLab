# evaluations/forms.py
from django import forms
from .models import Evaluation, Score

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['comments']