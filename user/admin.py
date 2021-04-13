from django.contrib import admin
from django.contrib.admin import register
from user.models import User,UserProfile,RoleMaster,UserRoles,Location,PermissionMaster,\
    UserPermissions,NeeriUserProfile,NeeriRelation,UserEducationDetails

# Register your models here.

@register(UserEducationDetails)
class UserEducationDetailsAdmin(admin.ModelAdmin):
    list_display = ['exam_name','university','college_name','passing_year','score','score_unit','specialization']

@register(NeeriRelation)
class NeeriRelationAdmin(admin.ModelAdmin):
    list_display = ['name','designation']

@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id','first_name','last_name','email']

@register(PermissionMaster)
class PermissionMasterAdmin(admin.ModelAdmin):
    list_display = ['permission_id','permission_name']

@register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ['permission','role']

@register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','gender','mobile_no','status' ]

@register(NeeriUserProfile)
class NeeriUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','gender','mobile_no']

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