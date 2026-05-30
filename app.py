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
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0f19 !important;
        color: #f1f5f9 !important;
    }
    .main {
        background-color: #0b0f19 !important;
    }
    
    /* Prevent black-on-black or low-contrast text on all headings, paragraphs, and list items */
    h1, h2, h3, p, li, span, label {
        color: #f1f5f9 !important;
    }
    
    /* Style all native text fields, selectboxes, and dropdowns for extreme high contrast */
    div[data-baseweb="select"] {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 6px !important;
    }
    
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    
    /* Dropdown popups styling */
    div[data-testid="stVirtualDropdown"] div {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    div[data-testid="stVirtualDropdown"] li {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    
    div[data-testid="stVirtualDropdown"] li:hover {
        background-color: #155e75 !important;
        color: #ffffff !important;
    }

    /* Style text input fields */
    div[data-testid="stTextInput"] input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 6px !important;
    }
    
    /* Expanders high contrast */
    div[data-testid="stExpander"] {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }
    
    div[data-testid="stExpander"] * {
        color: #ffffff !important;
    }

    /* Streamlit alert/notification high contrast overrides */
    div[data-testid="stNotification"] {
        background-color: #1e1b4b !important;
        border: 1px solid #4f46e5 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stNotification"] * {
        color: #ffffff !important;
    }
    
    /* Toggle switch contrast */
    div[data-testid="stCheckbox"] label * {
        color: #ffffff !important;
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
# 🔒 Premium Security Gateway (Password Lock: evergreen)
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    """Returns True if the user entered the correct password."""
    if st.session_state.authenticated:
        return True

    # Render a premium glassmorphic login gate
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="card-wrapper" style="text-align: center; padding: 40px 30px; border: 2px solid #14b8a6; box-shadow: 0 20px 40px rgba(0,0,0,0.6);">
            <div style="font-size: 60px; margin-bottom: 20px;">🔒</div>
            <h2 style="border-left: none; padding-left: 0; text-align: center; color: #f8fafc; margin-top: 0;">Evergreen LIMS Portal</h2>
            <p style="color: #cbd5e1; font-size: 14px; margin-bottom: 25px; line-height: 1.6;">
                본 시스템은 다기관 공동연구원 및 관계자 전용 LIMS 관제 포털입니다.<br>
                비허가자의 접근을 제한하기 위해 보안 암호를 입력해 주십시오.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        password_input = st.text_input("보안 패스워드 입력", type="password", key="login_pw", placeholder="Enter Portal Password")
        
        if password_input:
            if password_input == "evergreen":
                st.session_state.authenticated = True
                st.success("보안 암호 확인 완료. 포털에 진입합니다...")
                st.rerun()
            else:
                st.error("보안 암호가 올바르지 않습니다. 다시 시도해 주십시오.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align: center; color: #475569; font-size: 13px;'>"
            "© 2026 Evergreen Joint Laboratory. All Rights Reserved."
            "</div>", 
            unsafe_allow_html=True
        )
    return False

if not check_password():
    st.stop()

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
        {
            "Epic ID": "EP-EG1", 
            "Epic (Project)": "노화 대식세포 표적 황반변성 치료제 개발 (이욱빈 팀)", 
            "Year 1 (1차)": "TAM axis & SARM1 3D 구조 분석, In silico 가상 스크리닝(NPI Finder + Agentic AI), Senolysis/Efferocytosis 이중 평가모델 및 후안부 리포좀 기초 설계.", 
            "Year 2 (2차)": "ML/QSAR rescoring 및 off-target 리스크 평가, hERG/CYP 스크리닝, SARM1 저해 MoA 규명, 각막 투과형 지능형 능동 리포좀 설계 및 고안압 IOP 동물모델 단기 약효 실증.", 
            "Year 3 (3차)": "2차 가상 스크리닝 및 MMPA 분석, KRIBB 협력 환자 유래 망막 오가노이드 기반 인간 PoC 규명, 식물 엑소좀-LNP 하이브리드 전달체 최종 제조 및 scRNA-seq 종단 분석.", 
            "Year 4 (4차)": "SPR/MST 유도체 결합력 재검증, 점안 투여 vs 유리체강 내 주사 맹검 비교 검증, TFF(접선유동여과) 공정 Scale-up 및 화학적 Fingerprint 품질 동등성 검증, 비GLP 예비 안독성 확보.", 
            "Year 5 (5차)": "AIDD SOP 및 특허 권리화, CMC 완결 QC 사양서 및 eCTD e-패키지 구축, 28일 반복 투여 독성시험(TK 프로파일) 완료 및 FIH(초회 인체 용량) 산출을 통한 Pre-IND/Factbook 완결 및 기술이전."
        },
        {
            "Epic ID": "EP-EG2", 
            "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어 (김명석 팀)", 
            "Year 1 (1차)": "TCGA/ICGC 글로벌 오믹스 기반 ALK7/TGF-β 하위 아형 정의 및 타겟 확정, AlphaFold2 연계 알로스테릭 포켓 스크리닝, T세포 내 ALK7-Smad2/3 면역회피 기전(Anti-PD-L1 감작) 규명.", 
            "Year 2 (2차)": "병용 투여용 다중 탑재 하이브리드 나노 플랫폼(DDS) 구축, 미세 산성 환경 감응형 Smart Release 링커 설계, 저산소 유도 3D Tumor-Stroma on a chip 모사 및 암세포-Niche 동시 제어 최적화.", 
            "Year 3 (3차)": "Hit-to-lead 구조 정렬 및 표적 선택성 Rescue 실험, 예비 ADME/독성 스크리닝, 동소이식 및 전이 모델 기반 mOS 연장 시너지 실증, 장-근육-면역 축(Gut-Muscle-Immune Axis) 대사 정상화.", 
            "Year 4 (4차)": "RSM(반응표면분석법) 활용 나노 DDS 탑재 공정 스케일업, FOLFIRINOX SoC 병용 In vivo 최적화, cGAS-STING-IFN-β 경로 선천면역 활성화, 임상 코호트 TMA 디지털 병리 바이오마커 연계.", 
            "Year 5 (5차)": "하이브리드 나노 전달체 대량 제조 QC 균일성 검증, ALK7/TIGIT 연계 동반진단(CDx) 및 액체생검CTC/Exosome 상용화 타진, Pre-IND 패키지 eCTD 규격화 완결, 글로벌 L/O 팩트북 발간 및 빅파마 실사."
        },
        {
            "Epic ID": "EP-EG3", 
            "Epic (Project)": "면역노화 진단 바이오마커 개발 Ets1 (이충구 팀)", 
            "Year 1 (1차)": "CD127(생존 항상성) 급감 및 면역관문(PD-1, TIGIT, TIM-3) 축적에 따른 Ets1 저하 T세포 노화 프로파일링, NPI Finder + Agentic AI 활용 Ets1-크로마틴 복합체 가상 스크리닝 돌입.", 
            "Year 2 (2차)": "T세포 특이적 Ets1 결핍 마우스 모델(dLck-cre Ets1Δ/Δ) 구축, 비장 내 나이브/메모리 T세포 풀 변동 추적, 자연노화 vs D-galactose 노화 교차 검증 및 Ets1 조절 선도물질 In vitro 유효 Hit 실증.", 
            "Year 3 (3차)": "Ets1 결합 부위 ATAC-seq 및 ChIP-seq 후성유전 크로마틴 접근성 규명, Smarce1/Smarcc1 IP 규명, H3K27ac(활성) -> H3K27me3(잠금) Epigenetic-Rewiring 효율 정량화.", 
            "Year 4 (4차)": "In vivo T세포 특이적 Ets1 활성화 약물 치료 효능 검증, 종말 소진 T세포(Ttex)의 전구 상태(Tpex) 리프로그래밍 검증, SCENIC/GRN 계산생물학 네트워크 규명, 전신 염증 수치 저하 노화 극복 평가.", 
            "Year 5 (5차)": "Ets1 조절 최종 후보물질의 ADME/Tox 및 비임상 안전성 평가 패키징, 면역노화 진단 마커 및 치료 용도 특허 청구항 강력 IP 장벽 구축, 조기 L/O를 위한 비임상 팩트북 및 eCTD e-패키지 완결."
        }
    ],
    "Y1_1차년도": [
        {
            "Epic ID": "EP-EG1", 
            "Epic (Project)": "노화 대식세포 표적 황반변성 치료제", 
            "Milestone (Phase)": "M1. AI/구조 기반 안질환 표적 분석 및 1차 후보물질 우선순위화", 
            "Task — Specific Experiments (Bullet Points)": "• KIST 고유 천연물 라이브러리(자생 1,160종 / 생약 372종 / 버섯 118종) 빅데이터 큐레이션 및 MerTK/AXL/TYRO3/SARM1 단백질의 3차원 포켓 적합성 가상 스크리닝(NPI Finder + Agentic AI).\n• 위양성 배제 및 1차 우선 검증 화합물 도출.", 
            "담당 PI 연구팀": "이욱빈, 최용수", 
            "Timeline": "Y1-Q1~Q2"
        },
        {
            "Epic ID": "EP-EG1", 
            "Epic (Project)": "노화 대식세포 표적 황반변성 치료제", 
            "Milestone (Phase)": "M2. In vitro 세포 수준 병리기전 및 다중 타겟 평가 모델 구축", 
            "Task — Specific Experiments (Bullet Points)": "• 인간 망막색소상피 세포주(ARPE-19) Doxorubicin 노화 유도를 통한 SA-β-gal 활성 및 SASP(IL-6, IL-8, MCP-1) qPCR 프로파일링 시스템 구축.\n• THP-1 및 BV2 미세아교세포 기반 노화 모델 구축을 통한 Senolytic/Efferocytosis 이중 스크리닝 플랫폼 구축.\n• R28 망막 신경세포주 흥분독성(Glutamate) 및 지질과산화(4-HNE) 유발 ROS/미토콘드리아 기능 평가 모델 구축.", 
            "담당 PI 연구팀": "최용수, 강석우", 
            "Timeline": "Y1-Q2~Q3"
        },
        {
            "Epic ID": "EP-EG1", 
            "Epic (Project)": "노화 대식세포 표적 황반변성 치료제", 
            "Milestone (Phase)": "M3. 후안부 도달 장벽 극복형 첨단 약물 전달체 기초 설계", 
            "Task — Specific Experiments (Bullet Points)": "• 박막 수화법(Thin-film hydration) 및 고압 유화기를 활용한 80~120nm 균일 이온화 지질 리포좀 합성.\n• 능동 약물 탑재 공정 변수 초기 설계 및 식물 유래 항염증 엑소좀 고순도 정제 공정 확립.", 
            "담당 PI 연구팀": "강석우", 
            "Timeline": "Y1-Q3~Q4"
        },
        {
            "Epic ID": "EP-EG1", 
            "Epic (Project)": "노화 대식세포 표적 황반변성 치료제", 
            "Milestone (Phase)": "M4. 노화 기반 안질환 동물모델 SOP 수립 및 병리 표현형 규명", 
            "Task — Specific Experiments (Bullet Points)": "• NaIO₃ 건성 황반변성(AMD) 마우스 모델 구축 및 망막 분리 scRNA-seq 단일세포 전사체 분석.\n• 병리성 대식세포 DAM(Disease-Associated Microglia) 서브클러스터 동정 및 Efferocytosis 기능 저하 수용체 상호작용 맵핑.", 
            "담당 PI 연구팀": "이욱빈, 최용수", 
            "Timeline": "Y1-Q3~Y1-Q4"
        },
        {
            "Epic ID": "EP-EG2", 
            "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어", 
            "Milestone (Phase)": "M1. 다기원 오믹스 기반 종양 아형 정의 및 타깃 확정", 
            "Task — Specific Experiments (Bullet Points)": "• TCGA/ICGC/GEO 데이터셋 통합 분석을 통한 간암·췌장암의 ALK7 및 TGF-β 의존성 하위 아형 정의.\n• 전이 및 치료 저항성과 직결된 종양 아형별 예후 인자 분석 및 악액질 핵심 수용체 도메인 확정.", 
            "담당 PI 연구팀": "김명석, 김원규", 
            "Timeline": "Y1-Q1~Q2"
        },
        {
            "Epic ID": "EP-EG2", 
            "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어", 
            "Milestone (Phase)": "M2. AI-구조 융합 가상 스크리닝 5단계 파이프라인 가동", 
            "Task — Specific Experiments (Bullet Points)": "• FDA 승인 약물 및 NPI Finder 23,000종 화합물 대상 AlphaFold2 예측 ALK7 특이적 알로스테릭 유사 포켓 도킹 시뮬레이션 및 분자동역학(MD) 스크리닝.\n• PAINS 필터링을 적용한 true hits 검출.", 
            "담당 PI 연구팀": "김명석", 
            "Timeline": "Y1-Q2~Q3"
        },
        {
            "Epic ID": "EP-EG2", 
            "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어", 
            "Milestone (Phase)": "M3. In vitro 탐색 플랫폼 조건 확립 및 유효 물질 검증", 
            "Task — Specific Experiments (Bullet Points)": "• TGF-β 하위 신호전달(Smad2/3, MAPK, Rho/ROCK) 및 YAP/TAZ 활성 억제능 평가.\n• 췌장암/간암 HTS 3D invasion assay 확립.\n• T세포 내 ALK7-Smad2/3 경로의 직접 면역회피 제어 기전(Anti-PD-L1 감작) 검증.", 
            "담당 PI 연구팀": "김원규, 김명석", 
            "Timeline": "Y1-Q3~Q4"
        },
        {
            "Epic ID": "EP-EG2", 
            "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어", 
            "Milestone (Phase)": "M4. TME 기질 모사 Niche 조절 및 악액질 기초 모델 구축", 
            "Task — Specific Experiments (Bullet Points)": "• 스트레스 유도 BM-MSC(골수유래 줄기세포) 노화 모델 구축 및 SASP 인자 정량 분석.\n• 췌장암 CAF(암연관섬유아세포) 공동 배양 시스템 수립을 통한 기질 밀도 조절능 평가 및 skeletal muscle c2c12 악액질 결합 어세이 구축.", 
            "담당 PI 연구팀": "김명석", 
            "Timeline": "Y1-Q3~Q4"
        },
        {
            "Epic ID": "EP-EG3", 
            "Epic (Project)": "면역노화 진단 바이오마커 개발", 
            "Milestone (Phase)": "M1. Ets1 저하 T세포 노화/고갈 표현형 프로파일링", 
            "Task — Specific Experiments (Bullet Points)": "• T세포 만성 자극에 따른 Ets1 발현 추적.\n• Ets1 결핍 시 유도되는 CD127(생존 항상성) 급감 정량화.\n• 면역관문(PD-1, TIGIT, TIM-3) 및 노화 마커(CD57, CD28-, KLRG-1)의 세포 표면 축적 양상 분석.", 
            "담당 PI 연구팀": "이충구", 
            "Timeline": "Y1-Q1~Q2"
        },
        {
            "Epic ID": "EP-EG3", 
            "Epic (Project)": "면역노화 진단 바이오마커 개발", 
            "Milestone (Phase)": "M2. 면역노화 핵심 조절 인자 Ets1 기능적 타당성 규명", 
            "Task — Specific Experiments (Bullet Points)": "• 흉선 위축 및 나이브 T세포 감소와 Ets1 발현 상관관계 분석.\n• Ets1 N-말단(Thr38 인산화) p300/CBP 아세틸화 스캐폴드 결합성 검증 및 C-말단 RFWD2 결합 유비퀴틴화 분해 경로 기전 탐색.", 
            "담당 PI 연구팀": "이충구", 
            "Timeline": "Y1-Q2~Q3"
        },
        {
            "Epic ID": "EP-EG3", 
            "Epic (Project)": "면역노화 진단 바이오마커 개발", 
            "Milestone (Phase)": "M3. Ets1 타겟 후보물질 가상 스크리닝 및 Discovery 전략 수립", 
            "Task — Specific Experiments (Bullet Points)": "• NPI Finder 빅데이터 플랫폼 및 Agentic AI를 연동한 Ets1-크로마틴 결합 3D 구조 분석.\n• Ets1 활성화 및 안정화를 유도하는 저분자 화합물 In silico 1차 스크리닝 착수 및 ADMET/PAINS 위양성 필터링.", 
            "담당 PI 연구팀": "이충구, 김원규", 
            "Timeline": "Y1-Q3~Q4"
        },
        {
            "Epic ID": "EP-EG3", 
            "Epic (Project)": "면역노화 진단 바이오마커 개발", 
            "Milestone (Phase)": "M4. dLck-cre T세포 특이적 Ets1 결핍 In vivo 시스템 설계", 
            "Task — Specific Experiments (Bullet Points)": "• Distal Lck promoter (dLck-cre) Ets1ΔdLck T세포 특이적 결핍 마우스 교배 및 표현형 분석 시나리오 설계.\n• 4개월령(청년군) 대비 16개월령(자연 노화군) 마우스 비장 내 나이브/메모리 T세포 풀의 유세포분석(FACS) 프로토콜 설계.", 
            "담당 PI 연구팀": "이충구", 
            "Timeline": "Y1-Q3~Y1-Q4"
        }
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

# Initialize Session State for Pipelines to enable dynamic additions & modifications
if "pipeline_db" not in st.session_state or not isinstance(st.session_state.pipeline_db, dict):
    st.session_state.pipeline_db = {}
    for sheet_name, df in excel_data.items():
        st.session_state.pipeline_db[sheet_name] = df.copy()
    
    # Ensure sheets Y1 to Y5 all exist and are beautifully hydrated
    years_keys = ["Y1_1차년도", "Y2_2차년도", "Y3_3차년도", "Y4_4차년도", "Y5_5차년도"]
    for y in years_keys:
        if y not in st.session_state.pipeline_db:
            if y == "Y1_1차년도" and "Y1_1차년도" in BUILTIN_PIPELINES:
                st.session_state.pipeline_db["Y1_1차년도"] = pd.DataFrame(BUILTIN_PIPELINES["Y1_1차년도"])
            else:
                y_num = y.split("_")[0].replace("Y", "")
                mock_rows = []
                mock_rows.append({
                    "Epic ID": "EP-EG1", 
                    "Epic (Project)": "노화 대식세포 표적 황반변성 치료제", 
                    "Milestone (Phase)": f"M1. {y_num}차년도 핵심 병리 작용 분석 및 최적화", 
                    "Task — Specific Experiments (Bullet Points)": f"• EP-EG1 {y_num}차년도 비임상 효능 최적화 스크리닝 진행\n• MoA 분자 신호 전달 경로 검증", 
                    "담당 PI 연구팀": "1세부 공동연구팀", 
                    "Timeline": f"Y{y_num}-Q1~Q2"
                })
                mock_rows.append({
                    "Epic ID": "EP-EG2", 
                    "Epic (Project)": "소화기암 기질 해체 및 전이/악액질 제어", 
                    "Milestone (Phase)": f"M1. {y_num}차년도 나노 제형 효능 실증 및 3D 칩 검증", 
                    "Task — Specific Experiments (Bullet Points)": f"• EP-EG2 {y_num}차년도 암-Niche 상호작용 및 기질 해체 억제 테스트\n• 장-근육-면역 축 인자 모니터링 어세이", 
                    "담당 PI 연구팀": "2세부 공동연구팀", 
                    "Timeline": f"Y{y_num}-Q1~Q2"
                })
                mock_rows.append({
                    "Epic ID": "EP-EG3", 
                    "Epic (Project)": "면역노화 진단 바이오마커 개발", 
                    "Milestone (Phase)": f"M1. {y_num}차년도 Ets1 활성 및 후성유전학 재프로그래밍 MoA 규명", 
                    "Task — Specific Experiments (Bullet Points)": f"• EP-EG3 {y_num}차년도 T세포 크로마틴 접근성 ChIP-seq 및 ATAC-seq 분석\n• 동물 모델 효능 분석 및 ADME 평가", 
                    "담당 PI 연구팀": "3세부 공동연구팀", 
                    "Timeline": f"Y{y_num}-Q1~Q2"
                })
                st.session_state.pipeline_db[y] = pd.DataFrame(mock_rows)

# Initialize Session State for Blockers (Lab Sync) to enable dynamic additions & modifications
if "blockers_db" not in st.session_state or not isinstance(st.session_state.blockers_db, dict):
    st.session_state.blockers_db = {}
    
    # Prepopulate Year 1 (1차년도) blockers with premium examples
    y1_blockers = [
        {"과제 ID": "EP-EG1", "담당 PI/연구팀": "1세부 공동연구팀", "블로커 및 사전 조율 안건": "유리체 약산성(pH 5.5) 감응형 PEG-리포좀 3-Batch 봉입 프로토콜 사전 확립 지연", "상태 (Status)": "대기", "예상 해결일": "2026-08-01"},
        {"과제 ID": "EP-EG2", "담당 PI/연구팀": "2세부 공동연구팀", "블로커 및 사전 조율 안건": "췌장암 기질 해체 평가용 hu-HSC PDX 마우스 공급망 및 8월 입고 일정 사전 조율", "상태 (Status)": "대기", "예상 해결일": "2026-08-01"},
        {"과제 ID": "EP-EG3", "담당 PI/연구팀": "3세부 공동연구팀", "블로커 및 사전 조율 안건": "dLck-cre 마우스의 자연노화(16개월령) 개체군 후성유전 ATAC-seq 분석 시나리오 준비", "상태 (Status)": "대기", "예상 해결일": "2026-08-01"},
        {"과제 ID": "EP-EG1", "담당 PI/연구팀": "1세부 공동연구팀", "블로커 및 사전 조율 안건": "AMD 건성/습성 동물모델 SOP 수립을 위한 NaIO₃ 정맥투여 적정 농도 2차 검증 필요", "상태 (Status)": "대기", "예상 해결일": "2026-08-01"},
        {"과제 ID": "EP-EG2", "담당 PI/연구팀": "2세부 공동연구팀", "블로커 및 사전 조율 안건": "ALK7 알로스테릭 포켓 스크리닝 true hits 선별용 AlphaFold2 3D 가상 도킹 인프라 리소스 확보", "상태 (Status)": "대기", "예상 해결일": "2026-08-01"}
    ]
    st.session_state.blockers_db["Y1_1차년도"] = pd.DataFrame(y1_blockers)
    
    # Prepopulate other years with realistic academic-grade placeholders
    st.session_state.blockers_db["Y2_2차년도"] = pd.DataFrame([
        {"과제 ID": "EP-EG1", "담당 PI/연구팀": "1세부 공동연구팀", "블로커 및 사전 조율 안건": "각막 투과성 평가용 Franz diffusion cell 및 동적 유체 라인 셋업 지연 해결 필요", "상태 (Status)": "대기", "예상 해결일": "2027-02-15"},
        {"과제 ID": "EP-EG2", "담당 PI/연구팀": "2세부 공동연구팀", "블로커 및 사전 조율 안건": "3D Tumor-Stroma on a chip 미세 유체 제어 표준 유속 설정 검증", "상태 (Status)": "대기", "예상 해결일": "2027-03-10"},
        {"과제 ID": "EP-EG3", "담당 PI/연구팀": "3세부 공동연구팀", "블로커 및 사전 조율 안건": "dLck-cre Ets1Δ/Δ 마우스 F1 세대 유전형(Genotyping) PCR 검증 프로토콜 확립", "상태 (Status)": "대기", "예상 해결일": "2027-04-05"}
    ])
    st.session_state.blockers_db["Y3_3차년도"] = pd.DataFrame([
        {"과제 ID": "EP-EG1", "담당 PI/연구팀": "1세부 공동연구팀", "블로커 및 사전 조율 안건": "환자 유래 망막 오가노이드(KRIBB 협력) 품질 관리 규격 및 세포 생존도 확인 검증", "상태 (Status)": "대기", "예상 해결일": "2028-01-20"},
        {"과제 ID": "EP-EG2", "담당 PI/연구팀": "2세부 공동연구팀", "블로커 및 사전 조율 안건": "동소이식 및 전이 마우스 모델 생체 이미징 및 mOS 추적 장비 예약 조율", "상태 (Status)": "대기", "예상 해결일": "2028-02-15"},
        {"과제 ID": "EP-EG3", "담당 PI/연구팀": "3세부 공동연구팀", "블로커 및 사전 조율 안건": "ChIP-seq 시퀀싱 라이브러리 제작 및 Smarce1/Smarcc1 항체 특이성 검증", "상태 (Status)": "대기", "예상 해결일": "2028-03-30"}
    ])
    st.session_state.blockers_db["Y4_4차년도"] = pd.DataFrame([
        {"과제 ID": "EP-EG1", "담당 PI/연구팀": "1세부 공동연구팀", "블로커 및 사전 조율 안건": "유리체강 내 주사 vs 점안 투여 맹검(Blind) 비교 연구를 위한 동물 행동 및 통증 프로토콜 수립", "상태 (Status)": "대기", "예상 해결일": "2029-01-15"},
        {"과제 ID": "EP-EG2", "담당 PI/연구팀": "2세부 공동연구팀", "블로커 및 사전 조율 안건": "접선유동여과(TFF) 공정을 활용한 나노 전달체 합성 스케일업 공정성 확보", "상태 (Status)": "대기", "예상 해결일": "2029-02-28"},
        {"과제 ID": "EP-EG3", "담당 PI/연구팀": "3세부 공동연구팀", "블로커 및 사전 조율 안건": "SCENIC/GRN 계산생물학 알고리즘 가동을 위한 고성능 클러스터 메모리 증설", "상태 (Status)": "대기", "예상 해결일": "2029-04-10"}
    ])
    st.session_state.blockers_db["Y5_5차년도"] = pd.DataFrame([
        {"과제 ID": "EP-EG1", "담당 PI/연구팀": "1세부 공동연구팀", "블로커 및 사전 조율 안건": "Pre-IND eCTD 양식 작성 및 규제기관(식약처/FDA) 미팅 지원용 문서화 포맷 통일", "상태 (Status)": "대기", "예상 해결일": "2030-01-20"},
        {"과제 ID": "EP-EG2", "담당 PI/연구팀": "2세부 공동연구팀", "블로커 및 사전 조율 안건": "나노 DDS 제형 대량 제조 공정의 배치 간 재현성(Batch-to-Batch reproducibility) 문서화", "상태 (Status)": "대기", "예상 해결일": "2030-02-15"},
        {"과제 ID": "EP-EG3", "담당 PI/연구팀": "3세부 공동연구팀", "블로커 및 사전 조율 안건": "Ets1 조절 최종 선도물질의 신규 용도 및 조성물 특허 청구항 권리범위 최종 조율", "상태 (Status)": "대기", "예상 해결일": "2030-03-10"}
    ])


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
            <p style='color: #cbd5e1; font-size: 14px;'>주관: 1세부 공동연구팀</p>
            <div style='font-size: 26px; font-weight: 800; color: #2dd4bf; margin: 10px 0;'>대기상태 (0% / 1차년도)</div>
            <p style='color: #cbd5e1; font-size: 13px; line-height:1.5;'>• 5년차 EP: 28일 반복 투여 독성(안전성) 완료, IND-ready 패키지 완성 및 기술이전<br>• 핵심 타겟: SARM1, TAM axis (MerTK/AXL/TYRO3)<br>• 현황: 천연물 라이브러리 가상 스크리닝(NPI Finder + Agentic AI) 대기</p>
        </div>
        """, unsafe_allow_html=True)
    with col_ep2:
        st.markdown(r"""
        <div class="card-wrapper">
            <h3>🧬 EP-EG2: 소화기암 전이/악액질 극복</h3>
            <p style='color: #cbd5e1; font-size: 14px;'>주관: 2세부 공동연구팀</p>
            <div style='font-size: 26px; font-weight: 800; color: #2dd4bf; margin: 10px 0;'>대기상태 (0% / 1차년도)</div>
            <p style='color: #cbd5e1; font-size: 13px; line-height:1.5;'>• 5년차 EP: Pre-IND 패키지 eCTD 규격화 완결, L/O Factbook 발간 및 글로벌 기술이전<br>• 핵심 타겟: ALK7 알로스테릭 포켓, TME 기질 장벽<br>• 현황: 다기원 오믹스 기반 암 아형 정의 및 AlphaFold2 구조 모델링 대기</p>
        </div>
        """, unsafe_allow_html=True)
    with col_ep3:
        st.markdown(r"""
        <div class="card-wrapper">
            <h3>🩸 EP-EG3: 면역노화 진단 바이오마커</h3>
            <p style='color: #cbd5e1; font-size: 14px;'>주관: 3세부 공동연구팀</p>
            <div style='font-size: 26px; font-weight: 800; color: #2dd4bf; margin: 10px 0;'>대기상태 (0% / 1차년도)</div>
            <p style='color: #cbd5e1; font-size: 13px; line-height:1.5;'>• 5년차 EP: Ets1 조절 비임상 안전성 검증, 용도 특허 확보 및 조기 L/O 패키징 완결<br>• 핵심 타겟: Ets1 전사인자, dLck-cre 마우스 모델<br>• 현황: dLck-cre 결핍 마우스 교배 시나리오 및 T세포 노화 프로파일링 설계 대기</p>
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
    st.markdown(f"국가전략과제계획서에서 추출된 연차별 마일스톤 테이블입니다. 직접 데이터를 추가하거나 셀을 더블클릭하여 수정할 수 있으며, ({tooltip('TSA/DSF', dict_tooltip['TSA/DSF'])}, {tooltip('dLck-cre', dict_tooltip['dLck-cre'])}) 등 전문 용어에 호버하시면 측정 근거 주석이 팝업됩니다.", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 5-Year Navigation & Mode Switch
    col_nav1, col_nav2 = st.columns([3, 1])
    with col_nav1:
        selected_year = st.selectbox(
            "📅 연차별 계획 필터링",
            ["All (5개년 전체)", "1차년도 (Year 1)", "2차년도 (Year 2)", "3차년도 (Year 3)", "4차년도 (Year 4)", "5차년도 (Year 5)"],
            key="pipeline_year_select"
        )
    with col_nav2:
        edit_mode = st.toggle("🔓 LIMS 실시간 편집 활성화", value=False, key="pipeline_edit_toggle")

    # Map selected year to sheet keys
    year_map = {
        "All (5개년 전체)": ["Y1_1차년도", "Y2_2차년도", "Y3_3차년도", "Y4_4차년도", "Y5_5차년도"],
        "1차년도 (Year 1)": ["Y1_1차년도"],
        "2차년도 (Year 2)": ["Y2_2차년도"],
        "3차년도 (Year 3)": ["Y3_3차년도"],
        "4차년도 (Year 4)": ["Y4_4차년도"],
        "5차년도 (Year 5)": ["Y5_5차년도"]
    }
    target_sheets = year_map[selected_year]

    # --- Mode 1: Interactive Data Editor Mode ---
    if edit_mode:
        st.info("💡 **LIMS 데이터 실시간 편집 모드**: 표 내부의 셀을 더블클릭하여 자유롭게 수정하거나, 표 최하단의 `+ Add row` 버튼을 클릭하여 행을 추가할 수 있습니다. 수정한 뒤 좌측의 'All (5개년 전체)' 필터를 변경하거나 편집 모드를 끄면 고대비 완성본으로 렌더링됩니다.")
        
        if selected_year == "All (5개년 전체)":
            tab_names = ["1차년도", "2차년도", "3차년도", "4차년도", "5차년도"]
            tabs = st.tabs(tab_names)
            for idx, key in enumerate(target_sheets):
                with tabs[idx]:
                    df = st.session_state.pipeline_db[key]
                    edited_df = st.data_editor(
                        df,
                        use_container_width=True,
                        num_rows="dynamic",
                        key=f"editor_{key}",
                        column_config={
                            "Epic ID": st.column_config.SelectboxColumn("과제 ID (Epic ID)", options=["EP-EG1", "EP-EG2", "EP-EG3"], required=True),
                            "Epic (Project)": st.column_config.TextColumn("Epic 과제명", width="medium"),
                            "Milestone (Phase)": st.column_config.TextColumn("마일스톤 (Phase)", width="large"),
                            "Task — Specific Experiments (Bullet Points)": st.column_config.TextColumn("세부 실험 Task", width="large"),
                            "담당 PI 연구팀": st.column_config.TextColumn("담당 PI/연구팀", width="medium"),
                            "Timeline": st.column_config.TextColumn("일정", width="small")
                        }
                    )
                    st.session_state.pipeline_db[key] = edited_df
        else:
            key = target_sheets[0]
            df = st.session_state.pipeline_db[key]
            edited_df = st.data_editor(
                df,
                use_container_width=True,
                num_rows="dynamic",
                key=f"editor_single_{key}",
                column_config={
                    "Epic ID": st.column_config.SelectboxColumn("과제 ID (Epic ID)", options=["EP-EG1", "EP-EG2", "EP-EG3"], required=True),
                    "Epic (Project)": st.column_config.TextColumn("Epic 과제명", width="medium"),
                    "Milestone (Phase)": st.column_config.TextColumn("마일스톤 (Phase)", width="large"),
                    "Task — Specific Experiments (Bullet Points)": st.column_config.TextColumn("세부 실험 Task", width="large"),
                    "담당 PI/연구팀": st.column_config.TextColumn("담당 PI/연구팀", width="medium"),
                    "Timeline": st.column_config.TextColumn("일정", width="small")
                }
            )
            st.session_state.pipeline_db[key] = edited_df

    # --- Mode 2: Premium Visual Table Mode ---
    else:
        search_q = st.text_input("🔍 마일스톤 및 태스크 키워드 검색 (예: ALK7, 오가노이드, Ets1, SARM1 등)", "")
        
        rows = []
        for s_name in target_sheets:
            df = st.session_state.pipeline_db[s_name]
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
            table_html = """<table class="fixed-header-table">
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
<tbody>"""
            for r_data in rows:
                table_html += f"""<tr>
<td><b style="color: #f8fafc; font-size: 14px;">{r_data['연차']}</b></td>
<td>{get_epic_badge(r_data['Epic ID'])}</td>
<td><b style="color: #e2e8f0; font-size: 14px;">{r_data['Milestone']}</b></td>
<td style="color: #cbd5e1; font-size: 13.5px; padding: 12px 16px;">{r_data['세부 실험 Task']}</td>
<td><code style="background-color: #1e293b; color: #38bdf8; padding: 4px 8px; border-radius: 4px; border: 1px solid #334155; font-weight: 600;">{r_data['일정']}</code></td>
<td>{render_badge(r_data['상태'])}</td>
</tr>"""
            table_html += "</tbody></table>"
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.info("검색 조건에 부합하는 파이프라인 태스크가 없습니다.")

    with st.expander("📂 원본 데이터 엑셀 시트 뷰어"):
        if excel_data:
            sub_tabs = st.tabs(list(excel_data.keys()))
            for idx, (s_name, df) in enumerate(excel_data.items()):
                with sub_tabs[idx]:
                    st.dataframe(st.session_state.pipeline_db[s_name], use_container_width=True)

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
        sub_table_html = """<table class="fixed-header-table">
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
<tbody>"""
        for index, row in filtered.iterrows():
            sub_table_html += f"""<tr>
<td><b>{row['Substance ID']}</b></td>
<td><span style="color: #2dd4bf; font-weight: 700;">{row['Name']}</span></td>
<td>{row['Type']}</td>
<td><code>{row['ΔG']} kcal/mol</code></td>
<td><b>{row['Efficacy']}%</b></td>
<td>{render_badge(row['Status'])}</td>
</tr>"""
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
elif "랩 미팅" in menu_selection:
    st.markdown("<h1>📅 랩 미팅 & 실시간 블로커(병목) 트래커</h1>", unsafe_allow_html=True)
    st.markdown(f"다기관 PI 공동연구진의 주간 안건 및 병목 구간입니다. {tooltip('4-HNE', dict_tooltip['4-HNE'])} 독성 해소, {tooltip('H3K27me3', dict_tooltip['H3K27me3'])} 잠금장치 복원 등 랩 논의 안건이 투명하게 개방되며 실시간 추가/편집이 지원됩니다.", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 5-Year Navigation & Mode Switch for Blockers
    col_b_nav1, col_b_nav2 = st.columns([3, 1])
    with col_b_nav1:
        selected_blocker_year = st.selectbox(
            "📅 연차별 병목 필터링",
            ["All (5개년 전체)", "1차년도 (Year 1)", "2차년도 (Year 2)", "3차년도 (Year 3)", "4차년도 (Year 4)", "5차년도 (Year 5)"],
            key="blocker_year_select"
        )
    with col_b_nav2:
        blocker_edit = st.toggle("🔓 블로커 실시간 편집 활성화", value=False, key="blocker_edit_toggle")

    # Map selected blocker year to sheet keys
    blocker_year_map = {
        "All (5개년 전체)": ["Y1_1차년도", "Y2_2차년도", "Y3_3차년도", "Y4_4차년도", "Y5_5차년도"],
        "1차년도 (Year 1)": ["Y1_1차년도"],
        "2차년도 (Year 2)": ["Y2_2차년도"],
        "3차년도 (Year 3)": ["Y3_3차년도"],
        "4차년도 (Year 4)": ["Y4_4차년도"],
        "5차년도 (Year 5)": ["Y5_5차년도"]
    }
    target_blocker_sheets = blocker_year_map[selected_blocker_year]

    # --- Mode 1: Interactive Data Editor ---
    if blocker_edit:
        st.info("💡 **블로커 실시간 편집 모드**: 표 내부의 셀을 더블클릭하여 자유롭게 수정하거나, 표 최하단의 `+ Add row` 버튼을 클릭하여 행을 추가할 수 있습니다. 수정한 뒤 좌측의 'All (5개년 전체)' 필터를 변경하거나 편집 모드를 끄면 고대비 완성본으로 렌더링됩니다.")
        
        if selected_blocker_year == "All (5개년 전체)":
            tab_names = ["1차년도", "2차년도", "3차년도", "4차년도", "5차년도"]
            tabs = st.tabs(tab_names)
            for idx, key in enumerate(target_blocker_sheets):
                with tabs[idx]:
                    df_b = st.session_state.blockers_db[key]
                    edited_df_b = st.data_editor(
                        df_b,
                        use_container_width=True,
                        num_rows="dynamic",
                        key=f"blocker_editor_{key}",
                        column_config={
                            "과제 ID": st.column_config.SelectboxColumn("과제 ID", options=["EP-EG1", "EP-EG2", "EP-EG3"], required=True),
                            "담당 PI/연구팀": st.column_config.TextColumn("담당 PI/연구팀", width="medium"),
                            "블로커 및 사전 조율 안건": st.column_config.TextColumn("블로커 및 사전 조율 안건", width="large"),
                            "상태 (Status)": st.column_config.SelectboxColumn("상태 (Status)", options=["대기", "진행중", "완료"], required=True),
                            "예상 해결일": st.column_config.TextColumn("예상 해결일", width="small")
                        }
                    )
                    st.session_state.blockers_db[key] = edited_df_b
        else:
            key = target_blocker_sheets[0]
            df_b = st.session_state.blockers_db[key]
            edited_df_b = st.data_editor(
                df_b,
                use_container_width=True,
                num_rows="dynamic",
                key=f"blocker_editor_single_{key}",
                column_config={
                    "과제 ID": st.column_config.SelectboxColumn("과제 ID", options=["EP-EG1", "EP-EG2", "EP-EG3"], required=True),
                    "담당 PI/연구팀": st.column_config.TextColumn("담당 PI/연구팀", width="medium"),
                    "블로커 및 사전 조율 안건": st.column_config.TextColumn("블로커 및 사전 조율 안건", width="large"),
                    "상태 (Status)": st.column_config.SelectboxColumn("상태 (Status)", options=["대기", "진행중", "완료"], required=True),
                    "예상 해결일": st.column_config.TextColumn("예상 해결일", width="small")
                }
            )
            st.session_state.blockers_db[key] = edited_df_b

    # --- Mode 2: Premium Visual Table ---
    else:
        b_table = """<table class="fixed-header-table">
<thead>
<tr>
<th style="width: 12%;">연차</th>
<th style="width: 12%;">과제 ID</th>
<th style="width: 18%;">담당 PI/연구팀</th>
<th style="width: 43%;">블로커 및 사전 조율 안건</th>
<th style="width: 10%;">상태 (Status)</th>
<th style="width: 10%;">예상 해결일</th>
</tr>
</thead>
<tbody>"""
        for s_name in target_blocker_sheets:
            df_b = st.session_state.blockers_db[s_name]
            parts = s_name.replace("Y", "").split("_")
            y_display = f"{parts[1]} (Year {parts[0]})" if len(parts) >= 2 else s_name.replace("Y", "Year ").replace("_", " ")
            
            for idx, row in df_b.iterrows():
                blocker_text = str(row.get("블로커 및 사전 조율 안건", ""))
                
                # Auto-inject hover tooltips for biotech terms inside blocker descriptions
                for term, definition in dict_tooltip.items():
                    if term in blocker_text:
                        blocker_text = blocker_text.replace(term, tooltip(term, definition))
                
                b_table += f"""<tr>
<td><b style="color: #f8fafc; font-size: 14px;">{y_display}</b></td>
<td>{get_epic_badge(row.get('과제 ID', ''))}</td>
<td><b style="color: #f8fafc; font-size: 14px;">{row.get('담당 PI/연구팀', '')}</b></td>
<td style="color: #cbd5e1; font-size: 13.5px; padding: 12px 16px;">{blocker_text}</td>
<td>{render_badge(row.get('상태 (Status)', '대기'))}</td>
<td><code style="background-color: #1e293b; color: #38bdf8; padding: 4px 8px; border-radius: 4px; border: 1px solid #334155; font-weight: 600;">{row.get('예상 해결일', '')}</code></td>
</tr>"""
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
