from django.db import models

from django.contrib.auth.models import AbstractUser,PermissionsMixin
from neeri_recruitment_portal.validators import EmailValidator, UsernameValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.conf import settings

class BaseModel(models.Model):

    created_by = models.CharField(max_length=50, null=True, blank=True,help_text="username")
    updated_by = models.CharField(max_length=25, null=True, blank=True,help_text="username")
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, help_text="Used for Soft Delete")

    class Meta:
        abstract = True

class User(AbstractUser,BaseModel):

    REQUIRED_FIELDS = ["username"]
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Limiting the username input to accept only digits, ".", "-" and "_"
    username = models.CharField(
        _("username"),
        max_length=25,
        help_text=_(
            "Required. Between 5 and 25 characters. "
            "May only contain letters, digits, - (hyphen) and _ (underscore)."
        ),
        validators=[
            UsernameValidator(),
            MinLengthValidator(5, "Minimum 5 characters."),
        ],
        blank=True,
        unique=True
    )
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    middle_name = models.CharField(max_length=30,blank=True,null=True)
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.get_username()

    def get_email(self):
        email_field_name = self.get_email_field_name()
        return getattr(self, email_field_name, None)

    def set_email(self, new_mail):
        email_field_name = self.get_email_field_name()
        return setattr(self, email_field_name, new_mail)

class UserProfile(BaseModel):

    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'

    GENDER_CHOICES = [
        (GENDER_MALE,'Male'),
        (GENDER_FEMALE,'Female'),
    ]

    NOT_DECIDED = 'not_decided'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    ON_HOLD = 'on_hold'
    OTHER = 'other'

    STATUS_CHOICES = [
        (NOT_DECIDED,'Not Decided'),
        (ACCEPTED,'Accepted'),
        (REJECTED,'Rejected'),
        (ON_HOLD,'On Hold'),
        (OTHER,'Other'),
    ]

    SC = 'sc'
    ST = 'st'
    OBC = 'obc'
    GEN = 'gen'
    PWD = 'pwd'

    CASTE_CHOICES = [
        (SC,'SC'),
        (ST,'ST'),
        (OBC,'OBC'),
        (GEN,'GEN'),
        (PWD,'PWD'),
    ]

    user = models.OneToOneField('User',on_delete=models.CASCADE, related_name="user_profile")
    gender = models.CharField(null=True, blank=True, choices=GENDER_CHOICES, max_length=20)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    status = models.CharField(null=True, blank=True,choices=STATUS_CHOICES,default=NOT_DECIDED, max_length=20)
    local_address = models.OneToOneField('user.Location', on_delete=models.CASCADE, blank=True,null=True, related_name="local_address")
    permanent_address = models.OneToOneField('user.Location', on_delete=models.CASCADE, blank=True,null=True, related_name="permanent_address")
    date_of_birth_in_words = models.CharField(max_length=50, null=True, blank=True)
    place_of_birth = models.CharField(max_length=30, null=True, blank=True)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    father_address = models.OneToOneField('user.Location', on_delete=models.CASCADE, blank=True,null=True, related_name="father_address")
    father_occupation = models.CharField(max_length=30, null=True, blank=True)
    religion = models.CharField(max_length=30, null=True, blank=True)
    caste = models.CharField(max_length=30,choices=CASTE_CHOICES,null=True,blank=True)
    passport_number = models.IntegerField(null=True,blank=True)
    passport_expiry = models.DateField(null=True,blank=True)
    profile_photo = models.CharField(max_length=100, null=True, blank=True)
    fax_number = models.CharField(max_length=20, null=True, blank=True)
    is_indian_citizen = models.BooleanField(blank=True, null=True, default=True)
    whatsapp_id = models.CharField(max_length=50, null=True, blank=True)
    skype_id = models.CharField(max_length=50, null=True, blank=True)
    roles = models.ManyToManyField('user.RoleMaster', blank=True, null=True, related_name="user_roles")
    neeri_relation = models.ManyToManyField('NeeriRelation',blank=True,related_name="neeri_relations")
    documents = models.ManyToManyField('user.UserDocuments', blank=True, null=True, related_name="documents")
    education_details = models.ManyToManyField('user.UserEducationDetails', blank=True, null=True, related_name="education_details")
    experiences = models.ManyToManyField('user.UserExperienceDetails', blank=True, null=True, related_name="experiences")
    references = models.ManyToManyField('user.UserReference', blank=True, null=True, related_name="references")
    overseas_visits = models.ManyToManyField('user.OverseasVisits', blank=True, null=True, related_name="overseas_visits")
    languages = models.ManyToManyField('user.UserLanguages', blank=True, null=True, related_name="languages")
    published_papers = models.ManyToManyField('user.PublishedPapers', blank=True, null=True, related_name="published_papers")

    @property
    def profile_percentage(self):

        percent = {'gender': 2, 'mobile_no': 5, 'date_of_birth': 5, 'local_address': 5,
                   'permanent_address': 5, 'father_address': 5,'date_of_birth_in_words' : 2,
                   'place_of_birth': 2, 'father_name': 2, 'father_occupation': 2, 'religion': 2,
                   'caste': 2, 'passport_number': 2, 'passport_expiry': 2, 'profile_photo': 5,
                   'fax_number': 1, 'is_indian_citizen': 1, 'whatsapp_id': 5, 'skype_id': 5,
                   'neeri_relation': 5, 'documents': 5, 'education_details': 5, 'experiences': 5,
                   'references': 5, 'overseas_visits': 5, 'languages': 5, 'published_papers': 5,
                    }

        total = 0
        if self.gender:
            total += percent.get('gender', 0)

        if self.mobile_no:
            total += percent.get('mobile_no', 0)

        if self.date_of_birth:
            total += percent.get('date_of_birth', 0)

        if self.local_address:
            total += percent.get('local_address', 0)

        if self.permanent_address:
            total += percent.get('permanent_address', 0)

        if self.father_address:
            total += percent.get('father_address', 0)

        if self.date_of_birth_in_words:
            total += percent.get('date_of_birth_in_words', 0)

        if self.place_of_birth:
            total += percent.get('place_of_birth', 0)

        if self.father_name:
            total += percent.get('father_name', 0)

        if self.father_occupation:
            total += percent.get('father_occupation', 0)

        if self.religion:
            total += percent.get('religion', 0)

        if self.caste:
            total += percent.get('caste', 0)

        if self.passport_number:
            total += percent.get('passport_number', 0)

        if self.passport_expiry:
            total += percent.get('passport_expiry', 0)

        if self.profile_photo:
            total += percent.get('profile_photo', 0)

        if self.fax_number:
            total += percent.get('fax_number', 0)

        if self.is_indian_citizen:
            total += percent.get('is_indian_citizen', 0)

        if self.whatsapp_id:
            total += percent.get('whatsapp_id', 0)

        if self.skype_id:
            total += percent.get('skype_id', 0)

        if self.neeri_relation:
            total += percent.get('neeri_relation', 0)

        if self.documents:
            total += percent.get('documents', 0)

        if self.education_details:
            total += percent.get('education_details', 0)

        if self.experiences:
            total += percent.get('experiences', 0)

        if self.references:
            total += percent.get('references', 0)

        if self.overseas_visits:
            total += percent.get('overseas_visits', 0)

        if self.languages:
            total += percent.get('languages', 0)

        if self.published_papers:
            total += percent.get('published_papers', 0)

        return str(total) + " %"

    def __str__(self):
        return self.user.username

class NeeriUserProfile(BaseModel):

    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'

    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
    ]

    SC = 'sc'
    ST = 'st'
    OBC = 'obc'
    GEN = 'gen'
    PWD = 'pwd'

    CASTE_CHOICES = [
        (SC, 'SC'),
        (ST, 'ST'),
        (OBC, 'OBC'),
        (GEN, 'GEN'),
        (PWD, 'PWD'),
    ]

    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name="neeri_user_profile")
    gender = models.CharField(null=True, blank=True, choices=GENDER_CHOICES, max_length=20)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.OneToOneField('user.Location', on_delete=models.CASCADE, blank=True,null=True, related_name="neeri_user_address")
    religion = models.CharField(max_length=30, null=True, blank=True)
    caste = models.CharField(max_length=30,choices=CASTE_CHOICES, null=True, blank=True)
    profile_photo = models.CharField(max_length=100, null=True, blank=True)
    roles = models.ManyToManyField('user.RoleMaster',blank=True,null=True,related_name="neeri_user_roles")

    def __str__(self):
        return self.user.username


class Location(BaseModel):

    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    address3 = models.CharField(max_length=200,null=True, blank=True)
    city = models.CharField(max_length=200,null=True, blank=True)
    state = models.CharField(max_length=200,null=True, blank=True)
    country = models.CharField(max_length=200,null=True, blank=True)
    postcode = models.CharField(max_length=20,null=True, blank=True)
    telephone_no = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return u' '.join([self.address1, self.address2, self.address3 or '',
                          self.city or '', self.postcode or '',
                          self.country])

class RoleMaster(BaseModel):

    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=30,null=True, blank=True)

    def __str__(self):
        return self.role_name

class PermissionMaster(BaseModel):

    permission_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission_name = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.permission_name

class UserRoles(BaseModel):

    role = models.ForeignKey('RoleMaster', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="create_userrole")
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="create_userrole")

    def __str__(self):
        return ' '.join([self.user.username,self.role.role_name])


class UserPermissions(BaseModel):

    permission = models.ForeignKey('PermissionMaster', null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="permission")
    role = models.ForeignKey('RoleMaster', null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="user")

    def __str__(self):
        return ' '.join([self.role.role_name,self.permission.permission_name])

class UserDocuments(BaseModel):

    doc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doc_file_path = models.CharField(max_length=200, null=True, blank=True,help_text="path to document")
    doc_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.doc_name


class OverseasVisits(BaseModel):

    USA = 'usa'
    UK = 'uk'

    COUNTRY_CHOICES = [
        (USA,'USA'),
        (UK,'UK'),
    ]

    country_visited = models.CharField(max_length=50,choices=COUNTRY_CHOICES, null=True, blank=True)
    date_of_visit = models.DateField(null=True,blank=True)
    duration_of_visit = models.CharField(max_length=50, null=True, blank=True)
    purpose_of_visit = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.country_visited

class UserReference(BaseModel):

    reference_name = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    address = models.OneToOneField('Location',on_delete=models.CASCADE, related_name="referee_address")

    def __str__(self):
        return self.reference_name


class NeeriRelation(BaseModel):

    relation_name = models.CharField(max_length=50, null=True, blank=True)
    designation =models.CharField(max_length=50, null=True, blank=True)
    center_name = models.CharField(max_length=50, null=True, blank=True)
    relation = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.relation_name

class UserEducationDetails(BaseModel):

    PERCENTAGE = '%'
    CLASS = 'class'
    DIVISION = 'division'

    SCORE_UNIT_CHOICES = [
        (PERCENTAGE, '%'),
        (CLASS, 'class'),
        (DIVISION, 'division'),
    ]

    exam_name = models.CharField(max_length=50, null=True, blank=True)
    university = models.CharField(max_length=50, null=True, blank=True,help_text="university")
    college_name = models.CharField(max_length=50, null=True, blank=True)
    passing_year = models.CharField(max_length=50, null=True, blank=True)
    score = models.CharField(max_length=50, null=True, blank=True,help_text="score")
    score_unit = models.CharField(max_length=30,choices=SCORE_UNIT_CHOICES, null=True, blank=True)
    specialization = models.CharField(max_length=50, null=True, blank=True, help_text="special subject")

    def __str__(self):
        return self.exam_name

class UserExperienceDetails(BaseModel):

    PERMANENT = 'permanent'
    TEMPORARY = 'temporary'

    EMPLOYMENT_TYPE_CHOICES = [
        (PERMANENT,'PERMANENT'),
        (TEMPORARY,'TEMPORARY'),
    ]
    employer_name = models.CharField(max_length=50, null=True, blank=True)
    post = models.CharField(max_length=30, null=True, blank=True)
    employed_from = models.DateField(null=True, blank=True)
    employed_to = models.DateField(null=True, blank=True)
    employment_type = models.CharField(max_length=30,choices=EMPLOYMENT_TYPE_CHOICES, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    grade = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.employer_name


class PublishedPapers(BaseModel):

    paper_title = models.CharField(max_length=30, null=True, blank=True)
    attachments = models.ManyToManyField('user.UserDocuments',blank=True,related_name="attachments")

    def __str__(self):
        return self.paper_title

class UserLanguages(BaseModel):

    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    EXPERT = 'expert'

    LEVEL_CHOICES = [
        (BEGINNER,'BEGINNER'),
        (INTERMEDIATE,'INTERMEDIATE'),
        (EXPERT,'EXPERT')
    ]

    name = models.CharField(max_length=30, null=True, blank=True)
    read_level = models.CharField(max_length=20,choices=LEVEL_CHOICES, null=True, blank=True)
    write_level = models.CharField(max_length=20,choices=LEVEL_CHOICES, null=True, blank=True)
    speak_level = models.CharField(max_length=20,choices=LEVEL_CHOICES, null=True, blank=True)
    exam_passed = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class OtherInfo(BaseModel):
    bond_details = models.CharField(max_length=100, null=True, blank=True)
    notice_period_min = models.CharField(max_length=30, null=True, blank=True)
    notice_period_max = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.bond_details