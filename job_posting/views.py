from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from job_posting.models import QualificationMaster, PositionMaster
from job_posting.serializer import QualificationMasterSerializer, PositionMasterSerializer


class RetrieveQualificationMasterView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        qual = QualificationMaster.objects.get(qualification_id=id)
        serializer = QualificationMasterSerializer(qual)
        return Response(serializer.data, status=200)


class DeleteQualificationMasterView(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            qualification = QualificationMaster.objects.get(qualification_id=id)
            qualification.is_deleted = True
            qualification.save()
            return Response(data={"message": "Record Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)


class UpdateQualificationMasterView(APIView):
    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        qualification = QualificationMaster.objects.get(qualification_id=id)
        data = self.request.data
        serializer = QualificationMasterSerializer(qualification, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=qualification, validated_data=data)
        return Response(serializer.data, status=200)


class CreateQualificationMasterView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = QualificationMasterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class QualificationMasterListView(APIView):
    def get(self, request, *args, **kwargs):
        docs = QualificationMaster.objects.all()
        serializer = QualificationMasterSerializer(docs, many=True)
        return Response(serializer.data, status=200)


# PositionMaster
class RetrievePositionMasterView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        position = PositionMaster.objects.get(position_id=id)
        serializer = PositionMasterSerializer(position)
        return Response(serializer.data, status=200)


class DeletePositionMasterView(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            position = PositionMaster.objects.get(position_id=id)
            position.is_deleted = True
            position.save()
            return Response(data={"message": "Record Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)


class UpdatePositionMasterView(APIView):
    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        position = PositionMaster.objects.get(position_id=id)
        data = self.request.data
        serializer = PositionMasterSerializer(position, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=position, validated_data=data)
        return Response(serializer.data, status=200)


class CreatePositionMasterView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = PositionMasterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class PositionMasterListView(APIView):
    def get(self, request, *args, **kwargs):
        docs = PositionMaster.objects.all()
        serializer = PositionMasterSerializer(docs, many=True)
        return Response(serializer.data, status=200)

