from django.contrib import admin
from django.urls import path
from document.views import RetrieveDocumentView,CreateDocumentView,UpdateDocumentView,DocumentListView,DeleteDocumentView

urlpatterns = [
path('get-doc/<uuid:id>/', RetrieveDocumentView.as_view(), name="get-doc"),
    path('delete-doc/<uuid:id>', DeleteDocumentView.as_view(), name="delete-doc"),
    path('update-doc/<uuid:id>', UpdateDocumentView.as_view(), name="update-doc"),
    path('create-doc/', CreateDocumentView.as_view(), name="create-doc"),
    path('doc-list/', DocumentListView.as_view(), name="doc-list"),
]
