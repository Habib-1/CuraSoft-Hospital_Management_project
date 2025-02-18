from django.contrib import admin
from .models import patient
# Register your models here.
class patientAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','phone',]
    list_filter=['user']
    list_per_page=10

    def first_name(self, obj):
        return obj.user.first_name
    def last_name(self, obj):
        return obj.user.last_name
    
admin.site.register(patient,patientAdmin)