# Markdown Repair Notes

이 패키지는 GitHub에 올린 원고를 **읽기 좋은 Markdown 구조로 다시 정리한 대체본**입니다.

주요 수정 사항:

- 챕터 파일의 한 줄짜리 덤프/축약을 정상적인 Markdown 단락, 표, 리스트, 코드 블록으로 복원
- `book_from_pdf.md`를 통합 읽기용 Markdown으로 재구성
- `chapters/ch18_platform-playbook-trino와-nosql-sql-layer.md`를 Trino / NoSQL + SQL Layer 두 파일로 분리
- 루트 README, 목차, 스타일 문서를 GitHub 탐색 기준으로 재작성
- Companion Pack은 별도 `codes/` 경로로 유지

교체 권장 대상:

- `README.md`
- `book_from_pdf.md`
- `chapters/` 전체
- `00_meta/book_charter.md`
- `01_outline/master_toc.md`
- `07_styles/style_system.md`
- `codes/README.md` 및 필요 시 `codes/` 전체
