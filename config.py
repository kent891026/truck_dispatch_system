import streamlit as st

def setup_page():
    """初始化 Streamlit 頁面設定"""
    st.set_page_config(
        page_title="FLEETFLOW",
        page_icon="🚛",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def load_global_css():
    """載入企業 SaaS 風格的全局 CSS (思源宋體 安全修復版)"""
    st.markdown(
        """
        <style>
        /* 1. 從 Google Fonts 雲端安全載入「思源宋體」 */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600;700;800&display=swap');

        /* 2. 全局背景 */
        .stApp { background-color: #F5F7FA; }
        
        /* 🌟 精準字體套用：拔除 span 和 div 的強制覆寫，把 Streamlit 內建的圖示 (Icon) 還給系統！ */
        .stApp, h1, h2, h3, h4, p, label, input, li, .stButton > button {
            font-family: 'Noto Serif TC', serif !important;
        }

        /* 針對宋體微調字級，確保閱讀清晰度 */
        p, label, input, li {
            font-size: 1.05rem !important; 
        }

        /* 3. 安全的版面寬度與內距設定 */
        .block-container { max-width: 1200px !important; padding-top: 5rem !important; padding-bottom: 3rem; }

        /* 4. 柔化卡片與表單的邊框 */
        div[data-testid="stVerticalBlockBorderWrapper"] { 
            border-radius: 12px !important; 
            border: 1px solid #E4E7EC !important; 
            background: #FFFFFF !important; 
            box-shadow: 0 4px 12px rgba(16,24,40,0.03); 
        }
        
        /* 5. 統一按鈕美化 */
        .stButton > button { border-radius: 8px !important; font-weight: 600; border: 1px solid #D0D5DD; }
        .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        </style>
        """,
        unsafe_allow_html=True
    )