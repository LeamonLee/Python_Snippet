from django.db import models
# from djangotoolbox.fields import ListField, DictField

# Create your models here.
class Music(models.Model):
    song = models.TextField()
    singer = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # documents = DictField(child=models.CharField())

    class Meta:
        db_table = "music"