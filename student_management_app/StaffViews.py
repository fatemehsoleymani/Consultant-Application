import calendar
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from student_management_app.models import Staffs, FeedBackStaffs, CustomUser, Students, NotificationStaffs, Planning, \
    SchoolLesson, InstituteLesson
from student_management_app.utils import PlanningCalendar


def staff_home(request):
    staff_obj = Staffs.objects.get(admin=request.user)
    students = Students.objects.filter(staff_id=staff_obj).count()
    return render(request, "staff_template/staff_home_template.html", {'students': students})


def student_list(request):
    staff_obj = Staffs.objects.get(admin=request.user)
    students = Students.objects.filter(staff_id=staff_obj)
    return render(request, 'staff_template/student_list.html', {'students': students})


def staff_feedback(request):
    staff_id = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request, 'staff_template/staff_feedback.html', {'feedback_data': feedback_data})


def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg = request.POST.get('feedback_msg')
        staff_obj = Staffs.objects.get(admin=request.user.id)

        try:
            feedback = FeedBackStaffs(staff_id=staff_obj,
                                      feedback=feedback_msg,
                                      feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Feedback Sent.")
            return HttpResponseRedirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return HttpResponseRedirect('staff_feedback')


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)
    return render(request, "staff_template/staff_profile.html", {"user": user, "staff": staff})


def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password is not None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))


@csrf_exempt
def staff_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        staff = Staffs.objects.get(admin=request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_all_notification(request):
    staff=Staffs.objects.get(admin=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request,"staff_template/all_notification.html",{"notifications":notifications})


