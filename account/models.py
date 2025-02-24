from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, username,first_name,last_name,email,gender,age,address,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            age=age,
            address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username,first_name,last_name,email,gender,age,address,password):
        user=self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            age=age,
            address=address,
            password=password,
            )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.is_active=True
        user.save(using=self._db)
        return user

GENDER=[
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other'),
]
class Account(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(max_length=30,unique=True)
    email=models.EmailField(max_length=60,unique=True) 
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    gender=models.CharField(choices=GENDER,max_length=10,blank=True, null=True)
    age=models.IntegerField(blank=True, null=True)
    address=models.CharField(max_length=100,blank=True, null=True)

    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True) 
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name','gender','age','address']

    objects=AccountManager()

    def __str__(self):
        return self.email
    
    