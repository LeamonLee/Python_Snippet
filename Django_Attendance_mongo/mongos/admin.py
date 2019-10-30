from django.contrib import admin
from .models import (
    Author,
    Entry,
    Contact,
    DictEntry
)

# Register your models here.

# admin.site.register(Author)
admin.site.register(Entry)
admin.site.register(Contact)
admin.site.register(DictEntry)
