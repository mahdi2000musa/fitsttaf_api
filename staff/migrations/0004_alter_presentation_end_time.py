# Generated by Django 4.1.5 on 2023-01-30 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_presentation_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
