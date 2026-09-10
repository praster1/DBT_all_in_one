# GitHub Markdown 반영 검증

[책 첫 화면](../README.md) · [전체 목차](../01_outline/master_toc.md)

## 기준과 보존

반영 기준 저장소는 `praster1/DBT_all_in_one`, 기준 `main` 커밋은 `15ce73ed7fc7099176f6f9ad56617d269c2e9299`, Git tree는 `90a1e124c56ff0125f02fc677f5961fda7470a4d`다. 첨부 원본 ZIP을 전개해 계산한 Git tree가 기준 저장소와 일치함을 확인했다.

기존 `chapters/` 본문·부록 25편의 경로와 바이트는 그대로 유지한다. v3에서 수정한 참고편은 `chapters/reference-v3/`에 별도로 두었다. 원본 확인값은 [원본 보존 목록](original-preservation.json), v3에서 옮긴 경로는 [원고 경로 매핑](source-path-map.json)에 기록했다. 기존 `codes/`와 원래 그림도 유지한다.

## 반영 범위

Markdown 기준 README·전체 목차, 마당마켓 연속 실습 17장, 설계 패턴 26장, 개정 참고편 25편, 설계·운영 문서, 출처, 실습 프로젝트와 데이터, 시각 자료와 생성 소스를 반영한다. 통합 원고는 `scripts/build_markdown.py`가 `book.json`의 문서 순서에 따라 생성한다. HTML은 필요할 때 생성하는 파생 파일이며 GitHub 독서의 기준으로 사용하지 않는다.

## 실행한 검사의 근거

| 검사 | 기계 판독 결과 |
| --- | --- |
| Markdown의 로컬 파일·그림·장별 링크·앵커, 원본 25편 해시 | [markdown-validation.json](markdown-validation.json) |
| SQLite 기준 SQL와 데이터의 5단계 변화 | [sql-reference-validation.json](sql-reference-validation.json) |
| 서로 다른 모델링 방식의 결과 대사 | [model-comparisons.json](model-comparisons.json) |
| 11개 코드 체크포인트 | [checkpoint-results.json](checkpoint-results.json) |
| Python·YAML·SVG·PNG 등 정적 검사 | [static-validation.json](static-validation.json) |

검사 결과 파일에 기록된 실제 건수와 오류 목록을 기준으로 판단한다. 외부 웹 주소의 생존 여부, GitHub 서비스의 모든 렌더링 제한, dbt 엔진·어댑터·클라우드·분산 트랜잭션의 통합 동작은 위 로컬 검사에 포함하지 않는다.

## 그림과 화면의 출처

개념도는 책의 저작 소스이며, 화면 12개는 실제 SQLite 기준 실행 산출물을 표시한 로컬 결과 뷰어의 Chromium 캡처다. 상용 dbt 제품 화면이나 dbt 성공 로그가 아니다. 화면 재생성 환경에 따라 글꼴의 배치나 PNG 바이트는 달라질 수 있지만, 표시한 업무 숫자는 같은 기준 SQL의 결과다.

## 버전·엔진 범위

v3 제작 시점의 별도 보고서는 [delivery-validation.md](delivery-validation.md)에 남겨 두었다. SQLite 검사 통과와 dbt 엔진 실행 성공은 구별한다. 이 반영 작업은 원고·실습 파일의 게시와 그 로컬 재현성 확인이며, 실제 운영 데이터베이스에 접속하거나 테이블을 변경하지 않는다.
