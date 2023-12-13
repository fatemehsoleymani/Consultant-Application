from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()

    def __str__(self):
        return f"{self.admin}"


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=55, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True,)
    nationality_code = models.CharField(max_length=15, null=True, blank=True)
    field_of_study = models.CharField(max_length=50,  null=True, blank=True)
    grade = models.CharField(max_length=2,  null=True, blank=True)
    code_of_consultant = models.CharField(max_length=6,  null=True, blank=True)
    total_study_time_per_week = models.CharField(max_length=4,  null=True, blank=True)
    total_tests_per_week = models.CharField(max_length=5,  null=True, blank=True)
    state = models.CharField(max_length=75,  null=True, blank=True)
    city = models.CharField(max_length=75,  null=True, blank=True)
    has_consultant = models.CharField(max_length=55, null=True, blank=True)
    consultant_with_namak = models.CharField(max_length=50, null=True, blank=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE, blank=True, null=True)
    target_field = models.CharField(max_length=48, null=True, blank=True)
    rank_region_target = models.CharField(max_length=48,  null=True, blank=True)
    score_target = models.CharField(max_length=48,  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,  null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,  null=True, blank=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()

    def __str__(self):
        return f"{self.admin}"


class SchoolLesson(models.Model):
    YES = 1
    No = 2
    YES_NO_CHOICES = (
        (YES, 'yes'),
        (No, 'no')
    )
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    school_name = models.CharField(max_length=48)
    subject_name = models.CharField(max_length=48)
    teacher_name = models.CharField(max_length=100)
    total_time_studying_per_week = models.CharField(max_length=3)
    score = models.CharField(max_length=2)
    has_test_in_class = models.CharField(max_length=5)
    average_test_percentage = models.CharField(max_length=3)
    total_test_numbers = models.CharField(max_length=5)
    target_test_numbers = models.CharField(max_length=5)
    test_proficiency = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.subject_name}'



class InstituteLesson(models.Model):
    institute_name = models.CharField(max_length=48)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    subject_name = models.CharField(max_length=48)
    teacher_name = models.CharField(max_length=100)
    total_time_in_class_per_week = models.CharField(max_length=2)
    total_test_numbers = models.CharField(max_length=5)
    has_test_in_class = models.CharField(max_length=3)
    average_test_percentage = models.CharField(max_length=3)
    target_test_numbers = models.CharField(max_length=5)
    total_time_studying_per_week = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.subject_name}"


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()


class ExperimentalTest(models.Model):
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tests')
    name = models.CharField(max_length=48)
    average_test_score = models.CharField(max_length=7, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.average_test_score}"


class Assignment(models.Model):
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='homeworks')
    school_subject = models.ForeignKey(
        SchoolLesson, on_delete=models.CASCADE, related_name='homeworks', blank=True, null=True,
        default=None
    )
    institute_subject = models.ForeignKey(
        InstituteLesson, on_delete=models.CASCADE, related_name='homeworks', blank=True, null=True,
        default=None
    )
    content = models.FileField(upload_to='files/')
    text = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.school_subject}  {self.institute_subject} : {self.created_time}"


class MessageBox(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return f"{self.assignment.school_subject} {self.assignment.institute_subject} - Message"



class Planning(models.Model):
    STUDYING = 1
    REVIEWING = 2
    TESTING = 3
    FORM_Of_STUDYING = (
        (STUDYING, 'studying'),
        (REVIEWING, 'reviewing'),
        (TESTING, 'testing')
    )
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='planning')
    subject_school = models.ForeignKey(
        SchoolLesson, on_delete=models.CASCADE, blank=True, null=True, related_name='school_planning'
    )
    subject_institute = models.ForeignKey(
        InstituteLesson, on_delete=models.CASCADE, blank=True, null=True, related_name='institute_planning'
    )
    form_of_studying = models.IntegerField(choices=FORM_Of_STUDYING, blank=True, null=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    objects = models.Manager()

    @property
    def get_html_url(self):
        url = reverse('plan_edit', args=(self.id,))
        return f'<a href="{url}"> {self.subject_school or self.subject_institute}</a>'

    def __str__(self):
        return f'{self.subject_school or self.subject_institute}'


class Implementation(models.Model):
    COMPLETED = 1
    ABOUT = 2
    NOT_COMPLETED = 3
    COMPLETED_CHOICES = (
        (COMPLETED, 'green'),
        (ABOUT, 'yellow'),
        (NOT_COMPLETED, 'red')
    )

    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='implementation')
    subject = models.ForeignKey(
        Planning, on_delete=models.CASCADE, blank=True, null=True, related_name='implementation'
    )

    total_test = models.CharField(max_length=4, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_time = models.CharField(max_length=2)
    adherence_to_the_program = models.IntegerField(choices=COMPLETED_CHOICES)
    objects = models.Manager()

    def __str__(self):
        return f'{self.subject.subject_school or self.subject.subject_institute}'

    @property
    def get_html_url_imp(self):
        url = reverse('implement_edit', args=(self.id,))
        return f'<a href="{url}"> {self.subject.subject_school or self.subject.subject_institute}</a>'



