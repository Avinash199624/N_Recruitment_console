import http.client
from django.core.mail import send_mail
from rest_framework import request

from communication_template.models import CommunicationMaster
from job_posting.models import JobPosting
from neeri_recruitment_portal import settings
from neeri_recruitment_portal.settings import BASE_URL, BASE_QA_URL


def send_otp(mobile, otp):  # /verify_mobile/
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    senderid = "NEERIC"
    print("senderid---->", senderid)

    route = settings.ROUTE
    countrycode = settings.COUNTRY_CODE
    headers = {'content-type': "application/json"}
    # url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    url = "/api/v2/sendsms?authkey="+authkey+"&mobiles="+mobile+"&message=Your OTP for Verification is "+ otp +"&sender="+senderid+"&route="+route+"&country="+countrycode+""
    print("url---->", url)
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    print("OTP sent")
    return None


def send_verification_mail(email, email_token):
    template = CommunicationMaster.objects.filter(comm_type__communication_type='EMAIL',
                                                  action_type__comm_action_type='VERIFY EMAIL', is_active=True).first()
    subject = template.subject
    message = template.body + "\n" + BASE_QA_URL + f'/verify_email/{email_token}/\n\n' \
                                                   f'Regards,\nNEERI Recruitment Team'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False
    )
    print("email sent")
    return None


def send_update_jobpost_mail(email, user_name, job_posting):

    """Send mail to job-pist editable-user and management role users """
    template = CommunicationMaster.objects.filter(comm_type__communication_type='EMAIL',
                                                  action_type__comm_action_type='UPDATED JOBPOST', is_active=True).first()
    subject = template.subject
    job_post = JobPosting.objects.get(job_posting_id=job_posting.job_posting_id)
    if job_post:
        notification_id = job_posting.notification_id
        notification_title = job_posting.notification_title
        publication_date = job_posting.publication_date
        end_date = job_posting.end_date
        job_type = job_posting.job_type
    message = "Dear "+str(user_name)+"\n"+"\n"+template.body +"\n"+"\n"+"Notification ID : "+str(notification_id)+"\n"+"Notification Title : "+str(notification_title)+"\n"+"Notification Type : "+str(job_type)+"\n"+"Start Date : "+str(publication_date)+"\n"+"End Date : "+str(end_date)+"\n"+"\n"\
                                                                                +"\n"+"You can also view the updated job post using link below :"+"\n"+"\n"+BASE_QA_URL + f'/update_jobpost/{job_post}/\n\n'+f'Kindly Regards,\nNEERI Recruitment Team'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = email
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False
    )
    print("email sent")
    return None



def send_forget_password_mail(email , token ):
    template = CommunicationMaster.objects.filter(comm_type__communication_type='EMAIL',
                                                  action_type__comm_action_type='FORGOT PASSWORD', is_active=True).first()
    subject = template.subject
    message = template.body+" " + BASE_QA_URL + f'/reset_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_password_mail(email, password):
    template = CommunicationMaster.objects.filter(comm_type__communication_type='EMAIL',
                                                  action_type__comm_action_type='CHANGE PASSWORD',
                                                  is_active=True).first()
    subject = template.subject
    message = template.body + f' {password}.\n' + BASE_QA_URL + f'/admin/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False
    )
    print("email sent")
    return None
