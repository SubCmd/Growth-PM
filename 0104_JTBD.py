# 실습 1: 인터뷰 텍스트에서 JTBD 추출 (정규식 + 분류)
import re
import pandas as pd

# 가상의 고객 인터뷰 발언 데이터
interviews = pd.DataFrame({
    'user_id': range(8),
    'quote': [
        "출근길에 차에서 먹을 수 있는 든든한 아침이 필요해요",
        "복잡한 데이터를 한 번에 정리해서 임원에게 보고하고 싶어요",
        "헬스장 가는 사람으로 보이고 싶어서 고급 운동복을 사요",
        "주말에 친구 만날 때 자신감 있어 보이고 싶어요",
        "회의 중에 빠르게 메모해서 나중에 검색할 수 있어야 해요",
        "혼자 카페에서 일할 때 집중력을 높여줄 음악이 필요해요",
        "복잡한 SQL 작성 시간을 줄여서 분석에 시간을 더 쓰고 싶어요",
        "신뢰할 수 있는 사람으로 보여서 협상에서 우위를 점하고 싶어요",
    ]
})

# JTBD 차원 분류용 키워드
functional_keywords = ['시간', '효율', '정리', '검색', '메모', '빠르게', '줄여',
                        '작성', '분석', '데이터']
emotional_keywords = ['집중', '자신감', '편안', '안심', '즐거움', '지루', '스트레스']
social_keywords = ['보이고', '보여', '신뢰', '유능', '인상', '평판', '이미지']

def classify_jtbd(text):
    dims = []
    if any(kw in text for kw in functional_keywords):
        dims.append('Functional')
    if any(kw in text for kw in emotional_keywords):
        dims.append('Emotional')
    if any(kw in text for kw in social_keywords):
        dims.append('Social')
    return ', '.join(dims) if dims else 'Unclassified'

interviews['jtbd_dimentions'] = interviews['quote'].apply(classify_jtbd)
print(interviews[['quote', 'jtbd_dimentions']].to_string(index=False))

# ===============================================================================
# 실습 2: JTBD 문장으로 재구성 (LLM-style 프롬프트로 시뮬레이션)
import re
import pandas as pd

# 가상의 고객 인터뷰 발언 데이터
interviews = pd.DataFrame({
    'user_id': range(8),
    'quote': [
        "출근길에 차에서 먹을 수 있는 든든한 아침이 필요해요",
        "복잡한 데이터를 한 번에 정리해서 임원에게 보고하고 싶어요",
        "헬스장 가는 사람으로 보이고 싶어서 고급 운동복을 사요",
        "주말에 친구 만날 때 자신감 있어 보이고 싶어요",
        "회의 중에 빠르게 메모해서 나중에 검색할 수 있어야 해요",
        "혼자 카페에서 일할 때 집중력을 높여줄 음악이 필요해요",
        "복잡한 SQL 작성 시간을 줄여서 분석에 시간을 더 쓰고 싶어요",
        "신뢰할 수 있는 사람으로 보여서 협상에서 우위를 점하고 싶어요",
    ]
})

# When-I want to-So I can 패턴으로 발언 재구성
def reconstruct_jtbd(quote: str) -> dict:
    """
    실제로는 Claude/GPT API를 호출하지만,
    여시거는 룰 기반으로 시뮬레이션
    """
    # 단순 휴리스틱 예시
    patterns = {
        "출근길에 차에서 먹을": {
            "when": "출근길 차 안에서",
            "want": "한 손으로 먹을 수 있는 든든한 아침을 먹어서",
            "so_can": "지각하지 않으면서 허기를 채운다",
            "dimensions": ["Functional"]
        },
        "복잡한 데이터를 한 번에 정리": {
            "when": "임원 보고 직전",
            "want": "복잡한 데이터를 정리해서",
            "so_can": "유능한 분석가로 인정받는다",
            "dimensions": ["Functional", "Social"]
        },
        "복잡한 SQL 작성 시간을 줄여": {
            "when": "분석 업무 중 SQL 작성 단계에서",
            "want": "쿼리 작성 시간을 줄여서",
            "so_can": "더 가치있는 분석에 시간을 쓴다",
            "dimensions": ["Functional"]
        },
    }
    for pattern, jtbd in patterns.items():
        if pattern in quote:
            return jtbd
    return None

# 실제 적용
for idx, row in interviews.iterrows():
    jtbd = reconstruct_jtbd(row['quote'])
    if jtbd:
        print(f"\nQuote: {row['quote']}")
        print(f"  When:    {jtbd['when']}")
        print(f"  I want:  {jtbd['want']}")
        print(f"  So I can: {jtbd['so_can']}")
        print(f"  차원:    {', '.join(jtbd['dimensions'])}")

'''
Quote: 출근길에 차에서 먹을 수 있는 든든한 아침이 필요해요
  When:    출근길 차 안에서
  I want:  한 손으로 먹을 수 있는 든든한 아침을 먹어서
  So I can: 지각하지 않으면서 허기를 채운다
  차원:    Functional

Quote: 복잡한 데이터를 한 번에 정리해서 임원에게 보고하고 싶어요
  When:    임원 보고 직전
  I want:  복잡한 데이터를 정리해서
  So I can: 유능한 분석가로 인정받는다
  차원:    Functional, Social

Quote: 복잡한 SQL 작성 시간을 줄여서 분석에 시간을 더 쓰고 싶어요
  When:    분석 업무 중 SQL 작성 단계에서
  I want:  쿼리 작성 시간을 줄여서
  So I can: 더 가치있는 분석에 시간을 쓴다
  차원:    Functional
'''

# ===============================================================================
# 실습 3: JTBD-기능 매핑 매트릭스
import pandas as pd

# 식별된 JTBD를 제품 기능과 매핑하여 gap 발견
jtbd_features = pd.DataFrame({
    'jtbd': [
        '쿼리 작성 시간 줄이기',
        '데이터 신뢰성 검증',
        '분석 결과 임원 보고용 정리',
        '동료와 분석 결과 공유',
        '과거 분석 재활용',
    ],
    'frequency': [85, 60, 50, 40, 35],  # 인터뷰에서 언급 빈도
    'current_solution_satisfaction': [3, 5, 4, 6, 2],  # 1~10
    'has_feature': [True, True, False, True, False]
})

# Opportunity Score = Importance + max(Importance - Satisfaction, 0)
# (Tony Ulwick formula)
jtbd_features['importance'] = jtbd_features['frequency'] / 10  # 1~10 scale
jtbd_features['opportunity_score'] = (
    jtbd_features['importance'] +
    (jtbd_features['importance'] - jtbd_features['current_solution_satisfaction']).clip(lower=0)
)

# 우선순위 정렬
print(jtbd_features.sort_values('opportunity_score', ascending=False))

# 시각화: 4사분면 (Importance vs Satisfaction)
fig, ax = plt.subplots(figsize=(10, 6))
for _, row in jtbd_features.iterrows():
    color = 'red' if row['opportunity_score'] > 12 else 'gray'
    ax.scatter(row['importance'], row['current_solution_satisfaction'],
               s=row['frequency']*5, alpha=0.6, color=color)
    ax.annotate(row['jtbd'], (row['importance'], row['current_solution_satisfaction']),
                fontsize=9)

ax.axhline(5, color='k', linewidth=0.5); ax.axvline(5, color='k', linewidth=0.5)
ax.set_xlabel('Importance'); ax.set_ylabel('Current Satisfaction')
ax.set_title('JTBD Opportunity Map (빨강 = 기회 큼)')
ax.grid(alpha=0.3); plt.tight_layout(); plt.show()

# ===============================================================================
# 연습문제
# Q1 (기초)
# 다음 발언을 JTBD 문장 구조(When-I want-So I can)로 재구성하세요.
# "주말에 카페에서 책 읽고 싶은데, 자리 잡기 힘들어서 미리 알 수 있으면 좋겠어요."

# When : 주말 카페에서 책 읽으러 갈 때,
# I want : 미리 자리를 잡을 수 있는지
# So I can : 헛걸음 없이 독서 시간을 확보
# Dimensions : Functional(시간 절약) + Emotional(헛걸음 스트레스 회피)


# Q3 (실무 연결)
# 내가 추진하고자 하는 화장품 D2C 사업 (LATAM 타겟) 시장 조사 데이터에서 다음 인터뷰 발언
'''
"한국 화장품은 효과가 좋다고 듣지만,
영어 후기가 부족하고 가격대도 너무 다양해서 뭘 사야 할지 모르겠어요.
친구한테 추천 받은 브랜드만 계속 사요."
'''
# 이 발언에서 JTBD 3개 차원을 모두 식별하고, 각각 어떤 제품 기능으로 대응할 수 있는지 매칭하세요.

# 식별된 JTBD
# Functional : 영어 후기, 가격 비교로 의사결정 / 다국어 리뷰 + AI 추천 엔진 + 가격대별 필터
# Emotional : "잘못 살까봐" 두려움 회피 / 만족 보장 환불 + before/after 시각화
# Social : 친구 추천처험 "내 사람의 검증" / UGC(사용자 생성 콘텐츠) + 로컬 인플루언서 협업 + 리퍼럴
# 핵심 포인트 : "가격이 다양한건" 표면적 문제 // 진짜 문제는 불확실성 회피 -> 가격조정보다 신뢰성 제공이 필요함.