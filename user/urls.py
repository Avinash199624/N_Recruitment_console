from django.contrib import admin
from django.urls import path
from user.views import UserRegistartionView
from user.views import LoginView,LogoutView,UserListView,RetrievetUserView,UpdateUserView,CreateUserView,DeleteUserView,ForgotPassword,\
    ApplicantPersonalInformationView,ApplicantPersonalInformationUpdateView,\
    ApplicantPersonalInformationCreateView,ApplicantAddressView,ApplicantAddressCreateView,\
    ApplicantAddressUpdateView,ApplicantQualificationsListView,ApplicantQualificationCreateView,\
    ApplicantQualificationUpdateView,ApplicantExperiencesListView,ApplicantExperienceCreateView,\
    ApplicantExperienceUpdateView,NeeriRelationsListView,NeeriRelationCreateView,NeeriRelationUpdateView,\
    ApplicantLanguagesListView,ApplicantLanguagesCreateView,ApplicantLanguagesUpdateView,\
    ApplicantReferencesListView,ApplicantReferencesCreateView,ApplicantReferencesUpdateView,\
    OverseasVisitsListView,OverseasVisitsCreateView,OverseasVisitsUpdateView,PublishedPapersListView,\
    PublishedPapersCreateView,PublishedPapersUpdateView,ApplicantAppliedJobListView,\
    ApplicantProfilePercentageView,ProfessionalTrainingListView,ProfessionalTrainingCreateView,\
    ProfessionalTrainingUpdateView,ProfessionalTrainingDeleteView,ApplicantExperienceDeleteView,\
    ApplicantLanguagesDeleteView,ApplicantQualificationDeleteView,ApplicantReferencesDeleteView,NeeriRelationDeleteView,\
    OverseasVisitsDeleteView,PublishedPapersDeleteView

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

    path('public/applicant_qualifications/<uuid:id>/', ApplicantQualificationsListView.as_view(), name="get-applicant-qualifications"),
    path('public/applicant_qualification_create/<uuid:id>/', ApplicantQualificationCreateView.as_view(), name="create-applicant-qualification"),
    path('public/applicant_qualification_update/<uuid:id>/', ApplicantQualificationUpdateView.as_view(), name="update-applicant-qualification"),
    path('public/applicant_qualification_delete/<uuid:id>/', ApplicantQualificationDeleteView.as_view(), name="delete-applicant-qualification"),

    path('public/applicant_experiences/<uuid:id>/', ApplicantExperiencesListView.as_view(), name="get-applicant-experience"),
    path('public/applicant_experience_create/<uuid:id>/', ApplicantExperienceCreateView.as_view(), name="create-applicant-experience"),
    path('public/applicant_experience_update/<uuid:id>/', ApplicantExperienceUpdateView.as_view(), name="update-applicant-experience"),
    path('public/applicant_experience_delete/<uuid:id>/', ApplicantExperienceDeleteView.as_view(), name="delete-applicant-experience"),

    path('public/neeri_relations/<uuid:id>/', NeeriRelationsListView.as_view(), name="get-neeri-relations"),
    path('public/neeri_relation_create/<uuid:id>/', NeeriRelationCreateView.as_view(), name="create-neeri-relation"),
    path('public/neeri_relation_update/<uuid:id>/', NeeriRelationUpdateView.as_view(), name="update-neeri-relation"),
    path('public/neeri_relation_delete/<uuid:id>/', NeeriRelationDeleteView.as_view(), name="delete-neeri-relation"),

    path('public/published_papers/<uuid:id>/', PublishedPapersListView.as_view(), name="get-applicant-papers"),
    path('public/published_paper_create/<uuid:id>/', PublishedPapersCreateView.as_view(), name="create-neeri-relation"),
    path('public/published_paper_update/<uuid:id>/', PublishedPapersUpdateView.as_view(), name="update-neeri-relation"),
    path('public/published_paper_delete/<uuid:id>/', PublishedPapersDeleteView.as_view(), name="delete-neeri-relation"),

    path('public/overseas_visits/<uuid:id>/', OverseasVisitsListView.as_view(), name="get-overseas-visits"),
    path('public/overseas_visit_create/<uuid:id>/', OverseasVisitsCreateView.as_view(), name="create-overseas-visit"),
    path('public/overseas_visit_update/<uuid:id>/', OverseasVisitsUpdateView.as_view(), name="update-overseas-visit"),
    path('public/overseas_visit_delete/<uuid:id>/', OverseasVisitsDeleteView.as_view(), name="delete-overseas-visit"),

    path('public/applicant_references/<uuid:id>/', ApplicantReferencesListView.as_view(), name="get-applicant-references"),
    path('public/applicant_reference_create/<uuid:id>/', ApplicantReferencesCreateView.as_view(), name="create-applicant-references"),
    path('public/applicant_reference_update/<uuid:id>/', ApplicantReferencesUpdateView.as_view(), name="update-applicant-references"),
    path('public/applicant_reference_delete/<uuid:id>/', ApplicantReferencesDeleteView.as_view(), name="delete-applicant-references"),

    path('public/applicant_languages/<uuid:id>/', ApplicantLanguagesListView.as_view(), name="get-applicant-languages"),
    path('public/applicant_language_create/<uuid:id>/', ApplicantLanguagesCreateView.as_view(), name="create-applicant-language"),
    path('public/applicant_language_update/<uuid:id>/', ApplicantLanguagesUpdateView.as_view(), name="update-applicant-language"),
    path('public/applicant_language_delete/<uuid:id>/', ApplicantLanguagesDeleteView.as_view(), name="delete-applicant-language"),

    path('public/applicant_job_list/<uuid:id>/', ApplicantAppliedJobListView.as_view(), name="applicant-applied-job-list"),
    path('public/applicant_profile_percentage/<uuid:id>/', ApplicantProfilePercentageView.as_view(), name="applicant-profile-percentage"),

    path('public/professional_trainings/<uuid:id>/', ProfessionalTrainingListView.as_view(), name="get-professional-trainings"),
    path('public/professional_training_create/<uuid:id>/', ProfessionalTrainingCreateView.as_view(), name="create-professional-training"),
    path('public/professional_training_update/<uuid:id>/', ProfessionalTrainingUpdateView.as_view(), name="update-professional-training"),
    path('public/professional_training_delete/<uuid:id>/', ProfessionalTrainingDeleteView.as_view(), name="update-professional-training"),
]