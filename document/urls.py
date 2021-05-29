from django.contrib import admin
from django.urls import path
from document.views import NewDocumentListView, InformationListView

urlpatterns = [

    # new docs
    path('docs/', NewDocumentListView.as_view(), name="docs-list"),
    path('docs/<uuid:id>/', NewDocumentListView.as_view(), name="docs"),

    # new docs
    path('info/', InformationListView.as_view(), name="docs-list"),
    path('info/<uuid:id>/', InformationListView.as_view(), name="docs"),

]
