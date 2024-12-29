import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

# 데이터 파일 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DAILY_CHECKS_FILE = DATA_DIR / "daily_checks.json"

# Bristol Scale 설명
BRISTOL_SCALE = {
    1: "견과류처럼 분리된 단단한 덩어리들 (배변이 어려움)",
    2: "소세지 모양이지만 단단함",
    3: "소세지 같지만 표면에 금이 있음",
    4: "소세지 또는 뱀 같고, 매끄러우며 부드러움",
    5: "윤곽이 뚜렷한 가장자리의 부드러운 방울들 (배변이 쉬움)",
    6: "곡물죽 같은 가장자리의 술렁이는 조각들, 묽은 대변",
    7: "묽은, 단단한 조각이 없음, 전부 액체"
}

def load_data():
    if DAILY_CHECKS_FILE.exists():
        with open(DAILY_CHECKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DAILY_CHECKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.title("📝 일간 대변 기록")

# Bristol Scale 가이드
with st.expander("💡 브리스톨 대변 도표 가이드", expanded=True):
    for type_num, desc in BRISTOL_SCALE.items():
        st.write(f"**Type {type_num}**: {desc}")
    st.write("""
        > 💡 브리스톨 대변 도표는 대변의 형태를 7가지 유형으로 분류하여 
        장 건강 상태를 파악하는데 도움을 줍니다.
    """)

# 기록 폼
with st.form("daily_check_form"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        date = st.date_input(
            "날짜",
            datetime.now(),
            format="YYYY-MM-DD"
        )
        
        stool_type = st.select_slider(
            "대변 형태 (Bristol Scale)",
            options=list(range(1, 8)),
            value=4,
            format_func=lambda x: f"Type {x}"
        )
        st.info(f"선택한 형태 설명: {BRISTOL_SCALE[stool_type]}")
    
    with col2:
        time_options = [
            "새벽 (5~7시)",
            "아침 (7~9시)",
            "점심 (11~13시)",
            "저녁 (17~20시)",
            "밤 늦게 (21시 이후)"
        ]
        time = st.selectbox("배변 시간", time_options)
        
        color_options = [
            "연갈색 (정상)",
            "갈색 (이상적)",
            "짙은 갈색 (건조함)",
            "노란색 (지방성 설사)",
            "녹색 (빠른 장 통과)",
            "검은색 (소화관 출혈 가능)",
            "붉은색 (하부 출혈 가능)"
        ]
        color = st.selectbox("대변 색상", color_options)
    
    notes = st.text_area(
        "특이사항",
        placeholder="배변 시 불편감, 복통, 가스 등 특이사항을 기록해주세요."
    )
    
    submitted = st.form_submit_button("저장하기", 
        use_container_width=True,
        type="primary"
    )
    
    if submitted:
        data = load_data()
        new_record = {
            "date": date.strftime("%Y-%m-%d"),
            "stool_type": stool_type,
            "time": time,
            "color": color,
            "notes": notes,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data.append(new_record)
        save_data(data)
        st.success("기록이 저장되었습니다! 🎉")

# 최근 기록 표시
st.markdown("---")
st.subheader("최근 기록")

data = load_data()
if data:
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # 데이터프레임 보기 좋게 가공
    df_display = df.copy()
    df_display['stool_type'] = df_display['stool_type'].apply(lambda x: f'Type {x}')
    df_display = df_display.sort_values('date', ascending=False)
    
    # 컬럼 이름 한글화
    column_names = {
        'date': '날짜',
        'stool_type': '대변 형태',
        'time': '배변 시간',
        'color': '색상',
        'notes': '특이사항'
    }
    df_display = df_display.rename(columns=column_names)
    
    # 최근 5개 기록만 표시
    st.dataframe(
        df_display[column_names.values()].head(),
        use_container_width=True,
        hide_index=True
    )
    
    # 간단한 통계
    st.markdown("### 통계")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        most_common_type = df['stool_type'].mode().iloc[0]
        st.metric("가장 빈번한 대변 형태", f"Type {most_common_type}")
        
    with col2:
        most_common_time = df['time'].mode().iloc[0]
        st.metric("가장 빈번한 배변 시간", most_common_time)
        
    with col3:
        avg_type = df['stool_type'].mean()
        st.metric("평균 대변 형태", f"Type {avg_type:.1f}")
else:
    st.info("아직 기록된 데이터가 없습니다.")