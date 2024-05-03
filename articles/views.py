from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Article, Comment


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
    
    # 댓글 생성
    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        content = request.data.get("content")

        if not content:
            return Response({"error": "content is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            content=content,
            article=article,
            author=request.user,
        )
        return Response({
            "id": comment.id,
            "article": comment.article,
            "author": comment.author,
            "content": comment.content,
        }, status=status.HTTP_201_CREATED)


class CommentAPIView(APIView):

    # 로그인상태
    permission_classes = [IsAuthenticated]

    def get_comment(self, comment_id):
        return get_object_or_404(Comment, pk=comment_id)

    # 댓글 수정
    def put(self, request, comment_id):
        comment = self.get_comment(comment_id)
        content = request.data.get("content")
        
        if not comment:
            return Response({"error": "content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        comment.content = content
        comment.save()
        
        return Response({"Message": "comment updata successfully"}, status=status.HTTP_200_OK)

    # 댓글 삭제
    def delete(self, request, comment_id):
        
        comment = self.get_comment(comment_id)
        
        if request.user != comment.author:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        
        return Response({"Message": "comment delete successfully"}, status=status.HTTP_204_NO_CONTENT)

