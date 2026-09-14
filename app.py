
#  Streamlit 應用程式的主要入口點，負責初始化頁面、處理使用者登入狀態，以及根據使用者選擇的功能頁面渲染對應的內容。
import streamlit as st
import config
import auth
from components.header import page_header
from components.forms import render_dispatch_form, render_salary_form, render_settings_form

# 初始化 Streamlit 頁面設定與全域 CSS 樣式
config.setup_page()
config.load_global_css()
# 初始化使用者登入狀態，若尚未登入則渲染登入頁面
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None
# 若使用者尚未登入，則渲染登入頁面並停止後續程式執行
if not st.session_state["logged_in"]:
    auth.render_login_page()
    st.stop()

selected_page = auth.render_sidebar_logout()
# 根據使用者在側邊欄選擇的功能頁面，渲染對應的內容
if selected_page == "每日司機派車":
    page_header("每日司機派車", "建立 | 試算 | 儲存 每日貨櫃運輸派車單")
    render_dispatch_form()

elif selected_page == "月底結算收據":
    page_header("月底結算收據", "依司機與月份彙整派車趟次與薪資")
    render_salary_form()

elif selected_page == "資料費率設定":
    page_header("資料費率設定", "管理 司機 | 車輛 | 地區 計價規則")
    render_settings_form()