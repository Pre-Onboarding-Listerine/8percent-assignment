# 8percent-assignment

## 8️⃣ 기업과제
- 기업명: 8퍼센트
- 기업사이트: https://8percent.kr/
- 기업채용공고: https://www.wanted.co.kr/wd/64695

## 8️⃣ 과제 내용

#### **[필수 포함 사항]**

- READ.ME 작성
    - 프로젝트 빌드, 자세한 실행 방법 명시
    - 구현 방법과 이유에 대한 간략한 설명
    - 완료된 시스템이 배포된 서버의 주소
    - Swagger나 Postman을 통한 API 테스트할때 필요한 상세 방법
    - 해당 과제를 진행하면서 회고 내용 블로그 포스팅
- Swagger나 Postman을 이용하여 API 테스트 가능하도록 구현

<aside>
📝 “계좌 거래 API”를 구현해주세요. API는 3가지가 구현되어야 합니다.
</aside>

#### **[API 목록]**

- 거래내역 조회 API
- 입금 API
- 출금 API

#### **[고려 사항]**

**주요 고려 사항은 다음과 같습니다.**

- 계좌의 잔액을 별도로 관리해야 하며, 계좌의 잔액과 거래내역의 잔액의 무결성의 보장
- DB를 설계 할때 각 칼럼의 타입과 제약

**구현하지 않아도 되는 부분은 다음과 같습니다.**

- 문제와 관련되지 않은 부가적인 정보. 예를 들어 사용자 테이블의 이메일, 주소, 성별 등
- 프론트앤드 관련 부분

**제약사항은 다음과 같습니다.**

- (**8퍼센트가 직접 로컬에서 실행하여 테스트를 원하는 경우를 위해**) 테스트의 편의성을 위해 mysql, postgresql 대신 sqllite를 사용해 주세요.

**상세 설명**

**1)** 거래내역 조회 **API**

거래내역 API는 다음을 만족해야 합니다.

- 계좌의 소유주만 요청 할 수 있어야 합니다.
- 거래일시에 대한 필터링이 가능해야 합니다.
- 출금, 입금만 선택해서 필터링을 할 수 있어야 합니다.
- Pagination이 필요 합니다.
- 다음 사항이 응답에 포함되어야 합니다.
    - 거래일시
    - 거래금액
    - 잔액
    - 거래종류 (출금/입금)
    - 적요

**2)** 입금 **API**

입금 API는 다음을 만족해야 합니다.

- 계좌의 소유주만 요청 할 수 있어야 합니다.

**3)** 출금 **API**

출금 API는 다음을 만족해야 합니다.

- 계좌의 소유주만 요청 할 수 있어야 합니다.
- 계좌의 잔액내에서만 출금 할 수 있어야 합니다. 잔액을 넘어선 출금 요청에 대해서는 적절한 에러처리가 되어야 합니다.

**4)** 가산점

다음의 경우 가산점이 있습니다.

- Unit test의 구현
- Functional Test 의 구현 (입금, 조회, 출금에 대한 시나리오 테스트)
- 거래내역이 1억건을 넘어갈 때에 대한 고려
    - 이를 고려하여 어떤 설계를 추가하셨는지를 README에 남겨 주세요.
----

## 8️⃣ 팀: 리스테린(Listerine)

* 팀원

| 이름 | 역할 | GITHUB | BLOG |
| :---: | :---: | :---: | :---: |
| `김주완` | 개발 및 배포환경 설정, API 설계 및 구현 | [joowankim](https://github.com/joowankim) | https://make-easy-anything.tistory.com |
| `박은혜` | 애플리케이션 배포, 기능 구현 | [eunhye43](https://github.com/eunhye43) | https://velog.io/@majaeh43 |
| `윤수진` | API 구현 | [study-by-myself](https://github.com/study-by-myself)| https://pro-yomi.tistory.com |
| `주종민` | 모델 설계 및 구현 | [Gouache-studio](https://github.com/Gouache-studio) | https://gouache-studio.tistory.com/ |

## 구현 내용

8퍼센트의 과제로 구현된 엔드포인트는 다음과 같습니다.

- `POST /api/users`: 회원가입을 할 수 있습니다.
- `POST /api/auth/login`: 로그인(인증 토큰 발급)을 할 수 있습니다.
- `POST /api/accounts`: 입출금을 위한 계좌 생성을 할 수 있습니다.
- `GET /api/accounts`: 인증 토큰을 이용해 자신의 계좌 리스트를 검색할 수 있습니다.
- `GET /api/accounts/<account-number>`: 계좌 리스트를 불러와 자신의 계좌번호를 알았다면 그 계좌번호를 이용해 자신의 특정 계좌를 조회할 수 있습니다.
- `PUT /api/accounts/<account-number>`: 특정 계좌에 대한 입/출금을 수행할 수 있습니다.
- `GET /api/accounts/<account-number>/transactions`: 특정 계좌에 대한 거래내역을 조회할 수 있습니다.

### 이 중에서 과제에서 구현하도록 언급된 엔드포인트는 다음과 같습니다.

- `PUT /api/accounts/<account-number>`: 입/출금
- `GET /api/accounts/<account-number>/transactions`: 거래 내역 조회

구현된 엔드포인트에 대한 테스트는 다음 포스트맨 문서에서 수행하실 수 있습니다.

포스트맨 문서 주소: https://documenter.getpostman.com/view/15905881/UVC8CRFb

### Unit test와 Functional test

테스트는 `/tests` 디렉토리에서 확인하실 수 있습니다. 그리고 루트 디렉토리에서 다음 명령어로 테스트를 실행할 수 있습니다.

```commandline
$ pytest
```

## 8️⃣ 모델 관계

![image](https://user-images.githubusercontent.com/32446834/141298674-bd9d48c4-3fd3-4019-924f-e2c7c1ae7182.png)

[협업방식 및 모델링 회의](https://github.com/Pre-Onboarding-Listerine/8percent-assignment.wiki.git)

### 존재하는 모델

- `User`: 계좌를 소유할 수 있는 애플리케이션 사용자
- `Account`: 계좌의 잔액을 관리합니다.
- `TransactionEvent`: 계좌 잔액을 관리하면서 생성된 이벤트를 의미합니다.

## 애플리케이션 구조

저희팀은 해당 애플리케이션에서 다른 컨텍스트를 가지는 영역이 총 3가지 정도 있다고 판단했습니다.
그래서 애플리케이션의 내부를 `security`, `accounts`, `users` 모듈로 분류했습니다.
여기서 각 모듈은 다음과 같은 분류의 요청들을 처리합니다.

- `security`: 인증 및 인가에 대한 요청을 처리합니다.
- `accounts`: 계좌를 조작하는 요청을 처리합니다.
- `users`: 계정을 조작하는 요청을 처리합니다.

그 다음에는 각 영역에 도착할 요청들이 각 책임별로 나뉘어진 각 계층을 이동하면서 처리될 수 있도록 구현하고자 했습니다.
그래서 각 모듈에 `routers`, `application`, `domain`, `infra` 계층을 두어 각 계층의 책임을 분류했습니다.

- `routers`: 들어온 요청을 검증하고 전달받은 데이터를 정제해 애플리케이션 계층 컴포넌트에 전달합니다.
- `application`: 도메인 계층에서 요청을 처리할 수 있는 객체를 찾아 메시지를 넘기며 이 계층의 작업단위(Unit of Work) 컴포넌트를 이용해 트랜잭션을 관리합니다.
- `domain`: 도메인의 모델들이 위치하며 도메인의 규칙으로 전달받은 요청을 처리합니다.
- `infra`: 처리된 요청의 결과를 영속적으로 보존할 수 있도록 데이터베이스와 같은 세부사항과 직접적으로 소통합니다.

## 8️⃣ 실행환경 설절 방법

> `git`과 `docker`, `docker-compose`가 설치되어 있어야 합니다.

1. 레포지토리 git 클론

    ```bash
    $ git clone https://github.com/Pre-Onboarding-Listerine/8percent-assignment.git
    ```

2. 애플리케이션 실행하기

    ```bash
    $ docker-compose up

    # 애플리케이션을 백그라운드에서 실행하고 싶다면
    $ docker-compose up -d
    
    # 어플리케이션이 실행이 되고 난 후에 데이터베이스 migration이 필요하다면
    $ docker-compose exec api
    ```

3. 애플리케이션에 접근하기

    ```
    http://localhost:8080
    ```

## 8️⃣ 과제 결과물 테스트 및 확인 방법

1. POSTMAN 확인: https://documenter.getpostman.com/view/15905881/UVC8CRFb

2. 배포된 서버의 주소

    ```commandline
    http://15.164.145.89:8080
    ```

# 8️⃣ Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8퍼센트에서 출제한 과제를 기반으로 만들었습니다.
