from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Vender(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, null=True, help_text='Vender Name')

    def __str__(self):
        return self.user.username

