from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from user.models import User, RoleMaster, UserRoles, UserProfile, Location, UserEducationDetails, UserExperienceDetails, \
    UserLanguages, UserReference, NeeriRelation, OverseasVisits, PublishedPapers, ProfessionalTraining, UserDocuments, \
    OtherInformation, UserPermissions, UserAuthentication
from job_posting.models import UserJobPositions, JobDocuments, JobPosting,SelectionProcessContent
from user.serializer import UserSerializer,AuthTokenCustomSerializer,UserProfileSerializer,UserRolesSerializer,\
    CustomUserSerializer,ApplicantUserPersonalInformationSerializer,LocationSerializer,\
    UserEducationDetailsSerializer,UserExperienceDetailsSerializer,NeeriRelationSerializer,\
    OverseasVisitsSerializer,LanguagesSerializer,ReferencesSerializer,PublishedPapersSerializer,\
    ProfessionalTrainingSerializer,UserProfilePreviewSerializer,OtherInformationSerializer
from job_posting.serializer import ApplicantJobPositionsSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from neeri_recruitment_portal.messeges import INACTIVE_ACCOUNT_ERROR
from django.contrib.auth import login, logout
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from knox.views import LogoutView as KnoxLogoutView
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

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
        data = request.data
        user = User.objects.get(email__exact=data['email'])
        roles = [role.role.role_name for role in UserRoles.objects.filter(user=user)]
        permissions = [permission.permission.permission_name for permission in UserPermissions.objects.filter(role__role_name__in=roles).distinct('permission')]
#         if not 'applicant' in roles:
#             return Response(data = {"messege":"You are not authorised user"}, status=400)
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
        # authentication = UserAuthentication.objects.get(user=user)
        result.data['user'] = serializer.data
        result.data['roles'] = roles
        result.data['permissions'] = permissions
        # result.data['email_verified'] = authentication.email_verified
        # result.data['mobile_verified'] = authentication.mobile_verified
        return Response(result.data, status=200)

class LogoutView(KnoxLogoutView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        request._auth.delete()
        logout(request)
        return Response(data = {"messege":"Logged out successfully"}, status=200)


class UserRegistartionView(APIView):
    permission_classes = [AllowAny, ]

    def post(self,request,*args,**kwargs):
        mobile_no = self.request.data['mobile_no']
        email = self.request.data['email']
        password = self.request.data['password']
        role = RoleMaster.objects.get(role_name__exact='applicant')
        if User.objects.filter(email=email).exists():
            return JsonResponse(data={"messege":"User Already Exist"},status=200)
        elif User.objects.filter(mobile_no=mobile_no).exists():
            return JsonResponse(data={"messege": "Mobile Number Already Exist"}, status=200)
        else:
            user = User.objects.create_user(mobile_no, email, password)
            UserRoles.objects.create(role=role,user=user)
            roles = [role.role.role_name for role in UserRoles.objects.filter(user=user)]
            permissions = [permission.permission.permission_name for permission in
                           UserPermissions.objects.filter(role__role_name__in=roles).distinct('permission')]
            serializer = UserSerializer(user)

            result = {}

            result['user'] = serializer.data
            result['roles'] = roles
            result['permissions'] = permissions
            # result['email_verified'] = authentication.email_verified
            # result['mobile_verified'] = authentication.mobile_verified
            return JsonResponse(data=result, status=200, safe=False)

class UserListView(APIView):
    def get(self,request,*args,**kwargs):
        users = User.objects.filter(is_deleted = False)
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=200)

class RetrievetUserView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=200)

class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        mobile_no = data['mobile_no']
        email = data['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse(data={"messege": "User Already Exist"},status=200)
        elif User.objects.filter(mobile_no=mobile_no).exists():
            return JsonResponse(data={"messege": "User Already Exist"}, status=200)
        else:
            user = User.objects.create_user(mobile_no=mobile_no,email=email)
            serializer = CustomUserSerializer(user,data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(instance=user,validated_data=data)
            return Response(serializer.data,status=200)

class UpdateUserView(APIView):
    def put(self, request, *args,**kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = self.request.data
        serializer = CustomUserSerializer(user,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user,validated_data=data)
        return Response(serializer.data, status=200)

class DeleteUserView(APIView):
    def delete(self,request,*args,**kwargs):
        try:
            id = self.kwargs['id']
            user = User.objects.get(user_id=id)
            # user.delete()
            user.is_deleted = True
            user.save()
            print(user.is_deleted)
            return Response(data = {"messege":"User Deleted Successfully."}, status=200)
        except:
            return Response(data={"messege": "User Not Found."}, status=404)

class ForgotPassword(APIView):
    
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        data = self.request.data
        email = data['email']

        try:
            user = User.objects.get(email__exact = email)
            if user:
                # Need to send Email with a link where user can reset password.
                return Response(data={"messege": "Link sent to your registered Email."}, status=200)
        except:
            return Response(data={"messege": "Email not found, enter valid email."}, status=404)

class ResetPassword(APIView):

    def post(self, request, *args, **kwargs):
        data = self.request.data
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        password = data['password']
        user.set_password(password)
        user.save()
        return Response(data={"messege":"Password reset Successfully."},status=200)


class ApplicantPersonalInformationView(APIView):

    def get(self,request,*args,**kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile:
                user_profile = user.user_profile
                serializer = ApplicantUserPersonalInformationSerializer(user_profile)
                return Response(serializer.data,status=200)
        except:
            return Response(data={"messege": "UserProfile not created","isEmpty":"true", "mobile_no": user.mobile_no}, status=200)


class ApplicantPersonalInformationUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = self.request.data
        try:
            user_profile = user.user_profile
        except:
            return Response(data={"messege": "UserProfile does not exist for the given user,create UserProfile first."}, status=200)
        serializer = ApplicantUserPersonalInformationSerializer(user_profile, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user_profile, validated_data=data)
        return Response(serializer.data, status=200)


class ApplicantPersonalInformationCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile :
                return Response(data={"messege":"UserProfile for Given User Already Exist"},status=200)
        except:
            data = self.request.data
            serializer = ApplicantUserPersonalInformationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(validated_data=data)
            user_profile = UserProfile.objects.get(user = user)
            serializer = ApplicantUserPersonalInformationSerializer(user_profile)
            return Response(serializer.data,status=200)

class ApplicantAddressView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id = id)
        address_type = self.request.GET['address_type']
        try:
            if address_type == 'local_address' and user.user_profile.local_address:
                location = user.user_profile.local_address
            elif address_type == 'permanent_address' and user.user_profile.permanent_address:
                location = user.user_profile.permanent_address
            elif address_type == 'father_address' and user.user_profile.father_address:
                location = user.user_profile.father_address

            serializer = LocationSerializer(location)
            # serializer.is_valid(raise_exception=True)
            result = serializer.data
            result['is_permenant_address_same_as_local'] = user.user_profile.is_permenant_address_same_as_local
            result['is_father_address_same_as_local'] = user.user_profile.is_father_address_same_as_local
            return Response(result,status=200)
        except:
            return Response(data={"messege": "Address not created","isEmpty":"true"}, status=200)

class ApplicantAddressUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = self.request.data
        address_type = self.request.GET['address_type']
        if address_type == 'local_address':
            location = user.user_profile.local_address
            serializer = LocationSerializer(location, data=data)
        elif address_type == 'permanent_address':
            if 'is_permenant_address_same_as_local' in self.request.GET:
                is_permenant_address_same_as_local = self.request.GET['is_permenant_address_same_as_local']
                if is_permenant_address_same_as_local == True or is_permenant_address_same_as_local == 'true':
                    user.user_profile.permanent_address = user.user_profile.local_address
                    user.user_profile.is_permenant_address_same_as_local = True
                    user.user_profile.save()
                    location = user.user_profile.permanent_address
                    serializer = LocationSerializer(location, data=data)
                    serializer.is_valid(raise_exception=True)
                    result = serializer.data
                    result['is_permenant_address_same_as_local'] = user.user_profile.is_permenant_address_same_as_local
                    result['is_father_address_same_as_local'] = user.user_profile.is_father_address_same_as_local
                    return Response(result, status=200)
            else:
                location = user.user_profile.permanent_address
                serializer = LocationSerializer(location, data=data)
        else:
            if 'is_father_address_same_as_local' in self.request.GET:
                is_father_address_same_as_local = self.request.GET['is_father_address_same_as_local']
                if is_father_address_same_as_local == True or is_father_address_same_as_local == 'true':
                    user.user_profile.father_address = user.user_profile.local_address
                    user.user_profile.is_father_address_same_as_local = True
                    user.user_profile.save()
                    location = user.user_profile.father_address
                    serializer = LocationSerializer(location, data=data)
                    serializer.is_valid(raise_exception=True)
                    result = serializer.data
                    result['is_permenant_address_same_as_local'] = user.user_profile.is_permenant_address_same_as_local
                    result['is_father_address_same_as_local'] = user.user_profile.is_father_address_same_as_local
                    return Response(result, status=200)
            else:
                location = user.user_profile.father_address
                serializer = LocationSerializer(location, data=data)

        serializer.is_valid(raise_exception=True)
        serializer.update(instance=location, validated_data=data)
        serializer.is_valid(raise_exception=True)
        result = serializer.data
        result['is_permenant_address_same_as_local'] = user.user_profile.is_permenant_address_same_as_local
        result['is_father_address_same_as_local'] = user.user_profile.is_father_address_same_as_local
        return Response(result, status=200)

class ApplicantAddressCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        address_type = self.request.GET['address_type']
        if 'is_permenant_address_same_as_local' in self.request.GET:
            is_permenant_address_same_as_local = self.request.GET['is_permenant_address_same_as_local']
            if address_type == 'permanent_address' and is_permenant_address_same_as_local == True or is_permenant_address_same_as_local == 'true':
                permanent_address = user.user_profile.local_address
                user.user_profile.permanent_address = permanent_address
                user.user_profile.is_permenant_address_same_as_local = True
                user.user_profile.save()
                serializer = LocationSerializer(permanent_address)
                result = serializer.data
                result['is_permenant_address_same_as_local'] = user.user_profile.is_permenant_address_same_as_local
                result['is_father_address_same_as_local'] = user.user_profile.is_father_address_same_as_local
                return Response(result, status=200)
        elif 'is_father_address_same_as_local' in self.request.GET:
            is_father_address_same_as_local = self.request.GET['is_father_address_same_as_local']
            if address_type == 'father_address' and is_father_address_same_as_local == True or is_father_address_same_as_local == 'true':
                father_address = user.user_profile.local_address
                user.user_profile.father_address = father_address
                user.user_profile.is_father_address_same_as_local = True
                user.user_profile.save()
                serializer = LocationSerializer(father_address)
                result = serializer.data
                result['is_permenant_address_same_as_local'] = user.user_profile.is_permenant_address_same_as_local
                result['is_father_address_same_as_local'] = user.user_profile.is_father_address_same_as_local
                return Response(result, status=200)
        else:
            data = self.request.data
            serializer = LocationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=data)
            location = Location.objects.get(id=result)
            if address_type == 'local_address':
                if user.user_profile.local_address:
                    Location.objects.get(id=result).delete()
                    return Response(data={"messege":"Local Address for Given User Already Exist"},status=200)
                else:
                    user.user_profile.local_address = location
                    user.user_profile.save()
            elif address_type == 'permanent_address':
                if user.user_profile.permanent_address:
                    Location.objects.get(id=result).delete()
                    return Response(data={"messege":"Permanent Address for Given User Already Exist"},status=200)
                else:
                    user.user_profile.permanent_address = location
                    user.user_profile.save()
            else:
                if user.user_profile.father_address:
                    Location.objects.get(id=result).delete()
                    return Response(data={"messege":"Father Address for Given User Already Exist"},status=200)
                else:
                    user.user_profile.father_address = location
                    user.user_profile.save()

            serializer = LocationSerializer(location)
            # serializer.is_valid(raise_exception=True)
            result = serializer.data
            result['is_permenant_address_same_as_local'] = user.user_profile.is_permenant_address_same_as_local
            result['is_father_address_same_as_local'] = user.user_profile.is_father_address_same_as_local
            return Response(result, status=200)

class ApplicantQualificationsListView(APIView):


    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile.education_details.filter(is_deleted=False).count() > 0:
                qualifications = user.user_profile.education_details.filter(is_deleted=False)
                serializer = UserEducationDetailsSerializer(qualifications,many=True)
                return Response(serializer.data, status=200)
            else:
                return Response(data={"messege": "User Qualifications not found","isEmpty":"true"}, status=200)
        except:
            return Response(data={"messege": "User Qualifications not found","isEmpty":"true"}, status=200)


class ApplicantQualificationUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        qualifications = user.user_profile.education_details.filter(is_deleted=False)
        for qualification_data in data:
            qualification = user.user_profile.education_details.get(id = qualification_data['id'])
            serializer = UserEducationDetailsSerializer(qualification,data=qualification_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=qualification, validated_data=qualification_data)
        serializer = UserEducationDetailsSerializer(qualifications,many=True)
        return Response(serializer.data, status=200)

class ApplicantQualificationCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for qualification_data in data:
            serializer = UserEducationDetailsSerializer(data=qualification_data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=qualification_data)
            qualification = UserEducationDetails.objects.get(id=result)
            user.user_profile.education_details.add(qualification)
            user.user_profile.save()
        qualifications = user.user_profile.education_details.filter(is_deleted=False)
        serializer = UserEducationDetailsSerializer(qualifications,many=True)
        return Response(serializer.data, status=200)

class ApplicantQualificationDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            education = user.user_profile.education_details.get(id=data['id'])
            education.is_deleted = True
            education.save()
            return Response(data={"message": "Record Deleted Successfully."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

class ApplicantExperiencesListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile.experiences.filter(is_deleted=False).count() > 0:
                experiences = user.user_profile.experiences.filter(is_deleted=False)
                serializer = UserExperienceDetailsSerializer(experiences, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response(data={"messege": "User Experiences not found","isEmpty":"true"}, status=200)
        except:
            return Response(data={"messege": "User Experiences not found","isEmpty":"true"}, status=200)


class ApplicantExperienceUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        experiences = user.user_profile.experiences.filter(is_deleted=False)
        for experience_data in data:
            experience = user.user_profile.experiences.get(id=experience_data['id'])
            serializer = UserExperienceDetailsSerializer(experience, data=experience_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=experience, validated_data=experience_data)
        serializer = UserExperienceDetailsSerializer(experiences, many=True)
        return Response(serializer.data, status=200)


class ApplicantExperienceCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for experience_data in data:
            serializer = UserExperienceDetailsSerializer(data=experience_data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=experience_data)
            experience = UserExperienceDetails.objects.get(id=result)
            user.user_profile.experiences.add(experience)
            user.user_profile.save()
        experiences = user.user_profile.experiences.filter(is_deleted=False)
        serializer = UserExperienceDetailsSerializer(experiences, many=True)
        return Response(serializer.data, status=200)

class ApplicantExperienceDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            experience = user.user_profile.experiences.get(id=data['id'])
            experience.is_deleted = True
            experience.save()
            return Response(data={"message": "Record Deleted Successfully."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

class NeeriRelationsListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile.neeri_relation.filter(is_deleted=False).count() > 0:
                neeri_relations = user.user_profile.neeri_relation.filter(is_deleted=False)
                serializer = NeeriRelationSerializer(neeri_relations, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response(data={"messege": "Neeri Relations not found","isEmpty":"true"}, status=200)
        except:
            return Response(data={"messege": "Neeri Relations not found","isEmpty":"true"}, status=200)

class NeeriRelationUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        neeri_relations = user.user_profile.neeri_relation.filter(is_deleted=False)
        for relation_data in data:
            relation = user.user_profile.neeri_relation.get(id=relation_data['id'])
            serializer = NeeriRelationSerializer(relation, data=relation_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=relation, validated_data=relation_data)
        serializer = NeeriRelationSerializer(neeri_relations, many=True)
        return Response(serializer.data, status=200)

class NeeriRelationCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for relation_data in data:
            serializer = NeeriRelationSerializer(data=relation_data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=relation_data)
            relation = NeeriRelation.objects.get(id=result)
            user.user_profile.neeri_relation.add(relation)
            user.user_profile.save()
        experiences = user.user_profile.neeri_relation.filter(is_deleted=False)
        serializer = NeeriRelationSerializer(experiences, many=True)
        return Response(serializer.data, status=200)

class NeeriRelationDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            neeri_relation = user.user_profile.neeri_relation.get(id=data['id'])
            neeri_relation.is_deleted = True
            neeri_relation.save()
            return Response(data={"message": "Record Deleted Successfully."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

class OverseasVisitsListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile.overseas_visits.filter(is_deleted=False).count() > 0:
                visits = user.user_profile.overseas_visits.filter(is_deleted=False)
                serializer = OverseasVisitsSerializer(visits, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response(data={"messege": "Overseas Visits not found","isEmpty":"true"}, status=200)
        except:
            return Response(data={"messege": "Overseas Visits not found","isEmpty":"true"}, status=200)

class OverseasVisitsCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for visits_data in data:
            serializer = OverseasVisitsSerializer(data=visits_data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=visits_data)
            visit = OverseasVisits.objects.get(id=result)
            user.user_profile.overseas_visits.add(visit)
            user.user_profile.save()
        visits = user.user_profile.overseas_visits.filter(is_deleted=False)
        serializer = OverseasVisitsSerializer(visits, many=True)
        return Response(serializer.data, status=200)

class OverseasVisitsUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        visits = user.user_profile.overseas_visits.filter(is_deleted=False)
        for visits_data in data:
            visit = user.user_profile.overseas_visits.get(id=visits_data['id'])
            serializer = OverseasVisitsSerializer(visit, data=visits_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=visit, validated_data=visits_data)
        serializer = OverseasVisitsSerializer(visits, many=True)
        return Response(serializer.data, status=200)

class OverseasVisitsDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            overseas_visit = user.user_profile.overseas_visits.get(id=data['id'])
            overseas_visit.is_deleted = True
            overseas_visit.save()
            return Response(data={"message": "Record Deleted Successfully."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

class ApplicantReferencesListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile.references.filter(is_deleted=False).count() > 0:
                references = user.user_profile.references.filter(is_deleted=False)
                serializer = ReferencesSerializer(references, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response(data={"messege": "References not found","isEmpty":"true"}, status=200)
        except:
            return Response(data={"messege": "References not found","isEmpty":"true"}, status=200)

class ApplicantReferencesCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for reference_data in data:
            serializer = ReferencesSerializer(data=reference_data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=reference_data)
            reference = UserReference.objects.get(id=result)
            user.user_profile.references.add(reference)
            user.user_profile.save()
        references = user.user_profile.references.filter(is_deleted=False)
        serializer = ReferencesSerializer(references, many=True)
        return Response(serializer.data, status=200)

class ApplicantReferencesUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        references = user.user_profile.references.filter(is_deleted=False)
        for reference_data in data:
            reference = user.user_profile.references.get(id=reference_data['id'])
            serializer = ReferencesSerializer(reference, data=reference_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=reference, validated_data=reference_data)
        serializer = ReferencesSerializer(references, many=True)
        return Response(serializer.data, status=200)

class ApplicantReferencesDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            reference = user.user_profile.references.get(id=data['id'])
            reference.is_deleted = True
            reference.save()
            return Response(data={"message": "Record Deleted Successfully."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)


class ApplicantLanguagesListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile.languages.filter(is_deleted=False).count() > 0:
                languages = user.user_profile.languages.filter(is_deleted=False)
                serializer = LanguagesSerializer(languages, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response(data={"messege": "Languages not found","isEmpty":"true"}, status=200)
        except:
            return Response(data={"messege": "Languages not found","isEmpty":"true"}, status=200)

class ApplicantLanguagesCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for language_data in data:
            serializer = LanguagesSerializer(data=language_data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=language_data)
            language = UserLanguages.objects.get(id=result)
            user.user_profile.languages.add(language)
            user.user_profile.save()
        languages = user.user_profile.languages.filter(is_deleted=False)
        serializer = LanguagesSerializer(languages, many=True)
        return Response(serializer.data, status=200)

class ApplicantLanguagesUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        languages = user.user_profile.languages.filter(is_deleted=False)
        for language_data in data:
            language = user.user_profile.languages.get(id=language_data['id'])
            serializer = LanguagesSerializer(language, data=language_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=language, validated_data=language_data)
        serializer = LanguagesSerializer(languages, many=True)
        return Response(serializer.data, status=200)

class ApplicantLanguagesDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            language = user.user_profile.languages.get(id=data['id'])
            language.is_deleted = True
            language.save()
            return Response(data={"message": "Record Deleted Successfully."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

class PublishedPapersListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile.published_papers.filter(is_deleted=False).count() >0:
                papers = user.user_profile.published_papers.filter(is_deleted=False)
                serializer = PublishedPapersSerializer(papers, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response(data={"messege": "Published Papers not found","isEmpty":"true"}, status=200)
        except:
            return Response(data={"messege": "Published Papers not found","isEmpty":"true"}, status=200)

class PublishedPapersCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for paper_data in data:
            temp_paper_data = paper_data
            temp_paper_data['user_id'] = id
            serializer = PublishedPapersSerializer(data=temp_paper_data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=temp_paper_data)
            paper = PublishedPapers.objects.get(id=result)
            user.user_profile.published_papers.add(paper)
            user.user_profile.save()
        papers = user.user_profile.published_papers.filter(is_deleted=False)
        serializer = PublishedPapersSerializer(papers, many=True)
        return Response(serializer.data, status=200)

class PublishedPapersUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for paper_data in data:
            paper = user.user_profile.published_papers.get(id=paper_data['id'])
            serializer = PublishedPapersSerializer(paper, data=paper_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=paper, validated_data=paper_data)
        papers = user.user_profile.published_papers.filter(is_deleted=False)
        response_data = PublishedPapersSerializer(papers, many=True)
        return Response(response_data.data, status=200)

class PublishedPapersDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            paper = user.user_profile.published_papers.get(id=data['id'])
            paper.is_deleted = True
            paper.save()
            return Response(data={"message": "Record Deleted Successfully."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

class ApplicantAppliedJobListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if UserJobPositions.objects.filter(user=user,is_deleted=False).count() >0:
            user_job_positions = UserJobPositions.objects.filter(user=user,is_deleted=False)
            serializer = ApplicantJobPositionsSerializer(user_job_positions, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege": "Applied job list not found","isEmpty":"true"}, status=200)

##While creating new entry of UserJobPositions set closing_date to a closing_date og JobPosting

class ApplicantProfilePercentageView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            percentage = user.user_profile.profile_percentage
            return Response(data={"percentage": percentage}, status=200)
        except:
            return Response(data={"messsege": "User-Profile not found","percentage":"0"}, status=200)

class ProfessionalTrainingListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            if user.user_profile.professional_trainings.filter(is_deleted=False).count() > 0:
                professional_trainings = user.user_profile.professional_trainings.filter(is_deleted=False)
                serializer = ProfessionalTrainingSerializer(professional_trainings, many=True)
                return Response(serializer.data, status=200)
            else:
                return Response(data={"messege": "Professional Trainings not found", "isEmpty": "true"}, status=200)
        except:
            return Response(data={"messege": "Professional Trainings not found", "isEmpty": "true"}, status=200)

class ProfessionalTrainingUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        professional_trainings = user.user_profile.professional_trainings.filter(is_deleted=False)
        for professional_training_data in data:
            professional_training = user.user_profile.professional_trainings.get(id=professional_training_data['id'])
            serializer = ProfessionalTrainingSerializer(professional_training, data=professional_training_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=professional_training, validated_data=professional_training_data)
        serializer = ProfessionalTrainingSerializer(professional_trainings, many=True)
        return Response(serializer.data, status=200)


class ProfessionalTrainingCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        for professional_training_data in data:
            serializer = ProfessionalTrainingSerializer(data=professional_training_data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=professional_training_data)
            professional_training = ProfessionalTraining.objects.get(id=result)
            user.user_profile.professional_trainings.add(professional_training)
            user.user_profile.save()
        professional_trainings = user.user_profile.professional_trainings.filter(is_deleted=False)
        serializer = ProfessionalTrainingSerializer(professional_trainings, many=True)
        return Response(serializer.data, status=200)

class ProfessionalTrainingDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            professional_training = user.user_profile.professional_trainings.get(id=data['id'])
            professional_training.is_deleted = True
            professional_training.save()
            return Response(data={"message": "Record Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

class FileUpload(APIView):

    def post(self, request, *args, **kwargs):
        # id = self.kwargs['id']
        # data = self.request.data
        if 'file' not in request.data:
            Response(data={"messege": "No file Found"}, status=200)
        file = request.data['file']
        doc_type = self.request.GET['doc_type']
        print(doc_type)
        if doc_type == 'profile_photo':
            user = User.objects.get(user_id=self.request.GET['user_id'])
            if file.name.endswith('jpg') or file.name.endswith('png') or file.name.endswith('jpeg') or \
                file.name.endswith('JPG') or file.name.endswith('PNG') or file.name.endswith('JPEG'):
                default_storage.save(settings.MEDIA_ROOT + '/applicant_documents/' + str(user.user_id) + '/' + 'profile.' + file.name.split('.')[1], ContentFile(file.read()))
                filename = 'profile.' + file.name.split('.')[1]
                temp_path = settings.BASE_URL + settings.MEDIA_URL + 'applicant_documents/' + str(user.user_id) + '/' + filename
                doc = UserDocuments.objects.create(doc_file_path=temp_path, doc_name=filename)
                user.user_profile.documents.add(doc)
                user.user_profile.profile_photo = temp_path
                user.user_profile.save()
            else:
                    return Response(data={"messege":"Enter file of type jpg,jpeg and png."},status=200)

        elif doc_type == 'paper_attachment':
            user = User.objects.get(user_id=self.request.GET['user_id'])
            default_storage.save(
                settings.MEDIA_ROOT + '/applicant_documents/' + str(user.user_id) + '/' + file.name,
                ContentFile(file.read()))
            temp_path = settings.BASE_URL + settings.MEDIA_URL + 'applicant_documents/' + str(user.user_id) + '/' + file.name
            doc = UserDocuments.objects.create(doc_file_path=temp_path, doc_name=file.name)

        elif doc_type == 'office_memo':
            job_posting_id = str(self.request.GET['job_posting_id'])
            job_posting = JobPosting.objects.get(job_posting_id=job_posting_id)
            default_storage.save(settings.MEDIA_ROOT + '/job_posting_documents/' + str(job_posting.job_posting_id) + '/' + file.name, ContentFile(file.read()))
            temp_path = settings.BASE_URL + settings.MEDIA_URL + 'job_posting_documents/' + str(job_posting.job_posting_id) + '/' + file.name
            doc = JobDocuments.objects.create(doc_file_path = temp_path,doc_name = file.name)
            job_posting.office_memorandum = doc
            job_posting.save()
        return Response(data={"messege": "File uploaded successfully","doc_file_path":doc.doc_file_path,"doc_name":doc.doc_name,"doc_id":doc.doc_id}, status=200)

class OtherInformationDetailView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            user = User.objects.get(user_id=id)
            other_info = user.user_profile.other_info
            serializer = OtherInformationSerializer(other_info)
            return Response(serializer.data, status=200)
        except:
            return Response(data={"messege": "OtherInfo not found", "isEmpty": "true"}, status=200)

class OtherInformationCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        if user.user_profile.other_info:
            return Response(data={"messege":"OtherInformation Already Created"},status=200)
        else:
            serializer = OtherInformationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=data)
            other_info = OtherInformation.objects.get(id=result)
            user.user_profile.other_info = other_info
            user.user_profile.save()
            serializer = OtherInformationSerializer(other_info)
            return Response(serializer.data, status=200)

class OtherInformationUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        other_info = user.user_profile.other_info
        serializer = OtherInformationSerializer(other_info, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=other_info, validated_data=data)
        serializer = OtherInformationSerializer(other_info)
        return Response(serializer.data, status=200)

class OtherInformationDeleteView(APIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = request.data
        try:
            othet_info = user.user_profile.other_info
            othet_info.is_deleted = True
            othet_info.save()
            return Response(data={"message": "Record Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)

class ProfileDetailView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            user = User.objects.get(user_id=id)
            serializer = UserProfilePreviewSerializer(user.user_profile)
            return Response(serializer.data, status=200)
        except:
            return Response(data={"messege":"No Data Found."},status=200)

class ApplicantListView(APIView):

    def get(self, request, *args, **kwargs):
        applicants = User.objects.filter(is_deleted=False,user_profile__roles__role_name__icontains='applicant')
        serializer = CustomUserSerializer(applicants,many=True)
        return Response(serializer.data, status=200)

