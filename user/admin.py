from django.contrib import admin
from django.contrib.admin import register
from user.models import User,UserProfile,RoleMaster,UserRoles,Location,PermissionMaster,UserPermissions

# Register your models here.

@register(PermissionMaster)
class PermissionMasterAdmin(admin.ModelAdmin):
    list_display = ['permission_id','permission_name']

@register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ['role_name','permission']

@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','created_at']

@register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','gender','phone_no','mobile_no','status','higher_qualification' ]

@register(RoleMaster)
class RoleMasterAdmin(admin.ModelAdmin):
    list_display = ['role_name',]

@register(UserRoles)
class UserRolesAdmin(admin.ModelAdmin):
    list_display = ['user','role']
    list_filter = ['role',]

@register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['address1','address2','address3','city','state','country','postcode' ]