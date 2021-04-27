from rest_framework.views import APIView
from rest_framework.response import Response
from job_posting.models import Department,Division,ZonalLab,QualificationMaster,PositionMaster,\
    PositionQualificationMapping,JobPostingRequirement,JobTemplate,JobPosting
from job_posting.serializer import DepartmentSerializer,DivisionSerializer,ZonalLabSerializer,\
    PositionMasterSerializer,QualificationMasterSerializer,ProjectApprovalListSerializer,\
    PositionQualificationMappingSerializer,JobTemplateSerializer,JobPostingSerializer

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


class RetrieveQualificationMasterView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        qual = QualificationMaster.objects.get(qualification_id=id, is_deleted=False)
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
        docs = QualificationMaster.objects.filter(is_deleted=False)
        serializer = QualificationMasterSerializer(docs, many=True)
        return Response(serializer.data, status=200)


# PositionMaster
class RetrievePositionMasterView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        position = PositionMaster.objects.get(position_id=id, is_deleted=False)
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
        docs = PositionMaster.objects.filter(is_deleted=False)
        serializer = PositionMasterSerializer(docs, many=True)
        return Response(serializer.data, status=200)


class DepartmentListView(APIView):

    def get(self, request, *args, **kwargs):
        if Department.objects.filter().count() >0:
            departments = Department.objects.filter()
            serializer = DepartmentSerializer(departments,many=True)
            return Response(serializer.data,status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=404)

class DivisionListView(APIView):

    def get(self, request, *args, **kwargs):
        if Division.objects.filter().count() > 0:
            divisions = Division.objects.filter()
            serializer = DivisionSerializer(divisions,many=True)
            return Response(serializer.data,status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=404)

class ZonalLabListView(APIView):

    def get(self, request, *args, **kwargs):
        if ZonalLab.objects.filter().count() > 0:
            labs = ZonalLab.objects.filter()
            serializer = ZonalLabSerializer(labs,many=True)
            return Response(serializer.data,status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=404)
class ProjectApprovalListView(APIView):

    def get(self, request, *args, **kwargs):
        projects = JobPostingRequirement.objects.filter()
        serializer = ProjectApprovalListSerializer(projects,many=True)
        return Response(serializer.data,status=200)

class PositionQualificationMappingListView(APIView):

    def get(self, request, *args, **kwargs):
        projects = PositionQualificationMapping.objects.filter()
        serializer = PositionQualificationMappingSerializer(projects,many=True)
        return Response(serializer.data,status=200)

class JobTemplateCreateView(APIView):

    def post(self, request, *args, **kwargs):
        data = self.request.data
        for template_data in data:
            serializer = JobTemplateSerializer(data=template_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(validated_data=template_data)
        return Response(data={"messege": "Template Saved Successfully"}, status=200)
