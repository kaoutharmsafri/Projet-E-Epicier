from django.db import models
from django.contrib.auth.models import AbstractUser
from project.models import Epicerie
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
# Create your models here.
class User(AbstractUser):
    is_Client = models.BooleanField(default=False)
    is_Epicier = models.BooleanField(default=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    def __str__(self):
        return str(self.id)+" - "+self.username
    


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=10)
    adress = models.CharField(max_length=500)
    epicerie=models.ForeignKey(Epicerie, on_delete=models.CASCADE,related_name='epicerie',default='1')
    def __str__(self):
        return str(self.user_id)+" - "+self.user.username

class Epicier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=10)
    adress = models.CharField(max_length=500)



