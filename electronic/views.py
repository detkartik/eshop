from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset= Product.objects.all().order_by('name')
    serializer_class = ProductSerializer

    

