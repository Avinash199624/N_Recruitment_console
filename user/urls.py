from django.contrib import admin
from django.urls import path
from user.views import UserRegistartionView
from user.views import LoginView,LogoutView,UserListView,RetrievetUserView,UpdateUserView,CreateUserView,DeleteUserView,ForgotPassword

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', UserRegistartionView.as_view(), name='signup'),
    path('get-user/<uuid:id>/', RetrievetUserView.as_view(), name="get-user"),
    path('delete-user/<uuid:id>', DeleteUserView.as_view(), name="delete-user"),
    path('update-user/<uuid:id>', UpdateUserView.as_view(), name="update-user"),
    path('create-user/', CreateUserView.as_view(), name="create-user"),
    path('user-list/', UserListView.as_view(), name="user-list"),
    path('forgot-password/', ForgotPassword.as_view(), name="forgot-password"),
]