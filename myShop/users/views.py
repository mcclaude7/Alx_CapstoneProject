from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

# User Registration View
class UserRegistrationView(APIView):
    # Allow anyone to access the registration endpoint
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        # Check if the data is valid
        if serializer.is_valid():
            # Save the user (which will also create a profile)
            serializer.save()
            return Response(
                {
                    "message": "User created successfully!","user": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
