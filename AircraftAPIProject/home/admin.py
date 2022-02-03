from django.contrib import admin
from .models import *

class FooAdmin(admin.ModelAdmin):
    readonly_fields = ('Create_Date',)

admin.site.register(Profile) 
admin.site.register(Task,FooAdmin)
