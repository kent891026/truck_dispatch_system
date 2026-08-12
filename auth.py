<<<<<<< HEAD
import streamlit as st

def render_login_page():
    """渲染登入畫面，並處理身分驗證邏輯"""
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🔒 派車與薪資管理系統</h2>", unsafe_allow_html=True)
    
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
                    st.error("❌ 帳號或密碼錯誤！")

def render_sidebar_logout():
    """渲染側邊欄的身分資訊與登出按鈕"""
    with st.sidebar:
        st.title("🚚 系統選單")
        st.info(f"👤 目前身分：{st.session_state['role']}")
        
        # 決定選單內容
        menu_options = ["📝 每日派車單輸入", "📊 月底結算台", "⚙️ 基本資料與費率設定"]
        if st.session_state["role"] == "管理員":
            menu_options.append("🛠️ 開發者後台 (資料監管)")
            
        selected_page = st.radio("請選擇功能：", menu_options)
        
        st.markdown("---")
        if st.button("🚪 登出系統"):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.rerun()
            
=======
import streamlit as st

def render_login_page():
    """渲染登入畫面，並處理身分驗證邏輯"""
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🔒 派車與薪資管理系統</h2>", unsafe_allow_html=True)
    
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
                    st.error("❌ 帳號或密碼錯誤！")

def render_sidebar_logout():
    """渲染側邊欄的身分資訊與登出按鈕"""
    with st.sidebar:
        st.title("🚚 系統選單")
        st.info(f"👤 目前身分：{st.session_state['role']}")
        
        # 決定選單內容
        menu_options = ["📝 每日派車單輸入", "📊 月底結算台", "⚙️ 基本資料與費率設定"]
        if st.session_state["role"] == "管理員":
            menu_options.append("🛠️ 開發者後台 (資料監管)")
            
        selected_page = st.radio("請選擇功能：", menu_options)
        
        st.markdown("---")
        if st.button("🚪 登出系統"):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.rerun()
            
>>>>>>> 6dc226a02ff70a5de420748604475cf5f3b56fad
        return selected_page