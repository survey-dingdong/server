# dingdong-survey
> 연구자와 참여자를 손쉽게 연결하는 실험-인터뷰 중개 플랫폼

## 프로젝트 개요

본 프로젝트는 연구자와 실험 참여자를 손쉽게 연결하는 실험-인터뷰 중개 플랫폼입니다. 연구자는 실험을 등록하고 참여자를 모집할 수 있으며, 참여자는 실험 정보를 확인하고 예약을 진행할 수 있습니다. 또한, 연구자와 참여자가 직접 1:1 채팅을 통해 소통할 수 있는 기능을 제공합니다.

## 주요 기능

- **계정 관리**: 회원 가입, 로그인, 프로필 수정, 비밀번호 재설정
- **실험 관리**: 연구자의 실험 생성, 수정, 삭제, 참여자 관리
- **참여자 관리**: 참여자의 실험 목록 조회, 예약, 취소
- **채팅 기능**: 연구자와 참여자 간의 1:1 실시간 채팅
- **알림 시스템**: 실험 일정 및 채팅 알림

## 기능 구성도
![Image](https://github.com/user-attachments/assets/601928d4-26bf-45b5-80eb-c8a4fa82d04a)


## 기술 스택

- **백엔드**: Python 3.11 (FastAPI)
- **데이터베이스**: MySQL
- **인증**: Google OAuth, JWT 기반 인증
- **클라우드**: AWS
- **기타**: WebSocket (실시간 채팅), Celery (비동기 작업 처리)

## 설치 및 실행 방법

### Launch docker
```shell
> docker-compose up
```

### Install dependency
```shell
> poetry shell
> poetry install
```

### Apply alembic revision
```shell
> alembic upgrade head
```

### Run server
```shell
> python3 main.py --env local|dev|prod --debug
```

### Run test codes
```shell
> make test
```

### Make coverage report
```shell
> make cov
```

### Formatting

```shell
> make format
```


