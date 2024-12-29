import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

# 데이터 파일 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"
WEEKLY_CHECKS_FILE = DATA_DIR / "weekly_checks.json"

def load_data():
    if WEEKLY_CHECKS_FILE.exists():
        with open(WEEKLY_CHECKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(WEEKLY_CHECKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 체크리스트 항목 정의
CHECKLIST_ITEMS = {
    "식습관": [
        "매일 과일과 채소를 충분히 섭취했다 (하루 최소 5가지 종류)",
        "식이섬유가 풍부한 통곡물을 주 3회 이상 섭취했다",
        "하루 물을 8잔 이상 마셨다",
        "발효 식품을 주 3회 이상 섭취했다",
        "패스트푸드나 인스턴트 식품 섭취를 2회 이하로 줄였다",
        "음식을 천천히 씹어 먹었다",
        "과식이나 폭식을 하지 않았다",
        "음주를 피하거나 최소화했다"
    ],
    "생활습관": [
        "규칙적으로 아침, 점심, 저녁 식사를 했다",
        "매일 30분 이상 가벼운 운동을 했다",
        "스트레스 관리를 위한 시간을 가졌다",
        "충분한 수면을 취했다 (7~8시간)",
        "아침에 개운하게 일어났다",
        "전자기기 사용 시간을 줄였다",
        "변비나 설사 증상 개선을 위해 노력했다"
    ],
    "신체 증상": [
        "복부 팽만감이나 가스가 심하지 않았다",
        "복통이나 불편함이 없었다",
        "규칙적인 배변 활동을 했다",
        "소화가 잘 되었다",
        "피부 상태가 좋았다",
        "피로감이 심하지 않았다"
    ]
}

st.title("📊 주간 장건강 체크리스트")

with st.form("weekly_check_form"):
    week_start = st.date_input("체크 시작 날짜", datetime.now())
    
    all_checks = {}
    
    for category, items in CHECKLIST_ITEMS.items():
        st.subheader(f"✅ {category}")
        category_checks = {}
        
        for item in items:
            checked = st.checkbox(item)
            category_checks[item] = checked
        
        all_checks[category] = category_checks
    
    submitted = st.form_submit_button("저장하기")
    
    if submitted:
        data = load_data()
        new_record = {
            "week_start": week_start.strftime("%Y-%m-%d"),
            "checks": all_checks,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(new_record)
        save_data(data)
        st.success("체크리스트가 저장되었습니다! 🎉")

# 최근 기록 및 통계
st.markdown("---")
st.subheader("최근 체크 결과")

data = load_data()
if data:
    latest_check = data[-1]
    st.write(f"**체크 날짜**: {latest_check['week_start']}")
    
    for category, items in latest_check['checks'].items():
        st.write(f"\n**{category}**")
        total = len(items)
        checked = sum(1 for v in items.values() if v)
        progress = checked / total
        st.progress(progress)
        st.write(f"{checked}/{total} 항목 달성 ({progress*100:.0f}%)")
else:
    st.info("아직 체크된 데이터가 없습니다.")