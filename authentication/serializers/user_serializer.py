from rest_framework import serializers
from authentication.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(required=True, write_only=True)
    passwordConfirm = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'first_name',
            'last_name',
            'password',
            'passwordConfirm',
            'created_at',
            'updated_at',
        )
    
    def validate(self, data):
        if not data['email'] or data['email'] == '':
            raise serializers.ValidationError('Email cannot be empty')
        if data['password'] != data['passwordConfirm']:
            raise serializers.ValidationError('Passwords do not match')
        return data
    
    def create(self, validated_data):
        try:
            user = User(
                email=validated_data['email'],
                nickname=validated_data['nickname'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
    
class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )
    
    def validate(self, data):
        if not data['email'] or data['email'] == '':
            raise serializers.ValidationError('Email cannot be empty')
        if not data['password'] or data['password'] == '':
            raise serializers.ValidationError('Password cannot be empty')
        return data
    
        
    
