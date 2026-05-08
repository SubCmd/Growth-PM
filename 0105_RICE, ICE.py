# 실습 1: RICE 계산기 + 백로그 정렬

import pandas as pd
import numpy as np

backlog = pd.DataFrame({
    'experiment': [
        '온보딩 체크리스트',
        '프리미엄 업셀 배너',
        '다크 모드',
        '추천 알고리즘 v2',
        '결제 페이지 simplify',
        '이메일 onboarding 시퀀스',
        '모바일 앱 출시',
    ],
    'reach': [5000, 2000, 8000, 4000, 3500, 6000, 10000],
    'impact': [2, 3, 0.5, 2, 3, 1, 3],
    'confidence': [0.8, 0.5, 1.0, 0.5, 0.9, 0.8, 0.3],
    'effort': [2, 1, 3, 6, 1, 2, 12],  # person-months
})

# RICE Score 계산
backlog['rice'] = (backlog['reach'] * backlog['impact'] *
                    backlog['confidence']) / backlog['effort']

# ICE Score (참고용)
backlog['ice'] = (backlog['impact'] * 3 +  # 1-10 scale로 변환
                   backlog['confidence'] * 10 +
                   (1/backlog['effort']) * 30) / 3

# 정렬
backlog_sorted = backlog.sort_values('rice', ascending=False).reset_index(drop=True)
backlog_sorted['rank'] = backlog_sorted.index + 1

print(backlog_sorted[['rank', 'experiment', 'reach', 'impact', 'confidence',
                      'effort', 'rice']].to_string(index=False))

# ===============================================================================
# 실습 2: Sensitivity Analysis (Confidence가 흔들릴 때)
import pandas as pd
import numpy as np

backlog = pd.DataFrame({
    'experiment': [
        '온보딩 체크리스트',
        '프리미엄 업셀 배너',
        '다크 모드',
        '추천 알고리즘 v2',
        '결제 페이지 simplify',
        '이메일 onboarding 시퀀스',
        '모바일 앱 출시',
    ],
    'reach': [5000, 2000, 8000, 4000, 3500, 6000, 10000],
    'impact': [2, 3, 0.5, 2, 3, 1, 3],
    'confidence': [0.8, 0.5, 1.0, 0.5, 0.9, 0.8, 0.3],
    'effort': [2, 1, 3, 6, 1, 2, 12],  # person-months
})

# 각 실험의 RICE가 confidence 변화에 얼마나 민감한지
def sensitivity_analysis(row, conf_range=[0.3, 0.5, 0.7, 0.9, 1.0]):
    results = []
    for conf in conf_range:
        rice = row['reach'] * row['impact'] * conf / row['effort']
        results.append(rice)
    return results

sens_data = []
for _, row in backlog.iterrows():
    rices = sensitivity_analysis(row)
    sens_data.append({
        'experiment': row['experiment'],
        **{f'conf_{c}': r for c, r in zip([0.3, 0.5, 0.7, 0.9, 1.0], rices)}
    })

sens_df = pd.DataFrame(sens_data)
print(sens_df.to_string(index=False))

# 시각화: 어떤 실험이 confidence 민감한가?
fig, ax = plt.subplots(figsize=(10, 6))
for _, row in sens_df.iterrows():
    ax.plot([0.3, 0.5, 0.7, 0.9, 1.0],
            [row[f'conf_{c}'] for c in [0.3, 0.5, 0.7, 0.9, 1.0]],
            marker='o', label=row['experiment'])
ax.set_xlabel('Confidence'); ax.set_ylabel('RICE Score')
ax.set_title('RICE Score Sensitivity to Confidence')
ax.legend(loc='best', fontsize=8); ax.grid(alpha=0.3)
plt.tight_layout(); plt.show()

# 핵심 인사이트: 기울기가 가파른 실험은 confidence 검증이 더 중요

# ===============================================================================
# 실습 3: Team Calibration Score 분석 (3인 평가)

import pandas as pd
import numpy as np

# 3명의 PM이 동일 백로그에 점수 매김
calibration = pd.DataFrame({
    'experiment': ['온보딩 체크리스트', '프리미엄 업셀 배너', '다크 모드',
                   '추천 알고리즘 v2', '결제 페이지 simplify'],
    'pm1_impact': [2, 3, 0.5, 3, 2],
    'pm2_impact': [2, 2, 0.5, 2, 3],
    'pm3_impact': [3, 3, 1, 1, 3],
    'pm1_confidence': [0.8, 0.5, 1.0, 0.5, 0.9],
    'pm2_confidence': [0.7, 0.7, 1.0, 0.4, 0.9],
    'pm3_confidence': [0.9, 0.4, 0.9, 0.7, 0.8],
})

# 각 실험의 Impact 분산 (높을수록 정의 모호)
calibration['impact_std'] = calibration[['pm1_impact', 'pm2_impact',
                                         'pm3_impact']].std(axis=1)
calibration['conf_std'] = calibration[['pm1_confidence', 'pm2_confidence',
                                        'pm3_confidence']].std(axis=1)

# 평균값 vs 분산
calibration['impact_mean'] = calibration[['pm1_impact', 'pm2_impact',
                                          'pm3_impact']].mean(axis=1)
calibration['conf_mean'] = calibration[['pm1_confidence', 'pm2_confidence',
                                         'pm3_confidence']].mean(axis=1)

# 분산 큰 항목 식별
print("=== Calibration 결과 ===")
print(calibration[['experiment', 'impact_mean', 'impact_std',
                    'conf_mean', 'conf_std']].round(2).to_string(index=False))

print("\n=== 재정의 필요 (분산 > 0.5) ===")
needs_recal = calibration[
    (calibration['impact_std'] > 0.5) | (calibration['conf_std'] > 0.15)
]
print(needs_recal[['experiment', 'impact_std', 'conf_std']].to_string(index=False))