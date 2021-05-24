from django.contrib import admin
from django.urls import path
from document.views import RetrieveDocumentView, CreateDocumentView, UpdateDocumentView, DocumentListView, \
    DeleteDocumentView, NewDocumentListView, InformationListView

urlpatterns = [
    path('get_doc/<uuid:id>/', RetrieveDocumentView.as_view(), name="get-doc"),
    path('delete_doc/<uuid:id>/', DeleteDocumentView.as_view(), name="delete-doc"),
    path('update_doc/<uuid:id>/', UpdateDocumentView.as_view(), name="update-doc"),
    path('create_doc/', CreateDocumentView.as_view(), name="create-doc"),
    path('doc_list/', DocumentListView.as_view(), name="doc-list"),

    # new docs
    path('docs/', NewDocumentListView.as_view(), name="docs-list"),
    path('docs/<uuid:id>/', NewDocumentListView.as_view(), name="docs"),

    # new docs
    path('info/', InformationListView.as_view(), name="docs-list"),
    path('info/<uuid:id>/', InformationListView.as_view(), name="docs"),

]
