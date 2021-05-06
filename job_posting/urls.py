from django.urls import path
from job_posting.views import DepartmentListView, DivisionListView, ZonalLabListView, \
    ProjectApprovalListView, PositionQualificationMappingListView, JobTemplateCreateView, \
    RetrieveQualificationMasterView, CreateQualificationMasterView, \
    UpdateQualificationMasterView, DeleteQualificationMasterView, \
    RetrievePositionMasterView, DeletePositionMasterView, UpdatePositionMasterView, CreatePositionMasterView, \
    QualificationMasterListView, PositionMasterListView, JobPostingCreateView, JobPostingUpdateView, \
    GetSelectionContent, GetServiceConditions, CreateProjectRequirementView, UpdateProjectRequirementView, \
    DeleteProjectRequirementView, RetrieveProjectRequirementView, ProjectRequirementListView, GetSelectionContent, \
    GetServiceConditions, \
    ApplicantListByJobPositions, JosPostingListView

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

    path('department_list/', DepartmentListView.as_view(), name="user-list"),
    path('division_list/', DivisionListView.as_view(), name="user-list"),
    path('zonal_lab_list/', ZonalLabListView.as_view(), name="user-list"),
    path('position_list/', PositionMasterListView.as_view(), name="user-list"),
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
]
