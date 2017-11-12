from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.generic import View, TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from CounsellorStudentDBMS.forms import NotiForm, CounsRegParentxx, CSignupForm, CounsUpdateForm, Cloginform, StudentCourseForm, SSignupForm, Sloginform, PSignupForm, PLogin, StudentUpdateForm, StudentRegDetailsForm, StudentScholarshipForm, CoCurrForm, AttendanceImagesForm, AttendanceCoursesForm, ParentUpdateForm, CounsRegStudent, CounsRegParent, SemSectCgpaForm, GradeCocurrForm, EnrolledCourseForm, MarksAttForm
from CounsellorStudentDBMS.models import Notifications, RegDetails,Scholarship,parent_access,Parent,Student, UserProfile, counsellor, counselor_table, student_access, StudentCourse,CertImages,CourseCert, CoCurricular
from django.forms.models import model_to_dict
import copy
# Create your views here.
def index(request):
    return render(request, 'CounsellorStudentDBMS/index.html', {})

def student_signup_main(request, str):
    if request.method == 'POST':
        if (str == 'Login'):
            password = request.POST['password']
            name = request.POST['usn']
            user = authenticate(username=name, password=password)
            if user is not None:
                if user.user_profile.p_type == 1:
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url:
                        return HttpResponseRedirect(next_url)
                    else:
                        return HttpResponseRedirect(reverse('student_home'))
                else:
                    msg = "Invalid Username or password!"
                    messages.add_message(request, messages.INFO, msg)
                    return HttpResponseRedirect(reverse('ssignup', args=('Login',)))
            else:
                msg = "Invalid Username or password!"
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse('ssignup', args= ('Login',)))
        else:
            username = request.POST['usn']
            ak = request.POST['access_key']
            try:
                stud = student_access.objects.get(usn=username)
            except student_access.DoesNotExist:
                stud = None
            if stud is None:
                msg = 'This USN is not registered by any Counsellor!'
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse('index'))
            elif stud.access_key != ak:
                msg = 'Incorrect Student Access key!'
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse('ssignup', args= ('Signup',)))
            elif stud.counsellor_id != request.POST['counsellor_id']:
                msg = 'Enter correct counsellor id'
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse('ssignup', args = ('Signup',)))
            else:
                form = SSignupForm(request.POST)
                if form.is_valid():
                    stu = form.save(commit=False)
                    stu.cid_id = stud.counsellor_id
                    stu.save()
                    name = request.POST['Fname']
                    password = request.POST['password']
                    email = request.POST['email']
                    user = User.objects.create_user(username=username, email=email, first_name=name)
                    user.set_password(password)
                    user.user_profile.p_type = 1
                    user.save()
                    user.user_profile.save()
                    return HttpResponseRedirect(reverse('index'))
                else:
                    msg = form.errors
                    messages.add_message(request, messages.INFO, msg)
                    return HttpResponseRedirect(reverse('ssignup', args=('Signup', )))
    elif (str == 'Signup'):
        form = SSignupForm()
        return render(request, 'CounsellorStudentDBMS/signup.html', {'form': form})
    elif (str == 'Login'):
        form = Sloginform()
        return render(request, 'CounsellorStudentDBMS/login.html', {'form': form})

def counsellor_signup_main(request, c_str):
    if request.method == 'POST':
        if (c_str == 'Login'):
            password = request.POST['password']
            name = request.POST['cid']
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('counsellor_page'))
            else:
                error = 'Invalid username or password!'
                messages.add_message(request, messages.INFO, error)
                return HttpResponseRedirect(reverse(('c_signup'), args=('Login',)))
        else:
            username = request.POST['cid']
            ak = request.POST['access_key']
            try:
                coun = counselor_table.objects.get(cid=username)
            except counselor_table.DoesNotExist:
                coun = None
            if coun is None:
                msg = 'This Counsellor id is not registered by the Admin!'
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse(('c_signup'), args=('Signup',)))
            elif coun.access_key != ak:
                msg = 'Incorrect Counsellor Access key!'
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse(('c_signup'), args=('Signup',)))
            else:
                form = CSignupForm(request.POST)
                if form.is_valid():
                    stu = form.save()
                    name = request.POST['Fname']
                    password = request.POST['password']
                    email = request.POST['email']
                    user = User.objects.create_user(username=username, email=email,first_name =name)
                    user.set_password(password)
                    user.user_profile.p_type = 2
                    user.save()
                    user.user_profile.save()
                    return HttpResponseRedirect(reverse('index'))
                else:
                    msg = form.errors
                    messages.add_message(request, messages.INFO, msg)
                    return HttpResponseRedirect(reverse('c_signup', args=('Signup',)))
    elif (c_str == 'Signup'):
        form = CSignupForm()
        return render(request, 'CounsellorStudentDBMS/signup.html', {'form': form})
    elif (c_str == 'Login'):
        form = Cloginform()
        return render(request, 'CounsellorStudentDBMS/login.html', {'form': form})

def parentSignupLogin(request, str):
    if request.method == 'POST':
        if(str == 'Login'):
            password = request.POST['password']
            name = request.POST['pid']
            user = authenticate(username = name, password = password)
            if user is not None and user.user_profile.p_type == 3:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('parent_page'))
            else:
                error = 'Invalid username or password!'
                messages.add_message(request, messages.INFO, error)
                return HttpResponseRedirect(reverse(('p_signup'), args=('Login',)))
        else:
            username = request.POST['pid']
            ak = request.POST['access_key']
            try:
                par = parent_access.objects.get(pid=username)
            except parent_access.DoesNotExist:
                par = None
            if par is None:
                error = "This parent id is not registered by any Counsellor!"
                messages.add_message(request, messages.INFO, error)
                return HttpResponseRedirect(reverse(('p_signup'), args=('Signup',)))
            elif par.access_key != ak:
                error = "Incorrect Parent Access key!"
                messages.add_message(request, messages.INFO, error)
                return HttpResponseRedirect(reverse(('p_signup'), args=('Signup',)))
            else:
                form = PSignupForm(request.POST)
                if form.is_valid():
                    par = form.save(commit=False)
                    usn = request.POST['usn']
                    pare = parent_access.objects.get(pid=username)
                    if usn != pare.usn_id:
                        msg = 'Incorrect USN'
                        messages.add_message(request, messages.INFO, msg)
                        return HttpResponseRedirect(reverse(('p_signup'), args=('Signup',)))
                    par.save()
                    password = request.POST['password']
                    email = request.POST['email']
                    Fname = request.POST['Fname']
                    user = User.objects.create_user(username=username, email=email, first_name=Fname)
                    user.set_password(password)
                    user.user_profile.p_type = 3
                    user.save()
                    user.user_profile.save()
                    return HttpResponseRedirect(reverse('index'))
                else:
                    msg = form.errors
                    messages.add_message(request, messages.INFO, msg)
                    return HttpResponseRedirect(reverse('p_signup', args=('Signup',)))
    elif(str == 'Signup'):
        form = PSignupForm()
        return render(request, 'CounsellorStudentDBMS/signup.html', {'form':form})
    elif(str == 'Login'):
        form = PLogin()
        return render(request, 'CounsellorStudentDBMS/login.html', {'form':form})

def student_home(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a Student!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    else:
        s = Student.objects.get(usn = request.user.username)
        return render(request, 'CounsellorStudentDBMS/student.html', {'s':s})

def parent_main(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 3:
        msg = 'You are not a parent!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    else:
        p = Parent.objects.get(pid=request.user.username)
        return render(request, 'CounsellorStudentDBMS/parent.html', {'p':p})

def counsellor_main(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type !=2:
        return HttpResponse("You are not a counsellor.")
    else:
        c = counsellor.objects.get(cid = request.user.username)
        studs = Student.objects.filter(cid_id = c.cid)
        return render(request, 'CounsellorStudentDBMS/counsellor_home.html', {'studs': studs,'c':c})

def StudentProfile(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    s = Student.objects.get(usn= request.user.username)
    return render(request, 'CounsellorStudentDBMS/StudentProfile.html', {'s':s, 'user': request.user.user_profile.p_type})

def counsStudDetails(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    s = Student.objects.get(usn = usn)
    return render(request, 'CounsellorStudentDBMS/StudentProfile.html',{'s': s, 'user': request.user.user_profile.p_type})

def ParStudDetails(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 3:
        msg = 'You are not a parent!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    p = Parent.objects.get(pid = request.user.username)
    s = Student.objects.get(usn = p.usn_id)
    return render(request, 'CounsellorStudentDBMS/StudentProfile.html',{'s': s, 'user': request.user.user_profile.p_type})

def EditStudentProfile(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        usn = request.user.username
        s = Student.objects.get(usn = usn)
        form = StudentUpdateForm(request.POST, instance=s)
        if form.is_valid():
            s = form.save()
            return HttpResponseRedirect(reverse('student_home'))
        else:
            msg = 'Invalid Form!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('EditStudentProfile'))
    else:
        usn = request.user.username
        s = Student.objects.get(usn=usn)
        form = StudentUpdateForm(instance = s)
        return render(request, 'CounsellorStudentDBMS/Sform.html', {'form':form, 'user':request.user.user_profile.p_type})

def counsEditStudDetails(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        s = Student.objects.get(usn = usn)
        form = SemSectCgpaForm(request.POST, instance=s)
        if form.is_valid():
            s = form.save()
            return HttpResponseRedirect(reverse('counsStudDetails', args= (usn,)))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('counsEditStudDetails', args= (usn, )))
    else:
        form = SemSectCgpaForm()
        return render(request, 'CounsellorStudentDBMS/Sform.html', {'form': form, 'user': request.user.user_profile.p_type})

def Reg_Details(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    reg = RegDetails.objects.filter(usn=request.user.username)
    return render(request, 'CounsellorStudentDBMS/RegDetails.html', {'reg': reg, 'user':request.user.user_profile.p_type})

def counsRegDetails(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    reg = RegDetails.objects.filter(usn_id= usn)
    return render(request, 'CounsellorStudentDBMS/RegDetails.html',
                  {'reg': reg, 'usn':usn,'user': request.user.user_profile.p_type})

class AddRegDetails(View):
    form_class = StudentRegDetailsForm
    template_name = 'CounsellorStudentDBMS/Sform.html'
    def get(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'user':request.user.user_profile.p_type})
    def post(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST)
        if form.is_valid():
            new_student_reg = form.save(commit=False)
            new_student_reg.usn_id = request.user.username
            new_student_reg.save()
            return HttpResponseRedirect(reverse('RegDetails'))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('RegDetails'))

def Scholarships(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    sc = Scholarship.objects.filter(usn= request.user.username)
    return render(request, 'CounsellorStudentDBMS/Scholarships.html', {'sc':sc, 'user':request.user.user_profile.p_type})

def counsScholarships(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    sc = Scholarship.objects.filter(usn= usn)
    return render(request, 'CounsellorStudentDBMS/Scholarships.html',
                  {'sc': sc,'usn':usn, 'user': request.user.user_profile.p_type})

class AddScholarshipDetails(View):
    form_class = StudentScholarshipForm
    template_name = 'CounsellorStudentDBMS/Sform.html'
    def get(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'user':request.user.user_profile.p_type})
    def post(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST)
        if form.is_valid():
            new_student_reg = form.save(commit=False)
            new_student_reg.usn_id = request.user.username
            new_student_reg.save()
            return HttpResponseRedirect(reverse('Scholarships'))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('AddScholarships'))

def Cocurr(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    cc = CoCurricular.objects.filter(usn= request.user.username)
    return render(request, 'CounsellorStudentDBMS/Cocurr.html', {'cc':cc, 'user': request.user.user_profile.p_type})

def counsCocurr(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    cc = CoCurricular.objects.filter(usn= usn)
    return render(request, 'CounsellorStudentDBMS/Cocurr.html', {'cc':cc, 'usn':usn,'user': request.user.user_profile.p_type})

def ParCocurr(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 3:
        msg = 'You are not a parent!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    p = Parent.objects.get(pid=request.user.username)
    cc = CoCurricular.objects.filter(usn= p.usn_id)
    return render(request, 'CounsellorStudentDBMS/Cocurr.html', {'cc':cc, 'user': request.user.user_profile.p_type})

class AddCocurr(View):
    form_class = CoCurrForm
    template_name = 'CounsellorStudentDBMS/certificates.html'
    def get(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_cert = form.save(commit=False)
            new_cert.usn_id = request.user.username
            new_cert.save()
            return HttpResponseRedirect(reverse('Cocurr'))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('AddCocurr'))

def grade(request, usn, certno):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        cocurr_cert = CoCurricular.objects.get(certno=certno, usn_id=usn)
        form = GradeCocurrForm(request.POST, instance=cocurr_cert)
        if form.is_valid():
            cocurr_cert = form.save()
            return HttpResponseRedirect(reverse('counsCocurr', args=(usn,)))
        else:
            msg = "Invalid form"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('grade', args=(usn,)))
    else:
        form = GradeCocurrForm()
        return render(request, 'CounsellorStudentDBMS/Sform.html', {'form':form, 'user':request.user.user_profile.p_type})

def report(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    students = StudentCourse.objects.filter(usn=request.user.username)
    return render(request, 'CounsellorStudentDBMS/student_report.html', {'students': students, 'user': request.user.user_profile.p_type})

def ParReport(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 3:
        msg = 'You are not a parent!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    p = Parent.objects.get(pid=request.user.username)
    students = StudentCourse.objects.filter(usn=p.usn_id)
    return render(request, 'CounsellorStudentDBMS/student_report.html', {'students': students, 'user': request.user.user_profile.p_type})

def counsReport(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    students = StudentCourse.objects.filter(usn=usn)
    return render(request, 'CounsellorStudentDBMS/student_report.html', {'students': students, 'usn': usn, 'user': request.user.user_profile.p_type})

def editmarks(request, usn, course_code):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        studCourse = StudentCourse.objects.get(course_code_id=course_code, usn_id=usn)
        form = MarksAttForm(request.POST, instance=studCourse)
        if form.is_valid():
            studCourse = form.save()
            return HttpResponseRedirect(reverse('counsReport', args=(usn, )))
        else:
            msg = "Invalid form"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('editmarks', args=(usn, course_code, )))
    else:
        studCourse = StudentCourse.objects.get(course_code_id=course_code, usn_id=usn)
        form = MarksAttForm(instance = studCourse)
        return render(request, 'CounsellorStudentDBMS/Sform.html', {'form':form, 'user': request.user.user_profile.p_type})

def Att(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student !'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    cc = CertImages.objects.filter(usn_id= request.user.username)
    return render(request, 'CounsellorStudentDBMS/Att.html', {'cc':cc, 'user': request.user.user_profile.p_type})

def counsAtt(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    cc = CertImages.objects.filter(usn_id= usn)
    return render(request, 'CounsellorStudentDBMS/Att.html', {'cc':cc, 'user': request.user.user_profile.p_type})

def AttCourses(request, certno):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    try:
        courses = CourseCert.objects.filter(usn_id=request.user.username, cert_no=certno)
    except CourseCert.DoesNotExist:
        return HttpResponseRedirect(reverse('AddAttCourses', args=(certno, )))
    return render(request, 'CounsellorStudentDBMS/AttCourses.html', {'courses': courses, 'certno':certno, 'user': request.user.user_profile.p_type})

def counsAttCourses(request, usn, certno):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    courses = CourseCert.objects.filter(usn_id=usn, cert_no=certno)
    return render(request, 'CounsellorStudentDBMS/AttCourses.html', {'courses': courses, 'user': request.user.user_profile.p_type})

class AddAttCourses(View):
    form_class = AttendanceCoursesForm
    template_name = 'CounsellorStudentDBMS/Sform.html'
    def get(self, request, certno):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'user':request.user.user_profile.p_type})
    def post(self, request, certno):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST)
        if form.is_valid():
            cc = form.data['course_code']
            try:
                enco = StudentCourse.objects.get(usn_id = request.user.username, course_code_id=cc)
            except StudentCourse.DoesNotExist:
                msg = "You are not enrolled to this course!"
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse('AttCourses', args=(certno,)))
            new_student_reg = form.save(commit=False)
            new_student_reg.usn_id = request.user.username
            new_student_reg.cert_no = certno
            cc = new_student_reg.course_code_id
            new_student_reg.save()
            return HttpResponseRedirect(reverse('AttCourses', args= (certno,)))
        else:
                msg = form.errors
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse('AddAttCourses', args= (certno,)))

class AddAtt(View):
    form_class = AttendanceImagesForm
    template_name = 'CounsellorStudentDBMS/certificates.html'
    def get(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
            msg = 'You are not a student!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_cert = form.save(commit=False)
            new_cert.usn_id = request.user.username
            new_cert.save()
            return HttpResponseRedirect(reverse('Att'))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('AddAtt'))

def CounsDetails(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 1:
        msg = 'You are not a student!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    usn = request.user.username
    s = Student.objects.get(usn=usn)
    c = counsellor.objects.get(cid = s.cid_id)
    return render(request, 'CounsellorStudentDBMS/CounsProfile.html', {'c': c, 'user':request.user.user_profile.p_type})

def ParCounsDetails(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 3:
        msg = 'You are not a parent!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    p = Parent.objects.get(pid=request.user.username)
    s = Student.objects.get(usn=p.usn_id)
    c = counsellor.objects.get(cid = s.cid)
    return render(request, 'CounsellorStudentDBMS/CounsProfile.html', {'c': c, 'user':request.user.user_profile.p_type})

def CounsProfile(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    c = counsellor.objects.get(cid = request.user.username)
    return render(request, 'CounsellorStudentDBMS/CounsProfile.html', {'c': c, 'user':request.user.user_profile.p_type})

def EditCounsProfile(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        s = counsellor.objects.get(cid = request.user.username)
        form = CounsUpdateForm(request.POST, instance=s)
        if form.is_valid():
            s = form.save()
            return HttpResponseRedirect(reverse('counsellor_page'))
        else:
            msg = "Invalid form"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('EditCounsProfile'))
    else:
        s = counsellor.objects.get(cid=request.user.username)
        form = CounsUpdateForm(instance =s)
        return render(request, 'CounsellorStudentDBMS/Sform.html', {'form':form, 'user':request.user.user_profile.p_type})

def counsStud(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    s = Student.objects.get(usn = usn)
    return  render(request, 'CounsellorStudentDBMS/counsStud.html', {'s' :s})

def counsParDetails(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    try:
        p = Parent.objects.get(usn_id = usn)
    except Parent.DoesNotExist:
        msg = 'Parent has not yet signed up'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('counsStud', args=(usn,)))
    return  render(request, 'CounsellorStudentDBMS/ParProfile.html', {'p' :p, 'user':request.user.user_profile.p_type})

def ParProfile(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 3:
        msg = 'You are not a parent!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    p = Parent.objects.get(pid= request.user.username)
    return  render(request, 'CounsellorStudentDBMS/ParProfile.html', {'p' :p , 'user':request.user.user_profile.p_type})

def EditParProfile(request):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 3:
        msg = 'You are not a parent!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        s = Parent.objects.get(pid=request.user.username)
        form = ParentUpdateForm(request.POST, instance=s)
        if form.is_valid():
            s = form.save()
            return HttpResponseRedirect(reverse('parent_page'))
        else:
            msg = "Invalid form"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('EditParProfile'))
    else:
        s = Parent.objects.get(pid=request.user.username)
        form = ParentUpdateForm(instance=s)
        return render(request, 'CounsellorStudentDBMS/Sform.html', {'form': form, 'user': request.user.user_profile.p_type})

def counsCourses(request, usn):
    if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    try:
        courses = StudentCourse.objects.filter(usn= usn)
    except StudentCourse.DoesNotExist:
        return HttpResponseRedirect(reverse('AddcounsCourses', args=(usn,)))
    return render(request, 'CounsellorStudentDBMS/counsCourses.html', {'courses':courses, 'usn':usn})

class AddcounsCourses(View):
    form_class = EnrolledCourseForm
    template_name = 'CounsellorStudentDBMS/Sform.html'
    def get(self, request, usn):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'user':request.user.user_profile.p_type})
    def post(self, request, usn):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST)
        if form.is_valid():
            new_student_reg = form.save(commit=False)
            new_student_reg.usn_id = usn
            new_student_reg.save()
            return HttpResponseRedirect(reverse('counsCourses', args = (usn,)))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('AddcounsCourses', args=(usn,)))

class reg_student(View):
    form_class = CounsRegStudent
    template_name = 'CounsellorStudentDBMS/Sform.html'
    def get(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'user':request.user.user_profile.p_type})
    def post(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST)
        if form.is_valid():
            new_stud =  form.save()
            new_stud.counsellor_id = request.user.username
            new_stud.save()
            usn = new_stud.usn
            msg ="Student has been registered!"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('reg_parent', args = (usn, )))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('reg_student'))

class reg_parent1(View):
    form_class = CounsRegParent
    template_name = 'CounsellorStudentDBMS/Sform.html'
    def get(self, request, usn):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'user': request.user.user_profile.p_type})
    def post(self, request, usn):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST)
        if form.is_valid():
            new_stud =  form.save(commit=False)
            stude = student_access.objects.get(usn = usn)
            new_stud.usn = stude
            new_stud.save()

            return HttpResponseRedirect(reverse('counsellor_page'))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('reg_parent', args=(usn, )))

class reg_parentxx(View):
    form_class = CounsRegParentxx
    template_name = 'CounsellorStudentDBMS/Sform.html'
    def get(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'user': request.user.user_profile.p_type})
    def post(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST)
        if form.is_valid():
            new_stud =  form.save()
            msg = "Parent has been registered!"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('counsellor_page'))
        else:
            msg = form.errors
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('reg_parentxx'))

def Notification(request):
    if not request.user.is_authenticated or (request.user.user_profile.p_type != 1 and request.user.user_profile.p_type != 3):
        msg = 'You are not a student or parent!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    if request.user.user_profile.p_type == 1:
        s = Student.objects.get(usn= request.user.username)
    else:
        s1 = Parent.objects.get(pid = request.user.username)
        s = Student.objects.get(usn = s1.usn_id)
    nn = Notifications.objects.filter(cid_id= s.cid_id).exclude(to = 4- request.user.user_profile.p_type)
    return render(request, 'CounsellorStudentDBMS/Notifications.html', {'nn':nn, 'user': request.user.user_profile.p_type})

def SendNoti(request):
    if not request.user.is_authenticated or (request.user.user_profile.p_type != 2):
        msg = 'You are not a counsellor!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('index'))
    nn = Notifications.objects.filter(cid_id= request.user.username)
    return render(request, 'CounsellorStudentDBMS/Notifications.html', {'nn':nn, 'user': request.user.user_profile.p_type})

class SendNoti1(View):
    form_class = NotiForm
    template_name = 'CounsellorStudentDBMS/Sform.html'
    def get(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'user': request.user.user_profile.p_type})
    def post(self, request):
        if not request.user.is_authenticated or request.user.user_profile.p_type != 2:
            msg = 'You are not a counsellor!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST)
        if form.is_valid():
            new_student_reg = form.save(commit=False)
            new_student_reg.cid_id = request.user.username
            new_student_reg.save()
            msg = "Notification is sent succesfully"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('SendNoti'))
        else:
            msg = 'Invalid Form!'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse('SendNoti'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
