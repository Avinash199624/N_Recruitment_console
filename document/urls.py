from django.contrib import admin
from django.urls import path
from document.views import RetrievetDocumentView,CreateDocumentView,UpdateDocumentView,DocumentListView,DeleteDocumentView

urlpatterns = [
path('get-doc/<uuid:id>/', RetrievetDocumentView.as_view(), name="get-user"),
    path('delete-doc/<uuid:id>', DeleteDocumentView.as_view(), name="delete-user"),
    path('update-doc/<uuid:id>', UpdateDocumentView.as_view(), name="update-user"),
    path('create-doc/', CreateDocumentView.as_view(), name="create-user"),
    path('doc-list/', DocumentListView.as_view(), name="user-list"),
]
