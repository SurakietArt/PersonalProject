from django.db import models

class Case(models.Model):
    country = models.CharField(max_length=50, blank = True, null = True)
    case = models.JSONField(default=dict)

    def __str__(self):
        return self.country