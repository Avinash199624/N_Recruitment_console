from django.urls import path
from job_posting.views import (
    DepartmentListView,
    DivisionListView,
    ZonalLabListView,
    ProjectApprovalListView,
    PositionQualificationMappingListView,
    JobTemplateCreateView,
    RetrieveQualificationMasterView,
    CreateQualificationMasterView,
    UpdateQualificationMasterView,
    DeleteQualificationMasterView,
    QualificationMasterListView,
    JobPostingCreateView,
    JobPostingDetailView,
    CreateProjectRequirementView,
    UpdateProjectRequirementView,
    DeleteProjectRequirementView,
    RetrieveProjectRequirementView,
    ProjectRequirementListView,
    GetSelectionContent,
    GetServiceConditions,
    ApplicantListByJobPositions,
    JobPostingListView,
    UserAppealForJobPositions,
    AppealReasonMasterViews,
    NewPositionMasterViews,
    PermanentPositionMasterViews,
    TemporaryPositionMasterViews,
    ProjectApprovalStatusListView,
    QualificationJobHistoryMasterView,
    PublicJobPostingView,
    ApplicantJobPositions,
    QualificationMasterSearchListView,
    QualificationJobHistoryMasterSearchListView,
    ProjectApprovalFilterListView,
    ProjectApprovalSearchListView,
    TemporaryPositionMasterSearchListView,
    TemporaryPositionMasterFilterListView,
    PermanentPositionMasterFilterListView,
    PermanentPositionMasterSearchListView,
    JobPostingSearchListView,
    JobPostingFilterListView,
    PublicJobPostingFilterListView,
    PublicJobPostingSearchListView,
    ApproveRejectApplicantView,
    ApplicationCountByJobPositions, RejectionReasonViews, RejectApplicantsView,
)

urlpatterns = [
    #     QualificationMaster
    path(
        "search_qualification/",
        QualificationMasterSearchListView.as_view(),
        name="search-qualification-list",
    ),
    path(
        "get_qualification/<uuid:id>/",
        RetrieveQualificationMasterView.as_view(),
        name="get-qualification",
    ),
    path(
        "delete_qualification/<uuid:id>/",
        DeleteQualificationMasterView.as_view(),
        name="delete-qualification",
    ),
    path(
        "update_qualification/<uuid:id>/",
        UpdateQualificationMasterView.as_view(),
        name="update-qualification",
    ),
    path(
        "create_qualification/",
        CreateQualificationMasterView.as_view(),
        name="create-qualification",
    ),
    path(
        "qualification_list/",
        QualificationMasterListView.as_view(),
        name="qualification-list",
    ),
    #     QualificationJobHistoryMaster
    path(
        "search_qualification_job_history/",
        QualificationJobHistoryMasterSearchListView.as_view(),
        name="search-qualification-job-history-list",
    ),
    path(
        "qualification_job_history/",
        QualificationJobHistoryMasterView.as_view(),
        name="qualification-job-history",
    ),
    path(
        "qualification_job_history/<uuid:id>/",
        QualificationJobHistoryMasterView.as_view(),
        name="qualification-list",
    ),
    #     manPowerPositionMaster
    path("department_list/", DepartmentListView.as_view(), name="department-list"),
    path("division_list_and_create/", DivisionListView.as_view(), name="division-list"),
    path("division/<uuid:id>/", DivisionListView.as_view(), name="crud-division"),
    path(
        "zonal_lab_list_and_create/", ZonalLabListView.as_view(), name="zonal-lab-list"
    ),
    path("zonal_lab/<uuid:id>/", ZonalLabListView.as_view(), name="crud-zonal-lab"),
    path(
        "qualification_list/", QualificationMasterListView.as_view(), name="user-list"
    ),
    path(
        "project_approval_list/",
        ProjectApprovalListView.as_view(),
        name="project-approval-list",
    ),
    path(
        "project_approval_status/<int:id>/",
        ProjectApprovalStatusListView.as_view(),
        name="project-approval-status",
    ),
    path(
        "create_project_requirement/",
        CreateProjectRequirementView.as_view(),
        name="create-project-requirement",
    ),
    path(
        "update_project_requirement/<int:id>/",
        UpdateProjectRequirementView.as_view(),
        name="update-project-requirement",
    ),
    path(
        "delete_project_requirement/<int:id>/",
        DeleteProjectRequirementView.as_view(),
        name="delete-project-requirement",
    ),
    path(
        "get_project_requirement/<int:id>/",
        RetrieveProjectRequirementView.as_view(),
        name="get-project-requirement",
    ),
    path(
        "project_requirements_list/",
        ProjectRequirementListView.as_view(),
        name="project-requirement-list",
    ),
    path(
        "filter_project_requirements_list/",
        ProjectApprovalFilterListView.as_view(),
        name="filter-project-requirement-list",
    ),
    path(
        "search_project_requirements_list/",
        ProjectApprovalSearchListView.as_view(),
        name="search-project-requirement-list",
    ),
    path(
        "position_qualification_mapping_list/",
        PositionQualificationMappingListView.as_view(),
        name="position-qualification-mapping-list",
    ),
    path("save_template/", JobTemplateCreateView.as_view(), name="save-as-template"),
    path(
        "selection_process_content/",
        GetSelectionContent.as_view(),
        name="get-selection-content",
    ),
    path(
        "service_conditions/",
        GetServiceConditions.as_view(),
        name="get-service-conditions",
    ),
    path(
        "job_posting_create/", JobPostingCreateView.as_view(), name="job-posting-create"
    ),
    path(
        "detail/<uuid:id>/",
        JobPostingDetailView.as_view(),
        name="job-posting-detail",
    ),
    path(
        "filter_job_posting_list/",
        JobPostingFilterListView.as_view(),
        name="filter-job-posting-list",
    ),
    path(
        "search_job_posting_list/",
        JobPostingSearchListView.as_view(),
        name="search-job-posting-list",
    ),
    path("job_posting_list/", JobPostingListView.as_view(), name="job-posting-list"),
    path(
        "search_job_posting_list/applicant/",
        PublicJobPostingSearchListView.as_view(),
        name="search-applicant-job-posting-list",
    ),
    path(
        "filter_job_posting_list/applicant/",
        PublicJobPostingFilterListView.as_view(),
        name="filter-applicant-job-posting-list",
    ),
    path(
        "job_posting_list/applicant/",
        PublicJobPostingView.as_view(),
        name="applicant-job-posting-list",
    ),
    path(
        "applicant/<uuid:id>/",
        ApplicantJobPositions.as_view(),
        name="applicant-job-posting-positions",
    ),
    path(
        "applicant_status/<int:id>/",
        ApproveRejectApplicantView.as_view(),
        name="approve-reject-applicant-for-job",
    ),
    path(
        "applicant_list_by_job/",
        ApplicantListByJobPositions.as_view(),
        name="jobwise-applicant-list",
    ),
    path(
        "application_count/<uuid:id>/",
        ApplicationCountByJobPositions.as_view(),
        name="jobwise-application-count",
    ),
    path(
        "applicant_list_by_job/<uuid:id>/",
        ApplicantListByJobPositions.as_view(),
        name="jobwise-applicant-by-job",
    ),
    path(
        "update_user_appeal_for_job_position/<int:id>/",
        UserAppealForJobPositions.as_view(),
        name="user-appeal-for-job",
    ),
    path(
        "appeal_reason_master/",
        AppealReasonMasterViews.as_view(),
        name="appeal-master-list-and-create",
    ),
    path(
        "appeal_reason_master/<uuid:id>/",
        AppealReasonMasterViews.as_view(),
        name="appeal-reason-master",
    ),
    path("positions/", NewPositionMasterViews.as_view(), name="positions-master"),
    path("positions/<uuid:id>/", NewPositionMasterViews.as_view(), name="positions"),
    path(
        "filter_permanent_positions/",
        PermanentPositionMasterFilterListView.as_view(),
        name="filter-p-positions-master",
    ),
    path(
        "search_permanent_positions/",
        PermanentPositionMasterSearchListView.as_view(),
        name="search-p-positions-master",
    ),
    path(
        "permanent_positions/",
        PermanentPositionMasterViews.as_view(),
        name="p-positions-master",
    ),
    path(
        "permanent_positions/<uuid:id>/",
        PermanentPositionMasterViews.as_view(),
        name="p-positions",
    ),
    path(
        "filter_temporary_positions/",
        TemporaryPositionMasterFilterListView.as_view(),
        name="filter-t-positions-master",
    ),
    path(
        "search_temporary_positions/",
        TemporaryPositionMasterSearchListView.as_view(),
        name="search-t-positions-master",
    ),
    path(
        "temporary_positions/",
        TemporaryPositionMasterViews.as_view(),
        name="t-positions-master",
    ),
    path(
        "temporary_positions/<uuid:id>/",
        TemporaryPositionMasterViews.as_view(),
        name="t-positions",
    ),
    path(
        "rejection_reason/",
        RejectionReasonViews.as_view(),
        name="rejection-reason-list-and-create",
    ),
    path(
        "rejection_reason/<uuid:id>/",
        RejectionReasonViews.as_view(),
        name="rejection-reason-master",
    ),
    path(
        "reject/applicants/",
        RejectApplicantsView.as_view(),
        name="reject-applicants",
    ),
]
