from django.db import models

# Create your models here.
class List(models.Model):
    name = models.CharField(max_length=100)
    role = models.IntegerField()

    def __str__(self):
        return self.name

class Template(models.Model):
    template=models.ImageField(upload_to='templates/')
