
# 檔案使用 Streamlit 與 bcrypt 進行密碼驗證與登入流程
# 身份驗證與登入頁面模組
import streamlit as st
import bcrypt
# 定義已加密的密碼雜湊值，分別對應不同使用者
BOSS_HASH = b"$2b$12$k5VoChq.y4.EoguZCKqBMuZYrQt635PsUOBOYAQkIsfacQhIZ9ACy" # 老闆娘
YABI_HASH = b"$2b$12$6r7Gt3fkEYgTC7fWBDSXFOrHIyDSFshdqGOZNkqFANZB9E6OXaJWm" # 管理員

# 驗證輸入的密碼是否與已加密的密碼雜湊值匹配
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

# 渲染登入頁面，包含帳號、密碼輸入欄位與登入按鈕
def render_login_page():
    st.markdown(
        """
        <style>
        /* 登入頁面專屬背景 */
        .stApp { background: linear-gradient(135deg, #F4F7FA 0%, #E9EEF3 100%); }
        
        /* 登入卡片元件美化 */
        .login-brand { margin-top: 40px; text-align: center; }
        .login-logo { display: inline-flex; align-items: center; justify-content: center; width: 54px; height: 54px; border-radius: 14px; background: #1F4E79; color: white; font-size: 22px; font-weight: 800; margin-bottom: 18px; box-shadow: 0 10px 25px rgba(31, 78, 121, 0.18); }
        .login-title { margin: 0; color: #101828; font-size: 32px; font-weight: 800; letter-spacing: -0.8px; }
        .login-subtitle { margin-top: 8px; color: #667085; font-size: 14px; }
        .login-card { background: #FFFFFF; border: 1px solid #E4E7EC; border-radius: 18px; padding: 28px; margin-top: 26px; box-shadow: 0 15px 40px rgba(16, 24, 40, 0.05); }
        .login-card-title { color: #101828; font-size: 18px; font-weight: 700; margin-bottom: 4px; }
        .login-card-description { color: #667085; font-size: 13px; margin-bottom: 20px; }
        .stTextInput label { color: #344054 !important; font-weight: 600 !important; font-size: 13px !important; }
        .stTextInput input { border-radius: 10px !important; border: 1px solid #D0D5DD !important; min-height: 42px !important; }
        .stTextInput input:focus { border-color: #1F4E79 !important; box-shadow: 0 0 0 3px rgba(31, 78, 121, 0.10) !important; }
        .stButton > button { border-radius: 10px !important; min-height: 44px !important; font-weight: 700 !important; transition: transform 0.15s ease, box-shadow 0.15s ease; }
        .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(16, 24, 40, 0.10); }
        .login-footer { text-align: center; margin-top: 28px; color: #98A2B3; font-size: 12px; }
        </style>
        """, unsafe_allow_html=True
    )
    # 渲染登入頁面品牌標誌與系統名稱
    st.markdown(
        "<div class='login-brand'>"
        "<div class='login-logo'>Ff</div>"
        "<h1 class='login-title'>乖乖派車 | FleetFlow</h1>"
        "<div class='login-subtitle'>Fleet Dispatch | Payroll Management</div>"
        "</div>", unsafe_allow_html=True
    )
    # 渲染登入卡片元件，包含帳號、密碼輸入欄位與登入按鈕
    left, center, right = st.columns([1, 1.1, 1])
    with center:
        st.markdown(
            "<div class='login-card'>"
            "<div class='login-card-title'>登入乖乖派車系統</div>"
            "<div class='login-card-description'>輸入帳號進入管理系統</div>"
            "</div>", unsafe_allow_html=True
        )

        username = st.text_input("帳號", placeholder="輸入帳號", key="login_username")
        password = st.text_input("密碼", type="password", placeholder="輸入密碼", key="login_password")
        # 在帳號與密碼輸入欄位下方增加間距
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        # 渲染登入與訪客體驗按鈕，並處理按鈕點擊事件
        col_login, col_guest = st.columns(2)
        with col_login:
            login_btn = st.button("登入系統", use_container_width=True, type="primary", key="login_submit")
        with col_guest:
            guest_btn = st.button("訪客體驗", use_container_width=True, key="guest_submit")
        
        if login_btn:
            clean_user = username.strip().lower()
            clean_pass = password.strip()
            if clean_user == "boss" and verify_password(clean_pass, BOSS_HASH): # 老闆娘帳號密碼的雜湊值驗證
                st.session_state["logged_in"] = True
                st.session_state["role"] = "老闆娘"
                st.rerun()
            elif clean_user == "yabi" and verify_password(clean_pass, YABI_HASH): # 管理員帳號密碼的雜湊值驗證
                st.session_state["logged_in"] = True
                st.session_state["role"] = "管理員"
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請重新確認。")

        if guest_btn:
            st.session_state["logged_in"] = True
            st.session_state["role"] = "訪客"
            st.rerun()
        # 登入頁面底部的系統名稱與版權資訊
        st.markdown("<div class='login-footer'>GuaiGuai FleetFlow · Dispatch Management System</div>", unsafe_allow_html=True)

# 渲染側邊欄，顯示使用者角色、系統功能選單與登出按鈕
def render_sidebar_logout():
    role = st.session_state.get("role", "未知")

    with st.sidebar:
        st.markdown(
            "<div style='padding: 8px 4px 22px 4px;'>"
            "<div style='font-size:24px; font-weight:800; color:#1F4E79; letter-spacing:-0.8px;'>乖乖派車系統</div>"
            "<div style='font-size:11px; color:#98A2B3; margin-top:3px; letter-spacing:0.3px;'>FLEET DISPATCH SYSTEM</div>"
            "</div>", unsafe_allow_html=True
        )

        role_label = {"老闆娘": "管理者", "管理員": "系統管理員", "訪客": "訪客模式"}.get(role, role)

        st.markdown(
            "<div style='background:#F2F4F7; border:1px solid #E4E7EC; border-radius:10px; padding:11px 12px; margin-bottom:20px;'>"
            "<div style='font-size:11px; color:#98A2B3; margin-bottom:3px;'>CURRENT ROLE</div>"
            f"<div style='font-size:14px; font-weight:700; color:#344054;'>{role_label}</div>"
            "</div>", unsafe_allow_html=True
        )

        st.markdown("<div style='color:#98A2B3; font-size:11px; font-weight:700; letter-spacing:1px; margin-bottom:7px;'>OPERATIONS</div>", unsafe_allow_html=True)

        menu_options = ["每日司機派車", "月底結算收據", "資料費率設定"]
        selected_page = st.radio("系統功能", menu_options, label_visibility="collapsed", key="main_navigation")
        # 在側邊欄中顯示訪客體驗模式提示，並提供系統狀態與登出按鈕
        if role == "訪客":
            st.markdown(
                "<div style='margin-top:18px; background:#FFFAEB; border:1px solid #FEDF89; border-radius:10px; padding:12px;'>"
                "<div style='color:#B54708; font-size:12px; font-weight:700; margin-bottom:4px;'>體驗模式</div>"
                "<div style='color:#7A2E0E; font-size:11px; line-height:1.5;'>您可以瀏覽與試算系統功能</div>"
                "</div>", unsafe_allow_html=True
            )
        # 在側邊欄底部增加系統狀態顯示，顯示資料庫連線狀態
        st.markdown(
            "<div style='margin-top:30px; padding-top:18px; border-top:1px solid #EAECF0;'>"
            "<div style='font-size:11px; color:#98A2B3; margin-bottom:8px;'>SYSTEM STATUS</div>"
            "<div style='display:flex; align-items:center; gap:7px; font-size:12px; color:#475467;'>"
            "<span style='width:7px; height:7px; background:#12B76A; border-radius:50%; display:inline-block;'></span>Database connected"
            "</div></div>", unsafe_allow_html=True
        )
        # 在側邊欄底部增加登出按鈕，並處理登出事件
        st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
        if st.button("登出系統", use_container_width=True, key="logout_button"):
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.rerun()

    return selected_page