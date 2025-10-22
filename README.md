# Custom Speckit 🚀

> AI 기반 Spec-Driven Development를 위한 향상된 워크플로우

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

프로젝트의 명세서를 **단일 진실의 원천**으로 관리하고, 변경사항을 **Delta 방식**으로 추적하여 안전하게 개선하는 도구입니다.

**특징:**
- 🌐 **언어 무관** - Node.js, Rust, Python, Go 등 모든 프로젝트에서 사용
- 🐳 **로컬 개발** - Docker로 로컬 패키지 서버 운영, PyPI 계정 불필요
- ⚡ **간편 설치** - 명령어 하나로 설치 및 업데이트

## ⚡ Quick Start

### 방법 1: 로컬 개발 (Docker 사용) 🐳

PyPI 계정 없이 로컬에서 다른 프로젝트에 적용:

```bash
# Custom Speckit 프로젝트에서
cd custom-speckit
docker-compose up -d              # 로컬 PyPI 서버 실행
./scripts/upload-local.sh         # 패키지 빌드 & 업로드

# 다른 프로젝트에서 사용
cd /path/to/your-project
uvx --index-url http://localhost:8080/simple/ custom-speckit init

# Constitution 작성 후 Cursor AI에서 /speckit.specify 실행
```

### 방법 2: PyPI 배포 (전역 사용)

PyPI에 배포 후 어디서든 사용:

```bash
# 1. uv 설치 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 프로젝트에 설치
cd your-project
uvx custom-speckit init

# 3. Constitution 작성 (프로젝트 원칙)
vim .specify/memory/constitution.md

# 4. Cursor AI에서 /speckit.specify 실행
```

## 📦 설치

### 1. uv 설치

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Homebrew (macOS)
brew install uv
```

### 2. 프로젝트에 Custom Speckit 설치

```bash
cd your-project
uvx custom-speckit init
```

**결과:**
- ✅ `.specify/` 디렉토리 생성 (scripts, templates, specs)
- ✅ `.cursor/` 디렉토리 생성 (commands, rules)
- ✅ `.gitignore` 자동 업데이트
- ✅ 다른 프로젝트 파일은 그대로 유지

### 3. 업데이트

```bash
# 업데이트
uvx custom-speckit update

# 변경사항 미리보기
uvx custom-speckit update --dry-run

# 백업 없이 업데이트
uvx custom-speckit update --skip-backup
```

**특징:**
- ✅ **완전 동기화** - 템플릿과 동일하게 유지 (추가/수정/삭제)
- ✅ **스마트 보존** - 템플릿에 없는 파일은 보존 (사용자가 추가한 파일 유지)
- ✅ **자동 백업** - 기본적으로 백업 자동 생성 (--skip-backup으로 생략 가능)

**동작 방식:**
- 템플릿에 **있는** 파일 → 덮어쓰기 (항상 최신으로)
- 템플릿에 **추가된** 파일 → 추가 (new.sh 같은 신규 파일)
- 템플릿에서 **삭제된** 파일 → 삭제 (더 이상 필요 없는 파일)
- 템플릿에 **없는** 파일 → 보존 (사용자가 만든 spec.md, 커스텀 스크립트 등)

## 🐳 로컬 개발 서버 (선택)

PyPI 계정 없이 로컬 Docker 서버로 테스트할 수 있습니다.

### 1. 로컬 PyPI 서버 실행

```bash
# Custom Speckit 프로젝트 디렉토리에서
docker-compose up -d

# 서버 확인
curl http://localhost:8080
```

### 2. 패키지 빌드 및 업로드

```bash
# Custom Speckit 프로젝트에서
./scripts/upload-local.sh
```

### 3. 다른 프로젝트에서 사용

```bash
cd /path/to/your-project

# 로컬 서버에서 설치
uvx --index-url http://localhost:8080/simple/ custom-speckit init

# 업데이트
uvx --index-url http://localhost:8080/simple/ custom-speckit update
```

### 서버 관리

```bash
# 로그 확인
docker-compose logs -f

# 서버 중지
docker-compose down

# 서버 재시작
docker-compose restart
```

**장점:**
- ✅ PyPI 계정 불필요
- ✅ 빠른 로컬 테스트
- ✅ 오프라인 사용 가능
- ✅ 팀 내부 공유 가능 (같은 네트워크)

## 🎯 기본 사용법

### 신규 프로젝트

```bash
# 1. 명세서 생성
/speckit.specify "할 일 관리 앱을 만들고 싶어"

# 2. 구현 계획 생성
/speckit.plan

# 3. 작업 목록 생성
/speckit.tasks

# 4. 구현 실행
/speckit.implement
```

### 기존 프로젝트에 기능 추가

```bash
# 1. 변경사항 제안 (Delta 생성)
/speckit.specify "사용자 인증 기능 추가"

# 2. 변경사항 검토 (선택)
/speckit.review-delta

# 3. 변경사항 승인
/speckit.approve-delta

# 4. 구현 계획 및 실행
/speckit.plan
/speckit.tasks
/speckit.implement
```

## 📋 CLI 명령어

### 설치/업데이트

```bash
# 버전 확인
uvx custom-speckit           # 버전 및 사용 가능한 명령어 표시
uvx custom-speckit version   # 버전만 표시

# 프로젝트에 설치 (항상 덮어쓰기)
uvx custom-speckit init [PATH]

# 업데이트 (항상 덮어쓰기)
uvx custom-speckit update

# 변경사항 미리보기
uvx custom-speckit update --dry-run

# 백업 없이 업데이트
uvx custom-speckit update --skip-backup
```

### Cursor AI 명령어

| 명령어 | 설명 |
|--------|------|
| `/speckit.specify` | 명세서 생성/수정 |
| `/speckit.plan` | 구현 계획 생성 |
| `/speckit.tasks` | 작업 목록 생성 |
| `/speckit.implement` | 구현 실행 |
| `/speckit.review-delta` | Delta 검토 |
| `/speckit.approve-delta` | Delta 승인 |
| `/speckit.reject-delta` | Delta 거부 |
| `/speckit.analyze` | 일관성 분석 |
| `/speckit.checklist` | 품질 체크리스트 |

### 명령어 실행 순서

**신규 프로젝트:**
```
specify → plan → tasks → implement
```

**기존 프로젝트:**
```
specify → review-delta → approve-delta → plan → tasks → implement
```

## 📁 생성되는 디렉토리

```
your-project/
├── .specify/
│   ├── specs/          # 최종 명세서 (spec.md)
│   ├── features/       # 개발 이력 (plan.md, tasks.md)
│   ├── memory/         # Constitution (프로젝트 원칙)
│   ├── scripts/        # 헬퍼 스크립트
│   └── templates/      # 문서 템플릿
└── .cursor/
    ├── commands/       # Speckit 명령어
    └── rules/          # 워크플로우 규칙
```

## ❓ FAQ

**Q: 다른 프로젝트 파일에 영향을 주나요?**  
A: 아니요. `.specify/`와 `.cursor/`만 관리하고 package.json, Cargo.toml 등은 건드리지 않습니다.

**Q: 업데이트 시 내가 작성한 파일이 삭제되나요?**  
A: 템플릿에 **없는** 파일은 모두 보존됩니다. 템플릿에 있는 파일만 최신 버전으로 덮어씁니다. 예: 
- `spec.md`, `my-script.sh` (사용자 파일) → 보존 ✅
- `common.sh`, `constitution.md` (템플릿 파일) → 업데이트 ✅

**Q: 여러 프로젝트에서 사용할 수 있나요?**  
A: 네. 각 프로젝트에서 `uvx custom-speckit init`을 실행하면 됩니다. 항상 최신 버전으로 덮어씁니다.

**Q: 설치할 때 이미 설치되었다는 경고가 나오나요?**  
A: 아니요. 항상 최신 버전으로 덮어씁니다. 경고 없이 즉시 설치/업데이트됩니다.

**Q: Git에 커밋해야 하나요?**  
A: `.specify/`와 `.cursor/`는 커밋하세요. `.specify/.deltas/`는 임시 파일이므로 자동으로 .gitignore에 추가됩니다.

## 🔗 참고 자료

- [uv 공식 사이트](https://docs.astral.sh/uv/)
- [Cursor AI 문서](https://docs.cursor.com/)
- [GitHub Spec-Kit](https://github.com/github/spec-kit)
- [워크플로우 규칙](.cursor/rules/custom-speckit-workflow.mdc)

## 📄 라이선스

MIT License - Based on [GitHub Spec-Kit](https://github.com/github/spec-kit)

---

<div align="center">

**Custom Speckit으로 더 나은 Spec-Driven Development를!** 🚀

[⬆ 맨 위로](#custom-speckit-)

</div>
