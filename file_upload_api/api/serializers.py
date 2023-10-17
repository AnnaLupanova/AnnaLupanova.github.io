from rest_framework import serializers
from .models import File


class SerializersFile(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('file', 'uploaded_at', 'processed')
