from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag

@api_view(['GET'])
def get_routes(request):
    routes = [ 
        { 'GET': '/api/projects'},
        { 'GET': '/api/projects/id'},
        { 'POST': '/api/projects/id/vote'},
        { 'POST': '/api/users/token'},
        { 'POST': '/api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
def get_projects(request):
    # print(request.user)
    projects = Project.objects.all()
    serialized_projects = ProjectSerializer(projects, many=True)
    return Response(serialized_projects.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    serialized_project = ProjectSerializer(project, many=False)
    return Response(serialized_project.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_project(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project
    )
    review.value = data['value']
    review.save()

    project.get_vote_count
    serialized_project = ProjectSerializer(project, many=False)
    return Response(serialized_project.data)

@api_view(['DELETE'])
def remove_tag(request):
    
    tag_id = request.data['tag']
    project_id = request.data['project']
    project = Project.objects.get(id=project_id)
    tag = Tag.objects.get(id=tag_id)
    project.tags.remove(tag)


    
    return Response("Tag was deleted")