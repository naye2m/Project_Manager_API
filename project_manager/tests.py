from django.test import TestCase
from .models import Project

class ProjectTestCase(TestCase):
    def setUp(self):
        Project.objects.create(name="Test Project", description="Test Description")

    def test_project_name(self):
        project = Project.objects.get(name="Test Project")
        self.assertEqual(project.name, "Test Project")

