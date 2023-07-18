from rest_framework import serializers
from .models import *
from staff.serializers import ProfileSerializers


class TaskSerializer(serializers.ModelSerializer):

    assigner = ProfileSerializers(read_only=True)
    assigner_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Profile.objects.all(), source='assigner')
    participant = ProfileSerializers(read_only=True)
    participant_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Profile.objects.all(), source='participant')

    class Meta:
        model = Task
        fields = ('id','subject',  'description', 'file', 'status', 'participant','participant_id' ,'created_at', 'updated_at', 'assigner_id', 'assigner')

    def validate_subject(self, value):
        if not value:
            raise serializers.ValidationError('Subject can\'t be null')
        return value


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', 'profile', 'file', 'task')