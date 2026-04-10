# Markdown Style System

이 저장소는 GitHub에서 읽기 쉬운 Markdown을 기준으로 관리한다.

## 기본 원칙

- 본문은 짧은 문단과 분명한 제목 구조를 우선한다.
- 제목 체계는 `#`, `##`, `###` 세 수준을 기본으로 사용한다.
- 코드 블록은 fenced code block과 언어 태그를 사용한다.
- 표는 pipe table로 유지하되, 설명형 문장은 표보다 본문을 우선한다.
- 링크와 경로는 상대 경로 기준으로 통일한다.

## 파일 배치 규칙

- 본문과 부록 Markdown은 `chapters/`에 둔다.
- 본문과 부록에서 참조하는 그림은 모두 `chapters/images/`에 둔다.
- 실행 가능한 예제, bootstrap, snippets는 `codes/`에 둔다.
- 책의 범위와 구조 문서는 `00_meta/`, `01_outline/`에 둔다.

## 제목 체계

- 저장소 README: `#`
- 챕터/부록 파일 제목: `# CHAPTER N` 또는 `# APPENDIX X`
- 장 안의 큰 절: `##`
- 절 안의 하위 항목: `###`

## 코드 블록 규칙

- SQL: `sql`
- Bash/Shell: `bash`
- YAML: `yaml`
- JSON: `json`
- Python: `python`
- Text tree: `text`

## 링크 규칙

- 루트 README는 `chapters/`, `01_outline/`, `codes/`를 먼저 가리킨다.
- 챕터 파일에서 그림은 `./images/<filename>` 경로를 사용한다.
- 챕터 파일에서 코드 예시는 `../codes/...` 상대 경로를 사용한다.
- 챕터와 부록 사이 이동은 상대 경로 링크를 사용한다.

## 편집 규칙

- 굵게 강조 표시는 사용하지 않는다.
- 같은 정보를 여러 파일에 중복으로 붙이지 않는다.
- 잘게 쪼갠 요약 표보다 casebook, playbook, appendix 구조를 우선한다.
