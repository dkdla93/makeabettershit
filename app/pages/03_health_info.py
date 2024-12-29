import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 데이터 파일 경로
DATA_DIR = Path(__file__).parent.parent.parent / "data"
HEALTH_INFO_FILE = DATA_DIR / "health_info.json"

# 세션 상태 초기화
if 'show_details' not in st.session_state:
    st.session_state.show_details = {}

def load_data():
    if HEALTH_INFO_FILE.exists():
        with open(HEALTH_INFO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def create_statistics_plots(papers):
    # 연도별 논문 수와 인용 수
    df = pd.DataFrame(papers)
    yearly_stats = df.groupby('year').agg({
        'id': 'count',
        'citations': 'sum'
    }).reset_index()
    yearly_stats.columns = ['year', 'paper_count', 'total_citations']
    
    # 연도별 트렌드 그래프
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=yearly_stats['year'],
        y=yearly_stats['paper_count'],
        name='논문 수',
        line=dict(color='#1f77b4')
    ))
    fig1.add_trace(go.Scatter(
        x=yearly_stats['year'],
        y=yearly_stats['total_citations']/100,  # 스케일 조정
        name='인용 수(✕100)',
        line=dict(color='#ff7f0e')
    ))
    fig1.update_layout(
        title='연도별 논문 및 인용 트렌드',
        xaxis_title='연도',
        yaxis_title='수량',
        hovermode='x unified'
    )
    
    # 상위 인용 논문 차트
    top_cited = df.nlargest(5, 'citations')[['title', 'citations']]
    fig2 = go.Figure(go.Bar(
        x=top_cited['citations'],
        y=top_cited['title'],
        orientation='h'
    ))
    fig2.update_layout(
        title='상위 인용 논문',
        xaxis_title='인용 수',
        yaxis_title='논문 제목',
        height=300
    )
    
    return fig1, fig2

# 타이틀과 기본 레이아웃
st.title("📚 장건강 연구 정보")

# 통계 섹션
papers = load_data()
if papers:
    if st.checkbox("📊 연구 통계 보기"):
        st.subheader("연구 동향 분석")
        
        # 기본 통계
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 논문 수", len(papers))
        with col2:
            total_citations = sum(p['citations'] for p in papers)
            st.metric("총 인용 수", f"{total_citations:,}")
        with col3:
            avg_citations = total_citations / len(papers)
            st.metric("평균 인용 수", f"{avg_citations:.1f}")
        
        # 시각화
        fig1, fig2 = create_statistics_plots(papers)
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

# 논문 목록 표시
for paper in papers:
    paper_id = paper['id']
    if paper_id not in st.session_state.show_details:
        st.session_state.show_details[paper_id] = False
    
    with st.container():
        # 논문 제목과 기본 정보
        st.markdown(f"### {paper['title']} ({paper['year']})")
        
        # 메타 정보
        st.markdown(f"""
        📊 인용: {paper.get('citations', '정보없음')}회  
        👥 저자: {', '.join(paper['authors'])}  
        📰 저널: {paper['journal']}  
        🔍 DOI: `{paper['doi']}`
        """)
        
        # 핵심 내용
        st.markdown("#### 💡 핵심 내용")
        st.markdown(paper['core_content']['summary'])
        
        # 주요 발견
        st.markdown("#### 🎯 주요 발견")
        for finding in paper['core_content']['key_findings']:
            st.markdown(f"- {finding}")
        
        # 토글 버튼
        button_label = "📑 상세 내용 접기" if st.session_state.show_details[paper_id] else "📑 상세 내용 보기"
        if st.button(button_label, key=f"toggle_{paper_id}"):
            st.session_state.show_details[paper_id] = not st.session_state.show_details[paper_id]
        
        # 상세 내용 표시
        if st.session_state.show_details[paper_id]:
            detailed = paper.get('detailed_content', {})
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📋 연구 방법")
                st.markdown(detailed.get('methodology', '정보가 없습니다.'))
                
                st.markdown("##### 📊 연구 결과")
                st.markdown(detailed.get('results', '정보가 없습니다.'))
            
            with col2:
                st.markdown("##### 💭 논의사항")
                st.markdown(detailed.get('discussion', '정보가 없습니다.'))
                
                if 'practical_implications' in detailed:
                    st.markdown("##### 💪 실천 방안")
                    st.markdown(detailed['practical_implications'])
        
        st.markdown("---")

# 사이드바 필터
with st.sidebar:
    st.subheader("🔍 필터")
    search = st.text_input("검색어")
    citations = st.number_input("최소 인용 수", 0)
    year_range = st.slider("발행연도", 2000, 2024, (2000, 2024))
    
    # 통계 요약
    st.markdown("### 📈 요약 통계")
    if papers:
        st.markdown(f"- 검색된 논문: {len(papers)}개")
        st.markdown(f"- 평균 인용 수: {avg_citations:.1f}")
        st.markdown(f"- 최신 논문: {max(p['year'] for p in papers)}년")
    
    st.markdown("### ℹ️ 업데이트 정보")
    st.markdown(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d')}")
    st.markdown("업데이트 주기: 매일 자정")