from user.models import User,UserProfile,Location,UserRoles,UserPermissions,RoleMaster
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class AuthTokenCustomSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password
            )

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
        )

class UserProfileSerializer(serializers.ModelSerializer):

    local_address = LocationSerializer(required=False,many=True)
    permanent_address = LocationSerializer(required=False,many=True)

    class Meta:
        model = UserProfile

        profile_names = ("local_address","permanent_address",)
        fields = (
                    "gender",
                    "mobile_no",
                    "phone_no",
                    "date_of_birth",
                    "age",
                    "status",
                    "higher_qualification",
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                    "is_deleted",
                 ) + profile_names


class UserRolesSerializer(serializers.ModelSerializer):

    user_role = serializers.SerializerMethodField(
        method_name="get_user_role", read_only=True
    )

    class Meta:
        model = UserRoles
        fields = (
            "user_role",
        )

    def get_user_role(self,obj):
        user_role = obj.role.role_name
        return user_role

class UserPermissionSerializer(serializers.ModelSerializer):

    user_permission = serializers.SerializerMethodField(
        method_name="get_user_permission", read_only=True
    )

    class Meta:
        model = UserPermissions
        fields = (
            "user_permission",
        )

    def get_user_permission(self,obj):
        user_permission = obj.permission.permission_name
        return user_permission


class UserSerializer(serializers.ModelSerializer):

    user_profile = UserProfileSerializer(required=False)
    user_roles = serializers.SerializerMethodField(
        method_name="get_user_roles", read_only=True
    )
    user_permissions = serializers.SerializerMethodField(
        method_name="get_user_permissions", read_only=True
    )

    class Meta:
        model = User

        profile_names = ("user_profile","user_roles","user_permissions")

        fields = (
                    "id",
                     "username",
                     "email",
                     "created_at",
                     "is_deleted",
                     "user_roles",
                 ) + profile_names


    def get_user_roles(self,obj):
        user_roles = UserRoles.objects.filter(user=obj)
        serializer = UserRolesSerializer(user_roles,many=True)
        return serializer.data

    def get_user_permissions(self, obj):
        user_roles = UserRoles.objects.filter(user=obj)
        role_names = [role.role.role_name for role in user_roles]
        roles = RoleMaster.objects.filter(role_name__in=role_names)
        user_permissions = UserPermissions.objects.filter(role_name__in=roles).distinct('permission')
        serializer = UserPermissionSerializer(user_permissions, many=True)
        return serializer.data

class CustomUserSerializer(serializers.ModelSerializer):

    mobile_no = serializers.SerializerMethodField(
        method_name="get_mobile_no", read_only=True
    )

    phone_no = serializers.SerializerMethodField(
        method_name="get_phone_no", read_only=True
    )

    gender = serializers.SerializerMethodField(
        method_name="get_gender", read_only=True
    )

    date_of_birth = serializers.SerializerMethodField(
        method_name="get_date_of_birth", read_only=True
    )

    age = serializers.SerializerMethodField(
        method_name="get_age", read_only=True
    )

    status = serializers.SerializerMethodField(
        method_name="get_status", read_only=True
    )

    higher_qualification = serializers.SerializerMethodField(
        method_name="get_higher_qualification", read_only=True
    )

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
            "id",
            "username",
            "email",
            "created_at",
            "status",
            "gender",
            "date_of_birth",
            "age",
            "mobile_no",
            "phone_no",
            "higher_qualification",
            "local_address",
            "permanent_address",
            "is_deleted",
            "user_roles",
            "user_permissions",
        )

    def get_mobile_no(self,obj):
        try:
            mobile_no = obj.user_profile.mobile_no
            return mobile_no
        except:
            return None

    def get_phone_no(self,obj):
        try:
            phone_no = obj.user_profile.phone_no
            return phone_no
        except:
            return None

    def get_gender(self,obj):
        try:
            gender = obj.user_profile.gender
            return gender
        except:
            return None

    def get_date_of_birth(self,obj):
        try:
            date_of_birth = obj.user_profile.date_of_birth
            return date_of_birth
        except:
            return None

    def get_age(self,obj):
        try:
            age = obj.user_profile.age
            return age
        except:
            return None

    def get_status(self,obj):
        try:
            status = obj.user_profile.status
            return status
        except:
            return None

    def get_higher_qualification(self,obj):
        try:
            higher_qualification = obj.user_profile.higher_qualification
            return higher_qualification
        except:
            return None

    def get_local_address(self,obj):
        try:
            local_address = obj.user_profile.local_address.all()
            serializer = LocationSerializer(local_address,many=True)
            return serializer.data
        except:
            return None

    def get_permanent_address(self,obj):
        try:
            permanent_address = obj.user_profile.permanent_address.all()
            serializer = LocationSerializer(permanent_address,many=True)
            return serializer.data
        except:
            return None

    def get_user_roles(self,obj):
        user_roles = UserRoles.objects.filter(user=obj)
        serializer = UserRolesSerializer(user_roles,many=True)
        return serializer.data

    def get_user_permissions(self, obj):
        user_roles = UserRoles.objects.filter(user=obj)
        role_names = [role.role.role_name for role in user_roles]
        roles = RoleMaster.objects.filter(role_name__in=role_names)
        user_permissions = UserPermissions.objects.filter(role_name__in=roles).distinct('permission')
        serializer = UserPermissionSerializer(user_permissions, many=True)
        return serializer.data

    def update(self, instance, validated_data):


        instance.username = (
            validated_data["username"] if validated_data["username"] else instance.username
        )

        instance.email = (
            validated_data["email"] if validated_data["email"] else instance.email
        )

        instance.created_at = (
            validated_data["created_at"] if validated_data["created_at"] else instance.created_at
        )

        try:
            local_address_instance = instance.user_profile.local_address.filter()
            permanent_address_instance = instance.user_profile.permanent_address.filter()
            local_address_data = validated_data["local_address"][0]
            permanent_address_data = validated_data["permanent_address"][0]

            if instance.user_profile:
                instance.user_profile.phone_no = (
                    validated_data["phone_no"] if validated_data["phone_no"] else instance.user_profile.phone_no
                )

                instance.user_profile.mobile_no = (
                    validated_data["mobile_no"] if validated_data["mobile_no"] else instance.user_profile.mobile_no
                )

                instance.user_profile.gender = (
                    validated_data["gender"] if validated_data["gender"] else instance.user_profile.gender
                )

                instance.user_profile.date_of_birth = (
                    validated_data["date_of_birth"] if validated_data["date_of_birth"] else instance.user_profile.date_of_birth
                )

                instance.user_profile.age = (
                    validated_data["age"] if validated_data["age"] else instance.user_profile.age
                )

                instance.user_profile.status = (
                    validated_data["status"] if validated_data["status"] else instance.user_profile.status
                )

                instance.user_profile.higher_qualification = (
                    validated_data["higher_qualification"] if validated_data["higher_qualification"] else instance.user_profile.higher_qualification
                )

            if local_address_instance:
                local_address_instance[0].address1 = (
                    local_address_data['address1'] if local_address_data['address1'] else
                    local_address_instance[0].address1
                )

                local_address_instance[0].address2 = (
                    local_address_data['address2'] if local_address_data['address2'] else
                    local_address_instance[0].address2
                )

                local_address_instance[0].address3 = (
                    local_address_data['address3'] if local_address_data['address3'] else
                    local_address_instance[0].address3
                )

                local_address_instance[0].city = (
                    local_address_data['city'] if local_address_data['city'] else
                    local_address_instance[0].city
                )

                local_address_instance[0].state = (
                    local_address_data['state'] if local_address_data['state'] else
                    local_address_instance[0].state
                )

                local_address_instance[0].country = (
                    local_address_data['country'] if local_address_data['country'] else
                    local_address_instance[0].country
                )

                local_address_instance[0].postcode = (
                    local_address_data['postcode'] if local_address_data['postcode'] else
                    local_address_instance[0].postcode
                )
                local_address_instance[0].save()

            if permanent_address_instance:
                permanent_address_instance[0].address1 = (
                    permanent_address_data['address1'] if permanent_address_data['address1'] else
                    permanent_address_instance[0].address1
                )

                permanent_address_instance[0].address2 = (
                    permanent_address_data['address2'] if permanent_address_data['address2'] else
                    permanent_address_instance[0].address2
                )

                permanent_address_instance[0].address3 = (
                    permanent_address_data['address3'] if permanent_address_data['address3'] else
                    permanent_address_instance[0].address3
                )

                permanent_address_instance[0].city = (
                    permanent_address_data['city'] if permanent_address_data['city'] else
                    permanent_address_instance[0].city
                )

                permanent_address_instance[0].state = (
                    permanent_address_data['state'] if permanent_address_data['state'] else
                    permanent_address_instance[0].state
                )

                permanent_address_instance[0].country = (
                    permanent_address_data['country'] if permanent_address_data['country'] else
                    permanent_address_instance[0].country
                )

                permanent_address_instance[0].postcode = (
                    permanent_address_data['postcode'] if permanent_address_data['postcode'] else
                    permanent_address_instance[0].postcode
                )
                permanent_address_instance[0].save()
            instance.user_profile.save()
            instance.save()
        except:
            user_profile_local_address = validated_data['local_address']
            user_profile_permanent_address = validated_data['permanent_address']

            local_address = Location.objects.create(
                address1=user_profile_local_address[0]['address1'],
                address2=user_profile_local_address[0]['address2'],
                address3=user_profile_local_address[0]['address3'],
                city=user_profile_local_address[0]['city'],
                state=user_profile_local_address[0]['state'],
                country=user_profile_local_address[0]['country'],
                postcode=user_profile_local_address[0]['postcode'],
            )

            permanent_address = Location.objects.create(
                address1=user_profile_permanent_address[0]['address1'],
                address2=user_profile_permanent_address[0]['address2'],
                address3=user_profile_permanent_address[0]['address3'],
                city=user_profile_permanent_address[0]['city'],
                state=user_profile_permanent_address[0]['state'],
                country=user_profile_permanent_address[0]['country'],
                postcode=user_profile_permanent_address[0]['postcode'],
            )


            user_profile = UserProfile.objects.create(
                user=instance,
                gender=validated_data['gender'],
                phone_no=validated_data['phone_no'],
                mobile_no=validated_data['mobile_no'],
                date_of_birth=validated_data['date_of_birth'],
                age=validated_data['age'],
                status=validated_data['status'],
                higher_qualification=validated_data['higher_qualification'],
            )
            user_profile.local_address.add(local_address)
            user_profile.permanent_address.add(permanent_address)

            instance.user_profile = user_profile
            instance.save()


    def save(self, instance, validated_data):

        try:
            if instance.user_profile:
                pass
        except:
            if 'local_address' in validated_data:
                user_profile_local_address = validated_data['local_address']
                local_address = Location.objects.create(
                    address1=user_profile_local_address[0]['address1'],
                    address2=user_profile_local_address[0]['address2'],
                    address3=user_profile_local_address[0]['address3'],
                    city=user_profile_local_address[0]['city'],
                    state=user_profile_local_address[0]['state'],
                    country=user_profile_local_address[0]['country'],
                    postcode=user_profile_local_address[0]['postcode'],
                )
            if 'permanent_address' in validated_data:
                user_profile_permanent_address = validated_data['permanent_address']
                permanent_address = Location.objects.create(
                    address1=user_profile_permanent_address[0]['address1'],
                    address2=user_profile_permanent_address[0]['address2'],
                    address3=user_profile_permanent_address[0]['address3'],
                    city=user_profile_permanent_address[0]['city'],
                    state=user_profile_permanent_address[0]['state'],
                    country=user_profile_permanent_address[0]['country'],
                    postcode=user_profile_permanent_address[0]['postcode'],
                )

            user_profile = UserProfile.objects.create(
                user = instance,
                gender = validated_data['gender'] if 'gender' in validated_data else None,
                phone_no = validated_data['phone_no'] if 'phone_no' in validated_data else None,
                mobile_no = validated_data['mobile_no'] if 'mobile_no' in validated_data else None,
                date_of_birth = validated_data['date_of_birth'] if 'date_of_birth' in validated_data else None,
                age = validated_data['age'] if 'age' in validated_data else None,
                status = validated_data['status'] if 'status' in validated_data else None,
                higher_qualification = validated_data['higher_qualification'] if 'higher_qualification' in validated_data else None,
            )
            user_profile.local_address.add(local_address)
            user_profile.permanent_address.add(permanent_address)

            instance.user_profile = user_profile
            instance.user_profile.save()
            instance.save()

