from django.db.models import fields
from rest_framework import serializers
from task.models import Videos

class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'