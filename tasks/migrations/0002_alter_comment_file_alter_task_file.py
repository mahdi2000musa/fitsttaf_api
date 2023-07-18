# Generated by Django 4.1.4 on 2023-02-04 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='comment_file/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='task_file/'),
        ),
    ]