from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class AccountAPIView(APIView):
    
    # 회원 가입
    def post(self, request):
        return Response({}, status=200)

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