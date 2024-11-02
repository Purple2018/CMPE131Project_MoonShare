from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, TaskForm

@login_required
def project_list(request):
    projects = Project.objects.filter(created_by=request.user)
    return render(request, 'board/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, created_by=request.user)
    tasks = project.tasks.all()
    return render(request, 'board/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'board/project_form.html', {'form': form})

@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id, created_by=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm()
    return render(request, 'board/task_form.html', {'form': form})
