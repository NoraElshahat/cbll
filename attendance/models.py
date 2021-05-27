from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.translation import ugettext as _
from django.conf import settings


class Attendance(models.Model):
    def get_users_count(self):
        return self.users.all().count()

    visit = models.ForeignKey("visit.Visit", on_delete=DO_NOTHING)
    students = models.ManyToManyField(
        get_user_model(),
        limit_choices_to={
            "is_staff": False,
            "is_superuser": False,
            "is_super_admin": False,
        },
    )

    due_to = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str("Attendance for ") + str(self.visit)


class ApprovedUserVisit(models.Model):

    visit = models.ForeignKey(
        "visit.Visit",
        verbose_name=_("The requested Visit"),
        on_delete=models.DO_NOTHING,
    )
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("The Attendant"),
        limit_choices_to={
            "is_staff": False,
            "is_superuser": False,
            "is_super_admin": False,
        },
        on_delete=models.DO_NOTHING,
    )

    parent_signture = models.ImageField(
        upload_to="storage/signtures/", blank=True, default="", null=False
    )

    def __str__(self):
        return "Approvance for " + str(self.visit)
