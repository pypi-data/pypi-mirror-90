from django.db import models

# Create your models here.

class Harvest(models.Model):
    """
    docstring
    """
    name = models.CharField(max_length=144)    


class Bread(models.Model):
    harvest = models.ForeignKey(Harvest, on_delete=models.PROTECT)