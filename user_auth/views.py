from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics,status, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.create(serializer.validated_data)
        token = Token.objects.create(user=user).key
        return Response({'user': user.username, 'token': token})
    
@api_view(http_method_names=('POST',))
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    user = serializer.create(serializer.validated_data)
    token = Token.objects.create(user=user)
    token.save()
    return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(http_method_names=('POST',))
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
    # token.save()
    return Response({'message': 'successful login', 'token': token.key}, status=status.HTTP_201_CREATED)

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)