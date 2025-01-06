from django.db import models
from django.contrib.auth.models import  AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username




class Project(models.Model):
    """ Model for a project """
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def is_member(self, user:AbstractUser):

        return self.owner == user or self.members.filter(user=user.id).exists()
    
    def is_admin(self, user):
        print(self.owner.id, user.id)

        return self.owner == user or self.members.filter(user=user.id, role=ProjectMember.ADMIN).exists()



class ProjectMember(models.Model):
    """ Model for a project member """

    ADMIN = 'Admin'
    MEMBER = 'Member'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MEMBER, 'Member')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default=MEMBER)

    def __str__(self):
        return f"{self.user.username} ({self.role}) in {self.project.name}"



class Task(models.Model):
    """ Model for a task """

    TO_DO = 'To Do'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    STATUS_CHOICES = [
        (TO_DO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done')
    ]


    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=TO_DO)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default=LOW)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    def is_editable_by(self, user):

        return self.project.is_admin(user)
    



class Comment(models.Model):
    """ Model for a comment """
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"
    
    def is_admin(self, user):

        return self.task.project.is_admin(user)
    
    def is_updatable_by(self, user):

        return  self.user == user 

    def is_deletable_by(self, user):

        print(self.user.id, user.id)
        
        return self.user == user or self.is_admin(user)
        