# evaluations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Project, CustomUser
from .models import Criteria, Score, Evaluation
from .forms import EvaluationForm

@login_required
def evaluation_list(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'evaluations/evaluation_list.html', {
        'evaluations': evaluations
    })

@login_required
def evaluation_detail(request, pk):
    evaluation = get_object_or_404(Evaluation, pk=pk)
    scores = Score.objects.filter(evaluation=evaluation)
    return render(request, 'evaluations/evaluation_detail.html', {
        'evaluation': evaluation,
        'scores': scores
    })

def evaluate_student(request, project_id, student_id):
    project = get_object_or_404(Project, id=project_id)
    student = get_object_or_404(CustomUser, id=student_id)
    
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.student = student
            evaluation.project = project
            evaluation.evaluator = request.user
            evaluation.save()
            
            for criteria in Criteria.objects.all():
                score_value = form.cleaned_data[f'criteria_{criteria.id}']
                Score.objects.create(
                    evaluation=evaluation,
                    criteria=criteria,
                    value=score_value
                )
            return redirect('dashboard')
    else:
        form = EvaluationForm()
    
    return render(request, 'evaluate.html', {'form': form})