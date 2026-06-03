from django.contrib import admin
from.models import Task

@admin.register(Task)

class taskadmin(admin.ModelAdmin):

    fields=["title",'description','priority','status','owner','completed_at','due_date'] # field in form
    list_display=['title','status','completed_at','owner','created_at','updated_at'] # field display 
    list_filter=['status','priority']
    search_fields=['title']