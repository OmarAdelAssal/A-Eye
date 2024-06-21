from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5, required=True)
    # serializer for Customer model
    class Meta:
        model = Customer
        fields =[
            "id",
            "name",
            "email",
            "password",
            "gender",
            "birthdate",
            "address",
            "image",
            "date_joined",
        ]
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        """
        Encrypt password
        """

        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance