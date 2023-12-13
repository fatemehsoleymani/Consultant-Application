# from django.contrib import admin
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from student_management_app.models import CustomUser, AdminHOD, Students, Staffs
#
#
# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ['user_type_data', 'user_type']
#
#
# @admin.register(AdminHOD)
# class AdminHODAdmin(admin.ModelAdmin):
#     list_display = ['admin']
#
#
# @admin.register(Staffs)
# class StaffsAdmin(admin.ModelAdmin):
#     list_display = ['admin', 'first_name', 'last_name']
#
#
# @admin.register(Students)
# class StudentsAdmin(admin.ModelAdmin):
#     list_display = ['admin', 'date_of_birth', 'gender']
#

from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from student_management_app.models import *


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser,UserModel)
# admin.site.register(AdminHOD)
# admin.site.register(Staffs)
# admin.site.register(Students)
# admin.site.register(SchoolLesson)
# admin.site.register(InstituteLesson)
# admin.site.register(FeedBackStudent)
# admin.site.register(FeedBackStaffs)
# admin.site.register(NotificationStudent)
# admin.site.register(NotificationStaffs)