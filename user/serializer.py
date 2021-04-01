from user.models import User,UserProfile,Location
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
        fields = '__all__'

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
class UserSerializer(serializers.ModelSerializer):

    user_profile = UserProfileSerializer(required=False)
    # user_roles = UserRolesSerializer(required=False,many=True)

    class Meta:
        model = User

        profile_names = ("user_profile",)

        fields = (
                    "id",
                     "username",
                     "email",
                     "created_at",
                     "is_deleted",
                 ) + profile_names

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
        )

    def get_mobile_no(self,obj):
        mobile_no = obj.user_profile.mobile_no
        return mobile_no

    def get_phone_no(self,obj):
        phone_no = obj.user_profile.phone_no
        return phone_no

    def get_gender(self,obj):
        gender = obj.user_profile.gender
        return gender

    def get_date_of_birth(self,obj):
        date_of_birth = obj.user_profile.date_of_birth
        return date_of_birth

    def get_age(self,obj):
        age = obj.user_profile.age
        return age

    def get_status(self,obj):
        status = obj.user_profile.status
        return status

    def get_higher_qualification(self,obj):
        higher_qualification = obj.user_profile.higher_qualification
        return higher_qualification

    def get_local_address(self,obj):
        local_address = obj.user_profile.local_address.all()
        serializer = LocationSerializer(local_address,many=True)
        return serializer.data

    def get_permanent_address(self,obj):
        permanent_address = obj.user_profile.permanent_address.all()
        serializer = LocationSerializer(permanent_address,many=True)
        return serializer.data

    def update(self, instance, validated_data):

        user_profile = validated_data["user_profile"]

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
            local_address_data = user_profile["local_address"][0]
            permanent_address_data = user_profile["permanent_address"][0]

            if instance.user_profile:
                instance.user_profile.phone_no = (
                    user_profile["phone_no"] if user_profile["phone_no"] else instance.user_profile.phone_no
                )

                instance.user_profile.mobile_no = (
                    user_profile["mobile_no"] if user_profile["mobile_no"] else instance.user_profile.mobile_no
                )

                instance.user_profile.gender = (
                    user_profile["gender"] if user_profile["gender"] else instance.user_profile.gender
                )

                instance.user_profile.date_of_birth = (
                    user_profile["date_of_birth"] if user_profile["date_of_birth"] else instance.user_profile.date_of_birth
                )

                instance.user_profile.age = (
                    user_profile["age"] if user_profile["age"] else instance.user_profile.age
                )

                instance.user_profile.status = (
                    user_profile["status"] if user_profile["status"] else instance.user_profile.status
                )

                instance.user_profile.higher_qualification = (
                    user_profile["higher_qualification"] if user_profile["higher_qualification"] else instance.user_profile.higher_qualification
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
            user_profile_local_address = validated_data['user_profile']['local_address']
            user_profile_permanent_address = validated_data['user_profile']['permanent_address']

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

            user_profile_data = validated_data['user_profile']

            user_profile = UserProfile.objects.create(
                user=instance,
                gender=user_profile_data['gender'],
                phone_no=user_profile_data['phone_no'],
                mobile_no=user_profile_data['mobile_no'],
                date_of_birth=user_profile_data['date_of_birth'],
                age=user_profile_data['age'],
                status=user_profile_data['status'],
                higher_qualification=user_profile_data['higher_qualification'],
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
            user_profile_local_address = validated_data['user_profile']['local_address']
            user_profile_permanent_address = validated_data['user_profile']['permanent_address']

            local_address = Location.objects.create(
                address1 = user_profile_local_address[0]['address1'],
                address2 = user_profile_local_address[0]['address2'],
                address3 = user_profile_local_address[0]['address3'],
                city = user_profile_local_address[0]['city'],
                state = user_profile_local_address[0]['state'],
                country = user_profile_local_address[0]['country'],
                postcode = user_profile_local_address[0]['postcode'],
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

            user_profile_data = validated_data['user_profile']

            user_profile = UserProfile.objects.create(
                user = instance,
                gender = user_profile_data['gender'],
                phone_no = user_profile_data['phone_no'],
                mobile_no = user_profile_data['mobile_no'],
                date_of_birth = user_profile_data['date_of_birth'],
                age = user_profile_data['age'],
                status = user_profile_data['status'],
                higher_qualification = user_profile_data['higher_qualification'],
            )
            user_profile.local_address.add(local_address)
            user_profile.permanent_address.add(permanent_address)

            instance.user_profile = user_profile
            instance.user_profile.save()
            instance.save()

