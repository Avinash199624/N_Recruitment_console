from django.urls import path
from job_posting.views import DepartmentListView, DivisionListView, ZonalLabListView, \
    ProjectApprovalListView, PositionQualificationMappingListView, JobTemplateCreateView, \
    RetrieveQualificationMasterView, CreateQualificationMasterView, \
    UpdateQualificationMasterView, DeleteQualificationMasterView, \
    RetrievePositionMasterView, DeletePositionMasterView, UpdatePositionMasterView, CreatePositionMasterView, \
    QualificationMasterListView, PositionMasterListView, JobPostingCreateView, JobPostingUpdateView, \
    CreateProjectRequirementView, UpdateProjectRequirementView, \
    DeleteProjectRequirementView, RetrieveProjectRequirementView, ProjectRequirementListView, GetSelectionContent, \
    GetServiceConditions, \
    GetServiceConditions, \
    ApplicantListByJobPositions, JosPostingListView, UserAppealForJobPositions, AppealReasonMasterViews, \
    NewPositionMasterViews, PermanentPositionMasterViews, TemporaryPositionMasterViews

urlpatterns = [
    #     QualificationMaster
    path('get_qualification/<uuid:id>/', RetrieveQualificationMasterView.as_view(), name="get-qualification"),
    path('delete_qualification/<uuid:id>/', DeleteQualificationMasterView.as_view(), name="delete-qualification"),
    path('update_qualification/<uuid:id>/', UpdateQualificationMasterView.as_view(), name="update-qualification"),
    path('create_qualification/', CreateQualificationMasterView.as_view(), name="create-qualification"),
    path('qualification_list/', QualificationMasterListView.as_view(), name="qualification-list"),

    #     manPowerPositionMaster
    path('get_position/<uuid:id>/', RetrievePositionMasterView.as_view(), name="get-position"),
    path('delete_position/<uuid:id>/', DeletePositionMasterView.as_view(), name="delete-position"),
    path('update_position/<uuid:id>/', UpdatePositionMasterView.as_view(), name="update-position"),
    path('create_position/', CreatePositionMasterView.as_view(), name="create-position"),
    path('position_list/', PositionMasterListView.as_view(), name="position-list"),

    path('department_list/', DepartmentListView.as_view(), name="department-list"),
    path('division_list_and_create/', DivisionListView.as_view(), name="division-list"),
    path('division/<uuid:id>/', DivisionListView.as_view(), name="crud-division"),
    path('zonal_lab_list_and_create/', ZonalLabListView.as_view(), name="zonal-lab-list"),
    path('zonal_lab/<uuid:id>/', ZonalLabListView.as_view(), name="crud-zonal-lab"),
    path('position_list/', PositionMasterListView.as_view(), name="position-list"),
    path('qualification_list/', QualificationMasterListView.as_view(), name="user-list"),
    path('project_approval_list/', ProjectApprovalListView.as_view(), name="project-approval-list"),
    path('create_project_requirement/', CreateProjectRequirementView.as_view(), name="create-project-requirement"),
    path('update_project_requirement/<int:id>/', UpdateProjectRequirementView.as_view(), name="update-project-requirement"),
    path('delete_project_requirement/<int:id>/', DeleteProjectRequirementView.as_view(), name="delete-project-requirement"),
    path('get_project_requirement/<int:id>/', RetrieveProjectRequirementView.as_view(), name="get-project-requirement"),
    path('project_requirements_list/', ProjectRequirementListView.as_view(), name="project-requirement-list"),
    path('position_qualification_mapping_list/', PositionQualificationMappingListView.as_view(),
         name="position-qualification-mapping-list"),
    path('save_template/', JobTemplateCreateView.as_view(), name="save-as-template"),
    path('selection_process_content/', GetSelectionContent.as_view(), name="get-selection-content"),
    path('service_conditions/', GetServiceConditions.as_view(), name="get-service-conditions"),
    path('job_posting_create/', JobPostingCreateView.as_view(), name="job-posting-create"),
    path('job_posting_update/<uuid:id>/', JobPostingUpdateView.as_view(), name="job-posting-update"),
    path('job_posting_list/', JosPostingListView.as_view(), name="job-posting-list"),
    path('applicant_list_by_job/', ApplicantListByJobPositions.as_view(), name="jobwise-applicant-list"),
    path('applicant_list_by_job/<uuid:id>/', ApplicantListByJobPositions.as_view(), name="jobwise-applicant-by-job"),
    path('update_user_appeal_for_job_position/<str:id>/', UserAppealForJobPositions.as_view(), name="user-appeal-for-job"),
    path('appeal_reason_master/', AppealReasonMasterViews.as_view(), name="appeal-master-list-and-create"),
    path('appeal_reason_master/<uuid:id>/', AppealReasonMasterViews.as_view(), name="appeal-reason-master"),
    path('positions/', NewPositionMasterViews.as_view(), name="positions-master"),
    path('positions/<uuid:id>/', NewPositionMasterViews.as_view(), name="positions"),
    path('permanent_positions/', PermanentPositionMasterViews.as_view(), name="positions-master"),
    path('permanent_positions/<uuid:id>/', PermanentPositionMasterViews.as_view(), name="positions"),
    path('temporary_positions/', TemporaryPositionMasterViews.as_view(), name="positions-master"),
    path('temporary_positions/<uuid:id>/', TemporaryPositionMasterViews.as_view(), name="positions"),
]
