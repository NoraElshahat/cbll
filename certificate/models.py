from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.conf import settings


class Certificate(models.Model):
    title = models.CharField(max_length=250)
    img = models.ImageField(
        upload_to="storage/cbl_certificates/", blank=True, default="", null=False
    )
    visit = models.ForeignKey("visit.Visit", on_delete=DO_NOTHING)

    user = models.ForeignKey(get_user_model(), on_delete=DO_NOTHING)

    def __str__(self):
        return str(self.title)
