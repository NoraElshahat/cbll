from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    objective = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.title
