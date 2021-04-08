from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from user.models import User,UserProfile
from user.serializer import UserSerializer,AuthTokenCustomSerializer,UserProfileSerializer,CustomUserSerializer
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
    def post(self, request, *args, **kwargs):
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
        result.data['user'] = serializer.data
        # return result
        return Response(result.data,status=200)



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
    def post(self, request, *args, **kwargs):
        print('Logged Out Successfully')
        request._auth.delete()
        logout(request)
        return Response(data = {"messege":"Logged out successfully"}, status=200)

class UserListView(APIView):
    def get(self,request,*args,**kwargs):
        users = User.objects.filter(is_deleted = False)
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=200)

class RetrievetUserView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(id=id)
        print("HELLO");
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=200)

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        username = data['username']
        email = data['email']
        user = User.objects.create_user(username=username,email=email)
        serializer = CustomUserSerializer(user,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(instance=user,validated_data=data)
        return Response(serializer.data,status=200)

class UpdateUserView(APIView):
    def put(self, request, *args,**kwargs):
        id = self.kwargs['id']
        user = User.objects.get(id=id)
        data = self.request.data
        serializer = CustomUserSerializer(user,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user,validated_data=data)
        return Response(serializer.data, status=200)

class DeleteUserView(APIView):
    def delete(self,request,*args,**kwargs):
        try:
            id = self.kwargs['id']
            user = User.objects.get(id=id)
            # user.delete()
            user.is_deleted = True
            user.save()
            print(user.is_deleted)
            return Response(data = {"messege":"User Deleted Successfully."}, status=200)
        except:
            return Response(data={"messege": "User Not Found."}, status=401)

class ForgotPassword(APIView):
    
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        email = data['email']

        try:
            user = User.objects.get(email__exact = email)
            if user:
                return Response(data={"messege": "Mail sent to your registered Email."}, status=200)
        except:
            return Response(data={"messege": "Email not found, enter valid email."}, status=400)
