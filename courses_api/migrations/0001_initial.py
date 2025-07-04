# Generated by Django 5.2.2 on 2025-06-08 16:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transmission', models.CharField(max_length=50)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses_api.coursepackage')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSessionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meetings', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses_api.coursevariation')),
            ],
        ),
        migrations.CreateModel(
            name='EnrolledCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255)),
                ('package_type_display', models.CharField(max_length=50)),
                ('transmission_display', models.CharField(max_length=10)),
                ('total_meetings', models.PositiveIntegerField()),
                ('price_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FlexibleCourseOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meetings', models.IntegerField()),
                ('price_manual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_matic', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses_api.coursepackage')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_number', models.PositiveIntegerField()),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('enrolled_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='courses_api.enrolledcourse')),
            ],
            options={
                'ordering': ['session_number'],
                'unique_together': {('enrolled_course', 'session_number')},
            },
        ),
    ]
