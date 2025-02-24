from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class patient(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15)
    image=models.ImageField(upload_to='patient/images/')

    def __str__(self):
        return self.user.username