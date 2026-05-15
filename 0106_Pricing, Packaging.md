# 1-6. Pricing & Packaging

## 개념 및 정의
- Value Metric (가치 측정 단위)
: 유저가 느끼는 가치와 선형 비례해서 올라가는 과금 단위

```
"고객의 성공 = 매출 증가"
# 잘못된 Value Metric: 고객과 회사의 인센티브를 어긋나게 만듦.
예) 월정액 - light user는 비싸게 사용하는 느낌
          - heavy user는 싸게 쓰는 느낌
```

- 좋은 Value Metric
1. Slack의 "active user 수": 회사가 성장해서 직원이 늘면 Slack 가치도 같이 커짐.
2. Zapier의 "실행 횟수": 자동화가 많이 돌아갈수록 시간이 절약
3. OpenAI API의 "토큰 수": 더 많은 작업할 수록 더 많은 비용

- 나쁜 Value Metric
1. 단순 "저장 용량": 1TB 사용하는 고객이 100GB고객보다 10배 높은 가치라 할 수 없음
2. "월 정액": 가치와 분리됨

| 좋은 Value Metric | 나쁜 Value Metric |
|---|---|
| Active users (Slack) | 단순 월정액 |
| API call (Anthropic) | 저장 용량만 |
| Workflow 실행 수 (Zapier) | 사용자 무관 flat |

#### 좋은 Value Metric 판별 체크리스트
1. 고객이 직관적으로 이해하는가?
2. 가치 인식과 같이 자라는가?
3. 예측 가능한가?
4. 측정과 청구가 명확한가?


### 3가지 Pricing 모델
#### Flat Rate (정액제)
: 모든 고객에게 하나의 가격. Basecamp가 대표적 예($99/월로 무제한.)
> 장점: 영업 사이클로 짧고, 의사결정 단순, 매출 예측 쉬움
> 단점: 헤비 유저로 가치를 회수 못함. 라이트 유저는 비싸다고 느낌
> 적합한 때: 제품이 단순하고, 타켓 고객의 사용 패턴이 균일할 때, 초기 단계

#### Tiered (티어드)
: Good-Better-Best 같은 패키지로 묶어서 판매. SaaS의 표준
> 장점: 서로 다른 페르소나(스타트업/중견/엔터프라이즈) 동시 공략. 업그레이드 경로 명확
> 단점: 어떤 기능을 어디에 넣을지(Feature Fencing) 매우 어려움. 잘못 설계하면 고객이 "내 티어에 필요한 기능이 하나도 없다"라는 상황 발생
> 적합한 때: B2B SaaS, 여러 페르소나가 명확히 구분될 때

#### Usage-Based (사용량 기반)
: 실제 사용한 만큼만 과금. AWS, Twilio, OpenAI API 등이 대표
> 장점: 가치-과금 정렬이 가장 강함. 진입 장벽 매우 낮음("쓴 만큼만"). PLG와 궁합 좋음
> 단점: Bill Shock - 갑자기 다음 달 청구서가 10배 나오는 공포. 매출 예측 어려움. 고객의 예산 편성 어려움
> 적합한 때: AI, 인프라, API 비즈니스. 보통 "Committed minimum + Overage" 같은 하이브리드로 보완.

| 모델 | 적합한 상황 | 예측가능성 | 단점 |
|---|---|---|---|
| Flat rate | 초기, 단순 | 매우 높음 | 사용량 증가 시 손해 |
| Tiered | B2B, multiple personas | 높음 | tier 결정 복잡 |
| Usage-based | AI/인프라 | 낮음 | bill shock 위험 |


### 3-Tier Rule (Kyle Poyar의 매직 넘버)
: OpenView Partners의 PLG 전문가 Kyle Poyar가 강조한 원칙
- 3개가 magic number
1. Hick's Law: 선택지가 많아질수록 의사결정 시간이 로그함수로 증가.
4개 이상은 "결정 마비(Decision Paralysis)"를 유발
2. 인지 부담: 사람은 3개까지는 비교를 쉽게 하지만, 그 이상은 표를 그려야 비교 가능.
3. Compromise Effect: 3개 중 가운데를 고르는 심리. 가운데에 마진이 좋은 옵션을 놓으면 자연스럽게 그게 가장 많이 팔림.

- Good-Better-Best: 중간이 가장 많이 팔리도록
> Good: 진입용. 핵심 가치는 주지만, 협업/스케일은 제한
> Better: 가장 많이 팔리길 원하는 옵션. 마진과 기능의 스위트 스팟
> Best: 엔터프라이즈/대규모용. 가격을 일부러 비싸게 책정해 Better를 매력적으로 만듦


### Decoy Effect (미끼 효과)
: 행동경제학의 Asymmetric Dominance Effect에서 출발한 개념. 한 옵션을 일부러 매력 없게 만들어,
옆의 옵션을 더 매력적으로 보이게 함.

- 고전적인 The Economist 사례 (Dan Ariely):
> Web only: $59
> Print only: $125 <- 미끼
> Print + Web: $125
: Print only가 Print + Web과 같은 가격이라는게 비합리적이죠. 그래서 거의 모두가 Print + Web을 선택.
Print only를 빼고 실험하면, 다수가 Web only로 옮겨갑니다.
즉, "미끼"가 더 비싼 옵션을 팔게 만든 것임.

- $20 / $50 / $55 예시 해석:
> $20은 너무 싸 보여서 "품질이 의심" (Too Cheap 영역)
> $55는 $50과 비교했을 때 5달러 차이로 훨씬 많은 가치를 주는 것처럼 설계됨
그래서 $50이 "가성비 최고" 위치를 차지함.
=> 결과: 대부분 $50 선택

→ 실전 적용: 가운데 티어를 가장 팔고 싶다면, 상위 티어를 매력적으로 보이게 만들지 말고,
  가운데 티어가 상위 대비 가성비 있게 느껴지도록 가격 갭을 설계함.


### Feature Fencing (기능 분배 전략)
: 티어를 만들 때 가장 어려운 부분 - "어느 기능을 어느 티어에 넣을 것인가."

- 3가지 기능 분류:
| 분류 | 위치 | 이유 | 
| --- | --- | --- |
| Adoption-driving | Free/Lower | 사용자를 끌어들이고 습관화 (Aha moment) |
| Power Feature | Mid/Higher | 업그레이드 동기 부여 (Pay-to-unlock) | 
| Enterprise Feature | Top | SSO, SLA, Audit log, 전담 지원 | 

- 핵심 원칙:
1. 무료에는 "가치는 주되, 확장은 막는다." 예) Notion 무료는 1인 무제한이지만, 협업은 블록 1,000개 제한
2. 결제 동기가 명확해야 한다. 무료에 너무 많이 주면 유료 전환이 없고, 너무 적게 주면 신규 유저가 안 옴.
3. Power Feature는 대개 협업/자동화/API/팀 관리. 이런 건 진짜로 필요한 사람만 필요해서 페이먼트 트리거가 강함.\

→ 실수 예:
> 가장 중요한 기능을 최상위 티어에만 넣어버려서 중간 티어가 안 팔리는 경우.
> 반대로 무료에 너무 많이 줘서 유료 전환율 1% 미만으로 떨어지는 경우.


### Van Westendorp Price Sensitivity Meter (PSM)
: 네덜란드 경제학자 Peter van Westendorp가 1976년에 만든 가격 민감도 측정 기법.
고객에게 직접 가격을 물어보는 설문 방법론

- 4가지 질문:
1. 너무 비싸서 안 살 가격? (Too expensive)
2. 비싸지만 고민하면 살 가격? (Expensive)
3. 가성비 좋다고 느낄 가격? (Cheap / **Good Value**)
4. 너무 싸서 품질 의심할 가격? (Too cheap)

- 분석 방법: 응답을 누적 분포 곡선 4개로 그림. 곡선들의 교차점에서 4개의 중요한 가격대가 나옴.
1. Point of Marginal Cheapness (PMC): "너무 쌈" 곡선과 "쌈" 곡선의 교차점 → 가격의 하한선
2. Optimal Price Point (OPP): "너무 쌈"과 "너무 비쌈"의 교차점 → 저항이 최소인 최적 가격
3. Indifference Price Point (IPP): "쌈"과 "비쌈"의 교차점 → 중간값, 일반적으로 시장 평균가
4. Point of Marginal Expensiveness (PME): "비쌈"과 "너무 비쌈"의 교차점 → 가격의 상한선

**수용 가능 가격대 = PMC ~ PME 사이**
- 장점: 설문만으로 신제품의 가격 범위를 추정할 수 있음. 경쟁 정보가 없는 신시장에 유용.
- 한계
1. Stated vs. Revealed Preference: 사람들이 말로 하는 가격과 실제 지갑을 여는 가격은 다름.
2. 경쟁 제품을 고려하지 않음.
3. 가치를 잘 모르는 신제품은 응답 자체가 부정확
4. 그래서 보통 Conjoint 분석이나 A/B 가격 테스트와 함께 씀 