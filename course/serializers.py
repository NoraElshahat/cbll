from rest_framework import serializers
from .models import Course


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id",)
        model = Course


class DetailCourseSerializer(CoursesSerializer):
    class Meta:
        model = Course
        fields = ("id", "title")
