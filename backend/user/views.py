from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserLoginSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bidding.models import Teams

class UserRegistrationView(APIView):
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        
        if user is not None:
            django_login(request, user)
            refresh = RefreshToken.for_user(user)
            obj = {
                    "message": "User logged in successfully.",
                    "role":user.role,
                    'username':user.username,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            
            if user.role == 'team':
                team = Teams.objects.get(user_id=user.id)
                obj['team'] = team.id
                
            return Response(obj, status=status.HTTP_200_OK )
        else:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

