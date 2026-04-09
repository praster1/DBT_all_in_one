# Markdown Style System

이 저장소는 PDF 원고를 그대로 덤프하지 않고, GitHub에서 읽기 쉬운 Markdown 구조를 기준으로 정리한다.

## 기본 규칙

- 한 문단은 너무 길게 붙이지 않는다.
- 제목은 `# / ## / ###`만 명확하게 사용한다.
- 표는 가능한 한 pipe table로 유지한다.
- 코드 블록은 fenced code block(````lang`)을 사용한다.
- 노트/주의/안티패턴/직접 해보기는 굵은 제목 + 짧은 문단/리스트로 적는다.

## 제목 체계

- 책 앞머리: `#`
- 챕터 파일 제목: `# CHAPTER N · 제목` 또는 `# APPENDIX X · 제목`
- 장 안의 큰 절: `## 1.1. ...`
- 절 안의 하위 항목: `### 1.1.1. ...`

## 코드 블록

- SQL: `sql`
- Shell/Bash: `bash`
- YAML: `yaml`
- JSON: `json`
- Text tree: `text`
- Mermaid: `mermaid`

## 링크 규칙

- 챕터 간 이동은 상대 경로 링크를 사용한다.
- 루트 README는 `chapters/`, `01_outline/`, `codes/`를 우선 가리킨다.
- 이미지 경로는 루트 `assets/`를 기준으로 한다.

## GitHub 친화성

- 너무 큰 단일 Markdown보다 챕터 단위 파일을 우선한다.
- `book_from_pdf.md`는 전체 검색용/연속 읽기용으로 유지하되, 실제 편집과 리뷰는 `chapters/`에서 진행한다.
