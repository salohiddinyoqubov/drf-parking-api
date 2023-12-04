from coreapi.compat import force_text
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import User
from user.serializers import RegisterSerializer, MyTokenObtainPairSerializer, ProfileSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.core.mail import send_mail
from django.urls import reverse


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


class PasswordResetView(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # Generate token and send password reset email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_link = request.build_absolute_uri(reset_url)

            send_mail(
                'Password Reset',
                f'Use the following link to reset your password: {reset_link}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'success': 'Password reset link sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(generics.GenericAPIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            if new_password:
                try:
                    user.set_password(new_password)
                    user.save()
                    return Response({'success': 'Password has been reset!'}, status=400)
                except ValidationError as e:
                    # Password validation failed, format error messages and return a 400 Bad Request response
                    error_messages = list(e.messages)
                    return Response({'valid': False, 'errors': error_messages}, status=400)
            else:
                return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
