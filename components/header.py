import streamlit as st

def page_header(title, description):
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #EAECF0;">
            <div>
                <h1 style="font-size: 28px; font-weight: 800; color: #101828; margin: 0; padding: 0;">{title}</h1>
                <p style="font-size: 14px; color: #667085; margin: 6px 0 0 0;">{description}</p>
            </div>
            <div style="display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-radius: 999px; background: #ECFDF3; border: 1px solid #ABEFC6; color: #067647; font-size: 13px; font-weight: 600;">
                <span style="width: 8px; height: 8px; background: #12B76A; border-radius: 50%; display: inline-block;"></span>
                System Online
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def section_title(title, description=None):
    st.markdown(
        f"<div style='color: #344054; font-size: 16px; font-weight: 700; margin-top: 24px; margin-bottom: 8px;'>{title}</div>", 
        unsafe_allow_html=True
    )
    if description:
        st.markdown(f"<div style='color: #667085; font-size: 13px; margin-bottom: 16px;'>{description}</div>", unsafe_allow_html=True)