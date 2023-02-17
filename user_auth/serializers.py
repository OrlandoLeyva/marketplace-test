from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')
        extra_kwargs = {
            'email': {
                'required': True,
                'validators': [UniqueValidator(User.objects.all())]
            },
            'password': {
                # 'validators': [validate_password],
                'write_only': True
            },
        }

    def create(self, validated_data):
        if not validated_data['password'] == validated_data['password2']:
            raise serializers.ValidationError('Passwords does not match')
        del validated_data['password2']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        # print(User.objects.values())
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            data['user'] = user
            return data
        else:
           raise serializers.ValidationError('The provided credentials were not correct')
