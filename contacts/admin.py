from django.contrib import admin
from .models import Contact
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact

@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource





