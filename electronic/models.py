from django.db import models
from django.contrib.auth.models import User
from enum import IntEnum

# Create your models here.
class DeviceType(IntEnum):

    Mobile = 1
    Laptop = 2

    @classmethod
    def choices(cls):
        return [(key.value,key.name)for key in cls]


class Product(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device_type = models.CharField(max_length=255, choices=DeviceType.choices(),default=DeviceType.Laptop)


    def __str__(self):
        return self.name



