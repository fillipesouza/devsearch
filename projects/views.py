from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from projects.forms import ProjectForm
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginate_projects

# Create your views here.



def projects(request):
    projects, search_query = search_projects(request)
    
    custom_range, projects = paginate_projects(request, projects, results=3)

    context = {'projects': projects,  'search_query': search_query, 'custom_range': custom_range }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    form = ReviewForm()
    context = { 'project': project_obj, 'form': form }
    
    
    if request.method == 'POST':
        try:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.project = project_obj
                review.owner = request.user.profile
                review.save()            
                project_obj.get_vote_count
                messages.success(request, 'Review successfully sent')
                return redirect('project', pk=project_obj.id )
        except Exception:
            messages.error(request, 'Something went wrong')
    

    return render(request, 'projects/single-project.html', context)

@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    profile = request.user.profile
    
    if request.method == 'POST':
        tags = request.POST.get('newtags').replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES)
        #print(request.POST) - logging request
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
            

    context = {'form': form}
    return render(request, 'projects/project-form.html', context)

@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        tags = request.POST.get('newtags').replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, 'projects/project-form.html', context)

@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = { 'object': project }
    return render(request, 'projects/delete-form.html', context)

    