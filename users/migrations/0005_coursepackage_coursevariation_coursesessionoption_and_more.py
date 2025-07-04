# Generated by Django 5.2.2 on 2025-06-08 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_customuser_user'),
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
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coursepackage')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSessionOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meetings', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coursevariation')),
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
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coursepackage')),
            ],
        ),
    ]
