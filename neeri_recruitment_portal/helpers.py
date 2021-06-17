import http.client
from django.core.mail import send_mail
from neeri_recruitment_portal import settings
from neeri_recruitment_portal.settings import BASE_URL


def send_otp(mobile, otp):
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
    subject = 'Welcome to NEERI - Verify your Email.'
    message = f'Hi, please click on the link to verify your account ' + BASE_URL + f'/user/email_token_verify/{email_token}/'
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



def send_forget_password_mail(email , token ):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password ' + BASE_URL + f'/user/reset_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
