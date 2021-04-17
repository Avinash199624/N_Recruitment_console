from django.db import models
import uuid
from user.models import BaseModel

class Department(BaseModel):
    dept_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dept_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.dept_name


class Division(BaseModel):
    division_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    division_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.division_name


class ZonalLab(BaseModel):
    zonal_lab_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zonal_lab_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.zonal_lab_name


class QualificationMaster(BaseModel):
    qualification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qualification_name = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.qualification_name


class PositionMaster(BaseModel):
    position_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position_name = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return self.position_name

class PositionQualificationMapping(BaseModel):

    HRA = 'hra'
    CONSOLIDATED = 'consolidated'

    ALLOWANCE_CHOICES = [
        (HRA,'HRA'),
        (CONSOLIDATED,'CONSOLIDATED'),
    ]

    position = models.ForeignKey('PositionMaster',null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="postion")
    qualification = models.ManyToManyField('QualificationMaster', blank=True, related_name="qualification")
    min_age = models.IntegerField(blank=True,null=True)
    max_age = models.IntegerField(blank=True,null=True)
    number_of_vacancies = models.IntegerField(null=True, blank=True, help_text="total number of vacancies for post")
    monthly_emolements = models.CharField(max_length=80,null=True, blank=True)
    allowance = models.CharField(max_length=30,choices=ALLOWANCE_CHOICES, null=True, blank=True)
    extra_note = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.position.position_name


class JobTemplate(BaseModel):

    '''
    This model will be same as PositionQualificationMapping, it will be useful when we need to
    use existing PositionQualificationMappings as a template. It will allow Job_Posting User to
    autopopulate job position saved as template.
    '''

    HRA = 'hra'
    CONSOLIDATED = 'consolidated'

    ALLOWANCE_CHOICES = [
        (HRA, 'HRA'),
        (CONSOLIDATED, 'CONSOLIDATED'),
    ]

    template_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_name = models.CharField(max_length=50, null=True, blank=True)
    position = models.ForeignKey('PositionMaster', null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name="job_postion")
    qualification = models.ManyToManyField('QualificationMaster', blank=True, related_name="job_qualification")
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    number_of_vacancies = models.IntegerField(null=True, blank=True, help_text="total number of vacancies for post")
    monthly_emolements = models.CharField(max_length=80, null=True, blank=True)
    allowance = models.CharField(max_length=30, choices=ALLOWANCE_CHOICES, null=True, blank=True)
    extra_note = models.TextField(null=True, blank=True)

    def __str__(self):
        return ' '.join(["Template - ",self.id])

class JobPosting(BaseModel):

    Contract_Basis = 'Contract_Basis'
    Permanent = 'Permanent'

    JOB_TYPE_CHOICES = [
        (Contract_Basis, 'contract_basis'),
        (Permanent, 'permanent'),
    ]

    DRAFT = 'draft'
    READY_TO_BE_PUBLISHED = 'ready_to_be_published'
    PUBLISHED = 'published'
    SUSPENDED = 'suspended'
    CANCELLED = 'cancelled'
    CLOSED = 'closed'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (READY_TO_BE_PUBLISHED, 'Accepted'),
        (PUBLISHED, 'Published'),
        (SUSPENDED, 'Suspended'),
        (CANCELLED, 'Other'),
        (CLOSED, 'Closed'),
    ]

    job_posting_id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False,unique=True)
    notification_id = models.CharField(max_length=100, null=True, blank=True)
    notification_title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    project_number = models.CharField(max_length=50, null=True, blank=True)
    department = models.OneToOneField('Department',on_delete=models.CASCADE,null=True,blank=True, related_name="department")
    division = models.OneToOneField('Division',on_delete=models.CASCADE,null=True,blank=True, related_name="division")
    zonal_lab = models.OneToOneField('ZonalLab',on_delete=models.CASCADE,null=True,blank=True, related_name="zonal_lab")
    publication_date = models.DateTimeField(null=True, blank=True,help_text="start date of job notification")
    end_date = models.DateTimeField(null=True, blank=True,help_text="end date of job notification")
    documents_required = models.ManyToManyField('document.DocumentMaster', blank=True,
                                                related_name="required_documents")
    status = models.CharField(null=True, blank=True, choices=STATUS_CHOICES, max_length=30)
    job_type = models.CharField(null=True, blank=True, choices=JOB_TYPE_CHOICES, max_length=30)
    manpower_positions = models.ManyToManyField('PositionQualificationMapping',blank=True,related_name="job_positions")
    # agewise_relaxation = models.IntegerField(blank=True, null=True)
    # percentwise_relaxation = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.notification_title

class UserJobPositions(BaseModel):

    RECEIVED = 'received'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    SHORTLISTED = 'shortlisted'
    OFFERED = 'offered'
    HIRED = 'hired'
    INTERVIEW = 'interview'
    AWAITING_REVIEW = 'awaiting review'
    CLOSED = 'closed'

    APPLIED_JOB_STATUS_CHOICES = [
        (RECEIVED, 'RECEIVED'),
        (ACCEPTED, 'ACCEPTED'),
        (REJECTED, 'REJECTED'),
        (SHORTLISTED, 'SHORTLISTED'),
        (OFFERED, 'OFFERED'),
        (HIRED, 'HIRED'),
        (INTERVIEW, 'INTERVIEW'),
        (AWAITING_REVIEW, 'AWAITING_REVIEW'),
        (CLOSED, 'CLOSED'),
    ]

    user = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL,related_name="user")
    job_posting = models.ForeignKey('JobPosting',null=True, blank=True, on_delete=models.SET_NULL,related_name="job_posting")
    position = models.ForeignKey('PositionQualificationMapping',null=True, blank=True, on_delete=models.SET_NULL,related_name="job_position")
    applied_job_status = models.CharField(max_length=50,choices=APPLIED_JOB_STATUS_CHOICES,blank=True,null=True)
    appealed = models.BooleanField(null=True,blank=True,default=False)
    reason_to_appeal = models.TextField(blank=True,null=True)
    date_of_application = models.DateField(auto_now_add=True)
    date_of_closing = models.DateField(blank=True,null=True,help_text='Closing date of JobPosting')

    def __str__(self):
        return self.user.email