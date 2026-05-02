# matplotlib 한국어 깨짐 해결
from bdb import effective
import matplotlib.pyplot as plt
from matplotlib import rcParams

'''
rcParams['font.family'] = 'Malgun Gothic'  # 맑은 고딕
rcParams['axes.unicode_minus'] = False     # 마이너스 부호 깨짐 방지
'''

rcParams['font.family'] = 'AppleGothic' # mac version
rcParams['axes.unicode_minus'] = False


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