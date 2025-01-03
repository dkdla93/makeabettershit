import json
from datetime import datetime
from pathlib import Path

# 데이터 파일 경로
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)  # data 디렉토리가 없으면 생성
HEALTH_INFO_FILE = DATA_DIR / "health_info.json"

# 초기 논문 데이터
INITIAL_PAPERS = [
    {
        "id": "bmj_2016_1",
        "title": "Whole grain consumption and risk of cardiovascular disease, cancer, and all cause and cause specific mortality",
        "authors": ["Dagfinn Aune", "NaNa Keum", "Edward Giovannucci"],
        "journal": "BMJ (British Medical Journal)",
        "year": "2016",
        "citations": 1250,
        "doi": "10.1136/bmj.i2716",
        "core_content": {
            "summary": """
            식이섬유가 풍부한 전곡물 섭취가 장 건강에 미치는 영향에 대한 대규모 메타분석 연구입니다.
            
            주요 발견:
            1. 하루 90g의 전곡물 섭취는 대장암 위험을 17% 감소시킵니다.
            2. 식이섬유 섭취는 장 운동을 활성화하고 배변 규칙성을 향상시킵니다.
            3. 전곡물에 포함된 프리바이오틱스는 유익균 성장을 촉진합니다.
            
            실천 방안:
            - 매일 현미, 귀리, 퀴노아 등 다양한 전곡물을 섭취하세요
            - 하루 최소 3회 이상 전곡물 포함 식사를 하세요
            - 정제된 밀가루 대신 통밀 제품을 선택하세요
            """,
            "key_findings": [
                "전곡물 섭취와 장 건강의 직접적 연관성 입증",
                "식이섬유 섭취량과 배변 규칙성의 양의 상관관계",
                "장내 미생물 다양성 증가 효과"
            ]
        },
        "detailed_content": {
            "methodology": "29개 연구, 총 참여자 수 3.8백만 명 대상 메타분석",
            "results": "상세한 통계 분석 결과와 위험비(Hazard Ratio) 데이터",
            "discussion": "전곡물 섭취의 장기적 건강 영향과 최적 섭취량 제안"
        },
        "tags": ["전곡물", "식이섬유", "장건강"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "id": "gut_2018_1",
        "title": "Role of the gut microbiota in nutrition and health",
        "authors": ["Harry J Flint", "Karen P Scott", "Petra Louis"],
        "journal": "Nature Reviews Gastroenterology & Hepatology",
        "year": "2018",
        "citations": 890,
        "doi": "10.1038/s41575-018-0061-2",
        "core_content": {
            "summary": """
            장내 미생물과 건강한 배변 활동의 관계를 분석한 종합 연구입니다.
            
            핵심 내용:
            1. 장내 미생물 다양성이 높을수록 배변 건강이 향상됩니다.
            2. 프로바이오틱스와 프리바이오틱스의 균형이 중요합니다.
            3. 식단의 다양성이 장내 미생물 생태계에 직접적 영향을 미칩니다.
            
            권장 사항:
            - 발효식품을 규칙적으로 섭취하세요
            - 다양한 채소와 과일을 섭취하여 미생물 다양성을 높이세요
            - 과도한 항생제 사용을 피하세요
            """,
            "key_findings": [
                "장내 미생물 균형과 배변 건강의 상관관계",
                "식이 다양성의 중요성",
                "프로바이오틱스의 효과"
            ]
        },
        "detailed_content": {
            "methodology": "최근 10년간의 장내 미생물 연구 메타분석",
            "results": "미생물 다양성과 건강 지표의 상관관계 분석",
            "discussion": "식단 조절을 통한 장내 미생물 관리 방안"
        },
        "tags": ["장내미생물", "프로바이오틱스", "장건강"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

def update_papers():
    """초기 논문 정보를 저장합니다."""
    with open(HEALTH_INFO_FILE, 'w', encoding='utf-8') as f:
        json.dump(INITIAL_PAPERS, f, ensure_ascii=False, indent=2)
    print(f"Initial papers saved at {datetime.now()}")

if __name__ == "__main__":
    update_papers()
    print("Initial data has been created successfully!")