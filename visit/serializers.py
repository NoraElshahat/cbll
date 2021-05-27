from attendance.models import ApprovedUserVisit, Attendance
from attendance.serializers import AttendanceUserOnly
from course.models import Course
from course.serializers import CoursesSerializer, DetailCourseSerializer
from department.models import Department
from department.serializers import DepartmentSerializer
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from equipment.models import Equipment
from meeting.serializers import MeetingDetailedSerializer
from rest_framework import serializers
from users.serializers import (
    StudenSerializer,
    StudentSerializersWithHU,
    SupervisorSerializer,
    UsersSerializer,
)

from .models import Achievement, Activity, Benefician, Visit, VisitSites


class VisitSitesSeialzier(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = VisitSites


class AchievementSerialzier(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "body")
        # depth = 3
        model = Achievement


class BeneficianSerialzier(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "gender")
        # depth = 3
        model = Benefician


class VisitStudentsSerilaizer(serializers.Serializer):
    students = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )


class DetailVisitSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    visit_course = serializers.StringRelatedField()
    visit_site = serializers.StringRelatedField(source="site")
    students = StudentSerializersWithHU(many=True)
    meeting = MeetingDetailedSerializer()
    benefician_set = BeneficianSerialzier()
    achievement_set = AchievementSerialzier(many=True)
    start = serializers.DateField(source="date")
    leader = UsersSerializer()
    main_img = serializers.StringRelatedField()
    img_one = serializers.StringRelatedField()
    img_two = serializers.StringRelatedField()
    # is_allowed = serializers.SerializerMethodField()
    current_user = serializers.SerializerMethodField()
    students_no = serializers.IntegerField(default=0)

    def get_current_user(self, instance):
        blocked_students = instance.blocked_students()
        students = instance.students.all()
        current_user = self.context['request'].user
        current_user_ob = {}
        current_user_ob['is_allowed'] = False
        if current_user in blocked_students:
            current_user_ob['reason'] = blocked_students[current_user]
            return current_user_ob

        if current_user in students:
            current_user_ob['reason'] = 'You are Already Applied'
            return current_user_ob

        current_user_ob['is_allowed'] = True
        current_user_ob['reason'] = ''
        
        return  current_user_ob

    class Meta:
        model = Visit
        fields = (
            "id",
            "code",
            "name",
            "visit_course",
            "equipment",
            "objectives",
            "leader",
            "current_user",
            "students",
            "students_no",
            "studnets_gender_count",
            "visit_site",
            "department",
            "meeting",
            "start",
            "to",
            "benefician_set",
            "achievement_set",
            "visit_course",
            "main_img",
            "img_one",
            "img_two",
        )


class InitSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()
    code = serializers.ReadOnlyField()

    extra_kwargs = {"code": {"read_only": True}}

    students = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(), many=True
    )

    site = serializers.PrimaryKeyRelatedField(queryset=VisitSites.objects.all())

    department = DepartmentSerializer()

    visit_course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    start = serializers.DateField(source="date")

    class Meta:
        fields = [
            "id",
            "code",
            "name",
            "students",
            "meeting",
            "objectives",
            "site",
            "department",
            "start",
            "to",
            "visit_course",
            "main_img",
            "img_one",
            "img_two",
        ]

        model = Visit
        depth = 1


class MainVisitSerializer(InitSerializer):
    pass


class BeneficianRealatedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "gender")
        model = Benefician


class AchievementRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("body", "date")
        model = Achievement


class ListActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("id",)


class DetailedActivitiesSerializer(ListActivitiesSerializer):
    leader = UsersSerializer()

    class Meta:
        model = Activity
        fields = "__all__"


class ListVisitReportSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name")
        model = Visit


class DetailedVisitReportSerializer(serializers.ModelSerializer):
    supervisor = serializers.SerializerMethodField()
    students_no = serializers.DictField(source="studnets_gender_count", read_only=True)
    attendance_no = serializers.IntegerField(source="get_attendance_no", read_only=True)
    attendance_set = AttendanceUserOnly(many=True)
    beneficians_no = serializers.DictField(source="get_benefician_no", read_only=True)
    benefician_set = BeneficianRealatedSerializer(many=True)
    achievement_set = AchievementRelatedSerializer(many=True)
    achievements_no = serializers.IntegerField(source="get_achievement_no")
    department = DepartmentSerializer()
    activity_set = DetailedActivitiesSerializer(many=True)
    activities_no = serializers.IntegerField()
    activities_per_day = serializers.DictField(source="activity_days")
    students = serializers.StringRelatedField(many=True)
    visit_days_no = serializers.IntegerField(source="days_no")
    starts = serializers.DateField(source="date")
    visit_course = serializers.StringRelatedField()
    location = serializers.StringRelatedField(source="site")

    def get_supervisor(self, ob):
        return SupervisorSerializer(ob.leader).data

    class Meta:
        model = Visit
        fields = (
            "id",
            "code",
            "department",
            "starts",
            "to",
            "visit_course",
            "location",
            "supervisor",
            "objectives",
            "attendance_set",
            "benefician_set",
            "achievement_set",
            "activity_set",
            "students",
            "students_no",
            "attendance_no",
            "beneficians_no",
            "achievements_no",
            "activities_no",
            "activities_per_day",
            "visit_days_no",
        )

        read_only_fields = ["code", "id"]


class UploadPhotoSerializer(serializers.ModelSerializer):
    main_img = serializers.ImageField()

    class Meta:
        fields = ("id", "main_img", "img_one", "img_two")
        model = Visit


class VisitPlanSerializer(InitSerializer):
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipment.objects.all())

    class Meta:
        fields = InitSerializer.Meta.fields + ["equipment"]
        model = InitSerializer.Meta.model


class VisitPlanDetailSerializer(VisitPlanSerializer):
    site = VisitSitesSeialzier()
    department = DepartmentSerializer()
    visit_course = DetailCourseSerializer()

    class Meta:
        fields = VisitPlanSerializer.Meta.fields
        model = VisitPlanSerializer.Meta.model



class RemoveVisitUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = [
            'id',
            'students'
            ]