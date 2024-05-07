from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Article, Comment  # Article과 Comment 모델을 불러옵니다.
from django.contrib.auth import get_user_model
User = get_user_model()  # 현재 활성화된 사용자 모델을 가져옵니다.


# ArticleDetailAPIViewTest 클래스를 정의합니다.
class ArticleDetailAPIViewTest(TestCase):
    def setUp(self):  # 각 테스트 메서드가 실행되기 전에 실행되는 설정 메서드입니다.
        # 테스트에 필요한 초기 상태를 설정합니다.
        self.user = User.objects.create_user(
            username='testuser', password='12345')  # testuser라는 이름의 사용자를 생성합니다.
        self.client = APIClient()  # API 클라이언트를 생성합니다.
        self.client.force_authenticate(user=self.user)  # 클라이언트를 특정 사용자로 인증합니다.
        self.article = Article.objects.create(  # Article 모델의 인스턴스를 생성하여 테스트할 게시물을 만듭니다.
            title='Test Article', content='Test Content', author=self.user)

    def test_create_comment(self):  # 댓글 작성을 테스트하는 메서드입니다.
        url = reverse('articles:detail', kwargs={  # 'articles:detail' URL 패턴을 역으로 해석하여 URL을 생성합니다.
                      'article_id': self.article.id})

        data = {'content': 'Test Comment Content'}  # 댓글의 내용을 포함하는 데이터를 생성합니다.

        # 생성된 URL에 데이터를 전송하여 댓글을 작성합니다.
        response = self.client.post(url, data, format='json')
        # 응답의 상태 코드를 확인하여 요청이 성공적으로 처리되었는지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment = Comment.objects.last()  # Comment 모델에서 마지막 댓글을 가져옵니다.
        # 작성된 내용과 게시물, 작성자가 올바른지 확인합니다.
        self.assertEqual(comment.content, 'Test Comment Content')
        self.assertEqual(comment.article, self.article)
        self.assertEqual(comment.author, self.user)

    # 댓글의 내용이 빠진 경우를 테스트하는 메서드입니다.
    def test_create_comment_missing_content(self):
        url = reverse('articles:detail', kwargs={  # 'articles:detail' URL 패턴을 역으로 해석하여 URL을 생성합니다.
                      'article_id': self.article.id})

        data = {}  # 데이터에 내용이 빠진 경우를 표현하기 위해 빈 딕셔너리를 생성합니다.

        # 생성된 URL에 데이터를 전송하여 댓글을 작성합니다.
        response = self.client.post(url, data, format='json')
        # 응답의 상태 코드를 확인하여 요청이 실패하고 '400 Bad Request' 상태 코드를 반환하는지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentAPIViewTest(TestCase):
    def setUp(self):
        # 테스트를 위한 초기 설정
        self.user = User.objects.create_user(
            username='testuser', password='12345')  # 테스트용 유저 생성
        self.client = APIClient()  # 테스트용 클라이언트 생성
        self.client.force_authenticate(user=self.user)  # 인증된 유저로 설정
        self.article = Article.objects.create(
            title='Test Article', content='Test Content', author=self.user)  # 테스트용 게시물 생성
        self.comment = Comment.objects.create(
            content='Test Comment', author=self.user, article=self.article)  # 테스트용 댓글 생성

    def test_create_reply(self):
        # 답글 생성 테스트
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성
        data = {'content': 'Test Reply Content'}  # 생성할 답글 데이터

        response = self.client.post(
            url, data, format='json')  # POST 요청하여 답글 생성

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # 응답 코드 확인
        reply = Comment.objects.last()  # 가장 최근에 생성된 댓글 가져오기
        self.assertEqual(reply.content, 'Test Reply Content')  # 답글 내용 확인
        self.assertEqual(reply.parent_comment, self.comment)  # 부모 댓글 확인
        self.assertEqual(reply.author, self.user)  # 작성자 확인

    def test_create_reply_missing_content(self):
        # 댓글 생성 시 content가 없는 경우 테스트
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성
        data = {}  # content가 빠진 데이터

        response = self.client.post(
            url, data, format='json')  # POST 요청하여 답글 생성

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)  # 응답 코드 확인

    def test_update_comment(self):
        # 댓글 수정 테스트
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성
        data = {'content': 'Updated Test Comment'}  # 수정할 댓글 데이터

        response = self.client.put(url, data, format='json')  # PUT 요청하여 댓글 수정

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 응답 코드 확인
        self.comment.refresh_from_db()  # DB에서 댓글 다시 가져오기
        self.assertEqual(self.comment.content,
                         'Updated Test Comment')  # 댓글 내용 확인

    def test_update_missing_content(self):
        # 댓글 수정 시 content가 없는 경우 테스트
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성
        data = {}  # content가 빠진 데이터

        response = self.client.put(url, data, format='json')  # PUT 요청하여 댓글 수정

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)  # 응답 코드 확인

    def test_delete_comment(self):
        # 댓글 삭제 테스트
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성

        response = self.client.delete(url)  # DELETE 요청하여 댓글 삭제

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)  # 응답 코드 확인
        self.assertFalse(Comment.objects.filter(
            pk=self.comment.id).exists())  # 댓글이 삭제되었는지 확인

    def test_delete_comment_wrong_user(self):
        # 다른 유저가 댓글 삭제 시도 시 테스트
        another_user = User.objects.create_user(
            username='anotheruser', password='12345')  # 다른 유저 생성
        self.client.force_authenticate(user=another_user)  # 다른 유저로 인증 설정
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성

        response = self.client.delete(url)  # DELETE 요청하여 댓글 삭제

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)  # 응답 코드 확인
