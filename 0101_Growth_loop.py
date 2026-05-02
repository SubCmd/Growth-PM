# 실습 1: Viral Loop 시뮬레이션 (K-factor 영향 분석)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulate_viral_loop(initial_users: int, k_factor: float,
                         cycles: int, retention: float = 0.95) -> list:
    """
    Viral loop 누적 사용자 수 시뮬레이션

    Parameters
    ----------
    initial_users : 초기 유저 수
    k_factor : K = i × c (1 cycle 동안의 viral coefficient)
    cycles : 시뮬레이션 사이클 수 (보통 1 cycle = 1주)
    retention : cycle 간 유지율 (default 0.95)
    """
    cumulative = [initial_users]
    new_in_cycle = [initial_users]

    for _ in range(cycles):
        # 이번 사이클의 신규 유저 = 이전 사이클 유저 × K × retention
        new_users = new_in_cycle[-1] * k_factor * retention
        new_in_cycle.append(new_users)
        cumulative.append(cumulative[-1] + new_users)

    return cumulative

# K값별 12주 시뮬레이션
ks = [0.3, 0.5, 0.8, 1.1, 1.5]
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for k in ks:
    growth = simulate_viral_loop(1000, k, 12)
    axes[0].plot(range(13), growth, marker='o', label=f'K={k}')
    axes[1].plot(range(13), growth, marker='o', label=f'K={k}')

axes[0].set_title('Linear scale - K<1은 감쇠, K>1은 폭발')
axes[0].set_xlabel('Cycle (weeks)'); axes[0].set_ylabel('Cumulative users')
axes[0].legend(); axes[0].grid(alpha=0.3)

axes[1].set_yscale('log')
axes[1].set_title('Log scale - K값 차이가 만드는 격차')
axes[1].set_xlabel('Cycle (weeks)'); axes[1].set_ylabel('Cumulative users (log)')
axes[1].legend(); axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

# 12주차 결과 요약
print("=== 12주차 누적 사용자 수 ===")
for k in ks:
    final = simulate_viral_loop(1000, k, 12)[-1]
    multiplier = final / 1000
    print(f"K={k}: {final:>12,.0f}명  ({multiplier:.1f}x)")


# ===============================================================================
# 실습 2: Paid Acquisition 증폭 효과 계산

def paid_amplification(paid_users: int, k_factor: float) -> dict:
    """
    K < 1일 때, 유료 획득의 총 도달 효과 계산
    Total = Paid / (1 - K)
    """
    if k_factor >= 1:
        return  {"warning:" "K >= 1이면 자생 성장. 유료 획득 효율 측정 의미 약함"}

    total_reach = paid_users / (1 - k_factor)
    organic_lift = total_reach - paid_users
    effective_cac_multiplier = paid_users / total_reach

    return {
        "paid_users": paid_users,
        "k_factor": k_factor,
        "total_reach": round(total_reach),
        "organic_lift": round(organic_lift),
        "amplification": f"{total_reach / paid_users:.2f}x",
        "effective_cac": f"본래 CAC의 {effective_cac_multiplier*100:.0f}%"        
    }

# 광고비 1,000만원으로 100명 획득, K=0.6일 때
result = paid_amplification(paid_users=100, k_factor=0.6)
for k, v in result.items():
    print(f"{k}: {v}")

# 결과
# paid_users: 100
# k_factor: 0.6
# total_reach: 250
# organic_lift: 150
# amplification: 2.50x
# effective_cac: 본래 CAC의 40%


# ===============================================================================
# 실습 3: Loop 단계별 Drop-off 분석 (실무 직결)
# 가상의 Dropbox 스타일 viral loop 이벤트 데이터

import numpy as np
import pandas as pd

# 가상의 Dropbox 스타일 viral loop 이벤트 데이터
np.random.seed(42)
n_users = 10000

events = pd.DataFrame({
    'user_id': range(n_users),
    'signed_up': True,
    'sent_invite': np.random.binomial(1, 0.30, n_users).astype(bool),
    'invite_opened': np.random.binomial(1, 0.50, n_users).astype(bool),
    'invitee_signed_up': np.random.binomial(1, 0.40, n_users).astype(bool),
})

# 종속 관계 적용 (이전 단계 실패 시 이후 단계 불가)
events.loc[~events['sent_invite'], ['invite_opened', 'invitee_signed_up']] = False
events.loc[~events['invite_opened'], 'invitee_signed_up'] = False
# df.loc[조건, 열_이름] = 바꿀 값

# 각 단계 conversion rate 계산
funnel = pd.DataFrame({
    'step': ['signed_up', 'sent_invite', 'invite_opened', 'invitee_signed_up'],
    'count': [events[col].sum() for col in
              ['signed_up', 'sent_invite', 'invite_opened', 'invitee_signed_up']]
})
funnel['conv_from_prev'] = funnel['count'] / funnel['count'].shift(1)
funnel['conv_from_top'] = funnel['count'] / funnel['count'].iloc[0]

print("=== 초기 데이터 통계 ===")
print(events.head().to_string(index=False))
print(events.tail().to_string(index=False))

print("=== Funnel 통계 ===")
print(funnel.to_string(index=False))

# K-factor 계산
i = events['sent_invite'].sum() / len(events)   # 초대 행위 비율 (단순화)
c = events.loc[events['sent_invite'], 'invitee_signed_up'].mean()   # 초대받은 사람의 전환율
k = i * c
print(f"\n현재 K-factor: i={i:.3f} x c={c:.3f} = K={k:.3f}")
print(f"Paid 100명 획득 시 총 도달 : {100/(1-k):.0f}명")



# ===============================================================================
# 연습 문제
# Q1 (기초)
# 당신의 SaaS 제품은 다음과 같습니다.
# - 신규 가입자 1명이 평균 0.4명을 초대 (i = 0.4)
# - 초대받은 사람의 60%가 가입 (c = 0.6)
# - 광고비로 매월 500명을 신규 획득

# 1. 문제 : K-factor를 계산하고, 광고로 획득한 500명이 만들어내는 총 도달 인원을 계산하세요.

i, c = 0.4, 0.6
k = i * c
total = 500 / (1 - k)
print(f"K = {k:.2f}, 총 도달 = {total:.0f}명, 증폭 = {total/500:.2f}x")
# K = 0.24, 총 도달 = 658명, 증폭 = 1.32x


# Q2 (응용)
# 실습 3의 funnel 데이터에서 invite_opened 단계의 conversion rate를 30% → 50%로 올렸을 때의
# 새로운 K-factor를 계산하고, 가장 ROI가 높은 개선 포인트를 추천하세요.

# 각 단계 개선 시 K 변화 시뮬레이션
baseline_i = 0.30  # sent_invite rate
baseline_open = 0.50  # invite_opened rate (조건부)
baseline_signup = 0.40  # invitee_signed_up rate (조건부)

baseline_k = baseline_i * baseline_open * baseline_signup
print(f"Baseline K: {baseline_k:.3f}")

# 각 단계 +10%p 개선 시 K
scenarios = {
    'sent_invite +10%p': (0.40, 0.50, 0.40),
    'invite_opened +10%p': (0.30, 0.60, 0.40),
    'signup +10%p': (0.30, 0.50, 0.50),
}
for name, (i, o, s) in scenarios.items():
    new_k = i * o * s
    lift = (new_k - baseline_k) / baseline_k * 100
    print(f"{name}: K={new_k:.3f} ({lift:+.1f}%)")