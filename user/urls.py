from django.contrib import admin
from django.urls import path
from user.views import UserRegistartionView
from user.views import LoginView,LogoutView,UserListView,RetrievetUserView,UpdateUserView,CreateUserView,DeleteUserView,ForgotPassword,\
    ApplicantPersonalInformationView,ApplicantPersonalInformationUpdateView,\
    ApplicantPersonalInformationCreateView,ApplicantAddressView,ApplicantAddressCreateView,\
    ApplicantAddressUpdateView

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

    #### Public Portal User URL's

    path('public/personal_info/<uuid:id>/', ApplicantPersonalInformationView.as_view(), name="get-applicant-personal-info"),
    path('public/personal_info_update/<uuid:id>/', ApplicantPersonalInformationUpdateView.as_view(), name="update-applicant-personal-info"),
    path('public/personal_info_create/<uuid:id>/', ApplicantPersonalInformationCreateView.as_view(), name="create-applicant-personal-info"),

    path('public/applicant_address/<uuid:id>/', ApplicantAddressView.as_view(), name="get-applicant-address"),
    path('public/applicant_address_create/<uuid:id>/', ApplicantAddressCreateView.as_view(), name="create-applicant-address"),
    path('public/applicant_address_update/<uuid:id>/', ApplicantAddressUpdateView.as_view(), name="update-applicant-address"),
]