from django.db import models
from django.contrib.auth.models import User
from patient.models import patient
from django.conf import settings
# Create your models here.
class designation(models.Model):
    name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=100)

    def __str__(self):
        return self.name
    
class specialization(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

class available_time(models.Model):
    time=models.CharField(max_length=50)
    def __str__(self):
        return self.time
        
class doctor(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='doctor/images/')
    designation=models.ManyToManyField(designation)
    specializations=models.ManyToManyField(specialization)
    available_time=models.ManyToManyField(available_time)
    fee=models.IntegerField()
    meet_link=models.CharField(max_length=200)

    def __str__(self):
        return self.user.username
STAR_CHOICES=[
    ('⭐','⭐'),
    ('⭐⭐','⭐⭐'),
    ('⭐⭐⭐','⭐⭐⭐'),
    ('⭐⭐⭐⭐','⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐','⭐⭐⭐⭐⭐'),
]
class review(models.Model):
    reviewer=models.ForeignKey(patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(doctor,on_delete=models.CASCADE)
    review=models.TextField()
    date=models.DateField(auto_now_add=True)
    rating=models.CharField(choices= STAR_CHOICES,max_length=10)

    def __str__(self):
        return f'{self.reviewer.user.first_name} review on {self.doctor.user.first_name}'