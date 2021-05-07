from django.contrib import admin
from django.contrib.admin import register
from user.models import User,UserProfile,RoleMaster,UserRoles,Location,PermissionMaster,\
    UserPermissions,NeeriUserProfile,NeeriRelation,UserEducationDetails,UserExperienceDetails,\
    UserDocuments,UserLanguages,UserReference,OverseasVisits,PublishedPapers,ProfessionalTraining,OtherInformation

# Register your models here.
@register(OtherInformation)
class OtherInformationAdmin(admin.ModelAdmin):
    list_display = ['bond_title','organisation_name','bond_start_date','bond_end_date','notice_period_min','notice_period_max']


@register(UserEducationDetails)
class UserEducationDetailsAdmin(admin.ModelAdmin):
    list_display = ['exam_name','university','college_name','passing_year','score','score_unit','specialization']

@register(UserExperienceDetails)
class UserExperienceDetailsAdmin(admin.ModelAdmin):
    list_display = ['employer_name','post','employed_from','employed_to','employment_type','salary','grade']

@register(UserDocuments)
class UserDocumentsAdmin(admin.ModelAdmin):
    list_display = ['doc_id','doc_file_path','doc_name']

@register(UserLanguages)
class UserLanguagesAdmin(admin.ModelAdmin):
    list_display = ['name','read_level','write_level','speak_level','exam_passed']

@register(ProfessionalTraining)
class ProfessionalTrainingAdmin(admin.ModelAdmin):
    list_display = ['title','description','from_date','to_date']

@register(UserReference)
class UserReferenceAdmin(admin.ModelAdmin):
    list_display = ['reference_name','position','address']

@register(OverseasVisits)
class OverseasVisitsAdmin(admin.ModelAdmin):
    list_display = ['country_visited','date_of_visit','duration_of_visit','purpose_of_visit']

@register(PublishedPapers)
class PublishedPapersAdmin(admin.ModelAdmin):
    list_display = ['paper_title']

@register(NeeriRelation)
class NeeriRelationAdmin(admin.ModelAdmin):
    list_display = ['relation_name','designation','center_name','relation']

@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id','first_name','last_name','email', 'mobile_no']

@register(PermissionMaster)
class PermissionMasterAdmin(admin.ModelAdmin):
    list_display = ['permission_id','permission_name']

@register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ['permission','role']

@register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','gender','status' ]

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