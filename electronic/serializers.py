from rest_framework import serializers
from .models import Product
from . decorators import unauthenticated_user
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes,permission_classes

from .models import Product



class ProductSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(max_length=None,allow_empty_file=True,allow_null=True,required=False)
    class Meta:
        model = Product
        fields = ('id','name','description','image')
    