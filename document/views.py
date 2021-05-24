from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from document.models import DocumentMaster, NewDocumentMaster, InformationMaster
from document.serializer import DocumentMasterSerializer, NewDocumentMasterSerializer, InformationMasterSerializer

class RetrieveDocumentView(APIView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['id']
        doc = DocumentMaster.objects.get(doc_id=id, is_deleted=False)
        serializer = DocumentMasterSerializer(doc)
        return Response(serializer.data,status=200)

class DeleteDocumentView(APIView):
    def delete(self,request,*args,**kwargs):
        try:
            id = self.kwargs['id']
            doc = DocumentMaster.objects.get(doc_id=id)
            doc.is_deleted = True
            doc.save()
            return Response(data = {"messege":"Document Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"messege": "User Not Found."}, status=401)

class UpdateDocumentView(APIView):
    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        doc = DocumentMaster.objects.get(doc_id=id)
        data = self.request.data
        serializer = DocumentMasterSerializer(doc, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=doc, validated_data=data)
        return Response(serializer.data, status=200)

class CreateDocumentView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = DocumentMasterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

class DocumentListView(APIView):
    def get(self,request,*args,**kwargs):
        docs = DocumentMaster.objects.filter(is_deleted=False)
        serializer = DocumentMasterSerializer(docs, many=True)
        return Response(serializer.data, status=200)


# New Docs serializer
class NewDocumentListView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            doc = NewDocumentMaster.objects.get(doc_id=id, is_deleted=False)
            serializer = NewDocumentMasterSerializer(doc)
            return Response(serializer.data, status=200)
        except:
            docs = NewDocumentMaster.objects.filter(is_deleted=False)
            serializer = NewDocumentMasterSerializer(docs, many=True)
            return Response(serializer.data, status=200)

    def delete(self,request,*args,**kwargs):
        try:
            id = self.kwargs['id']
            doc = NewDocumentMaster.objects.get(doc_id=id)
            doc.is_deleted = True
            doc.save()
            return Response(data = {"messege":"Document Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"messege": "User Not Found."}, status=401)

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        doc = NewDocumentMaster.objects.get(doc_id=id)
        data = self.request.data
        serializer = NewDocumentMasterSerializer(doc, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=doc, validated_data=data)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = NewDocumentMasterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class InformationListView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            info = InformationMaster.objects.get(info_id=id, is_deleted=False)
            serializer = InformationMasterSerializer(info)
            return Response(serializer.data, status=200)
        except:
            info = InformationMaster.objects.filter(is_deleted=False)
            serializer = InformationMasterSerializer(info, many=True)
            return Response(serializer.data, status=200)

    def delete(self,request,*args,**kwargs):
        try:
            id = self.kwargs['id']
            info = InformationMaster.objects.get(info_id=id)
            info.is_deleted = True
            info.save()
            return Response(data = {"message": "info Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"message": "info Not Found."}, status=401)

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        info = InformationMaster.objects.get(info_id=id)
        data = self.request.data
        serializer = InformationMasterSerializer(info, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=info, validated_data=data)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = InformationMasterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

