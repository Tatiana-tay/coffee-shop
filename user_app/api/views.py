from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer

class LoginView(APIView):
    authentication_classes = []  # no auth required to log in
    permission_classes = []      # open endpoint

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "username": user.username,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
