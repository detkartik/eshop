from json import loads
from copy import deepcopy
from django.db.models import Q
from django.db import transaction
from .models import Vender
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, filters, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_text, force_bytes
from django.utils.http import is_safe_url, urlsafe_base64_decode, urlsafe_base64_encode


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    model = serializer_class.Meta.model
    queryset = Vender.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('id', 'user__username', 'user__email')
    lookup_field = 'id'
    ordering_fields = '__all__'
    ordering = ('-id',)
    
    def retrieve(self, request, id):
        try:
            vender = self.model.objects.get(id=id)
            data = UserSerializer(vender).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def update(self, request, id):
        req_data = request
        user = req_data.get('user')
        vender = Vender.objects.get(user=user)
        old_data = deepcopy(self.serializer_class(vender).data)
        req_data = dict(request.data)
        user_data = req_data.get('user')
        if req_data.get('user'):
            if vender.user:
                user = req_data.pop('user')
                # user= User.objects.filter(username=user['username'])[0].id
                userserializer = UserSerializer(vender.user, data=user, context = {'request' : request})
                if userserializer.is_valid():
                    userserializer.save()
                    req_data['user'] = user
            else:
                try:
                    user = self.userupdate(req_data)
                except Exception as e:
                    return Response({'status': 'error', 'response': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            req_data['name'] = user_data.get('first_name') + ' ' + user_data.get('last_name')

        serializer = UserSerializer(
            vender, data=req_data, partial=True, context={'request': request, 'old_data':old_data})
        if serializer.is_valid():
            serializer.save(force_update=True)
            return Response({'status': 'ok', 'id': id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)