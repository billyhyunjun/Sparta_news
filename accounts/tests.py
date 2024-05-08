from .models import PasswordQuestion
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()  # 현재 활성화된 사용자 모델을 가져옵니다.


class AccountAPITest(TestCase):
    # 기본 셋팅
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin_user', email='admin@example.com', password='admin_password')

        # 암호 질문 생성
        self.password_question = PasswordQuestion.objects.create(
            question='What is your favorite color?')

        # 유저 생성
        self.user = User.objects.create_user(
            username='test_user', email='test@example.com', password='test_password', password_question_id=self.password_question.id, password_answer="Test Answer")

        # 모든 테스트에 사용할 사용자로 로그인
        self.client.force_authenticate(user=self.user)

    # 관리자로 로그인
    def test_create_password_question(self):
        self.client.force_authenticate(user=self.admin_user)

        # 유효한 질문을 포함하여 암호 질문 생성 (절대 경로로 수정)
        question_data = {'question': 'What is your favorite color?'}
        response = self.client.post('/api/accounts/password/', question_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 생성된 암호 질문이 데이터베이스에 있는지 확인
        created_question = PasswordQuestion.objects.get(
            question='What is your favorite color?')
        self.assertIsNotNone(created_question)

    # 비밀번호 변경 요청
    def test_change_password(self):
        change_data = {
            'password_question': self.password_question.id,
            'password_answer': 'Test Answer',
            'new_password': 'new_test_password',
            'confirm_password': 'new_test_password'
        }
        response = self.client.post(
            f'/api/accounts/profile/{self.user.id}/', change_data)

        # 변경 요청이 실패한 경우 오류 메시지 출력
        if response.status_code != status.HTTP_200_OK:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 프로필 업데이트 요청
    def test_profile_update(self):
        update_data = {'email': 'new_email@example.com'}
        response = self.client.put(
            f'/api/accounts/profile/{self.user.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 계정 삭제 요청
    def test_delete_account(self):
        response = self.client.delete(
            f'/api/accounts/profile/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
