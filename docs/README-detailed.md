# 📚 Custom Speckit - 완전 가이드

> Spec-Driven Development의 모든 것

[← 메인으로](../README.md) | [🚀 빠른 시작](README-simple.md)

---

## 목차

1. [Spec-Driven Development란?](#-spec-driven-development란)
2. [왜 기획서를 먼저 작성해야 하나요?](#-왜-기획서를-먼저-작성해야-하나요)
3. [Custom Speckit 특징](#-custom-speckit-특징)
4. [설치 방법](#-설치-방법)
5. [Constitution 작성 가이드](#-constitution-작성-가이드)
6. [개발 워크플로우](#-개발-워크플로우)
7. [전체 명령어 레퍼런스](#-전체-명령어-레퍼런스)
8. [개발 시나리오](#-개발-시나리오)
9. [디렉토리 구조](#-디렉토리-구조)
10. [Git 워크플로우](#-git-워크플로우)
11. [언어 자동 감지](#-언어-자동-감지)
12. [고급 기능](#-고급-기능)
13. [트러블슈팅](#-트러블슈팅)
14. [FAQ](#-faq)

---

## 💡 Spec-Driven Development란?

**Spec-Driven Development (명세 주도 개발)**는 코드를 작성하기 전에 명세서를 먼저 작성하는 개발 방식입니다.

### 기본 원칙

```
명세서 작성 → 설계 → 구현 → 테스트
    ↑                           ↓
    └───────────── 피드백 ────────┘
```

### 전통적 개발 vs Spec-Driven Development

#### ❌ **전통적 개발 방식**
```
아이디어 → 바로 코딩 → 문제 발견 → 수정 → 또 수정 → ...
```

**문제점**:
- 방향성 없이 코드 작성
- 요구사항 누락 발견이 늦음
- 리팩토링 반복
- AI가 잘못된 방향으로 코드 생성

#### ✅ **Spec-Driven Development**
```
명세서 작성 → 설계 검증 → 코드 생성 → 테스트
```

**장점**:
- 📝 **명확한 목표**: 무엇을 만들지 먼저 정의
- 🤖 **AI 최적화**: AI가 정확한 방향으로 코드 생성
- 🔍 **조기 발견**: 요구사항 문제를 코딩 전 발견
- 📊 **추적 가능**: 모든 결정의 이유 기록
- 👥 **협업 용이**: 팀원 모두 같은 그림 공유

### GitHub의 Spec-Kit

Custom Speckit은 [GitHub Spec-Kit](https://github.com/github/spec-kit)을 기반으로 만들어졌습니다. GitHub에서 공식적으로 권장하는 AI 시대의 개발 방식입니다.

---

## 📋 왜 기획서를 먼저 작성해야 하나요?

### 1. AI와의 협업이 훨씬 효율적입니다

**기획서 없이 개발**:
```
개발자: "로그인 기능 만들어줘"
AI: [코드 생성]
개발자: "아니 OAuth도 지원해야 하는데..."
AI: [전체 수정]
개발자: "세션 유지는?"
AI: [또 수정]
...
```
→ 계속된 수정과 리팩토링

**기획서 먼저 작성**:
```
개발자: "로그인 기능 명세 작성"
        - 이메일/비밀번호 로그인
        - OAuth2 (Google, GitHub)
        - 세션 7일 유지
        - 자동 로그인 옵션
AI: [명세 기반으로 정확한 코드 생성]
```
→ 한 번에 정확하게

---

### 2. 요구사항 누락을 조기에 발견합니다

**Before (코딩 후 발견)**:
```
코딩 3일 → "어? 비밀번호 찾기 기능이 없네?" → 다시 설계 → 코드 수정
```

**After (기획 단계 발견)**:
```
기획 1시간 → "비밀번호 찾기 필요" → 명세에 추가 → 처음부터 올바르게 구현
```

**시간 절약**: 코딩 후 수정은 10배 더 오래 걸립니다.

---

### 3. 프로젝트 전체를 일관되게 유지합니다

**명세서가 Single Source of Truth** 역할:
- 모든 팀원이 같은 목표 공유
- 데이터 모델 중복 방지
- API 설계 일관성 유지
- 기술 스택 충돌 방지

---

### 4. 변경 이력을 추적할 수 있습니다

```
.specify/specs/
├── spec.md          # 현재 명세 (모든 기능)
├── tech-stack.md    # 기술 변경 이력 포함
└── CHANGELOG.md     # 변경 기록

.specify/features/
├── v1.0.0/2025_10_28-todo-app/    # 첫 개발
├── v1.1.0/2025_11_05-comment/     # 댓글 추가
└── v1.2.0/2025_11_20-search/      # 검색 추가
```

**이점**:
- 왜 이 결정을 했는지 기록
- 언제 무엇이 추가되었는지 추적
- 새 팀원 온보딩 쉬움

---

## 🎯 Custom Speckit 특징

### Delta 기반 변경 관리

기존 Spec-Kit과의 **가장 큰 차이점**:

```
기존 Spec-Kit:
specs/001-feature/spec.md
specs/002-feature/spec.md  # 명세가 분산됨
specs/003-feature/spec.md

Custom Speckit:
specs/spec.md  # 단일 진실의 원천
.deltas/new-feature/  # 변경사항만 (임시)
→ 승인 후 spec.md에 병합
```

**장점**:
- ✅ 명세서가 단일 파일로 통합
- ✅ 변경사항을 Delta로 검토
- ✅ 승인 후 안전하게 병합
- ✅ CHANGELOG 자동 기록

---

### 자동 언어 감지

```bash
# 한글 → 모든 문서 한글
/speckit.specify "사용자 관리"

# English → All docs in English
/speckit.specify "User management"
```

**기본값**: 한국어

---

### 버전별 이력 관리

```
features/
├── v1.0.0/2025_10_28-todo-app/
├── v1.1.0/2025_11_05-comment/
└── v1.2.0/2025_11_20-search/
```

각 버전의 구현 계획과 작업 목록이 보존됩니다.

---

## 📦 설치 방법

### 방법 1: 로컬 개발 (Docker)

PyPI 계정 없이 로컬에서 사용:

```bash
# Custom Speckit 프로젝트에서
cd custom-speckit
docker-compose up -d              # 로컬 PyPI 서버
./scripts/upload-local.sh         # 패키지 업로드

# 사용자 프로젝트에서
cd /path/to/your-project
uvx --index-url http://localhost:8080/simple/ custom-speckit init

# 업데이트
uvx --index-url http://localhost:8080/simple/ custom-speckit update
```

---

### 방법 2: GitHub에서 직접 설치

```bash
cd your-project
uvx --from git+https://github.com/David-Lee-dev/custom-speckit.git@main custom-speckit init
```

---

### 방법 3: PyPI 배포 (추후)

```bash
pip install custom-speckit
custom-speckit init
```

---

## 📖 Constitution 작성 가이드

**Constitution**은 프로젝트의 헌법입니다. AI가 코드를 작성할 때 반드시 따라야 할 원칙을 정의합니다.

### 왜 필요한가요?

**Constitution 없이**:
```
AI: "사용자 데이터를 localStorage에 저장했습니다"
→ 보안 문제!
```

**Constitution 있으면**:
```
Constitution: "민감한 데이터는 암호화 필수"
AI: "사용자 데이터를 암호화하여 secure storage에 저장했습니다"
→ 안전!
```

---

### 작성 방법

#### 1. 기본 템플릿 사용

```bash
/speckit.constitution
```

AI가 대화형으로 질문하며 Constitution을 작성해줍니다.

---

#### 2. 직접 작성

```bash
vim .specify/memory/constitution.md
```

**예시 - Todo 앱의 Constitution**:

```markdown
# Todo App Constitution

## Core Principles

### I. User Privacy First
- 사용자 데이터는 절대 외부로 유출되지 않습니다
- 모든 민감 정보는 암호화하여 저장합니다
- 로그에 개인정보를 남기지 않습니다

### II. Offline First
- 인터넷 없이도 기본 기능 동작해야 합니다
- 로컬 우선 저장, 동기화는 백그라운드
- 충돌 해결 전략 필수

### III. Test-Driven Development
- 모든 기능은 테스트 코드 포함 필수
- 테스트 커버리지 80% 이상 유지
- E2E 테스트로 핵심 시나리오 검증

### IV. Simple & Fast
- 복잡한 기능보다 단순한 UX 우선
- 페이지 로드 1초 이내
- 애니메이션 60fps 유지

## Technology Constraints

### Must Use
- TypeScript (JavaScript ❌)
- React 18+
- PostgreSQL

### Must NOT Use
- Class components (함수형만)
- any 타입 (타입 명시 필수)
- inline styles (CSS modules 사용)

## Governance

- Constitution 위반 시 코드 리뷰 거부
- 예외는 명시적 승인 필요
- 분기별 Constitution 검토

**Version**: 1.0.0 | **Ratified**: 2025-10-28
```

---

### Constitution 작성 팁

1. **구체적으로**: "품질 좋게" ❌ → "테스트 커버리지 80% 이상" ✅
2. **강제력 명시**: MUST, SHOULD, MAY 구분
3. **이유 포함**: 왜 이 원칙이 필요한지
4. **측정 가능**: 정량적 기준 제시

---

## 🔄 개발 워크플로우

### 전체 흐름

```
┌─────────────────────────────────────────┐
│ 1. Constitution 작성 (프로젝트 원칙)      │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ 2. /speckit.specify "요구사항"           │
│    → specs/spec.md 생성                 │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ 3. /speckit.plan                        │
│    → specs/tech-stack.md               │
│    → specs/data-model.md               │
│    → specs/contracts/                  │
│    → features/{v}/{date}-{branch}/plan.md │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ 4. /speckit.tasks                       │
│    → features/{v}/{date}-{branch}/tasks.md │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ 5. /speckit.implement                   │
│    → 실제 코드 작성                      │
└─────────────────────────────────────────┘
```

---

## 📖 전체 명령어 레퍼런스

### 핵심 워크플로우 명령어

#### `/speckit.specify`

**용도**: 기능 명세서 생성 또는 수정

**입력**: 자연어로 작성한 요구사항
```bash
/speckit.specify "할 일 관리 앱을 만들고 싶어요. 할 일 추가, 완료 표시, 삭제 기능이 필요합니다."
```

**출력**:
- 신규 프로젝트: `.specify/specs/spec.md`
- 기존 프로젝트: `.specify/.deltas/{branch}/delta-spec.md`

**생성되는 내용**:
- 기능 개요
- 사용자 스토리 (Priority 포함)
- 기능 요구사항
- 비기능 요구사항
- 성공 기준
- 핵심 엔티티

**언어**: 입력 언어 자동 감지 (한글/영어)

**예시 출력** (한글 입력 시):
```markdown
# 기능 명세서: 할 일 관리 앱

## 개요
사용자가 할 일을 효율적으로 관리할 수 있는 애플리케이션

## 사용자 스토리

### US1: 할 일 추가 (P1) 🎯 MVP
사용자로서, 할 일을 빠르게 추가하여 잊지 않고 관리하고 싶습니다.

**수락 기준**:
- [ ] 제목 입력 후 Enter로 할 일 추가
- [ ] 빈 제목은 추가 불가
- [ ] 추가 후 입력창 자동 초기화
...
```

---

#### `/speckit.plan`

**용도**: 구현 계획 수립 및 기술 스펙 생성

**입력**: (자동으로 spec.md 읽음)

**출력**:
- `.specify/specs/tech-stack.md` - 기술 스택 결정
- `.specify/specs/data-model.md` - 데이터 모델 설계
- `.specify/specs/contracts/` - API 스펙 정의
- `.specify/features/{v}/{date}-{branch}/plan.md` - 구현 계획

**생성되는 tech-stack.md 예시**:
```markdown
# Technology Stack

## Backend
- Node.js 20.x - 서버 런타임
- Express 4.x - 웹 프레임워크
- PostgreSQL 15.x - 메인 데이터베이스

**Initial Decision**: 2025-10-28 (todo-app)

## Frontend
- React 18.x - UI 프레임워크
- TypeScript 5.x - 타입 안정성
- Tailwind CSS 3.x - 스타일링

**Initial Decision**: 2025-10-28 (todo-app)
```

**Phase 구성**:
- Phase 0: 기술 스택 조사 및 결정
- Phase 1: 데이터 모델 및 API 설계
- Phase 2: 구현 계획 작성

---

#### `/speckit.tasks`

**용도**: 작업 목록을 구체적으로 분해

**입력**: (plan.md와 specs/ 파일들 읽음)

**출력**:
- `.specify/features/{v}/{date}-{branch}/tasks.md`

**생성되는 tasks.md 예시**:
```markdown
# Tasks: 할 일 관리 앱

## Phase 1: Setup

- [ ] T001 프로젝트 구조 생성
- [ ] T002 [P] Node.js 프로젝트 초기화
- [ ] T003 [P] React 앱 초기화

## Phase 2: Foundational

- [ ] T004 데이터베이스 스키마 생성
- [ ] T005 [P] API 라우팅 설정
- [ ] T006 [P] 에러 핸들링 미들웨어

## Phase 3: User Story 1 - 할 일 추가 (P1) 🎯 MVP

**Goal**: 사용자가 할 일을 추가할 수 있다

- [ ] T007 [P] [US1] Task 모델 생성 in src/models/task.ts
- [ ] T008 [US1] Task 생성 API in src/api/tasks.ts
- [ ] T009 [US1] Task 입력 컴포넌트 in src/components/TaskInput.tsx
- [ ] T010 [US1] 유효성 검증 추가
```

**특징**:
- User Story별로 그룹화
- `[P]` = 병렬 실행 가능
- 파일 경로 명시
- 체크박스로 진행 추적

---

#### `/speckit.implement`

**용도**: tasks.md를 기반으로 실제 코드 구현

**입력**: (tasks.md 읽음)

**출력**: 소스 코드, 테스트, 문서

**동작**:
1. tasks.md 파싱
2. 순서대로 작업 실행
3. 파일 생성/수정
4. 테스트 실행
5. 에러 처리

**주의**: 로컬에 필요한 도구(Node.js, Python 등) 설치 필요

---

### Delta 관리 명령어

#### `/speckit.review-delta`

**용도**: Delta 변경사항 분석

**출력**: 분석 리포트
- 변경 통계
- 영향 분석
- Constitution 검증
- 리스크 평가

---

#### `/speckit.approve-delta`

**용도**: Delta를 spec.md에 병합

**동작**:
1. spec.md 백업 생성
2. Delta 병합
3. CHANGELOG 기록
4. Delta 폴더 삭제

---

#### `/speckit.reject-delta`

**용도**: Delta 거부 및 삭제

**동작**:
1. Delta 아카이브 (선택)
2. Delta 폴더 삭제
3. spec.md 변경 없음

---

### 품질 관리 명령어

#### `/speckit.analyze`

**용도**: spec/plan/tasks 교차 검증

**검증 항목**:
- 요구사항 누락
- 중복 항목
- 불일치 사항
- 모호한 표현

---

#### `/speckit.checklist`

**용도**: 요구사항 품질 검증

**생성**: 체크리스트
- 완전성 검사
- 명확성 검사
- 테스트 가능성

---

#### `/speckit.clarify`

**용도**: 불명확한 부분 질문 및 해결

**동작**:
1. 명세서에서 모호한 부분 추출
2. 선택지 제시
3. 답변 받아 spec.md 업데이트

---

## 🔄 개발 시나리오

### 시나리오 1: 처음 프로젝트 시작

#### 상황
완전히 새로운 프로젝트를 시작합니다.

#### 단계별 가이드

**1. Constitution 작성 (10분)**

```bash
# Constitution 생성
/speckit.constitution
```

AI가 질문을 하면 답변:
```
Q1: 프로젝트의 핵심 원칙은?
A: 사용자 프라이버시, 오프라인 우선, 테스트 필수

Q2: 기술 제약사항은?
A: TypeScript 필수, React 사용, PostgreSQL

Q3: 품질 기준은?
A: 테스트 커버리지 80%, 페이지 로드 1초 이내
```

**결과**: `.specify/memory/constitution.md` 생성

---

**2. 기능 명세 작성 (20분)**

```bash
/speckit.specify "할 일 관리 앱을 만들고 싶어요.

주요 기능:
1. 할 일 추가/수정/삭제
2. 완료 표시 토글
3. 카테고리별 분류
4. 우선순위 설정
5. 마감일 알림

사용자:
- 개인 사용자 (회원가입 필요 없음)
- 로컬 스토리지 사용"
```

**AI 작업**:
- 요구사항 분석
- 사용자 스토리 생성 (US1, US2, ...)
- 우선순위 부여 (P1: MVP, P2, P3...)
- 수락 기준 작성
- 핵심 엔티티 추출

**생성**: `.specify/specs/spec.md`

**검토**: spec.md 열어서 확인
```bash
cat .specify/specs/spec.md
```

불명확한 부분이 있다면:
```bash
/speckit.clarify
```

---

**3. 구현 계획 수립 (15분)**

```bash
/speckit.plan
```

**AI 작업**:
- 기술 스택 결정 (Phase 0)
- 데이터 모델 설계 (Phase 1)
- API 스펙 정의 (Phase 1)
- 구현 단계 계획 (Phase 2)

**생성**:
```
specs/
├── tech-stack.md    # React, Node.js, PostgreSQL
├── data-model.md    # Task, Category 엔티티
└── contracts/       # task.yaml, category.yaml

features/v1.0.0/2025_10_28-todo-app/
└── plan.md          # 구현 계획
```

**검토**:
```bash
cat .specify/specs/tech-stack.md
cat .specify/specs/data-model.md
cat .specify/features/v1.0.0/*/plan.md
```

기술 스택이 마음에 안 든다면 직접 수정:
```bash
vim .specify/specs/tech-stack.md
```

---

**4. 작업 목록 생성 (5분)**

```bash
/speckit.tasks
```

**AI 작업**:
- User Story별 작업 분해
- 의존성 순서 정리
- 병렬 실행 가능 작업 표시
- 파일 경로 명시

**생성**:
```
features/v1.0.0/2025_10_28-todo-app/
└── tasks.md
```

**예시**:
```markdown
## Phase 3: User Story 1 - 할 일 추가 (P1)

- [ ] T007 [P] [US1] Task 모델 in src/models/Task.ts
- [ ] T008 [P] [US1] Task API in src/api/tasks.ts
- [ ] T009 [US1] TaskInput 컴포넌트 in src/components/TaskInput.tsx
```

**검증**: 분석 실행
```bash
/speckit.analyze
```

---

**5. 구현 실행 (AI가 자동)**

```bash
/speckit.implement
```

**AI 작업**:
- T001부터 순서대로 실행
- 파일 생성 및 코드 작성
- 테스트 작성 (TDD)
- 의존성 설치
- 빌드 및 검증

**진행 상황 확인**:
```bash
# tasks.md에서 체크박스 확인
cat .specify/features/v1.0.0/*/tasks.md
```

**완료 후**:
```bash
# 앱 실행 및 테스트
npm start
npm test
```

---

### 시나리오 2: 기존 프로젝트에 기능 추가

#### 상황
Todo 앱에 댓글 기능을 추가합니다.

#### 단계별 가이드

**1. Delta 생성**

```bash
/speckit.specify "각 할 일에 댓글을 달 수 있는 기능을 추가하고 싶어요.

요구사항:
- 할 일당 여러 개 댓글 가능
- 댓글 작성 시간 표시
- 댓글 수정/삭제 가능
- 실시간 업데이트 (다른 사용자 댓글도 보임)"
```

**AI 작업**:
- 기존 spec.md 읽기
- 변경사항만 추출
- delta-spec.md 생성

**생성**:
```
.specify/.deltas/comment-feature/
├── delta-spec.md
├── changes-summary.md
└── review-checklist.md
```

---

**2. Delta 검토 (선택)**

```bash
/speckit.review-delta
```

**AI 리포트**:
```markdown
# Delta Review: 댓글 기능

## 변경 통계
- ✅ Added: 3 user stories
- 🔄 Modified: 1 requirement
- ❌ Removed: 0

## 주요 변경사항
1. 새 User Story: US4-댓글 작성
2. 새 User Story: US5-댓글 수정
3. 기존 Task 엔티티에 commentCount 필드 추가

## Constitution 검증
✅ All checks passed

## 권장사항
- 실시간 업데이트는 복잡도 증가
- WebSocket vs Polling 고려 필요
```

**Delta 직접 수정 가능**:
```bash
vim .specify/.deltas/comment-feature/delta-spec.md
```

---

**3. Delta 승인**

```bash
/speckit.approve-delta
```

**AI 작업**:
- spec.md 백업
- Delta 병합
- CHANGELOG 기록
- Delta 폴더 삭제

**결과**:
```
specs/
├── spec.md          # 댓글 요구사항 포함됨
├── .backups/
│   └── spec_backup_20251105_140532_comment-feature.md
└── CHANGELOG.md     # 변경 기록
```

---

**4. 계획 및 구현**

```bash
/speckit.plan
```

**AI 작업**:
- tech-stack.md 확인 (WebSocket 추가 필요 여부)
- data-model.md에 Comment 엔티티 추가
- contracts/에 comment.yaml 추가
- plan.md 생성 (댓글 기능 구현 계획)

**생성**:
```
specs/
├── tech-stack.md    # Socket.io 추가됨
├── data-model.md    # Comment 엔티티 추가
└── contracts/
    └── comment.yaml # 신규

features/v1.1.0/2025_11_05-comment-feature/
└── plan.md
```

**tech-stack.md 업데이트 예시**:
```markdown
## Real-time Communication
- Socket.io 4.x - 실시간 댓글 동기화
  * Added: 2025_11_05 (comment-feature)
  * Reason: 댓글 실시간 업데이트 요구사항
```

**data-model.md 업데이트 예시**:
```markdown
## Comment
- id: UUID
- task_id: UUID (FK → Task)
- content: string
- created_at: timestamp
- updated_at: timestamp

**Added**: 2025_11_05 (comment-feature)
**Purpose**: 할 일별 댓글 기능
```

**이후 단계**:
```bash
/speckit.tasks
/speckit.implement
```

---

### 시나리오 3: 기술 스택 변경

#### 상황
검색 기능을 위해 Elasticsearch를 도입합니다.

#### 단계

**1. 요구사항 추가**

```bash
/speckit.specify "할 일을 빠르게 검색하는 기능이 필요해요. 제목, 내용, 태그로 검색하고 자동완성도 지원해야 합니다."
/speckit.approve-delta
```

---

**2. 계획 수립 (기술 변경 포함)**

```bash
/speckit.plan
```

**AI 판단**:
- "전문 검색 필요 → Elasticsearch 도입"
- tech-stack.md에 Elasticsearch 추가
- data-model.md에 SearchIndex 추가

**tech-stack.md 업데이트**:
```markdown
## Search Engine
- Elasticsearch 8.x - 전문 검색 엔진
  * Added: 2025_11_20 (search-feature)
  * Reason: 복잡한 검색 쿼리 및 자동완성 최적화
  * Alternative considered: PostgreSQL Full-Text Search (성능 부족)
```

**data-model.md 업데이트**:
```markdown
## SearchIndex (Elasticsearch)
- task_id: UUID
- title: text (analyzed)
- content: text (analyzed)
- tags: keyword[]
- suggest: completion

**Added**: 2025_11_20 (search-feature)
**Purpose**: 빠른 검색 및 자동완성
```

---

**3. 구현**

```bash
/speckit.tasks
/speckit.implement
```

**최종 구조**:
```
specs/
├── spec.md          # Todo + Comment + Search
├── tech-stack.md    # Node, React, PostgreSQL, Elasticsearch
├── data-model.md    # Task, Comment, SearchIndex
└── contracts/
    ├── task.yaml
    ├── comment.yaml
    └── search.yaml

features/
├── v1.0.0/2025_10_28-todo-app/
├── v1.1.0/2025_11_05-comment-feature/
└── v1.2.0/2025_11_20-search-feature/
```

---

## 📁 디렉토리 구조

### 전체 구조

```
your-project/
├── .specify/
│   ├── specs/              # 프로젝트 뼈대 (누적 관리)
│   │   ├── spec.md         # 전체 기능 명세
│   │   ├── tech-stack.md   # 기술 스택 (변경 이력 포함)
│   │   ├── data-model.md   # 전체 데이터 모델
│   │   ├── contracts/      # API 계약
│   │   ├── CHANGELOG.md    # 명세 변경 기록
│   │   └── .backups/       # 자동 백업
│   │
│   ├── .deltas/            # 임시 변경사항 (.gitignore)
│   │   └── {branch}/
│   │       ├── delta-spec.md
│   │       ├── changes-summary.md
│   │       └── review-checklist.md
│   │
│   ├── features/           # Feature 구현 기록
│   │   └── {version}/
│   │       └── {YYYY_MM_DD-branch}/
│   │           ├── plan.md
│   │           └── tasks.md
│   │
│   ├── memory/
│   │   └── constitution.md
│   │
│   ├── scripts/bash/       # 헬퍼 스크립트
│   └── templates/          # 문서 템플릿
│
└── .cursor/
    ├── commands/           # Speckit 명령어
    └── rules/              # 워크플로우 규칙
```

---

### 디렉토리 역할

#### **specs/ - 프로젝트 뼈대**

**역할**: 프로젝트 전반에 걸친 기술 스펙 중앙 관리

**특징**:
- ✅ 버전 디렉토리 없음 (항상 최신 상태)
- ✅ 누적 업데이트 (변경 이력은 파일 내부에 기록)
- ✅ 전체 프로젝트가 참조하는 Single Source of Truth
- ✅ Git으로 변경 추적

**파일**:
- `spec.md` - 전체 기능 명세 (Delta 워크플로우로 관리)
- `tech-stack.md` - 사용 기술/툴 (직접 수정, 이력 기록)
- `data-model.md` - 전체 엔티티 (추가 시 append)
- `contracts/` - 모든 API 스펙 (추가 시 파일 추가)

**변경 방법**:
```bash
# spec.md: Delta 워크플로우
/speckit.specify "새 기능"
/speckit.approve-delta

# 나머지: 직접 수정
vim .specify/specs/tech-stack.md
vim .specify/specs/data-model.md
```

---

#### **features/ - Feature 구현 기록**

**역할**: 각 feature의 구현 계획과 작업 목록 보존

**특징**:
- ✅ 버전/날짜별 디렉토리 분리
- ✅ 한 번 생성 후 수정 안 함 (스냅샷)
- ✅ 이력 보존용
- ✅ specs/의 파일들을 참조

**파일**:
- `plan.md` - 이 feature의 구현 계획
- `tasks.md` - 이 feature의 작업 목록

**명명 규칙**:
```
{VERSION}/{YYYY_MM_DD-branch}/
         └─ 날짜(언더스코어) - 브랜치(하이픈)

예시:
v1.0.0/2025_10_28-todo-app/
v1.1.0/2025_11_05-comment-feature/
```

---

## 🌿 Git 워크플로우

### Feature 개발 전체 과정

```bash
# 1. 브랜치 생성
git checkout -b user-auth

# 2. Speckit 워크플로우
/speckit.specify "사용자 인증 기능"
/speckit.plan
/speckit.tasks
/speckit.implement

# 디렉토리 자동 생성됨:
# features/v1.0.0/2025_10_28-user-auth/

# 3. Commit
git add src/auth/ .specify/
git commit -m "[Feature] 사용자 인증 기능 구현

- JWT 토큰 기반 인증
- 로그인/로그아웃 API
- 인증 미들웨어 추가
- 토큰 갱신 로직"

# 4. Push
git push origin user-auth
```

---

### Commit 메시지 규칙

**형식**:
```
[Type] 간결한 제목 (50자 이내)

- 상세 내용 1
- 상세 내용 2
- 상세 내용 3
```

**Type**:
- `[Feature]` - 새 기능 추가
- `[Fix]` - 버그 수정
- `[Refactor]` - 코드 개선
- `[Docs]` - 문서 변경
- `[Test]` - 테스트 추가
- `[Chore]` - 빌드/설정
- `[Release]` - 버전 릴리스

**예시**:
```
[Feature] OAuth2 인증 추가

- Google OAuth2 통합
- GitHub OAuth2 통합  
- 소셜 로그인 UI 컴포넌트
- 토큰 관리 서비스
```

**자세한 규칙**: 프로젝트의 `.cursor/rules/git-commit-guidelines.mdc` 참조

---

### Feature 디렉토리와 브랜치 매칭

**규칙**: 디렉토리명의 브랜치 부분 = Git 브랜치명

```
✅ CORRECT:
디렉토리: 2025_10_28-user-auth
브랜치:   user-auth

❌ WRONG:
디렉토리: 2025_10_28-user-auth
브랜치:   user-authentication
```

**검증**:
```bash
# 현재 브랜치
git branch --show-current

# Feature 디렉토리
ls .specify/features/v*/
```

---

## 🌐 언어 자동 감지

### 감지 규칙

Custom Speckit은 사용자 입력을 분석하여 자동으로 언어를 선택합니다:

**한글 감지**:
```bash
/speckit.specify "사용자 인증"
/speckit.specify "OAuth2 인증 시스템"
/speckit.specify "Add OAuth2 인증"  # 한글 포함

→ 모든 문서가 한글로 생성됨
```

**영어 감지**:
```bash
/speckit.specify "Add user authentication"
/speckit.specify "Build OAuth2 system"

→ All documents generated in English
```

**기본값**: 한국어 (빈 입력, 애매한 경우)

---

### 언어 일관성

한 번 정해진 언어는 프로젝트 전체에서 유지됩니다:

```
spec.md (한글로 작성됨)
    ↓
plan.md (자동으로 한글)
    ↓
tasks.md (자동으로 한글)
    ↓
코드 주석 (한글)
```

**코드는 항상 영어**:
- 변수명, 함수명, 클래스명
- 기술 식별자
- 파일명

---

## 🔧 고급 기능

### 1. Constitution 업데이트

```bash
/speckit.constitution "새 원칙 추가: 모든 API는 rate limiting 필수"
```

---

### 2. 명세서 명확화

명세서에 불명확한 부분이 있을 때:

```bash
/speckit.clarify
```

AI가 질문하고 답변을 받아 spec.md를 업데이트합니다.

---

### 3. 품질 검증

```bash
# 전체 일관성 검사
/speckit.analyze

# 요구사항 품질 검사
/speckit.checklist
```

---

### 4. 로컬 PyPI 서버 (팀 공유)

```bash
# Custom Speckit 프로젝트에서
docker-compose up -d

# 같은 네트워크의 다른 컴퓨터에서
uvx --index-url http://192.168.1.100:8080/simple/ custom-speckit init
```

**활용**:
- 팀 내부 배포
- 오프라인 개발
- 빠른 테스트

---

## 🐛 트러블슈팅

### "Already on the latest version" 계속 표시

**원인**: uvx 캐시

**해결**:
```bash
rm -rf ~/.local/share/uv/cache/
uvx --index-url http://localhost:8080/simple/ --refresh custom-speckit update
```

---

### Delta 승인 후에도 spec.md 변경 안 됨

**확인**:
```bash
# 백업 확인
ls .specify/specs/.backups/

# CHANGELOG 확인
cat .specify/specs/CHANGELOG.md
```

**해결**: `/speckit.approve-delta` 다시 실행

---

### Git 브랜치와 디렉토리 이름 불일치

**증상**:
```
브랜치: user-auth
디렉토리: 2025_10_28-authentication
```

**해결**: 브랜치명과 디렉토리명 일치시키기
```bash
# 브랜치 이름 변경
git branch -m user-auth authentication

# 또는 디렉토리 수동 이름 변경 (권장 안 함)
```

---

### 특정 기술 스택 강제 지정

**AI가 다른 기술을 선택했을 때**:

```bash
# plan.md에서 명시
vim .specify/features/v1.0.0/*/plan.md
```

또는 Constitution에 추가:
```markdown
## Technology Constraints

### Must Use
- PostgreSQL (MySQL ❌)
- React (Vue ❌)
```

---

## ❓ FAQ

### 일반

**Q: 어떤 프로젝트에 사용할 수 있나요?**

A: 모든 프로젝트! 언어/프레임워크 무관
- ✅ Node.js, Python, Go, Rust
- ✅ React, Vue, Svelte
- ✅ Web, Mobile, Desktop
- ✅ 기존 프로젝트, 신규 프로젝트

---

**Q: 기존 파일이 삭제되나요?**

A: 아니요. Custom Speckit은 `.specify/`와 `.cursor/`만 관리합니다.
- `package.json`, `Cargo.toml` → 건드리지 않음
- `src/`, `tests/` → 건드리지 않음

---

**Q: 팀에서 함께 사용할 수 있나요?**

A: 네!
```bash
# .specify/와 .cursor/를 Git에 커밋
git add .specify/ .cursor/
git commit -m "[Chore] Speckit 설정 추가"
git push

# 팀원이 Pull
git pull
# → 바로 /speckit 명령어 사용 가능
```

---

**Q: Constitution이 꼭 필요한가요?**

A: 선택사항이지만 **강력히 권장**합니다.

**Constitution 없으면**:
- AI가 일관성 없는 코드 생성
- 보안/성능 기준 없음
- 코드 스타일 뒤죽박죽

**Constitution 있으면**:
- AI가 프로젝트 원칙 준수
- 일관된 품질 유지
- 리뷰 시간 단축

---

### 명령어 관련

**Q: /speckit 명령어가 안 보여요**

A: `.cursor/commands/` 디렉토리 확인
```bash
ls .cursor/commands/
# speckit.specify.md 등이 있어야 함

# 없다면 재설치
uvx custom-speckit init
```

---

**Q: Delta를 승인하지 않고 바로 plan으로 가면?**

A: 에러 발생
```
ERROR: Delta pending approval
→ Run /speckit.approve-delta first
```

Delta는 **반드시 승인** 후 진행해야 합니다.

---

**Q: tasks.md의 체크박스를 수동으로 체크해야 하나요?**

A: 아니요. `/speckit.implement`가 자동으로 실행하고 체크합니다.
- 수동 체크: 수동 구현 시
- 자동 체크: `/speckit.implement` 사용 시

---

**Q: 명세서를 나중에 수정할 수 있나요?**

A: 네! 두 가지 방법:
1. **Delta 워크플로우** (권장):
   ```bash
   /speckit.specify "수정 내용"
   /speckit.approve-delta
   ```

2. **직접 수정**:
   ```bash
   vim .specify/specs/spec.md
   ```

---

### 파일 위치

**Q: data-model.md는 어디에 있나요?**

A: `.specify/specs/data-model.md` (프로젝트 전체 데이터 모델)

**이전 버전**에서는 `features/`에 있었지만, **v1.3.2부터** `specs/`로 이동했습니다.

---

**Q: research.md가 없어요**

A: **v1.3.2부터** `tech-stack.md`로 이름이 변경되었습니다.
- 위치: `.specify/specs/tech-stack.md`
- 내용: 기술 스택 및 결정 이유

---

## 🎓 Best Practices

### 1. Constitution은 구체적으로

❌ **나쁜 예**:
```markdown
### I. Code Quality
코드는 깨끗해야 합니다.
```

✅ **좋은 예**:
```markdown
### I. Code Quality
- 모든 함수는 단일 책임 원칙 준수
- 테스트 커버리지 80% 이상 필수
- 순환 복잡도 10 이하 유지
- ESLint 에러 0개 (경고 허용)
```

---

### 2. 명세서는 기술 용어 최소화

❌ **나쁜 예**:
```markdown
사용자가 JWT 토큰으로 인증하면 Redux store에 저장
```

✅ **좋은 예**:
```markdown
사용자가 로그인하면 인증 상태가 유지됩니다
```

**이유**: 명세서는 "무엇"이지 "어떻게"가 아닙니다.

---

### 3. 작은 단위로 자주 커밋

```bash
# User Story 1 완료 후
git commit -m "[Feature] US1 할 일 추가 기능 구현"

# User Story 2 완료 후
git commit -m "[Feature] US2 완료 표시 기능 구현"
```

**이점**:
- 리뷰 쉬움
- 롤백 쉬움
- 이력 명확

---

### 4. Delta는 리뷰 후 승인

```bash
/speckit.specify "새 기능"
/speckit.review-delta     # ← 꼭 리뷰하기
# 검토 후
/speckit.approve-delta
```

**이유**: 잘못된 변경사항 조기 발견

---

## 📚 참고 자료

- [GitHub Spec-Kit](https://github.com/github/spec-kit) - 원본 프로젝트
- [uv 공식 문서](https://docs.astral.sh/uv/) - uv 사용법
- [Cursor AI](https://docs.cursor.com/) - Cursor AI 문서
- [Spec-Driven Design 블로그](https://devjino.tistory.com/435) - 개념 설명

---

## 🙏 기여하기

Custom Speckit은 오픈소스 프로젝트입니다!

```bash
# 버그 리포트
https://github.com/David-Lee-dev/custom-speckit/issues

# Pull Request 환영
git clone https://github.com/David-Lee-dev/custom-speckit.git
```

---

## 📄 라이선스

MIT License - Based on [GitHub Spec-Kit](https://github.com/github/spec-kit)

---

<div align="center">

**Custom Speckit과 함께 더 나은 개발 경험을!** 🚀

[⬆ 맨 위로](#-custom-speckit---완전-가이드) | [🚀 빠른 시작](README-simple.md) | [← 메인으로](../README.md)

</div>

