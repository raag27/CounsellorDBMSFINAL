# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-10 06:42
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CertImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert_no', models.IntegerField()),
                ('image', models.ImageField(upload_to='attendance_certis')),
            ],
        ),
        migrations.CreateModel(
            name='CoCurricular',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certno', models.IntegerField()),
                ('image', models.ImageField(upload_to='achievement_certis')),
                ('category', models.CharField(max_length=10)),
                ('Club', models.CharField(max_length=10)),
                ('Grade', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='counsellor',
            fields=[
                ('cid', models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect Format')])),
                ('Fname', models.CharField(max_length=20)),
                ('Mname', models.CharField(blank=True, max_length=20, null=True)),
                ('Lname', models.CharField(blank=True, max_length=20, null=True)),
                ('pno', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('house_no', models.CharField(blank=True, max_length=10, null=True)),
                ('street', models.CharField(blank=True, max_length=50, null=True)),
                ('Area', models.CharField(blank=True, max_length=20, null=True)),
                ('City', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only letters are allowed.')])),
                ('State', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only letters are allowed.')])),
                ('PinCode', models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
            ],
        ),
        migrations.CreateModel(
            name='counselor_table',
            fields=[
                ('cid', models.CharField(max_length=10, primary_key='true', serialize=False, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect Format')])),
                ('access_key', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_code', models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(7), django.core.validators.RegexValidator('^[0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]?', 'Incorrect Course code Format')])),
                ('name', models.CharField(max_length=20)),
                ('credits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseCert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert_no', models.IntegerField()),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('Slno', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('to', models.IntegerField(choices=[(1, 'student'), (3, 'parent'), (2, 'both')])),
                ('SentOn', models.DateTimeField(auto_now_add=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.counsellor')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('pid', models.CharField(max_length=11, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.RegexValidator('^[pP][0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect pid Format')])),
                ('Fname', models.CharField(max_length=20)),
                ('Mname', models.CharField(blank=True, max_length=20, null=True)),
                ('Lname', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('house_no', models.CharField(blank=True, max_length=10, null=True)),
                ('street', models.CharField(blank=True, max_length=50, null=True)),
                ('Area', models.CharField(blank=True, max_length=20, null=True)),
                ('City', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only letters are allowed.')])),
                ('State', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only letters are allowed.')])),
                ('PinCode', models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
            ],
        ),
        migrations.CreateModel(
            name='parent_access',
            fields=[
                ('pid', models.CharField(max_length=11, primary_key='true', serialize=False, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.RegexValidator('^[pP][0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect pid Format')])),
                ('access_key', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='RegDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('challan_no', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
                ('fees', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('name', models.CharField(max_length=20)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('usn', models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect Format')])),
                ('Fname', models.CharField(max_length=20)),
                ('Mname', models.CharField(blank=True, max_length=20, null=True)),
                ('Lname', models.CharField(blank=True, max_length=20, null=True)),
                ('pno', models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('sec', models.CharField(blank=True, max_length=2, null=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('sem', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('cgpa', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('house_no', models.CharField(blank=True, max_length=10, null=True)),
                ('street', models.CharField(blank=True, max_length=50, null=True)),
                ('Area', models.CharField(blank=True, max_length=20, null=True)),
                ('City', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only letters are allowed.')])),
                ('State', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only letters are allowed.')])),
                ('PinCode', models.CharField(blank=True, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.RegexValidator('^[0-9]*$', 'Only numbers are allowed.')])),
                ('cid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='CounsellorStudentDBMS.counsellor')),
            ],
        ),
        migrations.CreateModel(
            name='student_access',
            fields=[
                ('usn', models.CharField(max_length=10, primary_key='true', serialize=False, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect Format')])),
                ('access_key', models.CharField(max_length=30)),
                ('counsellor_id', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10), models.CharField(max_length=10, primary_key='true', serialize=False, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.RegexValidator('^[0-9][a-zA-Z][a-zA-Z][0-9][0-9][a-zA-Z][a-zA-Z][0-9][0-9][0-9]', 'Incorrect Format')])])),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_test1', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('m_test2', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('m_test3', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('m_lab', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('self_study', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('Assgn', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('LabInt', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('LabExt', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('SEE', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('a_test1', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('a_test2', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('a_test3', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('a_lab', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Course')),
                ('usn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_type', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='scholarship',
            name='usn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Student'),
        ),
        migrations.AddField(
            model_name='regdetails',
            name='usn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Student'),
        ),
        migrations.AddField(
            model_name='parent_access',
            name='usn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.student_access', unique=True),
        ),
        migrations.AddField(
            model_name='parent',
            name='usn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Student', unique=True),
        ),
        migrations.AddField(
            model_name='coursecert',
            name='usn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Student'),
        ),
        migrations.AddField(
            model_name='cocurricular',
            name='usn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Student'),
        ),
        migrations.AddField(
            model_name='certimages',
            name='usn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CounsellorStudentDBMS.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='studentcourse',
            unique_together=set([('usn', 'course_code')]),
        ),
        migrations.AlterUniqueTogether(
            name='scholarship',
            unique_together=set([('usn', 'year', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='regdetails',
            unique_together=set([('usn', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursecert',
            unique_together=set([('usn', 'course_code', 'cert_no')]),
        ),
        migrations.AlterUniqueTogether(
            name='cocurricular',
            unique_together=set([('usn', 'certno')]),
        ),
        migrations.AlterUniqueTogether(
            name='certimages',
            unique_together=set([('usn', 'cert_no')]),
        ),
    ]
