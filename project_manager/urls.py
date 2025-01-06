from django.urls import path
from . import views

urlpatterns = [
    
    
    path('profile/', views.get_self_profile, name='register_user'),


    path('users/register/', views.register_user, name='register_user'),
    path('users/login/', views.login_user, name='login_user'),
    path('users/<int:id>/', views.user_detail, name='user_detail'),


    path('projects/', views.list_create_projects, name='list_create_projects'),
    path('projects/<int:id>/', views.project_detail, name='project_detail'),


    path('projects/<int:project_id>/tasks/', views.list_create_tasks, name='list_create_tasks'),
    path('tasks/<int:id>/', views.task_detail, name='task_detail'),


    path('tasks/<int:task_id>/comments/', views.list_create_comments, name='list_create_comments'),
    path('comments/<int:id>/', views.comment_detail, name='comment_detail'),
]
