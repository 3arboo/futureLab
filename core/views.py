from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Project, CustomUser
from .forms import ProjectForm, EvaluationForm, StudentAssignmentForm, VisitorEvaluationForm, AnonymousEvaluationForm

def home(request):
    upcoming_projects = Project.objects.filter(presentation_time__gt=timezone.now())
    past_projects = Project.objects.filter(presentation_time__lte=timezone.now())
    
    context = {
        'upcoming_projects': upcoming_projects,
        'past_projects': past_projects,
    }
    return render(request, 'core/home.html', context)

def dashboard(request):
    context = {
        'projects_count': Project.objects.count(),
        'students_count': CustomUser.objects.filter(role='S').count(),
    }
    return render(request, 'core/dashboard.html', context)

def join_project(request):
    if request.method == 'POST':
        form = StudentForm(request.POST , instance = request.user)
        if form.is_valid():
            user =form.save(commit=True)
            user.role = 'S'
            user.save()
            return redirect('dashboard')
        
    else:
        
        form = StudentForm(instance=request.user)

    return render(request, 'core/join_project.html', {'form': form})


def project_list(request):
    projects = Project.objects.all().order_by('presentation_time')
    context = {
        'projects': projects,
        'saturday_projects': projects.filter(presentation_time__week_day=7)
    }
    return render(request, 'core/project_list.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    evaluations = project.evaluations.all()
    
    context = {
        'project': project,
        'evaluations': evaluations,
    }
    return render(request, 'core/project_detail.html', context)

def visitor_evaluation(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = VisitorEvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.project = project
            evaluation.save()
            messages.success(request, 'شكراً لك! تم حفظ تقييمك بنجاح.')
            return redirect('core:project_detail', pk=pk)
    else:
        form = VisitorEvaluationForm()
    
    return render(request, 'core/visitor_evaluation.html', {
        'project': project,
        'form': form
    })


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Add update logic here
    return render(request, 'core/project_update.html', {'project': project})


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('core:dashboard')
    return render(request, 'core/project_delete.html', {'project': project})


def add_member(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Add member addition logic here
    return render(request, 'core/add_member.html', {'project': project})


def remove_member(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Add member removal logic here
    return render(request, 'core/remove_member.html', {'project': project})

def evaluate_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        form = AnonymousEvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.project = project
            evaluation.save()
            messages.success(request, 'شكراً لتقييمك!')
            return redirect('core:project_detail', pk=project_id)
    else:
        form = AnonymousEvaluationForm()
    
    return render(request, 'core/evaluate_project.html', {
        'project': project,
        'form': form
    })

def custom_404(request, exception):
    context = {
        'error_code': '404',
        'error_title': 'الصفحة غير موجودة',
        'error_message': 'عذراً، الصفحة التي تبحث عنها غير موجودة أو تم نقلها.'
    }
    return render(request, 'error.html', context, status=404)

def custom_500(request):
    context = {
        'error_code': '500',
        'error_title': 'خطأ في الخادم',
        'error_message': 'عذراً، حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى لاحقاً.'
    }
    return render(request, 'error.html', context, status=500)
