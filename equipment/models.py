from django.db import models
from django.db.models.deletion import DO_NOTHING


class Equipment(models.Model):
    name = models.CharField(max_length=250)
    department = models.ForeignKey("department.Department", on_delete=DO_NOTHING)

    def __str__(self):
        return self.name
