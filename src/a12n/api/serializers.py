# Create your DRF serializers here
# https://www.django-rest-framework.org/tutorial/1-serialization/#creating-a-serializer-class
from rest_framework import serializers


# TODO complete swagger for jwt
class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
