# FastAPI Backend Development Template
This template provides a basic setup for FastAPI backend development.
This template is influenced by https://github.com/fastapi/full-stack-fastapi-template.

## Branch Overview
- **basic**: Contains only the Python development environment setup (Poetry, linter, formatter, pre-commit) without any source code. If FastAPI, SQLModel, pyJWT, etc., are not needed, remove the unnecessary dependencies before starting development.
- **main**: A template for developing an API server using FastAPI. It is a simple version for API server.
- **webdev**: A template for developing an web API server using FastAPI with more functionalities.

## Backend Development Steps
This template follows a standard project structure for FastAPI backend development, as outlined below.

### Dependencies Used
#### Common
- FastAPI
- Pydantic
- SQLModel
- pyJWT

#### Development Environment
- black = "^24.4.2" (in `pyproject.toml`)
- pytest = "^8.2.2"
- pre-commit = "^3.7.1"
- ruff = "0.5.3" (in `pyproject.toml`)
- mypy = "^1.10.1" (in `pyproject.toml`)
- importlib-metadata = "4.13.0"

### Example Project Structure
```bash
.
├── app
│   ├── api
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── v1
│   │       ├── endpoints
│   │       │   ├── __init__.py
│   │       │   ├── login.py
│   │       │   └── users.py
│   │       └── router.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── db.py
│   │   └── security.py
│   ├── main.py
│   ├── models
│   │   ├── auth.py
│   │   └── user.py
│   ├── tests
│   │   └── api
│   └── utils
│       ├── auth_utils.py
│       └── email_utils.py
├── .env
└── pyproject.toml

10 directories, 16 files
```

## 0. Running the Project with this Template
1. Clone the repository.
2. Update `pyproject.toml` with your project details.
3. Run `poetry install`.
4. Set up pre-commit hooks with `pre-commit install`.
5. Activate the virtual environment with `poetry shell`.

## 1. Project Setup and Poetry Configuration
1. Create the root project directory.
2. Initialize the project with `poetry init`:
   - Set the project name, Python version, and install basic modules.
   - If the project won't be a package, set `package-mode = false`.
3. Add dependencies as needed:
   ```bash
   poetry add {module}
   poetry install
   ```
   For dev dependencies (like linters, formatters, and testing tools), use the `--dev` flag:
   ```bash
   poetry add --dev flake8
   ```

## 2. Setting Up Linter, Formatter, and Pre-commit Hooks
To install dev dependencies, use the `--dev` flag. This allows separating dev dependencies during installation. For production, it's recommended to freeze versions using the `--prod` flag. Write specific configurations in the `.pyproject.toml`.

To install without dev dependencies:
```bash
poetry install --without dev,docs
```

### Pre-commit Hook Setup
1. Create a `.pre-commit-config.yaml` file and define hooks.
2. Pre-commit hooks help check files before committing (e.g., checking for large files, formatting issues, etc.).

Example `.pre-commit-config.yaml`:
```yaml
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

Install the dependencies and pre-commit hooks:
```bash
poetry install
pre-commit install
```

## 3. Configure Secret Keys and Settings
1. Create the `app` directory.
2. In `app/core`, create `config.py` and define the settings class.
   - Include configurations such as CORS, API version, secret keys, domain, environment variables, database details, and SMTP.
3. Set up `secrets.py` for handling sensitive data.
4. Configure `db.py` for database connection information (exclude if no database is required yet).

## 4. Test with `main.py` and Start the Server
Create `main.py` and run the server to ensure everything works:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8888
```

## 5. Dockerfile Setup
Write a Dockerfile to containerize the application.

## 6. Miscellaneous
Add `.dockerignore`, `.gitignore`, and other necessary configuration files.

This structure and setup will help you get started quickly with FastAPI backend development.
