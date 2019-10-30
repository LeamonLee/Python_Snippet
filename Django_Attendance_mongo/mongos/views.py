from django.shortcuts import render, HttpResponse

import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .models import Contact

from django.core.mail import send_mail
from .tasks import task_mail

from .models import DictEntry


# Create your views here.

@permission_required("admin.can_add_log_entry")
def Contact_upload(request):

    template = "mongos/contact_upload.html"

    prompt = {
        "order": "Order of the csv should be first_name, last_name, email, ip_address, message"
    }

    if request.method == "GET":
        return render(request, template, prompt)


    csv_file = request.FILES["file"]        # The name "file" must be the same as the one defined in template html. In this case, it's "file"

    if not csv_file.name.endswith(".csv"):
        messages.error(request, "This is not a csv file")

    data_set = csv_file.read().decode("UTF-8")

    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar='|'):
        _, create = Contact.objects.update_or_create(
            first_name = column[0],
            last_name = column[1],
            email = column[2],
            ip_address = column[3],
            message = column[4]
        )
    
    messages.success(request, "You uploaded csv file and saved datas to the database successfully!")

    context = {}
    return render(request, template, context)

@permission_required("admin.can_add_log_entry")
def contact_download(request):
    items = Contact.objects.all()
    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = "attachment; filename='contact.csv'"

    writer = csv.writer(response, delimiter=',')
    writer.writerow(["first_name", "last_name", "email", "ip_address", "message"])

    for obj in items:
        writer.writerow([obj.first_name, obj.last_name, obj.email, obj.ip_address, obj.message])

    return response


# ========= ListField & DictField Test ===========
def DictEntryView(request):
    print("=========== DictEntryView ===========")
    dicts = DictEntry.objects.all()
    
    context = {"dicts": dicts}
    return render(request, "mongos/DictEntry.html", context)


# ========= Celery Test ===========

def celery_send_mail(request):
    return render(request,
                  'mongos/celery_send_mail.html')


def task_use_celery(request):
    task_mail.delay()
    return render(request, 'mongos/celery_send_mail_done.html')


def task_not_use_celery(request):
    subject = 'subject test'
    message = 'message test'
    recipient = ['leamon.lee13@gmail.com',
                 'leamon.lee13@gmail.com', 
                 'leamon.lee13@gmail.com']
    mail_sent = send_mail(subject,
                          message,
                          'leamon.lee@pioneerm.com',
                          recipient)
    return render(request,
                  'mongos/celery_send_mail_done.html')