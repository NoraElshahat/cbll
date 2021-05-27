from django.db import models
from django.db.models.deletion import DO_NOTHING


class Department(models.Model):
    name = models.CharField(max_length=250)
    faculty = models.ForeignKey("faculty.Faculty", on_delete=DO_NOTHING)

    def __str__(self):
        return str(self.name)
