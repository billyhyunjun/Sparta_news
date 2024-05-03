from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

# Create your views here.
class AccountAPIView(APIView):
    
    # 회원 가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']

            # username과 email 중복 체크
            if User.objects.filter(username=username).exists():
                return Response({"error": "이미 사용 중인 이름"}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({"error": "이미 사용 중인 이메"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            refresh_token = RefreshToken.for_user(user)
            data = {
                'user_id': user.id,
                'access_token': str(refresh_token.access_token),
                'refresh_token': str(refresh_token)
            }
            
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "아이디 및 비밀번호가 틀림?"}, status=status.HTTP_400_BAD_REQUEST)

class AccountDetailAPIView(APIView):
    # 로그인상태
    permission_classes = [IsAuthenticated]
    
    # 프로필 조회
    def get(self, request):
        return Response({}, status=200)   
    
    # 비밀번호 찾기
    def post(self, request):
        return Response({}, status=200)   
    
    # 프로필 수정
    def put(self, request):
        return Response({}, status=200)  
    
    # 회원 탈퇴
    def delete(self, request):
        return Response({}, status=200)   


@api_view(["POST"])  # put입력만 받기
@permission_classes([IsAuthenticated])  # 지금 로그인 중인지
def create_password(request):
    # 암호문 생성 
    pass