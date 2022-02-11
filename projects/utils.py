from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Page, PageNotAnInteger, Paginator, EmptyPage

def paginate_projects(request, projects, results):
    if request.GET.get('page'):
      page = request.GET.get('page')
    else:
      page = 1
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.get_page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.get_page(page)
    except EmptyPage:
        page = paginator.num_pages + 1
        projects = paginator.get_page(page)
    
    left_page = int(page) - 3
    if left_page < 1:
        left_page = 1

    right_page = int(page) + 4
    if right_page > paginator.num_pages:
        right_page = paginator.num_pages + 1

    custom_range = range(left_page, right_page)

    return custom_range, projects


def search_projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    profiles = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
      )
    return profiles, search_query