from django.contrib import admin
from .models import *

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_of_member')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'team', 'national_code', 'phone_number')

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'start_time', 'end_time', 'date')
