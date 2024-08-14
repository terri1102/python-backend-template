# 브랜치별 템플릿 종류
- basic: 소스 코드 없이 파이썬 개발 환경 설정(poetry, linter, formatter, pre-commit) 파일만 있음. FastAPI, SQLModel, pyJWT 등 사용하지 않는다면 디펜던시 제거 후 개발하기
- main: FastAPI로 API 서버 개발을 위한 템플릿

## 사용하는 dependency
개발 환경
- black = "^24.4.2" -> pyproject.toml
- pytest = "^8.2.2"
- pre-commit = "^3.7.1"
- ruff 0.5.3 -> pyproject.toml
- mypy = "^1.10.1" -> pyproject.toml
- importlib-metadata = "4.13.0"


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
