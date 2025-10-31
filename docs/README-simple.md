# 🚀 Custom Speckit - 빠른 시작 가이드

> 5분 안에 시작하는 Spec-Driven Development

[← 메인으로](../README.md) | [📚 상세 가이드](README-detailed.md)

---

## ⚡ 3단계로 시작하기

### 1️⃣ 설치

```bash
# uv 설치 (한 번만)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 프로젝트에 Custom Speckit 설치
cd your-project
uvx custom-speckit init
```

**결과**: `.specify/`와 `.cursor/` 디렉토리 생성됨

---

### 2️⃣ Constitution 작성 (프로젝트 원칙)

```bash
vim .specify/memory/constitution.md
```

**예시**:
```markdown
# My Project Constitution

## Core Principles

### I. Code Quality
모든 코드는 테스트를 포함해야 합니다.

### II. User First
사용자 경험을 최우선으로 고려합니다.

### III. Simplicity
복잡한 것보다 단순한 해결책을 선호합니다.
```

**팁**: Constitution은 AI가 코드 작성 시 따라야 할 프로젝트 원칙입니다.

---

### 3️⃣ 첫 기능 개발

Cursor AI에서 명령어 실행:

```bash
# 1. 명세서 생성 (한글로 자연스럽게 작성)
/speckit.specify "할 일 관리 앱을 만들고 싶어요. 할 일을 추가하고, 완료 표시하고, 삭제할 수 있어야 합니다."

# 2. 구현 계획 수립
/speckit.plan

# 3. 작업 목록 생성
/speckit.tasks

# 4. 구현 실행
/speckit.implement
```

**축하합니다!** 🎉 첫 번째 기능이 구현되었습니다.

---

## 🎯 핵심 4가지 명령어

| 명령어 | 무엇을 하나요? | 언제 쓰나요? |
|--------|---------------|-------------|
| `/speckit.specify` | 기능 명세서 작성 | 프로젝트 시작 또는 새 기능 추가 시 |
| `/speckit.plan` | 구현 계획 수립 | 명세서 확정 후 |
| `/speckit.tasks` | 작업 목록 생성 | 구현 계획 완료 후 |
| `/speckit.implement` | 실제 코드 작성 | 작업 목록 확정 후 |

---

## 🔄 두 번째 기능 추가하기

이미 프로젝트가 있다면:

```bash
# 1. 변경사항 제안 (Delta 생성)
/speckit.specify "댓글 기능을 추가하고 싶어요"

# 2. 변경사항 승인
/speckit.approve-delta

# 3. 구현
/speckit.plan
/speckit.tasks
/speckit.implement
```

**Delta 워크플로우**: 기존 명세서를 안전하게 수정하는 방식입니다.

---

## 📁 생성된 파일 구조

```
your-project/
├── .specify/
│   ├── specs/
│   │   ├── spec.md         # 기능 명세서
│   │   ├── tech-stack.md   # 사용 기술
│   │   ├── data-model.md   # 데이터 모델
│   │   └── contracts/      # API 스펙
│   └── features/
│       └── v1.0.0/2025_10_28-todo-app/
│           ├── plan.md     # 구현 계획
│           └── tasks.md    # 작업 목록
└── .cursor/
    ├── commands/           # Speckit 명령어
    └── rules/              # 워크플로우 규칙
```

**핵심**:
- `specs/` = 프로젝트 전체 설계 (계속 업데이트됨)
- `features/` = 각 기능의 구현 기록 (수정 안 함)

---

## 💡 자주 묻는 질문

### Q1. 기존 프로젝트에도 사용할 수 있나요?

**A**: 네! 언제든 설치 가능합니다.

```bash
cd existing-project
uvx custom-speckit init
# 기존 파일은 건드리지 않고 .specify/와 .cursor/만 추가됨
```

---

### Q2. 영어로 작성하고 싶어요

**A**: 영어로 입력하면 모든 문서가 영어로 생성됩니다.

```bash
# 영어 입력 → 영어 문서
/speckit.specify "Build a todo management app"

# 한글 입력 → 한글 문서
/speckit.specify "할 일 관리 앱 만들기"
```

**기본값**: 한국어

---

### Q3. 업데이트는 어떻게 하나요?

```bash
uvx custom-speckit update
```

**자동으로**:
- ✅ 최신 템플릿으로 업데이트
- ✅ 사용자 파일(spec.md 등)은 보존
- ✅ 백업 자동 생성

---

### Q4. 명세서를 수정하고 싶어요

**새 기능 추가**:
```bash
/speckit.specify "새 기능 설명"
/speckit.approve-delta  # 승인 후 병합
```

**직접 수정**:
```bash
vim .specify/specs/spec.md
# 직접 수정 가능 (작은 변경사항)
```

---

## 🌐 언어 자동 감지

Custom Speckit은 입력을 분석하여 자동으로 언어를 선택합니다:

```bash
# 한글 포함 → 한글 문서
/speckit.specify "OAuth2 인증 추가"

# 순수 영어 → 영어 문서
/speckit.specify "Add OAuth2 authentication"

# 빈 입력 → 한글 (기본값)
```

**일관성**: 한 번 정해진 언어는 프로젝트 전체에서 유지됩니다.

---

## 🐳 로컬 개발 서버 (선택)

팀 내부에서 사용하거나 오프라인 개발 시:

```bash
# 1. Custom Speckit 프로젝트에서
docker-compose up -d

# 2. 다른 프로젝트에서
uvx --index-url http://localhost:8080/simple/ custom-speckit init
```

---

## ❓ 도움이 필요하신가요?

- 📚 [상세 가이드](README-detailed.md) - 모든 기능과 개념 설명
- 💬 [GitHub Issues](https://github.com/David-Lee-dev/custom-speckit/issues) - 버그 리포트 및 질문
- 📖 [GitHub Spec-Kit](https://github.com/github/spec-kit) - 원본 프로젝트

---

## 🚀 다음 단계

1. **Constitution 작성하기** - 프로젝트 원칙 정의
2. **첫 기능 만들기** - `/speckit.specify`로 시작
3. **상세 가이드 읽기** - [README-detailed.md](README-detailed.md)에서 모든 기능 배우기

---

<div align="center">

**Custom Speckit으로 더 나은 개발 경험을!** 🎯

[⬆ 맨 위로](#-custom-speckit---빠른-시작-가이드)

</div>

