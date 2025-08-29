from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.core.commands import RegisterUserCommand
from users.services.user_services import UserService
from users.adapters.repository import DjangoUserRepository

repo = DjangoUserRepository()
service = UserService(repo)


class RegisterUserView(APIView):
    def post(self, request):
        cmd = RegisterUserCommand(
            email=request.data.get("email"), password=request.data.get("password")
        )
        try:
            user = service.register(cmd)
            return Response(
                {"id": user.id, "email": user.email}, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AuthenticateUserView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = service.authenticate(email, password)
            return Response(
                {"id": user.id, "email": user.email}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
