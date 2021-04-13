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
            "telephone_no",
        )

    def update(self, instance, validated_data):

        instance.address1 = (
            validated_data["address1"] if validated_data["address1"] else instance.address1
        )

        instance.address2 = (
            validated_data["address2"] if validated_data["address2"] else instance.address2
        )

        instance.address3 = (
            validated_data["address3"] if validated_data["address3"] else instance.address3
        )

        instance.city = (
            validated_data["city"] if validated_data["city"] else instance.city
        )

        instance.state = (
            validated_data["state"] if validated_data["state"] else instance.state
        )

        instance.country = (
            validated_data["country"] if validated_data["country"] else instance.country
        )

        instance.postcode = (
            validated_data["postcode"] if validated_data["postcode"] else instance.postcode
        )

        instance.telephone_no = (
            validated_data["telephone_no"] if validated_data["telephone_no"] else instance.telephone_no
        )

        instance.save()

    def save(self, validated_data):
        print("New Location Created")
        location = Location.objects.create(
            address1 = validated_data['address1'] if 'address1' in validated_data else None,
            address2 = validated_data['address2'] if 'address2' in validated_data else None,
            address3 = validated_data['address3'] if 'address3' in validated_data else None,
            city = validated_data['city'] if 'city' in validated_data else None,
            state = validated_data['state'] if 'state' in validated_data else None,
            country = validated_data['country'] if 'country' in validated_data else None,
            postcode = validated_data['postcode'] if 'postcode' in validated_data else None,
            telephone_no = validated_data['telephone_no'] if 'telephone_no' in validated_data else None,
        )
        return location.id



class UserProfileSerializer(serializers.ModelSerializer):

    local_address = LocationSerializer(required=False,many=True)
    permanent_address = LocationSerializer(required=False,many=True)

    class Meta:
        model = UserProfile

        profile_names = ("local_address","permanent_address",)
        fields = (
                    "gender",
                    "mobile_no",
                    "date_of_birth",
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
                    "user_id",
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
        user_permissions = UserPermissions.objects.filter(role__in=roles).distinct('permission')
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
            "user_id",
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
        user_permissions = UserPermissions.objects.filter(role__in=roles).distinct('permission')
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


class ApplicantUserPersonalInformationSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField(
        method_name="get_status", read_only=True
    )

    gender = serializers.SerializerMethodField(
        method_name="get_gender", read_only=True
    )

    mobile_no = serializers.SerializerMethodField(
        method_name="get_mobile_no", read_only=True
    )

    date_of_birth = serializers.SerializerMethodField(
        method_name="get_date_of_birth", read_only=True
    )

    date_of_birth_in_words = serializers.SerializerMethodField(
        method_name="get_date_of_birth_in_words", read_only=True
    )

    place_of_birth = serializers.SerializerMethodField(
        method_name="get_place_of_birth", read_only=True
    )

    local_address = serializers.SerializerMethodField(
        method_name="get_local_address", read_only=True
    )

    permanent_address = serializers.SerializerMethodField(
        method_name="get_permanent_address", read_only=True
    )

    father_name = serializers.SerializerMethodField(
        method_name="get_father_name", read_only=True
    )

    father_address = serializers.SerializerMethodField(
        method_name="get_father_address", read_only=True
    )

    father_occupation = serializers.SerializerMethodField(
        method_name="get_father_occupation", read_only=True
    )

    religion = serializers.SerializerMethodField(
        method_name="get_religion", read_only=True
    )

    caste = serializers.SerializerMethodField(
        method_name="get_caste", read_only=True
    )

    passport_number = serializers.SerializerMethodField(
        method_name="get_passport_number", read_only=True
    )

    passport_expiry = serializers.SerializerMethodField(
        method_name="get_passport_expiry", read_only=True
    )

    profile_photo = serializers.SerializerMethodField(
        method_name="get_profile_photo", read_only=True
    )

    whatsapp_id = serializers.SerializerMethodField(
        method_name="get_whatsapp_id", read_only=True
    )

    skype_id = serializers.SerializerMethodField(
        method_name="get_skype_id", read_only=True
    )

    user_id = serializers.SerializerMethodField(
        method_name="get_user_id", read_only=True
    )

    fax_number = serializers.SerializerMethodField(
        method_name="get_fax_number", read_only=True
    )

    is_indian_citizen = serializers.SerializerMethodField(
        method_name="get_is_indian_citizen", read_only=True
    )

    class Meta:
        model = UserProfile
        fields = (
            "user_id",
            "status",
            "gender",
            "mobile_no",
            "date_of_birth",
            "date_of_birth_in_words",
            "place_of_birth",
            "local_address",
            "permanent_address",
            "father_name",
            "father_address",
            "father_occupation",
            "religion",
            "caste",
            "passport_number",
            "passport_expiry",
            "fax_number",
            "is_indian_citizen",
            "profile_photo",
            "whatsapp_id",
            "skype_id",
        )

    def get_user_id(self,obj):
        try:
            user_id = obj.user.user_id
            return user_id
        except:
            return None

    def get_fax_number(self,obj):
        try:
            fax_number = obj.fax_number
            return fax_number
        except:
            return None

    def get_is_indian_citizen(self,obj):
        try:
            is_indian_citizen = obj.is_indian_citizen
            return is_indian_citizen
        except:
            return None

    def get_mobile_no(self,obj):
        try:
            mobile_no = obj.mobile_no
            return mobile_no
        except:
            return None

    def get_gender(self,obj):
        try:
            gender = obj.gender
            return gender
        except:
            return None

    def get_date_of_birth(self,obj):
        try:
            date_of_birth = obj.date_of_birth
            return date_of_birth
        except:
            return None

    def get_date_of_birth_in_words(self,obj):
        try:
            get_date_of_birth_in_words = obj.get_date_of_birth_in_words
            return get_date_of_birth_in_words
        except:
            return None

    def get_place_of_birth(self,obj):
        try:
            place_of_birth = obj.place_of_birth
            return place_of_birth
        except:
            return None

    def get_father_name(self,obj):
        try:
            father_name = obj.father_name
            return father_name
        except:
            return None

    def get_father_address(self,obj):
        try:
            father_address = obj.father_address
            serializer = LocationSerializer(father_address)
            return serializer.data
        except:
            return None


    def get_father_occupation(self,obj):
        try:
            father_occupation = obj.father_occupation
            return father_occupation
        except:
            return None


    def get_status(self,obj):
        try:
            status = obj.status
            return status
        except:
            return None


    def get_local_address(self,obj):
        try:
            local_address = obj.local_address
            serializer = LocationSerializer(local_address)
            return serializer.data
        except:
            return None

    def get_permanent_address(self,obj):
        try:
            permanent_address = obj.permanent_address
            serializer = LocationSerializer(permanent_address)
            return serializer.data
        except:
            return None


    def get_religion(self,obj):
        try:
            religion = obj.religion
            return religion
        except:
            return None

    def get_caste(self,obj):
        try:
            caste = obj.caste
            return caste
        except:
            return None

    def get_passport_number(self,obj):
        try:
            passport_number = obj.passport_number
            return passport_number
        except:
            return None

    def get_passport_expiry(self,obj):
        try:
            passport_expiry = obj.passport_expiry
            return passport_expiry
        except:
            return None

    def get_profile_photo(self,obj):
        try:
            profile_photo = obj.profile_photo
            return profile_photo
        except:
            return None

    def get_skype_id(self,obj):
        try:
            skype_id = obj.skype_id
            return skype_id
        except:
            return None

    def get_whatsapp_id(self,obj):
        try:
            whatsapp_id = obj.whatsapp_id
            return whatsapp_id
        except:
            return None

    def update(self, instance, validated_data):

        print("Instance",instance.is_indian_citizen)
        print("validated_data",validated_data)

        instance.status = (
            validated_data["status"] if validated_data["status"] else instance.status
        )

        instance.gender = (
            validated_data["gender"] if validated_data["gender"] else instance.gender
        )

        instance.mobile_no = (
            validated_data["mobile_no"] if validated_data["mobile_no"] else instance.mobile_no
        )

        instance.date_of_birth = (
            validated_data["date_of_birth"] if validated_data["date_of_birth"] else instance.date_of_birth
        )

        instance.date_of_birth_in_words = (
            validated_data["date_of_birth_in_words"] if validated_data["date_of_birth_in_words"] else instance.date_of_birth_in_words
        )

        instance.place_of_birth = (
            validated_data["place_of_birth"] if validated_data["place_of_birth"] else instance.place_of_birth
        )

        instance.father_name = (
            validated_data["father_name"] if validated_data["father_name"] else instance.father_name
        )

        instance.father_occupation = (
            validated_data["father_occupation"] if validated_data["father_occupation"] else instance.father_occupation
        )

        instance.religion = (
            validated_data["religion"] if validated_data["religion"] else instance.religion
        )

        instance.caste = (
            validated_data["caste"] if validated_data["caste"] else instance.caste
        )

        instance.passport_number = (
            validated_data["passport_number"] if validated_data["passport_number"] else instance.passport_number
        )

        instance.passport_expiry = (
            validated_data["passport_expiry"] if validated_data["passport_expiry"] else instance.passport_expiry
        )

        instance.profile_photo = (
            validated_data["profile_photo"] if validated_data["profile_photo"] else instance.profile_photo
        )

        instance.whatsapp_id = (
            validated_data["whatsapp_id"] if validated_data["whatsapp_id"] else instance.whatsapp_id
        )

        instance.skype_id = (
            validated_data["skype_id"] if validated_data["skype_id"] else instance.skype_id
        )

        instance.fax_number = (
            validated_data["fax_number"] if validated_data["fax_number"] else instance.fax_number
        )

        instance.is_indian_citizen = (
            validated_data["is_indian_citizen"] if validated_data["is_indian_citizen"] else instance.is_indian_citizen
        )
        instance.save()

        if instance.local_address:
            local_address_instance = instance.local_address
            validated_local_address = validated_data['local_address']

            local_address_instance.address1 = (
                validated_local_address['address1'] if validated_local_address['address1'] else local_address_instance.address1
            )

            local_address_instance.address2 = (
                validated_local_address['address2'] if validated_local_address[
                    'address2'] else local_address_instance.address2
            )

            local_address_instance.address3 = (
                validated_local_address['address3'] if validated_local_address[
                    'address3'] else local_address_instance.address3
            )

            local_address_instance.city = (
                validated_local_address['city'] if validated_local_address[
                    'city'] else local_address_instance.city
            )

            local_address_instance.state = (
                validated_local_address['state'] if validated_local_address[
                    'state'] else local_address_instance.state
            )

            local_address_instance.country = (
                validated_local_address['country'] if validated_local_address[
                    'country'] else local_address_instance.country
            )

            local_address_instance.postcode = (
                validated_local_address['postcode'] if validated_local_address[
                    'postcode'] else local_address_instance.postcode
            )

            local_address_instance.telephone_no = (
                validated_local_address['telephone_no'] if validated_local_address[
                    'telephone_no'] else local_address_instance.telephone_no
            )

            local_address_instance.save()

        if instance.permanent_address:
            permanent_address_instance = instance.permanent_address
            validated_permanent_address = validated_data['permanent_address']

            permanent_address_instance.address1 = (
                validated_permanent_address['address1'] if validated_permanent_address['address1'] else permanent_address_instance.address1
            )

            permanent_address_instance.address2 = (
                validated_permanent_address['address2'] if validated_permanent_address[
                    'address2'] else permanent_address_instance.address2
            )

            permanent_address_instance.address3 = (
                validated_permanent_address['address3'] if validated_permanent_address[
                    'address3'] else permanent_address_instance.address3
            )

            permanent_address_instance.city = (
                validated_permanent_address['city'] if validated_permanent_address[
                    'city'] else permanent_address_instance.city
            )

            permanent_address_instance.state = (
                validated_permanent_address['state'] if validated_permanent_address[
                    'state'] else permanent_address_instance.state
            )

            permanent_address_instance.country = (
                validated_permanent_address['country'] if validated_permanent_address[
                    'country'] else permanent_address_instance.country
            )

            permanent_address_instance.postcode = (
                validated_permanent_address['postcode'] if validated_permanent_address[
                    'postcode'] else permanent_address_instance.postcode
            )

            permanent_address_instance.telephone_no = (
                validated_permanent_address['telephone_no'] if validated_permanent_address[
                    'telephone_no'] else permanent_address_instance.telephone_no
            )

            permanent_address_instance.save()

        if instance.father_address:
            father_address_instance = instance.father_address
            validated_father_address = validated_data['father_address']

            father_address_instance.address1 = (
                validated_father_address['address1'] if validated_father_address['address1'] else father_address_instance.address1
            )

            father_address_instance.address2 = (
                validated_father_address['address2'] if validated_father_address[
                    'address2'] else father_address_instance.address2
            )

            father_address_instance.address3 = (
                validated_father_address['address3'] if validated_father_address[
                    'address3'] else father_address_instance.address3
            )

            father_address_instance.city = (
                validated_father_address['city'] if validated_father_address[
                    'city'] else father_address_instance.city
            )

            father_address_instance.state = (
                validated_father_address['state'] if validated_father_address[
                    'state'] else father_address_instance.state
            )

            father_address_instance.country = (
                validated_father_address['country'] if validated_father_address[
                    'country'] else father_address_instance.country
            )

            father_address_instance.postcode = (
                validated_father_address['postcode'] if validated_father_address[
                    'postcode'] else father_address_instance.postcode
            )

            father_address_instance.telephone_no = (
                validated_father_address['telephone_no'] if validated_father_address[
                    'telephone_no'] else father_address_instance.telephone_no
            )

            father_address_instance.save()

        instance.save()

    def save(self, validated_data):

        if 'local_address' in validated_data:
            local_address_data = validated_data['local_address']
            local_address = Location.objects.create(
                address1=local_address_data['address1'] if 'address1' in local_address_data else None,
                address2=local_address_data['address2'] if 'address2' in local_address_data else None,
                address3=local_address_data['address3'] if 'address3' in local_address_data else None,
                city=local_address_data['city'] if 'city' in local_address_data else None,
                state=local_address_data['state'] if 'state' in local_address_data else None,
                country=local_address_data['country'] if 'country' in local_address_data else None,
                postcode=local_address_data['postcode'] if 'postcode' in local_address_data else None,
                telephone_no=local_address_data['telephone_no'] if 'telepone_no' in local_address_data else None,
            )
        else:
            local_address = None

        if 'permanent_address' in validated_data:
            permanent_address_data = validated_data['permanent_address']
            permanent_address = Location.objects.create(
                address1=permanent_address_data['address1'] if 'address1' in local_address_data else None,
                address2=permanent_address_data['address2'] if 'address2' in local_address_data else None,
                address3=permanent_address_data['address3'] if 'address3' in local_address_data else None,
                city=permanent_address_data['city'] if 'city' in local_address_data else None,
                state=permanent_address_data['state'] if 'state' in local_address_data else None,
                country=permanent_address_data['country'] if 'country' in local_address_data else None,
                postcode=permanent_address_data['postcode'] if 'postcode' in local_address_data else None,
                telephone_no=permanent_address_data['telephone_no'] if 'telephone_no' in local_address_data else None,
            )
        else:
            permanent_address = None

        if 'father_address' in validated_data:
            father_address_data = validated_data['father_address']
            father_address = Location.objects.create(
                address1=father_address_data['address1'] if 'address1' in local_address_data else None,
                address2=father_address_data['address2'] if 'address2' in local_address_data else None,
                address3=father_address_data['address3'] if 'address3' in local_address_data else None,
                city=father_address_data['city'] if 'city' in local_address_data else None,
                state=father_address_data['state'] if 'state' in local_address_data else None,
                country=father_address_data['country'] if 'country' in local_address_data else None,
                postcode=father_address_data['postcode'] if 'postcode' in local_address_data else None,
                telephone_no=father_address_data['telephone_no'] if 'telephone_no' in local_address_data else None,
            )
        else:
            father_address = None

        user = User.objects.get(user_id = validated_data['user_id'])

        user_profile = UserProfile.objects.create(
            user = user,
            gender = validated_data['gender'] if 'gender' in validated_data else None,
            mobile_no = validated_data['mobile_no'] if 'mobile_no' in validated_data else None,
            date_of_birth = validated_data['date_of_birth'] if 'date_of_birth' in validated_data else None,
            status = validated_data['status'] if 'status' in validated_data else None,
            date_of_birth_in_words = validated_data['date_of_birth_in_words'] if 'date_of_birth_in_words' in validated_data else None,
            place_of_birth = validated_data['place_of_birth'] if 'place_of_birth' in validated_data else None,
            father_name = validated_data['father_name'] if 'father_name' in validated_data else None,
            father_occupation = validated_data['father_occupation'] if 'father_occupation' in validated_data else None,
            religion = validated_data['religion'] if 'religion' in validated_data else None,
            caste = validated_data['caste'] if 'caste' in validated_data else None,
            passport_number = validated_data['passport_number'] if 'passport_number' in validated_data else None,
            passport_expiry = validated_data['passport_expiry'] if 'passport_expiry' in validated_data else None,
            profile_photo = validated_data['profile_photo'] if 'profile_photo' in validated_data else None,
            fax_number = validated_data['fax_number'] if 'fax_number' in validated_data else None,
            is_indian_citizen = validated_data['is_indian_citizen'] if 'is_indian_citizen' in validated_data else None,
            whatsapp_id = validated_data['whatsapp_id'] if 'whatsapp_id' in validated_data else None,
            skype_id = validated_data['skype_id'] if 'skype_id' in validated_data else None,
            local_address = local_address if local_address else None,
            permanent_address = permanent_address if local_address else None,
            father_address = father_address if local_address else None,
        )
        return user_profile

