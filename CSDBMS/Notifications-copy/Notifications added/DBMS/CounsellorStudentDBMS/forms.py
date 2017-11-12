from django.forms import ModelForm
from django import forms
from CounsellorStudentDBMS.models import Notifications, Student, counsellor, student_access, \
    StudentCourse, CoCurricular, CertImages, CourseCert, RegDetails, Scholarship, Parent, parent_access
import urllib
from django.http import QueryDict
from django.forms.models import model_to_dict

class CSignupForm(ModelForm):
    access_key = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = counsellor
        fields = '__all__'


class Cloginform(forms.Form):
    cid = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)


class CounsUpdateForm(ModelForm):
    class Meta:
        model = counsellor
        exclude = ['cid']

class ParentUpdateForm(ModelForm):
    class Meta:
        model = Parent
        exclude = ['pid', 'usn']


class CounsRegStudent(ModelForm):
    class Meta:
        model = student_access
        exclude = ['counsellor_id']


class CounsRegParent(ModelForm):
    class Meta:
        model = parent_access
        exclude = ['usn']


class CounsRegParentxx(ModelForm):
    class Meta:
        model = parent_access
        fields = '__all__'


class SemSectCgpaForm(ModelForm):
    class Meta:
        model = Student
        fields = ['sem', 'sec', 'cgpa']



class GradeCocurrForm(ModelForm):
    class Meta:
        model = CoCurricular
        fields = ['Grade']


class EnrolledCourseForm(ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['course_code']


class MarksAttForm(ModelForm):
    class Meta:
        model = StudentCourse
        exclude = ['usn', 'course_code']


class NotiForm(ModelForm):
    class Meta:
        model = Notifications
        exclude = ['cid', 'Slno', 'SentOn']


class SSignupForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    access_key = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    counsellor_id = forms.CharField(max_length=10)

    class Meta:
        model = Student
        exclude = ['sem', 'cgpa', 'cid', 'sec']
        include = ['access_key', 'password']
        widgets = {
            'access_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': True, }),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': True, }),
            'counsellor_id': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Title', 'required': True, }),
        }

class Sloginform(forms.Form):
    usn = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['usn', 'sec', 'sem', 'cgpa', 'cid']


class StudentRegDetailsForm(ModelForm):
    class Meta:
        model = RegDetails
        exclude = ['usn']


class StudentScholarshipForm(ModelForm):
    class Meta:
        model = Scholarship
        exclude = ['usn']


class CoCurrForm(ModelForm):
    class Meta:
        model = CoCurricular
        exclude = ['usn', 'Grade']


class AttendanceImagesForm(ModelForm):
    class Meta:
        model = CertImages
        exclude = ['usn']


class AttendanceCoursesForm(ModelForm):
    class Meta:
        model = CourseCert
        fields = ['course_code']


class StudentCourseForm(ModelForm):
    class Meta:
        model = StudentCourse
        fields = '__all__'


class PSignupForm(ModelForm):
    access_key = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Parent
        fields = '__all__'


class PLogin(forms.Form):
    pid = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)
