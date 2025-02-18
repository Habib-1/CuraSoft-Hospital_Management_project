from django.db import models

# Create your models here.
class contact_us(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    subject=models.CharField(max_length=50)
    message=models.TextField()
    date=models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural='contact_us'
        
    def __str__(self):
        return self.name