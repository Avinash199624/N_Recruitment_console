from job_posting.models import UserJobPositions, QualificationMaster, PositionMaster
from rest_framework import serializers
from job_posting.models import UserJobPositions,Department,Division,ZonalLab,QualificationMaster,\
    PositionMaster,PositionQualificationMapping,JobPostingRequirement,JobTemplate,JobDocuments,\
    JobPosting,SelectionProcessContent,SelectionCommitteeMaster,ServiceConditions
from document.serializer import DocumentMasterSerializer
from document.models import DocumentMaster

class ApplicantJobPositionsSerializer(serializers.ModelSerializer):

    notification_id = serializers.SerializerMethodField(
        method_name="get_notification_id", read_only=True
    )

    description = serializers.SerializerMethodField(
        method_name="get_description", read_only=True
    )

    date_of_application = serializers.SerializerMethodField(
        method_name="get_date_of_application", read_only=True
    )

    date_of_closing = serializers.SerializerMethodField(
        method_name="get_date_of_closing", read_only=True
    )

    hiring_status = serializers.SerializerMethodField(
        method_name="get_hiring_status", read_only=True
    )

    class Meta:
        model = UserJobPositions
        fields = (
            "id",
            "notification_id",
            "description",
            "date_of_application",
            "date_of_closing",
            "hiring_status",
        )

    def get_notification_id(self,obj):
        notification_id = obj.job_posting.notification_id
        return notification_id

    def get_description(self,obj):
        description = obj.position.position.position_name
        return description

    def get_date_of_application(self,obj):
        date_of_application = obj.date_of_application
        return date_of_application

    def get_date_of_closing(self,obj):
        date_of_closing = obj.date_of_closing
        return date_of_closing

    def get_hiring_status(self,obj):
        hiring_status = obj.applied_job_status
        return hiring_status

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = (
            "dept_id",
            "dept_name",
        )

class DivisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Division
        fields = (
            "division_id",
            "division_name",
        )

class ZonalLabSerializer(serializers.ModelSerializer):

    class Meta:
        model = ZonalLab
        fields = (
            "zonal_lab_id",
            "zonal_lab_name",
        )

class QualificationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualificationMaster
        fields = (
            "qualification_id",
            "qualification",
            "short_code",
        )


class PositionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionMaster
        fields = (
            "position_id",
            "position_name",
            "position_desc",
            "salary",
        )

class PositionQualificationMappingSerializer(serializers.ModelSerializer):

    position = serializers.SerializerMethodField(
        method_name="get_position", read_only=True
    )

    qualification = QualificationMasterSerializer(many=True)

    class Meta:
        model = PositionQualificationMapping
        fields = (
            "id",
            "position",
            "qualification",
            "min_age",
            "max_age",
            "number_of_vacancies",
            "monthly_emolements",
            "allowance",
            "extra_note",
        )

    def get_position(self,obj):
        return obj.position.position_name


class ProjectApprovalListSerializer(serializers.ModelSerializer):

    project_number = serializers.SerializerMethodField(
        method_name="get_project_number", read_only=True
    )

    class Meta:
        model = JobPostingRequirement
        fields = (
            "project_number",
        )

    def get_project_number(self,obj):
        return obj.project_number


class JobTemplateSerializer(serializers.ModelSerializer):

    position = serializers.SerializerMethodField(
        method_name="get_position", read_only=True
    )

    qualification = serializers.SerializerMethodField(
        method_name="get_qualification", read_only=True
    )

    class Meta:
        model = JobTemplate
        fields = (
            "template_name",
            "position",
            "qualification",
            "min_age",
            "max_age",
            "number_of_vacancies",
            "monthly_emolements",
            "allowance",
            "extra_note",
        )

    def get_position(self, obj):
        serializer = PositionMasterSerializer(obj.position)
        return serializer.data

    def get_qualification(self, obj):
        qualifications = obj.qualification.filter()
        serializer = QualificationMasterSerializer(qualifications,many=True)
        return serializer.data

    def save(self, validated_data):

        template = JobTemplate.objects.create(
            template_name = validated_data['template_name'],
            min_age = validated_data['min_age'],
            max_age = validated_data['max_age'],
            number_of_vacancies = validated_data['number_of_vacancies'],
            monthly_emolements = validated_data['monthly_emolements'],
            allowance = validated_data['allowance'],
            extra_note = validated_data['extra_note'],
        )

        position = PositionMaster.objects.get(position_id=validated_data['position']['position_id'])
        template.position = position
        template.save()

        for qualification_data in validated_data['qualification']:
            qualification = QualificationMaster.objects.get(qualification_id = qualification_data['qualification_id'])
            template.qualification.add(qualification)

class JobDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobDocuments
        fields = (
            "doc_id",
            "doc_file_path",
            "doc_name",
        )

class JobPostingSerializer(serializers.ModelSerializer):

    manpower_positions = serializers.SerializerMethodField(
        method_name='get_manpower_positions',required=False
    )

    department = serializers.SerializerMethodField(
        method_name='get_department',required=False
    )

    division = serializers.SerializerMethodField(
        method_name='get_division',required=False
    )

    zonal_lab = serializers.SerializerMethodField(
        method_name='get_zonal_lab',required=False
    )
    office_memorandum = serializers.SerializerMethodField(
        method_name='get_office_memorandum',required=False
    )

    documents_required = serializers.SerializerMethodField(
        method_name='get_documents_required',required=False
    )

    documents_uploaded = serializers.SerializerMethodField(
        method_name='get_documents_uploaded',required=False
    )

    project_number = serializers.SerializerMethodField(
        method_name='get_project_number',required=False
    )

    class Meta:
        model = JobPosting
        fields = (
            "job_posting_id",
            "notification_id",
            "notification_title",
            "description",
            "project_number",
            "department",
            "division",
            "zonal_lab",
            "publication_date",
            "end_date",
            "documents_required",
            "documents_uploaded",
            "office_memorandum",
            "status",
            "job_type",
            "manpower_positions",
        )

    def get_division(self,obj):
        division = obj.division
        serializer = DivisionSerializer(division)
        return serializer.data

    def get_department(self,obj):
        department = obj.department
        serializer = DepartmentSerializer(department)
        return serializer.data

    def get_zonal_lab(self,obj):
        zonal_lab = obj.zonal_lab
        serializer = ZonalLabSerializer(zonal_lab)
        return serializer.data

    def get_project_number(self,obj):
        return obj.project_number.project_number

    def get_manpower_positions(self,obj):
        positions = obj.manpower_positions.filter()
        serializer = PositionQualificationMappingSerializer(positions,many=True)
        return serializer.data

    def get_documents_required(self,obj):
        documents_required = obj.documents_required.filter()
        serializer = DocumentMasterSerializer(documents_required,many=True)
        return serializer.data

    def get_documents_uploaded(self,obj):
        documents_uploaded = obj.documents_uploaded.filter()
        serializer = JobDocumentsSerializer(documents_uploaded,many=True)
        return serializer.data

    def get_office_memorandum(self,obj):
        office_memorandum = obj.office_memorandum
        serializer = JobDocumentsSerializer(office_memorandum)
        return serializer.data

    def update(self, instance, validated_data):

        instance.notification_id = (
            validated_data["notification_id"] if validated_data["notification_id"] else instance.notification_id
        )

        instance.notification_title = (
            validated_data["notification_title"] if validated_data["notification_title"] else instance.notification_title
        )

        instance.description = (
            validated_data["description"] if validated_data["description"] else instance.description
        )

        instance.publication_date = (
            validated_data["publication_date"] if validated_data["publication_date"] else instance.publication_date
        )

        instance.end_date = (
            validated_data["end_date"] if validated_data["end_date"] else instance.end_date
        )

        instance.status = (
            validated_data["status"] if validated_data["status"] else instance.status
        )

        instance.job_type = (
            validated_data["job_type"] if validated_data["job_type"] else instance.job_type
        )

        department = Department.objects.get(dept_id=validated_data['department']['dept_id'])
        division = Division.objects.get(division_id=validated_data['division']['division_id'])
        zonal_lab = ZonalLab.objects.get(zonal_lab_id=validated_data['zonal_lab']['zonal_lab_id'])
        project_number = JobPostingRequirement.objects.get(project_number__icontains=validated_data['project_number'])

        if instance.department == department:
            pass
        else:
            instance.department = department

        if instance.division == division:
            pass
        else:
            instance.division = division

        if instance.zonal_lab == zonal_lab:
            pass
        else:
            instance.zonal_lab = zonal_lab

        if instance.project_number == project_number:
            pass
        else:
            instance.project_number = project_number

        instance.save()

        return instance.job_posting_id

    def save(self, validated_data):

        posting = JobPosting.objects.create(
            notification_id = validated_data['notification_id'],
            notification_title = validated_data['notification_title'],
            description = validated_data['description'],
            publication_date = validated_data['publication_date'],
            end_date = validated_data['end_date'],
            status = validated_data['status'],
            job_type = validated_data['job_type'],
        )

        for position_qualification_mapping_data in validated_data['manpower_positions']:
            position_qualification_mapping = PositionQualificationMapping.objects.get(id=position_qualification_mapping_data['id'])
            posting.manpower_positions.add(position_qualification_mapping)

        for documents_required_data in validated_data['documents_required']:
            document_required = DocumentMaster.objects.get(doc_id=documents_required_data['doc_id'])
            posting.documents_required.add(document_required)

        project_number = JobPostingRequirement.objects.get(id=validated_data['project_number'])
        department = Department.objects.get(dept_id=validated_data['department']['dept_id'])
        division = Division.objects.get(division_id=validated_data['division']['division_id'])
        zonal_lab = ZonalLab.objects.get(zonal_lab_id=validated_data['zonal_lab']['zonal_lab_id'])

        posting.project_number = project_number
        posting.department = department
        posting.division = division
        posting.zonal_lab = zonal_lab
        posting.save()

        return posting.job_posting_id

class SelectionCommitteeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelectionCommitteeMaster
        fields = (
            "committee_id",
            "committee_name",
        )


class SelectionProcessContentSerializer(serializers.ModelSerializer):

    selection_committee = serializers.SerializerMethodField(
        method_name='get_selection_committee',required=False
    )

    class Meta:
        model = SelectionProcessContent
        fields = (
            "description",
            "selection_committee",
        )

    def get_selection_committee(self,obj):
        selection_committee = obj.selection_committee
        serializer = SelectionCommitteeSerializer(selection_committee,many=True)
        return serializer.data

class ServiceConditionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceConditions
        fields = (
            "id",
            "title",
            "descriprtion",
        )