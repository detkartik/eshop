from rest_framework import serializers
from electronic.decorators import unauthenticated_user
from .models import Vender
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance,attr,value)

        instance.save()
        return instance

    class Meta:
        model = User
        extra_kwargs = {'password':{'write_only':True}}
        fields = ('id','email','password')

class CustomRegisterSerializer(RegisterSerializer):

    class Meta:
        model = User
        fields = ('email', 'email', 'password')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        Vender.objects.create(user=user)
        return user


