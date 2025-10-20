# Custom Speckit 🚀

> AI 기반 Spec-Driven Development를 위한 향상된 워크플로우

Custom Speckit은 [GitHub Spec-Kit](https://github.com/github/spec-kit)을 기반으로, 프로젝트의 명세서를 **단일 진실의 원천**으로 관리하고, 변경사항을 **Delta 방식**으로 추적하여 안전하게 개선할 수 있도록 만든 도구입니다.

## 📌 왜 Custom Speckit인가?

### 기존 Spec-Kit의 문제점
- ✗ 각 feature마다 spec.md를 새로 생성 → **중복 및 불일치 발생**
- ✗ 기존 프로젝트 개선 시 전체 spec을 다시 생성 → **비효율적**
- ✗ 변경사항 추적 불가 → **이력 관리 어려움**
- ✗ spec 검토 단계 없음 → **실수 발견 어려움**

### Custom Speckit의 해결책
- ✓ **단일 spec.md** - 프로젝트의 유일한 명세서, AI context로 최적
- ✓ **Delta 워크플로우** - 변경사항만 추출, 검토 후 승인
- ✓ **버전별 이력 관리** - features/{version}/{date}_{branch}/ 구조
- ✓ **자동 백업** - 변경 전 자동 백업, 롤백 가능
- ✓ **Constitution 기반 검증** - 프로젝트 원칙 자동 체크

## 🎯 핵심 기능

| 기능 | 설명 | 장점 |
|------|------|------|
| **Single Source of Truth** | 프로젝트당 하나의 `.specify/specs/spec.md` | AI가 일관된 context 사용 가능 |
| **Delta Management** | 변경점만 추출하여 관리 | 무엇이 바뀌는지 명확히 파악 |
| **Review → Approve** | 변경사항 검토 후 승인/거부 | 실수 방지, 품질 보장 |
| **Version History** | 개발 이력을 버전별로 보관 | 과거 결정 추적 가능 |
| **Auto Backup** | 변경 전 자동 백업 생성 | 언제든 이전 상태로 복구 |

## 🏗️ 어떻게 동작하나요?

### 신규 프로젝트 생성

```mermaid
graph LR
    A[요구사항 입력] --> B[/speckit.specify]
    B --> C[.specify/specs/spec.md 생성]
    C --> D[/speckit.plan]
    D --> E[.specify/features/v1.0.0/.../plan.md]
    E --> F[/speckit.tasks]
    F --> G[.specify/features/v1.0.0/.../tasks.md]
    G --> H[/speckit.implement]
```

### 기존 프로젝트 개선

```mermaid
graph LR
    A[변경 요청] --> B[/speckit.specify]
    B --> C[.specify/.deltas/.../delta-spec.md]
    C --> D[/speckit.review-delta]
    D --> E{검토}
    E -->|승인| F[/speckit.approve-delta]
    E -->|거부| G[/speckit.reject-delta]
    F --> H[.specify/specs/spec.md 업데이트]
    H --> I[/speckit.plan]
```

## 📦 설치 및 설정

### 1. 프로젝트에 Custom Speckit 추가

```bash
# 프로젝트 디렉토리로 이동
cd your-project

# Custom Speckit 복사 (또는 git submodule 추가)
# .specify/, .cursor/ 디렉토리를 프로젝트 루트에 복사

# 실행 권한 부여
chmod +x .specify/scripts/bash/*.sh
```

### 2. 초기 설정

```bash
# 1. Constitution 작성 (프로젝트 원칙 정의)
# .specify/memory/constitution.md 편집

# 2. Git 설정 (선택)
git add .specify/ .cursor/
git commit -m "feat: add Custom Speckit"

# 3. 버전 설정 (선택, 없으면 v1.0.0 사용)
# package.json 또는 pyproject.toml에 version 추가
# 또는 git tag v1.0.0
```

### 3. Cursor AI에서 사용

Custom Speckit은 Cursor AI 에디터에서 사용하도록 설계되었습니다:

1. Cursor AI 에디터 실행
2. 프로젝트 열기
3. Command Palette (Cmd/Ctrl + Shift + P)에서 `/speckit.` 명령어 사용

## 📁 디렉토리 구조

```
your-project/
│
├── .specify/                           ← ⚙️ Speckit (모든 명세 관련 파일)
│   │
│   ├── specs/                          ← 📌 최종 명세서 (단일 진실의 원천)
│   │   ├── spec.md                     ✓ 프로젝트의 유일한 명세서
│   │   ├── CHANGELOG.md                ✓ 변경 이력
│   │   └── .backups/                   ✓ 자동 백업
│   │       └── spec_backup_20250120_*.md
│   │
│   ├── .specify/.deltas/                        ← 🔄 임시 변경점 (.gitignore에 추가)
│   │   └── {branch}/
│   │       ├── delta-spec.md           ⏳ 승인 대기 중인 변경사항
│   │       ├── changes-summary.md      📋 변경 요약
│   │       └── review-checklist.md     ✅ 검토 체크리스트
│   │
│   ├── features/                       ← 📚 개발 이력 (커밋 대상)
│   │   ├── v1.0.0/
│   │   │   └── 2025-01-20_001-auth/
│   │   │       ├── plan.md             📝 구현 계획
│   │   │       ├── tasks.md            ✓ 작업 목록
│   │   │       ├── research.md         🔍 기술 조사
│   │   │       ├── data-model.md       💾 데이터 모델
│   │   │       ├── quickstart.md       🚀 빠른 시작
│   │   │       └── contracts/          📋 API 계약
│   │   ├── v1.1.0/
│   │   │   └── 2025-02-15_002-payment/
│   │   └── v2.0.0/
│   │       └── 2025-03-01_003-redesign/
│   │
│   ├── memory/
│   │   └── constitution.md             📜 프로젝트 헌장
│   │
│   ├── scripts/bash/                   🔧 헬퍼 스크립트
│   │   ├── compare-specs.sh
│   │   ├── get-version.sh
│   │   └── merge-delta-spec.sh
│   │
│   └── templates/                      📄 문서 템플릿
│       ├── spec-template.md
│       ├── delta-spec-template.md
│       └── plan-template.md
│
└── .cursor/                            ← 🤖 AI 에이전트 설정
    ├── commands/                       ⚡ Speckit 명령어
    │   ├── speckit.specify.md
    │   ├── speckit.review-delta.md
    │   ├── speckit.approve-delta.md
    │   └── ...
    └── rules/                          📏 워크플로우 규칙
        └── custom-speckit-workflow.mdc
```

### 디렉토리 역할 요약

| 디렉토리 | 용도 | Git 커밋 | 설명 |
|----------|------|----------|------|
| `.specify/specs/` | 최종 명세서 | ✅ Yes | 프로젝트의 유일한 spec.md, AI context |
| `.specify/.specify/.deltas/` | 임시 변경점 | ❌ No | 승인 전 임시 파일, .gitignore 추가 |
| `.specify/features/` | 개발 이력 | ✅ Yes | 버전별 plan/tasks 보관 |
| `.specify/memory/` | 프로젝트 원칙 | ✅ Yes | Constitution 문서 |
| `.specify/scripts/` | 헬퍼 스크립트 | ✅ Yes | Bash 스크립트들 |
| `.specify/templates/` | 문서 템플릿 | ✅ Yes | Spec, plan, tasks 템플릿 |
| `.cursor/` | AI 설정 | ✅ Yes | 명령어, 규칙 |

## 🚀 빠른 시작 가이드

### 시나리오 1: 새 프로젝트 시작하기

프로젝트를 처음 시작할 때 사용합니다.

#### 1️⃣ 명세서 작성

Cursor AI에서 Command Palette를 열고 (`Cmd+Shift+P`):

```
/speckit.specify "할 일 관리 앱을 만들고 싶어. 사용자는 태스크를 추가, 수정, 삭제할 수 있고, 마감일과 우선순위를 설정할 수 있어야 해"
```

**결과:**
- ✅ `.specify/specs/spec.md` 생성
- AI가 자동으로 요구사항 분석, 사용자 스토리 작성, 수락 기준 정의

**확인:**
```bash
cat .specify/specs/spec.md  # 생성된 명세서 확인
```

#### 2️⃣ 구현 계획 생성

```
/speckit.plan
```

**결과:**
- ✅ `.specify/features/v1.0.0/2025-01-20_001-task-app/plan.md` 생성
- 기술 스택, 아키텍처, 데이터 모델, API 계약 등 설계

#### 3️⃣ 작업 분해

```
/speckit.tasks
```

**결과:**
- ✅ `.specify/features/v1.0.0/2025-01-20_001-task-app/tasks.md` 생성
- 사용자 스토리별로 세부 작업 분해, 의존성 관리

#### 4️⃣ 구현 시작

```
/speckit.implement
```

**결과:**
- tasks.md의 작업을 순차적으로 실행
- 코드 자동 생성, 테스트 작성, 문서화

---

### 시나리오 2: 기존 프로젝트에 기능 추가하기

이미 `.specify/specs/spec.md`가 있는 프로젝트에 새 기능을 추가할 때 사용합니다.

#### 1️⃣ 변경사항 제안 (Delta 생성)

```
/speckit.specify "사용자 인증 기능을 추가하고 싶어. 이메일/비밀번호 로그인, 회원가입, 비밀번호 재설정이 필요해"
```

**결과:**
- ✅ `.specify/.deltas/002-auth/delta-spec.md` 생성
- 기존 spec과 비교하여 **추가/수정/삭제**할 내용만 추출
- ✅ `.specify/.deltas/002-auth/changes-summary.md` - 변경 요약
- ✅ `.specify/.deltas/002-auth/review-checklist.md` - 검토 체크리스트

**확인:**
```bash
cat .specify/.deltas/002-auth/delta-spec.md  # 변경사항 확인
```

#### 2️⃣ 변경사항 검토 (선택사항, 권장)

```
/speckit.review-delta
```

**결과:**
- 변경사항 분석 리포트 생성
- Constitution 준수 여부 확인
- 영향 받는 컴포넌트 분석
- 리스크 평가

**리포트 예시:**
```markdown
## Critical Issues: 0
## High Priority Issues: 1
- H1: FR-005와 충돌 가능성 (수동 확인 필요)
## Medium Priority Issues: 2
...
```

#### 3️⃣ 수동 검토 및 수정 (필요시)

Delta가 마음에 들지 않으면 직접 수정 가능:

```bash
# Cursor에서 파일 열기
open .specify/.deltas/002-auth/delta-spec.md

# 또는 vim/nano 등으로 편집
vim .specify/.deltas/002-auth/delta-spec.md
```

#### 4️⃣ 변경사항 승인

검토가 끝나면 승인:

```
/speckit.approve-delta
```

**확인 프롬프트:**
```
⚠️ 2개 추가, 1개 수정, 0개 삭제를 .specify/specs/spec.md에 반영합니다. 계속하시겠습니까? (yes/no)
```

**응답: `yes`**

**결과:**
- ✅ `.specify/specs/spec.md` 업데이트 (delta 내용 병합)
- ✅ `.specify/specs/.backups/spec_backup_20250120_143022_002-auth.md` 백업 생성
- ✅ `.specify/specs/CHANGELOG.md` 변경 이력 기록
- ✅ `.specify/.deltas/002-auth/` 아카이브 또는 삭제

#### 5️⃣ 구현 계획 및 작업 분해

승인 후 계획 생성:

```
/speckit.plan
```

**결과:**
- ✅ `.specify/features/v1.1.0/2025-01-22_002-auth/plan.md`

```
/speckit.tasks
```

**결과:**
- ✅ `.specify/features/v1.1.0/2025-01-22_002-auth/tasks.md`

#### 6️⃣ 구현

```
/speckit.implement
```

---

### 시나리오 3: 변경사항 거부하기

Delta를 검토한 후 적용하고 싶지 않을 때:

```
/speckit.reject-delta
```

**확인 프롬프트:**
```
⚠️ .specify/.deltas/002-auth/를 삭제합니다. 계속하시겠습니까? (yes/no)
Archive하시겠습니까? (yes/no)
```

**결과:**
- ✅ `.specify/.deltas/002-auth/` 삭제 (또는 아카이브)
- ✅ `.specify/specs/spec.md` 그대로 유지 (변경 없음)
- ✅ 거부 이력 기록

---

### 시나리오 4: 롤백하기

승인 후 문제가 발생하면 롤백 가능:

```bash
# 1. 백업 파일 확인
ls .specify/specs/.backups/

# 2. 가장 최근 백업으로 복구
cp .specify/specs/.backups/spec_backup_20250120_143022_002-auth.md .specify/specs/spec.md

# 3. Delta 복원 (아카이브된 경우)
mv specs/.deltas-archive/20250120_143022_002-auth .specify/.deltas/002-auth

# 4. CHANGELOG 수동 되돌리기
vim .specify/specs/CHANGELOG.md
```

## 📝 명령어 레퍼런스

### 필수 명령어

| 명령어 | 단계 | 설명 | 입력 | 출력 |
|--------|------|------|------|------|
| `/speckit.specify` | 1️⃣ | 명세서 생성/수정 | 자연어 요구사항 | `.specify/specs/spec.md` 또는 `.specify/.deltas/{branch}/` |
| `/speckit.plan` | 2️⃣ | 구현 계획 생성 | (자동) | `features/{version}/{date}_{branch}/plan.md` |
| `/speckit.tasks` | 3️⃣ | 작업 목록 생성 | (자동) | `features/{version}/{date}_{branch}/tasks.md` |
| `/speckit.implement` | 4️⃣ | 구현 실행 | (자동) | 소스 코드, 테스트 |

### Delta 관리 명령어

| 명령어 | 목적 | 사용 시점 | 필수 여부 |
|--------|------|-----------|-----------|
| `/speckit.review-delta` | Delta 분석 | Delta 생성 후 | 선택 (권장) |
| `/speckit.approve-delta` | Delta 승인 | 검토 완료 후 | **필수** |
| `/speckit.reject-delta` | Delta 거부 | 변경 불필요 시 | 선택 |

### 품질 관리 명령어

| 명령어 | 목적 | 출력 |
|--------|------|------|
| `/speckit.checklist` | 품질 체크리스트 생성 | 요구사항 검증 체크리스트 |
| `/speckit.analyze` | 일관성 분석 | spec/plan/tasks 교차 검증 리포트 |
| `/speckit.constitution` | Constitution 정의 | 프로젝트 원칙 문서 |

### 명령어 실행 순서

**신규 프로젝트:**
```
specify → plan → tasks → implement
```

**기존 프로젝트:**
```
specify → review-delta → approve-delta → plan → tasks → implement
```

## Key Differences from Original Spec-Kit

| Aspect | Original Spec-Kit | Custom Speckit |
|--------|-------------------|----------------|
| **Spec Location** | `specs/{branch}/spec.md` | `.specify/specs/spec.md` (single file) |
| **Change Management** | Create new spec per feature | Delta → Review → Approve |
| **Plan/Tasks Location** | `specs/{branch}/` | `features/{version}/{date}_{branch}/` |
| **Version Tracking** | Branch number only | Version + Date + Branch |
| **Change Review** | None | Built-in review workflow |
| **Spec Duplication** | High (per feature) | None (single source) |

## Workflow Rules

See [`.cursor/rules/custom-speckit-workflow.mdc`](.cursor/rules/custom-speckit-workflow.mdc) for detailed workflow rules enforced by the AI agent.

### Critical Rules

1. ✅ **Only one spec file**: `.specify/specs/spec.md` is the single source of truth
2. ✅ **Delta approval required**: Changes must be approved via `/speckit.approve-delta`
3. ✅ **Features directory**: Save plan.md and tasks.md to `features/{version}/{date}_{branch}/`
4. ✅ **Constitution compliance**: All changes must comply with `.specify/memory/constitution.md`
5. ❌ **Never create**: `specs/{branch}/spec.md` (old pattern)
6. ❌ **Never modify directly**: `.specify/specs/spec.md` (use delta workflow)

## Version Management

Version is detected from:
1. Git tags (e.g., `v1.0.0`)
2. `pyproject.toml` (Python projects)
3. `package.json` (Node.js projects)
4. User input (if none above)
5. Default: `v1.0.0`

## Scripts

Helper scripts in `.specify/scripts/bash/`:

- `compare-specs.sh` - Check if spec exists, determine workflow
- `get-version.sh` - Extract project version
- `merge-delta-spec.sh` - Validate delta merge prerequisites
- `create-new-feature.sh` - Initialize new feature branch
- `check-prerequisites.sh` - Validate command prerequisites

## Constitution

Define your project's core principles in `.specify/memory/constitution.md`. All specifications and changes are automatically validated against these principles.

## Examples

### Example 1: First Feature

```bash
# Start new project
/speckit.specify "Build a blog platform with posts, comments, and user profiles"

# Review generated spec at: .specify/specs/spec.md

# Generate plan
/speckit.plan
# Output: .specify/features/v1.0.0/2025-01-20_001-blog-platform/plan.md

# Generate tasks
/speckit.tasks
# Output: .specify/features/v1.0.0/2025-01-20_001-blog-platform/tasks.md
```

### Example 2: Adding a Feature

```bash
# Propose changes
/speckit.specify "Add comment moderation and spam detection"

# Review delta
/speckit.review-delta
# Analyzes: .specify/.deltas/002-comment-moderation/delta-spec.md

# Edit manually if needed
# vim .specify/.deltas/002-comment-moderation/delta-spec.md

# Approve
/speckit.approve-delta
# Merges to: .specify/specs/spec.md

# Continue with plan and tasks
/speckit.plan
/speckit.tasks
```

## 🎓 Best Practices

### 1. Constitution 작성하기

프로젝트 시작 시 `.specify/memory/constitution.md`를 작성하세요:

```markdown
# My Project Constitution

## Core Principles

### I. API-First Development
- 모든 기능은 API로 먼저 설계
- OpenAPI 3.0 spec 필수
- REST 원칙 준수

### II. Test Coverage (NON-NEGOTIABLE)
- 최소 80% 커버리지 유지
- 모든 API 엔드포인트는 테스트 필수
- TDD 접근 권장

### III. Code Review
- 2명 이상 승인 필요
- Constitution 준수 여부 확인
...
```

### 2. 의미 있는 Commit 메시지

```bash
# Delta 승인 후
git add .specify/specs/spec.md features/
git commit -m "feat(auth): add user authentication spec

- Add login, signup, password reset user stories
- Define JWT-based authentication flow
- Add security requirements for password storage
"
```

### 3. 버전 관리 전략

**Semantic Versioning 사용:**
- `v1.0.0` - 초기 릴리스
- `v1.1.0` - 기능 추가 (backwards compatible)
- `v2.0.0` - Breaking changes

```bash
# 주요 버전 릴리스 시
git tag v1.0.0
git push --tags
```

### 4. Delta 검토 체크리스트

Delta 승인 전 확인사항:
- [ ] 변경사항이 Constitution을 준수하는가?
- [ ] 기존 기능과 충돌하지 않는가?
- [ ] 모든 변경에 명확한 rationale이 있는가?
- [ ] 영향받는 컴포넌트가 모두 식별되었는가?
- [ ] 마이그레이션 계획이 필요한가?

### 5. 팀 협업

**Delta 검토 프로세스:**
1. 개발자가 `/speckit.specify`로 Delta 생성
2. PR 생성, Delta 파일 포함
3. 리뷰어가 `/speckit.review-delta` 실행
4. 리뷰 승인 후 개발자가 `/speckit.approve-delta`
5. 병합 후 구현 시작

### 6. 문서화

각 feature 디렉토리에 추가 문서 작성:
```
.specify/features/v1.1.0/2025-01-22_002-auth/
├── plan.md
├── tasks.md
├── implementation-notes.md    ← 구현 중 발견한 사항
├── decisions.md                ← 주요 기술 결정 기록
└── retrospective.md            ← 회고
```

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: .specify/specs/spec.md를 직접 수정하면 안 되나요?

**A:** 안 됩니다. 반드시 Delta 워크플로우를 거쳐야 합니다.

**이유:**
- 변경 이력 추적 불가
- 백업 미생성
- Constitution 검증 건너뜀
- 팀원과의 동기화 문제

**예외:** 첫 프로젝트 생성 시에만 `/speckit.specify`가 직접 생성

---

### Q2: .specify/.deltas/를 Git에 커밋해야 하나요?

**A:** 아니요, `.gitignore`에 추가하세요.

**이유:**
- Delta는 임시 파일 (승인/거부 후 정리됨)
- 각 개발자의 로컬 작업 공간
- 충돌 가능성 높음

**예외:** 팀 리뷰가 필요하면 PR에 포함 가능 (일시적)

---

### Q3: 여러 기능을 동시에 개발하려면?

**A:** 각 기능마다 별도 브랜치 사용:

```bash
# Feature 1
git checkout -b 001-feature-a
/speckit.specify "..."
/speckit.approve-delta
/speckit.plan

# Feature 2
git checkout main
git checkout -b 002-feature-b
/speckit.specify "..."
...
```

**주의:** Delta는 브랜치별로 관리되므로 충돌 없음

---

### Q4: Plan이나 Tasks를 수정하고 싶어요

**A:** 직접 편집 가능합니다:

```bash
# Plan 수정
vim .specify/features/v1.0.0/2025-01-20_001-feature/plan.md

# 수정 후 재생성 (선택)
/speckit.tasks  # plan.md 기반으로 tasks.md 재생성
```

**Spec 수정:** Spec은 반드시 Delta 워크플로우 사용

---

### Q5: 버전을 수동으로 지정하려면?

**A:** 다음 중 하나:

```bash
# 방법 1: Git tag
git tag v2.0.0

# 방법 2: package.json
{
  "version": "2.0.0"
}

# 방법 3: pyproject.toml
[project]
version = "2.0.0"

# 방법 4: 스크립트 실행 시 지정
.specify/scripts/bash/get-version.sh --version v2.0.0
```

---

### Q6: Delta 승인 후 되돌리려면?

**A:** 백업에서 복구:

```bash
# 1. 백업 확인
ls .specify/specs/.backups/

# 2. 복구
cp .specify/specs/.backups/spec_backup_20250120_*.md .specify/specs/spec.md

# 3. Git으로도 가능
git checkout HEAD~1 .specify/specs/spec.md
```

---

### Q7: Constitution을 수정하려면?

**A:** 직접 편집 후 커밋:

```bash
vim .specify/memory/constitution.md
git add .specify/memory/constitution.md
git commit -m "docs: update constitution - add new principle"
```

**주의:** Constitution 변경은 팀 전체 합의 필요

---

### Q8: 기존 Spec-Kit 프로젝트를 마이그레이션하려면?

**A:** 다음 절차:

1. 최신 feature의 spec을 `.specify/specs/spec.md`로 복사
2. 기존 `specs/` 디렉토리를 `.specify/features/v1.0.0/`로 이동
3. 날짜 정보를 Git commit date에서 추출
4. Custom Speckit 설정 추가

```bash
# 1. 최신 spec 복사
cp specs/003-latest-feature/spec.md .specify/specs/spec.md

# 2. 기존 디렉토리 이동
mkdir -p .specify/features/v1.0.0
mv specs/001-* specs/002-* specs/003-* .specify/features/v1.0.0/

# 3. 날짜 추가 (수동 또는 스크립트)
cd .specify/features/v1.0.0
for dir in */; do
  date=$(git log --format=%cd --date=short -- "$dir" | head -1)
  mv "$dir" "${date}_${dir}"
done
```

---

## 🔧 문제 해결 (Troubleshooting)

### 오류: "No delta found for branch"

**원인:** `.specify/.deltas/{branch}/` 디렉토리가 없음

**해결:**
```bash
# 1. 현재 브랜치 확인
git branch --show-current

# 2. Delta 생성
/speckit.specify "요구사항 입력"

# 3. .specify/specs/spec.md가 없는 경우
# → 신규 프로젝트 워크플로우 (Delta 생성 안 됨)
# → 정상 동작
```

---

### 오류: "Delta not approved"

**원인:** `/speckit.plan` 실행 전 Delta 승인 안 함

**해결:**
```bash
# Delta 확인
cat .specify/.deltas/{branch}/delta-spec.md

# 승인 또는 거부
/speckit.approve-delta  # 승인
# 또는
/speckit.reject-delta   # 거부
```

---

### 오류: "plan.md not found"

**원인:** `/speckit.tasks` 실행 전 plan.md 미생성

**해결:**
```bash
# 1. Plan 생성
/speckit.plan

# 2. 올바른 경로 확인
ls .specify/features/*/2025-*-*/plan.md

# 3. 버전 확인
.specify/scripts/bash/get-version.sh
```

---

### 오류: "Constitution violation detected"

**원인:** Delta가 `.specify/memory/constitution.md` 원칙 위반

**해결:**
```bash
# 1. 리뷰 리포트 확인
/speckit.review-delta

# 2. Delta 수정
vim .specify/.deltas/{branch}/delta-spec.md

# 3. Constitution 수정 (팀 합의 필요)
vim .specify/memory/constitution.md

# 4. 재검토
/speckit.review-delta
```

---

### 오류: Wrong file locations

**원인:** AI가 잘못된 경로에 파일 저장

**해결:**
```bash
# 1. 워크플로우 규칙 확인
cat .cursor/rules/custom-speckit-workflow.mdc

# 2. Cursor 재시작 (규칙 reload)

# 3. 스크립트 권한 확인
chmod +x .specify/scripts/bash/*.sh

# 4. 스크립트 테스트
.specify/scripts/bash/compare-specs.sh --json
.specify/scripts/bash/get-version.sh --json
```

---

### 오류: Version detection failed

**원인:** 버전 정보를 찾을 수 없음

**해결:**
```bash
# 방법 1: Git tag 추가
git tag v1.0.0

# 방법 2: package.json 생성
echo '{"version": "1.0.0"}' > package.json

# 방법 3: pyproject.toml 추가
cat >> pyproject.toml << EOF
[project]
version = "1.0.0"
EOF

# 방법 4: 기본값 사용
# → v1.0.0으로 자동 설정됨
```

---

## 🔗 참고 자료

### 공식 문서
- [Cursor AI 문서](https://docs.cursor.com/)
- [GitHub Spec-Kit](https://github.com/github/spec-kit)
- [Semantic Versioning](https://semver.org/)

### 워크플로우 규칙
- [`.cursor/rules/custom-speckit-workflow.mdc`](.cursor/rules/custom-speckit-workflow.mdc) - AI 에이전트 규칙 (필독)

### 스크립트 문서
- `compare-specs.sh --help` - Spec 비교 스크립트
- `get-version.sh --help` - 버전 추출 스크립트
- `merge-delta-spec.sh --help` - Delta 병합 스크립트

---

## 🚦 시작하기 전 체크리스트

프로젝트에 Custom Speckit을 적용하기 전에:

- [ ] Cursor AI 에디터 설치 및 실행
- [ ] `.specify/` 및 `.cursor/` 디렉토리 복사
- [ ] 스크립트 실행 권한 부여 (`chmod +x`)
- [ ] `.specify/memory/constitution.md` 작성 (프로젝트 원칙)
- [ ] `.gitignore`에 `.specify/.deltas/` 추가
- [ ] 버전 정보 설정 (Git tag 또는 package.json/pyproject.toml)
- [ ] 팀원과 워크플로우 공유

---

## 🤝 기여하기 (Contributing)

Custom Speckit 개선에 기여하고 싶으신가요?

### 기여 방법

1. **이슈 생성**
   - 버그 리포트, 기능 제안, 문서 개선 등
   - 명확한 제목과 설명 작성

2. **Pull Request**
   - Fork 후 feature 브랜치 생성
   - 변경사항 커밋
   - PR 생성 및 설명 작성

### 기여 가이드라인

- ✅ 워크플로우 규칙 준수
- ✅ 신규/기존 프로젝트 워크플로우 모두 테스트
- ✅ 새 명령어 추가 시 문서 업데이트
- ✅ Constitution 기반 검증 유지
- ✅ 기존 스크립트 스타일 유지

### 테스트

```bash
# 신규 프로젝트 워크플로우
/speckit.specify "test project"
/speckit.plan
/speckit.tasks

# 기존 프로젝트 워크플로우
/speckit.specify "test change"
/speckit.review-delta
/speckit.approve-delta
/speckit.plan
```

---

## 📄 라이선스

MIT License - [GitHub Spec-Kit](https://github.com/github/spec-kit)에서 상속

```
MIT License

Copyright (c) 2025 Custom Speckit Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 크레딧

### 기반 프로젝트
- [GitHub Spec-Kit](https://github.com/github/spec-kit) by GitHub
- Spec-Driven Development 방법론

### 커스텀 개선
- **버전 관리 시스템** - features/{version}/{date}_{branch}/ 구조
- **Delta 워크플로우** - 변경사항 추적 및 검토
- **Constitution 기반 검증** - 프로젝트 원칙 자동 체크
- **자동 백업** - 변경 전 안전 백업

---

## 📞 문의 및 지원

- **이슈**: GitHub Issues에 등록
- **토론**: GitHub Discussions
- **문서**: 이 README 및 [워크플로우 규칙](.cursor/rules/custom-speckit-workflow.mdc)

---

## 📊 프로젝트 상태

| 항목 | 상태 |
|------|------|
| 버전 | v1.0.0 |
| 유지보수 | ✅ Active |
| 문서화 | ✅ Complete |
| 테스트 | ✅ Verified |
| 라이선스 | MIT |

---

**마지막 업데이트**: 2025-01-20  
**다음 버전**: v1.1.0 (계획 중 - UI 개선, 추가 명령어)

---

<div align="center">

**Custom Speckit으로 더 나은 Spec-Driven Development를!** 🚀

Made with ❤️ for AI-powered development

[⬆ 맨 위로](#custom-speckit-)

</div>

