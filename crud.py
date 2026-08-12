<<<<<<< HEAD
import datetime # 匯入時間套件，方便在備註裡加上修改時間戳記
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 把 models.py 寫好的所有藍圖完整匯入
from models import Base, DispatchOrderModel, DriverModel, TruckModel, PriceRuleModel

# 建立固定的連線設定
engine = create_engine('sqlite:///test_truck.db', echo=False) 
Base.metadata.create_all(bind=engine)  
SessionLocal = sessionmaker(bind=engine)


def create_or_update_dispatch_order(dispatch_order: DispatchOrderModel) -> bool:
    session = SessionLocal()
    try:
        existing_order = session.query(DispatchOrderModel).filter(
            DispatchOrderModel.date == dispatch_order.date,
            DispatchOrderModel.driver_id == dispatch_order.driver_id,
            DispatchOrderModel.container_id == dispatch_order.container_id
        ).first() 

        if existing_order:
            print(f"發現重複單號！準備進行資料覆寫 (司機:{dispatch_order.driver_id} / 櫃號:{dispatch_order.container_id})")
            
            existing_order.point_of_origin = dispatch_order.point_of_origin
            existing_order.destination_address = dispatch_order.destination_address
            existing_order.truck_number = dispatch_order.truck_number
            existing_order.cargo_owner = dispatch_order.cargo_owner
            existing_order.billing_region = dispatch_order.billing_region
            existing_order.is_return_trip = dispatch_order.is_return_trip
            
            # --- 加給項目更新 ---
            existing_order.has_weighting = dispatch_order.has_weighting
            existing_order.has_danger_tag = dispatch_order.has_danger_tag
            existing_order.has_instrument_inspection = dispatch_order.has_instrument_inspection
            existing_order.has_freezing_plate = dispatch_order.has_freezing_plate
            existing_order.is_night_shift = dispatch_order.is_night_shift
            existing_order.is_holiday = dispatch_order.is_holiday
            existing_order.early_shift_type = dispatch_order.early_shift_type
            existing_order.unloading_overtime_hours = dispatch_order.unloading_overtime_hours
            
            # --- 金額拆解更新 ---
            existing_order.basic_freight = dispatch_order.basic_freight
            existing_order.subsidy_total = dispatch_order.subsidy_total
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            old_remarks = existing_order.remarks if existing_order.remarks else ""
            new_remarks_input = dispatch_order.remarks if dispatch_order.remarks else ""
            existing_order.remarks = f"{old_remarks} ➔ 更新為: {new_remarks_input} [系統強制紀錄: 於 {current_time} 覆寫]"

            session.commit()
            print("資料覆寫與紀錄追加成功！")
            
        else:
            session.add(dispatch_order)
            session.commit()
            print(f"成功新增一筆派車單：{dispatch_order.date} - 司機 {dispatch_order.driver_id}")

        return True

    except Exception as e:
        session.rollback() 
        print(f"寫入/更新失敗：{e}")
        return False

    finally:
        session.close()


def get_order_by_driver_and_month(driver_id: str, year_month: str):
    session = SessionLocal()
    try:
        orders = session.query(DispatchOrderModel).filter(
            DispatchOrderModel.driver_id == driver_id, 
            DispatchOrderModel.date.startswith(year_month)
        ).all()
        return orders
    except Exception as e:
        print(f"讀取失敗：{e}")
        return [] 
    finally:
        session.close()


# --- 基本資料設定專用函式 ---

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
    except Exception as e:
        session.rollback()
        print(f"新增司機失敗: {e}")
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
    except Exception as e:
        session.rollback()
        print(f"新增車輛失敗: {e}")
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
            new_rule = PriceRuleModel(region_name=region_name, base_price=base_price)
            session.add(new_rule)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"更新費率失敗: {e}")
        return False
    finally:
=======
import datetime # 匯入時間套件，方便在備註裡加上修改時間戳記
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 把 models.py 寫好的所有藍圖完整匯入
from models import Base, DispatchOrderModel, DriverModel, TruckModel, PriceRuleModel

# 建立固定的連線設定
engine = create_engine('sqlite:///test_truck.db', echo=False) 
Base.metadata.create_all(bind=engine)  
SessionLocal = sessionmaker(bind=engine)


def create_or_update_dispatch_order(dispatch_order: DispatchOrderModel) -> bool:
    session = SessionLocal()
    try:
        existing_order = session.query(DispatchOrderModel).filter(
            DispatchOrderModel.date == dispatch_order.date,
            DispatchOrderModel.driver_id == dispatch_order.driver_id,
            DispatchOrderModel.container_id == dispatch_order.container_id
        ).first() 

        if existing_order:
            print(f"發現重複單號！準備進行資料覆寫 (司機:{dispatch_order.driver_id} / 櫃號:{dispatch_order.container_id})")
            
            existing_order.point_of_origin = dispatch_order.point_of_origin
            existing_order.destination_address = dispatch_order.destination_address
            existing_order.truck_number = dispatch_order.truck_number
            existing_order.cargo_owner = dispatch_order.cargo_owner
            existing_order.billing_region = dispatch_order.billing_region
            existing_order.is_return_trip = dispatch_order.is_return_trip
            
            # --- 加給項目更新 ---
            existing_order.has_weighting = dispatch_order.has_weighting
            existing_order.has_danger_tag = dispatch_order.has_danger_tag
            existing_order.has_instrument_inspection = dispatch_order.has_instrument_inspection
            existing_order.has_freezing_plate = dispatch_order.has_freezing_plate
            existing_order.is_night_shift = dispatch_order.is_night_shift
            existing_order.is_holiday = dispatch_order.is_holiday
            existing_order.early_shift_type = dispatch_order.early_shift_type
            existing_order.unloading_overtime_hours = dispatch_order.unloading_overtime_hours
            
            # --- 金額拆解更新 ---
            existing_order.basic_freight = dispatch_order.basic_freight
            existing_order.subsidy_total = dispatch_order.subsidy_total
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            old_remarks = existing_order.remarks if existing_order.remarks else ""
            new_remarks_input = dispatch_order.remarks if dispatch_order.remarks else ""
            existing_order.remarks = f"{old_remarks} ➔ 更新為: {new_remarks_input} [系統強制紀錄: 於 {current_time} 覆寫]"

            session.commit()
            print("資料覆寫與紀錄追加成功！")
            
        else:
            session.add(dispatch_order)
            session.commit()
            print(f"成功新增一筆派車單：{dispatch_order.date} - 司機 {dispatch_order.driver_id}")

        return True

    except Exception as e:
        session.rollback() 
        print(f"寫入/更新失敗：{e}")
        return False

    finally:
        session.close()


def get_order_by_driver_and_month(driver_id: str, year_month: str):
    session = SessionLocal()
    try:
        orders = session.query(DispatchOrderModel).filter(
            DispatchOrderModel.driver_id == driver_id, 
            DispatchOrderModel.date.startswith(year_month)
        ).all()
        return orders
    except Exception as e:
        print(f"讀取失敗：{e}")
        return [] 
    finally:
        session.close()


# --- 基本資料設定專用函式 ---

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
    except Exception as e:
        session.rollback()
        print(f"新增司機失敗: {e}")
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
    except Exception as e:
        session.rollback()
        print(f"新增車輛失敗: {e}")
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
            new_rule = PriceRuleModel(region_name=region_name, base_price=base_price)
            session.add(new_rule)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"更新費率失敗: {e}")
        return False
    finally:
>>>>>>> 6dc226a02ff70a5de420748604475cf5f3b56fad
        session.close()