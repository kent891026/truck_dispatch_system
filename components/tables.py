import pandas as pd
import streamlit as st

def money(value):
    return f"${value:,.0f}"

def render_dispatch_table(table_data):
    """渲染派車明細表"""
    if not table_data:
        st.info("尚無派車資料。")
        return
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_driver_table(drivers):
    """渲染司機名冊"""
    if drivers:
        driver_df = pd.DataFrame([{"代號": d.driver_id, "姓名": d.name, "狀態": "啟用" if d.is_active else "停用"} for d in drivers])
        st.dataframe(driver_df, use_container_width=True, hide_index=True)
    else:
        st.info("目前尚無司機資料。")

def render_truck_table(trucks):
    """渲染車輛名冊"""
    if trucks:
        truck_df = pd.DataFrame([{"車號": t.truck_number, "尺寸": t.size} for t in trucks])
        st.dataframe(truck_df, use_container_width=True, hide_index=True)
    else:
        st.info("目前尚無車輛資料。")

def render_price_rule_table(rules):
    """渲染地區費率表"""
    if rules:
        rule_df = pd.DataFrame([{"地區": r.region_name, "基本運費": money(r.base_price)} for r in rules])
        st.dataframe(rule_df, use_container_width=True, hide_index=True)
    else:
        st.info("目前尚無地區費率資料。")