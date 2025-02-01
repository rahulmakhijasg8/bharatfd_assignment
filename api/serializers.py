from rest_framework import serializers
from .models import FAQ


class FAQserializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']
