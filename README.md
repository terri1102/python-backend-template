# 백엔드 개발 순서
이 템플릿은 FastAPI 백엔드 개발을 위한 기본 세팅 템플릿이며, 아래의 프로젝트 예시 구조를 따름

## 사용하는 dependency
공통
- FastAPI
- Pydantic
- SQLModel
- pyJWT

개발 환경
- black = "^24.4.2" -> pyproject.toml
- pytest = "^8.2.2"
- pre-commit = "^3.7.1"
- ruff 0.5.3 -> pyproject.toml
- mypy = "^1.10.1" -> pyproject.toml
- importlib-metadata = "4.13.0"


### 프로젝트 예시 구조
```bash
.
├── app
│   ├── api
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── v1
│   │       ├── endpoints
│   │       │   ├── __init__.py
│   │       │   ├── login.py
│   │       │   └── users.py
│   │       └── router.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── db.py
│   │   └── security.py
│   ├── main.py
│   ├── models
│   │   ├── auth.py
│   │   └── user.py
│   ├── tests
│   │   └── api
│   └── utils
│       ├── auth_utils.py
│       └── email_utils.py
├── .env
└── pyproject.toml

10 directories, 16 files

```

## 0. 이 템플릿으로 프로젝트 실행하기
- git clone
- poetry install
- pre-commit install


## 1. 프로젝트 생성 및 poetry 설정
1. 프로젝트 루트 디렉토리 생성

2. poetry init으로 시작
- 프로젝트명, 파이썬 버전, 기본 모듈 설치
- 패키지로 설치 가능하게 할 것이 아니면 package-mode = false 설정

3. 이 프로젝트에서 사용할 것 같은 dependency 설치
```bash
poetry add {module}
poetry install
```
- dev용 dependency는 `--dev` flag로 설치(주로 linter, formatter, test)
```bash
poetry add --dev flake8
```

## 2. Linter, formatter, pre-commit hook 등 기존에 사용하던 설정 추가
위에서 말한 것처럼 `--dev` flag를 넣어서 add하자.
그러면 나중에 `poetry install`시 그룹을 구분해서 설치할 수 있다.
참고로 prod도 따로 `--prod`를 붙여서 버전을 freeze하는 것도 권장된다.
기본 설정대로 add하면 특정 버전 이상을 다운받기 때문에 freeze하는 게 좋을듯
`.pyproject.toml`에 세부 설정도 작성하자.

```
poetry install --without dev,docs
```

### black
- Black은 *formatter*로 코드를 자동으로 포매팅하여 스타일 가이드에 맞게 정리해 줌.
- PEP 8 스타일 가이드라인을 기반으로 함
- 최신 버전: 24.4.2
- pyproject.toml
```toml
[tool.black]
line-length = 88
```

- pre-commit hook으로 사용
```
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
```


<!--
### isort
- Python 코드에서 import 문을 정렬하고 그룹화하는 도구
- 최신 버전: 5.13.2
- pyproject.toml, .isort.cfg, setup.cfg, 또는 tox.ini 파일을 사용하여 설정
- pyproject.toml
```
[tool.isort]
profile = "black"
line_length = 88
```

### flake8
- flake8은 *Linter*로 Python 코드에서 스타일 위반, 버그 가능성, 보안 문제 등을 검사함
- Black은 코드 포매팅을 자동화하고, flake8은 코드 품질을 검사하기 때문에 같이 쓰는 게 좋음
- 최신 버전: 7.1.0
- .flake8나 setup.cfg로 설정 가능
- pre-commit에서 이 설정 파일을 읽는데 문제가 있음

```

``` -->

### ruff
- Ruff는 빠르고 확장 가능한 Python *Linter*임.
- Flake8과 isort를 대체할 수 있으며, 일부 Black과 Mypy 기능도 지원함
- 최신 버전: 0.5.3
- pyproject.toml로 설정
```
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.5.3
    hooks:
      - id: ruff
        args:
          - --fix
      - id: ruff-f
```
E:
- "E203" : Whitespace before ':' (This rule is often ignored because it conflicts with the PEP 8 recommendation for slicing).
- "E302" : Expected 2 blank lines, found 1 (Function or class definition missing required blank lines before it).
- "E305" : Expected 2 blank lines after end of function or class.
- "E401": Multiple imports on one line.
- "E402": Module level import not at top of file.
- "E501": Line too long (This rule is often ignored or adjusted because longer lines can be acceptable in many projects).

F
- "F401": Module imported but unused.
- "F403": 'from module import *' used; unable to detect undefined names.


W
- "W503": Line break occurred before a binary operator (This rule is often ignored in favor of W504, which enforces the opposite and is more aligned with modern PEP 8).



### mypy
- Python 코드의 타입 힌트를 검사하는 정적 타입 체커
- Mypy를 사용하면 코드의 타입 오류를 컴파일 타임에 발견하여 런타임 오류를 줄일 수 있음
- 최신 버전: 1.10.1
- mypy.ini, setup.cfg, 또는 pyproject.toml로 설정
- pyproject.toml
```
[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true
ignore_missing_imports = true
strict = true
```

호환성을 위해 `importlib-metadata = "4.13.0"`를 같이 설치한다.
반드시 5.0.0 이전 버전이어야 함


### pytest
- Python용 테스트 프레임워크로, 유닛 테스트, 기능 테스트, 통합 테스트 등을 쉽게 작성하고 실행할 수 있게 해줌
- 최신 버전:
- pre-commit hook
```
  - repo: https://github.com/pre-commit/mirrors-pytest
    rev: v6.2.5
    hooks:
      - id: pytest
```

### python-check-blanket-noqa
- python-check-blanket-noqa 훅은 코드에서 광범위하게 사용된 # noqa 주석을 찾아내고 이를 방지

## 2-2. pre-commit
- 이제 `.pre-commit-config.yaml` 을 생성하고 hook을 작성하자
- pre-commit은 커밋하기 전에 파일을 검사해주는 hook으로 큰 파일이 포함되었는지 등 다양한 검사 가능함
- 최신 버전: 3.7.1
```
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: check-added-large-files
      - id: check-toml
      - id: check-yaml
        args:
          - --unsafe
      - id: end-of-file-fixer
      - id: trailing-whitespace
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.215
    hooks:
      - id: ruff
        args: ["--config=pyproject.toml"]
  - repo: https://github.com/pre-commit/pygrep-hooks
    rev: v1.7.0
    hooks:
      - id: python-check-blanket-noqa
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.1
    hooks:
      - id: mypy
  - repo: https://github.com/pre-commit/mirrors-pytest
    rev: v6.2.5
    hooks:
      - id: pytest
```


이제 .pyproject.toml과 .pre-commit-config.yaml이 작성되었다면 poetry install로 dependency들을 설치하고 pre-commit install 해주자
```
poetry install
pre-commit install
```


## 3. Config에 시크릿키, 아이디 등 세팅 하기
- 아직 DB 결정이 안 되었다면 DB는 제외


1. app/core의 config를 먼저 만들고 settings 클래스 작성
2. app/core의 secrets.py
3. app/core db.py # connection 정보


## 4. main.py 작성하고 uvicorn run으로 서버 잘 뜨나 확인

## 5. 도커 파일 작성

## 6. 기타
- .dockerignore, .gitignore 등 작성
