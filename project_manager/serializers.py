from rest_framework import serializers

from .models import Project, ProjectMember, Task, Comment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        




class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']



class ProjectMemberSerializer(serializers.ModelSerializer):
    """ Serializer for ProjectMember model """
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    role = serializers.ChoiceField(choices=ProjectMember.ROLE_CHOICES)

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'role']
        
        



class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assigned_to',
            'project',
            'created_at',
            'due_date'
        ]



class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'task', 'created_at']
