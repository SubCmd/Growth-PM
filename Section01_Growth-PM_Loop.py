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
