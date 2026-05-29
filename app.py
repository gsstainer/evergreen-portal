import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ---------------------------------------------------------
# Page Configuration & Styling (Bio-Slate 10yr UX System)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Evergreen LIMS & Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Bio-Slate CSS Styling (High Contrast Inter Font, Responsive Tables)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* GNB & Core App Styling with Strict Contrast */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0f19;
        color: #f1f5f9; /* High-contrast white text */
    }
    .main {
        background-color: #0b0f19;
    }
    
    /* Typography Scannability Contrast */
    h1 {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #f8fafc;
        margin-bottom: 8px;
    }
    h2 {
        font-size: 24px;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #f8fafc;
        border-left: 5px solid #14b8a6; /* Radiant Teal border */
        padding-left: 14px;
        margin-top: 28px;
        margin-bottom: 18px;
    }
    h3 {
        font-size: 18px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 12px;
    }
    
    /* Breadcrumb Component */
    .breadcrumb {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 24px;
        font-weight: 500;
    }
    .breadcrumb-active {
        color: #14b8a6;
        font-weight: 700;
    }
    
    /* Metric & Card Wrapper Components with Enhanced Text Contrast */
    .card-wrapper {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    
    /* Extreme metric value contrast adjustment */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 800;
        color: #2dd4bf !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    div[data-testid="stMetricLabel"] {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* GNB Banner component with Teal-Emerald Accent */
    .gnb-banner {
        background: linear-gradient(90deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid #334155;
        border-left: 6px solid #0d9488;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 28px;
    }
    .gnb-banner p {
        color: #cbd5e1;
        margin: 6px 0 0 0;
        font-size: 15px;
    }

    /* Highly Readable LIMS Fixed-Header Responsive Tables */
    .fixed-header-table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 15px;
        text-align: left;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .fixed-header-table th {
        background-color: #1e293b;
        color: #f8fafc;
        font-weight: 700;
        padding: 14px 16px;
        border-bottom: 3px solid #0f172a;
        letter-spacing: 0.5px;
    }
    .fixed-header-table td {
        padding: 14px 16px;
        border-bottom: 1px solid #334155;
        color: #f1f5f9;
        line-height: 1.5;
    }
    .fixed-header-table tr {
        background-color: #0f172a;
    }
    .fixed-header-table tr:hover {
        background-color: #155e75;
        transition: background-color 0.15s ease-in-out;
    }
    
    /* Custom Interactive Tooltips */
    .custom-tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 2px dashed #14b8a6;
        color: #14b8a6 !important;
        font-weight: 700;
        cursor: help;
    }
    .custom-tooltip .tooltip-box {
        visibility: hidden;
        width: 320px;
        background-color: #1e293b;
        color: #f8fafc;
        text-align: left;
        border: 2px solid #0d9488;
        border-radius: 8px;
        padding: 14px;
        position: absolute;
        z-index: 9999;
        bottom: 130%;
        left: 50%;
        margin-left: -160px;
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
        font-size: 13px;
        font-weight: 400;
        line-height: 1.5;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.7);
    }
    .custom-tooltip:hover .tooltip-box {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Helper Functions (State Badges & Custom Tooltips)
# ---------------------------------------------------------
def render_badge(status):
    """Generates premium pastel-toned badges representing lab status. (All set to 대기 for Year 1 pre-start)"""
    if status == "완료":
        bg_col, txt_col = "#064e3b", "#a7f3d0"
    elif status == "진행중":
        bg_col, txt_col = "#1e3a8a", "#bfdbfe"
    elif status == "대기":
        bg_col, txt_col = "#1e293b", "#f1f5f9"  # High-contrast slate blue with off-white text
    else:
        bg_col, txt_col = "#7f1d1d", "#fecdd3"
    
    if status == "대기":
        return f'<span style="background-color: {bg_col}; color: {txt_col}; padding: 5px 14px; border-radius: 20px; font-weight: 800; font-size: 12px; border: 1px solid #475569; letter-spacing: 0.5px;">{status}</span>'
    return f'<span style="background-color: {bg_col}; color: {txt_col}; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 12px; border: 1px solid {txt_col}40;">{status}</span>'

def get_epic_badge(epic_id):
    """Generates a highly-stylized visual badge for subtasks based on Epic ID (EP-EG1, EP-EG2, EP-EG3)"""
    if "EP-EG1" in epic_id:
        bg, fg = "#0b253a", "#38bdf8"  # Slate Blue-Cyan contrast
    elif "EP-EG2" in epic_id:
        bg, fg = "#3b122d", "#f472b6"  # Deep Plum-Pink contrast
    elif "EP-EG3" in epic_id:
        bg, fg = "#062f22", "#34d399"  # Emerald Green contrast
    else:
        bg, fg = "#1e293b", "#cbd5e1"
    return f'<span style="background-color: {bg}; color: {fg}; padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 12px; border: 1px solid {fg}40; font-family: monospace; letter-spacing: 0.5px;">{epic_id}</span>'

def tooltip(term, definition):
    """Generates an embedded custom tooltip anchor."""
    return f'<span class="custom-tooltip">{term}<span class="tooltip-box">{definition}</span></span>'

dict_tooltip = {
    "mOS": "<b>mOS (median Overall Survival)</b>: 환자군의 50%가 생존하는 시점으로 항암 약물 효능 평가의 최종 표준 마커.",
    "TME": "<b>TME (Tumor Microenvironment)</b>: 종양을 둘러싼 복잡한 기질, 혈관, 면역세포 환경으로 ALK7 억제제 및 면역 항암제의 핵심 작용처.",
    "4-HNE": "<b>4-HNE (4-Hydroxynonenal)</b>: 지질 과산화의 최종 산물로 세포 독성을 유발하고 T세포의 노화(Immunosenescence)를 가속화하는 독성 매개자.",
    "H3K27ac": "<b>H3K27ac</b>: Histone 3 Lysine 27 아세틸화 마커. 활발한 후성유전학적 전사 복원을 상징하는 젊음 회복 유전자 지표.",
    "H3K27me3": "<b>H3K27me3</b>: 유전자 발현을 억제하는 크로마틴 후성유전학적 '잠금 장치' 마커.",
    "ALK7": "<b>ALK7 (ACVR1C)</b>: 소화기암(췌장암, 간암)의 전이 및 기질 축적, 체중 감소(악액질)를 활성화하는 TGF-β 패밀리 수용체.",
    "SARM1": "<b>SARM1</b>: 안구 신경 장벽 극복 및 녹내장 신경 손상 시 NAD⁺ 고갈을 유도하여 Axon(축삭) 사멸을 활성화하는 인자.",
    "dLck-cre": "<b>dLck-cre</b>: Distal Lck 프로모터를 활용하여 흉선 발달 간섭을 전면 차단하고 말초 T세포의 순수 연령 노화만을 분리 분석하는 최첨단 마우스 모델.",
    "TSA/DSF": "<b>TSA/DSF (Thermal Shift Assay)</b>: 화합물이 표적 단백질에 결합 시 열 변성 온도(Melting Temp, dTm)를 상승시키는 원리를 이용한 물리적 결합 검증법."
}

# ---------------------------------------------------------
# Static Fail-Safe Built-in Pipeline Data
# ---------------------------------------------------------
BUILTIN_PIPELINES = {
    "Y0_5yr_Summary": [
        {"Epic ID": "EP-EG1", "Epic (Project)": "노화 대식세포 표적 황반변성 치료제 개발 (이욱빈 팀)", "Year 1 (1차)": "AI 후보 도출 / In vitro 모델 / 전달체 기초 / In vivo SOP", "Year 2 (2차)": "Hit 검증 / Lead 확정 / MoA / 전달체 최적화", "Year 3 (3차)": "ML 2차 / KRIBB 오가노이드 PoC / 하이브리드 전달체", "Year 4 (4차)": "유도체 재검증 / Scale-up / PK/PD·비GLP 독성", "Year 5 (5차)": "AIDD SOP / CMC 완결 / NOAEL 확보 / 휴온스바이오파마 기술이전"},
        {"Epic ID": "EP-EG2", "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어 (김명석 팀)", "Year 1 (1차)": "오믹스 아형 정의 / VS 5단계 / ALK7 도메인별 In silico", "Year 2 (2차)": "LPHNP 설계 / Smart Release / 3D Chip / 예비 In vivo", "Year 3 (3차)": "Hit-to-lead / ADME·Tox / 장-근육-면역 축 / BM Chimera", "Year 4 (4차)": "FOLFIRINOX 병용 / 간암 전이 봉쇄 / cGAS-STING 면역 재설계", "Year 5 (5차)": "GLP 독성 완료 / CMC eCTD 규격화 / CDx 플랫폼 상용화 / 글로벌 기술이전"},
        {"Epic ID": "EP-EG3", "Epic (Project)": "면역노화 진단 바이오마커 개발 Ets1 (이충구 팀)", "Year 1 (1차)": "Ets1 저하 T세포 노화 프로파일링 / AI 통합 라이브러리 가상 스크리닝", "Year 2 (2차)": "dLck-cre 마우스 모델 분석 / 자연 vs D-gal 노화 교차 검증 / In vitro Hit 검증", "Year 3 (3차)": "ATAC-seq + ChIP-seq / In vitro T세포 후성유전 리프로그래밍", "Year 4 (4차)": "In vivo 면역 감시 능력 회복 / SCENIC Tex->Tpex 복원 약효 실증 / 동반 질환 개선", "Year 5 (5차)": "ML 경구 BA 예측 / 기초 독성 및 Druggability 검증 / 특허 청구항 설계 및 IP 장벽 구축"}
    ],
    "Y1_1차년도": [
        {"Epic ID": "EP-EG1", "Epic (Project)": "노화 대식세포 표적 황반변성 치료제", "Milestone (Phase)": "M1. AI/구조 기반 안질환 표적 분석 및 1차 후보물질 우선순위화", "Task — Specific Experiments (Bullet Points)": "• KIST 천연물 라이브러리 큐레이션 (자생 1,160 / 생약 372 / 버섯 118)\n• NPI Finder + Agentic AI 연동: TAM axis 및 SARM1 3D 포켓 적합성 분석", "담당 PI 연구팀": "이욱빈, 최용수", "Timeline": "Y1-Q1~Q2"},
        {"Epic ID": "EP-EG1", "Epic (Project)": "노화 대식세포 표적 황반변성 치료제", "Milestone (Phase)": "M2. In vitro 세포 수준 병리기전 및 다중 타겟 평가 모델 구축", "Task — Specific Experiments (Bullet Points)": "• [황반변성] ARPE-19 + Doxorubicin -> SA-β-gal·노화표지 모델\n• Senolysis + Efferocytosis 통합 어세이 확립", "담당 PI 연구팀": "최용수, 강석우", "Timeline": "Y1-Q2~Q3"},
        {"Epic ID": "EP-EG2", "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어", "Milestone (Phase)": "M1. 다기원 오믹스 기반 종양 아형 정의 및 타깃 확정", "Task — Specific Experiments (Bullet Points)": "• TCGA + GTEx + GEO 데이터셋 분석을 통한 ALK7 핵심 타겟 확정\n• 간암 Hoshida S1-3 및 췌장암 Classical·Basal 분류 상관성 규명", "담당 PI 연구팀": "김명석, 김원규", "Timeline": "Y1-Q1~Q2"},
        {"Epic ID": "EP-EG2", "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어", "Milestone (Phase)": "M2. AI 기반 가상 스크리닝 5단계 파이프라인 가동", "Task — Specific Experiments (Bullet Points)": "• NPI Finder 23,000종 + FDA 약물 대상 ALK7 알로스테릭 cavity 도킹 시뮬레이션\n• ΔG < -8.5 및 ΔΔG < -1.5 kcal/mol 필터링 기준 true hits 도출", "담당 PI 연구팀": "김명석", "Timeline": "Y1-Q2~Q3"},
        {"Epic ID": "EP-EG3", "Epic (Project)": "면역노화 진단 바이오마커 개발 (Ets1)", "Milestone (Phase)": "M1. Ets1 저하 T세포 노화/고갈 표현형 프로파일링", "Task — Specific Experiments (Bullet Points)": "• Ets1 결핍 시 CD127(생존 항상성) 급감 분석 및 면역관문(PD-1, TIGIT) 축적 분석\n• Th17 편향 비가역적 면역노화 임계 지점 정의", "담당 PI 연구팀": "이충구", "Timeline": "Y1-Q1~Q2"}
    ]
}

# ---------------------------------------------------------
# Data Loading and Caching (MUST BE DEFINED BEFORE CALLING)
# ---------------------------------------------------------
EXCEL_PATH = r"g:\내 드라이브\KIST\공동연구\Sarcopenia_김명석\01_Grants_and_Proposals\2026\NST_에버그린\에버그린_프로젝트_연차별_연구내용_정리.xlsx"

@st.cache_data
def load_excel_data():
    sheets = {}
    if os.path.exists(EXCEL_PATH):
        try:
            xl = pd.ExcelFile(EXCEL_PATH)
            for sheet in xl.sheet_names:
                df = pd.read_excel(EXCEL_PATH, sheet_name=sheet)
                df = df.dropna(how='all').fillna("")
                sheets[sheet] = df
        except Exception as e:
            st.error(f"Error reading Excel: {str(e)}")
    return sheets

# --- CRITICAL FIX: Safe execution call after function definition ---
excel_data = load_excel_data()
if not excel_data:
    excel_data = {}
    for sheet_name, rows in BUILTIN_PIPELINES.items():
        excel_data[sheet_name] = pd.DataFrame(rows)

# ---------------------------------------------------------
# [1. Navigation GNB Sidebar - 3-Click Rule]
# ---------------------------------------------------------
menu_selection = st.sidebar.radio(
    "전역 내비게이션 바 (GNB)",
    [
        "📊 대시보드 총괄 (Summary Dashboard)",
        "🧬 세부과제별 파이프라인 (Pipelines)",
        "🧪 물질 라이브러리 (LIMS Explorer)",
        "📅 랩 미팅 & 블로커 (Lab Sync)",
        "📈 행정 매트릭스 (Admin Metrics)"
    ]
)

st.sidebar.markdown("---")

# ---------------------------------------------------------
# 🏠 Dynamic Breadcrumbs Setup
# ---------------------------------------------------------
breadcrumb_base = "🏠 홈 > "
if "대시보드 총괄" in menu_selection:
    st.markdown(f'<div class="breadcrumb">{breadcrumb_base}<span class="breadcrumb-active">📊 대시보드 총괄</span></div>', unsafe_allow_html=True)
elif "세부과제별 파이프라인" in menu_selection:
    st.markdown(f'<div class="breadcrumb">{breadcrumb_base}🧬 파이프라인 > <span class="breadcrumb-active">세부과제별 마일스톤</span></div>', unsafe_allow_html=True)
elif "물질 라이브러리" in menu_selection:
    st.markdown(f'<div class="breadcrumb">{breadcrumb_base}🧪 물질 라이브러리 > <span class="breadcrumb-active">Wet-Dry 통합 탐색기</span></div>', unsafe_allow_html=True)
elif "랩 미팅 & 블로커" in menu_selection:
    st.markdown(f'<div class="breadcrumb">{breadcrumb_base}📅 랩 미팅 > <span class="breadcrumb-active">병목(Blocker) 트래커</span></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="breadcrumb">{breadcrumb_base}📈 행정 > <span class="breadcrumb-active">예산 및 특허 지표</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 📊 [MENU 1] 대시보드 총괄 (Summary Dashboard)
# ---------------------------------------------------------
if "대시보드 총괄" in menu_selection:
    st.markdown("<h1>📊 에버그린 국가전략사업 총괄 대시보드</h1>", unsafe_allow_html=True)
    st.markdown(f"3대 핵심 Exit Points(EP)의 비임상, 특허 및 기술이전 진척률을 통합 모니터링하는 LIMS 관제 대시보드입니다. ({tooltip('mOS', dict_tooltip['mOS'])}, {tooltip('TME', dict_tooltip['TME'])}, {tooltip('4-HNE', dict_tooltip['4-HNE'])} 등 주요 바이오 마커에 호버 시 상세 가이드가 팝업됩니다.)", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_ep1, col_ep2, col_ep3 = st.columns(3)
    with col_ep1:
        st.markdown(r"""
        <div class="card-wrapper">
            <h3>👁️ EP-EG1: 황반변성 치료제 개발</h3>
            <p style='color: #cbd5e1; font-size: 14px;'>주관: 이욱빈 박사팀</p>
            <div style='font-size: 26px; font-weight: 800; color: #2dd4bf; margin: 10px 0;'>대기상태 (0% / 1차년도)</div>
            <p style='color: #cbd5e1; font-size: 13px; line-height:1.5;'>• 5년차 EP: 28일 독성 수립 및 휴온스바이오파마 권리 이전<br>• 핵심 타겟: SARM1, TAM axis<br>• 현황: 올해 8월 연구 개시 준비 단계</p>
        </div>
        """, unsafe_allow_html=True)
    with col_ep2:
        st.markdown(r"""
        <div class="card-wrapper">
            <h3>🧬 EP-EG2: 소화기암 전이/악액질 극복</h3>
            <p style='color: #cbd5e1; font-size: 14px;'>주관: 김명석 박사팀</p>
            <div style='font-size: 26px; font-weight: 800; color: #2dd4bf; margin: 10px 0;'>대기상태 (0% / 1차년도)</div>
            <p style='color: #cbd5e1; font-size: 13px; line-height:1.5;'>• 5년차 EP: GLP 독성 완료 및 글로벌 L/O 데이터룸 발간<br>• 핵심 타겟: ALK7 도메인 이원화<br>• 현황: 중앙 라이브러리 및 3D 칩 설계 설계 대기</p>
        </div>
        """, unsafe_allow_html=True)
    with col_ep3:
        st.markdown(r"""
        <div class="card-wrapper">
            <h3>🩸 EP-EG3: 면역노화 진단 바이오마커</h3>
            <p style='color: #cbd5e1; font-size: 14px;'>주관: 이충구 박사팀</p>
            <div style='font-size: 26px; font-weight: 800; color: #2dd4bf; margin: 10px 0;'>대기상태 (0% / 1차년도)</div>
            <p style='color: #cbd5e1; font-size: 13px; line-height:1.5;'>• 5년차 EP: ML 경구 BA 예측 및 특허 청구항 강력 IP 장벽<br>• 핵심 타겟: Ets1, dLck-cre<br>• 현황: dLck-cre 모델 수립 및 ATAC 프로토콜 설계 대기</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(r"""
    <div style="background-color: #1e1b4b; border-left: 6px solid #2dd4bf; padding: 18px; border-radius: 8px; margin-top: 15px; margin-bottom: 25px;">
        <span style="color: #f8fafc; font-weight: 800; font-size: 16px;">📢 에버그린 프로젝트 1차년도 개시 일정 안내</span>
        <p style="color: #cbd5e1; margin: 6px 0 0 0; font-size: 14px; line-height: 1.5;">본 프로젝트는 <b>올해 8월 1일 자로 공식 개시</b>될 예정이며, 현재는 1차년도 연구 개시를 위한 In Silico 사전 데이터 클리닝 및 라이브러리 입고 준비 단계입니다. 이에 따라 모든 마일스톤과 과제 진척도는 <b>'대기'</b> 상태로 표시되어 안전하게 트래킹되고 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📈 5개년 연차별 마일스톤 온트랙(On-Track) 목표 비중")
    chart_data = pd.DataFrame({
        "연차": ["1차년도", "2차년도", "3차년도", "4차년도", "5차년도"] * 3,
        "과제": ["EP-EG1 (황반변성)"]*5 + ["EP-EG2 (소화기암)"]*5 + ["EP-EG3 (면역노화)"]*5,
        "목표 진척도 (%)": [20, 45, 70, 90, 100, 20, 50, 75, 92, 100, 15, 40, 65, 85, 100]
    })
    fig_line = px.line(chart_data, x="연차", y="목표 진척도 (%)", color="과제", markers=True, color_discrete_sequence=["#06b6d4", "#ec4899", "#10b981"])
    fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0", xaxis=dict(showgrid=True, gridcolor="#334155"), yaxis=dict(showgrid=True, gridcolor="#334155"))
    st.plotly_chart(fig_line, use_container_width=True)

# ---------------------------------------------------------
# 🧬 [MENU 2] 세부과제별 파이프라인 (Pipelines)
# ---------------------------------------------------------
elif "세부과제별 파이프라인" in menu_selection:
    st.markdown("<h1>🧬 세부과제별 마일스톤 및 실험 파이프라인</h1>", unsafe_allow_html=True)
    st.markdown(f"국가전략과제계획서에서 추출된 연차별 마일스톤 테이블입니다. 8월 과제 시작에 맞춰 모든 세부 실험 태스크는 <b>'대기'</b> 상태로 안전하게 셋업되었습니다. ({tooltip('TSA/DSF', dict_tooltip['TSA/DSF'])}, {tooltip('dLck-cre', dict_tooltip['dLck-cre'])}) 등 전문 용어에 호버하시면 측정 근거 주석이 팝업됩니다.", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    search_q = st.text_input("🔍 마일스톤 및 태스크 키워드 검색 (예: ALK7, 오가노이드, Ets1, SARM1 등)", "")
    
    rows = []
    for s_name, df in excel_data.items():
        if s_name == "Y0_5yr_Summary":
            continue
        for idx, r in df.iterrows():
            task_text = r.get("Task — Specific Experiments (Bullet Points)", "") or r.get("Unnamed: 3", "")
            if not task_text or "Task" in str(task_text) or "Data Source" in str(task_text):
                continue
                
            # Clean up the Year string display (e.g. Y1_1차년도 -> 1차년도 (Year 1))
            parts = s_name.replace("Y", "").split("_")
            y_display = f"{parts[1]} (Year {parts[0]})" if len(parts) >= 2 else s_name.replace("Y", "Year ").replace("_", " ")
            
            # Format raw specific task bullets to clean styling and auto-link custom biotech tooltips
            task_html = ""
            for item in str(task_text).split("\n"):
                item = item.strip()
                if not item:
                    continue
                if item.startswith("•"):
                    clean_item = item.replace("•", "").strip()
                    # Auto-inject hover tooltips for biotech terminology
                    for term, definition in dict_tooltip.items():
                        if term in clean_item:
                            clean_item = clean_item.replace(term, tooltip(term, definition))
                    task_html += f"<div style='margin-bottom: 8px; padding-left: 10px; border-left: 2px solid #2dd4bf; line-height: 1.6;'>• {clean_item}</div>"
                else:
                    for term, definition in dict_tooltip.items():
                        if term in item:
                            item = item.replace(term, tooltip(term, definition))
                    task_html += f"<div style='margin-bottom: 8px; line-height: 1.6;'>{item}</div>"
            
            # Auto-inject hover tooltips for Milestone phase too
            milestone_text = r.get("Milestone (Phase)", "") or r.get("Unnamed: 2", "")
            for term, definition in dict_tooltip.items():
                if term in milestone_text:
                    milestone_text = milestone_text.replace(term, tooltip(term, definition))

            row_data = {
                "연차": y_display,
                "Epic ID": r.get("Epic ID", "") or r.get("에버그린 프로젝트 1차년도 (Year 1) — Epic → Milestone → Task", ""),
                "Milestone": milestone_text,
                "세부 실험 Task": task_html,
                "일정": r.get("Timeline", "") or r.get("Unnamed: 5", ""),
                "상태": "대기"
            }
            
            if search_q:
                # Include task text search
                row_str = " ".join([str(v) for v in [row_data["연차"], row_data["Epic ID"], row_data["Milestone"], task_text, row_data["일정"]]]).lower()
                if search_q.lower() in row_str:
                    rows.append(row_data)
            else:
                rows.append(row_data)

    if rows:
        st.subheader(f"📊 공식 실험 파이프라인 (총 {len(rows)}개 태스크 조회됨)")
        table_html = """
        <table class="fixed-header-table">
            <thead>
                <tr>
                    <th style="width: 12%;">연차</th>
                    <th style="width: 12%;">과제 ID</th>
                    <th style="width: 23%;">마일스톤 (Phase)</th>
                    <th style="width: 38%;">세부 실험 Task (Specific Experiments)</th>
                    <th style="width: 10%;">일정</th>
                    <th style="width: 5%;">상태</th>
                </tr>
            </thead>
            <tbody>
        """
        for r_data in rows:
            table_html += f"""
                <tr>
                    <td><b style="color: #f8fafc; font-size: 14px;">{r_data['연차']}</b></td>
                    <td>{get_epic_badge(r_data['Epic ID'])}</td>
                    <td><b style="color: #e2e8f0; font-size: 14px;">{r_data['Milestone']}</b></td>
                    <td style="color: #cbd5e1; font-size: 13.5px; padding: 12px 16px;">{r_data['세부 실험 Task']}</td>
                    <td><code style="background-color: #1e293b; color: #38bdf8; padding: 4px 8px; border-radius: 4px; border: 1px solid #334155; font-weight: 600;">{r_data['일정']}</code></td>
                    <td>{render_badge(r_data['상태'])}</td>
                </tr>
            """
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.info("검색 조건에 부합하는 파이프라인 태스크가 없습니다.")

    with st.expander("📂 원본 데이터 엑셀 시트 뷰어"):
        if excel_data:
            sub_tabs = st.tabs(list(excel_data.keys()))
            for idx, (s_name, df) in enumerate(excel_data.items()):
                with sub_tabs[idx]:
                    st.dataframe(df, use_container_width=True)

# ---------------------------------------------------------
# 🧪 [MENU 3] 물질 라이브러리 (LIMS Explorer)
# ---------------------------------------------------------
elif "물질 라이브러리" in menu_selection:
    st.markdown("<h1>🧪 Wet-Dry 통합 물질 라이브러리 Explorer</h1>", unsafe_allow_html=True)
    st.markdown(f"Selleckchem L3800 및 미생물 대사산물 23,000종 중 선별된 {tooltip('ALK7', dict_tooltip['ALK7'])}, TAM, SARM1, Ets1 표적 라이브러리의 Wet-Dry 통합 데이터 매퍼입니다. 과제 시작 전이므로 모든 물질 검증 상태는 <b>'대기'</b>로 연동됩니다.", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        f_epic = st.selectbox("Epic 과제 필터", ["All", "EP-EG1 (황반변성)", "EP-EG2 (소화기암)", "EP-EG3 (면역노화)"])
    with col_f2:
        f_type = st.selectbox("화합물 모달리티", ["All", "Kinase Domain (저분자)", "ECD Domain (중분자 펩타이드)", "Natural Product (천연물/미생물)"])
    with col_f3:
        min_eff_val = st.slider("최소 약효 활성도 (Efficacy) [%]", 0, 100, 0, step=5)

    np.random.seed(42)
    substances = []
    
    substances.append({"Substance ID": "EVG-EG1-001", "Name": "Auraptene Derivative", "Type": "Natural Product (천연물/미생물)", "Epic ID": "EP-EG1 (황반변성)", "Target": "MerTK / SARM1", "ΔG": -9.2, "ΔΔG": -2.1, "TSA dTm": 4.5, "Efficacy": 78.0, "Tox": 82.0, "True Lead": True, "Status": "대기"})
    substances.append({"Substance ID": "EVG-EG2-001", "Name": "Micheliolide", "Type": "Natural Product (천연물/미생물)", "Epic ID": "EP-EG2 (소화기암)", "Target": "ALK7 Kinase domain", "ΔG": -8.7, "ΔΔG": -1.8, "TSA dTm": 3.8, "Efficacy": 68.0, "Tox": 71.0, "True Lead": True, "Status": "대기"})
    substances.append({"Substance ID": "EVG-EG2-002", "Name": "ALK7 Extracellular Peptide", "Type": "ECD Domain (중분자 펩타이드)", "Epic ID": "EP-EG2 (소화기암)", "Target": "ALK7 ECD domain", "ΔG": -8.9, "ΔΔG": -1.6, "TSA dTm": 2.8, "Efficacy": 72.0, "Tox": 69.0, "True Lead": True, "Status": "대기"})
    substances.append({"Substance ID": "EVG-EG3-001", "Name": "Ets1 Stabilizing Compound", "Type": "Kinase Domain (저분자)", "Epic ID": "EP-EG3 (면역노화)", "Target": "Ets1 chromatin complex", "ΔG": -9.0, "ΔΔG": -2.0, "TSA dTm": 4.1, "Efficacy": 75.0, "Tox": 80.0, "True Lead": True, "Status": "대기"})

    for ep_name in ["EP-EG1 (황반변성)", "EP-EG2 (소화기암)", "EP-EG3 (면역노화)"]:
        for i in range(3, 20):
            dg = round(np.random.uniform(-11.0, -6.0), 2)
            ddg = round(np.random.uniform(-2.5, 0.1), 2)
            dtm = round(np.random.uniform(0.1, 5.0), 2)
            eff = round(np.random.uniform(25.0, 85.0), 1)
            tox = round(np.random.uniform(20.0, 90.0), 1)
            if dg < -8.5 and ddg < -1.5:
                dtm += 1.0; eff += 15.0
            substances.append({
                "Substance ID": f"EVG-{ep_name[3:6]}-{i:03d}", "Name": f"Compound_{ep_name[3:6]}_{i:03d}",
                "Type": np.random.choice(["Kinase Domain (저분자)", "ECD Domain (중분자 펩타이드)", "Natural Product (천연물/미생물)"]),
                "Epic ID": ep_name, "Target": "Target factor", "ΔG": dg, "ΔΔG": ddg,
                "TSA dTm": min(dtm, 6.0), "Efficacy": min(eff, 100.0), "Tox": round(np.random.uniform(20.0, 95.0), 1),
                "True Lead": False, "Status": "대기"
            })

    df_sub = pd.DataFrame(substances)

    filtered = df_sub.copy()
    if f_epic != "All":
        filtered = filtered[filtered["Epic ID"] == f_epic]
    if f_type != "All":
        filtered = filtered[filtered["Type"] == f_type]
    filtered = filtered[filtered["Efficacy"] >= min_eff_val]

    col_m1, col_m2 = st.columns([3, 2])
    with col_m1:
        st.subheader(f"📊 스크리닝 필터링 결과 (조회됨: {len(filtered)} 건)")
        sub_table_html = """
        <table class="fixed-header-table">
            <thead>
                <tr>
                    <th>물질 ID</th>
                    <th>물질명</th>
                    <th>모달리티</th>
                    <th>ΔG (Affinity)</th>
                    <th>Efficacy (%)</th>
                    <th>상태</th>
                </tr>
            </thead>
            <tbody>
        """
        for index, row in filtered.iterrows():
            sub_table_html += f"""
                <tr>
                    <td><b>{row['Substance ID']}</b></td>
                    <td><span style="color: #2dd4bf; font-weight: 700;">{row['Name']}</span></td>
                    <td>{row['Type']}</td>
                    <td><code>{row['ΔG']} kcal/mol</code></td>
                    <td><b>{row['Efficacy']}%</b></td>
                    <td>{render_badge(row['Status'])}</td>
                </tr>
            """
        sub_table_html += "</tbody></table>"
        st.markdown(sub_table_html, unsafe_allow_html=True)
        
    with col_m2:
        st.subheader("🎯 Wet-Dry 데이터 상관관계 시각화 (산점도)")
        if not filtered.empty:
            fig = px.scatter(
                filtered, x="ΔG", y="Efficacy", size="TSA dTm", color="Type",
                hover_name="Name", hover_data=["Substance ID", "Epic ID", "ΔΔG"],
                color_discrete_map={"Kinase Domain (저분자)": "#06b6d4", "ECD Domain (중분자 펩타이드)": "#ec4899", "Natural Product (천연물/미생물)": "#10b981"},
                title=f"Affinity (ΔG) vs Efficacy (%)"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#f1f5f9",
                xaxis=dict(showgrid=True, gridcolor="#334155"),
                yaxis=dict(showgrid=True, gridcolor="#334155")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("데이터가 없습니다.")

# ---------------------------------------------------------
# 📅 [MENU 4] 랩 미팅 및 블로커 (Lab Sync)
# ---------------------------------------------------------
elif "랩 미팅 및 블로커" in menu_selection:
    st.markdown("<h1>📅 랩 미팅 & 실시간 블로커(병목) 트래커</h1>", unsafe_allow_html=True)
    st.markdown(f"다기관 PI 공동연구진의 주간 안건 및 병목 구간입니다. {tooltip('4-HNE', dict_tooltip['4-HNE'])} 독성 해소, {tooltip('H3K27me3', dict_tooltip['H3K27me3'])} 잠금장치 복원 등 랩 논의 안건이 투명하게 개방됩니다.", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    blockers = [
        {"과제 ID": "EP-EG2", "담당 PI": "김명석 박사", "블로커 내용": "췌장암 기질 해체 평가용 hu-HSC PDX 마우스 공급망 및 8월 입고 일정 사전 조율", "심각도": "대기", "예상해결": "2026-08-01"},
        {"과제 ID": "EP-EG1", "담당 PI": "최용수 박사", "블로커 내용": "유리체 약산성(pH 5.5) 감응형 PEG-리포좀 3-Batch 봉입 프로토콜 사전 확립", "심각도": "대기", "예상해결": "2026-08-01"},
        {"과제 ID": "EP-EG3", "담당 PI": "이충구 박사", "블로커 내용": "dLck-cre 마우스의 자연노화(16개월령) 개체군 후성유전 ATAC-seq 분석 시나리오 준비", "심각도": "대기", "예상해결": "2026-08-01"}
    ]

    st.subheader("🚨 공동 연구팀 병목(Blocker) 현황 (과제 개시 전 준비)")
    b_table = """
    <table class="fixed-header-table">
        <thead>
            <tr>
                <th style="width: 15%;">과제 ID</th>
                <th style="width: 15%;">담당 PI</th>
                <th style="width: 50%;">블로커 및 사전 조율 안건</th>
                <th style="width: 10%;">상태 (Status)</th>
                <th style="width: 10%;">예상 해결일</th>
            </tr>
        </thead>
        <tbody>
    """
    for b in blockers:
        b_table += f"<tr><td><b>{b['과제 ID']}</b></td><td>{b['담당 PI']}</td><td>{b['블로커 내용']}</td><td>{render_badge(b['심각도'])}</td><td><code>{b['예상해결']}</code></td></tr>"
    b_table += "</tbody></table>"
    st.markdown(b_table, unsafe_allow_html=True)

# ---------------------------------------------------------
# 📈 [MENU 5] 행정 매트릭스 (Admin Metrics)
# ---------------------------------------------------------
else:
    st.markdown("<h1>📈 에버그린 프로젝트 행정 매트릭스 (KPI & 예산)</h1>", unsafe_allow_html=True)
    st.markdown("특허 출원 목표 달성 및 예산 소집 집행률을 추적하는 실시간 행정 포털입니다. 과제 시작(8월) 전이므로 모든 소진율은 <b>'0%'</b>로 초기화되어 기동됩니다.")
    st.markdown("<br>", unsafe_allow_html=True)

    col_ad1, col_ad2, col_ad3 = st.columns(3)
    with col_ad1:
        st.markdown(r"""
        <div class="card-wrapper">
            <h3>💸 누적 예산 집행률</h3>
            <div style='font-size: 32px; font-weight: 800; color: #2dd4bf; margin: 10px 0;'>0.0%</div>
            <p style='color: #cbd5e1; font-size: 13px;'>올해 8월 연구 개시 후 실시간 소진율 연동 예정</p>
        </div>
        """, unsafe_allow_html=True)
    with col_ad2:
        st.markdown(r"""
        <div class="card-wrapper">
            <h3>📜 공동 특허 출원</h3>
            <div style='font-size: 32px; font-weight: 800; color: #2dd4bf; margin: 10px 0;'>0 / 4 건</div>
            <p style='color: #cbd5e1; font-size: 13px;'>EP-EG2 신규 용도 및 조성물 특허 2건 출원 예정</p>
        </div>
        """, unsafe_allow_html=True)
    with col_ad3:
        st.markdown(r"""
        <div class="card-wrapper">
            <h3>🎯 마일스톤 적기 달성도</h3>
            <div style='font-size: 32px; font-weight: 800; color: #cbd5e1; margin: 10px 0;'>대기중</div>
            <p style='color: #cbd5e1; font-size: 13px;'>8월 과제 시작 시 마일스톤 온트랙 비율 가동</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; font-size: 14px;'>"
    "© 2026 Evergreen National Strategic Research Project Coordination Group. "
    "KIST & KRIBB Joint Laboratory. All Rights Reserved."
    "</div>", 
    unsafe_allow_html=True
)
