from user.models import User,UserProfile,Location
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
#
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
        # fields = "__all__"
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
                 ) + profile_names

class UserSerializer(serializers.ModelSerializer):

    user_profile = UserProfileSerializer(required=False)

    class Meta:
        model = User

        profile_names = ("user_profile",)

        fields = (
                    "id",
                     "username",
                     "email",
                     "created_at",
                 ) + profile_names



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
        print('attrs',attrs)
        return attrs