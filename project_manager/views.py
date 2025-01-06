from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest, QueryDict
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task, Comment, User
from rest_framework.authtoken.models import Token
from .serializers import (
    UserSerializer,
    ProjectSerializer,
    TaskSerializer,
    CommentSerializer,
    ProjectMemberSerializer,
)


@api_view(['POST'])
def register_user(request) -> Response:
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user: AbstractBaseUser | None = authenticate(request, username=username, password=password)
    if user is not None:

        token, created = Token.objects.get_or_create(user=user)
        res = Response({"message": "Login successful", "user_id": user.id})


        res.set_cookie(key='Authorization', value='Token ' + token.key, httponly=True, secure=True, samesite='Lax')
        res.data = {"token": token.key, "user_id": user.id}
        return res

    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_self_profile(request):
    user = request.user
    if user.is_authenticated:
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
    return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def list_create_projects(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    is_modifiable = project.is_admin(request.user)
    
    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)
    elif not is_modifiable:
        return Response({"error": "User not authorized to Edit or Delete this project"}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        project.delete()
        return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def list_create_tasks(request:HttpRequest, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    is_member = project.is_member(request.user)    
    if request.method == 'GET':
        tasks = Task.objects.filter(project=project)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not is_member:
            return Response({"error": "User not authorized to create tasks for this project. Not a perticipant"}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data.copy()
        data['project'] = project_id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def list_create_comments(request:HttpRequest, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data.copy()
        data['task'] = task_id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not comment.is_updatable_by(request.user):
            return Response({"error": "User not authorized to Edit this comment"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if not comment.is_deletable_by(request.user):
            return Response({"error": "User not authorized to Delete this comment"}, status=status.HTTP_401_UNAUTHORIZED)
        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
