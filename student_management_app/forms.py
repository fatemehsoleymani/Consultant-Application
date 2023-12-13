from django import forms
from django.forms import ModelForm

from student_management_app.models import Staffs, Students, SchoolLesson, InstituteLesson, ExperimentalTest, Assignment, \
    MessageBox, Planning, Implementation


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    sex = forms.ChoiceField(label="Sex", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="Date Of Birth", widget=DateInput(attrs={"class": "form-control"}))
    nationality_code = forms.CharField(
        label="Nationality Code", max_length=10, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    field_of_study = forms.CharField(
        label="Field Of Study", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    grade = forms.CharField(
        label="Grade", max_length=2, widget=forms.TextInput(attrs={"class": "form-control"}))
    yes_no_choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    has_consultant = forms.ChoiceField(
        label='Has_Consultant', choices=yes_no_choices, widget=forms.Select(attrs={"class": "form-control"})
    )
    code_of_consultant = forms.CharField(
        label="Code Of Consultant", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    consultant_with_namak = forms.ChoiceField(
        label="Consultant With Namak", choices=yes_no_choices, widget=forms.Select(attrs={"class": "form-control"})
    )
    staff_id = forms.ModelChoiceField(queryset=Staffs.objects.all())
    total_study_time_per_week = forms.CharField(
        label="Total Study Time Per Week", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    total_tests_per_week = forms.CharField(
        label="Total Test Per Week", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    state = forms.CharField(
        label="State", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    city = forms.CharField(
        label="City", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    target_field = forms.CharField(
        label="Target Field", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    rank_region_target = forms.CharField(
        label="Rang_Region Target", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    score_target = forms.CharField(
        label="Score Target", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )


class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    sex = forms.ChoiceField(label="Sex", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="Date Of Birth", widget=DateInput(attrs={"class": "form-control"}))
    nationality_code = forms.CharField(
        label="Nationality Code", max_length=10, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    field_of_study = forms.CharField(
        label="Field Of Study", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    grade = forms.CharField(
        label="Grade", max_length=2, widget=forms.TextInput(attrs={"class": "form-control"}))
    yes_no_choices = (
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    has_consultant = forms.ChoiceField(
        label='Has_Consultant', choices=yes_no_choices, widget=forms.Select(attrs={"class": "form-control"})
    )
    code_of_consultant = forms.CharField(
        label="Code Of Consultant", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    consultant_with_namak = forms.ChoiceField(
        label="Consultant With Namak", choices=yes_no_choices, widget=forms.Select(attrs={"class": "form-control"})
    )
    staff_id = forms.ModelChoiceField(queryset=Staffs.objects.all())
    total_study_time_per_week = forms.CharField(
        label="Total Study Time Per Week", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    total_tests_per_week = forms.CharField(
        label="Total Test Per Week", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    state = forms.CharField(
        label="State", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    city = forms.CharField(
        label="City", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    target_field = forms.CharField(
        label="Target Field", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    rank_region_target = forms.CharField(
        label="Rang_Region Target", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    score_target = forms.CharField(
        label="Score Target", max_length=6, widget=forms.TextInput(attrs={"class": "form-control"})
    )


class SchoolSubjectForm(forms.ModelForm):
    class Meta:
        model = SchoolLesson
        fields = [
            'subject_name', 'teacher_name', 'school_name', 'total_time_studying_per_week',
            'score', 'has_test_in_class', 'average_test_percentage', 'total_test_numbers', 'target_test_numbers',
            'test_proficiency'
        ]


class InstituteLessonForm(forms.ModelForm):
    class Meta:
        model = InstituteLesson
        fields = [
            'institute_name', 'subject_name', 'teacher_name', 'total_time_in_class_per_week',
            'total_test_numbers', 'has_test_in_class', 'average_test_percentage',
            'target_test_numbers', 'total_time_studying_per_week'
        ]


class ExperimentalTestForm(forms.ModelForm):
    class Meta:
        model = ExperimentalTest
        fields = [
            'name', 'average_test_score'
        ]


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['school_subject', 'institute_subject', 'content', 'text']


class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageBox
        fields = ['message']


class PlanningForm(ModelForm):
    class Meta:
        model = Planning
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        exclude = ('student_id',)

    def __init__(self, *args, **kwargs):
        super(PlanningForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


class ImplementationForm(ModelForm):
    class Meta:
        model = Implementation
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        exclude = ('student_id',)

    def __init__(self, *args, **kwargs):
        super(ImplementationForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
