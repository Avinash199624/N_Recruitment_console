from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

import job_posting
from job_posting.models import JobPosting, Division
from user.models import (
    User,
    UserProfile,
    Location,
    UserEducationDetails,
    UserExperienceDetails,
    NeeriRelation,
    UserReference,
    OverseasVisits,
    UserLanguages,
    UserDocuments,
    PublishedPapers,
    ProfessionalTraining,
    OtherInformation,
    NeeriUserProfile,
    MentorMaster,
    Trainee,
    RelaxationCategoryMaster,
    RelaxationMaster,
    UserAuthentication, FellowshipMaster, ReligionMaster,
)


class AuthTokenCustomSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")
        attrs["user"] = user
        return attrs


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "address1",
            "address2",
            "address3",
            "city",
            "state",
            "country",
            "postcode",
            "telephone_no",
        )

    def update(self, instance, validated_data):

        instance.address1 = validated_data.get("address1") or instance.address1

        instance.address2 = validated_data.get("address2")

        instance.address3 = validated_data.get("address3")

        instance.city = validated_data.get("city") or instance.city

        instance.state = validated_data.get("state") or instance.state

        instance.country = validated_data.get("country") or instance.country

        instance.postcode = validated_data.get("postcode") or instance.postcode

        instance.telephone_no = (
            validated_data.get("telephone_no") or instance.telephone_no
        )

        instance.save()

    def save(self, validated_data):
        location = Location.objects.create(
            address1=validated_data.get("address1"),
            address2=validated_data.get("address2"),
            address3=validated_data.get("address3"),
            city=validated_data.get("city"),
            state=validated_data.get("state"),
            country=validated_data.get("country"),
            postcode=validated_data.get("postcode"),
            telephone_no=validated_data.get("telephone_no"),
        )
        return location.id


class RelaxationCategoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelaxationCategoryMaster
        fields = (
            "relaxation_cat_id",
            "relaxation_category",
        )


class RelaxationMasterSerializer(serializers.ModelSerializer):
    relaxation = RelaxationCategoryMasterSerializer()
    age_relaxation = serializers.SerializerMethodField(
        method_name="get_age_relaxation", required=False
    )
    fee_relaxation = serializers.SerializerMethodField(
        method_name="get_fee_relaxation", required=False
    )

    class Meta:
        model = RelaxationMaster
        fields = (
            "relaxation_rule_id",
            "relaxation",
            "age_relaxation",
            "fee_relaxation",
        )

    def get_age_relaxation(self, obj):
        age_relaxation = f"{obj.age_relaxation} years"
        return age_relaxation

    def get_fee_relaxation(self, obj):
        fee_relaxation = f"{obj.fee_relaxation} %"
        return fee_relaxation


class UserProfileSerializer(serializers.ModelSerializer):
    local_address = LocationSerializer(required=False)
    permanent_address = LocationSerializer(required=False)
    father_address = LocationSerializer(required=False)

    class Meta:
        model = UserProfile

        profile_names = (
            "local_address",
            "permanent_address",
            "father_address",
        )
        fields = (
            "gender",
            # "mobile_no",
            "date_of_birth",
            "profile_photo",
            "status",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "is_deleted",
        ) + profile_names


class CompareApplicantSerializer(serializers.ModelSerializer):
    name_of_applicant = serializers.CharField(source="user.get_full_name")
    mobile_no = serializers.CharField(source="user.mobile_no")
    age_of_applicant = serializers.SerializerMethodField(
        method_name="get_age_of_applicant", read_only=True
    )
    # application_id = serializers.SerializerMethodField(
    #     method_name="get_application_id", read_only=True
    # )
    specialization_in = serializers.SerializerMethodField(
        method_name="get_specialization", read_only=True
    )
    exp_in_years = serializers.SerializerMethodField(
        method_name="get_exp_in_years", read_only=True
    )

    class Meta:
        model = UserProfile

        fields = (
            # todo: job id ---> application no.
            # "application_id",
            "user_id",
            "name_of_applicant",
            "date_of_birth",
            "age_of_applicant",
            "gender",
            "caste",
            "mobile_no",
            "specialization_in",
            "exp_in_years",
        )

    def get_specialization(self, obj):
        specialization_in = obj.education_details.filter()
        serializer = SubjectSpecializationSerializer(specialization_in, many=True)
        return serializer.data

    # def get_application_id(self, obj):
    #     app_id = obj.notification_id
    #     serializer = JobPostingSerializer(app_id)
    #     return serializer.data

    def get_exp_in_years(self, obj):
        exp_in_years = obj.experiences.filter()
        serializer = EmployeeExperienceSerializer(exp_in_years, many=True)
        return serializer.data

    def get_age_of_applicant(self, obj):
        today = date.today()
        age_of_applicant = (
            today.year
            - obj.date_of_birth.year
            - (
                (today.month, today.day)
                < (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        )
        return age_of_applicant


class SubjectSpecializationSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField(method_name="get_score", read_only=True)

    class Meta:
        model = UserEducationDetails
        fields = (
            "specialization",
            "score",
        )

    def get_score(self, obj):
        score = obj.score + obj.score_unit
        return score


class JobPostingSerializer(serializers.ModelSerializer):
    notification_id = serializers.SerializerMethodField(
        method_name="get_job_id", read_only=True
    )

    class Meta:
        model = JobPosting
        fields = ("notification_id",)

    def get_job_id(self, obj):
        job_id = obj.notification_id
        return job_id


class EmployeeExperienceSerializer(serializers.ModelSerializer):
    years = serializers.SerializerMethodField(
        method_name="get_experience", read_only=True
    )

    class Meta:
        model = UserExperienceDetails
        fields = ("years",)

    def get_experience(self, obj):
        year = abs(obj.employed_from.year - obj.employed_to.year)
        month = abs(obj.employed_from.month - obj.employed_to.month)
        years = str(year) + " year and " + str(month) + " months"
        return years


class RoleMasterSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(source="id")
    role_name = serializers.CharField(source="name")

    class Meta:
        model = Group
        fields = (
            "role_id",
            "role_name",
        )


class UserRolesSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(source="name")

    class Meta:
        model = Group
        fields = ("user_role",)


class UserPermissionSerializer(serializers.ModelSerializer):
    user_permission = serializers.CharField(source="name")

    class Meta:
        model = Group
        fields = ("user_permission",)


class UserAuthenticationSerializer(serializers.ModelSerializer):
    mobile_no = serializers.CharField(source="user.mobile_no")
    email = serializers.EmailField(source="user.email")
    user_id = serializers.UUIDField(source="user.user_id")
    middle_name = serializers.CharField(source="user.middle_name")
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    is_deleted = serializers.CharField(source="user.is_deleted")

    class Meta:
        model = UserAuthentication
        fields = (
            "user_id",
            "is_suspended",
            "is_locked",
            "first_name",
            "middle_name",
            "last_name",
            "mobile_no",
            "email",
            "is_deleted",
        )


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(required=False)

    # user_roles = serializers.SerializerMethodField(
    #     method_name="get_user_roles", read_only=True
    # )

    # user_permissions = serializers.SerializerMethodField(
    #     method_name="get_user_permissions", read_only=True
    # )

    username = serializers.SerializerMethodField(
        method_name="get_username", read_only=True
    )
    is_first_login = serializers.SerializerMethodField(
        method_name="get_first_login", read_only=True
    )

    class Meta:
        model = User

        # profile_names = ("user_profile", "user_roles", "user_permissions")
        profile_names = ("user_profile",)

        fields = (
            "user_id",
            "username",
            "email",
            "mobile_no",
            "created_at",
            "is_deleted",
            "is_first_login",
            # "user_roles",
        ) + profile_names

    def get_username(self, obj):
        return obj.get_full_name()

    def get_first_login(self, obj):
        auth = UserAuthentication.objects.get(user=obj)
        is_first_login = auth.is_first_login
        return is_first_login

    # def get_first_login(self, obj):
    #     auth = UserAuthentication.objects.get(user__user_id=obj.user_id)
    #     is_first_login = UserAuthenticationSerializer(auth)
    #     return is_first_login

    # def get_user_roles(self, obj):
    #     user_roles = UserRoles.objects.filter(user=obj)
    #     serializer = UserRolesSerializer(user_roles, many=True)
    #     return serializer.data
    #
    # def get_user_permissions(self, obj):
    #     user_roles = UserRoles.objects.filter(user=obj)
    #     role_names = [role.role.role_name for role in user_roles]
    #     roles = RoleMaster.objects.filter(role_name__in=role_names)
    #     user_permissions = UserPermissions.objects.filter(role__in=roles).distinct('permission')
    #     serializer = UserPermissionSerializer(user_permissions, many=True)
    #     return serializer.data


class NeeriUserSerializer(serializers.ModelSerializer):
    # n_user_profile = UserProfileSerializer(required=False)

    # user_roles = serializers.SerializerMethodField(
    #     method_name="get_user_roles", read_only=True
    # )

    # user_permissions = serializers.SerializerMethodField(
    #     method_name="get_user_permissions", read_only=True
    # )

    username = serializers.SerializerMethodField(
        method_name="get_username", read_only=True
    )

    class Meta:
        model = User

        # profile_names = ("user_profile", "user_roles", "user_permissions")
        # profile_names = ("user_profile",)

        fields = (
            "user_id",
            "username",
            "email",
            "mobile_no",
            "created_at",
            "is_deleted",
            # "user_roles",
        )

    def get_username(self, obj):
        return obj.email or obj.get_full_name()

    # def get_user_roles(self, obj):
    #     user_roles = UserRoles.objects.filter(user=obj)
    #     serializer = UserRolesSerializer(user_roles, many=True)
    #     return serializer.data
    #
    # def get_user_permissions(self, obj):
    #     user_roles = UserRoles.objects.filter(user=obj)
    #     role_names = [role.role.role_name for role in user_roles]
    #     roles = RoleMaster.objects.filter(role_name__in=role_names)
    #     user_permissions = UserPermissions.objects.filter(role__in=roles).distinct('permission')
    #     serializer = UserPermissionSerializer(user_permissions, many=True)
    #     return serializer.data


class CustomUserSerializer(serializers.ModelSerializer):
    phone_no = serializers.SerializerMethodField(
        method_name="get_phone_no", read_only=True
    )
    gender = serializers.SerializerMethodField(method_name="get_gender", read_only=True)
    date_of_birth = serializers.SerializerMethodField(
        method_name="get_date_of_birth", read_only=True
    )
    status = serializers.SerializerMethodField(method_name="get_status", read_only=True)
    local_address = serializers.SerializerMethodField(
        method_name="get_local_address", read_only=True
    )
    permanent_address = serializers.SerializerMethodField(
        method_name="get_permanent_address", read_only=True
    )
    user_roles = serializers.SerializerMethodField(
        method_name="get_user_roles", read_only=True
    )
    user_permissions = serializers.SerializerMethodField(
        method_name="get_user_permissions", read_only=True
    )

    class Meta:
        model = User

        fields = (
            "user_id",
            "username",
            "email",
            "created_at",
            "status",
            "gender",
            "date_of_birth",
            "mobile_no",
            "phone_no",
            "local_address",
            "permanent_address",
            "is_deleted",
            "user_roles",
            "user_permissions",
        )

    def get_phone_no(self, obj):
        return hasattr(obj, "user_profile") and obj.user_profile.phone_no

    def get_gender(self, obj):
        return hasattr(obj, "user_profile") and obj.user_profile.gender

    def get_date_of_birth(self, obj):
        return hasattr(obj, "user_profile") and obj.user_profile.date_of_birth

    def get_status(self, obj):
        return hasattr(obj, "user_profile") and obj.user_profile.status

    def get_local_address(self, obj):
        try:
            local_address = obj.user_profile.local_address.all()
            serializer = LocationSerializer(local_address, many=True)
            return serializer.data
        except:
            return None

    def get_permanent_address(self, obj):
        try:
            permanent_address = obj.user_profile.permanent_address.all()
            serializer = LocationSerializer(permanent_address, many=True)
            return serializer.data
        except:
            return None

    def get_user_roles(self, obj):
        groups = obj.groups.all()
        serializer = UserRolesSerializer(groups, many=True)
        return serializer.data

    def get_user_permissions(self, obj):
        groups = obj.groups.all()
        serializer = UserPermissionSerializer(groups, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username") or instance.username
        instance.email = validated_data.get("email") or instance.email
        instance.created_at = validated_data.get("created_at") or instance.created_at
        try:
            local_address_instance = instance.user_profile.local_address.filter()
            permanent_address_instance = (
                instance.user_profile.permanent_address.filter()
            )
            local_address_data = validated_data.get("local_address")[0]
            permanent_address_data = validated_data.get("permanent_address")[0]

            if instance.user_profile:
                instance.user_profile.phone_no = (
                    validated_data.get("phone_no") or instance.user_profile.phone_no
                )

                instance.mobile_no = (
                    validated_data.get("mobile_no") or instance.mobile_no
                )

                instance.user_profile.gender = (
                    validated_data.get("gender") or instance.user_profile.gender
                )

                instance.user_profile.date_of_birth = (
                    validated_data.get("date_of_birth")
                    or instance.user_profile.date_of_birth
                )

                instance.user_profile.status = (
                    validated_data.get("status") or instance.user_profile.status
                )

            if local_address_instance:
                local_address_instance[0].address1 = (
                    local_address_data.get("address1")
                    or local_address_instance[0].address1
                )
                local_address_instance[0].address2 = (
                    local_address_data.get("address2")
                    or local_address_instance[0].address2
                )
                local_address_instance[0].address3 = (
                    local_address_data.get("address3")
                    or local_address_instance[0].address3
                )
                local_address_instance[0].city = (
                    local_address_data.get("city") or local_address_instance[0].city
                )
                local_address_instance[0].state = (
                    local_address_data.get("state") or local_address_instance[0].state
                )
                local_address_instance[0].country = (
                    local_address_data.get("country")
                    or local_address_instance[0].country
                )

                local_address_instance[0].postcode = (
                    local_address_data.get("postcode")
                    or local_address_instance[0].postcode
                )
                local_address_instance[0].save()

            if permanent_address_instance:
                permanent_address_instance[0].address1 = (
                    permanent_address_data.get("address1")
                    or permanent_address_instance[0].address1
                )

                permanent_address_instance[0].address2 = (
                    permanent_address_data.get("address2")
                    or permanent_address_instance[0].address2
                )

                permanent_address_instance[0].address3 = (
                    permanent_address_data.get("address3")
                    or permanent_address_instance[0].address3
                )

                permanent_address_instance[0].city = (
                    permanent_address_data.get("city")
                    or permanent_address_instance[0].city
                )

                permanent_address_instance[0].state = (
                    permanent_address_data.get("state")
                    or permanent_address_instance[0].state
                )
                permanent_address_instance[0].country = (
                    permanent_address_data.get("country")
                    or permanent_address_instance[0].country
                )

                permanent_address_instance[0].postcode = (
                    permanent_address_data.get("postcode")
                    or permanent_address_instance[0].postcode
                )
                permanent_address_instance[0].save()
            instance.user_profile.save()
            instance.save()
        except:
            user_profile_local_address = validated_data["local_address"]
            user_profile_permanent_address = validated_data["permanent_address"]

            local_address = Location.objects.create(
                address1=user_profile_local_address[0]["address1"],
                address2=user_profile_local_address[0]["address2"],
                address3=user_profile_local_address[0]["address3"],
                city=user_profile_local_address[0]["city"],
                state=user_profile_local_address[0]["state"],
                country=user_profile_local_address[0]["country"],
                postcode=user_profile_local_address[0]["postcode"],
            )

            permanent_address = Location.objects.create(
                address1=user_profile_permanent_address[0]["address1"],
                address2=user_profile_permanent_address[0]["address2"],
                address3=user_profile_permanent_address[0]["address3"],
                city=user_profile_permanent_address[0]["city"],
                state=user_profile_permanent_address[0]["state"],
                country=user_profile_permanent_address[0]["country"],
                postcode=user_profile_permanent_address[0]["postcode"],
            )

            user_profile = UserProfile.objects.create(
                user=instance,
                gender=validated_data["gender"],
                phone_no=validated_data["phone_no"],
                # mobile_no=validated_data['mobile_no'],
                date_of_birth=validated_data["date_of_birth"],
                status=validated_data["status"],
            )
            user_profile.local_address.add(local_address)
            user_profile.permanent_address.add(permanent_address)

            instance.user_profile = user_profile
            instance.save()

    def save(self, instance, validated_data):
        if not hasattr(instance, "user_profile"):
            user_profile = UserProfile.objects.create(
                user=instance,
                gender=validated_data.get("gender"),
                phone_no=validated_data.get("phone_no"),
                # mobile_no = validated_data['mobile_no'] if 'mobile_no' in validated_data else None,
                date_of_birth=validated_data.get("date_of_birth"),
                status=validated_data.get("status"),
            )
            if "local_address" in validated_data:
                user_profile_local_address = validated_data["local_address"]
                local_address = Location.objects.create(
                    address1=user_profile_local_address[0]["address1"],
                    address2=user_profile_local_address[0]["address2"],
                    address3=user_profile_local_address[0]["address3"],
                    city=user_profile_local_address[0]["city"],
                    state=user_profile_local_address[0]["state"],
                    country=user_profile_local_address[0]["country"],
                    postcode=user_profile_local_address[0]["postcode"],
                )
                user_profile.local_address.add(local_address)

            if "permanent_address" in validated_data:
                user_profile_permanent_address = validated_data["permanent_address"]
                permanent_address = Location.objects.create(
                    address1=user_profile_permanent_address[0]["address1"],
                    address2=user_profile_permanent_address[0]["address2"],
                    address3=user_profile_permanent_address[0]["address3"],
                    city=user_profile_permanent_address[0]["city"],
                    state=user_profile_permanent_address[0]["state"],
                    country=user_profile_permanent_address[0]["country"],
                    postcode=user_profile_permanent_address[0]["postcode"],
                )
                user_profile.permanent_address.add(permanent_address)


class ApplicantUserPersonalInformationSerializer(serializers.ModelSerializer):
    mobile_no = serializers.CharField(source="user.mobile_no")
    email = serializers.EmailField(source="user.email")
    user_id = serializers.UUIDField(source="user.user_id")
    middle_name = serializers.CharField(
        source="user.middle_name", required=False, allow_blank=True
    )
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    relaxation_rule = RelaxationMasterSerializer()
    passport_expiry = serializers.DateField(
        format="%Y-%m-%d", input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = UserProfile
        fields = (
            "user_id",
            "first_name",
            "middle_name",
            "last_name",
            "status",
            "gender",
            "mobile_no",
            "date_of_birth",
            "date_of_birth_in_words",
            "place_of_birth",
            # "local_address",
            # "permanent_address",
            "father_name",
            # "father_address",
            "father_occupation",
            "religion",
            "caste",
            "passport_number",
            "passport_expiry",
            "fax_number",
            # "nationality",
            "relaxation_rule",
            "is_indian_citizen",
            "profile_photo",
            "whatsapp_id",
            "skype_id",
            "is_fresher",
            "email",
        )

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status") or instance.status
        instance.gender = validated_data.get("gender") or instance.gender
        instance.date_of_birth = (
            validated_data.get("date_of_birth") or instance.date_of_birth
        )
        instance.date_of_birth_in_words = (
            validated_data.get("date_of_birth_in_words")
            or instance.date_of_birth_in_words
        )
        instance.place_of_birth = validated_data.get("place_of_birth")
        instance.father_name = validated_data.get("father_name") or instance.father_name
        instance.father_occupation = validated_data.get("father_occupation")
        instance.religion = validated_data.get("religion") or instance.religion
        instance.caste = validated_data.get("caste") or instance.caste
        instance.passport_number = validated_data.get("passport_number")
        instance.passport_expiry = validated_data.get("passport_expiry")
        instance.profile_photo = (
            validated_data.get("profile_photo") or instance.profile_photo
        )
        instance.whatsapp_id = validated_data.get("whatsapp_id")
        instance.skype_id = validated_data.get("skype_id")
        instance.fax_number = validated_data.get("fax_number")
        instance.is_indian_citizen = (
            validated_data.get("is_indian_citizen") or instance.is_indian_citizen
        )
        instance.is_fresher = validated_data.get("is_fresher") or instance.is_fresher
        instance.user.first_name = (
            validated_data.get("first_name") or instance.user.first_name
        )
        instance.user.last_name = (
            validated_data.get("last_name") or instance.user.last_name
        )
        instance.user.middle_name = validated_data.get("middle_name")
        instance.is_fresher = validated_data["is_fresher"]
        instance.is_indian_citizen = validated_data["is_indian_citizen"]
        instance.user.save()
        relaxation_rule = RelaxationMaster.objects.get(
            relaxation_rule_id=validated_data["relaxation_rule"]["relaxation_rule_id"]
        )
        instance.relaxation_rule = relaxation_rule
        instance.save()

    def save(self, validated_data):
        user = User.objects.get(user_id=validated_data["user_id"])
        user.first_name = validated_data.get("first_name")
        user.middle_name = validated_data.get("middle_name")
        user.last_name = validated_data.get("last_name")
        user.save()

        user_profile = UserProfile.objects.create(
            user=user,
            gender=validated_data.get("gender"),
            date_of_birth=validated_data.get("date_of_birth"),
            status=validated_data.get("status"),
            date_of_birth_in_words=validated_data.get("date_of_birth_in_words"),
            place_of_birth=validated_data.get("place_of_birth"),
            father_name=validated_data.get("father_name"),
            father_occupation=validated_data.get("father_occupation"),
            religion=validated_data.get("religion"),
            caste=validated_data.get("caste"),
            passport_number=validated_data.get("passport_number"),
            passport_expiry=validated_data.get("passport_expiry"),
            profile_photo=validated_data.get("profile_photo"),
            fax_number=validated_data.get("fax_number"),
            is_indian_citizen=validated_data.get("is_indian_citizen"),
            whatsapp_id=validated_data.get("whatsapp_id"),
            skype_id=validated_data.get("skype_id"),
            is_fresher=validated_data.get("is_fresher"),
        )
        relaxation_rule = RelaxationMaster.objects.get(
            relaxation_rule_id=validated_data["relaxation_rule"]["relaxation_rule_id"]
        )
        user_profile.relaxation_rule = relaxation_rule
        user_profile.save()

        return user_profile.user.user_id


class ApplicantIsAddressSameSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.user_id", read_only=True)
    is_father_address_same_as_local = serializers.BooleanField()
    is_permenant_address_same_as_local = serializers.BooleanField()

    class Meta:
        model = UserProfile
        fields = (
            "user_id",
            "is_permenant_address_same_as_local",
            "is_father_address_same_as_local",
        )

    def update(self, instance, validated_data):
        instance.is_permenant_address_same_as_local = validated_data[
            "is_permenant_address_same_as_local"
        ]
        instance.is_father_address_same_as_local = validated_data[
            "is_father_address_same_as_local"
        ]
        instance.save()


class ApplicantIsFresherSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.user_id", read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "user_id",
            "is_fresher",
        )

    def update(self, instance, validated_data):
        instance.is_fresher = validated_data["is_fresher"]
        instance.save()


class NeeriUsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    mobile_no = serializers.CharField(source="user.mobile_no", read_only=True)
    user_id = serializers.UUIDField(source="user.user_id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    middle_name = serializers.CharField(source="user.middle_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    roles = serializers.SerializerMethodField(method_name="get_roles", required=False)
    zonal = serializers.SerializerMethodField(method_name="get_zonal", required=False)
    division = serializers.SerializerMethodField(
        method_name="get_division", required=False
    )
    user_address = serializers.SerializerMethodField(
        method_name="get_address", required=False
    )

    class Meta:
        model = NeeriUserProfile
        fields = (
            "user_id",
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "mobile_no",
            "division",
            "zonal",
            "email",
            "date_of_birth",
            "user_address",
            "religion",
            "caste",
            "profile_photo",
            "roles",
        )

    def get_address(self, obj):
        return obj.address and f"{obj.address.address1}, {obj.address.address2}"

    def get_roles(self, obj):
        groups = obj.user.groups.filter()
        serializer = RoleMasterSerializer(groups, many=True)
        return serializer.data

    def get_division(self, obj):
        division = obj.division.filter()
        serializer = job_posting.serializer.DivisionSerializer(division, many=True)
        return serializer.data

    def get_zonal(self, obj):
        zonal = obj.zonal.filter()
        serializer = job_posting.serializer.ZonalLabSerializer(zonal, many=True)
        return serializer.data

    def save(self, validated_data, password):
        neeri_user = User.objects.create_user(
            first_name=validated_data["first_name"],
            middle_name=validated_data.get("middle_name"),
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            mobile_no=validated_data["mobile_no"],
            password=password,
        )

        neeri_user_profile = NeeriUserProfile.objects.create(
            user=neeri_user,
            gender=validated_data.get("gender"),
            date_of_birth=validated_data.get("date_of_birth"),
            religion=validated_data.get("religion"),
            caste=validated_data.get("caste"),
            profile_photo=validated_data.get("profile_photo"),
        )

        for role_data in validated_data["roles"]:
            neeri_user.groups.add(role_data["role_id"])

        for zonal_data in validated_data["zonal"]:
            neeri_user_profile.zonal.add(zonal_data["zonal_lab_id"])

        for division_data in validated_data["division"]:
            neeri_user_profile.division.add(division_data["division_id"])

        neeri_user_profile.save()

        return neeri_user_profile.user_id

    def update(self, instance, validated_data):
        instance.gender = validated_data.get("gender") or instance.gender
        instance.date_of_birth = (
            validated_data.get("date_of_birth") or instance.date_of_birth
        )
        instance.religion = validated_data.get("religion") or instance.religion
        instance.caste = validated_data.get("caste") or instance.caste
        instance.profile_photo = (
            validated_data.get("profile_photo") or instance.profile_photo
        )
        instance.user.first_name = (
            validated_data.get("first_name") or instance.user.first_name
        )
        instance.user.last_name = (
            validated_data.get("last_name") or instance.user.last_name
        )
        instance.user.middle_name = (
            validated_data.get("middle_name") or instance.user.middle_name
        )
        instance.user.save()

        instance.user.groups.clear()
        updated_groups = [int(role["role_id"]) for role in validated_data["roles"]]
        instance.user.groups.add(*updated_groups)

        instance.division.clear()
        divisions = [division["division_id"] for division in validated_data["division"]]
        instance.division.add(*divisions)

        instance.zonal.clear()
        zones = [zone["zonal_lab_id"] for zone in validated_data["zonal"]]
        instance.zonal.add(*zones)
        instance.save()


class UserEducationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducationDetails
        fields = (
            "id",
            "exam_name",
            "university",
            "college_name",
            "passing_year",
            "score",
            "score_unit",
            "specialization",
        )

    def update(self, instance, validated_data):
        instance.exam_name = (
            validated_data["exam_name"]
            if validated_data["exam_name"]
            else instance.exam_name
        )

        instance.university = (
            validated_data["university"]
            if validated_data["university"]
            else instance.university
        )

        instance.college_name = (
            validated_data["college_name"]
            if validated_data["college_name"]
            else instance.college_name
        )

        instance.passing_year = (
            validated_data["passing_year"]
            if validated_data["passing_year"]
            else instance.passing_year
        )

        instance.score = (
            validated_data["score"] if validated_data["score"] else instance.score
        )

        instance.score_unit = (
            validated_data["score_unit"]
            if validated_data["score_unit"]
            else instance.score_unit
        )

        instance.specialization = (
            validated_data["specialization"]
            if validated_data["specialization"]
            else instance.specialization
        )

        instance.save()

    def save(self, validated_data):
        user_education = UserEducationDetails.objects.create(
            exam_name=validated_data["exam_name"]
            if "exam_name" in validated_data
            else None,
            university=validated_data["university"]
            if "university" in validated_data
            else None,
            college_name=validated_data["college_name"]
            if "college_name" in validated_data
            else None,
            passing_year=validated_data["passing_year"]
            if "passing_year" in validated_data
            else None,
            score=validated_data["score"] if "score" in validated_data else None,
            score_unit=validated_data["score_unit"]
            if "score_unit" in validated_data
            else None,
            specialization=validated_data["specialization"]
            if "specialization" in validated_data
            else None,
        )

        return user_education.id


class UserExperienceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperienceDetails
        fields = (
            "id",
            "employer_name",
            "post",
            "employed_from",
            "employed_to",
            "employment_type",
            "salary",
            "grade",
        )

    def save(self, validated_data):

        user_experience = UserExperienceDetails.objects.create(
            employer_name=validated_data["employer_name"]
            if "employer_name" in validated_data
            else None,
            post=validated_data["post"] if "post" in validated_data else None,
            employed_from=validated_data["employed_from"]
            if "employed_from" in validated_data
            else None,
            employed_to=validated_data["employed_to"]
            if "employed_to" in validated_data
            else None,
            employment_type=validated_data["employment_type"]
            if "employment_type" in validated_data
            else None,
            salary=validated_data["salary"] if "salary" in validated_data else None,
            grade=validated_data["grade"] if "grade" in validated_data else None,
        )

        return user_experience.id

    def update(self, instance, validated_data):

        instance.employer_name = (
            validated_data["employer_name"]
            if validated_data["employer_name"]
            else instance.employer_name
        )

        instance.post = (
            validated_data["post"] if validated_data["post"] else instance.post
        )

        instance.employed_from = (
            validated_data["employed_from"]
            if validated_data["employed_from"]
            else instance.employed_from
        )
        if not validated_data.get("employed_to"):
            instance.employed_to = None
        else:
            instance.employed_to = (
                validated_data.get("employed_to")
                if validated_data.get("employed_to")
                else instance.employed_to
            )

        instance.employment_type = (
            validated_data["employment_type"]
            if validated_data["employment_type"]
            else instance.employment_type
        )

        instance.salary = (
            validated_data["salary"] if validated_data["salary"] else instance.salary
        )

        instance.grade = (
            validated_data["grade"] if validated_data["grade"] else instance.grade
        )

        instance.save()


class FellowshipMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FellowshipMaster
        fields = (
            "id",
            "entrance_examination",
            "score",
            "scoring_unit",
            "passing_year",

        )


    def save(self, validated_data):

        user_fellowship = FellowshipMaster.objects.create(
            entrance_examination=validated_data["entrance_examination"]
            if "entrance_examination" in validated_data
            else None,
            score=validated_data["score"] if "score" in validated_data else None,
            scoring_unit=validated_data["scoring_unit"] if "scoring_unit" in validated_data else None,
            passing_year=validated_data["passing_year"] if "passing_year" in validated_data else None,
        )

        return user_fellowship.id

    def update(self, instance, validated_data):

        instance.entrance_examination = (
            validated_data["entrance_examination"]
            if validated_data["entrance_examination"]
            else instance.entrance_examination
        )

        instance.score = (
            validated_data["score"] if validated_data["score"] else instance.score
        )

        instance.scoring_unit = (
            validated_data["scoring_unit"] if validated_data["scoring_unit"] else instance.scoring_unit
        )

        instance.passing_year = (
            validated_data["passing_year"] if validated_data["passing_year"] else instance.passing_year
        )

        instance.save()


class ReligionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligionMaster
        fields = (
            "religion_id",
            "religion_name",

        )


    def save(self, validated_data):


        user_religion = ReligionMaster.objects.create(
            religion_name=validated_data["religion_name"]
            if "religion_name" in validated_data
            else None,
        )

        return user_religion.religion_id

    def update(self, instance, validated_data):


        instance.religion_name = (
            validated_data["religion_name"]
            if validated_data["religion_name"]
            else instance.religion_name
        )
        instance.save()


class NeeriRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeeriRelation

        fields = (
            "id",
            "relation_name",
            "designation",
            "center_name",
            "relation",
        )

    def save(self, validated_data):
        neeri_relation = NeeriRelation.objects.create(
            relation_name=validated_data["relation_name"]
            if "relation_name" in validated_data
            else None,
            designation=validated_data["designation"]
            if "designation" in validated_data
            else None,
            center_name=validated_data["center_name"]
            if "center_name" in validated_data
            else None,
            relation=validated_data["relation"]
            if "relation" in validated_data
            else None,
        )

        return neeri_relation.id

    def update(self, instance, validated_data):
        instance.relation_name = (
            validated_data["relation_name"]
            if validated_data["relation_name"]
            else instance.relation_name
        )

        instance.designation = (
            validated_data["designation"]
            if validated_data["designation"]
            else instance.designation
        )

        instance.center_name = (
            validated_data["center_name"]
            if validated_data["center_name"]
            else instance.center_name
        )

        instance.relation = (
            validated_data["relation"]
            if validated_data["relation"]
            else instance.relation
        )

        instance.save()


class ReferencesSerializer(serializers.ModelSerializer):
    address = LocationSerializer()

    class Meta:
        model = UserReference
        fields = (
            "id",
            "reference_name",
            "position",
            "address",
        )

    def save(self, validated_data):
        address = Location.objects.create(
            address1=validated_data["address"]["address1"],
            address2=validated_data["address"].get("address2"),
            address3=validated_data["address"].get("address3"),
            city=validated_data["address"]["city"],
            state=validated_data["address"]["state"],
            country=validated_data["address"]["country"],
            postcode=validated_data["address"]["postcode"],
            telephone_no=validated_data["address"]["telephone_no"],
        )

        reference = UserReference.objects.create(
            reference_name=validated_data["reference_name"]
            if "reference_name" in validated_data
            else None,
            position=validated_data["position"]
            if "position" in validated_data
            else None,
            address=address,
        )

        return reference.id

    def update(self, instance, validated_data):
        instance.reference_name = (
            validated_data["reference_name"]
            if validated_data["reference_name"]
            else instance.reference_name
        )

        instance.position = (
            validated_data["position"]
            if validated_data["position"]
            else instance.position
        )

        if validated_data["address"]:
            address_data = instance.address
            validated_address_data = validated_data["address"]

            print("AddressData", address_data)
            print("ValidatedData", validated_address_data)

            address_data.address1 = (
                validated_address_data["address1"]
                if validated_address_data["address1"]
                else address_data.address1
            )

            address_data.address2 = (
                validated_address_data.get("address2") or address_data.address2
            )

            address_data.address3 = (
                validated_address_data.get("address3") or address_data.address3
            )

            address_data.city = (
                validated_address_data["city"]
                if validated_address_data["city"]
                else address_data.city
            )

            address_data.state = (
                validated_address_data["state"]
                if validated_address_data["state"]
                else address_data.state
            )

            address_data.country = (
                validated_address_data["country"]
                if validated_address_data["country"]
                else address_data.country
            )

            address_data.postcode = (
                validated_address_data["postcode"]
                if validated_address_data["postcode"]
                else address_data.postcode
            )

            address_data.telephone_no = (
                validated_address_data["telephone_no"]
                if validated_address_data["telephone_no"]
                else address_data.telephone_no
            )
            address_data.save()
        instance.save()


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLanguages
        fields = (
            "id",
            "name",
            "read_level",
            "write_level",
            "speak_level",
            "exam_passed",
        )

    def save(self, validated_data):
        language = UserLanguages.objects.create(
            name=validated_data["name"] if "name" in validated_data else None,
            read_level=validated_data["read_level"]
            if "read_level" in validated_data
            else None,
            write_level=validated_data["write_level"]
            if "write_level" in validated_data
            else None,
            speak_level=validated_data["speak_level"]
            if "speak_level" in validated_data
            else None,
            exam_passed=validated_data["exam_passed"]
            if "exam_passed" in validated_data
            else None,
        )

        return language.id

    def update(self, instance, validated_data):
        instance.name = (
            validated_data["name"] if validated_data["name"] else instance.name
        )

        instance.read_level = (
            validated_data["read_level"]
            if validated_data["read_level"]
            else instance.read_level
        )

        instance.write_level = (
            validated_data["write_level"]
            if validated_data["write_level"]
            else instance.write_level
        )

        instance.speak_level = (
            validated_data["speak_level"]
            if validated_data["speak_level"]
            else instance.speak_level
        )

        instance.exam_passed = (
            validated_data["exam_passed"]
            if validated_data["exam_passed"]
            else instance.exam_passed
        )

        instance.save()


class OverseasVisitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverseasVisits
        fields = (
            "id",
            "country_visited",
            "date_of_visit",
            "duration_of_visit",
            "purpose_of_visit",
        )

    def save(self, validated_data):
        visit = OverseasVisits.objects.create(
            country_visited=validated_data["country_visited"]
            if "country_visited" in validated_data
            else None,
            date_of_visit=validated_data["date_of_visit"]
            if "date_of_visit" in validated_data
            else None,
            duration_of_visit=validated_data["duration_of_visit"]
            if "duration_of_visit" in validated_data
            else None,
            purpose_of_visit=validated_data["purpose_of_visit"]
            if "purpose_of_visit" in validated_data
            else None,
        )

        return visit.id

    def update(self, instance, validated_data):
        instance.country_visited = (
            validated_data["country_visited"]
            if validated_data["country_visited"]
            else instance.country_visited
        )

        instance.date_of_visit = (
            validated_data["date_of_visit"]
            if validated_data["date_of_visit"]
            else instance.date_of_visit
        )

        instance.duration_of_visit = (
            validated_data["duration_of_visit"]
            if validated_data["duration_of_visit"]
            else instance.duration_of_visit
        )

        instance.purpose_of_visit = (
            validated_data["purpose_of_visit"]
            if validated_data["purpose_of_visit"]
            else instance.purpose_of_visit
        )

        instance.save()


class UserDocumentsSerializer(serializers.ModelSerializer):
    doc_name = serializers.CharField(
        source="document_master.doc_type", required=False, default=None
    )

    class Meta:
        model = UserDocuments
        fields = (
            "doc_id",
            "doc_file_path",
            "doc_name",
        )


class PublishedPapersSerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField(
        method_name="get_attachments", read_only=True
    )

    class Meta:
        model = PublishedPapers
        fields = (
            "id",
            "paper_title",
            "attachments",
        )

    def get_attachments(self, obj):
        attachments = obj.attachments.filter()
        serializer = UserDocumentsSerializer(attachments, many=True)
        return serializer.data

    def save(self, validated_data):

        user = User.objects.get(user_id=validated_data["user_id"])
        user_profile = user.user_profile

        paper = PublishedPapers.objects.create(
            paper_title=validated_data["paper_title"]
            if "paper_title" in validated_data
            else None,
        )

        # for attachment_data in validated_data['attachments']:
        #     attachment = UserDocuments.objects.create(
        #         # doc_file_path = attachment_data['doc_file_path'],
        #         doc_name = attachment_data['doc_name'],
        #     )
        #     paper.attachments.add(attachment)

        for attachment_data in validated_data["attachments"]:
            attachment = UserDocuments.objects.get(doc_id=attachment_data["doc_id"])
            paper.attachments.add(attachment)

        user_profile.published_papers.add(paper)

        return paper.id

    def update(self, instance, validated_data):

        instance.paper_title = (
            validated_data["paper_title"]
            if "paper_title" in validated_data
            else instance.paper_title
        )

        for attachment_data in validated_data["attachments"]:
            doc = UserDocuments.objects.get(doc_id=attachment_data["doc_id"])
            doc.file_path_name = (
                attachment_data["doc_file_path"]
                if "doc_file_path" in attachment_data
                else doc.file_path_name
            )

            doc.doc_name = (
                attachment_data["doc_name"]
                if "doc_name" in attachment_data
                else doc.doc_name
            )
            doc.save()

        instance.save()


class ProfessionalTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalTraining
        fields = (
            "id",
            "title",
            "description",
            "from_date",
            "to_date",
        )

    def save(self, validated_data):
        professional_training = ProfessionalTraining.objects.create(
            title=validated_data["title"] if "title" in validated_data else None,
            description=validated_data["description"]
            if "description" in validated_data
            else None,
            from_date=validated_data["from_date"]
            if "from_date" in validated_data
            else None,
            to_date=validated_data["to_date"] if "to_date" in validated_data else None,
        )

        return professional_training.id

    def update(self, instance, validated_data):
        instance.title = (
            validated_data["title"] if validated_data["title"] else instance.title
        )

        instance.description = (
            validated_data["description"]
            if validated_data["description"]
            else instance.description
        )

        instance.from_date = (
            validated_data["from_date"]
            if validated_data["from_date"]
            else instance.from_date
        )

        instance.to_date = (
            validated_data["to_date"] if validated_data["to_date"] else instance.to_date
        )

        instance.save()


class OtherInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherInformation
        fields = (
            "id",
            "bond_title",
            "bond_details",
            "organisation_name",
            "bond_start_date",
            "bond_end_date",
            "notice_period_min",
            "notice_period_max",
        )

    def save(self, validated_data):
        other_info = OtherInformation.objects.create(
            bond_title=validated_data["bond_title"]
            if "bond_title" in validated_data
            else None,
            bond_details=validated_data["bond_details"]
            if "bond_details" in validated_data
            else None,
            organisation_name=validated_data["organisation_name"]
            if "organisation_name" in validated_data
            else None,
            bond_start_date=validated_data["bond_start_date"]
            if "bond_start_date" in validated_data
            else None,
            bond_end_date=validated_data["bond_end_date"]
            if "bond_end_date" in validated_data
            else None,
            notice_period_min=validated_data["notice_period_min"]
            if "notice_period_min" in validated_data
            else None,
            notice_period_max=validated_data["notice_period_max"]
            if "notice_period_max" in validated_data
            else None,
        )
        return other_info.id

    def update(self, instance, validated_data):
        instance.bond_title = validated_data["bond_title"]
        instance.bond_details = validated_data["bond_details"]
        instance.organisation_name = validated_data["organisation_name"]
        instance.bond_start_date = validated_data["bond_start_date"]
        instance.bond_end_date = validated_data["bond_end_date"]
        instance.notice_period_min = validated_data["notice_period_min"]
        instance.notice_period_max = validated_data["notice_period_max"]
        instance.save()


class UserProfilePreviewSerializer(serializers.ModelSerializer):
    name_of_applicant = serializers.CharField(source="user.get_full_name")
    mobile_no = serializers.CharField(source="user.mobile_no")
    local_address = LocationSerializer()
    permanent_address = LocationSerializer()
    father_address = LocationSerializer()
    education_details = serializers.SerializerMethodField()
    professional_trainings = serializers.SerializerMethodField()
    published_papers = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    other_info = OtherInformationSerializer()
    neeri_relation = serializers.SerializerMethodField()
    overseas_visits = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    references = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()
    fellow_ships = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            "name_of_applicant",
            "mobile_no",
            "gender",
            "profile_photo",
            "local_address",
            "permanent_address",
            "date_of_birth",
            "place_of_birth",
            "is_indian_citizen",
            "father_name",
            "father_address",
            "father_occupation",
            "religion",
            "caste",
            "passport_number",
            "passport_expiry",
            "fax_number",
            "whatsapp_id",
            "skype_id",
            "education_details",
            "professional_trainings",
            "published_papers",
            "experiences",
            "fellow_ships",
            "other_info",
            "neeri_relation",
            "overseas_visits",
            "languages",
            "references",
            "resume",
        )

    def get_education_details(self, obj):
        edu = obj.education_details.filter(is_deleted=False)
        serializer = UserEducationDetailsSerializer(edu, many=True)
        return serializer.data

    def get_professional_trainings(self, obj):
        edu = obj.professional_trainings.filter(is_deleted=False)
        serializer = ProfessionalTrainingSerializer(edu, many=True)
        return serializer.data

    def get_published_papers(self, obj):
        edu = obj.published_papers.filter(is_deleted=False)
        serializer = PublishedPapersSerializer(edu, many=True)
        return serializer.data

    def get_experiences(self, obj):
        edu = obj.experiences.filter(is_deleted=False)
        serializer = UserExperienceDetailsSerializer(edu, many=True)
        return serializer.data

    def get_fellow_ships(self, obj):
        fellow = obj.fellow_ships.filter(is_deleted=False)
        serializer = FellowshipMasterSerializer(fellow, many=True)
        return serializer.data

    def get_neeri_relation(self, obj):
        edu = obj.neeri_relation.filter(is_deleted=False)
        serializer = NeeriRelationSerializer(edu, many=True)
        return serializer.data

    def get_overseas_visits(self, obj):
        edu = obj.overseas_visits.filter(is_deleted=False)
        serializer = OverseasVisitsSerializer(edu, many=True)
        return serializer.data

    def get_languages(self, obj):
        edu = obj.languages.filter(is_deleted=False)
        serializer = LanguagesSerializer(edu, many=True)
        return serializer.data

    def get_references(self, obj):
        edu = obj.references.filter(is_deleted=False)
        serializer = ReferencesSerializer(edu, many=True)
        return serializer.data

    def get_resume(self, obj):
        resume = obj.documents.filter(document_master__doc_name__iexact="resume") or None
        return resume and resume[0].doc_file_path


class MentorMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorMaster
        fields = (
            "mentor_id",
            "mentor_name",
        )


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = (
            "division_id",
            "division_name",
        )


class TraineeSerializer(serializers.ModelSerializer):
    division = serializers.SerializerMethodField(
        method_name="get_division_name", required=False
    )
    mentor = serializers.SerializerMethodField(
        method_name="get_mentor_name", required=False
    )

    class Meta:
        model = Trainee
        fields = (
            "trainee_id",
            "generated_trainee_id",
            "trainee_name",
            "division",
            "mentor",
            "email",
            "mobile_no",
            "emp_start_date",
            "emp_end_date",
            "status",
        )

    def get_division_name(self, obj):
        division = obj.division
        serializer = DivisionSerializer(division)
        return serializer.data

    def get_mentor_name(self, obj):
        mentor = obj.mentor
        serializer = MentorMasterSerializer(mentor)
        return serializer.data

    def save(self, validated_data):
        print("validated_data-------------->", validated_data)

        valid_mentor = Trainee.objects.filter(
            mentor=validated_data["mentor"]["mentor_id"], is_deleted=False
        )
        print("valid_mentor-------------->", valid_mentor)
        print("valid_mentor.count()-------------->", valid_mentor.count())
        if not valid_mentor.count() >= 4:

            trainee = Trainee.objects.create(
                trainee_name=validated_data["trainee_name"],
                email=validated_data["email"],
                mobile_no=validated_data["mobile_no"],
                emp_start_date=validated_data["emp_start_date"],
                emp_end_date=validated_data["emp_end_date"],
                status=validated_data["status"],
            )

            division = Division.objects.get(
                division_name=validated_data["division"]["division_name"]
            )
            mentor = MentorMaster.objects.get(
                mentor_id=validated_data["mentor"]["mentor_id"]
            )
            trainee.division = division
            trainee.mentor = mentor
            trainee.save()
            return trainee.trainee_id
        else:
            return None

    def update(self, instance, validated_data):
        valid_mentor = Trainee.objects.filter(
            mentor=validated_data["mentor"]["mentor_id"]
        )
        if not valid_mentor.count() > 4:
            if instance:
                instance.trainee_name = (
                    validated_data["trainee_name"]
                    if validated_data["trainee_name"]
                    else instance.trainee_name
                )
                instance.email = (
                    validated_data["email"]
                    if validated_data["email"]
                    else instance.email
                )
                instance.mobile_no = (
                    validated_data["mobile_no"]
                    if validated_data["mobile_no"]
                    else instance.mobile_no
                )
                instance.emp_start_date = (
                    validated_data["emp_start_date"]
                    if validated_data["emp_start_date"]
                    else instance.emp_start_date
                )
                instance.emp_end_date = (
                    validated_data["emp_end_date"]
                    if validated_data["emp_end_date"]
                    else instance.emp_end_date
                )
                instance.status = (
                    validated_data["status"]
                    if validated_data["status"]
                    else instance.status
                )

                division_name = validated_data["division"]["division_name"]
                mentor_name = validated_data["mentor"]["mentor_name"]
                division = Division.objects.get(division_name__exact=division_name)
                mentor = MentorMaster.objects.get(mentor_name__exact=mentor_name)
                instance.division = division
                instance.mentor = mentor
                instance.save()

            return instance.trainee_id
        else:
            return None


