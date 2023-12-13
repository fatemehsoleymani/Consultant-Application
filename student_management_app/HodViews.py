import json

import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student_management_app.forms import AddStudentForm, EditStudentForm
from student_management_app.models import CustomUser, Staffs, Students, SchoolLesson, InstituteLesson, FeedBackStaffs, \
    FeedBackStudent, NotificationStaffs, NotificationStudent


def admin_home(request):
    student_count1 = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    school_subject_count = SchoolLesson.objects.all().count()
    institute_subject_count = InstituteLesson.objects.all().count()

    return render(
        request, "hod_template/home_content.html", {'student_count1': student_count1, 'staff_count': staff_count,
                                                    'school_subject_count': school_subject_count,
                                                    'institute_subject_count': institute_subject_count,
                                                    }
    )


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password,
                                                  last_name=last_name, first_name=first_name, user_type=2)
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_template/manage_staff_template.html", {"staffs": staffs})


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/edit_staff_template.html", {"staff": staff, "id": staff_id})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, "Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))


def add_student(request):
    form = AddStudentForm()
    return render(request, "hod_template/add_student_template.html", {"form": form})


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            sex = form.cleaned_data["sex"]
            date_of_birth = form.cleaned_data['date_of_birth']
            nationality_code = form.cleaned_data["nationality_code"]
            field_of_study = form.cleaned_data["field_of_study"]
            grade = form.cleaned_data["grade"]
            has_consultant = form.cleaned_data["has_consultant"]
            code_of_consultant = form.cleaned_data["code_of_consultant"]
            consultant_with_namek = form.cleaned_data["consultant_with_namak"]
            staff_id = form.cleaned_data["staff_id"]
            total_study_time_per_week = form.cleaned_data["total_study_time_per_week"]
            total_tests_per_week = form.cleaned_data["total_tests_per_week"]
            state = form.cleaned_data["state"]
            city = form.cleaned_data["city"]
            target_field = form.cleaned_data["target_field"]
            rank_region_target = form.cleaned_data["rank_region_target"]
            score_target = form.cleaned_data["score_target"]

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name, first_name=first_name, user_type=3)
                user.students.gender = sex
                user.students.date_of_birth = date_of_birth
                user.students.nationality_code = nationality_code
                user.students.field_of_study = field_of_study
                user.students.grade = grade
                user.students.has_consultant = has_consultant
                user.students.code_of_consultant = code_of_consultant
                user.students.consultant_with_namak = consultant_with_namek
                user.students.staff_id = staff_id
                user.students.total_study_time_per_week = total_study_time_per_week
                user.students.total_tests_per_week = total_tests_per_week
                user.students.state = state
                user.students.city = city
                user.students.target_field = target_field
                user.students.rank_region_target = rank_region_target
                user.students.score_target = score_target

                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))

        else:
            form = AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})


def manage_student(request):
    students = Students.objects.all()
    return render(request, "hod_template/manage_student_template.html", {"students": students})


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['nationality_code'].initial = student.nationality_code
    form.fields['field_of_study'].initial = student.field_of_study
    form.fields['sex'].initial = student.gender
    form.fields['date_of_birth'].initial = student.date_of_birth
    form.fields['grade'].initial = student.grade
    form.fields['has_consultant'].initial = student.has_consultant
    form.fields['code_of_consultant'].initial = student.code_of_consultant
    form.fields['consultant_with_namak'].initial = student.consultant_with_namak
    form.fields['staff_id'].initial = student.staff_id
    form.fields['total_study_time_per_week'].initial = student.total_study_time_per_week
    form.fields['total_tests_per_week'].initial = student.total_tests_per_week
    form.fields['state'].initial = student.state
    form.fields['city'].initial = student.city
    form.fields['target_field'].initial = student.target_field
    form.fields['rank_region_target'].initial = student.rank_region_target
    form.fields['score_target'].initial = student.score_target
    return render(request, "hod_template/edit_student_template.html",
                  {"form": form, "id": student_id, "username": student.admin.username})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.session.get("student_id")
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))
        form = EditStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            sex = form.cleaned_data["sex"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            nationality_code = form.cleaned_data["nationality_code"]
            field_of_study = form.cleaned_data["field_of_study"]
            grade = form.cleaned_data["grade"]
            has_consultant = form.cleaned_data["has_consultant"]
            code_of_consultant = form.cleaned_data["code_of_consultant"]
            consultant_with_namek = form.cleaned_data["consultant_with_namak"]
            staff_id = form.cleaned_data["staff_id"]
            total_study_time_per_week = form.cleaned_data["total_study_time_per_week"]
            total_tests_per_week = form.cleaned_data["total_tests_per_week"]
            state = form.cleaned_data["state"]
            city = form.cleaned_data["city"]
            target_field = form.cleaned_data["target_field"]
            rank_region_target = form.cleaned_data["rank_region_target"]
            score_target = form.cleaned_data["score_target"]
            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Students.objects.get(admin=student_id)
                student.gender = sex
                student.date_of_birth = date_of_birth
                student.nationality_code = nationality_code
                student.field_of_study = field_of_study
                student.grade = grade
                student.has_consultant = has_consultant
                student.code_of_consultant = code_of_consultant
                student.consultant_with_namak = consultant_with_namek
                student.staff_id = staff_id
                student.total_study_time_per_week = total_study_time_per_week
                student.total_tests_per_week = total_tests_per_week
                student.state = state
                student.city = city
                student.target_field = target_field
                student.rank_region_target = rank_region_target
                student.score_target = score_target
                student.save()
                del request.session['student_id']
                messages.success(request, "Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
            except:
                messages.error(request, "Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request, "hod_template/edit_student_template.html",
                          {"form": form, "id": student_id, "username": student.admin.username})


def add_school_subject(request):
    students = CustomUser.objects.filter(user_type=3)
    return render(request, "hod_template/add_school_subject_template.html", {'students': students})


def add_school_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        student_id = request.POST.get("student")
        student = CustomUser.objects.get(id=student_id)
        teacher_name = request.POST.get("teacher_name")
        total_time_studying_per_week = request.POST.get("total_time_studying_per_week")
        score = request.POST.get("score")
        has_test_in_class = request.POST.get("has_test_in_class")
        average_test_percentage = request.POST.get("average_test_percentage")
        total_test_numbers = request.POST.get("total_test_numbers")
        target_test_numbers = request.POST.get("target_test_numbers")
        test_proficiency = request.POST.get("test_proficiency")

        try:
            subject = SchoolLesson(
                subject_name=subject_name, student_id=student, teacher_name=teacher_name, total_time_studying_per_week=
                total_time_studying_per_week, score=score, average_test_percentage=average_test_percentage,
                total_test_numbers=total_test_numbers, target_test_numbers=target_test_numbers, has_test_in_class=
                has_test_in_class,
                test_proficiency=test_proficiency
            )
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_school_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_school_subject"))


def manage_school_subject(request):
    subjects = SchoolLesson.objects.all()
    return render(request, "hod_template/manage_school_subject_template.html", {"subjects": subjects})


def edit_school_subject(request, subject_id):
    subject = SchoolLesson.objects.get(id=subject_id)
    students = CustomUser.objects.filter(user_type=3)
    return render(request, "hod_template/edit_school_subject_template.html",
                  {"subject": subject, "students": students})


def edit_school_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        student_id = request.POST.get("student")
        teacher_name = request.POST.get("teacher_name")
        total_time_studying_per_week = request.POST.get("total_time_studying_per_week")
        score = request.POST.get("score")
        has_test_in_class = request.POST.get("has_test_in_class")
        average_test_percentage = request.POST.get("average_test_percentage")
        total_test_numbers = request.POST.get("total_test_numbers")
        target_test_numbers = request.POST.get("target_test_numbers")
        test_proficiency = request.POST.get("test_proficiency")
        try:
            subject = SchoolLesson.objects.get(id=subject_id)
            subject.subject_name = subject_name
            student = CustomUser.objects.get(id=student_id)
            subject.student = student
            subject.teacher_name = teacher_name
            subject.total_time_studying_per_week = total_time_studying_per_week
            subject.score = score
            subject.has_test_in_class = has_test_in_class
            subject.average_test_percentage = average_test_percentage
            subject.total_test_numbers = total_test_numbers
            subject.target_test_numbers = target_test_numbers
            subject.test_proficiency = test_proficiency
            subject.save()

            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_school_subject", kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, "Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_school_subject", kwargs={"subject_id": subject_id}))


def add_institute_subject(request):
    students = CustomUser.objects.filter(user_type=3)
    return render(request, "hod_template/add_institute_subject_template.html", {"students": students})


def add_institute_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        student_id = request.POST.get("student")
        student = CustomUser.objects.get(id=student_id)
        teacher_name = request.POST.get("teacher_name")
        total_time_in_class_per_week = request.POST.get("total_time_in_class_per_week")
        total_time_studying_per_week = request.POST.get("total_time_studying_per_week")
        has_test_in_class = request.POST.get("has_test_in_class")
        average_test_percentage = request.POST.get("average_test_percentage")
        total_test_numbers = request.POST.get("total_test_numbers")
        target_test_numbers = request.POST.get("target_test_numbers")

        try:
            subject = InstituteLesson(
                subject_name=subject_name, student_id=student, teacher_name=teacher_name, total_time_studying_per_week=
                total_time_studying_per_week, average_test_percentage=average_test_percentage,
                total_test_numbers=total_test_numbers, target_test_numbers=target_test_numbers, has_test_in_class=
                has_test_in_class, total_time_in_class_per_week=total_time_in_class_per_week

            )
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_institute_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_institute_subject"))


def manage_institute_subject(request):
    subjects = InstituteLesson.objects.all()
    return render(request, "hod_template/manage_institute_subject_template.html", {"subjects": subjects})


def edit_institute_subject(request, subject_id):
    subject = InstituteLesson.objects.get(id=subject_id)
    students = CustomUser.objects.filter(user_type=3)
    return render(request, "hod_template/edit_institute_subject_template.html",
                  {"subject": subject, "students": students})


def edit_institute_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        student_id = request.POST.get("student")
        teacher_name = request.POST.get("teacher_name")
        total_time_studying_per_week = request.POST.get("total_time_studying_per_week")
        total_time_in_class_per_week = request.POST.get("total_time_in_class_per_week")
        has_test_in_class = request.POST.get("has_test_in_class")
        average_test_percentage = request.POST.get("average_test_percentage")
        total_test_numbers = request.POST.get("total_test_numbers")
        target_test_numbers = request.POST.get("target_test_numbers")
        try:
            subject = InstituteLesson.objects.get(id=subject_id)
            subject.subject_name = subject_name
            student = CustomUser.objects.get(id=student_id)
            subject.student = student
            subject.teacher_name = teacher_name
            subject.total_time_studying_per_week = total_time_studying_per_week
            subject.total_time_in_class_per_week = total_time_in_class_per_week
            subject.has_test_in_class = has_test_in_class
            subject.average_test_percentage = average_test_percentage
            subject.total_test_numbers = total_test_numbers
            subject.target_test_numbers = target_test_numbers
            subject.save()

            messages.success(request, "Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_institute_subject", kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, "Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_institute_subject", kwargs={"subject_id": subject_id}))


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    return render(request, "hod_template/staff_feedback_template.html", {"feedbacks": feedbacks})


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(request, "hod_template/student_feedback_template.html", {"feedbacks": feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "hod_template/admin_profile.html", {"user": user})


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


def admin_send_notification_student(request):
    students = Students.objects.all()
    return render(request, "hod_template/student_notification.html", {"students": students})


def admin_send_notification_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_template/staff_notification.html", {"staffs": staffs})


@csrf_exempt
def send_student_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    student = Students.objects.get(admin=id)
    token = student.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json", "Authorization": "key=SERVER_KEY_HERE"}
    data = requests.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStudent(student_id=student, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get("id")
    message = request.POST.get("message")
    staff = Staffs.objects.get(admin=id)
    token = staff.fcm_token
    url = "https://fcm.googleapis.com/fcm/send"
    body = {
        "notification": {
            "title": "Student Management System",
            "body": message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to": token
    }
    headers = {"Content-Type": "application/json", "Authorization": "key=SERVER_KEY_HERE"}
    data = requests.post(url, data=json.dumps(body), headers=headers)
    notification = NotificationStaffs(staff_id=staff, message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")
