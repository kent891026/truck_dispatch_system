
# 用來渲染派車單右側的即時估價卡片與結算台下方的最終薪資卡片的元件模組
import streamlit as st

# 將數值格式化為貨幣格式，並加上千分位逗號
def money(value):
    return f"${value:,.0f}"

# 渲染派車單右側的即時估價卡片
def render_live_fare_card(total_price, basic_freight, subsidy_total, real_region):
    st.markdown(
        f"""
        <div style="background: #102A43; border-radius: 16px; padding: 24px; color: white; box-shadow: 0 12px 30px rgba(16,42,67,0.15);">
            <div style="font-size: 11px; color: #BFD0DF; letter-spacing: 0.8px; font-weight: 700;">REAL-TIME ESTIMATE</div>
            <div style="font-size: 34px; font-weight: 800; margin-top: 8px; margin-bottom: 16px;">{money(total_price)}</div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 13px;">
                <span style="color: #9FB3C8;">基本運費</span>
                <span style="font-weight: 600;">{money(basic_freight)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1); font-size: 13px;">
                <span style="color: #9FB3C8;">特殊加給</span>
                <span style="font-weight: 600; color: #48BB78;">+{money(subsidy_total)}</span>
            </div>
            <div style="margin-top: 16px; font-size: 11px; color: #9FB3C8;">該單計價地區</div>
            <div style="font-size: 14px; font-weight: 600; margin-top: 4px;">{real_region}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 渲染結算台下方的最終薪資卡片
def render_payroll_card(final_salary, driver_name, month):
    st.markdown(
        f"""
        <div style="background: #102A43; border-radius: 16px; padding: 24px; text-align: right; color: white; box-shadow: 0 12px 30px rgba(16,42,67,0.15);">
            <div style="color: #BFD0DF; font-size: 12px; letter-spacing: 0.8px; font-weight: 700;">NET PAYROLL</div>
            <div style="font-size: 34px; font-weight: 800; margin-top: 5px;">{money(final_salary)}</div>
            <div style="color: #BFD0DF; font-size: 11px; margin-top: 4px;">{driver_name} · {month}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )