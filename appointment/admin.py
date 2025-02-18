from django.contrib import admin
from .models import appointemt
# Register your models here.
class appointemtAdmin(admin.ModelAdmin):
    list_display=['patient_name','doctor_name','appointment_type','appointment_status','time','canceled']
    list_filter=['appointment_status','appointment_type','canceled']
    list_per_page=10

    def patient_name(self,obj):
        return obj.patient.user.first_name
    
    def doctor_name(self,obj):
        return obj.doctor.user.first_name
admin.site.register(appointemt,appointemtAdmin)