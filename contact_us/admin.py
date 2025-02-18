from django.contrib import admin
from .models import contact_us
# Register your models here.

class contact_usAdmin(admin.ModelAdmin):
    list_display=['name','email','subject','date']
    #search_fields=['name','email','subject','date']
    list_filter=['date']
    list_per_page=10
admin.site.register(contact_us,contact_usAdmin)