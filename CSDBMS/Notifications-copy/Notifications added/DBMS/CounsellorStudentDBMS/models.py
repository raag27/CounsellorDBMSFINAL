from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator,RegexValidator

# Create your models here.
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
usn = RegexValidator(r'^[0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect Format')
pusn = RegexValidator(r'^[pP][0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect pid Format')
course = RegexValidator(r'^[0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]?', 'Incorrect Course code Format')
numeric = RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')
alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile")
    p_type = models.IntegerField(default=0)

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])
            user_profile.save()

    post_save.connect(create_profile, sender=User)


class counselor_table(models.Model):
    cid = models.CharField(max_length=10, primary_key='true', validators=[MinLengthValidator(10),usn])
    access_key = models.CharField(max_length=30)

    def __str__(self):
        return self.cid


class counsellor(models.Model):
    cid = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10),usn])
    Fname = models.CharField(max_length=20,validators=[alpha])
    Mname = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    Lname = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    pno = models.CharField(max_length=10, validators=[MinLengthValidator(10),numeric], blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    house_no = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    Area = models.CharField(max_length=20, blank=True, null=True)
    City = models.CharField(max_length=20, blank=True, null=True, validators=[alpha])
    State = models.CharField(max_length=20, blank=True, null=True, validators=[alpha])
    PinCode = models.CharField(max_length=6, validators=[MinLengthValidator(6), numeric], blank=True, null=True)

    def __str__(self):
        return self.cid


class student_access(models.Model):
    usn = models.CharField(max_length=10, primary_key='true', validators=[MinLengthValidator(10),usn])
    access_key = models.CharField(max_length=30)
    counsellor_id = models.CharField(max_length=10, validators=[MinLengthValidator(10), usn])

    def __str__(self):
        return self.usn


class parent_access(models.Model):
    pid = models.CharField(max_length=11, primary_key='true', validators=[MinLengthValidator(11),pusn])
    access_key = models.CharField(max_length=30)
    usn = models.ForeignKey(student_access, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.pid


class Student(models.Model):
    usn = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10),usn])
    Fname = models.CharField(max_length=20,validators=[alpha])
    Mname = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    Lname = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    pno = models.CharField(max_length=10, validators=[MinLengthValidator(10),numeric], blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    sec = models.CharField(max_length=2, blank=True, null=True,validators=[alphanumeric])
    sem = models.IntegerField(blank=True, null=True,validators=[MinValueValidator(1),MaxValueValidator(8)])
    cgpa = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1, validators=[MaxValueValidator(10),MinValueValidator(0)])
    house_no = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    Area = models.CharField(max_length=20, blank=True, null=True)
    City = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    State = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    PinCode = models.CharField(max_length=6, validators=[MinLengthValidator(6),numeric], blank=True, null=True)
    cid = models.ForeignKey(counsellor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.usn


class RegDetails(models.Model):
    class Meta:
        unique_together = 'usn', 'year'

    usn = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    challan_no = models.CharField(max_length=10,validators=[numeric])
    fees = models.FloatField()

    def __str__(self):
        return '%s %s' % (self.usn, self.year)


class CoCurricular(models.Model):
    class Meta:
        unique_together = 'usn', 'certno'

    usn = models.ForeignKey(Student, on_delete=models.CASCADE)
    certno = models.IntegerField()
    image = models.ImageField(upload_to="achievement_certis")
    category = models.CharField(max_length=10)
    Club = models.CharField(max_length=10)
    Grade = models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1, validators=[MaxValueValidator(10),MinValueValidator(0)])

    def __str__(self):
        return '%s %s' % (self.usn, self.certno)


class Scholarship(models.Model):
    class Meta:
        unique_together = 'usn', 'year', 'name'

    usn = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    name = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return '%s %s %s' % (self.usn, self.year, self.name)


class Parent(models.Model):
    pid = models.CharField(max_length=11, primary_key=True, validators=[MinLengthValidator(11),pusn])
    usn = models.ForeignKey(Student, on_delete=models.CASCADE, unique=True)
    Fname = models.CharField(max_length=20,validators=[alpha])
    Mname = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    Lname = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(10),numeric], blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    house_no = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    Area = models.CharField(max_length=20, blank=True, null=True)
    City = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    State = models.CharField(max_length=20, blank=True, null=True,validators=[alpha])
    PinCode = models.CharField(max_length=6, validators=[MinLengthValidator(6),numeric], blank=True, null=True)

    def __str__(self):
        return self.pid


class Course(models.Model):
    course_code = models.CharField(max_length=10, primary_key=True,validators=[MinLengthValidator(6), MaxLengthValidator(7), course])
    name = models.CharField(max_length=20)
    credits = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.course_code


class StudentCourse(models.Model):
    class Meta:
        unique_together = 'usn', 'course_code'

    usn = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    m_test1 = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    m_test2 = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    m_test3 = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    m_lab = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    self_study = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    Assgn = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    LabInt = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    LabExt = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    SEE = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0)])
    a_test1 = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=1, validators=[MaxValueValidator(100),MinValueValidator(0)])
    a_test2 = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=1, validators=[MaxValueValidator(100),MinValueValidator(0)])
    a_test3 = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=1, validators=[MaxValueValidator(100),MinValueValidator(0)])
    a_lab = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=1, validators=[MaxValueValidator(100),MinValueValidator(0)])

    def __str__(self):
        return '%s %s' % (self.usn, self.course_code)


class CertImages(models.Model):
    class Meta:
        unique_together = 'usn', 'cert_no'

    usn = models.ForeignKey(Student, on_delete=models.CASCADE)
    cert_no = models.IntegerField()
    image = models.ImageField(upload_to="attendance_certis")

    def __str__(self):
        return '%s %s' % (self.usn, self.cert_no)


class CourseCert(models.Model):
    class Meta:
        unique_together = 'usn', 'course_code', 'cert_no'

    usn = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    cert_no = models.IntegerField()

    def __str__(self):
        return '%s %s %s' % (self.usn, self.cert_no, self.course_code)


class Notifications(models.Model):
    Slno = models.AutoField(primary_key=True)
    label = models.CharField(max_length=200)
    content = models.TextField()
    cid = models.ForeignKey(counsellor, on_delete=models.CASCADE)
    to = models.IntegerField(choices=((1, "student"), (3, "parent"), (2, "both")))
    SentOn = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.Slno)
