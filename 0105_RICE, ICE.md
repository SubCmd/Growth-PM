# 1-5. RICE/ICE 우선순위화

## 개념 및 정의
- 이론
: 실험/기능 백로그가 쌓이면 "무엇을 먼저 할지"가 항상 병목이다.
RICE/ICE는 정량적 점수 매김으로 이 의사결정을 투명하게 만드는 프레임워크

- ICE Score (간단, Sean Ellis)
> Impact : 이 실험이 성공하면 지표가 얼마나 움직일까? (1~10)
> Confidence : 성공할 확률에 대한 확신? (1~10)
> Ease : 구현이 얼마나 쉬운가? (1~10)
      ICE = (I + C + E) / 3

- RICE Score (정교, Intercom)
> Reach : 일정 기간 내 몇 명의 유저가 영향받나? (절대 수치)
> Impact : 유저당 영향도 (3=massive, 2=high, 1=medium, 0.5=low, 0.25-minimal)
> Confidence : 추정에 대한 신뢰도 (100%/80%/50%)
> Effort : person-months (작을수록 좋음)
      RICE = (R x I x C) / E

ICE의 함정 : "내가 하고 싶은 실험일수록 Impact/Confidence를 높게 매김"
> team calibration 필요 (같은 실험을 3명이 평가해서 분산 체크)

RICE의 함정
1. Confidence inflation : PM이 자기가 하고 싶은 거에 confidence 높게
2. Effort underestimation : 개발자 합의 없이 PM 혼자 추정
3. Reach 측정 어려움 : 신기능은 "영향 받을 유저"가 모호


- Calibration의 중요성
1. 같은 실험을 3명이 평가했을 때 점수 분산이 크면 -> 정의 모호
2. Wide-band Delphi : 분산 줄이기 위한 반복 평가


🔹 예시 — 백로그 우선순위 (가상)
| 실험 | Reach | Impact | Confidence | Effort | RICE |
| --- | --- | --- | --- | --- | --- |
| 온보딩 체크리스트 추가 | 5,000 | 2 | 80% | 2 | 4,000 |
| 프리미엄 업셀 배너 | 2,000 | 3 | 50% | 1 | 3,000 |
| 다크모드 출시 | 8,000 | 0.5 | 100% | 3 | 1,333 |

-> 온보딩 체크리스트가 우선순위 1위


### 실무 포인트
"RICE는 정답을 주는 도구가 아닌, 대화를 구조화하는 도구이다.
이 실험의 Confidence가 왜 80%인지?'를 팀이 논의하는 과정이 핵심.
점수 자체에 매목되면 안 된다."