from pathlib import Path
import subprocess,json,html
R=Path(__file__).resolve().parents[1];F=R/'assets/figures';F.mkdir(parents=True,exist_ok=True)
diagrams={}
def diagram(slug,title,nodes,edges,rank='LR'):
    # 노드 본문은 짧은 줄로 고정해 SVG와 모바일 확대 모두 읽을 수 있게 한다.
    lines=['digraph G {',f'graph [rankdir={rank}, bgcolor="#ffffff", pad="0.3", nodesep="0.4", ranksep="0.55", fontname="Noto Sans CJK KR"];',
    'node [shape=box, style="rounded,filled", fillcolor="#edf5f7", color="#267882", fontcolor="#14343b", fontname="Noto Sans CJK KR", fontsize=14, margin="0.2,0.15"];',
    'edge [color="#58717a", fontname="Noto Sans CJK KR", fontsize=11, arrowsize=0.75];']
    for i,label in enumerate(nodes):lines.append(f'n{i} [label={json.dumps(label,ensure_ascii=False)}];')
    for edge in edges:
        a,b,*label=edge;attr=f' [label={json.dumps(label[0],ensure_ascii=False)}]' if label else ''
        lines.append(f'n{a} -> n{b}{attr};')
    lines.append('}')
    src='\n'.join(lines);(F/f'{slug}.dot').write_text(src)
    subprocess.run(['dot','-Tsvg',str(F/f'{slug}.dot'),'-o',str(F/f'{slug}.svg')],check=True)
    svg=(F/f'{slug}.svg').read_text();svg=svg.replace('<title>G</title>',f'<title>{html.escape(title)}</title><desc>교재 저자 작성 개념도. {html.escape(title)}의 구성과 흐름.</desc>')
    (F/f'{slug}.svg').write_text(svg)
    diagrams[slug]={'title':title,'nodes':nodes,'kind':'original concept diagram','source':f'assets/figures/{slug}.dot','image':f'assets/figures/{slug}.svg'}
diagram('pattern-map','설계 질문별 패턴 지도',['어떤 문제를 푸는가?','데이터 품질 단계\nMedallion / 계층형','전사 통합\nHub & Spoke / Bus / Vault','시간·처리 흐름\nBatch / Lambda / Kappa','저장·접근\nWarehouse / Lakehouse / Federation','책임과 계약\nMesh / Data Product','모델의 모양\nStar / Snowflake / Wide'],[(0,i) for i in range(1,7)])
diagram('medallion','메달리온의 품질 경계',['원천·파일·CDC','Bronze\n원천 보존 + 적재 메타데이터','Silver\n중복·타입·키·업무 엔터티','Gold\n인정 매출·분석용 데이터','검역 공간\n이유 + 원천 추적'],[(0,1),(1,2),(2,3),(2,4)])
diagram('layer-map','네 계층과 세 품질 구역의 예시 매핑',['l0_cus\n원천 보존\nBronze','l1_cus\n표준화\nSilver 진입','l2_cus\n통합·검증\nSilver 심화','l3_cus\n소비용 마트\nGold','숫자와 색의 대응은\n조직의 설계 결정'],[(0,1),(1,2),(2,3),(4,1,'규칙을 문서화')])
diagram('hub-spoke','중앙 통합과 종속 마트',['POS','온라인 주문','CRM','통합 핵심 저장소\n고객 식별·정합성','영업 마트','재무 마트','마케팅 마트'],[(0,3),(1,3),(2,3),(3,4),(3,5),(3,6)])
diagram('bus','적합 차원으로 연결하는 버스 아키텍처',['주문 팩트','환불 팩트','구독 팩트','공통 고객 차원','공통 날짜 차원','같은 차원 수준으로 집계\n그 뒤 지표 결합'],[(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(0,5),(1,5),(2,5)])
diagram('lambda','람다의 이중 처리 경로',['불변 입력 기록','배치 재계산\n확정값','저지연 경로\n최근·잠정값','결과 경계 선택\n중복 영역 제거','조회 API / 대시보드'],[(0,1),(0,2),(1,3,'확정 경계까지'),(2,3,'경계 이후'),(3,4)])
diagram('kappa','카파의 로그 재생과 투영 버전',['보존된 이벤트 로그','단일 스트림 로직','현재 투영 v1','재생용 동일 로직\n새 소비자·상태','후보 투영 v2','대사 후 읽기 전환'],[(0,1),(1,2),(0,3,'replay'),(3,4),(2,5),(4,5)])
diagram('lakehouse','레이크하우스의 역할 구분',['객체 저장소\n데이터 파일','테이블 메타데이터\n스냅샷·스키마','카탈로그\n위치·권한·이름','쿼리 엔진\nTrino / Spark 등','dbt\nSQL 변환·테스트','소비자\nBI / ML'],[(0,1),(1,2),(2,3),(4,3,'SQL 요청'),(3,5)])
diagram('mesh','데이터 메시의 계약 경계',['주문 도메인\n소유자 + 공개 데이터','고객 도메인\n소유자 + 공개 데이터','구독 도메인\n소유자 + 공개 데이터','공통 셀프서비스 플랫폼\n배포·관측·권한','연합 거버넌스\n공통 키·정책·호환성','분석 소비자'],[(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(0,5),(1,5),(2,5)])
diagram('fabric','패브릭·가상화·실물화를 구분',['원천 A','원천 B','연합 쿼리 계층\n접근을 통합','메타데이터·정책·계보\n관리와 자동화','반복 조회 결과를\n선별 실물화','dbt 마트'],[(0,2),(1,2),(3,2),(2,4),(4,5)])
diagram('vault','Data Vault의 세 가지 중심 구성',['Hub Customer\n업무 키','Link Customer Order\n관계의 키','Hub Order\n업무 키','Satellite Customer\n속성·관측 이력','Satellite Order\n상태·금액 이력','소비용 마트'],[(0,1),(2,1),(0,3),(2,4),(3,5),(1,5),(4,5)])
diagram('staging-dag','표준화에서 소비 모델로',['source: 주문 변경','stg_order_changes\n전달 중복 제거','stg_orders_current\n최신 업무 상태','int_orders_classified\n업무 품질 판정','fct_orders\n주문 grain','mart_daily_sales\n일 grain'],[(0,1),(1,2),(2,3),(3,4),(4,5)])
diagram('star','주문 상세 스타 스키마',['dim_customer\n고객','dim_product\n상품','fct_order_lines\n주문 상세 한 행','dim_date\n날짜','dim_channel\n채널'],[(0,2),(1,2),(3,2),(4,2)])
diagram('fanout','잘못된 조인의 금액 증폭',['주문 5003\n금액 29.00','상세 A\n18.00','상세 B\n11.00','헤더 금액을 복제\n29.00 + 29.00 = 58.00','정상: 상세 금액 합\n18.00 + 11.00 = 29.00'],[(0,1),(0,2),(1,3),(2,3),(1,4),(2,4)])
diagram('facts','서로 다른 팩트의 grain',['업무: 주문·재고·배송','거래 팩트\n판매 상세 1건','주기 스냅샷\n상품·창고·하루','누적 스냅샷\n배송 업무 1건','무측정 팩트\n고객·프로모션 자격'],[(0,1),(0,2),(0,3),(0,4)])
diagram('scd2','시점 차원과 반열린 구간',['고객 103\nstandard\n01-01 ≤ t < 04-03','고객 103\nvip\n04-03 ≤ t','주문 5003\n04-02 00:00','현재 고객 보고서\nvip','주문 당시 보고서\nstandard'],[(0,1,'유효 경계'),(2,0,'as-of 조인'),(1,3),(0,4)])
diagram('cdc','변경 전달과 현재 상태 투영',['업무 트랜잭션\n원천 상태 + outbox','CDC / 이벤트 전달\n중복·지연 가능','불변 적재 기록','업무 순서로 최신 선택','삭제 이벤트 판정','현재 상태'],[(0,1),(1,2),(2,3),(3,4),(4,5)])
diagram('watermark','처리 경계와 사건 발생시각',['업무 발생\n04-01 주문 5005','실제 수신\n04-05 도착','수신 경계로 발견\nsource offset / ingestion','영향받는 주문 키\n5005','04-01 일별 마트 재계산'],[(0,1),(1,2),(2,3),(3,4)])
diagram('quality','허용·격리·복구 흐름',['현재 원천 행 6개','판정 규칙\n키·상태·금액·대사','허용 4개\n발행 후보','격리 2개\n누락 고객·음수','원천 정정 / 고객 도착','재판정 후 허용 6개'],[(0,1),(1,2),(1,3),(3,4),(4,5)])
diagram('routing','논리 이름과 물리 위치 분리',['SQL\nref / source','논리 계층\nl0 / l1 / l2 / l3','중앙 매핑\n스키마·카탈로그','환경 네임스페이스\ndev_A / dev_B / prod','물리 relation\n단일 쓰기 소유자'],[(0,1),(1,2),(2,3),(3,4)])
diagram('components','순수 계산과 단일 쓰기 소유자',['컴포넌트 A\n명시된 출력 계약','컴포넌트 B\nresult_mode 있음','컴포넌트 C\n고정 연산 메타데이터','정규화·중복 키 검사','통합 계산 결과','단일 owner\n쓰기·커밋·로그'],[(0,3),(1,3),(2,3),(3,4),(4,5)])
diagram('ci','검증에서 발행까지',['변경 SQL / 계약','전체 파싱·정적 정책','변경 + 영향 모델 빌드','고정 기준선과 대사','승인·읽기 포인터 전환','롤백 가능한 이전 버전'],[(0,1),(1,2),(2,3),(3,4),(4,5)])
diagram('observability','실패 위치별 관측',['입력 완전성\n파일·오프셋·배치','계산 실행\n구문·계획·리소스','데이터 검증\n행·금액·분포','발행 상태\n현재 버전·신선도','외부 전달\n멱등 키·응답'],[(0,1),(1,2),(2,3),(3,4)])
diagram('privacy','보존과 삭제 의무의 분리',['원천 접근 제한','최소화·가명화','분석용 모델','공개 마트','삭제 요청·보존 정책','복제·백업·과거 버전 점검'],[(0,1),(1,2),(2,3),(4,0),(4,2),(4,3),(4,5)])
diagram('journey','마당마켓의 다섯 데이터 단계',['P1\n기준선\n27.00','P2\n늦은 주문\n118.00','P3\n정정·취소\n107.00','P4\n삭제·격리\n95.00','P5\n복구 완료\n130.00'],[(0,1),(1,2),(2,3),(3,4)])
diagram('final-architecture','마당마켓 최종 배치 구조',['원천 변경·웹 이벤트·구독','L0 원본 및 수신 메타데이터','L1 표준화·최신 상태','L2 통합·검증·시간 구간','L3 팩트·차원·업무 지표','공개 계약 + 문서 + 테스트','BI / 운영 전달','오케스트레이터\n재시도·배치 경계·발행'],[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(7,1),(7,4),(7,5)])
diagram('incremental','변경 키 재계산과 전체 결과 비교',['이번 배치 주문 변경','상세 변경','고객 변경','영향받는 주문 키의 합집합','최신 원천으로 재계산','트랜잭션 안에서 키 교체','전체 재계산과 동등성 대사'],[(0,3),(1,3),(2,3),(3,4),(4,5),(5,6)])
diagram('bluegreen','후보 결과의 검증 후 발행',['기존 공개 버전 v1','새 후보 버전 v2','품질·계약·대사 검사','읽기 포인터','소비자','실패 시 v1 유지'],[(1,2),(2,3,'통과'),(0,3),(3,4),(2,5,'실패')])
diagram('decision-tree','시간 요구에 따른 첫 설계 판단',['허용 지연은?','시간·일 단위\n단일 배치부터','초·분 단위\n스트림 상태 운영 가능?','가능\n카파 / 스트림 투영 검토','재계산 별도 필요\n람다 비용 검토','단계·모델·소유권은\n별도로 결정'],[(0,1),(0,2),(2,3),(2,4),(1,5),(3,5),(4,5)])
diagram('boundary-matrix','책임 경계와 도구의 자리',['ETL / CDC 도구\n데이터를 가져온다','dbt\nSQL로 변환·검증한다','오케스트레이터\n실행 시점·의존성을 조율','카탈로그 / IAM\n이름·권한·정책','소비 API / Reverse ETL\n외부에 전달한다'],[(0,1),(2,0),(2,1),(3,0),(3,1),(1,4)])
diagram('wide-vs-star','중앙 표준 모델과 목적별 wide 모델',['원천 통합','공통 팩트·차원','일별 요약 wide','고객 현황 wide','분석 목적별 파생','원천마다 별도 wide\n정의 불일치 위험'],[(0,1),(1,2),(1,3),(2,4),(3,4),(0,5,'반례')])
diagram('bitemporal','유효시간과 관측시간',['업무 유효시간\n언제 실제로 유효했나?','시스템 관측시간\n언제 알게 되었나?','4월 2일 주문 당시 사실','4월 3일 보고서가 알던 사실','4월 5일 정정 후 재작성'],[(0,2),(1,3),(0,4),(1,4)])
diagram('anchor','Anchor의 식별과 속성 이력',['고객 Anchor\ncustomer_id = 103','등급 Attribute\nstandard → vip','주소 Attribute\n별도의 변경 주기','시점별 조합 조회','소비용 고객 차원'],[(0,1),(0,2),(1,3),(2,3),(3,4)])
diagram('model-branches','동일 입력의 모델링 비교',['마당마켓 정상 현재 주문','스타','정규화 코어','Wide','Vault 단편','Anchor 단편','같은 주문별 결과 대사\n성능 우열 시험은 아님'],[(0,i) for i in range(1,6)]+[(i,6) for i in range(1,6)])
(R/'assets/figure-manifest.json').write_text(json.dumps(diagrams,ensure_ascii=False,indent=2))
print('generated',len(diagrams),'original diagrams')
