from django.db import models


class Translation(models.Model):
    text = models.TextField()
    lang = models.CharField(max_length=10)
    result = models.TextField()

    def __str__(self):
        return f"{self.text} ({self.lang})"