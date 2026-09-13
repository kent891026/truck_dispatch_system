import streamlit as st
import config
import auth
from components.header import page_header
from components.forms import render_dispatch_form, render_salary_form, render_settings_form

config.setup_page()
config.load_global_css()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None

if not st.session_state["logged_in"]:
    auth.render_login_page()
    st.stop()

selected_page = auth.render_sidebar_logout()

if selected_page == "每日派車單輸入":
    page_header("每日派車", "建立、試算與儲存每日貨櫃運輸派車單")
    render_dispatch_form()

elif selected_page == "月底結算台":
    page_header("月底結算", "依司機與月份彙整派車趟次與薪資")
    render_salary_form()

elif selected_page == "基本資料與費率設定":
    page_header("基本資料", "管理司機、車輛與地區計價規則")
    render_settings_form()