from rest_framework import serializers
from .models import User, Project, Proposal
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str, force_str,force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_freelancer', 'is_client']

class ProjectSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'budget', 'client','department']

class ProposalSerializer(serializers.ModelSerializer):
    freelancer = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = Proposal
        fields = ['id', 'project', 'freelancer', 'bid_amount', 'description']


class CreateProposalSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Proposal
        fields = ['id', 'project', 'freelancer', 'bid_amount', 'description']



'''
Config setting.py
PASSWORD_RESET_TIMEOUT : 900 (15 MINUTES)
'''
class Useremailpassword(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields  = ['email']

    def validate(self, attrs):
        email = attrs.get('email')  
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('encode data', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('email password token', token)
            link = 'http://127.0.0.1:8000/set-new-password/'+uid+'/'+token 
            print('password reset email link', link)
            return attrs

        else:
            raise ValidationError('You are not registered user')

class ResetPassword(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, data):
        try:
            pas1 = data.get('password')
            pas2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if pas1 != pas2:
                return serializers.ValidationError('password does not match')
            # xid = force_str(urlsafe_base64_decode(uid))
            xid = smart_str(urlsafe_base64_decode(uid))

            user = User.objects.get(id=xid)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is not alive')
            user.set_password(pas1)
            user.save()
            # return user
            return data
        except DjangoUnicodeDecodeError as identifear:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Currently token is not a Alive')
            
class ChangePassword(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, data):
        pas1 = data.get('password')
        pas2 = data.get('password2')
        user = self.context.get('user')
        if pas1 != pas2:
            return serializers.ValidationError('password does not match')
        user.set_password(pas1)
        user.save()
        # return user
        return data


class UserregisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'is_freelancer','is_client','password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        p1 = data.get('password')
        p2 = data.get('password2')
        if p1 != p2:
            raise serializers.ValidationError('Password & confirm password do not match')
        return data

    def create(self, validated_data):
        # Remove the password2 field from validated_data as it's not needed for user creation
        validated_data.pop('password2', None)
        
        # Create the user with the remaining validated_data
        return User.objects.create_user(**validated_data)


class UserloginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['username','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username']
