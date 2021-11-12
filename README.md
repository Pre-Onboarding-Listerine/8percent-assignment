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
| `김주완` |  | [joowankim](https://github.com/joowankim) | https://make-easy-anything.tistory.com |
| `박은혜` |  | [eunhye43](https://github.com/eunhye43) | https://velog.io/@majaeh43 |
| `윤수진` |  | [study-by-myself](https://github.com/study-by-myself)| https://pro-yomi.tistory.com |
| `주종민` |  | [Gouache-studio](https://github.com/Gouache-studio) | https://gouache-studio.tistory.com/ |

## 구현 기능

### 거래내역 조회 API

- <간단설명>

**구현 내용**

-
-
-

**요청 예시**

```

```

  **응답 예시**

```

```


### 입금 API

- <간단설명>

**구현 내용**

-
-
-

**요청 예시**

```

```

  **응답 예시**

```

```

### 출금 API

- <간단설명>

**구현 내용**

-
-
-

**요청 예시**

```

```

  **응답 예시**

```

```

## 8️⃣ 모델 관계

![image](https://user-images.githubusercontent.com/32446834/141298674-bd9d48c4-3fd3-4019-924f-e2c7c1ae7182.png)

[협업방식 및 모델링 회의](https://github.com/Pre-Onboarding-Listerine/8percent-assignment.wiki.git)

### 존재하는 모델

- `User`: 회사의 이름 문자열과 표현된 언어를 속성으로 가지는 모델
- `Account`: 회사에 대한 메타정보를 속성으로 가지는 모델
- `TransactionEvent`: `Company`와 `Tag` 테이블 사이의 관계 테이블

## 8️⃣ 실행환경 설절 방법

> `git`과 `docker`, `docker-compose`가 설치되어 있어야 합니다.

1. 레포지토리 git 클론

    ```bash
    $ git clone https://github.com/Pre-Onboarding-Listerine/wanted-lab-assignment.git
    ```

2. `my_settings.py` 프로젝트 루트 디렉토리에 위치시키기

3. 애플리케이션 실행하기

    ```bash
    $ docker-compose up

    # 애플리케이션을 백그라운드에서 실행하고 싶다면
    $ docker-compose up -d
    
    # 어플리케이션이 실행이 되고 난 후에 데이터베이스 migration이 필요하다면
    $ docker-compose exec api
    ```

4. 애플리케이션에 접근하기

    django의 디폴트 포트인 8000포트가 아닌 8002번 포트와 연결되어 있습니다. 따라서 아래 주소로 로컬에 실행한 애플리케이션에 접근하실 수 있습니다.
    ```
    http://localhost:8002
    ```

## 8️⃣ 과제 결과물 테스트 및 확인 방법

[`test_app.py` 연동 설정 PR]()

1. `test_app.py` 실행시키기
    
    ```
    $ pytest
    ```
   
2. POSTMAN 확인: 

3. 배포된 서버의 주소

    ```commandline

    ```

# 8️⃣ Reference

이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8퍼센트에서 출제한 과제를 기반으로 만들었습니다.
