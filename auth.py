
import streamlit as st
import bcrypt

def render_login_page():
    """渲染登入畫面，並處理身分驗證邏輯"""
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>派車與薪資管理系統</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.container(border=True):
            username = st.text_input("帳號")
            password = st.text_input("密碼", type="password")
            login_btn = st.button("登入系統", use_container_width=True)
            
            if login_btn:
                clean_user = username.strip().lower()
                clean_pass = password.strip()
                
                # 簡易權限判定
                if clean_user == "boss" and clean_pass == "1234":
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "老闆"
                    st.rerun()
                elif clean_user == "yabi" and clean_pass == "admin888":
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "管理員"
                    st.rerun()
                else:
                    st.error("帳號或密碼錯誤！")

def render_sidebar_logout():
    """渲染側邊欄的身分資訊與登出按鈕"""
    with st.sidebar:
        st.title("系統選單")
        st.info(f"目前身分：{st.session_state['role']}")
        
        # 決定選單內容
        menu_options = ["每日派車單輸入", "月底結算台", "基本資料與費率設定"]
        if st.session_state["role"] == "管理員":
            menu_options.append("開發者後台 (資料監管)")
            
        selected_page = st.radio("請選擇功能：", menu_options)
        
        st.markdown("---")
        if st.button("登出系統"):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.rerun()


# 生成的兩組雜湊值貼在這邊 (注意保留前面的 b，代表 bytes 格式)
BOSS_HASH = b'$2b$12$k5VoChq.y4.EoguZCKqBMuZYrQt635PsUOBOYAQkIsfacQhIZ9ACy'
YABI_HASH = b'$2b$12$6r7Gt3fkEYgTC7fWBDSXFOrHIyDSFshdqGOZNkqFANZB9E6OXaJWm'

def verify_password(plain_password, hashed_password):
    """用 bcrypt 驗證使用者輸入的密碼是否與雜湊值相符"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def render_login_page():
    """渲染登入畫面，並處理身分驗證邏輯"""
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>派車與薪資管理系統</h2>", unsafe_allow_html=True)
    
    # 注入唯美的 CSS 視覺設定
    st.markdown("""
        <style>
        /* 隱藏預設的頂部選單與底部浮水印 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 設置全畫面漸層背景 (柔和的藍灰系，視覺無壓迫感) */
        .stApp {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            font-family: 'Helvetica Neue', Helvetica, Arial, 'Microsoft JhengHei', sans-serif;
        }
        
        /* 半透明玻璃擬態 (Glassmorphism) 登入框設計 */
        div[data-testid="stVerticalBlock"] > div:first-child {
            background: rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        }
        
        /* 美化輸入框與按鈕 */
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        .stButton>button {
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2c3e50; font-weight: 700; letter-spacing: 2px;'>派車與薪資管理系統</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555; margin-bottom: 30px;'>系統登入 / System Login</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        # 使用空的 container 讓 CSS 捕捉並套用玻璃特效
        with st.container():
            username = st.text_input("帳號 Username", key="login_username")
            password = st.text_input("密碼 Password", type="password", key="login_password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 將登入與訪客模式並排
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                login_btn = st.button("登入系統", use_container_width=True, type="primary", key="login_submit_btn")
            with btn_col2:
                guest_btn = st.button("訪客體驗", use_container_width=True, key="guest_submit_btn")
            
            # 登入邏輯
            if login_btn:
                clean_user = username.strip().lower()
                clean_pass = password.strip()
                
                if clean_user == "boss" and verify_password(clean_pass, BOSS_HASH):
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "老闆"
                    st.rerun()
                elif clean_user == "yabi" and verify_password(clean_pass, YABI_HASH):
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = "管理員"
                    st.rerun()
                else:
                    st.error("帳號或密碼錯誤！")
            
            # 訪客邏輯 (給面試教授或其他人測試用)
            if guest_btn:
                st.session_state["logged_in"] = True
                st.session_state["role"] = "訪客"
                st.rerun()

def render_sidebar_logout():
    """渲染側邊欄的身分資訊與登出按鈕"""
    with st.sidebar:
        st.markdown(f"### 目前身分：<span style='color:#3498db;'>{st.session_state['role']}</span>", unsafe_allow_html=True)
        if st.session_state["role"] == "訪客":
            st.info("提示：您正處於訪客體驗模式，所有操作皆為模擬，不會真實影響後台資料庫。")
            
        st.markdown("---")
        
        menu_options = ["每日派車單輸入", "月底結算台", "基本資料與費率設定"]
        if st.session_state["role"] == "管理員":
            menu_options.append("開發者後台 (資料監管)")
            
        selected_page = st.radio("請選擇功能：", menu_options)
        
        st.markdown("---")
        if st.button("登出系統", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.rerun()
        return selected_page