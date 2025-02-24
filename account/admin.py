from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('username','email','first_name','last_name','gender','age','address','is_active')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('username', 'first_name', 'last_name', 'gender', 'age', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
     
    )  
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username','email','first_name',)    

    ordering = ('date_joined',)
    
admin.site.register(Account,AccountAdmin)