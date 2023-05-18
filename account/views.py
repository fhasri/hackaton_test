from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 
from rest_framework.permissions import IsAuthenticated 


from .permissions import IsActivePermissions
from .serializers import RegistrationSerializer , ActivationSerializer, LoginSerializer , ChangePasswordSerializer , ForgotPasswordSerializer , ForgotPasswordCompleteSerializer

# from .permissions import isActivePermission
# from .serializers import RegistrationSerializer, LoginSerializer, ActivationSealizer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordComplateSerializer

class RegistrationView(APIView):
    def post(self, request):
        serilizer = RegistrationSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        return Response('Аккаунт успешно создан', status=200)
  

class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.activate()
        return Response('Аккаунт успещно акивирован', status=200)

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer 



class LogoutView(APIView):
    permission_classes = [IsActivePermissions]
    def post(self, request):
        user = request.user 
        Token.objects.filter(user = user).delete()
        return Response('You have loged out from your account' )
    

class ChangePasswordView(APIView):
    permission_classes = [IsActivePermissions]
    def post(self, request):
        serializer = ChangePasswordSerializer( data = request.data, context ={'request': request})  # What is context?
        if serializer.is_valid(raise_exception = True):
            serializer.set_new_password()
        return Response('Status: 200. Password changes seccesfully!')
        


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.send_verification_email()
            return Response('Code sent to your email address! ')


        
class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.set_new_password()
            return Response('Password has been changed seccesfully! ')
        