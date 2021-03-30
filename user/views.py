from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from user.models import User
from user.serializer import UserSerializer,AuthTokenCustomSerializer
from django.contrib.auth.models import auth
from knox.views import LoginView as KnoxLoginView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from neeri_recruitment_portal.messeges import INACTIVE_ACCOUNT_ERROR
from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from knox.views import LogoutView as KnoxLogoutView


class LoginResponseViewMixin:

    def get_post_response_data(self, request, token, instance):

        print('INSIDE LoginResponseViewMixin')

        serializer = self.response_serializer_class(
            data={
                "expiry": self.format_expiry_datetime(instance.expiry),
                "token": token,
                "user": self.get_user_serializer_class()(
                    request.user, context=self.get_context()
                ).data,
            }
        )
        # Note: This serializer was only created to easily document on swagger
        # the return of this endpoint, so the validation it's not really used
        serializer.is_valid(raise_exception=True)
        print('DONE')
        return serializer.initial_data

class LoginView(KnoxLoginView,LoginResponseViewMixin):
    """
    Login view adapted for our needs. Since by default all user operations
    need to be authenticated, we need to explicitly set it to AllowAny.
    """
    permission_classes = [AllowAny, ]

    @csrf_exempt
    def post(self, request, format=None):
        serializer = AuthTokenCustomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        print('user',serializer.data)

        if not getattr(user, "is_active", None):
            raise AuthenticationFailed(INACTIVE_ACCOUNT_ERROR, code="account_disabled")
        res = login(request, user)
        print('res',res)

        result = super(LoginView, self).post(request, format=None)
        serializer = UserSerializer(user)
        # return result
        return JsonResponse(serializer.data,status=200,safe=False)



class UserRegistartionView(APIView):
    permission_classes = [AllowAny, ]

    def post(self,request,*args,**kwargs):
        username = self.request.data['fullname']
        email = self.request.data['email']
        password = self.request.data['password']
        if User.objects.filter(email=email).exists():
            return JsonResponse(data={"messege":"User Already Exist"},status=401)
        else:
            user = User.objects.create_user(username, email, password)
            serializer = UserSerializer(user)
            return JsonResponse(data=serializer.data, status=200, safe=False)

class LogoutView(KnoxLogoutView):

    @csrf_exempt
    def post(self, request, format=None):
        print('Logged Out Successfully')
        request._auth.delete()
        logout(request)

        return Response(None, status=HTTP_204_NO_CONTENT)