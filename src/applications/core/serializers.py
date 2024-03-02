from rest_framework import serializers
from core.models import User
import pandas as pd

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username')


class UserCSVSerializer(serializers.Serializer):
    csv_file = serializers.FileField(write_only=True)

    def validate_csv_file(self, value):
        if value.size == 0:
            raise serializers.ValidationError("The uploaded file is empty")

        return value
    

class CSVSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'