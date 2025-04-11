from django.contrib import admin
from .models import CustomUser, AndroidApp, Subcategory, Category, TaskSubmission

admin.site.register(CustomUser)
admin.site.register(AndroidApp)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(TaskSubmission)

