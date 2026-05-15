# 실습 1: Van Westendorp PSM 분석

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 가상의 100명 응답 데이터 (단위: 만원/월)
np.random.seed(42)
n = 100

responses = pd.DataFrame({
    'too_cheap': np.random.normal(0.5, 0.3, n).clip(0.1, 5),
    'cheap': np.random.normal(1.5, 0.5, n).clip(0.5, 8),
    'expensive': np.random.normal(3.5, 1.0, n).clip(1, 15),
    'too_expensive': np.random.normal(5.0, 1.5, n).clip(2, 20),
})

# 가격 grid
price_grid = np.linspace(0, 10, 200)

# 누적 분포 함수 (CDF) 계산
def cdf(values, grid):
    return np.array([np.mean(values <= p) for p in grid])

# 4개 곡선
too_cheap_cdf = 1 - cdf(responses['too_cheap'], price_grid)  # 역방향 (가격 ↑ → 응답 ↓)
cheap_cdf = 1 - cdf(responses['cheap'], price_grid)
expensive_cdf = cdf(responses['expensive'], price_grid)
too_expensive_cdf = cdf(responses['too_expensive'], price_grid)

# 시각화
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(price_grid, too_cheap_cdf * 100, label='Too cheap (싸 보임)',
        color='red', linestyle='--')
ax.plot(price_grid, cheap_cdf * 100, label='Cheap (가성비 좋음)', color='green')
ax.plot(price_grid, expensive_cdf * 100, label='Expensive (비쌈)', color='orange')
ax.plot(price_grid, too_expensive_cdf * 100, label='Too expensive (안 삼)',
        color='red')
ax.set_xlabel('Price (만원/월)'); ax.set_ylabel('% of Respondents')
ax.set_title('Van Westendorp PSM')
ax.legend(); ax.grid(alpha=0.3)

# 4개 핵심 지점 찾기
def intersection(curve1, curve2, grid):
    diff = np.abs(curve1 - curve2)
    return grid[np.argmin(diff)]

opp = intersection(too_cheap_cdf, expensive_cdf, price_grid)  # Optimal price
ipp = intersection(cheap_cdf, expensive_cdf, price_grid)  # Indifference price
pmc = intersection(too_cheap_cdf, cheap_cdf, price_grid)  # Point of marginal cheapness
pme = intersection(expensive_cdf, too_expensive_cdf, price_grid)  # Point of marginal expensiveness

ax.axvline(opp, color='blue', linestyle=':', alpha=0.5)
ax.axvline(ipp, color='purple', linestyle=':', alpha=0.5)
ax.text(opp, 50, f' OPP\n{opp:.1f}만', color='blue')
ax.text(ipp, 60, f' IPP\n{ipp:.1f}만', color='purple')

plt.tight_layout(); plt.show()

print(f"\nOPP (Optimal Price Point): {opp:.2f}만원")
print(f"IPP (Indifference Price Point): {ipp:.2f}만원")
print(f"PMC (수용 하한): {pmc:.2f}만원")
print(f"PME (수용 상한): {pme:.2f}만원")
print(f"\n수용 가능 가격대: {pmc:.1f}만원 ~ {pme:.1f}만원")


# ===============================================================================
# 실습 2: Tier Pricing 시뮬레이션 (Decoy Effect)

# 3-tier 설계 + 각 tier의 전환율 시뮬레이션
def simulate_tier_revenue(n_users=10000, tier_design=None):
    """
    각 tier 디자인이 매출에 미치는 영향 시뮬레이션
    """
    if tier_design is None:
        tier_design = {
            'Free': {'price': 0, 'choice_prob': 0.50},
            'Pro': {'price': 9.9, 'choice_prob': 0.35},
            'Business': {'price': 49, 'choice_prob': 0.15},
        }

    total_revenue = 0
    distribution = {}
    for tier, info in tier_design.items():
        n_in_tier = int(n_users * info['choice_prob'])
        revenue = n_in_tier * info['price']
        total_revenue += revenue
        distribution[tier] = {'users': n_in_tier, 'revenue': revenue}

    return total_revenue, distribution

# 디자인 A: 기본
design_a = {
    'Free': {'price': 0, 'choice_prob': 0.55},
    'Pro': {'price': 9.9, 'choice_prob': 0.35},
    'Business': {'price': 49, 'choice_prob': 0.10},
}

# 디자인 B: Pro tier에 decoy 가까이 (Pro 선호 증가 효과)
design_b = {
    'Free': {'price': 0, 'choice_prob': 0.50},
    'Pro': {'price': 9.9, 'choice_prob': 0.40},
    'Pro Plus': {'price': 12.9, 'choice_prob': 0.10},  # decoy
    'Business': {'price': 49, 'choice_prob': 0.10},  # 4-tier로 결정 마비 위험
}

# 디자인 C: 단순화 (Free + Pro만)
design_c = {
    'Free': {'price': 0, 'choice_prob': 0.65},
    'Pro': {'price': 14.9, 'choice_prob': 0.35},
}

for name, design in [('A: 기본 3tier', design_a), ('B: 4tier (decoy)', design_b),
                       ('C: 2tier 단순화', design_c)]:
    rev, dist = simulate_tier_revenue(10000, design)
    print(f"\n=== Design {name} ===")
    print(f"Total Revenue: {rev:,.0f}만원")
    for tier, info in dist.items():
        print(f"  {tier}: {info['users']}명, 매출 {info['revenue']:,.0f}만원")

'''
=== Design A: 기본 3tier ===
Total Revenue: 83,650만원
  Free: 5500명, 매출 0만원
  Pro: 3500명, 매출 34,650만원
  Business: 1000명, 매출 49,000만원

=== Design B: 4tier (decoy) ===
Total Revenue: 101,500만원
  Free: 5000명, 매출 0만원
  Pro: 4000명, 매출 39,600만원
  Pro Plus: 1000명, 매출 12,900만원
  Business: 1000명, 매출 49,000만원

=== Design C: 2tier 단순화 ===
Total Revenue: 52,150만원
  Free: 6500명, 매출 0만원
  Pro: 3500명, 매출 52,150만원
'''

# ===============================================================================
# 실습 3: Usage-Based Pricing 시뮬레이션

import numpy as np
import pandas as pd

# 사용량 기반 과금: 토큰 100만개당 X만원
def usage_pricing_simulation(users_data, price_per_unit=0.01):
    """
    각 유저의 월간 사용량 기반 매출 계산
    """
    users_data = users_data.copy()
    users_data['monthly_revenue'] = users_data['units_used'] * price_per_unit
    return users_data

# 가상의 1000명 유저 (heavy / medium / light 유저 분포)
np.random.seed(42)
n = 1000
user_types = np.random.choice(['heavy', 'medium', 'light'], n, p=[0.1, 0.3, 0.6])
units = np.where(
    user_types == 'heavy', np.random.gamma(20, 100, n),
    np.where(user_types == 'medium', np.random.gamma(10, 50, n),
             np.random.gamma(2, 20, n))
)

users = pd.DataFrame({
    'user_id': range(n),
    'user_type': user_types,
    'units_used': units.astype(int),
})

# 사용량 분포
print("=== 사용량 분포 ===")
print(users.groupby('user_type')['units_used'].describe()[['count', 'mean', '50%', 'max']])

# 가격 정책 비교
flat_revenue = n * 50  # 모두 5만원/월 (10,000명 × 5만)
pricing = usage_pricing_simulation(users, price_per_unit=0.05)
usage_revenue = pricing['monthly_revenue'].sum()

print(f"\nFlat rate (5만원/월): {flat_revenue:,.0f}만원")
print(f"Usage-based (0.05만원/unit): {usage_revenue:,.0f}만원")

# Heavy 유저가 매출 얼마나 차지?
top10_revenue = pricing.nlargest(int(n*0.1), 'monthly_revenue')['monthly_revenue'].sum()
print(f"\n상위 10% 유저 매출 비중: {top10_revenue/usage_revenue:.1%}")
print("(80/20 법칙 검증: usage-based에선 보통 상위 20%가 80% 매출)")

'''
=== 사용량 분포 ===
           count         mean     50%     max
user_type
heavy      108.0  2033.592593  1953.5  3333.0
light      579.0    40.086356    33.0   192.0
medium     313.0   500.728435   482.0  1386.0

Flat rate (5만원/월): 50,000만원
Usage-based (0.05만원/unit): 19,978만원

상위 10% 유저 매출 비중: 52.4%
(80/20 법칙 검증: usage-based에선 보통 상위 20%가 80% 매출)
'''