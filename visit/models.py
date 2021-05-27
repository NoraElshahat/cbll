import uuid
from datetime import datetime, timedelta

from PIL import Image
from course.models import Course
from department.models import Department
from django.contrib.auth import get_user_model
from django.core.signals import request_finished
from django.dispatch import receiver
from django.conf import settings
from  django.urls import reverse
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from equipment.models import Equipment
from faculty.models import Faculty
from meeting.models import Meeting
from django.conf import settings
from report.models import Report
from users.models import BlockedStudents

upload_to_path = "storage/visits/"

DATE_FORMAT = "%Y-%m-%d"


def tommorrow():
    tommorrow = timezone.now() + timedelta(1)

    return str(tommorrow).split(" ")[0]


class VisitSites(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Benefician(models.Model):

    gender = (("male", "Male"), ("female", "Female"))

    name = models.CharField(_("name"), max_length=150)
    gender = models.CharField(
        max_length=6, choices=gender, default="male", help_text="select a gender"
    )

    visit = models.ForeignKey("visit.Visit", on_delete=DO_NOTHING)

    def __str__(self):
        return str(self.name)


class Achievement(models.Model):
    body = models.CharField(_("Achievement Desc"), max_length=250)
    visit = models.ForeignKey("visit.Visit", on_delete=DO_NOTHING)
    date = models.DateTimeField(_("Done at"), auto_now=True)

    def __str__(self):
        return str(self.body)


class Activity(models.Model):
    title = models.CharField(max_length=50)
    visit = models.ForeignKey("visit.Visit", on_delete=DO_NOTHING)

    date = models.DateField(_("Due to"), auto_now=False, auto_now_add=False)

    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Leader"),
        limit_choices_to={"is_staff": True},
        on_delete=DO_NOTHING,
    )

    desc = models.TextField(_("Activities were in the visit"))

    def __str__(self):
        return str(self.title)


class Visit(models.Model):
    days_no = 0
    days = []
    activiy_active_days = set()

    def validate_not_less_than(self):
        to = datetime.strptime(str(self), DATE_FORMAT).timestamp()
        start = datetime.strptime(tommorrow(), DATE_FORMAT).timestamp()

        if to < start:
            raise ValueError("Please select valide date")

    def days_no(self):
        return len(self.days)

    def visit_code():
        return str(uuid.uuid4)[:8]

    def tommorrow():
        tommorrow = timezone.now() + timedelta(1)

        return str(tommorrow).split(" ")[0]

    def week_after():
        week_after = timezone.now() + timedelta(7)

        return str(week_after).split(" ")[0]

    def students_no(self):
        return self.students.count()


    def studnets_gender_count(self):
        males = self.students.filter(gender="male").count()
        females = self.students.filter(gender="female").count()

        return {"male": males, "female": females}

    def days_between(self, start: datetime, end: datetime, increment_by=1):
        self.days = []
        result = {}
        desc = []
        while start.timestamp() <= end.timestamp():
            day = start.strftime(DATE_FORMAT)
            self.days.append(day)
            if self.activity_set.filter(date=day).exists():
                for activity in self.activity_set.filter(date=day).all():
                    desc.append(
                        {
                            "id": activity.id,
                            "title": activity.title,
                            "desc": activity.desc,
                        }
                    )
                    # result[activity.date] = desc
                result[day] = desc

                self.activiy_active_days.add(activity.date)
                desc = []
            start = start + timedelta(increment_by)
        return result

    def activity_days(self):
        date_filed = datetime.strptime(str(self.date), DATE_FORMAT)
        to_filed = datetime.strptime(str(self.to), DATE_FORMAT)

        return self.days_between(date_filed, to_filed)

    def activities_no(self):
        return self.activity_set.filter(date__in=self.activiy_active_days).count()

    def get_achievement_no(self):
        return self.achievement_set.all().count()

    def get_benefician_no(self):
        males = self.benefician_set.filter(gender="male").count()
        females = self.benefician_set.filter(gender="female").count()

        return {"male": males, "females": females}

    def get_attendance_no(self):
        try:
            return self.attendance_set.get().get_users_count()
        except:
            return 0

    name = models.CharField(max_length=250)

    date = models.DateField(_("Starts in"), default=timezone.now)

    to = models.DateField(
        _("Ends in"), auto_now=False, auto_now_add=False, default=week_after
    )

    objectives = models.TextField()

    code = models.CharField(
        max_length=8, default=uuid.uuid4, editable=False, unique=True
    )

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="visit",
        limit_choices_to={
            "is_staff": False,
            "is_super_admin": False,
            "is_superuser": False,
        },
    )

    equipment = models.ForeignKey(
        "equipment.Equipment",
        on_delete=DO_NOTHING,
        blank=True,
        null=True,
        verbose_name="equipments",
    )

    department = models.ForeignKey("department.Department", on_delete=DO_NOTHING)

    site = models.ForeignKey("visit.VisitSites", on_delete=CASCADE)
    visit_course = models.ForeignKey(Course, on_delete=DO_NOTHING)

    meeting = models.ForeignKey(
        "meeting.Meeting", on_delete=DO_NOTHING, blank=True, null=True
    )

    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Leader"),
        on_delete=models.DO_NOTHING,
        limit_choices_to={
            "is_staff": True,
            "is_super_admin": False,
            "is_superuser": False,
        },
        related_name="leader",
    )

    main_img = models.ImageField(
        _("Main image"), blank=True, null=False, upload_to=upload_to_path
    )
    img_one = models.ImageField(
        _("Other image"), blank=True, null=False, upload_to=upload_to_path
    )
    img_two = models.ImageField(
        _("Other image"), blank=True, null=False, upload_to=upload_to_path
    )

    complex_report = models.ForeignKey(
        "report.ComplexReport",
        verbose_name=_("visit report"),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)

    def is_tomorrow(self):
        tomorrow = datetime.now() + timedelta(1)
        tomorrow = tomorrow.strftime(DATE_FORMAT)
        to = self.to.strftime(DATE_FORMAT)

        return tomorrow == to

    def faculty(self):
        return str(self.department.faculty)

    def _safe_img(self, img: str):
        if img:
            return img
        return ""

    def relative_path(self):
        return reverse('visit:visit-detail',args=[self.id])

    def blocked_students(self):
            return {row.student: row.reason for row in BlockedStudents.objects.filter(visit__id=self.id).all()}
 