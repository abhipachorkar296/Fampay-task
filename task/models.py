from django.db import models
from django.db.models.base import Model

# Create your models here.

class Videos(models.Model):
    id = models.CharField(max_length=500, primary_key=True, unique=True)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    urls = models.URLField()
    created_datetime = models.DateTimeField()
    
    class Meta:
        ordering = ('-created_datetime',)
    
    def __str__(self):
        return "{}, {}".format(self.id, self.title)