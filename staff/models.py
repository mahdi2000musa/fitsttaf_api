from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Team(models.Model):
    NAME_CHOISES = (
        ('FE', 'Front_end'),
        ('BE', 'Back_end'),
        ('DS', 'Data_science'),
        ('DO', 'Dev_ops'),
        ('MA', 'Marketing'),
        ('SU', 'Support'),
        ('MG', 'Managers'),
    )

    name = models.CharField(max_length = 50, choices=NAME_CHOISES, null=False, blank=False)
    num_of_member = models.SmallIntegerField(default=1)


    def __str__(self):
        return f'{self.name}team, {self.num_of_member} member'


class Profile(models.Model):
    ROLE_CHOISES = (
        ('T', 'Team_leader'),
        ('S','Senior' ),
        ('J','Junior' ),
        ('I', 'Intern_ship'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length = 30, choices=ROLE_CHOISES)
    phone_number = models.CharField(max_length=11, default='')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    national_code = models.CharField(max_length=10, null = False, blank=False)
    profile_image = models.ImageField(upload_to='profiles/', null=True)



    def __str__(self):
        full_name = self.user.get_full_name() # concate first name and last name
        return f'{full_name} in team {self.team.name}'

    def save(self):
        super().save()

        img = Image.open(self.profile_image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.profile_image.path)


class Presentation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    is_updated = models.BooleanField(default=False)

    @property
    def present_time(self):
        start_hour = self.start_time.hour
        start_min = self.start_time.minute
        end_hour = self.end_time.hour
        end_min = self.end_time.minute
        duration = 0
        if end_min > start_min:
            duration += (end_min - start_min)
        else :
            duration += (start_min - end_min)
        
        duration += ((end_hour - start_hour)*60)

        return duration