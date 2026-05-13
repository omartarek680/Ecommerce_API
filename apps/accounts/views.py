from rest_framework.generics import  RetrieveUpdateAPIView, GenericAPIView, ListCreateAPIView
from django.contrib.auth import get_user_model, authenticate, logout
from .serializers import UserSerializer, LoginSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView

User = get_user_model()

class RegisterView(GenericAPIView):
    
    serializer_class = UserSerializer
    permission_classes = []
    def post(self, request):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh" : str(refresh),
            "access" : str(refresh.access_token),
            "user" : serializer.data

        }, status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = authenticate(request,email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)

            return Response({"message": "login success",
                             "refresh": str(refresh),
                             "access" : str(refresh.access_token),
                             "email" : user.email
                             }, status=status.HTTP_200_OK)

        return Response({"message" : "Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)



class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):

        return self.request.user
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        except TokenError:
            return Response({"detail": "Token is invalid or already blacklisted."}, status= status.HTTP_400_BAD_REQUEST)
        
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )
        



class UserList(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


