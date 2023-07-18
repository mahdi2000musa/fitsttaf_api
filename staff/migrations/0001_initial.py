# Generated by Django 4.1.4 on 2023-01-21 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FE', 'Front_end'), ('BE', 'Back_end'), ('DS', 'Data_science'), ('DO', 'Dev_ops'), ('MA', 'Marketing'), ('SU', 'Support'), ('MG', 'Managers')], max_length=50)),
                ('num_of_member', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('T', 'Team_leader'), ('S', 'Senior'), ('J', 'Junior'), ('I', 'Intern_ship')], max_length=30)),
                ('phone_number', models.CharField(default='', max_length=11)),
                ('national_code', models.CharField(max_length=10)),
                ('profile_image', models.ImageField(null=True, upload_to='profiles/')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff.team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]