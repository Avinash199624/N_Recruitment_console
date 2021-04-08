from django.db import models

# Create your models here.
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

class User(AbstractUser):

    REQUIRED_FIELDS = ["username"]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    middle_name = models.CharField(max_length=30)
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,related_name="create_user")
    updated_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,related_name="modify_user")
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, help_text="Used for Soft Delete")

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

class UserProfile(models.Model):

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

    user = models.OneToOneField('User',on_delete=models.CASCADE, related_name="user_profile")
    gender = models.CharField(null=True, blank=True, choices=GENDER_CHOICES, max_length=20)
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    status = models.CharField(null=True, blank=True,choices=STATUS_CHOICES,default=NOT_DECIDED, max_length=20)
    higher_qualification = models.CharField(max_length=50, null=True, blank=True)
    local_address = models.ManyToManyField('user.Location',blank=True,related_name="local_address")
    permanent_address = models.ManyToManyField('user.Location',blank=True,related_name="permanent_address")
    created_by = models.ForeignKey('User',null=True, blank=True,on_delete=models.SET_NULL,related_name="create_userprofile")
    updated_by = models.ForeignKey('User',null=True, blank=True,on_delete=models.SET_NULL,related_name="modify_userprofile")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, help_text="Used for Soft Delete")

    def __str__(self):
        return self.user.username

class Location(models.Model):
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    address3 = models.CharField(max_length=200,null=True, blank=True)
    city = models.CharField(max_length=200,null=True, blank=True)
    state = models.CharField(max_length=200,null=True, blank=True)
    country = models.CharField(max_length=200,null=True, blank=True)
    postcode = models.CharField(max_length=20,null=True, blank=True)
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,related_name="create_location")
    updated_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,related_name="modify_location")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, help_text="Used for Soft Delete")

    def __str__(self):
        return u' '.join([self.address1, self.address2, self.address3 or '',
                          self.city or '', self.postcode or '',
                          self.country])


class RoleMaster(models.Model):

    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=30,null=True, blank=True)
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="create_role")
    updated_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="modify_role")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.role_name

class UserRoles(models.Model):
    role = models.ForeignKey('RoleMaster', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="create_userrole")
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="create_userrole")
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="create_user_role")
    updated_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="modify_user_role")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return ' '.join([self.user.username,self.role.role_name])


class PermissionMaster(models.Model):

    permission_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission_name = models.CharField(max_length=30, null=True, blank=True)
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="create_permission")
    updated_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="modify_permission")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.permission_name


class UserPermissions(models.Model):
    permission = models.ForeignKey('PermissionMaster', null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="permission")
    role_name = models.ForeignKey('RoleMaster', null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="user")
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="create_user_permission")
    updated_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="modify_user_permission")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return ' '.join([self.role_name.role_name,self.permission.permission_name])