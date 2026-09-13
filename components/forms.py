import datetime
import streamlit as st

from calculator import calculate_single_trip, calculate_monthly_salary, DESTINATION_PRICES
from models import DispatchOrderModel
from crud import (
    create_or_update_dispatch_order, get_order_by_driver_and_month, get_all_drivers,
    add_driver, get_all_trucks, add_truck, get_all_price_rules, update_or_add_price_rule
)

from components.header import section_title
from components.cards import render_live_fare_card, render_payroll_card
from components.tables import render_dispatch_table, render_driver_table, render_truck_table, render_price_rule_table

def money(value):
    return f"${value:,.0f}"

def get_driver_options():
    drivers = get_all_drivers()
    if not drivers:
        return ["0599 (AAA)", "1099 (BBB)"]
    return [f"{d.driver_id} ({d.name})" for d in drivers if d.is_active]

def get_truck_options():
    trucks = get_all_trucks()
    if not trucks:
        return [
            "2L-22 (XXX) (20呎)", "39-J6 (206) (20呎)", "M4-41 (207) (20呎)",
            "07-J6 (208) (20呎)", "82-PJ (209) (20呎)", "22-H5 (309) (40呎)",
            "FC-S2 (310) (40呎)", "62-AJ (311) (40呎)", "FE-B9 (312) (40呎)",
            "9H-40 (315) (40呎)", "DJ-91 (316) (40呎)", "65-J5 (318) (40呎)",
            "HD-763 (319) (40呎)",
        ]
    return [f"{t.truck_number} ({t.size})" for t in trucks]

def get_region_options():
    return list(DESTINATION_PRICES.keys())


# --- 模組 1：每日派車單 ---
def render_dispatch_form():
    drivers = get_driver_options()
    trucks = get_truck_options()
    regions = get_region_options()

    section_title("基本資訊", "輸入司機、車輛與貨櫃識別資訊")
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_driver = st.selectbox("司機", drivers + ["新增司機..."], key="dispatch_driver")
            if selected_driver == "新增司機...":
                real_driver = st.text_input("新司機代號", placeholder="例如：001", key="new_driver_id")
            else:
                real_driver = selected_driver.split(" ")[0]
        with col2:
            date = st.date_input("出車日期", value=datetime.date.today(), key="dispatch_date")
            is_return_trip = st.checkbox("來回車趟 A → B → A", key="dispatch_return")
        with col3:
            truck_filter = st.radio("車型", ["全部", "20呎", "40呎"], horizontal=True, key="truck_filter")
            filtered_trucks = trucks
            if truck_filter != "全部":
                filtered_trucks = [t for t in trucks if truck_filter in t]
            
            selected_truck = st.selectbox("出勤車輛", filtered_trucks + ["新增車輛..."], key="dispatch_truck")
            if selected_truck == "新增車輛...":
                new_truck_num = st.text_input("新車號", placeholder="例如：AA-1234", key="new_truck_number")
                new_truck_size = st.radio("車型", ["20呎", "40呎"], horizontal=True, key="new_truck_size")
                real_truck = f"{new_truck_num} ({new_truck_size})" if new_truck_num else ""
            else:
                real_truck = selected_truck
        raw_container_id = st.text_input("貨櫃櫃號", placeholder="例如：TGHU1234567", max_chars=13, key="dispatch_container")

    section_title("運送路線", "設定起運點、目的地與實際計價區域")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            point_of_origin = st.text_input("起運點", placeholder="例如：某海運公司", key="dispatch_origin")
            cargo_owner = st.text_input("貨主名稱", placeholder="例如：長榮海運", key="dispatch_cargo_owner")
        with col2:
            destination_address = st.text_input("下貨地址", placeholder="例如：新北市五股區...", key="dispatch_destination")
            region_filter = st.radio("計價區域", ["全部", "北部", "中部", "南部"], horizontal=True, key="region_filter")
            central_keywords = ["苗栗", "通霄", "後龍", "三義", "后里", "台中", "彰化", "員林", "南投", "雲林", "斗六", "斗南"]
            south_keywords = ["嘉義", "台南", "高雄", "屏東"]
            
            filtered_regions = []
            for region in regions:
                is_south = any(kw in region for kw in south_keywords)
                is_central = any(kw in region for kw in central_keywords)
                is_north = not is_south and not is_central
                if region_filter == "全部": filtered_regions.append(region)
                elif region_filter == "北部" and is_north: filtered_regions.append(region)
                elif region_filter == "中部" and is_central: filtered_regions.append(region)
                elif region_filter == "南部" and is_south: filtered_regions.append(region)

            selected_region = st.selectbox("實際計價地區", filtered_regions, key="dispatch_region")
            real_region = selected_region

    section_title("特殊條件與即時試算", "選擇本趟運輸的特殊條件，右側會同步更新金額")
    left, right = st.columns([1.55, 0.85], gap="large")
    
    with left:
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**作業加給**")
                has_freezing_plate = st.checkbox("冷凍板 +$300", key="add_freezing")
                has_weighting = st.checkbox("異地過磅 +$100", key="add_weighting")
                has_danger_tag = st.checkbox("危險標誌 +$100", key="add_danger")
                has_instrument_inspection = st.checkbox("儀器檢查 +$100", key="add_instrument")
            with col2:
                st.markdown("**時段加給**")
                is_night_shift = st.checkbox("夜間出車 +$1,000", key="add_night")
                is_holiday = st.checkbox("假日出車 +$1,000", key="add_holiday")
                early_shift_option = st.selectbox("早車時段", ["無", "03:00 +$200", "05:00 +$100"], key="add_early")
                unloading_overtime_hours = st.number_input("卸貨超時（小時）", min_value=0, max_value=24, value=0, step=1, key="add_overtime")

            early_shift_type = None
            if "03:00" in early_shift_option: early_shift_type = "03:00"
            elif "05:00" in early_shift_option: early_shift_type = "05:00"

            auto_tags = []
            if has_freezing_plate: auto_tags.append("冷凍板")
            if has_weighting: auto_tags.append("過磅")
            if has_danger_tag: auto_tags.append("危標")
            if has_instrument_inspection: auto_tags.append("儀檢")
            if is_night_shift: auto_tags.append("夜間")
            if is_holiday: auto_tags.append("假日")
            if early_shift_type: auto_tags.append(f"早車{early_shift_type}")
            if unloading_overtime_hours > 0: auto_tags.append(f"超時{unloading_overtime_hours}hr")

            auto_text = ""
            if auto_tags:
                auto_text = "[系統標記: " + ", ".join(auto_tags) + "]"
                st.caption(f"自動標記：{auto_text}")

            remarks = st.text_area("備註", placeholder="輸入其他交辦事項...", key="dispatch_remarks")

    with right:
        fees = calculate_single_trip(real_region, has_freezing_plate, has_weighting, has_danger_tag, has_instrument_inspection, is_night_shift, is_holiday, early_shift_type, unloading_overtime_hours)
        # 呼叫 cards.py 內的 UI 元件
        render_live_fare_card(fees["total_price"], fees["basic_freight"], fees["subsidy_total"], real_region)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    submitted = st.button("儲存派車單", use_container_width=True, type="primary", key="save_dispatch")

    if submitted:
        clean_id = raw_container_id.replace(" ", "").replace("-", "").upper()
        if len(clean_id) != 11:
            st.error("櫃號格式錯誤：需要 11 碼。")
        elif not real_driver or not real_truck or not point_of_origin or not real_region:
            st.error("請先完成所有必填欄位。")
        else:
            formatted_container_id = f"{clean_id[:4]} {clean_id[4:]}"
            final_remarks = f"{remarks} {auto_text}".strip() if auto_text else remarks

            if st.session_state["role"] == "訪客":
                st.info("系統提示：訪客模式僅進行模擬，不會寫入資料庫。")
                st.success(f"[模擬成功] 司機 {real_driver} 的派車單已處理。總計金額試算為 {money(fees['total_price'])}")
            else:
                new_order = DispatchOrderModel(
                    driver_id=real_driver, date=date.strftime("%Y-%m-%d"), container_id=formatted_container_id,
                    point_of_origin=point_of_origin, destination_address=(destination_address or "未填寫"),
                    truck_number=real_truck, cargo_owner=(cargo_owner or "未填寫"), billing_region=real_region,
                    is_return_trip=is_return_trip, has_weighting=has_weighting, has_danger_tag=has_danger_tag,
                    has_instrument_inspection=has_instrument_inspection, has_freezing_plate=has_freezing_plate,
                    is_night_shift=is_night_shift, is_holiday=is_holiday, early_shift_type=early_shift_type,
                    unloading_overtime_hours=unloading_overtime_hours, basic_freight=fees["basic_freight"],
                    subsidy_total=fees["subsidy_total"], remarks=final_remarks
                )
                if create_or_update_dispatch_order(new_order):
                    st.success(f"[系統提示] 派車單已成功儲存。總額：{money(fees['total_price'])}")


# --- 模組 2：月底結算台 ---
def render_salary_form():
    drivers = get_all_drivers()
    driver_options = [f"{d.driver_id} ({d.name})" for d in drivers] if drivers else ["0599 (AAA)"]

    section_title("結算條件", "選擇司機與結算月份")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            query_driver = st.selectbox("司機", driver_options, key="salary_driver")
            real_query_driver = query_driver.split(" ")[0]
        with col2:
            query_month = st.text_input("結算月份", value=datetime.date.today().strftime("%Y-%m"), placeholder="YYYY-MM", key="salary_month")

    section_title("薪資調整", "設定本月固定獎金、補貼與扣款")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            full_attendance = st.number_input("全勤獎金", value=3000, step=500, key="salary_attendance")
            safety_check = st.checkbox("安全獎金", key="salary_safety")
            safety_bonus = 15000 if safety_check else 0
        with c2:
            labor_health = st.number_input("勞健保", value=5000, step=500, key="salary_labor_health")
            phone_sub = st.number_input("電話費補助", value=700, step=100, key="salary_phone")
        with c3:
            other_add = st.number_input("其他補貼", value=0, step=100, key="salary_other_add")
            other_deduct = st.number_input("其他扣款", value=0, step=100, key="salary_other_deduct")

    calculate_btn = st.button("開始結算", use_container_width=True, type="primary", key="calculate_salary")

    if calculate_btn:
        records = get_order_by_driver_and_month(real_query_driver, query_month)
        if not records:
            st.warning(f"找不到 {real_query_driver} 在 {query_month} 的派車紀錄。")
        else:
            table_data, trip_prices = [], []
            for record in records:
                single_total = record.basic_freight + record.subsidy_total
                trip_prices.append(single_total)
                table_data.append({
                    "日期": record.date, "貨櫃號碼": record.container_id,
                    "路線": f"{record.point_of_origin} → {record.billing_region}",
                    "車號": record.truck_number, "貨主": record.cargo_owner,
                    "基本運費": record.basic_freight, "特殊加給": record.subsidy_total,
                    "單趟總額": single_total, "備註": record.remarks,
                })

            table_data = sorted(table_data, key=lambda x: x["日期"])
            salary_report = calculate_monthly_salary(trip_prices, full_attendance, safety_bonus, other_add, labor_health, phone_sub, other_deduct)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("跑車趟次", f"{len(records)} 趟")
            m2.metric("月趟次總額", money(salary_report["月趟次總額"]))
            m3.metric("出車加給", "+" + money(salary_report["6%出車加給"]))
            m4.metric("安全獎金", "+" + money(safety_bonus))

            section_title("派車明細")
            # 呼叫 tables.py 內的 UI 元件
            render_dispatch_table(table_data)

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            # 呼叫 cards.py 內的 UI 元件
            render_payroll_card(salary_report["實領薪資"], real_query_driver, query_month)


# --- 模組 3：基本資料設定 ---
def render_settings_form():
    tab_driver, tab_truck, tab_region = st.tabs(["司機名冊", "車輛管理", "地區費率"])

    with tab_driver:
        col1, col2 = st.columns([0.85, 1.5], gap="large")
        with col1:
            with st.container(border=True):
                st.markdown("### 新增司機")
                new_d_id = st.text_input("司機代號", placeholder="例如：001", key="settings_driver_id")
                new_d_name = st.text_input("司機姓名", placeholder="例如：王小明", key="settings_driver_name")
                if st.button("新增司機", use_container_width=True, type="primary", key="add_driver_btn"):
                    if st.session_state["role"] == "訪客":
                        st.warning("系統提示：訪客模式無法修改正式資料。")
                    elif new_d_id and new_d_name:
                        if add_driver(new_d_id, new_d_name):
                            st.success(f"[系統提示] 已新增司機 {new_d_id}")
                            st.rerun()
                    else:
                        st.error("請完整填寫司機代號與姓名。")
        with col2:
            with st.container(border=True):
                st.markdown("### 現有司機")
                drivers = get_all_drivers()
                render_driver_table(drivers)

    with tab_truck:
        col1, col2 = st.columns([0.85, 1.5], gap="large")
        with col1:
            with st.container(border=True):
                st.markdown("### 新增車輛")
                new_t_num = st.text_input("車號", placeholder="例如：AA-1234", key="settings_truck_number")
                new_t_size = st.radio("車型", ["20呎", "40呎"], horizontal=True, key="settings_truck_size")
                if st.button("新增車輛", use_container_width=True, type="primary", key="add_truck_btn"):
                    if st.session_state["role"] == "訪客":
                        st.warning("系統提示：訪客模式無法修改正式資料。")
                    elif new_t_num:
                        if add_truck(new_t_num, new_t_size):
                            st.success(f"[系統提示] 已新增車輛 {new_t_num}")
                            st.rerun()
                    else:
                        st.error("請輸入車號。")
        with col2:
            with st.container(border=True):
                st.markdown("### 現有車輛")
                trucks = get_all_trucks()
                render_truck_table(trucks)

    with tab_region:
        with st.container(border=True):
            st.markdown("### 地區計價規則")
            st.caption("新增或更新各計價區域的基本運費。")
            c1, c2, c3 = st.columns([1.3, 0.8, 0.7])
            with c1:
                region_name = st.text_input("地區名稱", placeholder="例如：五股", key="settings_region_name")
            with c2:
                region_price = st.number_input("基本運費", min_value=0, value=900, step=50, key="settings_region_price")
            with c3:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                save_price = st.button("儲存費率", use_container_width=True, type="primary", key="save_price_btn")
            
            if save_price:
                if st.session_state["role"] == "訪客":
                    st.warning("系統提示：訪客模式無法修改正式資料。")
                elif not region_name:
                    st.error("請輸入地區名稱。")
                else:
                    if update_or_add_price_rule(region_name, region_price):
                        st.success("[系統提示] 地區費率已更新。")
                        st.rerun()
            
            rules = get_all_price_rules()
            render_price_rule_table(rules)