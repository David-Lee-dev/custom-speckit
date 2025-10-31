# Custom Speckit 🚀

> AI 기반 Spec-Driven Development 도구 - 명세서 먼저, 코드는 나중에

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 문서 선택

### 🚀 [빠른 시작 가이드](docs/README-simple.md)
**5분 안에 시작하기**
- 바로 사용하고 싶다면
- 설치부터 첫 기능까지
- 핵심 명령어만 간단히

### 📚 [상세 가이드](docs/README-detailed.md)
**완전 정복하기**
- Spec-Driven Development 개념
- 왜 기획서를 먼저 작성해야 하는가
- 모든 명령어와 시나리오
- 고급 기능과 트러블슈팅

---

## 💡 Spec-Driven Development란?

> **"명세서를 먼저 작성하고, AI가 그에 맞춰 코드를 생성하는 개발 방식"**

### 전통적 개발 방식의 문제

```
아이디어 → 바로 코딩 → 문제 발견 → 수정 → 또 수정 → ...
```

❌ 방향성 없이 코드 작성  
❌ 요구사항 누락을 늦게 발견  
❌ AI가 잘못된 방향으로 코드 생성  
❌ 계속된 리팩토링과 시간 낭비

---

### Spec-Driven Development

```
기획서 작성 → 설계 검증 → AI가 정확한 코드 생성 → 테스트
```

✅ **명확한 목표**: 무엇을 만들지 먼저 정의  
✅ **AI 최적화**: AI가 정확한 방향으로 코드 생성  
✅ **조기 발견**: 요구사항 문제를 코딩 전 발견  
✅ **시간 절약**: 코딩 후 수정은 10배 더 오래 걸림

**참고**: [GitHub Spec-Kit](https://github.com/github/spec-kit) - GitHub에서 공식 권장하는 AI 시대의 개발 방식

---

## ⚡ 30초 요약

```bash
# 1. 설치
uvx custom-speckit init

# 2. Constitution 작성 (프로젝트 원칙 정의)
vim .specify/memory/constitution.md

# 3. 개발 시작
/speckit.specify "할 일 관리 앱 만들기"  # 기획서 작성
/speckit.plan                           # 설계
/speckit.tasks                          # 작업 분해
/speckit.implement                      # AI가 구현
```

**결과**: 명세서 기반으로 정확하게 구현된 앱 🎉

---

## 🎯 핵심 특징

### 1. 📋 기획서 우선 개발

**코딩 전 기획서 작성이 왜 중요한가요?**

| 기획서 없이 | 기획서 먼저 | 차이 |
|-----------|-----------|------|
| 3일 코딩 → 요구사항 누락 발견 → 다시 설계 | 1시간 기획 → 요구사항 확정 → 한 번에 정확히 구현 | **시간 10배 절약** |
| AI가 틀린 방향으로 코드 생성 → 계속 수정 | 명세서 기반으로 AI가 정확한 코드 생성 | **리팩토링 최소화** |
| 팀원마다 다른 이해 → 충돌 | 명세서로 통일된 이해 → 원활한 협업 | **커뮤니케이션 비용 감소** |

**결론**: 기획 1시간이 코딩 10시간을 절약합니다.

---

### 2. 🔄 Delta 기반 변경 관리

**기존 Spec-Kit**:
```
specs/001-todo/spec.md
specs/002-comment/spec.md
specs/003-search/spec.md
→ 명세가 분산됨, 전체 파악 어려움
```

**Custom Speckit**:
```
specs/spec.md  ← 단일 진실의 원천
.deltas/new-feature/  ← 변경사항 (임시)
→ 검토 후 안전하게 병합
```

**장점**:
- ✅ 전체 명세를 한 곳에서 파악
- ✅ 변경사항을 Delta로 검토
- ✅ 승인 후 안전하게 병합
- ✅ 변경 이력 자동 추적

---

### 3. 🌐 자동 언어 감지

```bash
# 한글 입력 → 모든 문서 한글
/speckit.specify "사용자 인증"

# 영어 입력 → 모든 문서 영어
/speckit.specify "User authentication"
```

**기본값**: 한국어

---

### 4. 🎯 명확한 디렉토리 구조

```
specs/        프로젝트 뼈대 (계속 업데이트)
features/     Feature 구현 기록 (수정 안 함)
```

**specs/ 예시**:
```markdown
# tech-stack.md

## Database
- PostgreSQL 15.x - 메인 DB
  * Initial: 2025-10-28 (todo-app)
- MongoDB 7.x - 검색 엔진
  * Added: 2025-11-20 (search-feature)
  * Reason: 전문 검색 최적화
```

**features/ 예시**:
```
v1.0.0/2025_10_28-todo-app/     # 첫 개발
v1.1.0/2025_11_05-comment/      # 댓글 추가
v1.2.0/2025_11_20-search/       # 검색 추가
```

---

## 🔥 핵심 워크플로우

### 신규 프로젝트

```bash
# 1. 명세서 생성
/speckit.specify "프로젝트 설명"

# 2. 기술 설계
/speckit.plan

# 3. 작업 분해
/speckit.tasks

# 4. 구현
/speckit.implement
```

### 기능 추가

```bash
# 1. 변경사항 제안
/speckit.specify "새 기능"

# 2. 승인
/speckit.approve-delta

# 3-4. 구현
/speckit.plan
/speckit.tasks
/speckit.implement
```

---

## 📦 설치

```bash
# uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 프로젝트에 설치
cd your-project
uvx custom-speckit init

# 업데이트
uvx custom-speckit update
```

**로컬 개발 서버** (선택):
```bash
# Custom Speckit 프로젝트에서
docker-compose up -d

# 다른 프로젝트에서
uvx --index-url http://localhost:8080/simple/ custom-speckit init
```

---

## 🎓 학습 경로

### 1. 처음 사용자
👉 [빠른 시작 가이드](docs/README-simple.md)
- 5분 튜토리얼
- 핵심 4가지 명령어
- 바로 시작하기

### 2. 개념 이해
👉 [상세 가이드](docs/README-detailed.md)
- Spec-Driven Development란?
- 왜 기획서가 먼저인가?
- 워크플로우 상세 설명

### 3. 실전 활용
👉 [상세 가이드 - 개발 시나리오](docs/README-detailed.md#-개발-시나리오)
- 최초 프로젝트 시작
- 기능 추가
- 기술 스택 변경

### 4. 고급 기능
👉 [상세 가이드 - 고급 기능](docs/README-detailed.md#-고급-기능)
- Delta 워크플로우
- Constitution 고급 활용
- 팀 협업 전략

---

## 🌟 왜 Custom Speckit인가?

### GitHub Spec-Kit 기반

[GitHub Spec-Kit](https://github.com/github/spec-kit)을 기반으로 만들어졌습니다.
- ⭐ 43.7k stars
- 🏢 GitHub 공식 도구
- 🤖 AI 시대의 표준 개발 방식

### Custom Speckit의 개선사항

| 기능 | GitHub Spec-Kit | Custom Speckit |
|------|----------------|----------------|
| 명세서 관리 | 분산 (feature별) | ✅ 통합 (spec.md 단일 파일) |
| 변경 관리 | 없음 | ✅ Delta 워크플로우 (검토 후 병합) |
| 기술 스펙 | feature별 분산 | ✅ specs/에서 중앙 관리 |
| 언어 지원 | 영어만 | ✅ 한글/영어 자동 감지 |
| Git 규칙 | 기본 | ✅ 디렉토리-브랜치 매칭 규칙 |
| 문서화 | 영어 | ✅ 한글 우선 |

---

## 💬 커뮤니티

- 💡 [GitHub Issues](https://github.com/David-Lee-dev/custom-speckit/issues) - 질문 및 버그 리포트
- 📖 [GitHub Spec-Kit](https://github.com/github/spec-kit) - 원본 프로젝트
- 📝 [블로그 - Spec-Driven Development](https://devjino.tistory.com/435)

---

## 📄 라이선스

MIT License - Based on [GitHub Spec-Kit](https://github.com/github/spec-kit)

---

<div align="center">

### 🚀 시작하기

**처음 사용하시나요?** → [빠른 시작 가이드](docs/README-simple.md)

**제대로 배우고 싶으신가요?** → [상세 가이드](docs/README-detailed.md)

---

**Custom Speckit으로 더 나은 개발 경험을!** 🎯

Made with ❤️ by Custom Speckit Contributors

</div>
