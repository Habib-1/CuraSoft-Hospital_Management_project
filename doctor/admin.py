from django.contrib import admin
from .models import doctor,designation,specialization,available_time,review
# Register your models here.
class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
admin.site.register(designation,DesignationAdmin)
admin.site.register(specialization)
admin.site.register(available_time)
admin.site.register(doctor)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['reviewer','doctor','rating','date']
    list_filter=['date']
    list_per_page=10
admin.site.register(review,ReviewAdmin)