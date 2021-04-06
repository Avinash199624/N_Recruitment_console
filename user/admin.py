from django.contrib import admin
from django.contrib.admin import register
from user.models import User,UserProfile,Location

# Register your models here.

@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','created_at']

@register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','gender','phone_no','mobile_no','status','higher_qualification' ]


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['address1','address2','address3','city','state','country','postcode' ]