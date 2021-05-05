from user.models import User,UserProfile,Location,UserRoles,UserPermissions,RoleMaster,UserEducationDetails,\
    UserExperienceDetails,NeeriRelation,UserReference,OverseasVisits,UserLanguages,UserDocuments,\
    PublishedPapers,ProfessionalTraining,OtherInformation
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

    local_address = LocationSerializer(required=False)
    permanent_address = LocationSerializer(required=False)
    father_address = LocationSerializer(required=False)

    class Meta:
        model = UserProfile

        profile_names = ("local_address","permanent_address","father_address",)
        fields = (
                    "gender",
                    "mobile_no",
                    "date_of_birth",
                    "status",
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

    username = serializers.SerializerMethodField(
        method_name="get_username", read_only=True
    )

    class Meta:
        model = User

        profile_names = ("user_profile", "user_roles", "user_permissions")

        fields = (
                     "user_id",
                     "username",
                     "email",
                     "mobile_no",
                     "created_at",
                     "is_deleted",
                     "user_roles",
                 ) + profile_names

    def get_username(self,obj):
        if obj.first_name == '' and obj.last_name == '':
            return obj.email
        else:
            return obj.first_name + ' ' + obj.last_name

    def get_user_roles(self, obj):
        user_roles = UserRoles.objects.filter(user=obj)
        serializer = UserRolesSerializer(user_roles, many=True)
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

    status = serializers.SerializerMethodField(
        method_name="get_status", read_only=True
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
            "mobile_no",
            "phone_no",
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


    def get_status(self,obj):
        try:
            status = obj.user_profile.status
            return status
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


                instance.user_profile.status = (
                    validated_data["status"] if validated_data["status"] else instance.user_profile.status
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
                status=validated_data['status'],
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
                status = validated_data['status'] if 'status' in validated_data else None,
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

    # local_address = serializers.SerializerMethodField(
    #     method_name="get_local_address", read_only=True
    # )
    #
    # permanent_address = serializers.SerializerMethodField(
    #     method_name="get_permanent_address", read_only=True
    # )

    father_name = serializers.SerializerMethodField(
        method_name="get_father_name", read_only=True
    )

    # father_address = serializers.SerializerMethodField(
    #     method_name="get_father_address", read_only=True
    # )

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

    middle_name = serializers.SerializerMethodField(
        method_name="get_middle_name", read_only=True
    )

    last_name = serializers.SerializerMethodField(
        method_name="get_last_name", read_only=True
    )

    first_name = serializers.SerializerMethodField(
        method_name="get_first_name", read_only=True
    )

    nationality = serializers.SerializerMethodField(
        method_name="get_nationality", read_only=True
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
            "nationality",
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

    def get_first_name(self,obj):
        try:
            first_name = obj.user.first_name
            return first_name
        except:
            return None

    def get_last_name(self,obj):
        try:
            last_name = obj.user.last_name
            return last_name
        except:
            return None

    def get_middle_name(self,obj):
        try:
            middle_name = obj.user.middle_name
            return middle_name
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

    # def get_father_address(self,obj):
    #     try:
    #         father_address = obj.father_address
    #         serializer = LocationSerializer(father_address)
    #         return serializer.data
    #     except:
    #         return None


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


    # def get_local_address(self,obj):
    #     try:
    #         local_address = obj.local_address
    #         serializer = LocationSerializer(local_address)
    #         return serializer.data
    #     except:
    #         return None

    # def get_permanent_address(self,obj):
    #     try:
    #         permanent_address = obj.permanent_address
    #         serializer = LocationSerializer(permanent_address)
    #         return serializer.data
    #     except:
    #         return None


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

    def get_nationality(self,obj):
        try:
            nationality = obj.nationality
            return nationality
        except:
            return None

    def update(self, instance, validated_data):

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

        instance.nationality = (
            validated_data["nationality"] if validated_data["nationality"] else instance.nationality
        )

        instance.user.first_name = (
            validated_data["first_name"] if validated_data["first_name"] else instance.user.first_name
        )

        instance.user.last_name = (
            validated_data["last_name"] if validated_data["last_name"] else instance.user.last_name
        )

        instance.user.middle_name = (
            validated_data["middle_name"] if validated_data["middle_name"] else instance.user.middle_name
        )

        instance.is_indian_citizen = validated_data["is_indian_citizen"]
        instance.user.save()
        instance.save()

        # if instance.local_address:
        #     local_address_instance = instance.local_address
        #     validated_local_address = validated_data['local_address']
        #
        #     local_address_instance.address1 = (
        #         validated_local_address['address1'] if validated_local_address['address1'] else local_address_instance.address1
        #     )
        #
        #     local_address_instance.address2 = (
        #         validated_local_address['address2'] if validated_local_address[
        #             'address2'] else local_address_instance.address2
        #     )
        #
        #     local_address_instance.address3 = (
        #         validated_local_address['address3'] if validated_local_address[
        #             'address3'] else local_address_instance.address3
        #     )
        #
        #     local_address_instance.city = (
        #         validated_local_address['city'] if validated_local_address[
        #             'city'] else local_address_instance.city
        #     )
        #
        #     local_address_instance.state = (
        #         validated_local_address['state'] if validated_local_address[
        #             'state'] else local_address_instance.state
        #     )
        #
        #     local_address_instance.country = (
        #         validated_local_address['country'] if validated_local_address[
        #             'country'] else local_address_instance.country
        #     )
        #
        #     local_address_instance.postcode = (
        #         validated_local_address['postcode'] if validated_local_address[
        #             'postcode'] else local_address_instance.postcode
        #     )
        #
        #     local_address_instance.telephone_no = (
        #         validated_local_address['telephone_no'] if validated_local_address[
        #             'telephone_no'] else local_address_instance.telephone_no
        #     )
        #
        #     local_address_instance.save()
        #
        # if instance.permanent_address:
        #     permanent_address_instance = instance.permanent_address
        #     validated_permanent_address = validated_data['permanent_address']
        #
        #     permanent_address_instance.address1 = (
        #         validated_permanent_address['address1'] if validated_permanent_address['address1'] else permanent_address_instance.address1
        #     )
        #
        #     permanent_address_instance.address2 = (
        #         validated_permanent_address['address2'] if validated_permanent_address[
        #             'address2'] else permanent_address_instance.address2
        #     )
        #
        #     permanent_address_instance.address3 = (
        #         validated_permanent_address['address3'] if validated_permanent_address[
        #             'address3'] else permanent_address_instance.address3
        #     )
        #
        #     permanent_address_instance.city = (
        #         validated_permanent_address['city'] if validated_permanent_address[
        #             'city'] else permanent_address_instance.city
        #     )
        #
        #     permanent_address_instance.state = (
        #         validated_permanent_address['state'] if validated_permanent_address[
        #             'state'] else permanent_address_instance.state
        #     )
        #
        #     permanent_address_instance.country = (
        #         validated_permanent_address['country'] if validated_permanent_address[
        #             'country'] else permanent_address_instance.country
        #     )
        #
        #     permanent_address_instance.postcode = (
        #         validated_permanent_address['postcode'] if validated_permanent_address[
        #             'postcode'] else permanent_address_instance.postcode
        #     )
        #
        #     permanent_address_instance.telephone_no = (
        #         validated_permanent_address['telephone_no'] if validated_permanent_address[
        #             'telephone_no'] else permanent_address_instance.telephone_no
        #     )
        #
        #     permanent_address_instance.save()
        #
        # if instance.father_address:
        #     father_address_instance = instance.father_address
        #     validated_father_address = validated_data['father_address']
        #
        #     father_address_instance.address1 = (
        #         validated_father_address['address1'] if validated_father_address['address1'] else father_address_instance.address1
        #     )
        #
        #     father_address_instance.address2 = (
        #         validated_father_address['address2'] if validated_father_address[
        #             'address2'] else father_address_instance.address2
        #     )
        #
        #     father_address_instance.address3 = (
        #         validated_father_address['address3'] if validated_father_address[
        #             'address3'] else father_address_instance.address3
        #     )
        #
        #     father_address_instance.city = (
        #         validated_father_address['city'] if validated_father_address[
        #             'city'] else father_address_instance.city
        #     )
        #
        #     father_address_instance.state = (
        #         validated_father_address['state'] if validated_father_address[
        #             'state'] else father_address_instance.state
        #     )
        #
        #     father_address_instance.country = (
        #         validated_father_address['country'] if validated_father_address[
        #             'country'] else father_address_instance.country
        #     )
        #
        #     father_address_instance.postcode = (
        #         validated_father_address['postcode'] if validated_father_address[
        #             'postcode'] else father_address_instance.postcode
        #     )
        #
        #     father_address_instance.telephone_no = (
        #         validated_father_address['telephone_no'] if validated_father_address[
        #             'telephone_no'] else father_address_instance.telephone_no
        #     )
        #
        #     father_address_instance.save()

        instance.save()

    def save(self, validated_data):

        # if 'local_address' in validated_data:
        #     local_address_data = validated_data['local_address']
        #     local_address = Location.objects.create(
        #         address1=local_address_data['address1'] if 'address1' in local_address_data else None,
        #         address2=local_address_data['address2'] if 'address2' in local_address_data else None,
        #         address3=local_address_data['address3'] if 'address3' in local_address_data else None,
        #         city=local_address_data['city'] if 'city' in local_address_data else None,
        #         state=local_address_data['state'] if 'state' in local_address_data else None,
        #         country=local_address_data['country'] if 'country' in local_address_data else None,
        #         postcode=local_address_data['postcode'] if 'postcode' in local_address_data else None,
        #         telephone_no=local_address_data['telephone_no'] if 'telepone_no' in local_address_data else None,
        #     )
        # else:
        #     local_address = None
        #
        # if 'permanent_address' in validated_data:
        #     permanent_address_data = validated_data['permanent_address']
        #     permanent_address = Location.objects.create(
        #         address1=permanent_address_data['address1'] if 'address1' in local_address_data else None,
        #         address2=permanent_address_data['address2'] if 'address2' in local_address_data else None,
        #         address3=permanent_address_data['address3'] if 'address3' in local_address_data else None,
        #         city=permanent_address_data['city'] if 'city' in local_address_data else None,
        #         state=permanent_address_data['state'] if 'state' in local_address_data else None,
        #         country=permanent_address_data['country'] if 'country' in local_address_data else None,
        #         postcode=permanent_address_data['postcode'] if 'postcode' in local_address_data else None,
        #         telephone_no=permanent_address_data['telephone_no'] if 'telephone_no' in local_address_data else None,
        #     )
        # else:
        #     permanent_address = None
        #
        # if 'father_address' in validated_data:
        #     father_address_data = validated_data['father_address']
        #     father_address = Location.objects.create(
        #         address1=father_address_data['address1'] if 'address1' in local_address_data else None,
        #         address2=father_address_data['address2'] if 'address2' in local_address_data else None,
        #         address3=father_address_data['address3'] if 'address3' in local_address_data else None,
        #         city=father_address_data['city'] if 'city' in local_address_data else None,
        #         state=father_address_data['state'] if 'state' in local_address_data else None,
        #         country=father_address_data['country'] if 'country' in local_address_data else None,
        #         postcode=father_address_data['postcode'] if 'postcode' in local_address_data else None,
        #         telephone_no=father_address_data['telephone_no'] if 'telephone_no' in local_address_data else None,
        #     )
        # else:
        #     father_address = None

        user = User.objects.get(user_id = validated_data['user_id'])
        user.first_name = validated_data['first_name'] if 'first_name' in validated_data else None
        user.middle_name = validated_data['middle_name'] if 'middle_name' in validated_data else None
        user.last_name = validated_data['last_name'] if 'last_name' in validated_data else None
        user.save()

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
            nationality = validated_data['nationality'] if 'nationality' in validated_data else None,
            # local_address = local_address if local_address else None,
            # permanent_address = permanent_address if local_address else None,
            # father_address = father_address if local_address else None,
        )
        return user_profile

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
            validated_data["exam_name"] if validated_data["exam_name"] else instance.exam_name
        )

        instance.university = (
            validated_data["university"] if validated_data["university"] else instance.university
        )

        instance.college_name = (
            validated_data["college_name"] if validated_data["college_name"] else instance.college_name
        )

        instance.passing_year = (
            validated_data["passing_year"] if validated_data["passing_year"] else instance.passing_year
        )

        instance.score = (
            validated_data["score"] if validated_data["score"] else instance.score
        )

        instance.score_unit = (
            validated_data["score_unit"] if validated_data["score_unit"] else instance.score_unit
        )

        instance.specialization = (
            validated_data["specialization"] if validated_data["specialization"] else instance.specialization
        )

        instance.save()

    def save(self, validated_data):

        user_education = UserEducationDetails.objects.create(
            exam_name = validated_data['exam_name'] if 'exam_name' in validated_data else None,
            university = validated_data['university'] if 'university' in validated_data else None,
            college_name = validated_data['college_name'] if 'college_name' in validated_data else None,
            passing_year = validated_data['passing_year'] if 'passing_year' in validated_data else None,
            score = validated_data['score'] if 'score' in validated_data else None,
            score_unit = validated_data['score_unit'] if 'score_unit' in validated_data else None,
            specialization = validated_data['specialization'] if 'specialization' in validated_data else None,
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
            employer_name = validated_data['employer_name'] if 'employer_name' in validated_data else None,
            post = validated_data['post'] if 'post' in validated_data else None,
            employed_from = validated_data['employed_from'] if 'employed_from' in validated_data else None,
            employed_to = validated_data['employed_to'] if 'employed_to' in validated_data else None,
            employment_type = validated_data['employment_type'] if 'employment_type' in validated_data else None,
            salary = validated_data['salary'] if 'salary' in validated_data else None,
            grade = validated_data['grade'] if 'grade' in validated_data else None,
        )

        return user_experience.id

    def update(self, instance, validated_data):

        instance.employer_name = (
            validated_data["employer_name"] if validated_data["employer_name"] else instance.employer_name
        )

        instance.post = (
            validated_data["post"] if validated_data["post"] else instance.post
        )

        instance.employed_from = (
            validated_data["employed_from"] if validated_data["employed_from"] else instance.employed_from
        )

        instance.employed_to = (
            validated_data["employed_to"] if validated_data["employed_to"] else instance.employed_to
        )

        instance.employment_type = (
            validated_data["employment_type"] if validated_data["employment_type"] else instance.employment_type
        )

        instance.salary = (
            validated_data["salary"] if validated_data["salary"] else instance.salary
        )

        instance.grade = (
            validated_data["grade"] if validated_data["grade"] else instance.grade
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
            relation_name = validated_data['relation_name'] if 'relation_name' in validated_data else None,
            designation = validated_data['designation'] if 'designation' in validated_data else None,
            center_name = validated_data['center_name'] if 'center_name' in validated_data else None,
            relation = validated_data['relation'] if 'relation' in validated_data else None,
        )

        return neeri_relation.id

    def update(self, instance, validated_data):

        instance.relation_name = (
            validated_data["relation_name"] if validated_data["relation_name"] else instance.relation_name
        )

        instance.designation = (
            validated_data["designation"] if validated_data["designation"] else instance.designation
        )

        instance.center_name = (
            validated_data["center_name"] if validated_data["center_name"] else instance.center_name
        )

        instance.relation = (
            validated_data["relation"] if validated_data["relation"] else instance.relation
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
            address1 = validated_data['address']['address1'],
            address2 = validated_data['address']['address2'],
            address3 = validated_data['address']['address3'],
            city = validated_data['address']['city'],
            state = validated_data['address']['state'],
            country = validated_data['address']['country'],
            postcode = validated_data['address']['postcode'],
            telephone_no = validated_data['address']['telephone_no'],
        )

        reference = UserReference.objects.create(
            reference_name = validated_data['reference_name'] if 'reference_name' in validated_data else None,
            position = validated_data['position'] if 'position' in validated_data else None,
            address = address,
        )

        return reference.id

    def update(self, instance, validated_data):

        instance.reference_name = (
            validated_data["reference_name"] if validated_data["reference_name"] else instance.reference_name
        )

        instance.position = (
            validated_data["position"] if validated_data["position"] else instance.position
        )

        if validated_data['address']:
            address_data = instance.address
            validated_address_data = validated_data['address']

            print("AddressData",address_data)
            print("ValidatedData",validated_address_data)

            address_data.address1 = (
                validated_address_data["address1"] if validated_address_data["address1"] else address_data.address1
            )

            address_data.address2 = (
                validated_address_data["address2"] if validated_address_data["address2"] else address_data.address2
            )

            address_data.address3 = (
                validated_address_data["address3"] if validated_address_data["address3"] else address_data.address3
            )

            address_data.city = (
                validated_address_data["city"] if validated_address_data["city"] else address_data.city
            )

            address_data.state = (
                validated_address_data["state"] if validated_address_data["state"] else address_data.state
            )

            address_data.country = (
                validated_address_data["country"] if validated_address_data["country"] else address_data.country
            )

            address_data.postcode = (
                validated_address_data["postcode"] if validated_address_data["postcode"] else address_data.postcode
            )

            address_data.telephone_no = (
                validated_address_data["telephone_no"] if validated_address_data["telephone_no"] else address_data.telephone_no
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
            name = validated_data['name'] if 'name' in validated_data else None,
            read_level = validated_data['read_level'] if 'read_level' in validated_data else None,
            write_level = validated_data['write_level'] if 'write_level' in validated_data else None,
            speak_level = validated_data['speak_level'] if 'speak_level' in validated_data else None,
            exam_passed = validated_data['exam_passed'] if 'exam_passed' in validated_data else None,
        )

        return language.id

    def update(self, instance, validated_data):

        instance.name = (
            validated_data["name"] if validated_data["name"] else instance.name
        )

        instance.read_level = (
            validated_data["read_level"] if validated_data["read_level"] else instance.read_level
        )

        instance.write_level = (
            validated_data["write_level"] if validated_data["write_level"] else instance.write_level
        )

        instance.speak_level = (
            validated_data["speak_level"] if validated_data["speak_level"] else instance.speak_level
        )

        instance.exam_passed = (
            validated_data["exam_passed"] if validated_data["exam_passed"] else instance.exam_passed
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
            country_visited = validated_data['country_visited'] if 'country_visited' in validated_data else None,
            date_of_visit = validated_data['date_of_visit'] if 'date_of_visit' in validated_data else None,
            duration_of_visit = validated_data['duration_of_visit'] if 'duration_of_visit' in validated_data else None,
            purpose_of_visit = validated_data['purpose_of_visit'] if 'purpose_of_visit' in validated_data else None,
        )

        return visit.id

    def update(self, instance, validated_data):

        instance.country_visited = (
            validated_data["country_visited"] if validated_data["country_visited"] else instance.country_visited
        )

        instance.date_of_visit = (
            validated_data["date_of_visit"] if validated_data["date_of_visit"] else instance.date_of_visit
        )

        instance.duration_of_visit = (
            validated_data["duration_of_visit"] if validated_data["duration_of_visit"] else instance.duration_of_visit
        )

        instance.purpose_of_visit = (
            validated_data["purpose_of_visit"] if validated_data["purpose_of_visit"] else instance.purpose_of_visit
        )

        instance.save()

class UserDocumentsSerializer(serializers.ModelSerializer):

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

    def get_attachments(self,obj):
        attachments = obj.attachments.filter()
        serializer = UserDocumentsSerializer(attachments,many=True)
        return serializer.data

    def save(self, validated_data):

        user = User.objects.get(user_id = validated_data['user_id'])
        user_profile = user.user_profile

        paper = PublishedPapers.objects.create(
            paper_title = validated_data['paper_title'] if 'paper_title' in validated_data else None,
        )

        # for attachment_data in validated_data['attachments']:
        #     attachment = UserDocuments.objects.create(
        #         # doc_file_path = attachment_data['doc_file_path'],
        #         doc_name = attachment_data['doc_name'],
        #     )
        #     paper.attachments.add(attachment)

        for attachment_data in validated_data['attachments']:
            attachment = UserDocuments.objects.get(doc_id = attachment_data['doc_id'])
            paper.attachments.add(attachment)

        user_profile.published_papers.add(paper)

        return paper.id

    def update(self, instance, validated_data):

        instance.paper_title = (
            validated_data['paper_title'] if 'paper_title' in validated_data else instance.paper_title
        )

        for attachment_data in validated_data['attachments']:
            doc = UserDocuments.objects.get(doc_id = attachment_data['doc_id'])
            doc.file_path_name = (
                attachment_data['doc_file_path'] if 'doc_file_path' in attachment_data else doc.file_path_name
            )

            doc.doc_name = (
                attachment_data['doc_name'] if 'doc_name' in attachment_data else doc.doc_name
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
            title = validated_data['title'] if 'title' in validated_data else None,
            description = validated_data['description'] if 'description' in validated_data else None,
            from_date = validated_data['from_date'] if 'from_date' in validated_data else None,
            to_date = validated_data['to_date'] if 'to_date' in validated_data else None,
        )

        return professional_training.id

    def update(self, instance, validated_data):

        instance.title = (
            validated_data["title"] if validated_data["title"] else instance.title
        )

        instance.description = (
            validated_data["description"] if validated_data["description"] else instance.description
        )

        instance.from_date = (
            validated_data["from_date"] if validated_data["from_date"] else instance.from_date
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
            bond_title = validated_data['bond_title'] if 'bond_title' in validated_data else None,
            bond_details = validated_data['bond_details'] if 'bond_details' in validated_data else None,
            organisation_name = validated_data['organisation_name'] if 'organisation_name' in validated_data else None,
            bond_start_date = validated_data['bond_start_date'] if 'bond_start_date' in validated_data else None,
            bond_end_date=validated_data['bond_end_date'] if 'bond_end_date' in validated_data else None,
            notice_period_min = validated_data['notice_period_min'] if 'notice_period_min' in validated_data else None,
            notice_period_max = validated_data['notice_period_max'] if 'notice_period_max' in validated_data else None,
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

    name_of_applicant = serializers.SerializerMethodField(
        method_name="get_name_of_applicant", read_only=True
    )

    local_address = serializers.SerializerMethodField(
        method_name="get_local_address", read_only=True
    )

    permanent_address = serializers.SerializerMethodField(
        method_name="get_permanent_address", read_only=True
    )

    father_address = serializers.SerializerMethodField(
        method_name="get_father_address", read_only=True
    )

    education_details = serializers.SerializerMethodField(
        method_name="get_education_details", read_only=True
    )

    professional_trainings = serializers.SerializerMethodField(
        method_name="get_professional_trainings", read_only=True
    )

    published_papers = serializers.SerializerMethodField(
        method_name="get_published_papers", read_only=True
    )

    experiences = serializers.SerializerMethodField(
        method_name="get_experiences", read_only=True
    )

    other_info = serializers.SerializerMethodField(
        method_name="get_other_info", read_only=True
    )

    neeri_relation = serializers.SerializerMethodField(
        method_name="get_neeri_relation", read_only=True
    )

    overseas_visits = serializers.SerializerMethodField(
        method_name="get_overseas_visits", read_only=True
    )

    languages = serializers.SerializerMethodField(
        method_name="get_languages", read_only=True
    )

    references = serializers.SerializerMethodField(
        method_name="get_references", read_only=True
    )



    class Meta:
        model = UserProfile
        fields = (
            "name_of_applicant",
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
            "other_info",
            "neeri_relation",
            "overseas_visits",
            "languages",
            "references",
        )

    def get_name_of_applicant(self,obj):
        name_of_applicant = obj.user.first_name + ' ' + obj.user.middle_name + ' ' + obj.user.last_name
        return name_of_applicant

    def get_local_address(self,obj):
        local_address = obj.local_address
        serializer = LocationSerializer(local_address)
        return serializer.data

    def get_permanent_address(self,obj):
        permanent_address = obj.permanent_address
        serializer = LocationSerializer(permanent_address)
        return serializer.data

    def get_father_address(self,obj):
        father_address = obj.father_address
        serializer = LocationSerializer(father_address)
        return serializer.data

    def get_education_details(self,obj):
        education_details = obj.education_details.filter()
        serializer = UserEducationDetailsSerializer(education_details,many=True)
        return serializer.data

    def get_professional_trainings(self,obj):
        professional_trainings = obj.professional_trainings.filter()
        serializer = ProfessionalTrainingSerializer(professional_trainings,many=True)
        return serializer.data

    def get_published_papers(self,obj):
        published_papers = obj.published_papers.filter()
        serializer = PublishedPapersSerializer(published_papers,many=True)
        return serializer.data

    def get_experiences(self,obj):
        experiences = obj.experiences.filter()
        serializer = UserExperienceDetailsSerializer(experiences,many=True)
        return serializer.data

    def get_other_info(self,obj):
        othet_info = obj.other_info
        serializer = OtherInformationSerializer(othet_info)
        return serializer.data

    def get_neeri_relation(self,obj):
        neeri_relation = obj.neeri_relation.filter()
        serializer = NeeriRelationSerializer(neeri_relation,many=True)
        return serializer.data

    def get_overseas_visits(self,obj):
        overseas_visits = obj.overseas_visits.filter()
        serializer = OverseasVisitsSerializer(overseas_visits,many=True)
        return serializer.data

    def get_languages(self,obj):
        languages = obj.languages.filter()
        serializer = LanguagesSerializer(languages,many=True)
        return serializer.data

    def get_references(self,obj):
        references = obj.references.filter()
        serializer = ReferencesSerializer(references,many=True)
        return serializer.data
