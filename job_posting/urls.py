from django.contrib import admin
from django.urls import path
from job_posting.views import RetrieveQualificationMasterView, CreateQualificationMasterView, \
    UpdateQualificationMasterView, DeleteQualificationMasterView, \
    RetrievePositionMasterView, DeletePositionMasterView, UpdatePositionMasterView, CreatePositionMasterView

urlpatterns = [
    #     QualificationMaster
    path('get_qualification/<uuid:id>/', RetrieveQualificationMasterView.as_view(), name="get-qualification"),
    path('delete_qualification/<uuid:id>/', DeleteQualificationMasterView.as_view(), name="delete-qualification"),
    path('update_qualification/<uuid:id>/', UpdateQualificationMasterView.as_view(), name="update-qualification"),
    path('create_qualification/', CreateQualificationMasterView.as_view(), name="create-qualification"),
    # path('qualification-list/', QualificationMasterListView.as_view(), name="qualification-list"),

    #     manPowerPositionMaster
    path('get_position/<uuid:id>/', RetrievePositionMasterView.as_view(), name="get-position"),
    path('delete_position/<uuid:id>/', DeletePositionMasterView.as_view(), name="delete-position"),
    path('update_position/<uuid:id>/', UpdatePositionMasterView.as_view(), name="update-position"),
    path('create_position/', CreatePositionMasterView.as_view(), name="create-position"),

]
