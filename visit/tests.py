from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from visit.models import Visit, VisitSites
from department.models import Department
from faculty.models import Faculty
from course.models import Course
