import sha
import random
import datetime
from django.core.mail import send_mail
from django.conf import settings
import os
import datetime


us_states = ["Alabama",
             "Alaska",
             "Arizona",
             "Arkansas",
             "California",
             "Coloroda",
             "Connecticut",
             "Delaware",
             "Florida",
             "Georgia",
             "Hawaii",
             "idaho",
             "Illinois",
             "Indiana",
             "Lowa",
             "Kansas",
             "Kentucky",
             "Louisiana",
             "Maine",
             "Maryland",
             "Massachusetts",
             "Michigan",
             "Minnesota",
             "Mississippi",
             "Missouri",
             "Montana",
             "Nebraska",
             "Nevada",
             "New Hampshire",
             "New Jersey",
             "New Mexico",
             "New York",
             "North Carolina",
             "North Dakota",
             "Ohio",
             "Oklahoma",
             "Oregon",
             "Pennsylvania",
             "Rhode Island",
             "South Carolina",
             "South Dakota",
             "Tennessee",
             "Texas",
             "Utah",
             "Vermont",
             "Virginia",
             "Washington",
             "West Virginia",
             "Wisconsin",
             "Wyoming"]




def delete_uploaded_file(file_name):
    try:
        os.remove(settings.UPLOAD_PATH + file_name)
    except:
        pass
    return


def send_activation_email(email, key):
    email_subject = 'Activate your account'
    email_body = 'Account activation Link %(site_url)s/activate/%(activation_key)s' % {"site_url": settings.SITE_URL, "activation_key": key}
    send_mail(email_subject,
              email_body,
              settings.ADMIN_EMAIL,
              [email],
              fail_silently=False)


def send_password_reset_email(email, key):
    email_subject = 'Password reset'
    email_body = 'Password Reset Link %(site_url)s/password/reset/form/%(activation_key)s' % {"site_url": settings.SITE_URL, "activation_key": key}
    send_mail(email_subject,
              email_body,
              settings.ADMIN_EMAIL,
              [email],
              fail_silently=False)


def send_contact_email(contact_name, contact_email, contact_inquiry):
    email_subject = 'Fratography - Inquiry - ' + contact_email
    email_body = contact_inquiry
    send_mail(email_subject,
              email_body,
              contact_email,
              [settings.ADMIN_EMAIL],
              fail_silently=False
          )

def create_key(mixer, expiry):
    salt = sha.new(str(random.random())).hexdigest()[:10]
    key = sha.new(salt + mixer).hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    return {"key": key, "expiry": key_expires}


def unique_name(mixer):
    salt = sha.new(str(random.random())).hexdigest()[:10]
    key = sha.new(salt + mixer).hexdigest()
    return key


def reply_object():
    """
    reference for the reply json object
    """
    reply_object = {"code": ""}
    return reply_object


def paginate(page, per_page):
    if page:
        page = int(page)
    else:
        page = 1
    pages = {"from": 0, "to": 0}
    pages["from"] = page * per_page - per_page
    pages["to"] = page * per_page
    return pages


def calculate_points(votes, created_date):
    gravity = 3.6
    naive_date = created_date.replace(tzinfo=None)
    time_elapsed = datetime.datetime.now() - naive_date
    semester = time_elapsed.total_seconds() / 3600 / 24 / 180
    points = (votes - 1) / pow((semester + 2), gravity)
    return points
