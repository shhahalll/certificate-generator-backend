from rest_framework import serializers
from . models import List

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = "__all__"