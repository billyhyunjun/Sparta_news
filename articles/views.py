from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class ArticleAPIView(APIView):
    
    # 게시물 전체 조회
    def get(self, request):
        return Response({}, status=200)   
    
    # 게시물 생성
    @permission_classes([IsAuthenticated])  # 지금 로그인 중인지
    def post(self, request):
        return Response({}, status=200)   

class ArticleDetailAPIView(APIView):
    
    # 로그인상태
    permission_classes = [IsAuthenticated]
    
    # 게시물 상세 조회
    def get(self, request):
        return Response({}, status=200)  
    
    # 게시물 수정
    def put(self, request):
        return Response({}, status=200)  
    
    # 게시물 삭제
    def delete(self, request):
        return Response({}, status=200) 

class CommentAPIView(APIView):
    
    # 로그인상태
    permission_classes = [IsAuthenticated]
    
    # 댓글 생성
    def post(self, request):
        return Response({}, status=200)   
    
    # 댓글 수정
    def put(self, request):
        return Response({}, status=200)  
     
    # 댓글 삭제
    def delete(self, request):
        return Response({}, status=200) 
