from django.db import models

# Create your models here.
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField()
    url = models.URLField()
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title