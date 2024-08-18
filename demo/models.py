from django.db import models

# create a simple model called TestPerson with just name and age fields
class TestPerson(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()