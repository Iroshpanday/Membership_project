from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer # aghi hamla banako userregistrationwala serializer connect hunxa ra usre hunxa

    permission_classes = [permissions.AllowAny] # unauthorised user lah pani yo view acess garna milxa


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # authorized user only can acess it
    
    def get_object(self):
        return self.request.user    