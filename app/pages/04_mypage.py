import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 데이터 파일 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DAILY_CHECKS_FILE = DATA_DIR / "daily_checks.json"
WEEKLY_CHECKS_FILE = DATA_DIR / "weekly_checks.json"

def load_daily_data():
    if DAILY_CHECKS_FILE.exists():
        with open(DAILY_CHECKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_weekly_data():
    if WEEKLY_CHECKS_FILE.exists():
        with open(WEEKLY_CHECKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

st.title("👤 마이페이지")

# 기간 선택
period = st.selectbox(
    "분석 기간",
    ["최근 7일", "최근 30일", "최근 90일", "전체 기간"]
)

# 데이터 로드
daily_data = load_daily_data()
weekly_data = load_weekly_data()

if daily_data or weekly_data:
    # 일간 대변 기록 분석
    st.subheader("📊 일간 대변 기록 분석")
    
    if daily_data:
        df_daily = pd.DataFrame(daily_data)
        df_daily['date'] = pd.to_datetime(df_daily['date'])
        
        # 기간에 따른 데이터 필터링
        now = datetime.now()
        if period == "최근 7일":
            df_daily = df_daily[df_daily['date'] > now - timedelta(days=7)]
        elif period == "최근 30일":
            df_daily = df_daily[df_daily['date'] > now - timedelta(days=30)]
        elif period == "최근 90일":
            df_daily = df_daily[df_daily['date'] > now - timedelta(days=90)]
        
        # 브리스톨 척도 분포
        fig_bristol = px.histogram(
            df_daily, 
            x='stool_type',
            title='브리스톨 척도 분포',
            labels={'stool_type': '대변 형태', 'count': '횟수'}
        )
        st.plotly_chart(fig_bristol, use_container_width=True)
        
        # 배변 시간대 분포
        fig_time = px.histogram(
            df_daily,
            x='time',
            title='배변 시간대 분포',
            labels={'time': '시간대', 'count': '횟수'}
        )
        st.plotly_chart(fig_time, use_container_width=True)
        
    else:
        st.info("아직 일간 기록이 없습니다.")
    
    # 주간 체크리스트 분석
    st.subheader("📈 주간 체크리스트 분석")
    
    if weekly_data:
        # 주간 데이터 처리
        weekly_stats = []
        for week in weekly_data:
            stats = {
                'week_start': week['week_start'],
                'total_items': 0,
                'checked_items': 0
            }
            
            for category, items in week['checks'].items():
                stats['total_items'] += len(items)
                stats['checked_items'] += sum(1 for v in items.values() if v)
            
            stats['achievement_rate'] = (stats['checked_items'] / stats['total_items']) * 100
            weekly_stats.append(stats)
        
        df_weekly = pd.DataFrame(weekly_stats)
        df_weekly['week_start'] = pd.to_datetime(df_weekly['week_start'])
        
        # 주간 달성률 그래프
        fig_weekly = px.line(
            df_weekly,
            x='week_start',
            y='achievement_rate',
            title='주간 체크리스트 달성률 추이',
            labels={'week_start': '주차', 'achievement_rate': '달성률 (%)'}
        )
        st.plotly_chart(fig_weekly, use_container_width=True)
        
    else:
        st.info("아직 주간 체크리스트 기록이 없습니다.")
    
    # 전체 통계 요약
    st.subheader("📋 전체 통계 요약")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if daily_data:
            total_records = len(df_daily)
            st.metric("총 기록 수", total_records)
        else:
            st.metric("총 기록 수", 0)
    
    with col2:
        if daily_data:
            avg_bristol = df_daily['stool_type'].mean()
            st.metric("평균 브리스톨 척도", f"{avg_bristol:.1f}")
        else:
            st.metric("평균 브리스톨 척도", "-")
    
    with col3:
        if weekly_data:
            avg_achievement = df_weekly['achievement_rate'].mean()
            st.metric("평균 주간 달성률", f"{avg_achievement:.1f}%")
        else:
            st.metric("평균 주간 달성률", "-")

else:
    st.info("아직 기록된 데이터가 없습니다. 일간 대변 기록과 주간 체크리스트를 작성해주세요.")