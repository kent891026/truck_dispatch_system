
# app.py (整合最終版：內嵌所有資料庫管家，絕不發生匯入錯誤)
import streamlit as st
import datetime
import pandas as pd
import auth
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. 網頁基礎設定
st.set_page_config(page_title="派車管理系統", page_icon="🚚", layout="wide")

# ==========================================
# 資料庫藍圖與管家直接宣告 (避免跨檔案匯入失敗)
# ==========================================
Base = declarative_base()

class DriverModel(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

class TruckModel(Base):
    __tablename__ = 'trucks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_number = Column(String(50), unique=True, nullable=False)
    size = Column(String(20), nullable=False)

class PriceRuleModel(Base):
    __tablename__ = 'price_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    region_name = Column(String(100), unique=True, nullable=False)
    base_price = Column(Integer, nullable=False)

class DispatchOrderModel(Base):
    __tablename__ = 'dispatch_orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String(50), nullable=False)
    date = Column(String(10), nullable=False) 
    container_id = Column(String(50), nullable=False)
    truck_number = Column(String(50), nullable=False)
    cargo_owner = Column(String(100), nullable=False)
    point_of_origin = Column(String(100), nullable=False)
    destination_address = Column(String(200), nullable=False)
    billing_region = Column(String(100), nullable=False)
    is_return_trip = Column(Boolean, default=False)
    has_weighting = Column(Boolean, default=False)
    has_danger_tag = Column(Boolean, default=False)
    has_instrument_inspection = Column(Boolean, default=False)
    has_freezing_plate = Column(Boolean, default=False)
    is_night_shift = Column(Boolean, default=False)
    is_holiday = Column(Boolean, default=False)
    early_shift_type = Column(String(20), nullable=True)
    unloading_overtime_hours = Column(Integer, default=0)
    basic_freight = Column(Integer, default=0)
    subsidy_total = Column(Integer, default=0)
    remarks = Column(String(500), nullable=True)

engine = create_engine('sqlite:///test_truck.db', echo=False) 
Base.metadata.create_all(bind=engine)  
SessionLocal = sessionmaker(bind=engine)

# 資料庫操作函式
def create_or_update_dispatch_order(dispatch_order: DispatchOrderModel) -> bool:
    session = SessionLocal()
    try:
        existing_order = session.query(DispatchOrderModel).filter(
            DispatchOrderModel.date == dispatch_order.date,
            DispatchOrderModel.driver_id == dispatch_order.driver_id,
            DispatchOrderModel.container_id == dispatch_order.container_id
        ).first() 
        if existing_order:
            existing_order.point_of_origin = dispatch_order.point_of_origin
            existing_order.destination_address = dispatch_order.destination_address
            existing_order.truck_number = dispatch_order.truck_number
            existing_order.cargo_owner = dispatch_order.cargo_owner
            existing_order.billing_region = dispatch_order.billing_region
            existing_order.is_return_trip = dispatch_order.is_return_trip
            existing_order.has_weighting = dispatch_order.has_weighting
            existing_order.has_danger_tag = dispatch_order.has_danger_tag
            existing_order.has_instrument_inspection = dispatch_order.has_instrument_inspection
            existing_order.has_freezing_plate = dispatch_order.has_freezing_plate
            existing_order.is_night_shift = dispatch_order.is_night_shift
            existing_order.is_holiday = dispatch_order.is_holiday
            existing_order.early_shift_type = dispatch_order.early_shift_type
            existing_order.unloading_overtime_hours = dispatch_order.unloading_overtime_hours
            existing_order.basic_freight = dispatch_order.basic_freight
            existing_order.subsidy_total = dispatch_order.subsidy_total
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            old_remarks = existing_order.remarks if existing_order.remarks else ""
            new_remarks_input = dispatch_order.remarks if dispatch_order.remarks else ""
            existing_order.remarks = f"{old_remarks} ➔ 更新為: {new_remarks_input} [系統紀錄: 於 {current_time} 覆寫]"
            session.commit()
        else:
            session.add(dispatch_order)
            session.commit()
        return True
    except Exception as e:
        session.rollback() 
        return False
    finally:
        session.close()

def get_order_by_driver_and_month(driver_id: str, year_month: str):
    session = SessionLocal()
    try:
        return session.query(DispatchOrderModel).filter(
            DispatchOrderModel.driver_id == driver_id, 
            DispatchOrderModel.date.startswith(year_month)
        ).all()
    except:
        return [] 
    finally:
        session.close()

def get_all_drivers():
    session = SessionLocal()
    try:
        return session.query(DriverModel).all()
    finally:
        session.close()

def add_driver(driver_id: str, name: str):
    session = SessionLocal()
    try:
        new_driver = DriverModel(driver_id=driver_id, name=name, is_active=True)
        session.add(new_driver)
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

def get_all_trucks():
    session = SessionLocal()
    try:
        return session.query(TruckModel).all()
    finally:
        session.close()

def add_truck(truck_number: str, size: str):
    session = SessionLocal()
    try:
        new_truck = TruckModel(truck_number=truck_number, size=size)
        session.add(new_truck)
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

def get_all_price_rules():
    session = SessionLocal()
    try:
        return session.query(PriceRuleModel).all()
    finally:
        session.close()

def update_or_add_price_rule(region_name: str, base_price: int):
    session = SessionLocal()
    try:
        rule = session.query(PriceRuleModel).filter(PriceRuleModel.region_name == region_name).first()
        if rule:
            rule.base_price = base_price
        else:
            session.add(PriceRuleModel(region_name=region_name, base_price=base_price))
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

# 匯入計價大腦
from calculator import calculate_single_trip, calculate_monthly_salary, DESTINATION_PRICES

# ==========================================
# 登入狀態初始化
# ==========================================
# 初始化登入狀態
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None

# 判斷是否登入
if not st.session_state["logged_in"]:
    auth.render_login_page()
else:
    # 呼叫 auth 裡的側邊選單，並取得目前選中的頁面
    selected_page = auth.render_sidebar_logout()

    if selected_page == "📝 每日派車單輸入":
        st.markdown("<h2 style='text-align: center; color: #2C3E50;'>📝 填寫每日派車單</h2><hr>", unsafe_allow_html=True)
        
        drivers_db = get_all_drivers()
        EXISTING_DRIVERS = [f"{d.driver_id} ({d.name})" for d in drivers_db] if drivers_db else ["0599 (AAA)", "1099 (BBB)"]
        EXISTING_DRIVERS.append("新增司機...")
        
        # 完整車輛清單與尺寸
        RAW_TRUCKS = [
            "2L-22 (XXX) (20呎)", "39-J6 (206) (20呎)", "M4-41 (207) (20呎)", 
            "07-J6 (208) (20呎)", "82-PJ (209) (20呎)", 
            "22-H5 (309) (40呎)", "FC-S2 (310) (40呎)", "62-AJ (311) (40呎)", 
            "FE-B9 (312) (40呎)", "9H-40 (315) (40呎)", "DJ-91 (316) (40呎)", 
            "65-J5 (318) (40呎)", "HD-763 (319) (40呎)"
        ]
        EXISTING_REGIONS = list(DESTINATION_PRICES.keys()) + ["新增地區..."]

        # === 卡片 1：司機與車輛配置 (帶有 20/40 呎快速篩選) ===
        st.markdown("#### 👤 司機與車輛配置")
        with st.container(border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("司機代號 <span style='color:red'>*</span>", unsafe_allow_html=True)
                selected_driver = st.selectbox("司機代號", EXISTING_DRIVERS, label_visibility="collapsed")
                if selected_driver == "新增司機...":
                    st.markdown("請輸入新司機代號 <span style='color:red'>*</span>", unsafe_allow_html=True)
                    real_driver = st.text_input("新司機代號", key="new_driver", label_visibility="collapsed")
                else:
                    real_driver = selected_driver.split(" ")[0]
                    
                st.markdown("出車日期 <span style='color:red'>*</span>", unsafe_allow_html=True)
                date = st.date_input("出車日期", label_visibility="collapsed") 
                is_return_trip = st.checkbox("🔄 這是一組來回車趟 (A>B>A)")
                
            with col2:
                st.markdown("出勤車號 (含尺寸) <span style='color:red'>*</span>", unsafe_allow_html=True)
                # 🌟 找回車號尺寸快速篩選按鈕
                truck_filter = st.radio("快速篩選", ["顯示全部", "只看 20呎", "只看 40呎"], horizontal=True, label_visibility="collapsed")
                
                filtered_trucks = []
                for truck in RAW_TRUCKS:
                    if truck_filter == "顯示全部": filtered_trucks.append(truck)
                    elif truck_filter == "只看 20呎" and "20呎" in truck: filtered_trucks.append(truck)
                    elif truck_filter == "只看 40呎" and "40呎" in truck: filtered_trucks.append(truck)
                filtered_trucks.append("新增車輛...")
                
                selected_truck = st.selectbox("出勤車號", filtered_trucks, label_visibility="collapsed")
                
                if selected_truck == "新增車輛...":
                    st.markdown("請輸入新車號 <span style='color:red'>*</span>", unsafe_allow_html=True)
                    new_truck_num = st.text_input("新車號", key="new_truck", label_visibility="collapsed")
                    new_truck_size = st.radio("請選擇車型", ["20呎", "40呎"], horizontal=True)
                    real_truck = f"{new_truck_num} ({new_truck_size})" if new_truck_num else ""
                else:
                    real_truck = selected_truck
                    
                st.markdown("貨櫃櫃號 <span style='color:red'>*</span>", unsafe_allow_html=True)
                raw_container_id = st.text_input("貨櫃櫃號", placeholder="例如：TGHU1234567", label_visibility="collapsed")

        # === 卡片 2：運送路線資訊 (帶有北中南地區快選) ===
        st.markdown("#### 📍 運送路線資訊")
        with st.container(border=True):
            col3, col4 = st.columns(2)
            with col3:
                st.markdown("起運點 (公司名) <span style='color:red'>*</span>", unsafe_allow_html=True)
                point_of_origin = st.text_input("起運點", placeholder="例如：某海運公司", label_visibility="collapsed")
                cargo_owner = st.text_input("貨主名稱 (非必填)", placeholder="例如：貨主名稱")
                
            with col4:
                destination_address = st.text_input("下貨地址 (非必填)", placeholder="例如：新北市五股區...")
                st.markdown("計價地區 (用於計算薪資) <span style='color:red'>*</span>", unsafe_allow_html=True)
                
                # 🌟 找回地區北中南分區快選按鈕
                region_filter = st.radio("地區篩選", ["顯示全部", "北部 (北北基桃竹宜)", "中部 (苗中彰投雲)", "南部 (嘉南高屏)"], horizontal=True, label_visibility="collapsed")
                CENTRAL_KWS = ["苗栗", "通霄", "後龍", "三義", "后里", "台中", "彰化", "員林", "南投", "雲林", "斗六", "斗南"]
                SOUTH_KWS = ["嘉義", "台南", "高雄", "屏東"]
                
                filtered_regions = []
                for r in EXISTING_REGIONS[:-1]: 
                    is_south = any(kw in r for kw in SOUTH_KWS)
                    is_central = any(kw in r for kw in CENTRAL_KWS)
                    is_north = not is_south and not is_central 
                    
                    if region_filter == "顯示全部": filtered_regions.append(r)
                    elif "北部" in region_filter and is_north: filtered_regions.append(r)
                    elif "中部" in region_filter and is_central: filtered_regions.append(r)
                    elif "南部" in region_filter and is_south: filtered_regions.append(r)
                        
                filtered_regions.append("新增地區...")
                selected_region = st.selectbox("計價地區", filtered_regions, label_visibility="collapsed")
                
                if selected_region == "新增地區...":
                    st.markdown("請輸入新計價地區 <span style='color:red'>*</span>", unsafe_allow_html=True)
                    real_region = st.text_input("新計價地區", key="new_region", label_visibility="collapsed")
                else:
                    real_region = selected_region
                    
        st.markdown("#### 💰 特殊加給與備註")
        with st.container(border=True):
            col5, col6 = st.columns(2)
            with col5:
                has_freezing_plate = st.checkbox("❄️ 冷凍板 (+300元)")
                has_weighting = st.checkbox("⚖️ 異地過磅 (+100元)")
                has_danger_tag = st.checkbox("⚠️ 危險標誌 (+100元)")
                has_instrument_inspection = st.checkbox("🔍 儀器檢查 (+100元)")
            with col6:
                is_night_shift = st.checkbox("🌙 夜間出車 (+1000元)")
                is_holiday = st.checkbox("🏖️ 假日出車 (+1000元)")
                early_shift_option = st.selectbox("🌅 早車時段", ["無", "03:00 (+200元)", "05:00 (+100元)"])
                early_shift_type = "03:00" if "03:00" in early_shift_option else "05:00" if "05:00" in early_shift_option else None
                unloading_overtime_hours = st.number_input("⏱️ 卸貨超時 (小時)", min_value=0, max_value=24, value=0)
                
            auto_tags = []
            if has_freezing_plate: auto_tags.append("冷凍板")
            if has_weighting: auto_tags.append("過磅")
            if has_danger_tag: auto_tags.append("危標")
            if has_instrument_inspection: auto_tags.append("儀檢")
            if is_night_shift: auto_tags.append("夜間")
            if is_holiday: auto_tags.append("假日")
            if early_shift_type: auto_tags.append(f"早車{early_shift_type}")
            if unloading_overtime_hours > 0: auto_tags.append(f"超時{unloading_overtime_hours}hr")
            
            auto_text = f"[系統標記: {', '.join(auto_tags)}]" if auto_tags else ""
            if auto_text:
                st.info(f"🔒 **自動鎖定備註：** {auto_text}")
            remarks = st.text_area("備註說明 (選填)")

        submitted = st.button("🚀 送出並儲存派車單", use_container_width=True)
        if submitted:
            clean_id = raw_container_id.replace(" ", "").replace("-", "").upper()
            if len(clean_id) != 11:
                st.error("❌ 櫃號格式需為 11 碼！")
            elif not real_driver or not real_truck or not point_of_origin or not real_region:
                st.error("❌ 必填欄位未填寫！")
            else:
                formatted_container_id = f"{clean_id[:4]} {clean_id[4:]}"
                final_remarks = f"{remarks} {auto_text}".strip() if auto_text else remarks
                fees = calculate_single_trip(real_region, has_freezing_plate, has_weighting, has_danger_tag, has_instrument_inspection, is_night_shift, is_holiday, early_shift_type, unloading_overtime_hours)
                
                new_order = DispatchOrderModel(
                    driver_id=real_driver, date=date.strftime("%Y-%m-%d"), container_id=formatted_container_id,
                    point_of_origin=point_of_origin, destination_address=destination_address or "未填寫", 
                    truck_number=real_truck, cargo_owner=cargo_owner or "未填寫", billing_region=real_region,
                    is_return_trip=is_return_trip, has_weighting=has_weighting, has_danger_tag=has_danger_tag,
                    has_instrument_inspection=has_instrument_inspection, has_freezing_plate=has_freezing_plate,
                    is_night_shift=is_night_shift, is_holiday=is_holiday, early_shift_type=early_shift_type,
                    unloading_overtime_hours=unloading_overtime_hours, basic_freight=fees["basic_freight"],
                    subsidy_total=fees["subsidy_total"], remarks=final_remarks
                )
                if create_or_update_dispatch_order(new_order):
                    st.success(f"✅ 成功！司機 {real_driver} 派車單已儲存。總計 ${fees['total_price']}")

    elif selected_page == "📊 月底結算台":
        st.markdown("<h2 style='text-align: center; color: #2C3E50;'>📊 月底薪資結算台</h2><hr>", unsafe_allow_html=True)
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                drivers_db = get_all_drivers()
                EXISTING_DRIVERS = [f"{d.driver_id} ({d.name})" for d in drivers_db] if drivers_db else ["0599 (AAA)"]
                query_driver = st.selectbox("👨‍✈️ 選擇結算司機", EXISTING_DRIVERS)
                real_query_driver = query_driver.split(" ")[0] if " (" in query_driver else query_driver
            with col2:
                current_ym = datetime.date.today().strftime("%Y-%m")
                query_month = st.text_input("📅 選擇結算月份 (YYYY-MM)", value=current_ym)

        with st.container(border=True):
            col3, col4, col5 = st.columns(3)
            with col3:
                full_attendance = st.number_input("全勤獎金 (+)", value=3000, step=500)
                safety_check = st.checkbox("✅ 本月達標安全獎金")
                safety_bonus = 15000 if safety_check else 0
            with col4:
                labor_health = st.number_input("勞健保扣款 (-)", value=5000, step=500)
                phone_sub = st.number_input("電話費補助 (+)", value=700, step=100)
            with col5:
                other_add = st.number_input("其他額外補貼 (+)", value=0, step=100)
                other_deduct = st.number_input("其他扣款 (-)", value=0, step=100)

        if st.button("🧾 開始結算並產出報表", use_container_width=True, type="primary"):
            records = get_order_by_driver_and_month(real_query_driver, query_month)
            if not records:
                st.warning(f"⚠️ 找不到司機 {real_query_driver} 在 {query_month} 的派車紀錄！")
            else:
                st.success(f"✅ 成功撈取 {len(records)} 筆派車單！")
                table_data, trip_prices_array = [], []
                for r in records:
                    single_total = r.basic_freight + r.subsidy_total
                    trip_prices_array.append(single_total)
                    table_data.append({
                        "日期": r.date, "貨櫃號碼": r.container_id,
                        "路線軌跡": f"{r.point_of_origin} ➔ {r.billing_region}",
                        "車號 / 板號": r.truck_number, "貨主": r.cargo_owner,
                        "基本運費": r.basic_freight, "各項補貼": r.subsidy_total,
                        "單趟總計": single_total, "備註說明": r.remarks
                    })
                table_data = sorted(table_data, key=lambda x: x["日期"])
                salary_report = calculate_monthly_salary(
                    trip_prices_array, full_attendance, safety_bonus, other_add, labor_health, phone_sub, other_deduct
                )
                st.markdown(f"### 📋 司機 `{real_query_driver}` ｜ {query_month} 薪資核對總表")
                st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True, column_config={
                    "基本運費": st.column_config.NumberColumn(format="$%d"),
                    "各項補貼": st.column_config.NumberColumn(format="$%d"),
                    "單趟總計": st.column_config.NumberColumn(format="$%d"),
                })
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("總跑車趟次", f"{len(records)} 趟")
                m2.metric("趟次薪資總額", f"${salary_report['月趟次總額']:,}")
                m3.metric("6% 出車加給", f"+${salary_report['6%出車加給']:,}")
                m4.metric("浮動加減項總計", f"${(full_attendance + safety_bonus + phone_sub + other_add - labor_health - other_deduct):,}")
                st.markdown("---")
                st.markdown(f"<div style='background-color: #F8F9F9; padding: 20px; border-radius: 10px; border-left: 5px solid #E74C3C;'><h3 style='margin: 0; color: #2C3E50; text-align: right;'>👑 本月最終實領總薪資： <span style='color: #E74C3C;'>${salary_report['實領薪資']:,} 元</span></h3></div>", unsafe_allow_html=True)

    elif selected_page == "⚙️ 基本資料與費率設定":
        st.markdown("<h2 style='text-align: center; color: #2C3E50;'>⚙️ 系統基本資料與費率設定</h2><hr>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["👨‍✈️ 司機名冊管理", "🚚 車輛與尺寸管理", "💰 地區運費標準設定"])
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.markdown("#### ➕ 新增司機")
                    new_d_id = st.text_input("司機代號")
                    new_d_name = st.text_input("司機姓名")
                    if st.button("確認新增司機", use_container_width=True):
                        if new_d_id and new_d_name and add_driver(new_d_id, new_d_name):
                            st.success(f"✅ 成功新增：{new_d_id}")
                            st.rerun()
                        else:
                            st.error("❌ 新增失敗")
            with col2:
                with st.container(border=True):
                    st.markdown("#### 📋 現有司機")
                    drivers = get_all_drivers()
                    if drivers:
                        st.dataframe(pd.DataFrame([{"代號": d.driver_id, "姓名": d.name} for d in drivers]), use_container_width=True, hide_index=True)
        with tab2:
            col3, col4 = st.columns(2)
            with col3:
                with st.container(border=True):
                    st.markdown("#### ➕ 新增車輛")
                    new_t_num = st.text_input("車號")
                    new_t_size = st.radio("尺寸", ["20呎", "40呎"], horizontal=True)
                    if st.button("確認新增車輛", use_container_width=True):
                        if new_t_num and add_truck(new_t_num, new_t_size):
                            st.success(f"✅ 成功新增車號：{new_t_num}")
                            st.rerun()
            with col4:
                with st.container(border=True):
                    st.markdown("#### 📋 現有車輛")
                    trucks = get_all_trucks()
                    if trucks:
                        st.dataframe(pd.DataFrame([{"車號": t.truck_number, "尺寸": t.size} for t in trucks]), use_container_width=True, hide_index=True)
        with tab3:
            with st.container(border=True):
                c5, c6, c7 = st.columns(3)
                r_name = c5.text_input("地區名稱")
                r_price = c6.number_input("基礎運費", value=900, step=50)
                if c7.button("💾 儲存費率", use_container_width=True) and r_name:
                    update_or_add_price_rule(r_name, r_price)
                    st.success("✅ 費率更新成功！")
                    st.rerun()
                rules = get_all_price_rules()
                if rules:
=======
# app.py (整合最終版：內嵌所有資料庫管家，絕不發生匯入錯誤)
import streamlit as st
import datetime
import pandas as pd
import auth
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. 網頁基礎設定
st.set_page_config(page_title="派車管理系統", page_icon="🚚", layout="wide")

# ==========================================
# 資料庫藍圖與管家直接宣告 (避免跨檔案匯入失敗)
# ==========================================
Base = declarative_base()

class DriverModel(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

class TruckModel(Base):
    __tablename__ = 'trucks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_number = Column(String(50), unique=True, nullable=False)
    size = Column(String(20), nullable=False)

class PriceRuleModel(Base):
    __tablename__ = 'price_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    region_name = Column(String(100), unique=True, nullable=False)
    base_price = Column(Integer, nullable=False)

class DispatchOrderModel(Base):
    __tablename__ = 'dispatch_orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String(50), nullable=False)
    date = Column(String(10), nullable=False) 
    container_id = Column(String(50), nullable=False)
    truck_number = Column(String(50), nullable=False)
    cargo_owner = Column(String(100), nullable=False)
    point_of_origin = Column(String(100), nullable=False)
    destination_address = Column(String(200), nullable=False)
    billing_region = Column(String(100), nullable=False)
    is_return_trip = Column(Boolean, default=False)
    has_weighting = Column(Boolean, default=False)
    has_danger_tag = Column(Boolean, default=False)
    has_instrument_inspection = Column(Boolean, default=False)
    has_freezing_plate = Column(Boolean, default=False)
    is_night_shift = Column(Boolean, default=False)
    is_holiday = Column(Boolean, default=False)
    early_shift_type = Column(String(20), nullable=True)
    unloading_overtime_hours = Column(Integer, default=0)
    basic_freight = Column(Integer, default=0)
    subsidy_total = Column(Integer, default=0)
    remarks = Column(String(500), nullable=True)

engine = create_engine('sqlite:///test_truck.db', echo=False) 
Base.metadata.create_all(bind=engine)  
SessionLocal = sessionmaker(bind=engine)

# 資料庫操作函式
def create_or_update_dispatch_order(dispatch_order: DispatchOrderModel) -> bool:
    session = SessionLocal()
    try:
        existing_order = session.query(DispatchOrderModel).filter(
            DispatchOrderModel.date == dispatch_order.date,
            DispatchOrderModel.driver_id == dispatch_order.driver_id,
            DispatchOrderModel.container_id == dispatch_order.container_id
        ).first() 
        if existing_order:
            existing_order.point_of_origin = dispatch_order.point_of_origin
            existing_order.destination_address = dispatch_order.destination_address
            existing_order.truck_number = dispatch_order.truck_number
            existing_order.cargo_owner = dispatch_order.cargo_owner
            existing_order.billing_region = dispatch_order.billing_region
            existing_order.is_return_trip = dispatch_order.is_return_trip
            existing_order.has_weighting = dispatch_order.has_weighting
            existing_order.has_danger_tag = dispatch_order.has_danger_tag
            existing_order.has_instrument_inspection = dispatch_order.has_instrument_inspection
            existing_order.has_freezing_plate = dispatch_order.has_freezing_plate
            existing_order.is_night_shift = dispatch_order.is_night_shift
            existing_order.is_holiday = dispatch_order.is_holiday
            existing_order.early_shift_type = dispatch_order.early_shift_type
            existing_order.unloading_overtime_hours = dispatch_order.unloading_overtime_hours
            existing_order.basic_freight = dispatch_order.basic_freight
            existing_order.subsidy_total = dispatch_order.subsidy_total
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            old_remarks = existing_order.remarks if existing_order.remarks else ""
            new_remarks_input = dispatch_order.remarks if dispatch_order.remarks else ""
            existing_order.remarks = f"{old_remarks} ➔ 更新為: {new_remarks_input} [系統紀錄: 於 {current_time} 覆寫]"
            session.commit()
        else:
            session.add(dispatch_order)
            session.commit()
        return True
    except Exception as e:
        session.rollback() 
        return False
    finally:
        session.close()

def get_order_by_driver_and_month(driver_id: str, year_month: str):
    session = SessionLocal()
    try:
        return session.query(DispatchOrderModel).filter(
            DispatchOrderModel.driver_id == driver_id, 
            DispatchOrderModel.date.startswith(year_month)
        ).all()
    except:
        return [] 
    finally:
        session.close()

def get_all_drivers():
    session = SessionLocal()
    try:
        return session.query(DriverModel).all()
    finally:
        session.close()

def add_driver(driver_id: str, name: str):
    session = SessionLocal()
    try:
        new_driver = DriverModel(driver_id=driver_id, name=name, is_active=True)
        session.add(new_driver)
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

def get_all_trucks():
    session = SessionLocal()
    try:
        return session.query(TruckModel).all()
    finally:
        session.close()

def add_truck(truck_number: str, size: str):
    session = SessionLocal()
    try:
        new_truck = TruckModel(truck_number=truck_number, size=size)
        session.add(new_truck)
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

def get_all_price_rules():
    session = SessionLocal()
    try:
        return session.query(PriceRuleModel).all()
    finally:
        session.close()

def update_or_add_price_rule(region_name: str, base_price: int):
    session = SessionLocal()
    try:
        rule = session.query(PriceRuleModel).filter(PriceRuleModel.region_name == region_name).first()
        if rule:
            rule.base_price = base_price
        else:
            session.add(PriceRuleModel(region_name=region_name, base_price=base_price))
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

# 匯入計價大腦
from calculator import calculate_single_trip, calculate_monthly_salary, DESTINATION_PRICES

# ==========================================
# 登入狀態初始化
# ==========================================
# 初始化登入狀態
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None

# 判斷是否登入
if not st.session_state["logged_in"]:
    auth.render_login_page()
else:
    # 呼叫 auth 裡的側邊選單，並取得目前選中的頁面
    selected_page = auth.render_sidebar_logout()

    if selected_page == "📝 每日派車單輸入":
        st.markdown("<h2 style='text-align: center; color: #2C3E50;'>📝 填寫每日派車單</h2><hr>", unsafe_allow_html=True)
        
        drivers_db = get_all_drivers()
        EXISTING_DRIVERS = [f"{d.driver_id} ({d.name})" for d in drivers_db] if drivers_db else ["0599 (AAA)", "1099 (BBB)"]
        EXISTING_DRIVERS.append("新增司機...")
        
        RAW_TRUCKS = ["2L-22 (20呎)", "39-J6 (20呎)", "22-H5 (40呎)", "FC-S2 (40呎)", "新增車輛..."]
        EXISTING_REGIONS = list(DESTINATION_PRICES.keys()) + ["新增地區..."]

        st.markdown("#### 👤 司機與車輛配置")
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("司機代號 <span style='color:red'>*</span>", unsafe_allow_html=True)
                selected_driver = st.selectbox("司機代號", EXISTING_DRIVERS, label_visibility="collapsed")
                if selected_driver == "新增司機...":
                    real_driver = st.text_input("新司機代號", key="new_driver")
                else:
                    real_driver = selected_driver.split(" ")[0]
                    
                st.markdown("出車日期 <span style='color:red'>*</span>", unsafe_allow_html=True)
                date = st.date_input("出車日期", label_visibility="collapsed") 
                is_return_trip = st.checkbox("🔄 這是一組來回車趟 (A>B>A)")
                
            with col2:
                st.markdown("出勤車號 <span style='color:red'>*</span>", unsafe_allow_html=True)
                selected_truck = st.selectbox("出勤車號", RAW_TRUCKS, label_visibility="collapsed")
                if selected_truck == "新增車輛...":
                    new_t = st.text_input("新車號", key="new_t")
                    new_sz = st.radio("車型", ["20呎", "40呎"], horizontal=True)
                    real_truck = f"{new_t} ({new_sz})" if new_t else ""
                else:
                    real_truck = selected_truck
                    
                st.markdown("貨櫃櫃號 <span style='color:red'>*</span>", unsafe_allow_html=True)
                raw_container_id = st.text_input("貨櫃櫃號", placeholder="例如：TGHU1234567", label_visibility="collapsed")

        st.markdown("#### 📍 運送路線資訊")
        with st.container(border=True):
            col3, col4 = st.columns(2)
            with col3:
                st.markdown("起運點 (公司名) <span style='color:red'>*</span>", unsafe_allow_html=True)
                point_of_origin = st.text_input("起運點", placeholder="例如：某海運公司", label_visibility="collapsed")
                cargo_owner = st.text_input("貨主名稱 (非必填)", placeholder="例如：貨主名稱")
            with col4:
                destination_address = st.text_input("下貨地址 (非必填)", placeholder="例如：新北市五股區...")
                st.markdown("計價地區 <span style='color:red'>*</span>", unsafe_allow_html=True)
                selected_region = st.selectbox("計價地區", EXISTING_REGIONS, label_visibility="collapsed")
                real_region = st.text_input("新計價地區") if selected_region == "新增地區..." else selected_region

        st.markdown("#### 💰 特殊加給與備註")
        with st.container(border=True):
            col5, col6 = st.columns(2)
            with col5:
                has_freezing_plate = st.checkbox("❄️ 冷凍板 (+300元)")
                has_weighting = st.checkbox("⚖️ 異地過磅 (+100元)")
                has_danger_tag = st.checkbox("⚠️ 危險標誌 (+100元)")
                has_instrument_inspection = st.checkbox("🔍 儀器檢查 (+100元)")
            with col6:
                is_night_shift = st.checkbox("🌙 夜間出車 (+1000元)")
                is_holiday = st.checkbox("🏖️ 假日出車 (+1000元)")
                early_shift_option = st.selectbox("🌅 早車時段", ["無", "03:00 (+200元)", "05:00 (+100元)"])
                early_shift_type = "03:00" if "03:00" in early_shift_option else "05:00" if "05:00" in early_shift_option else None
                unloading_overtime_hours = st.number_input("⏱️ 卸貨超時 (小時)", min_value=0, max_value=24, value=0)
                
            auto_tags = []
            if has_freezing_plate: auto_tags.append("冷凍板")
            if has_weighting: auto_tags.append("過磅")
            if has_danger_tag: auto_tags.append("危標")
            if has_instrument_inspection: auto_tags.append("儀檢")
            if is_night_shift: auto_tags.append("夜間")
            if is_holiday: auto_tags.append("假日")
            if early_shift_type: auto_tags.append(f"早車{early_shift_type}")
            if unloading_overtime_hours > 0: auto_tags.append(f"超時{unloading_overtime_hours}hr")
            
            auto_text = f"[系統標記: {', '.join(auto_tags)}]" if auto_tags else ""
            if auto_text:
                st.info(f"🔒 **自動鎖定備註：** {auto_text}")
            remarks = st.text_area("備註說明 (選填)")

        submitted = st.button("🚀 送出並儲存派車單", use_container_width=True)
        if submitted:
            clean_id = raw_container_id.replace(" ", "").replace("-", "").upper()
            if len(clean_id) != 11:
                st.error("❌ 櫃號格式需為 11 碼！")
            elif not real_driver or not real_truck or not point_of_origin or not real_region:
                st.error("❌ 必填欄位未填寫！")
            else:
                formatted_container_id = f"{clean_id[:4]} {clean_id[4:]}"
                final_remarks = f"{remarks} {auto_text}".strip() if auto_text else remarks
                fees = calculate_single_trip(real_region, has_freezing_plate, has_weighting, has_danger_tag, has_instrument_inspection, is_night_shift, is_holiday, early_shift_type, unloading_overtime_hours)
                
                new_order = DispatchOrderModel(
                    driver_id=real_driver, date=date.strftime("%Y-%m-%d"), container_id=formatted_container_id,
                    point_of_origin=point_of_origin, destination_address=destination_address or "未填寫", 
                    truck_number=real_truck, cargo_owner=cargo_owner or "未填寫", billing_region=real_region,
                    is_return_trip=is_return_trip, has_weighting=has_weighting, has_danger_tag=has_danger_tag,
                    has_instrument_inspection=has_instrument_inspection, has_freezing_plate=has_freezing_plate,
                    is_night_shift=is_night_shift, is_holiday=is_holiday, early_shift_type=early_shift_type,
                    unloading_overtime_hours=unloading_overtime_hours, basic_freight=fees["basic_freight"],
                    subsidy_total=fees["subsidy_total"], remarks=final_remarks
                )
                if create_or_update_dispatch_order(new_order):
                    st.success(f"✅ 成功！司機 {real_driver} 派車單已儲存。總計 ${fees['total_price']}")

    elif selected_page == "📊 月底結算台":
        st.markdown("<h2 style='text-align: center; color: #2C3E50;'>📊 月底薪資結算台</h2><hr>", unsafe_allow_html=True)
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                drivers_db = get_all_drivers()
                EXISTING_DRIVERS = [f"{d.driver_id} ({d.name})" for d in drivers_db] if drivers_db else ["0599 (AAA)"]
                query_driver = st.selectbox("👨‍✈️ 選擇結算司機", EXISTING_DRIVERS)
                real_query_driver = query_driver.split(" ")[0] if " (" in query_driver else query_driver
            with col2:
                current_ym = datetime.date.today().strftime("%Y-%m")
                query_month = st.text_input("📅 選擇結算月份 (YYYY-MM)", value=current_ym)

        with st.container(border=True):
            col3, col4, col5 = st.columns(3)
            with col3:
                full_attendance = st.number_input("全勤獎金 (+)", value=3000, step=500)
                safety_check = st.checkbox("✅ 本月達標安全獎金")
                safety_bonus = 15000 if safety_check else 0
            with col4:
                labor_health = st.number_input("勞健保扣款 (-)", value=5000, step=500)
                phone_sub = st.number_input("電話費補助 (+)", value=700, step=100)
            with col5:
                other_add = st.number_input("其他額外補貼 (+)", value=0, step=100)
                other_deduct = st.number_input("其他扣款 (-)", value=0, step=100)

        if st.button("🧾 開始結算並產出報表", use_container_width=True, type="primary"):
            records = get_order_by_driver_and_month(real_query_driver, query_month)
            if not records:
                st.warning(f"⚠️ 找不到司機 {real_query_driver} 在 {query_month} 的派車紀錄！")
            else:
                st.success(f"✅ 成功撈取 {len(records)} 筆派車單！")
                table_data, trip_prices_array = [], []
                for r in records:
                    single_total = r.basic_freight + r.subsidy_total
                    trip_prices_array.append(single_total)
                    table_data.append({
                        "日期": r.date, "貨櫃號碼": r.container_id,
                        "路線軌跡": f"{r.point_of_origin} ➔ {r.billing_region}",
                        "車號 / 板號": r.truck_number, "貨主": r.cargo_owner,
                        "基本運費": r.basic_freight, "各項補貼": r.subsidy_total,
                        "單趟總計": single_total, "備註說明": r.remarks
                    })
                table_data = sorted(table_data, key=lambda x: x["日期"])
                salary_report = calculate_monthly_salary(
                    trip_prices_array, full_attendance, safety_bonus, other_add, labor_health, phone_sub, other_deduct
                )
                st.markdown(f"### 📋 司機 `{real_query_driver}` ｜ {query_month} 薪資核對總表")
                st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True, column_config={
                    "基本運費": st.column_config.NumberColumn(format="$%d"),
                    "各項補貼": st.column_config.NumberColumn(format="$%d"),
                    "單趟總計": st.column_config.NumberColumn(format="$%d"),
                })
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("總跑車趟次", f"{len(records)} 趟")
                m2.metric("趟次薪資總額", f"${salary_report['月趟次總額']:,}")
                m3.metric("6% 出車加給", f"+${salary_report['6%出車加給']:,}")
                m4.metric("浮動加減項總計", f"${(full_attendance + safety_bonus + phone_sub + other_add - labor_health - other_deduct):,}")
                st.markdown("---")
                st.markdown(f"<div style='background-color: #F8F9F9; padding: 20px; border-radius: 10px; border-left: 5px solid #E74C3C;'><h3 style='margin: 0; color: #2C3E50; text-align: right;'>👑 本月最終實領總薪資： <span style='color: #E74C3C;'>${salary_report['實領薪資']:,} 元</span></h3></div>", unsafe_allow_html=True)

    elif selected_page == "⚙️ 基本資料與費率設定":
        st.markdown("<h2 style='text-align: center; color: #2C3E50;'>⚙️ 系統基本資料與費率設定</h2><hr>", unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["👨‍✈️ 司機名冊管理", "🚚 車輛與尺寸管理", "💰 地區運費標準設定"])
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.markdown("#### ➕ 新增司機")
                    new_d_id = st.text_input("司機代號")
                    new_d_name = st.text_input("司機姓名")
                    if st.button("確認新增司機", use_container_width=True):
                        if new_d_id and new_d_name and add_driver(new_d_id, new_d_name):
                            st.success(f"✅ 成功新增：{new_d_id}")
                            st.rerun()
                        else:
                            st.error("❌ 新增失敗")
            with col2:
                with st.container(border=True):
                    st.markdown("#### 📋 現有司機")
                    drivers = get_all_drivers()
                    if drivers:
                        st.dataframe(pd.DataFrame([{"代號": d.driver_id, "姓名": d.name} for d in drivers]), use_container_width=True, hide_index=True)
        with tab2:
            col3, col4 = st.columns(2)
            with col3:
                with st.container(border=True):
                    st.markdown("#### ➕ 新增車輛")
                    new_t_num = st.text_input("車號")
                    new_t_size = st.radio("尺寸", ["20呎", "40呎"], horizontal=True)
                    if st.button("確認新增車輛", use_container_width=True):
                        if new_t_num and add_truck(new_t_num, new_t_size):
                            st.success(f"✅ 成功新增車號：{new_t_num}")
                            st.rerun()
            with col4:
                with st.container(border=True):
                    st.markdown("#### 📋 現有車輛")
                    trucks = get_all_trucks()
                    if trucks:
                        st.dataframe(pd.DataFrame([{"車號": t.truck_number, "尺寸": t.size} for t in trucks]), use_container_width=True, hide_index=True)
        with tab3:
            with st.container(border=True):
                c5, c6, c7 = st.columns(3)
                r_name = c5.text_input("地區名稱")
                r_price = c6.number_input("基礎運費", value=900, step=50)
                if c7.button("💾 儲存費率", use_container_width=True) and r_name:
                    update_or_add_price_rule(r_name, r_price)
                    st.success("✅ 費率更新成功！")
                    st.rerun()
                rules = get_all_price_rules()
                if rules:
                    st.dataframe(pd.DataFrame([{"地區": r.region_name, "運費": r.base_price} for r in rules]), use_container_width=True, hide_index=True)