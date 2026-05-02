# 실습 1: NSM 후보 평가 (어떤 지표가 진짜 NSM인가?)

import pandas as pd
import numpy as np

# 가상의 코호트 데이터 : 가입 후 30일 시점 + 90일 시점
np.random.default_rng(42)
n = 5000

cohort = pd.DataFrame({
    'user_id' : range(n),
    'd30_logins' : np.random.poisson(3, n),
    'd30_messages_sent' : np.random.poisson(5, n),
    'd30_features_used' : np.random.choice([1, 2, 3, 4, 5], n), 
    'd30_invited_friend' : np.random.binomial(1, 0.3, n), 
    # 90일 시점 retention (0/1)
    'd90_retained' : None
})

# 진짜 NSM 후보 : 어떤 지표가 d90_retained와 가장 강한 상관?
# (시뮬레이션을 위해 messages_sent)와 features_used 기반으로 생성
cohort['d90_retained'] = (
    (cohort['d30_messages_sent'] > 5) & (cohort['d30_features_used'] >= 3)
).astype(int) | np.random.binomial(1, 0.1, n)   # noise

# 각 후보 지표와 d90 retention의 상관계수
candidates = ['d30_logins', 'd30_messages_sent',
              'd30_features_used', 'd30_invited_friend']
print("=== NSM 후보 지표별 90일 유지율과의 상관 ===")
for c in candidates:
    corr = cohort[c].corr(cohort['d90_retained'])
    print(f"{c:30s}: corr = {corr:.3f}")

# 임계값 분석 (각 지표의 어느 값에서 retention이 급등하나?)
print("\n=== d30_messages_sent 임계값별 d90 유지율 ===")
for threshold in [1, 3, 5, 7, 10, 15]:
    above = cohort[cohort['d30_messages_sent'] >= threshold]['d90_retained'].mean()
    n_users = (cohort['d30_messages_sent'] >= threshold).sum()
    print(f"  >= {threshold:2d} messages: 유지율 {above:.1%} (유저 {n_users}명)")


# ===============================================================================
# 실습 2: Input Metric 트리 분해 + 기여도 계산

import pandas as pd
import numpy as np

# MAU = 신규 + 유지 + 부활 (분해)
months = pd.date_range('2024-01', periods=12, freq='ME')
data = pd.DataFrame({
    'month': months,
    'new_active': [1200, 1300, 1450, 1500, 1600, 1750, 1800, 1900, 2000, 2100, 2200, 2300],
    'retained_active': [3000, 3200, 3400, 3500, 3700, 3850, 4000, 4100, 4200, 4300, 4400, 4500],
    'resurrected_active': [200, 220, 250, 240, 270, 280, 290, 310, 320, 340, 350, 360],
})
data['MAU'] = data[['new_active', 'retained_active', 'resurrected_active']].sum(axis=1)

# 각 input의 MoM 변화율과 MAU 변화율 비교
data['mau_growth'] = data['MAU'].pct_change() * 100
for col in ['new_active', 'retained_active', 'resurrected_active']:
    data[f'{col}_growth'] = data[col].pct_change() * 100

# 각 input이 MAU 증가에 기여한 비율 계산
data['mau_delta'] = data['MAU'].diff()
for col in ['new_active', 'retained_active', 'resurrected_active']:
    delta = data[col].diff()
    data[f'{col}_contribution'] = delta / data['mau_delta']

# 시각화
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 좌: stacked bar
axes[0].bar(data['month'].dt.strftime('%b'), data['new_active'], label='New')
axes[0].bar(data['month'].dt.strftime('%b'), data['retained_active'],
            bottom=data['new_active'], label='Retained')
axes[0].bar(data['month'].dt.strftime('%b'), data['resurrected_active'],
            bottom=data['new_active']+data['retained_active'], label='Resurrected')
axes[0].set_title('MAU decomposition'); axes[0].legend()

# 우: 기여도 추이
contrib_cols = [c for c in data.columns if 'contribution' in c]
axes[1].plot(data['month'].dt.strftime('%b'), data[contrib_cols] * 100, marker='o')
axes[1].set_title('Each input의 MAU 증가 기여도 (%)')
axes[1].legend([c.replace('_contribution', '') for c in contrib_cols])
axes[1].axhline(0, color='k', linewidth=0.5)

plt.tight_layout(); plt.show()


# ===============================================================================
# 실습3: Aha Moment 임계값 찾기 (Decision Tree 활용)

from sklearn.tree import DecisionTreeClassifier, export_text
import pandas as pd
import numpy as np

# 가상의 코호트 데이터: 가입 후 30일 시점 + 90일 시점
np.random.seed(42)
n = 5000

cohort = pd.DataFrame({
    'user_id': range(n),
    'd30_logins': np.random.poisson(3, n),
    'd30_messages_sent': np.random.poisson(5, n),
    'd30_features_used': np.random.choice([1, 2, 3, 4, 5], n),
    'd30_invited_friend': np.random.binomial(1, 0.3, n),
    # 90일 시점 retention (0/1)
    'd90_retained': None
})

# 진짜 NSM 후보: 어떤 지표가 d90_retained와 가장 강한 상관?
# (시뮬레이션을 위해 messages_sent와 features_used 기반으로 생성)
cohort['d90_retained'] = (
    (cohort['d30_messages_sent'] > 5) & (cohort['d30_features_used'] >= 3)
).astype(int) | np.random.binomial(1, 0.1, n)  # noise

# 어떤 행동 조합이 90일 retention을 가장 잘 예측하는가?
features = ['d30_logins', 'd30_messages_sent', 'd30_features_used', 'd30_invited_friend']
X = cohort[features]
y = cohort['d90_retained']

tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=200, random_state=42)
tree.fit(X, y)
print(export_text(tree, feature_names=features))

# 결과 해석:
# tree가 자동으로 찾는 split point들이 곧 Aha moment 후보 임계값
# 예: "messages_sent > 5 AND features_used > 2" 같은 룰

'''
|--- d30_messages_sent <= 5.50
|   |--- d30_messages_sent <= 2.50
|   |   |--- d30_invited_friend <= 0.50
|   |   |   |--- class: 0
|   |   |--- d30_invited_friend >  0.50
|   |   |   |--- class: 0
|   |--- d30_messages_sent >  2.50
|   |   |--- d30_features_used <= 1.50
|   |   |   |--- class: 0
|   |   |--- d30_features_used >  1.50
|   |   |   |--- class: 0
|--- d30_messages_sent >  5.50
|   |--- d30_features_used <= 2.50
|   |   |--- d30_messages_sent <= 6.50
|   |   |   |--- class: 0
|   |   |--- d30_messages_sent >  6.50
|   |   |   |--- class: 0
|   |--- d30_features_used >  2.50
|   |   |--- class: 1
'''