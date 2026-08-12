<<<<<<< HEAD


# 匯入會用到的欄位型態
import string
from sqlalchemy import Column, Integer, String, Boolean
# 匯入建立地基的工具
from sqlalchemy.orm import declarative_base

# 建立地基，以後所有的 Class 都要繼承這個 Base
Base = declarative_base()


# 基礎設定表 (給老闆娘後台動態新增用的)
class DriverModel(Base):
    # 資料庫表格名稱
    __tablename__ = 'drivers'

    # 系統自動產生的唯一編號，設為 primary_key (主鍵)
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 開始把變數轉換成 Column
    driver_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

class TruckModel(Base):
    # 車輛名冊表
    __tablename__ = 'trucks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_number = Column(String(50), unique=True, nullable=False) # 例如：AB-1234
    size = Column(String(20), nullable=False)                      # 20尺 或 40尺

class PriceRuleModel(Base):
    # 地區計價規則表
    __tablename__ = 'price_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    region_name = Column(String(100), unique=True, nullable=False) # 例如：五股
    base_price = Column(Integer, nullable=False)                   # 例如：900


# 核心業務表：派車單
class DispatchOrderModel(Base):
    # 資料庫表格名稱
    __tablename__ = 'dispatch_orders'

    # 系統自動產生的唯一編號，設為 primary_key (主鍵)
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 開始把變數轉換成 Column
    # 基本資訊
    driver_id = Column(String(50), nullable=False)
    date = Column(String(10), nullable=False) 
    container_id = Column(String(50), nullable=False)
    truck_number = Column(String(50), nullable=False)
    cargo_owner = Column(String(100), nullable=False)
    
    # 路線資訊
    point_of_origin = Column(String(100), nullable=False)
    destination_address = Column(String(200), nullable=False)
    billing_region = Column(String(100), nullable=False)
    is_return_trip = Column(Boolean, default=False)            # 標記是否為來回車趟 (A>B>A)
    
    # 加給項目 (對齊手稿的所有補貼)
    has_weighting = Column(Boolean, default=False)             # 過磅 (100)
    has_danger_tag = Column(Boolean, default=False)            # 危標 (100)
    has_instrument_inspection = Column(Boolean, default=False) # 儀檢 (100)
    has_freezing_plate = Column(Boolean, default=False)        # 冷凍板 (300)

    is_night_shift = Column(Boolean, default=False)            # 夜間出車 (1000)
    is_holiday = Column(Boolean, default=False)                # 假日出車 (1000)

    early_shift_type = Column(String(20), nullable=True)       # 早車時段：填入 "03:00" 或 "05:00" 或 Null
    unloading_overtime_hours = Column(Integer, default=0)      # 卸貨超時：輸入小時數，每小時 500
    
    # 金額拆解 (確保報表帳目清晰)
    basic_freight = Column(Integer, default=0)                 # 單趟基本運費 (對應計價地區)
    subsidy_total = Column(Integer, default=0)                 # 單趟補貼總和 (過磅+超時+夜間等)
    
    remarks = Column(String(500), nullable=True)


# 資料庫初始化執行區 (建表用)
if __name__ == "__main__":
    from sqlalchemy import create_engine
    
    print("開始更新資料庫結構...")
    engine = create_engine('sqlite:///test_truck.db', echo=True)
    
    # create_all 會自動檢查，把尚未建立的新表格 (Driver, Truck, PriceRule) 蓋出來
    # 注意：SQLite 原生不支援直接在舊表格 (dispatch_orders) 中新增欄位。
    # 為了開發方便，如果遇到舊表格無法自動擴充的問題，建議先刪除舊的 test_truck.db 檔案，
    # 讓程式重新建立一個包含所有新欄位的乾淨資料庫。
    Base.metadata.create_all(engine)
=======


# 匯入會用到的欄位型態
import string
from sqlalchemy import Column, Integer, String, Boolean
# 匯入建立地基的工具
from sqlalchemy.orm import declarative_base

# 建立地基，以後所有的 Class 都要繼承這個 Base
Base = declarative_base()


# 基礎設定表 (給老闆娘後台動態新增用的)
class DriverModel(Base):
    # 資料庫表格名稱
    __tablename__ = 'drivers'

    # 系統自動產生的唯一編號，設為 primary_key (主鍵)
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 開始把變數轉換成 Column
    driver_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

class TruckModel(Base):
    # 車輛名冊表
    __tablename__ = 'trucks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    truck_number = Column(String(50), unique=True, nullable=False) # 例如：AB-1234
    size = Column(String(20), nullable=False)                      # 20尺 或 40尺

class PriceRuleModel(Base):
    # 地區計價規則表
    __tablename__ = 'price_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    region_name = Column(String(100), unique=True, nullable=False) # 例如：五股
    base_price = Column(Integer, nullable=False)                   # 例如：900


# 核心業務表：派車單
class DispatchOrderModel(Base):
    # 資料庫表格名稱
    __tablename__ = 'dispatch_orders'

    # 系統自動產生的唯一編號，設為 primary_key (主鍵)
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 開始把變數轉換成 Column
    # 基本資訊
    driver_id = Column(String(50), nullable=False)
    date = Column(String(10), nullable=False) 
    container_id = Column(String(50), nullable=False)
    truck_number = Column(String(50), nullable=False)
    cargo_owner = Column(String(100), nullable=False)
    
    # 路線資訊
    point_of_origin = Column(String(100), nullable=False)
    destination_address = Column(String(200), nullable=False)
    billing_region = Column(String(100), nullable=False)
    is_return_trip = Column(Boolean, default=False)            # 標記是否為來回車趟 (A>B>A)
    
    # 加給項目 (對齊手稿的所有補貼)
    has_weighting = Column(Boolean, default=False)             # 過磅 (100)
    has_danger_tag = Column(Boolean, default=False)            # 危標 (100)
    has_instrument_inspection = Column(Boolean, default=False) # 儀檢 (100)
    has_freezing_plate = Column(Boolean, default=False)        # 冷凍板 (300)

    is_night_shift = Column(Boolean, default=False)            # 夜間出車 (1000)
    is_holiday = Column(Boolean, default=False)                # 假日出車 (1000)

    early_shift_type = Column(String(20), nullable=True)       # 早車時段：填入 "03:00" 或 "05:00" 或 Null
    unloading_overtime_hours = Column(Integer, default=0)      # 卸貨超時：輸入小時數，每小時 500
    
    # 金額拆解 (確保報表帳目清晰)
    basic_freight = Column(Integer, default=0)                 # 單趟基本運費 (對應計價地區)
    subsidy_total = Column(Integer, default=0)                 # 單趟補貼總和 (過磅+超時+夜間等)
    
    remarks = Column(String(500), nullable=True)


# 資料庫初始化執行區 (建表用)
if __name__ == "__main__":
    from sqlalchemy import create_engine
    
    print("開始更新資料庫結構...")
    engine = create_engine('sqlite:///test_truck.db', echo=True)
    
    # create_all 會自動檢查，把尚未建立的新表格 (Driver, Truck, PriceRule) 蓋出來
    # 注意：SQLite 原生不支援直接在舊表格 (dispatch_orders) 中新增欄位。
    # 為了開發方便，如果遇到舊表格無法自動擴充的問題，建議先刪除舊的 test_truck.db 檔案，
    # 讓程式重新建立一個包含所有新欄位的乾淨資料庫。
    Base.metadata.create_all(engine)
>>>>>>> 6dc226a02ff70a5de420748604475cf5f3b56fad
    print("資料庫結構更新完成！")