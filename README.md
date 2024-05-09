# Sparta_news [잠궈]
[2024.05.10] 심화프로젝트 : Django DRF를 활용, API 뉴스 사이트를 구현하라

### :calendar: **개발기간**
- 2024.05.03 ~ 2024/05.10 (5일)

### 포지션
- 박현준 : accounts, 영상제작, 총괄
- 박우영 : accounts, article, 발표
- 홍순호 : article, S.A.
- 용석민 : article, readme

### 적용기술
- Programming Language : Python 3.12.3
- Web Framework : Django DRF
- DB : SQLite
- etc. : Github

## 프로젝트 특징
1. __Account__
   - 회원가입, 로그인, 로그아웃, 프로필 수정 기본 기능 구현
   - 비밀번호 찾기는 나만의 암호 답변문으로 가능
   - 로그인 여부를 체크하여 접근 가능한 영역을 제한
2. __Article__
   - 게시글 조회는 로그인 여부 체크 없이 조회, 나머지 기능은 로그인 여부 체크 필요 
   - 게시물 전체보기, 상세보기 검색, 작성, 수정, 삭제 기본 기능 구현
   - 게시물 추천, 즐겨찾기 가능
3. __Comment__
   - 댓글 관련 기능은 로그인 여부 체크 필요
   - 댓글 작성, 수정, 삭제 기본 기능 구현
   - 댓글에 댓글을 추가로 작성 가능
4. __Features__
   - 추천(좋아요)기능은 공개된 정보로 조회 가능
   - 즐겨찾기(북마크)기능은 비공개된 정보로 나만 조회 가능

## ERD
![image](https://github.com/billyhyunjun/Sparta_news/assets/160443825/2b99e306-a86c-4400-a698-125b775047ed)


