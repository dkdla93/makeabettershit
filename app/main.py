import streamlit as st
import json
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="장건강 체크",
    page_icon="🏥",
    layout="wide"
)

# 데이터 디렉토리 설정
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def main():
    st.title("🏥 장건강 체크")
    
    st.markdown("""
    ## 당신의 장건강을 관리해보세요
    
    이 앱은 당신의 장건강을 매일 체크하고 관리하는데 도움을 드립니다.
    
    ### 주요 기능
    1. 📝 일간 대변 기록
        - 브리스톨 척도 기반 기록
        - 시간, 색상, 특이사항 체크
    
    2. 📊 주간 장건강 체크리스트
        - 식습관 체크
        - 생활습관 체크
        - 신체 증상 체크
    
    3. 📚 장건강 정보
        - 최신 정보
        - 중요 정보
        - 기억할 정보
        - 아카이브
        
    4. 👤 마이페이지
        - 기록 분석
        - 저장된 정보 관리
    """)

if __name__ == "__main__":
    main()