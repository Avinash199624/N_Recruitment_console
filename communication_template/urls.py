from django.contrib import admin
from django.urls import path
from communication_template.views import RetrievetTemplateView,DeleteTemplateView,UpdateTemplateView,CreateTemplateView,TemplateListView

urlpatterns = [
    path('get-template/<uuid:id>/', RetrievetTemplateView.as_view(), name="get-template"),
    path('delete-template/<uuid:id>', DeleteTemplateView.as_view(), name="delete-template"),
    path('update-template/<uuid:id>', UpdateTemplateView.as_view(), name="update-template"),
    path('create-template/', CreateTemplateView.as_view(), name="create-template"),
    path('template-list/', TemplateListView.as_view(), name="template-list"),
]
