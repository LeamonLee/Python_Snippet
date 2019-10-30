from django.urls import path
from .views import (
    Contact_upload, 
    contact_download,
    celery_send_mail,
    DictEntryView
)
    
# from . import views

app_name = "mongos"

urlpatterns = [
    path('upload_csv/', Contact_upload, name="contact_upload"),
    path('download_csv/', contact_download, name="download_csv"),
    path('celery_send_mail/', celery_send_mail, name="celery_send_mail"),
    path('dict_entry/', DictEntryView, name="dict_entry"),
]