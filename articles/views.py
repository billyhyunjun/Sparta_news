from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Article, Comment
from rest_framework.permissions import IsAuthenticated
from .serializers import ArticleSerializer
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer



class ArticleAPIView(APIView):
    # 게시물 전체 조회
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   
    


    def post(self, request):
        # 로그인 여부 확인
        if not request.user.is_authenticated:
            return Response({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 클라이언트로부터 데이터 받기
        data = request.data
        
        # Serializer를 사용하여 유효성 검사 및 데이터 저장
        serializer = ArticleSerializer(data=data)
        
        # 필수 요소 확인
        required_fields = ["title", "url", "content"]
        if not all(field in data for field in required_fields):
            return Response({"error": "필수 요소가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(author=request.user)  # 현재 로그인한 사용자를 작성자로 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticleDetailAPIView(APIView):


    # 게시물 상세 조회
    def get(self, request, article_id):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
    # 게시물 수정
    def put(self, request, article_id):
        # 로그인 여부 확인
        if not request.user.is_authenticated:
            return Response({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 게시물 존재 여부 확인
        article = get_object_or_404(Article, pk=article_id)

        # 프로필 유저와 로그인 유저가 일치하는지 확인
        if request.user != article.author:
            return Response({"error": "게시물 수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        # 클라이언트로부터 데이터 받기
        data = request.data

        # Serializer를 사용하여 유효성 검사 및 데이터 수정
        serializer = ArticleSerializer(article, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 게시물 삭제
    def delete(self, request, article_id):
        # 로그인 여부 확인
        if not request.user.is_authenticated:
            return Response({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 게시물 존재 여부 확인
        article = get_object_or_404(Article, pk=article_id)

        # 프로필 유저와 로그인 유저가 일치하는지 확인
        if request.user != article.author:
            return Response({"error": "게시물 삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        article.delete()
        return Response({"message": "게시물이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
    

    # 댓글 생성
    def post(self, request, article_id):
      
        # 로그인 여부 확인
        if not request.user.is_authenticated:
            return Response({"error": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
      
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
            "article": comment.article.id,
            "author": comment.author.id,
            "content": comment.content,
        }, status=status.HTTP_201_CREATED)


class CommentAPIView(APIView):

    # 로그인상태
    permission_classes = [IsAuthenticated]

    def get_comment(self, comment_id):
        return get_object_or_404(Comment, pk=comment_id)

    # 대댓글 작성
    def post(self, request, comment_id):
        comment = self.get_comment(comment_id)
        content = request.data.get("content")
        
        if content is None:
            return Response({"error": "content is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            content=content,
            parent_comment=comment,
            author=request.user,
        )
        return Response({
            "id": comment.id,
            "parent_comment": comment.parent_comment.id,
            "author": comment.author.id,
            "content": comment.content,
        }, status=status.HTTP_201_CREATED)

    # 댓글 수정
    def put(self, request, comment_id):
        comment = self.get_comment(comment_id)
        content = request.data.get("content")


        if content is None:
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


class SearchAPIView(APIView):

    # 로그인상태
    permission_classes = [IsAuthenticated]

    # 게시물 검색
    def get(self, request):
        query = request.query_parms.get('q')
        if query:
            articles = Article.objects.filter(
                title__icontains=query) | Article.objects.filter(content__icontains=query)
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "검색어를 입려갛세요."}, status=status.HTTP_400_BAD_REQUEST)
