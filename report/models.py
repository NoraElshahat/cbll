from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from django.db.models.deletion import DO_NOTHING
from django.contrib.auth import get_user_model
from django.conf import settings


class Report(models.Model):
    class ReportTypes(models.IntegerChoices):
        BEFORE_VISIT = 1
        AFTER_VISIT = 2

    title = models.IntegerField(_("Report Type"), choices=ReportTypes.choices)

    is_active = models.BooleanField(_("Is Portion active"), default=False)

    def tommorrow():
        tommorrow = datetime.today() + timedelta(1)

        return str(tommorrow).split(" ")[0]

    questions = models.ManyToManyField(
        "report.Question", verbose_name=_("Report Questions")
    )

    is_for_staff = models.BooleanField(_("Is for staff"), default=False)

    # created_at = models.DateField(auto_now=True)

    to_beactive_in = models.DateField(
        verbose_name=_("The activate date"), default=tommorrow, blank=True
    )

    def __str__(self):
        """
            Getting a string for the class
        """

        return str(self.title)


class QuestionType(models.Model):
    title = models.CharField(_("question type"), max_length=10)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "question types"


class Question(models.Model):
    title = models.CharField(_("Question Title"), max_length=250)

    question_type = models.ForeignKey(
        "report.QuestionType",
        verbose_name=_("question type"),
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return str(self.title)

    def needle_set_active(self):
        return self.needle_set.filter(is_active=True)

    def needle_set_no(self):
        return self.needle_set_active().count()

    class Meta:
        verbose_name_plural = "questiones"


class Needle(models.Model):
    is_active = models.BooleanField(_("Activated"), default=True)

    init_value = models.CharField(_("Proposed Value for Question Type"), max_length=250)

    question = models.ForeignKey(
        "report.Question", verbose_name=_("Question"), on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return str(self.init_value)

    class Meta:
        verbose_name_plural = "needles"


class Answer(models.Model):
    question = models.ForeignKey(
        "report.Question", verbose_name=_("Question"), on_delete=models.DO_NOTHING
    )

    body = models.TextField(_("answer"))

    file_to = models.FileField(
        _("Uploaded File"), upload_to="storage/answers/", blank=True
    )

    def __str__(self):
        return "Answer:" + str(self.question)


class ComplexReport(models.Model):
    after_report = models.ForeignKey(
        "report.Report",
        limit_choices_to={"is_active": True, "title": "2"},
        verbose_name=_("The Questions after visit"),
        related_name="after",
        on_delete=models.DO_NOTHING,
    )

    before_report = models.ForeignKey(
        "report.Report",
        limit_choices_to={"is_active": True, "title": "1"},
        verbose_name=_("The Questions before visit"),
        related_name="before",
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    is_active = models.BooleanField(_("Is report Active"), default=True)

    is_for_staff = models.BooleanField(_("Is for staff"), default=False)
