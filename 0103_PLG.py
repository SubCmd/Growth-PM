# 실습 1: Time to Value(TTV) 측정
# 신규 가입자의 가입의 가입-첫 Activation까지 시간 분포
import numpy as np
import pandas as pd

np.random.seed(42)
n = 3000

events = pd.DataFrame({
    'user_id': range(n),
    'signup_at': pd.date_range('2024-01-01', periods=n, freq='30min'),
})

# 80%는 활성화, 활성화하는 사람의 TTV는 lognormal
activated = np.random.binomial(1, 0.8, n).astype(bool)
ttv_minutes = np.where(
    activated,
    np.random.lognormal(mean=4, sigma=1, size=n),
    np.nan
)
events['ttv_minutes'] = ttv_minutes
events['activated'] = activated

# TTV 분포 확인
print(f"Activation rate: {events['activated'].mean():.1%}")
print(f"\nTTV 분포 (활성화한 유저만, 단위: 분):")
print(events.loc[events['activated'], 'ttv_minutes'].describe())
print(f"\nMedian TTV: {events.loc[events['activated'], 'ttv_minutes'].median():.1f}분")
print(f"P90 TTV: {events.loc[events['activated'], 'ttv_minutes'].quantile(0.9):.1f}분")

# 시각화
fig, axes = plt.subplots(1, 2, figsize=(14, 4))
axes[0].hist(events.loc[events['activated'], 'ttv_minutes'], bins=50)
axes[0].set_xlim(0, 600)
axes[0].set_title('TTV 분포 (분)')
axes[0].axvline(events.loc[events['activated'], 'ttv_minutes'].median(),
                color='r', linestyle='--', label='Median')
axes[0].legend()

# Cumulative Activation
sorted_ttv = events.loc[events['activated'], 'ttv_minutes'].sort_values()
axes[1].plot(sorted_ttv, np.arange(1, len(sorted_ttv)+1) / n)
axes[1].set_title('누적 Activation 비율 vs 시간')
axes[1].set_xlabel('Minutes since signup'); axes[1].set_ylabel('Cumulative activation')
axes[1].set_xlim(0, 600); axes[1].grid(alpha=0.3)
plt.tight_layout(); plt.show()


# ===============================================================================
# 실습 2: Activation 정의 + Retention 검증
import numpy as np
import pandas as pd

np.random.seed(42)
n = 5000

# Day 0~7 행동 데이터 + Day 30 retention
users = pd.DataFrame({
    'user_id': range(n),
    'signup_features_used': np.random.choice([0, 1, 2, 3, 4], n, p=[0.2, 0.3, 0.25, 0.15, 0.1]),
    'first_week_logins': np.random.poisson(3, n),
    'created_first_artifact': np.random.binomial(1, 0.4, n),
    'invited_team_member': np.random.binomial(1, 0.15, n),
})

# Day 30 retention (시뮬레이션 : 어떤 조합이 retention 만드는지?)
users['d30_retained'] = (
    (users['signup_features_used'] >= 2) &
    (users['first_week_logins'] >= 3) &
    (users['created_first_artifact'] == 1)
).astype(int)
# add noise
users['d30_retained'] = (users['d30_retained'] |
                         np.random.binomial(1, 0.05, n)).astype(int)

# 다양한 Activation 정의 후보 평가
candidates = {
    "1주에 3+ 로그인": (users['first_week_logins'] >= 3),
    "첫 artifact 생성": (users['created_first_artifact'] == 1),
    "팀원 초대": (users['invited_team_member'] == 1),
    "기능 2+ 사용": (users['signup_features_used'] >= 2),
    "복합: 로그인 3+ AND artifact 생성":
        (users['first_week_logins'] >= 3) & (users['created_first_artifact'] == 1),
}

print("=== Activation 정의 후보 평가 ===")
print(f"{'Definition':<40} {'활성화율':<10} {'유지율(활성O)':<15} {'유지율(활성X)':<15} {'Lift':<8}")
print("-" * 90)
for name, mask in candidates.items():
    activation_rate = mask.mean()
    retained_active = users.loc[mask, 'd30_retained'].mean()
    retained_inactive = users.loc[~mask, 'd30_retained'].mean()
    lift = retained_active / retained_inactive if retained_inactive > 0 else float('inf')
    print(f"{name:<40} {activation_rate:.1%}      {retained_active:.1%}           "
          f"{retained_inactive:.1%}           {lift:.1f}x")

'''
=== Activation 정의 후보 평가 ===
Definition                               활성화율       유지율(활성O)        유지율(활성X)        Lift
------------------------------------------------------------------------------------------
1주에 3+ 로그인                               58.0%      23.2%           5.3%           4.4x
첫 artifact 생성                            39.2%      31.8%           5.3%           6.0x
팀원 초대                                    14.9%      16.8%           15.5%           1.1x
기능 2+ 사용                                 50.0%      26.7%           4.7%           5.7x
복합: 로그인 3+ AND artifact 생성               22.7%      51.9%           5.1%           10.2x
'''


# ===============================================================================
# 실습 3: Cohort Retention Curve (PLG 핵심 지표)
import numpy as np
import pandas as pd
import seaborn as sns

np.random.seed(42)

# 6개월간 매월 코호트 시뮬레이션
cohorts=[]
for cohort_month in range(6):
    n_cohort = 1000 - cohort_month * 50 # 월별 가입자 수 다르게
    base_retention = [1.0, 0.6, 0.45, 0.38, 0.34, 0.32, 0.31]  # 일반적 SaaS curve
    for week, ret in enumerate(base_retention):
        noise = np.random.normal(0, 0.02)
        retained = int(n_cohort * (ret + noise))
        cohorts.append({
            'cohort': f'M{cohort_month+1}',
            'week': week,
            'cohort_size': n_cohort,
            'retained': retained,
            'retention_rate': retained / n_cohort
        })

cohort_df = pd.DataFrame(cohorts)

# Cohort 테이블 (피벗)
pivot = cohort_df.pivot_table(index='cohort', columns='week',
                              values='retention_rate', aggfunc='mean')
print("=== Cohort Retention Heatmap ===")
print((pivot * 100).round(1).fillna(''))

# 시각화
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot * 100, annot=True, fmt='.1f', cmap='YlGnBu',
            cbar_kws={'label': 'Retention %'}, ax=ax)
ax.set_title('Weekly Retention Cohort Heatmap')
plt.tight_layout(); plt.show()

# Smile curve 확인 (retention이 안정화되는 지점)
avg_retention = cohort_df.groupby('week')['retention_rate'].mean()
print(f"\nAvg retention curve: {avg_retention.round(3).to_dict()}")


# ===============================================================================
# Q1 (기초)
# 다음 PLG pricing 시나리오 중 어느 것이 가장 적합한지 골라보세요.

# (a) 단순한 협업 도구, 가치 즉시 체감
# (b) 복잡한 데이터 분석 SaaS, 가치 인지에 시간 필요
# (c) AI 코딩 어시스턴트

# (a) : freemium : 즉각 체험 가능 & 무료 영구 사용 가능
# (b) : free Trial 14 ~ 30일 : 가치 인지 시간 필요 -> 압박 필요
# (c) : Reverse Trial : 핵심 기능 즉시 보여줘야 함! -> 강력한 on-boarding 능력