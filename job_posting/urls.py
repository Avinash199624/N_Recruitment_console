from django.urls import path
from job_posting.views import DepartmentListView,DivisionListView,ZonalLabListView,\
    ProjectApprovalListView,PositionQualificationMappingListView,JobTemplateCreateView,\
    RetrieveQualificationMasterView, CreateQualificationMasterView, \
    UpdateQualificationMasterView, DeleteQualificationMasterView, \
    RetrievePositionMasterView, DeletePositionMasterView, UpdatePositionMasterView, CreatePositionMasterView, \
    QualificationMasterListView, PositionMasterListView

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
    path('position_qualification_mapping_list/', PositionQualificationMappingListView.as_view(),
         name="position-qualification-mapping-list"),
    path('save_template/', JobTemplateCreateView.as_view(), name="save-as-template"),
]
