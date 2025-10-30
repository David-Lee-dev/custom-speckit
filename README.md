# Custom Speckit 🚀

> AI 기반 Spec-Driven Development를 위한 향상된 워크플로우

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

프로젝트의 명세서를 **단일 진실의 원천**으로 관리하고, 변경사항을 **Delta 방식**으로 추적하여 안전하게 개선하는 도구입니다.

> **✨ v1.3.2 업데이트**
> - 📁 **디렉토리 구조 개선**: specs/는 프로젝트 뼈대(누적), features/는 구현 기록(스냅샷)
> - 🔧 **tech-stack.md**: 기술 스택을 specs/에서 중앙 관리, 변경 이력 추적
> - 📊 **data-model.md**: 전체 데이터 모델을 specs/에서 관리, 엔티티 누적
> - 🔌 **contracts/**: API 스펙을 specs/에서 관리, 엔드포인트 누적
> - 🎯 **features/ 간소화**: plan.md, tasks.md만 보관 (기술 스펙은 specs/로 이동)

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

### 🌐 자동 언어 감지 (v1.3.0+)

Custom Speckit은 사용자 입력을 자동으로 분석하여 적절한 언어로 문서를 생성합니다:

```bash
# 한글 입력 → 모든 문서 한글 생성
/speckit.specify "사용자 인증 기능 추가"
# → spec.md, plan.md, tasks.md 모두 한글로 작성

# 영어 입력 → 모든 문서 영어 생성
/speckit.specify "Add user authentication feature"
# → spec.md, plan.md, tasks.md all in English

# 혼용 입력 (한글 포함) → 한글로 생성
/speckit.specify "OAuth2 인증 시스템 구현"
# → 한글이 포함되면 한글로 작성

# 기본값: 한글
/speckit.specify ""  # 빈 입력
# → 한글로 작성 (기본값)
```

**언어 일관성**: 한 번 정해진 언어는 프로젝트 전체에서 유지됩니다.
- spec.md가 한글 → plan.md, tasks.md도 자동으로 한글
- spec.md가 영어 → plan.md, tasks.md도 자동으로 영어

### 신규 프로젝트

```bash
# 1. 명세서 생성 (한글/영어 자동 감지)
/speckit.specify "할 일 관리 앱을 만들고 싶어"

# 2. 구현 계획 생성 (spec.md 언어 따름)
/speckit.plan

# 3. 작업 목록 생성 (plan.md 언어 따름)
/speckit.tasks

# 4. 구현 실행 (tasks.md 언어 따름)
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

#### 핵심 워크플로우 명령어

| 명령어 | 용도 | 입력 | 출력 | 사용 시점 |
|--------|------|------|------|----------|
| `/speckit.specify` | 명세서 생성/수정 | 자연어 요구사항 | `spec.md` 또는 `delta-spec.md` | 프로젝트 시작 또는 기능 추가 시 |
| `/speckit.plan` | 구현 계획 작성 | (spec.md 읽음) | `features/{version}/{date}_{branch}/plan.md` | 명세 확정 후 설계 단계 |
| `/speckit.tasks` | 작업 목록 분해 | (plan.md 읽음) | `features/{version}/{date}_{branch}/tasks.md` | 구현 전 작업 분할 |
| `/speckit.implement` | 실제 구현 실행 | (tasks.md 읽음) | 소스 코드, 테스트, 문서 | 개발 실행 단계 |

#### Delta 관리 명령어 (기존 프로젝트용)

| 명령어 | 용도 | 출력 | 필수 여부 |
|--------|------|------|----------|
| `/speckit.review-delta` | Delta 분석 및 영향 평가 | 분석 리포트, Constitution 검증 | 선택 (권장) |
| `/speckit.approve-delta` | Delta를 spec.md에 병합 | spec.md 업데이트, 백업 생성, CHANGELOG 기록 | **필수** |
| `/speckit.reject-delta` | Delta 거부 및 삭제 | Delta 삭제 또는 아카이브 | 선택 |

#### 품질 관리 명령어

| 명령어 | 용도 | 출력 |
|--------|------|------|
| `/speckit.analyze` | spec/plan/tasks 교차 검증 | 일관성 분석 리포트, 누락/중복 항목 식별 |
| `/speckit.checklist` | 요구사항 검증 | 수락 기준 체크리스트, 테스트 시나리오 |
| `/speckit.constitution` | Constitution 정의/수정 | `.specify/memory/constitution.md` |

### 명령어 실행 순서

#### 신규 프로젝트
```
1. /speckit.specify "요구사항 설명"
   → .specify/specs/spec.md 생성

2. /speckit.plan
   → features/v1.0.0/{date}_{branch}/plan.md 생성

3. /speckit.tasks
   → features/v1.0.0/{date}_{branch}/tasks.md 생성

4. /speckit.implement
   → 코드 구현, 테스트 작성
```

#### 기존 프로젝트 (기능 추가/수정)
```
1. /speckit.specify "새 기능 설명"
   → .specify/.deltas/{branch}/delta-spec.md 생성

2. /speckit.review-delta (선택)
   → Delta 분석 리포트

3. /speckit.approve-delta
   → spec.md 업데이트, delta 삭제

4. /speckit.plan
   → 새 plan.md 생성

5. /speckit.tasks
   → 새 tasks.md 생성

6. /speckit.implement
   → 코드 구현
```

## 📁 생성되는 디렉토리

```
your-project/
├── .specify/
│   ├── specs/              # 프로젝트 뼈대 (버전 관리 없이 누적)
│   │   ├── spec.md         # 전체 기능 명세
│   │   ├── tech-stack.md   # 기술 스택 (최초 생성, 추가 시 수정)
│   │   ├── data-model.md   # 데이터 모델 (엔티티 누적)
│   │   └── contracts/      # API 계약 (엔드포인트 누적)
│   ├── features/           # Feature별 구현 기록
│   │   └── v1.0.0/
│   │       └── 2025_10_24-user-auth/
│   │           ├── plan.md    # 이 feature의 구현 계획
│   │           └── tasks.md   # 이 feature의 작업 목록
│   ├── memory/         # Constitution (프로젝트 원칙)
│   ├── scripts/        # 헬퍼 스크립트
│   └── templates/      # 문서 템플릿
└── .cursor/
    ├── commands/       # Speckit 명령어
    └── rules/          # 워크플로우 규칙
```

### 📊 디렉토리 역할

#### **specs/ - 프로젝트 뼈대** (Single Source of Truth)
- ✅ 프로젝트 전체에서 공유
- ✅ 버전 디렉토리 없음 (항상 최신)
- ✅ 누적 업데이트 (변경 이력은 파일 내부에 기록)
- 예: 새 엔티티 추가 시 `data-model.md`에 추가, MongoDB 도입 시 `tech-stack.md` 수정

#### **features/ - Feature 구현 기록** (Historical Snapshots)
- ✅ Feature별로 버전/날짜 디렉토리 분리
- ✅ plan.md, tasks.md만 보관
- ✅ 한 번 생성 후 수정 안 함 (이력 보존)
- 예: `v1.0.0/2025_10_24-user-auth/plan.md` → user-auth feature의 구현 계획만

---

## 🔄 개발 시나리오

### **최초 프로젝트 개발**

```bash
# 1. 명세 생성
/speckit.specify "할 일 관리 앱"
→ .specify/specs/spec.md

# 2. 계획 수립
/speckit.plan
→ .specify/specs/tech-stack.md     (React, Node.js 결정)
→ .specify/specs/data-model.md     (User, Task 엔티티)
→ .specify/specs/contracts/        (API 스펙)
→ .specify/features/v1.0.0/2025_10_28-todo-app/plan.md

# 3. 작업 생성
/speckit.tasks
→ .specify/features/v1.0.0/2025_10_28-todo-app/tasks.md
   (specs/의 tech-stack, data-model, contracts 참조)
```

**결과**:
```
.specify/
├── specs/
│   ├── spec.md           # 할 일 관리 명세
│   ├── tech-stack.md     # React, Node.js
│   ├── data-model.md     # User, Task
│   └── contracts/        # user.yaml, task.yaml
└── features/v1.0.0/2025_10_28-todo-app/
    ├── plan.md
    └── tasks.md
```

### **추가 기능 개발 (기존 기술 사용)**

```bash
# 1. 기능 추가
/speckit.specify "댓글 기능 추가"
/speckit.approve-delta
→ .specify/specs/spec.md (댓글 요구사항 병합)

# 2. 계획 수립
/speckit.plan
→ .specify/specs/tech-stack.md     (변경 없음)
→ .specify/specs/data-model.md     (Comment 엔티티 추가)
→ .specify/specs/contracts/        (comment.yaml 추가)
→ .specify/features/v1.1.0/2025_11_05-comment/plan.md

# 3. 작업 생성
/speckit.tasks
→ .specify/features/v1.1.0/2025_11_05-comment/tasks.md
```

**결과**:
```
.specify/
├── specs/                # 누적 업데이트
│   ├── spec.md          # Todo + Comment
│   ├── tech-stack.md    # React, Node.js (동일)
│   ├── data-model.md    # User, Task, Comment
│   └── contracts/       # user, task, comment
└── features/
    ├── v1.0.0/2025_10_28-todo-app/
    └── v1.1.0/2025_11_05-comment/  # 추가됨
```

### **기술 스택 변경**

```bash
# 1. 검색 기능 (MongoDB 도입)
/speckit.specify "전문 검색 기능"
/speckit.approve-delta

# 2. 계획 수립
/speckit.plan
→ .specify/specs/tech-stack.md     (MongoDB 추가됨!)
→ .specify/specs/data-model.md     (SearchIndex 추가)
→ .specify/specs/contracts/        (search.yaml 추가)
→ .specify/features/v1.2.0/2025_11_20-search/plan.md
```

**tech-stack.md 변경 예시**:
```markdown
## Database
- PostgreSQL 15.x - 메인 DB
- MongoDB 7.x - 검색 엔진
  * Added: 2025_11_20 (search)
  * Reason: 전문 검색 최적화
```

---

## 🌿 Git 워크플로우

### Feature 디렉토리 & 브랜치 명명 규칙

**디렉토리명**: `YYYY_MM_DD-branch-name`
- 날짜: 언더스코어(`_`)로 구분 - 디렉토리 정렬용
- 브랜치명: 하이픈(`-`)으로 구분

**브랜치명**: `branch-name` (날짜 제외)

**예시**:
```bash
# 브랜치 생성
git checkout -b user-auth

# Speckit 실행 시 자동 생성됨
/speckit.plan
# → .specify/features/v1.0.0/2025_10_24-user-auth/

# 디렉토리명과 브랜치명이 일치함 (날짜 부분 제외)
```

### Commit 메시지 형식

```
[Type] 간결한 제목 (50자 이내)

- 상세 내용 1
- 상세 내용 2
- 상세 내용 3
```

**Commit Type**:
- `[Feature]` - 새 기능
- `[Fix]` - 버그 수정
- `[Refactor]` - 리팩토링
- `[Docs]` - 문서 변경
- `[Test]` - 테스트 추가
- `[Chore]` - 빌드/설정
- `[Release]` - 버전 릴리스

**예시**:
```bash
git commit -m "[Feature] 사용자 인증 기능 추가

- JWT 토큰 기반 인증 구현
- 로그인/로그아웃 API 추가
- 인증 미들웨어 구현"
```

**자세한 규칙**: `.cursor/rules/git-commit-guidelines.mdc` 참조

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
