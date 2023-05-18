from rest_framework import serializers
from django.contrib.auth import get_user_model , authenticate
from .utils import send_activation_code
from django.core.mail import send_mail

User = get_user_model()

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required= True)
    password = serializers.CharField(min_length = 4, required = True)
    password_confirm = serializers.CharField(min_length = 4 ,required = True)
    name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = False)


    def validate_email(self, email):
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError(' User with this email addres already exists!')
        return email
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm: 
            raise serializers.ValidationError(
                'Password is not matches'
            )
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code() 
        send_activation_code(user.email, user.activation_code)
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')

        if not User.objects.filter(email = email , activation_code = code).exists():
            raise serializers.ValidationError(

                'User not found!'
            )
        return attrs
    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email = email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate_email(self, email):
        if not User.objects.filter(email = email).exists():
            raise serializers.ValidationError(
                'No user with this email!'
            )
        return email
    
    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(
                username= email,
                password = password,
                request= request
                 )
            if not user:
                raise serializers.ValidationError(
                    'Not valid email or password!'
                )
        else:
            raise serializers.ValidationError
        (
                'Email and password is required! '
            
            )
            
        data['user'] = user 
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length = 4, required = True)
    new_password = serializers.CharField(min_length = 4, required = True)
    new_password_conf = serializers.CharField(min_length = 4 , required = True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                'not correct '
            )
        return old_password


    
    def validate(self, data):
        old_pass = data.get('old_password')
        new_pass1 = data.get('new_password')
        new_pass2 = data.get('new_password_conf')
    
        if new_pass1 != new_pass2:
            raise serializers.ValidationError(
                'Password is not matchin!'
            )
        if old_pass == new_pass1:
            raise serializers.ValidationError(
                'This pass used before!'
            )
        return data
    
    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required =True)
    # code = serializers.CharField()

    def validate_email(self, email):
        if not User.objects.filter(email = email).exists():
            raise serializers.ValidationError(' User with this email addres does not exist exists!')
        return email
    
    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email = email)
        user.create_activation_code()
        send_mail(
            'Password recovery,',f'Verification code {user.activation_code}', 'test@gmail.com',[user.email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()
    password = serializers.CharField(min_length = 4, required = True)
    password_confirm = serializers.CharField(min_length = 4 ,required = True)  

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        password1 = attrs.get('password')
        password2= attrs.pop('password_confirm')


        if not User.objects.filter(email = email, activation_code= code).exists():
            raise serializers.ValidationError(

                'User not found!'
            )



        if password1 != password2:
            raise serializers.ValidationError(
                'Passwords are not matching!'
            )
        return attrs
    
    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email = email)
        user.activation_code('')
        user.save()



    




    


    
    