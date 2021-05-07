from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from document.models import DocumentMaster
from document.serializer import DocumentMasterSerializer

class RetrieveDocumentView(APIView):
    def get(self,request,*args,**kwargs):
        id = self.kwargs['id']
        doc = DocumentMaster.objects.get(doc_id=id)
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
        docs = DocumentMaster.objects.all()
        serializer = DocumentMasterSerializer(docs, many=True)
        return Response(serializer.data, status=200)

