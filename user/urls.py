from django.urls import path
from user.views import (
    UserRegistrationView,
    NeeriPersonalInformation,
    CompareApplicantListView,
    NeeriLoginView,
    RoleMasterView,
    CreateNeeriUserView,
    MentorMasterListView,
    NeeriUserListView,
    TraineeListView,
    RelaxationCategoryMasterListView,
    RelaxationMasterListView,
    TraineeSearchListView,
    NeeriUserSearchListView,
    ApplicantIsFresherUpdateView,
    UserDocumentView,
    ApplicantIsAddressUpdateView,
    verify_email,
    verify_sms,
    ChangePassword,
    ApplicantLockedStatusView,
    ApplicantSuspendStatusView,
    MobileOTP,
    ChangeMobileNumber,
    UpdateMobileOTP,
    ManageApplicantListView,
    ApplicantAppliedJobDetailView,
    JobApplyCheckoutView,
    ApplicationDocumentUpdateView,
    DownloadApplicantsView, ApplicantFellowShipsListView, ApplicantFellowShipsCreateView,
    ApplicantFellowShipsUpdateView, ApplicantFellowShipsDeleteView,
)
from user.views import (
    LoginView,
    LogoutView,
    UserListView,
    RetrieveUserView,
    UpdateUserView,
    CreateUserView,
    DeleteUserView,
    ForgotPassword,
    ApplicantPersonalInformationView,
    ApplicantPersonalInformationUpdateView,
    ApplicantPersonalInformationCreateView,
    ApplicantAddressView,
    ApplicantAddressCreateView,
    ApplicantAddressUpdateView,
    ApplicantQualificationsListView,
    ApplicantQualificationCreateView,
    ApplicantQualificationUpdateView,
    ApplicantExperiencesListView,
    ApplicantExperienceCreateView,
    ApplicantExperienceUpdateView,
    NeeriRelationsListView,
    NeeriRelationCreateView,
    NeeriRelationUpdateView,
    ApplicantLanguagesListView,
    ApplicantLanguagesCreateView,
    ApplicantLanguagesUpdateView,
    ApplicantReferencesListView,
    ApplicantReferencesCreateView,
    ApplicantReferencesUpdateView,
    OverseasVisitsListView,
    OverseasVisitsCreateView,
    OverseasVisitsUpdateView,
    PublishedPapersListView,
    PublishedPapersCreateView,
    PublishedPapersUpdateView,
    ApplicantAppliedJobListView,
    ApplicantProfilePercentageView,
    ProfessionalTrainingListView,
    ProfessionalTrainingCreateView,
    ProfessionalTrainingUpdateView,
    ProfessionalTrainingDeleteView,
    ApplicantExperienceDeleteView,
    ApplicantLanguagesDeleteView,
    ApplicantQualificationDeleteView,
    ApplicantReferencesDeleteView,
    NeeriRelationDeleteView,
    OverseasVisitsDeleteView,
    PublishedPapersDeleteView,
    FileUpload,
    ProfileDetailView,
    OtherInformationDetailView,
    OtherInformationCreateView,
    OtherInformationUpdateView,
    OtherInformationDeleteView,
    ApplicantListView,
    ResetPassword,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("neeri_login/", NeeriLoginView.as_view(), name="neeri-login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", UserRegistrationView.as_view(), name="signup"),
    path(
        "email_token_verify/<user_email_token>/",
        verify_email,
        name="email-token-verification",
    ),
    # path("sms_token_verify/<user_mobile_otp>/", verify_sms, name="sms-token-verification"),
    path(
        "sms_token_verify/<int:id>/", MobileOTP.as_view(), name="sms-token-verification"
    ),
    path(
        "sms_otp_verify/<int:id>/",
        UpdateMobileOTP.as_view(),
        name="sms-otp-verification",
    ),
    path("get-user/<uuid:id>/", RetrieveUserView.as_view(), name="get-user"),
    path("delete-user/<uuid:id>/", DeleteUserView.as_view(), name="delete-user"),
    path("update-user/<uuid:id>/", UpdateUserView.as_view(), name="update-user"),
    path("create-user/", CreateUserView.as_view(), name="create-user"),
    path("create_neeri_user/", CreateNeeriUserView.as_view(), name="create-neeri-user"),
    path(
        "search_neeri_user/",
        NeeriUserSearchListView.as_view(),
        name="search-neeri-user",
    ),
    path("neeri_user/", NeeriUserListView.as_view(), name="neeri-user"),
    path("neeri_user/<uuid:id>/", CreateNeeriUserView.as_view(), name="neeri-user-api"),
    path("user-list/", UserListView.as_view(), name="user-list"),
    path("forgot_password/", ForgotPassword.as_view(), name="forgot-password"),
    path(
        "reset_password/<uuid:token>/", ResetPassword.as_view(), name="reset-password"
    ),
    path(
        "change_password/<uuid:id>/", ChangePassword.as_view(), name="change-password"
    ),
    path(
        "change_mobile_number/<uuid:id>/",
        ChangeMobileNumber.as_view(),
        name="change-number",
    ),
    path(
        "manage_applicants/",
        ManageApplicantListView.as_view(),
        name="manage-applicants-list",
    ),
    path(
        "manage_applicants/<uuid:id>/",
        ManageApplicantListView.as_view(),
        name="delete-manage-applicants",
    ),
    path(
        "applicant_suspend/<uuid:id>/",
        ApplicantSuspendStatusView.as_view(),
        name="get-applicant-status-suspend",
    ),
    path(
        "applicant_locked/<uuid:id>/",
        ApplicantLockedStatusView.as_view(),
        name="get-applicant-status-locked",
    ),
    #### Public Portal User URL's
    path(
        "public/personal_info/<uuid:id>/",
        ApplicantPersonalInformationView.as_view(),
        name="get-applicant-personal-info",
    ),
    path(
        "public/personal_info/",
        ApplicantPersonalInformationView.as_view(),
        name="get-applicant-list",
    ),
    path(
        "public/applicant_is_fresher/<uuid:id>/",
        ApplicantIsFresherUpdateView.as_view(),
        name="update-applicant-is-fresher-detail",
    ),
    path(
        "public/applicant_is_address_same/<uuid:id>/",
        ApplicantIsAddressUpdateView.as_view(),
        name="update-applicant-is-address-same",
    ),
    path(
        "public/personal_info_update/<uuid:id>/",
        ApplicantPersonalInformationUpdateView.as_view(),
        name="update-applicant-personal-info",
    ),
    path(
        "public/personal_info_create/<uuid:id>/",
        ApplicantPersonalInformationCreateView.as_view(),
        name="create-applicant-personal-info",
    ),
    path(
        "public/neeri_user_personal_info/",
        NeeriPersonalInformation.as_view(),
        name="list-neeri-user-personal-info",
    ),
    path(
        "public/neeri_user_personal_info/<uuid:id>/",
        NeeriPersonalInformation.as_view(),
        name="neeri-user-personal-info",
    ),
    path(
        "public/applicant_address/<uuid:id>/",
        ApplicantAddressView.as_view(),
        name="get-applicant-address",
    ),
    path(
        "public/applicant_address_create/<uuid:id>/",
        ApplicantAddressCreateView.as_view(),
        name="create-applicant-address",
    ),
    path(
        "public/applicant_address_update/<uuid:id>/",
        ApplicantAddressUpdateView.as_view(),
        name="update-applicant-address",
    ),
    path(
        "public/applicant_qualifications/<uuid:id>/",
        ApplicantQualificationsListView.as_view(),
        name="get-applicant-qualifications",
    ),
    path(
        "public/applicant_qualification_create/<uuid:id>/",
        ApplicantQualificationCreateView.as_view(),
        name="create-applicant-qualification",
    ),
    path(
        "public/applicant_qualification_update/<uuid:id>/",
        ApplicantQualificationUpdateView.as_view(),
        name="update-applicant-qualification",
    ),
    path(
        "public/applicant_qualification_delete/<uuid:id>/",
        ApplicantQualificationDeleteView.as_view(),
        name="delete-applicant-qualification",
    ),
    path(
        "public/applicant_experiences/<uuid:id>/",
        ApplicantExperiencesListView.as_view(),
        name="get-applicant-experience",
    ),
    path(
        "public/applicant_experience_create/<uuid:id>/",
        ApplicantExperienceCreateView.as_view(),
        name="create-applicant-experience",
    ),
    path(
        "public/applicant_experience_update/<uuid:id>/",
        ApplicantExperienceUpdateView.as_view(),
        name="update-applicant-experience",
    ),
    path(
        "public/applicant_experience_delete/<uuid:id>/",
        ApplicantExperienceDeleteView.as_view(),
        name="delete-applicant-experience",
    ),
    path(
        "public/neeri_relations/<uuid:id>/",
        NeeriRelationsListView.as_view(),
        name="get-neeri-relations",
    ),
    path(
        "public/neeri_relation_create/<uuid:id>/",
        NeeriRelationCreateView.as_view(),
        name="create-neeri-relation",
    ),
    path(
        "public/neeri_relation_update/<uuid:id>/",
        NeeriRelationUpdateView.as_view(),
        name="update-neeri-relation",
    ),
    path(
        "public/neeri_relation_delete/<uuid:id>/",
        NeeriRelationDeleteView.as_view(),
        name="delete-neeri-relation",
    ),
    path(
        "public/published_papers/<uuid:id>/",
        PublishedPapersListView.as_view(),
        name="get-applicant-papers",
    ),
    path(
        "public/published_paper_create/<uuid:id>/",
        PublishedPapersCreateView.as_view(),
        name="create-neeri-relation",
    ),
    path(
        "public/published_paper_update/<uuid:id>/",
        PublishedPapersUpdateView.as_view(),
        name="update-neeri-relation",
    ),
    path(
        "public/published_paper_delete/<uuid:id>/",
        PublishedPapersDeleteView.as_view(),
        name="delete-neeri-relation",
    ),
    path(
        "public/overseas_visits/<uuid:id>/",
        OverseasVisitsListView.as_view(),
        name="get-overseas-visits",
    ),
    path(
        "public/overseas_visit_create/<uuid:id>/",
        OverseasVisitsCreateView.as_view(),
        name="create-overseas-visit",
    ),
    path(
        "public/overseas_visit_update/<uuid:id>/",
        OverseasVisitsUpdateView.as_view(),
        name="update-overseas-visit",
    ),
    path(
        "public/overseas_visit_delete/<uuid:id>/",
        OverseasVisitsDeleteView.as_view(),
        name="delete-overseas-visit",
    ),
    path(
        "public/applicant_references/<uuid:id>/",
        ApplicantReferencesListView.as_view(),
        name="get-applicant-references",
    ),
    path(
        "public/applicant_reference_create/<uuid:id>/",
        ApplicantReferencesCreateView.as_view(),
        name="create-applicant-references",
    ),
    path(
        "public/applicant_reference_update/<uuid:id>/",
        ApplicantReferencesUpdateView.as_view(),
        name="update-applicant-references",
    ),
    path(
        "public/applicant_reference_delete/<uuid:id>/",
        ApplicantReferencesDeleteView.as_view(),
        name="delete-applicant-references",
    ),
    path(
        "public/applicant_languages/<uuid:id>/",
        ApplicantLanguagesListView.as_view(),
        name="get-applicant-languages",
    ),
    path(
        "public/applicant_language_create/<uuid:id>/",
        ApplicantLanguagesCreateView.as_view(),
        name="create-applicant-language",
    ),
    path(
        "public/applicant_language_update/<uuid:id>/",
        ApplicantLanguagesUpdateView.as_view(),
        name="update-applicant-language",
    ),
    path(
        "public/applicant_language_delete/<uuid:id>/",
        ApplicantLanguagesDeleteView.as_view(),
        name="delete-applicant-language",
    ),
    path(
        "public/applicant_job_list/<uuid:id>/",
        ApplicantAppliedJobListView.as_view(),
        name="applicant-applied-job-list",
    ),
    path(
        "public/applicant_job/detail/<int:id>/",
        ApplicantAppliedJobDetailView.as_view(),
        name="applicant-applied-job-detail",
    ),
    path(
        "apply/<uuid:id>/",
        JobApplyCheckoutView.as_view(),
        name="job-apply",
    ),
    path(
        "applications/documents/",
        ApplicationDocumentUpdateView.as_view(),
        name="application-doc-update",
    ),
    path(
        "public/applicant_profile_percentage/<uuid:id>/",
        ApplicantProfilePercentageView.as_view(),
        name="applicant-profile-percentage",
    ),
    path(
        "public/professional_trainings/<uuid:id>/",
        ProfessionalTrainingListView.as_view(),
        name="get-professional-trainings",
    ),
    path(
        "public/professional_training_create/<uuid:id>/",
        ProfessionalTrainingCreateView.as_view(),
        name="create-professional-training",
    ),
    path(
        "public/professional_training_update/<uuid:id>/",
        ProfessionalTrainingUpdateView.as_view(),
        name="update-professional-training",
    ),
    path(
        "public/professional_training_delete/<uuid:id>/",
        ProfessionalTrainingDeleteView.as_view(),
        name="update-professional-training",
    ),
    path(
        "public/other_info/<uuid:id>/",
        OtherInformationDetailView.as_view(),
        name="get-other-info",
    ),
    path(
        "public/other_info_create/<uuid:id>/",
        OtherInformationCreateView.as_view(),
        name="create-other-info",
    ),
    path(
        "public/other_info_update/<uuid:id>/",
        OtherInformationUpdateView.as_view(),
        name="update-other-info",
    ),
    path(
        "public/other_info_delete/<uuid:id>/",
        OtherInformationDeleteView.as_view(),
        name="update-other-info",
    ),
    path(
        "public/documents/<uuid:id>/", UserDocumentView.as_view(), name="user-documents"
    ),
    path(
        "public/profile_details/<uuid:id>/",
        ProfileDetailView.as_view(),
        name="user-profile-details",
    ),
    path("public/applicant_list/", ApplicantListView.as_view(), name="applicant-list"),
    path("public/file_upload/", FileUpload.as_view(), name="file_upload"),
    path(
        "public/compare_applicants_for_job/",
        CompareApplicantListView.as_view(),
        name="compare-applicants-for-job",
    ),
    path(
        "download/applicants/",
        DownloadApplicantsView.as_view(),
        name="download-applicants",
    ),
    path("public/role_master/", RoleMasterView.as_view(), name="role-master-list"),
    path("mentor/", MentorMasterListView.as_view(), name="mentor-list"),
    path("mentor/<uuid:id>/", MentorMasterListView.as_view(), name="mentor"),
    path("trainee/", TraineeListView.as_view(), name="trainee-list"),
    path(
        "filter_trainee/", TraineeSearchListView.as_view(), name="filter-trainee-list"
    ),
    path("trainee/<uuid:id>/", TraineeListView.as_view(), name="trainee"),
    path(
        "relaxation_category/",
        RelaxationCategoryMasterListView.as_view(),
        name="relaxation-category",
    ),
    path(
        "relaxation_category/<uuid:id>/",
        RelaxationCategoryMasterListView.as_view(),
        name="relaxation-category",
    ),
    path("relaxation/", RelaxationMasterListView.as_view(), name="relaxation-list"),
    path(
        "relaxation/<uuid:id>/", RelaxationMasterListView.as_view(), name="relaxation"
    ),

    path(
        "public/applicant_fellow_ships/<uuid:id>/",
        ApplicantFellowShipsListView.as_view(),
        name="applicant-fellow-ships",
    ),
    path(
        "public/applicant_fellow_ships_create/<uuid:id>/",
        ApplicantFellowShipsCreateView.as_view(),
        name="applicant-fellow-ships-create",
    ),
    path(
        "public/applicant_fellow_ships_update/<uuid:id>/",
        ApplicantFellowShipsUpdateView.as_view(),
        name="applicant-fellow-ships-update",
    ),
    path(
        "public/applicant_fellow_ships_delete/<uuid:id>/",
        ApplicantFellowShipsDeleteView.as_view(),
        name="applicant-fellow-ships-delete",
    ),
]
