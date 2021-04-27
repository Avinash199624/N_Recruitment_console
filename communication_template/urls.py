from django.contrib import admin
from django.urls import path
from communication_template.views import RetrievetCommunicationTemplateView,DeleteCommunicationTemplateView,UpdateCommunicationTemplateView,CreateCommunicationTemplateView,CommunicationTemplateListView

urlpatterns = [
    path('get_template/<uuid:id>/', RetrievetCommunicationTemplateView.as_view(), name="get-template"),
    path('delete_template/<uuid:id>/', DeleteCommunicationTemplateView.as_view(), name="delete-template"),
    path('update_template/<uuid:id>/', UpdateCommunicationTemplateView.as_view(), name="update-template"),
    path('create_template/', CreateCommunicationTemplateView.as_view(), name="create-template"),
    path('template_list/', CommunicationTemplateListView.as_view(), name="template-list"),
]
