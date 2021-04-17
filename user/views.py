from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from user.models import User,RoleMaster,UserRoles,UserProfile,Location,UserEducationDetails,UserExperienceDetails,\
    UserLanguages,UserReference,NeeriRelation,OverseasVisits,PublishedPapers
from job_posting.models import UserJobPositions
from user.serializer import UserSerializer,AuthTokenCustomSerializer,UserProfileSerializer,UserRolesSerializer,\
    CustomUserSerializer,ApplicantUserPersonalInformationSerializer,LocationSerializer,\
    UserEducationDetailsSerializer,UserExperienceDetailsSerializer,NeeriRelationSerializer,\
    OverseasVisitsSerializer,LanguagesSerializer,ReferencesSerializer,PublishedPapersSerializer
from job_posting.serializer import ApplicantJobPositionsSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from neeri_recruitment_portal.messeges import INACTIVE_ACCOUNT_ERROR
from django.contrib.auth import login, logout
from rest_framework.response import Response
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

class LogoutView(KnoxLogoutView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print('Logged Out Successfully')
        request._auth.delete()
        logout(request)
        return Response(data = {"messege":"Logged out successfully"}, status=200)

class UserRegistartionView(APIView):
    permission_classes = [AllowAny, ]

    def post(self,request,*args,**kwargs):
        username = self.request.data['fullname']
        email = self.request.data['email']
        password = self.request.data['password']
        role = RoleMaster.objects.get(role_name__exact='applicant')
        if User.objects.filter(email=email).exists():
            return JsonResponse(data={"messege":"User Already Exist"},status=401)
        elif User.objects.filter(username=username).exists():
            return JsonResponse(data={"messege": "User Already Exist"}, status=401)
        else:
            user = User.objects.create_user(username, email, password)
            UserRoles.objects.create(role=role,user=user)
            serializer = UserSerializer(user)
            return JsonResponse(data=serializer.data, status=200, safe=False)

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
        username = data['username']
        email = data['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse(data={"messege":"User Already Exist"},status=401)
        elif User.objects.filter(username=username).exists():
            return JsonResponse(data={"messege": "User Already Exist"}, status=401)
        else:
            user = User.objects.create_user(username=username,email=email)
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


class ApplicantPersonalInformationView(APIView):

    def get(self,request,*args,**kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        user_profile = user.user_profile
        serializer = ApplicantUserPersonalInformationSerializer(user_profile)
        return Response(serializer.data,status=200)

class ApplicantPersonalInformationUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = self.request.data
        try:
            user_profile = user.user_profile
        except:
            return Response(data={"messege": "UserProfile does not exist for the given user,create UserProfile first."}, status=401)
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
                return Response(data={"messege":"UserProfile for Given User Already Exist"},status=401)
        except:
            data = self.request.data
            serializer = ApplicantUserPersonalInformationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            result = serializer.save(validated_data=data)
            user_profile = UserProfile.objects.get(user__username=result)
            serializer = ApplicantUserPersonalInformationSerializer(user_profile)
            return Response(serializer.data,status=200)

class ApplicantAddressView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id = id)
        address_type = self.request.GET['address_type']
        if address_type == 'local_address':
            location = user.user_profile.local_address
        elif address_type == 'permanent_address':
            location = user.user_profile.permanent_address
        else:
            location = user.user_profile.father_address

        serializer = LocationSerializer(location)
        return Response(serializer.data,status=200)

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
            location = user.user_profile.permanent_address
            serializer = LocationSerializer(location, data=data)
        else:
            location = user.user_profile.father_address
            serializer = LocationSerializer(location, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=location, validated_data=data)
        return Response(serializer.data, status=200)

class ApplicantAddressCreateView(APIView):

    def post(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        data = self.request.data
        serializer = LocationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=data)
        location = Location.objects.get(id=result)
        address_type = self.request.GET['address_type']
        if address_type == 'local_address':
            if user.user_profile.local_address:
                Location.objects.get(id=result).delete()
                return Response(data={"messege":"Local Address for Given User Already Exist"},status=401)
            else:
                user.user_profile.local_address = location
                user.user_profile.save()
        elif address_type == 'permanent_address':
            if user.user_profile.permanent_address:
                Location.objects.get(id=result).delete()
                return Response(data={"messege":"Permanent Address for Given User Already Exist"},status=401)
            else:
                user.user_profile.permanent_address = location
                user.user_profile.save()
        else:
            if user.user_profile.father_address:
                Location.objects.get(id=result).delete()
                return Response(data={"messege":"Father Address for Given User Already Exist"},status=401)
            else:
                user.user_profile.father_address = location
                user.user_profile.save()

        serializer = LocationSerializer(location)
        return Response(serializer.data, status=200)

class ApplicantQualificationsListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if user.user_profile.education_details.filter().count() > 0:
            qualifications = user.user_profile.education_details.filter()
            serializer = UserEducationDetailsSerializer(qualifications,many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=401)

class ApplicantQualificationUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        qualifications = user.user_profile.education_details.filter()
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
        qualifications = user.user_profile.education_details.filter()
        serializer = UserEducationDetailsSerializer(qualifications,many=True)
        return Response(serializer.data, status=200)


class ApplicantExperiencesListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if user.user_profile.experiences.filter().count() > 0:
            experiences = user.user_profile.experiences.filter()
            serializer = UserExperienceDetailsSerializer(experiences, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=401)



class ApplicantExperienceUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        experiences = user.user_profile.experiences.filter()
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
        experiences = user.user_profile.experiences.filter()
        serializer = UserExperienceDetailsSerializer(experiences, many=True)
        return Response(serializer.data, status=200)

class NeeriRelationsListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if user.user_profile.neeri_relation.filter().count() > 0:
            neeri_relations = user.user_profile.neeri_relation.filter()
            serializer = NeeriRelationSerializer(neeri_relations, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=401)


class NeeriRelationUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        neeri_relations = user.user_profile.neeri_relation.filter()
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
        experiences = user.user_profile.neeri_relation.filter()
        serializer = NeeriRelationSerializer(experiences, many=True)
        return Response(serializer.data, status=200)

class OverseasVisitsListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if user.user_profile.overseas_visits.filter().count() > 0:
            visits = user.user_profile.overseas_visits.filter()
            serializer = OverseasVisitsSerializer(visits, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=401)

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
        visits = user.user_profile.overseas_visits.filter()
        serializer = OverseasVisitsSerializer(visits, many=True)
        return Response(serializer.data, status=200)

class OverseasVisitsUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        visits = user.user_profile.overseas_visits.filter()
        for visits_data in data:
            visit = user.user_profile.overseas_visits.get(id=visits_data['id'])
            serializer = OverseasVisitsSerializer(visit, data=visits_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=visit, validated_data=visits_data)
        serializer = OverseasVisitsSerializer(visits, many=True)
        return Response(serializer.data, status=200)

class ApplicantReferencesListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if user.user_profile.references.filter().count() > 0:
            references = user.user_profile.references.filter()
            serializer = ReferencesSerializer(references, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege":"No Records found"},status=401)

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
        references = user.user_profile.references.filter()
        serializer = ReferencesSerializer(references, many=True)
        return Response(serializer.data, status=200)

class ApplicantReferencesUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        references = user.user_profile.references.filter()
        for reference_data in data:
            reference = user.user_profile.references.get(id=reference_data['id'])
            serializer = ReferencesSerializer(reference, data=reference_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=reference, validated_data=reference_data)
        serializer = ReferencesSerializer(references, many=True)
        return Response(serializer.data, status=200)

class ApplicantLanguagesListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if user.user_profile.languages.filter().count() > 0:
            languages = user.user_profile.languages.filter()
            serializer = LanguagesSerializer(languages, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege":"No Records found"},status=401)

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
        languages = user.user_profile.languages.filter()
        serializer = LanguagesSerializer(languages, many=True)
        return Response(serializer.data, status=200)

class ApplicantLanguagesUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        data = self.request.data
        user = User.objects.get(user_id=id)
        languages = user.user_profile.languages.filter()
        for language_data in data:
            language = user.user_profile.languages.get(id=language_data['id'])
            serializer = LanguagesSerializer(language, data=language_data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=language, validated_data=language_data)
        serializer = LanguagesSerializer(languages, many=True)
        return Response(serializer.data, status=200)

class PublishedPapersListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if user.user_profile.published_papers.filter().count() >0:
            papers = user.user_profile.published_papers.filter()
            serializer = PublishedPapersSerializer(papers, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=401)

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
        papers = user.user_profile.published_papers.filter()
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
        papers = user.user_profile.published_papers.filter()
        response_data = PublishedPapersSerializer(papers, many=True)
        return Response(response_data.data, status=200)

class ApplicantAppliedJobListView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        if UserJobPositions.objects.filter(user=user).count() >0:
            user_job_positions = UserJobPositions.objects.filter(user=user)
            serializer = ApplicantJobPositionsSerializer(user_job_positions, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=401)

##While creating new entry of UserJobPositions set closing_date to a closing_date og JobPosting

class ApplicantProfilePercentageView(APIView):

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        user = User.objects.get(user_id=id)
        try:
            percentage = user.user_profile.profile_percentage
            return Response(data={"percentage": percentage}, status=200)
        except:
            return Response(data={"messsege": "UserProfile not found"}, status=401)
