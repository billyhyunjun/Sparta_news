from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password
from .models import PasswordQuestion

# Create your views here.


class AccountAPIView(APIView):

    # 회원 가입
    def post(self, request):
        return Response({}, status=200)


class AccountDetailAPIView(APIView):
    # 로그인상태
    permission_classes = [IsAuthenticated]

    def get_user(self, user_id):
        return get_object_or_404(get_user_model(), pk=user_id)

    # 프로필 조회
    def get(self, request, user_id):
        # 1. get user
        user = self.get_user(user_id)
        # 2. serializer userdata
        serializer = UserSerializer(user)
        # 3. return user using serializer
        return Response(serializer.data, status=200)

    # 비밀번호 찾기
    def post(self, request, user_id):
        # 1. get user
        user = self.get_user(user_id)

        # 2. check if request user is the same as the user
        if request.user != user:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # 3. get password_question
        password_question = request.data.get("password_question")

        # 4. Verify with user data
        if password_question == user.password_question:
            return Response({"password": user.password}, status=status.HTTP_200_OK)
        else:
            return Response({"Message": "wrong password_question"}, status=status.HTTP_400_BAD_REQUEST)

    # 프로필 수정
    def put(self, request, user_id):
        # 1. get user
        user = self.get_user(user_id)
        
        # 2. check if request user is the same as the user
        if request.user != user:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        # 3. Verify with data
        email = request.data.get("email")
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if email:
            user.email = email

        # 현재 비밀번호 확인
        if not check_password(current_password, user.password):
            return Response({"Error": "Incorrect current password"}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 비밀번호와 기존 비밀번호 확인
        if new_password == current_password:
            return Response({"Error": "New password and current_password match"}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 비밀번호와 확인용 비밀번호 일치 여부 확인
        if new_password != confirm_password:
            return Response({"Error": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # save data
        user.set_password(new_password) # 새로운 비밀번호 설정
        user.save()


        return Response({"Message": "User account delete successfully"}, status=status.HTTP_200_OK)

    # 회원 탈퇴
    def delete(self, request, user_id):
        # 1. get user
        user = self.get_user(user_id)

        # 2. check if request user is the same as the user
        if request.user != user:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # 3. delete user account
        user.delete()
        return Response({"Message": "User account delete successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])  # POST입력만 받기
@permission_classes([IsAuthenticated])  # 지금 로그인 중인지
def create_password(request):
    # 암호문 생성
    question = request.data.get("question")
    if not question:
        return Response({"error": "question is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    question, _ = PasswordQuestion.objects.get_or_create(question=question)
    return Response({"id": question.id, "question": question.question}, status=status.HTTP_200_OK)
