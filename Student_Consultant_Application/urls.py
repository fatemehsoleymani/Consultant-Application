"""
URL configuration for Student_Consultant_Application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from student_management_app import HodViews, views, StaffViews, StudentViews

urlpatterns = [
                  path('demo', views.showDemoPage),
                  path('signup_student', views.signup_student, name="signup_student"),
                  path('do_signup_student', views.do_signup_student, name="do_signup_student"),
                  path('admin/', admin.site.urls),
                  path('', views.ShowLoginPage, name="show_login"),
                  path('get_user_details', views.GetUserDetails),
                  path('logout_user', views.logout_user, name="logout"),
                  path('doLogin', views.doLogin, name="do_login"),
                  path('firebase-messaging-sw.js', views.showFirebaseJS, name="show_firebase_js"),
                  # admin
                  path('admin_home', HodViews.admin_home, name="admin_home"),
                  path('add_staff', HodViews.add_staff, name="add_staff"),
                  path('add_staff_save', HodViews.add_staff_save, name="add_staff_save"),
                  path('manage_staff', HodViews.manage_staff, name="manage_staff"),
                  path('edit_staff/<str:staff_id>', HodViews.edit_staff, name="edit_staff"),
                  path('edit_staff_save', HodViews.edit_staff_save, name="edit_staff_save"),
                  path('add_student', HodViews.add_student, name="add_student"),
                  path('add_student_save', HodViews.add_student_save, name="add_student_save"),
                  path('manage_student', HodViews.manage_student, name="manage_student"),
                  path('edit_student/<str:student_id>', HodViews.edit_student, name="edit_student"),
                  path('edit_student_save', HodViews.edit_student_save, name="edit_student_save"),
                  path('add_school_subject', HodViews.add_school_subject, name="add_school_subject"),
                  path('add_school_subject_save', HodViews.add_school_subject_save, name="add_school_subject_save"),
                  path('manage_subject', HodViews.manage_school_subject, name="manage_school_subject"),
                  path('edit_school_subject/<str:subject_id>', HodViews.edit_school_subject,
                       name="edit_school_subject"),
                  path('edit_school_subject_save', HodViews.edit_school_subject_save, name="edit_school_subject_save"),
                  path('add_institute_subject', HodViews.add_institute_subject, name="add_institute_subject"),
                  path('add_institute_subject_save', HodViews.add_institute_subject_save,
                       name="add_institute_subject_save"),
                  path('manage_institute_subject', HodViews.manage_institute_subject, name="manage_institute_subject"),
                  path('edit_institute_subject/<str:subject_id>', HodViews.edit_institute_subject,
                       name="edit_institute_subject"),
                  path('edit_institute_subject_save', HodViews.edit_institute_subject_save,
                       name="edit_institute_subject_save"),
                  path('staff_feedback_message', HodViews.staff_feedback_message, name="staff_feedback_message"),
                  path('student_feedback_message', HodViews.student_feedback_message, name="student_feedback_message"),
                  path('student_feedback_message_replied', HodViews.student_feedback_message_replied,
                       name="student_feedback_message_replied"),
                  path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied,
                       name="staff_feedback_message_replied"),
                  path('admin_profile', HodViews.admin_profile, name="admin_profile"),
                  path('admin_profile_save', HodViews.admin_profile_save, name="admin_profile_save"),
                  path('admin_send_notification_staff', HodViews.admin_send_notification_staff,
                       name="admin_send_notification_staff"),
                  path('admin_send_notification_student', HodViews.admin_send_notification_student,
                       name="admin_send_notification_student"),
                  path('send_student_notification', HodViews.send_student_notification,
                       name="send_student_notification"),
                  path('send_staff_notification', HodViews.send_staff_notification, name="send_staff_notification"),
                  # staff
                  path('staff_home', StaffViews.staff_home, name="staff_home"),
                  path('student_list', StaffViews.student_list, name='student_list'),
                  path('staff_feedback', StaffViews.staff_feedback, name='staff_feedback'),
                  path('staff_feedback_save', StaffViews.staff_feedback_save, name='staff_feedback_save'),
                  path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
                  path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),
                  path('staff_fcmtoken_save', StaffViews.staff_fcmtoken_save, name="staff_fcmtoken_save"),
                  path('staff_all_notification', StaffViews.staff_all_notification, name="staff_all_notification"),
                  # student
                  path('student_home', StudentViews.student_home, name="student_home"),
                  path('student_profile', StudentViews.student_profile, name='student_profile'),
                  path('student_profile', StudentViews.student_profile, name="student_profile"),
                  path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),
                  path('student_fcmtoken_save', StudentViews.student_fcmtoken_save, name="student_fcmtoken_save"),
                  path('student_feedback', StudentViews.student_feedback, name='student_feedback'),
                  path('student_feedback_save', StudentViews.student_feedback_save, name='student_feedback_save'),
                  path('student_all_notification', StudentViews.student_all_notification,
                       name="student_all_notification"),
                  path('create_school_subject', StudentViews.create_school_subject, name='create_school_subject'),
                  path('school_subjects_list', StudentViews.school_subjects_list, name='school_subjects_list'),
                  path('school_subject_detail/<int:pk>', StudentViews.school_subject_detail,
                       name='school_subject_detail'),
                  path('school_subject_edit/<int:pk>', StudentViews.school_subject_edit, name='school_subject_edit'),
                  path('create_institute_subject', StudentViews.create_institute_subject,
                       name='create_institute_subject'),
                  path('institute_subjects_list', StudentViews.institute_subjects_list, name='institute_subjects_list'),
                  path('institute_subject_detail/<int:pk>', StudentViews.institute_subject_detail,
                       name='institute_subject_detail'),
                  path('institute_subject_edit/<int:pk>', StudentViews.institute_subject_edit,
                       name='institute_subject_edit'),
                  path('test_create', StudentViews.institute_test_create, name='test_create'),
                  path('test_list', StudentViews.test_list, name='test_list'),
                  path('test_detail/<int:pk>', StudentViews.test_detail, name='test_detail'),
                  path('test_edit/<int:pk>', StudentViews.test_update, name='test_edit'),
                  path('assignment_create', StudentViews.assignment_create, name='assignment_create'),
                  path('assignment_list', StudentViews.assignment_list, name='assignment_list'),
                  path('institute_assignment_list', StudentViews.institute_assignment_list,
                       name='institute_assignment_list'),
                  path('assignment/detail/<int:pk>/', StudentViews.assignment_detail, name='assignment_detail'),
                  path('assignment/message/<int:pk>/', StudentViews.assignment_message, name='assignment_message'),
                  path('assignment/download/<int:pk>/', StudentViews.download_assignment_file,
                       name='assignment_download'),
                  path('planning', StudentViews.PlanningCalendarView.as_view(), name='planning'),
                  path('new_plan', StudentViews.plan, name='new_plan'),
                  path('plan_edit/<int:plan_id>', StudentViews.plan, name='plan_edit'),
                  path('implementation', StudentViews.ImplementationCalendarView.as_view(), name='implementation'),
                  path('implement', StudentViews.implementation, name='new_implement'),
                  path('implement/<int:implement_id>', StudentViews.implementation, name='implement_edit')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
