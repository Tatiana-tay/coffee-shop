# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.authtoken.models import Token
# from user_app.api.serializers import LoginSerializer


# class LoginView(APIView):
#     permission_classes = [AllowAny]  # open endpoint

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']

#             # Delete old token if it exists
#             Token.objects.filter(user=user).delete()

#             # Create a new token
#             token = Token.objects.create(user=user)

#             return Response({
#                 "token": token.key,
#                 "username": user.username,
#             })

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # Delete the current token
#         Token.objects.filter(user=request.user).delete()
#         return Response({"detail": "Successfully logged out."})