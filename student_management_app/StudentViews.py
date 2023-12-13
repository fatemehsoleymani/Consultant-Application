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
from django.views.decorators.http import require_http_methods, require_POST

from student_management_app.forms import EditStudentForm, SchoolSubjectForm, InstituteLessonForm, ExperimentalTestForm, \
    AssignmentForm, MessageForm, PlanningForm, ImplementationForm
from student_management_app.models import Students, FeedBackStudent, CustomUser, SchoolLesson, InstituteLesson, \
    NotificationStudent, ExperimentalTest, MessageBox, Assignment, Planning, Implementation
from student_management_app.utils import PlanningCalendar, ImplementationCalendar


def student_home(request):
    student_obj = CustomUser.objects.get(id=request.user.id)
    school_subjects = SchoolLesson.objects.filter(student_id=student_obj).count()
    institute_subjects = InstituteLesson.objects.filter(student_id=student_obj).count()
    return render(
        request, "student_template/student_home_template.html", {'school_subjects': school_subjects,
                                                                 'institute_subjects': institute_subjects}
    )


def student_feedback(request):
    student_id = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_id)
    return render(request, 'student_template/student_feedback.html', {'feedback_data': feedback_data})


def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback_save"))
    else:
        feedback_msg = request.POST.get('feedback_msg')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            feedback = FeedBackStudent(student_id=student_obj,
                                       feedback=feedback_msg,
                                       feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Feedback Sent.")
            return HttpResponseRedirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return HttpResponseRedirect('student_feedback')


def manage_feedback(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(request, 'student_template/student_feedback.html', {'feedbacks': feedbacks})


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    return render(request, "student_template/student_profile.html", {"user": user, "student": student})


def student_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        nationality_code = request.POST.get("nationality_code")
        field_of_study = request.POST.get("field_of_study")
        grade = request.POST.get("grade")
        code_of_consultant = request.POST.get("code_of_consultant")
        total_study_time_per_week = request.POST.get("total_study_time_per_week")
        total_tests_per_week = request.POST.get("total_tests_per_week")
        state = request.POST.get("state")
        city = request.POST.get("city")
        has_consultant = request.POST.get("has_consultant")
        consultant_with_namak = request.POST.get("consultant_with_namak")
        target_field = request.POST.get("target_field")
        rank_region_target = request.POST.get("rank_region_target")
        score_target = request.POST.get("score_target")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password is not None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser)
            student.gender = gender
            student.date_of_birth = date_of_birth
            student.nationality_code = nationality_code
            student.field_of_study = field_of_study
            student.grade = grade
            student.code_of_consultant = code_of_consultant
            student.total_study_time_per_week = total_study_time_per_week
            student.total_tests_per_week = total_tests_per_week
            student.state = state
            student.city = city
            student.has_consultant = has_consultant
            student.target_field = target_field
            student.rank_region_target = rank_region_target
            student.score_target = score_target
            student.consultant_with_namak = consultant_with_namak
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))


@csrf_exempt
def student_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        student = Students.objects.get(admin=request.user.id)
        student.fcm_token = token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_all_notification(request):
    student = Students.objects.get(admin=request.user.id)
    notifications = NotificationStudent.objects.filter(student_id=student.id)
    return render(request, "student_template/all_notification.html", {"notifications": notifications})


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def create_school_subject(request):
    if request.method == "POST":
        form = SchoolSubjectForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.student_id = request.user
            instance.save()
            messages.success(request, 'Subject created successfully ')
        else:
            messages.error(request, 'Error create your subject')
    else:
        form = SchoolSubjectForm()
    return render(request, 'student_template/create_school_subject.html', {'form': form})


@login_required
def school_subjects_list(request):
    context = dict()
    context['subjects'] = SchoolLesson.objects.filter(student_id=request.user)
    return render(request, 'student_template/school_subjects_list.html', context)


def school_subject_detail(request, pk):
    school_subject = SchoolLesson.objects.get(pk=pk)
    return render(request, 'student_template/school_subject_detail.html', {'school_subject': school_subject})


def school_subject_edit(request, pk):
    school_subject = SchoolLesson.objects.get(pk=pk)
    if request.method == 'POST':
        form = SchoolSubjectForm(request.POST, instance=school_subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully ')
        else:
            messages.error(request, 'Error create your subject')
    else:
        form = SchoolSubjectForm(instance=school_subject)
    return render(request, 'student_template/school_subject_edit.html', {'form': form})


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def create_institute_subject(request):
    if request.method == "POST":
        form = InstituteLessonForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.student_id = request.user
            instance.save()
            messages.success(request, 'Subject created successfully ')
        else:
            messages.error(request, 'Error create your subject')
    else:
        form = InstituteLessonForm()
    return render(request, 'student_template/create_institute_subject.html', {'form': form})


@login_required
def institute_subjects_list(request):
    context = dict()
    context['subjects'] = InstituteLesson.objects.filter(student_id=request.user)
    return render(request, 'student_template/institute_subjects_list.html', context)


def institute_subject_detail(request, pk):
    institute_subject = InstituteLesson.objects.get(pk=pk)
    return render(request, 'student_template/institute_subject_detail.html', {'institute_subject': institute_subject})


def institute_subject_edit(request, pk):
    school_subject = InstituteLesson.objects.get(pk=pk)
    if request.method == 'POST':
        form = InstituteLessonForm(request.POST, instance=school_subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully ')
        else:
            messages.error(request, 'Error create your subject')
    else:
        form = InstituteLessonForm(instance=school_subject)
    return render(request, 'student_template/institute_subject_edit.html', {'form': form})


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def institute_test_create(request):
    if request.method == "POST":
        form = ExperimentalTestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.student_id = request.user
            instance.save()
            messages.success(request, 'Test created successfully ')
        else:
            messages.error(request, 'Error create your test')

    else:
        form = ExperimentalTestForm()
    return render(request, 'student_template/institute_test_create.html', {'form': form})


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def test_list(request):
    context = dict()
    context['tests'] = ExperimentalTest.objects.filter(student_id=request.user)
    return render(request, 'student_template/test_list.html', context=context)


def test_detail(request, pk):
    test = ExperimentalTest.objects.get(pk=pk)
    return render(request, 'student_template/test_detail.html', {'test': test})


def test_update(request, pk):
    test = ExperimentalTest.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExperimentalTestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            messages.success(request, 'Test updated successfully ')
        else:
            messages.error(request, 'Error update your test')
    else:
        form = ExperimentalTestForm(instance=test)
    return render(request, 'student_template/test_update.html', {'form': form})


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def assignment_create(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.student_id = request.user
            instance.save()
            messages.success(request, 'assignment uploaded successfully ')
        else:
            messages.error(request, 'Error upload your assignment')
            return HttpResponseRedirect(reverse('assignment_list'))

    else:
        form = AssignmentForm()
    user_school_subjects = SchoolLesson.objects.filter(student_id=request.user)
    form.fields['school_subject'].queryset = user_school_subjects
    user_institute_subjects = InstituteLesson.objects.filter(student_id=request.user)
    form.fields['institute_subject'].queryset = user_institute_subjects
    return render(request, 'student_template/assignment_create.html', {'form': form})


def download_assignment_file(request, pk):
    uploaded_file = Assignment.objects.get(pk=pk)
    file_path = uploaded_file.content.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application-octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.content.name}"'
        return response


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def assignment_list(request):
    context = dict()
    context['assignments'] = Assignment.objects.filter(
        school_subject__student_id=request.user
    )

    return render(request, 'student_template/assignment_list.html', context=context)


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def institute_assignment_list(request):
    context = dict()
    context['assignments'] = Assignment.objects.filter(
        institute_subject__student_id=request.user
    )

    return render(request, 'student_template/assignment_list.html', context=context)


@login_required
def assignment_detail(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    comments = assignment.messages.filter(assignment=assignment)
    form = MessageForm()
    return render(request, 'student_template/assignment_detail.html', {'assignment': assignment,
                                                                       'comments': comments,
                                                                       'form': form}
                  )


@require_POST
def assignment_message(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    message = None
    #     A comment was posted
    form = MessageForm(data=request.POST)
    if form.is_valid():
        # created a comment object without saving t to the database
        message = form.save(commit=False)
        # Assign the post to the comment
        message.assignment = assignment
        # Save the comment to the database
        message.save()
    return render(request, 'student_template/message.html', {'assignment': assignment,
                                                             'form': form,
                                                             'message': message})


class PlanningCalendarView(generic.ListView):
    model = Planning
    template_name = 'student_template/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = plan_get_date(self.request.GET.get('month', None))
        cal = PlanningCalendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, student_id=self.request.user)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def plan_get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required
def plan(request, plan_id=None):
    instance = Planning()
    if plan_id:
        instance = get_object_or_404(Planning, pk=plan_id)
    else:
        instance = Planning()

    form = PlanningForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.student_id = request.user
        instance.save()
        return HttpResponseRedirect(reverse('planning'))
    user_school_subjects = SchoolLesson.objects.filter(student_id=request.user)
    form.fields['subject_school'].queryset = user_school_subjects
    user_institute_subjects = InstituteLesson.objects.filter(student_id=request.user)
    form.fields['subject_institute'].queryset = user_institute_subjects
    return render(request, 'student_template/plan.html', {'form': form})


class ImplementationCalendarView(generic.ListView):
    model = Implementation
    context_object_name = 'implementation'
    template_name = 'student_template/implement_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = implement_get_date(self.request.GET.get('month', None))
        cal = ImplementationCalendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, student_id=self.request.user)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def implement_get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def imp_get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required
def implementation(request, implement_id=None):
    instance = Implementation
    if implement_id:
        instance = get_object_or_404(Implementation, pk=implement_id)
    else:
        instance = Implementation()

    form = ImplementationForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.student_id = request.user
        instance.save()
        return HttpResponseRedirect(reverse('implementation'))
    user_subjects = Planning.objects.filter(student_id=request.user)
    form.fields['subject'].queryset = user_subjects
    return render(request, 'student_template/implement.html', {'form': form})

