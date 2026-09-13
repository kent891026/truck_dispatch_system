
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
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.container(border=True):
            username = st.text_input("帳號", key="login_username")
            password = st.text_input("密碼", type="password", key="login_password")
            login_btn = st.button("登入系統", use_container_width=True, key="login_submit_btn")
            
            if login_btn:
                clean_user = username.strip().lower()
                clean_pass = password.strip()
                
                # bcrypt 雜湊驗證
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
        return selected_page