from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Page, PageNotAnInteger, Paginator, EmptyPage

def paginate_profiles(request, profiles, results):
    if request.GET.get('page'):
      page = request.GET.get('page')
    else:
      page = 1
    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.get_page(int(page))
    except PageNotAnInteger:
        page = 1
        profiles = paginator.get_page(page)
    except EmptyPage:
        page = paginator.num_pages + 1
        profiles = paginator.get_page(page)
    
    left_page = int(page) - 3
    if left_page < 1:
        left_page = 1

    right_page = int(page) + 4
    if right_page > paginator.num_pages:
        right_page = paginator.num_pages + 1

    custom_range = range(left_page, right_page)

    return custom_range, profiles


def search_profiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
      )
    return profiles, search_query