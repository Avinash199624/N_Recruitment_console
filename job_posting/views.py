from rest_framework.views import APIView
from rest_framework.response import Response
from job_posting.models import Department,Division,ZonalLab,QualificationMaster,PositionMaster,\
    PositionQualificationMapping,JobPostingRequirement,JobTemplate,JobPosting,SelectionProcessContent,\
    ServiceConditions,UserJobPositions
from job_posting.serializer import DepartmentSerializer, DivisionSerializer, ZonalLabSerializer, \
    PositionMasterSerializer, QualificationMasterSerializer, ProjectApprovalListSerializer, \
    PositionQualificationMappingSerializer, JobTemplateSerializer, JobPostingSerializer, \
    SelectionProcessContentSerializer, \
    ServiceConditionsSerializer, UserJobPositionsSerializer, ProjectRequirementSerializer

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
        if Department.objects.filter(is_deleted=False).count() >0:
            departments = Department.objects.filter(is_deleted=False)
            serializer = DepartmentSerializer(departments,many=True)
            return Response(serializer.data,status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=404)

class DivisionListView(APIView):

    def get(self, request, *args, **kwargs):
        if Division.objects.filter(is_deleted=False).count() > 0:
            divisions = Division.objects.filter(is_deleted=False)
            serializer = DivisionSerializer(divisions,many=True)
            return Response(serializer.data,status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=404)

class ZonalLabListView(APIView):

    def get(self, request, *args, **kwargs):
        if ZonalLab.objects.filter(is_deleted=False).count() > 0:
            labs = ZonalLab.objects.filter(is_deleted=False)
            serializer = ZonalLabSerializer(labs,many=True)
            return Response(serializer.data,status=200)
        else:
            return Response(data={"messege": "No Records found"}, status=404)
			
class ProjectApprovalListView(APIView):

    def get(self, request, *args, **kwargs):
        req = JobPostingRequirement.objects.filter(is_deleted=False)
        serializer = ProjectApprovalListSerializer(req, many=True)
        return Response(serializer.data, status=200)

# project Requirement

class UpdateProjectRequirementView(APIView):
    def put(self, request, *args, **kwargs):
        data = self.request.data
        id = self.kwargs['id']
        project = JobPostingRequirement.objects.get(id=id, is_deleted=False)
        serializer = ProjectRequirementSerializer(project, data=data)
        serializer.is_valid(raise_exception=True)
        result = serializer.update(instance=project, validated_data=data)
        project = JobPostingRequirement.objects.get(id=result)
        serializer = ProjectRequirementSerializer(project)
        return Response(serializer.data, status=200)


class CreateProjectRequirementView(APIView):
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = ProjectRequirementSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=data)
        job_posting = JobPostingRequirement.objects.get(id=result)
        serializer = ProjectRequirementSerializer(job_posting)
        return Response(serializer.data, status=200)


class DeleteProjectRequirementView(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            id = self.kwargs['id']
            project = JobPostingRequirement.objects.get(id=id)
            project.is_deleted = True
            project.save()
            return Response(data={"message": "Record Deleted Successfully(Soft Delete)."}, status=200)
        except:
            return Response(data={"message": "Details Not Found."}, status=401)



class ProjectRequirementListView(APIView):

    def get(self, request, *args, **kwargs):
        job = JobPostingRequirement.objects.filter(is_deleted=False)
        serializer = ProjectRequirementSerializer(job, many=True)
        return Response(serializer.data, status=200)

class RetrieveProjectRequirementView(APIView):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        job = JobPostingRequirement.objects.get(id=id, is_deleted=False)
        serializer = ProjectRequirementSerializer(job)
        return Response(serializer.data, status=200)


class PositionQualificationMappingListView(APIView):

    def get(self, request, *args, **kwargs):
        projects = PositionQualificationMapping.objects.filter(is_deleted=False)
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

class JobPostingCreateView(APIView):

    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = JobPostingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=data)
        job_posting = JobPosting.objects.get(job_posting_id = result)
        serializer = JobPostingSerializer(job_posting)
        return Response(serializer.data,status=200)

class JobPostingUpdateView(APIView):

    def put(self, request, *args, **kwargs):
        data = self.request.data
        job_posting_id = self.kwargs['id']
        job_posting = JobPosting.objects.get(job_posting_id = job_posting_id)
        serializer = JobPostingSerializer(job_posting,data=data)
        serializer.is_valid(raise_exception=True)
        result = serializer.update(job_posting,validated_data=data)
        job_posting = JobPosting.objects.get(job_posting_id = result)
        serializer = JobPostingSerializer(job_posting)
        return Response(serializer.data,status=200)

class GetSelectionContent(APIView):

    def get(self, request, *args, **kwargs):
        # position_name_list = []
        #Todo: #Imagine you will get list of selected positions(Position_names) for the job
        # queryset = SelectionProcessContent.objects.none()
        # for i in position_name_list:
        #     if SelectionProcessContent.objects.filter(description__icontains=i):
        #         queryset |= SelectionProcessContent.objects.filter(description__icontains=i)
        #
        # serializer = SelectionProcessContentSerializer(queryset,many=True)

        # For now sending all records
        process_content = SelectionProcessContent.objects.filter(is_deleted=False)
        serializer = SelectionProcessContentSerializer(process_content, many=True)
        return Response(serializer.data,status=200)


class GetServiceConditions(APIView):

    def get(self, request, *args, **kwargs):
        conditions = ServiceConditions.objects.filter(is_deleted=False)
        serializer = ServiceConditionsSerializer(conditions,many=True)
        return Response(serializer.data,status=200)

class JosPostingListView(APIView):

    def get(self, request, *args, **kwargs):
        postings = JobPosting.objects.filter(is_deleted=False)
        serializer = JobPostingSerializer(postings, many=True)
        return Response(serializer.data, status=200)

class ApplicantListByJobPositions(APIView):

    def get(self, request, *args, **kwargs):
        try:
            job_posting_id = self.kwargs['id']
            applicants = UserJobPositions.objects.filter(job_posting__job_posting_id=job_posting_id, is_deleted=False)
            serializer = UserJobPositionsSerializer(applicants, many=True)
            return Response(serializer.data, status=200)
        except:
            applicants = UserJobPositions.objects.filter(is_deleted=False)
            serializer = UserJobPositionsSerializer(applicants, many=True)
            return Response(serializer.data, status=200)
