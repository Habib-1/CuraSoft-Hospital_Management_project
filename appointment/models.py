from django.db import models
from patient.models import patient
from doctor.models import doctor
from doctor.models import available_time
# Create your models here.
APPOINTMENT_STATUS=(
    ('Pending','Pending'),
    ('Approved','Approved'),
    ('Cancelled','Cancelled'),
    ('Completed','Completed'),
)
APPOINTMENT_TYPE=(
    ('Online','Online'),
    ('Offline','Offline'),
)
class appointemt(models.Model):
    patient=models.ForeignKey(patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(doctor,on_delete=models.CASCADE)
    appointment_type=models.CharField(choices=APPOINTMENT_TYPE,max_length=10)
    appointment_status=models.CharField(choices=APPOINTMENT_STATUS,default="Pending",max_length=10)
    symptoms=models.TextField()
    time=models.ForeignKey(available_time,on_delete=models.CASCADE)
    canceled=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.patient.user.first_name} appointment with {self.doctor.user.first_name}'
