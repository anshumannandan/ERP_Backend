# Generated by Django 4.1.2 on 2022-11-09 18:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_student_dob_alter_student_class_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='assigntime',
            name='class_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.class'),
        ),
        migrations.AddField(
            model_name='assigntime',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.teacher'),
        ),
        migrations.AlterField(
            model_name='user',
            name='otp_created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 9, 18, 19, 54, 831931, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterUniqueTogether(
            name='assigntime',
            unique_together={('period', 'day', 'class_id'), ('period', 'day', 'teacher')},
        ),
        migrations.CreateModel(
            name='StudentAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_present', models.BooleanField(default=True)),
                ('classattendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.classattendance')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.subject')),
            ],
        ),
        migrations.AddField(
            model_name='classattendance',
            name='assign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.assigntime'),
        ),
    ]
