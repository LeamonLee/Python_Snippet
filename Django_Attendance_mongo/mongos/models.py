# from django.db import models
from djongo import models
from django import forms

# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        abstract = True

# class BlogForm(forms.ModelForm):

#     class Meta:
#         model = Blog
#         fields = "__all__"

class MetaData(models.Model):
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    class Meta:
        abstract = True

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name



class Entry(models.Model):
    blog = models.EmbeddedModelField(
        model_container=Blog,
        # model_form_class=BlogForm
    )
    meta_data = models.EmbeddedModelField(
        model_container=MetaData,
    )

    headline = models.CharField(max_length=255)
    body_text = models.TextField()

    # authors = models.ManyToManyField(Author)

    authors = models.ArrayModelField(
        model_container=Author,
    )

    n_comments = models.IntegerField()

    # Failed!!!
    # test_int_list = models.ArrayModelField(
    #     model_container=models.IntegerField(), default=None, blank=True, null=True,
    # )

    def __str__(self):
        return self.headline


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField(null=True)
    message = models.TextField()


    def __str__(self):
        return f"{self.first_name}.{self.last_name}"

# Test the usage of ListField
class ListEntry(models.Model):
    _id = models.ObjectIdField()
    headline = models.CharField(max_length=255)
    authors = models.ListField()

    def __str__(self):
        return self.headline

# Test the usage of DictField
class DictEntry(models.Model):
    _id = models.ObjectIdField()
    headline = models.CharField(max_length=255)
    blog = models.DictField()

    def __str__(self):
        return self.headline