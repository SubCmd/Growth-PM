# 1-1. Growth Loops

## 개념 및 이론
: 전통적 모델인 AARRR 퍼널(획득→활성화→유지→수익→추천)은 물이 위에서 아래로 흐르는 모델임.
유입이 멈추면 성장도 멈춤...

### AARRR 퍼널 방식
Awareness (인지/인식): 잠재 고객이 브랜드나 제품을 처음 인지하는 단계 (노출, 도달율 등).
Acquisition (유입/획득): 고객이 웹사이트나 앱에 방문하거나 설치하는 등 유입되는 단계 (클릭률, 방문자 수).
Activation (활성화): 유입된 고객이 처음으로 가치 있는 경험을 하는 단계 (회원가입, 튜토리얼 완료 등).
Retention (리텐션/유지): 고객이 서비스를 지속적으로 재방문하거나 사용하는 단계 (재방문율, 이탈률).
Referral (추천): 기존 고객이 지인에게 제품을 추천하여 신규 유입을 유도하는 단계 (공유, 추천율).
Revenue (매출/수익): 고객이 구매하여 최종적으로 기업에 수익을 창출하는 단계 (결제율, 평균 결제액)
> AARRR은 마케팅비가 끊기면 흐름이 멈춤.

> 즉, 한 번 유저를 획득하면 그 유저는 단계를 거치며 줄어들기만 함.
> 신규 유입을 위해서는 항상 외부에서 새로운 물을 부어줘야 함.

- Loop(루프): 유저의 행동 결과가 다시 신규 유입 연료가 되는 구조.
> 한 번 돌아가기 시작하면, 외부 투입 없어도 스스로 다음 사이클을 만들어냄.

> 퍼널(funnel): "물의 흐름" (외부 펌프 필요)
> Loop: "엔진" (내부 연소로 동력 생산)

- 왜 중요한가?
: Reforge의 Brian Balfour, Andrew Chen 등이 강조한 핵심
```
시장 성숙이게 진입한 회사는 퍼널 최적화만으로는 더 이상 성장 못한다.
한계 CAC(Customer Acquisition Cost)가 계속 오르기 때문에, 결국 "자기강화 메커니즘"이 있어야 지속 성장이 가능
```

- 예시)
> 퍼널 사고:  "광고 노출 → 클릭 → 가입 → 활성화" (광고비가 멈추면 가입도 멈춤)
> 루프 사고: "Dropbox 유저가 친구에게 파일 공유 → 친구가 가입 → 그 친구도 다른 친구에게 공유" (외부 입력 없이 자생)

### 4단계 구조 상세 해부

: 사용자의 행동 결과(Output)가 다시 신규 유입 연료(Input)로 돌아오는 자기강화 사이클

> Reforge의 Brian Balfour가 정립한 핵심 원칙
- 4단계 구조
```
Input → Action → Output → Reinvestment → (다시 Input)
```

-> 회사마다 주력 Loop는 1 ~ 2개로 압축됨.
예) Notion = UGC + Viral Loop

### 주요 Loop 유형
1. Viral Loop : 사용자가 제품을 쓰면서 다른 사용자를 끌어옴 (Drop Box 초대)
2. Content Loop : 사용자 콘텐츠가 검색 유입을 만듦 (Pinterest 핀, Stack Overflow 답변)
3. Paid Loop : 매출 → 광고비 재투자 → 신규 고객 (D2C 브랜드)
4. Sales-assisted Loop : PLG에서 sales motion이 개입하는 B2B
 
| 유형 | 대표 사례 | Action | Output | 회사가 투자할 자원 |
|---|---|---|---|---|
| Viral | Dropbox, Calendly | 초대/공유 | 신규 가입자 | UI 마찰 제거 |
| Content | Pinterest, SO | 콘텐츠 생성 | SEO 트래픽 | 콘텐츠 품질·생성 도구 |
| Paid | D2C 브랜드 | 구매 | 매출 → 광고비 | LTV/CAC 최적화 |
| UGC | YouTube, TikTok | 창작 | 시청 트래픽 | 창작자 수익화 |


예) - 현재 우리 서비스 "대학 입시 RAG 툴에 적용"
Input: 수험생 유입 (SEO/커뮤니티)
Action: 점수 입력 → AI 진단 리포트 받음
Output: 리포트를 오픈채팅방/인스타/블로그에 공유 ("나 이 대학 적정이래")
Reinvest: 공유된 스크린샷이 다른 수험생의 호기심 → 사이트 방문 → 새 Input

### Loop 수학 : K-factor (Viral Coefficient)
```
K = i × c
 
i = 유저 1명당 초대/공유 횟수
c = 초대받은 사람의 전환율
```
- K > 1 : 자생적 폭발 성장 (현실에서 드뭄)
- K < 1 : 감쇠하지만 paid acquisition을 증폭
- K = 0.5 : 유료 100명 획득 시: 100 / (1-0.5) = 200명 (2배 증폭 효과)

> MCP 활용 실무 적용
> Amplitude MCP / GA4 MCP
> Notion/Slack MCP
> Custom MCP 서버