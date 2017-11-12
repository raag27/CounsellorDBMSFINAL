from django.contrib import admin
from .models import  Notifications, parent_access, Student,Course, UserProfile,counselor_table,counsellor,student_access,StudentCourse,CoCurricular,CertImages,CourseCert,Parent,RegDetails,Scholarship

# Register your models here.
admin.site.register(Notifications)
admin.site.register(parent_access)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(UserProfile)
admin.site.register(counselor_table)
admin.site.register(counsellor)
admin.site.register(student_access)
admin.site.register(StudentCourse)
admin.site.register(CoCurricular)
admin.site.register(CertImages)
admin.site.register(CourseCert)
admin.site.register(Parent)
admin.site.register(RegDetails)
admin.site.register(Scholarship)