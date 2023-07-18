from rest_framework import serializers
from .models import *


class ProfileSerializers(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Profile
        fields = ('id', 'role', 'team', 'national_code', 'phone_number', 'user', 'profile_image')



class TeamSerializers(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('name', 'num_of_member')


class PresentationSerializers(serializers.ModelSerializer):

    profile=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Presentation
        fields =('profile', 'end_time','description', 'start_time', 'date','is_updated')


class DurationSerializers(serializers.Serializer):

    duration = serializers.IntegerField()
    profile = serializers.CharField(max_length=100)

    def validate_duration(self):
        if self.duration < 0 or self.duration > 600:
            error = 'wrong value'
            raise serializers.ValidationError(error)
        return self.duration

