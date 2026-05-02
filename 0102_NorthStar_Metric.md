# 1-2. North Star Metric & Input Metrics

## 핵심 정의
NSM(North Star Metric) : 제품이 고객에게 전달하는 핵심 가치를 가장 잘 반영하는 단일 지표. 회사 전체가 한 방향으로 정렬되도록 만드는 "별"
- Amplitude의 John Cutler가 정립한 개념으로, "이 숫자 하나만 오르면 사업이 건강해진다"는 지표예요.

### 좋은 NSM의 3대 조건
1. 고객 가치 반영 (단순 매출/MAU X)
2. 반복 행동 측정 (일회성 X / 습관 O)
3. 장기 성장 선행지표 (회사의 장기 성장을 선행)

#### 유명한 사례
Airbnb: "예약된 박(nights booked)"
Spotify: "Time spent listening"
Facebook: "Monthly Active Users"
Slack: "조직 내 주 2,000메시지 이상 보낸 팀 수"

### NSM vs. Vanity Metric
| 분류 | NSM 후보 | 이유 |
|---|---|---|
| ❌ Vanity | 회원 가입자 수 | 가입만 하고 사라지는 유저 포함 |
| ❌ Vanity | 페이지뷰 | 가치 전달과 분리될 수 있음 |
| ✅ NSM | 주간 활성 유저(WAU) | 반복 사용 측정 |
| ✅ NSM | 월간 재구매 고객 수 | 반복 가치 + 충성도 |
| ✅ NSM | 주 2,000+ 메시지 팀 수 (Slack) | 임계값 기반, 진짜 활성 |

### Input Metrics 트리
: NSM은 직접 움직일 수 없는 결과지표. 움직일 수 있는 건 Input Metrics(선행지표)뿐.

NSM : 월간 활성 유지 (MAU)
├─ 신규 활성 유저 (Acquisition)
│  ├─ 트래픽
│  └─ 가입 전환율
├─ 유지 활성 유저 (Retention)
│  ├─ 7일 재방문율
│  └─ 핵심 기능 사용률
└─ 부활 유저 (Resurrection)
   ├─ 이메일 오픈율
   └─ 푸시 클릭률

### Magic Number / Aha Moment
- Facebook : 10일 안에 7명 친구 추가 → 유지율 급등
- Twitter : 30명 팔로우 → 활성 유저 전환
- Slack : 2,000개 메세지 보낸 팀 → 월 churn 거의 0

이런 임계값을 찾으면 NSM이 정의됨.

