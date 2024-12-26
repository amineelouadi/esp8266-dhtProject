from rest_framework import serializers
from .models import Device, Reading

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'device_id', 'name', 'location', 'is_active', 'created_at', 'updated_at']

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ['id', 'device', 'temperature', 'humidity', 'timestamp']