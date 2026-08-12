<<<<<<< HEAD


# 定義地區與薪資的對應字典 (Key: 地區, Value: 基礎薪資)
RAW_DESTINATION_RATES = {
    "基隆、汐止": 700,
    "南港、內湖、松山、台北市區": 750,
    "士林、北投、新店、深坑、三重": 800,
    "蘆洲、五股、新莊、板橋、泰山、中和、永和、樹林、土城、三芝": 900,
    "龜山、鶯歌、林口、淡水、八里、三峽": 1000,
    "桃園、中壢、蘆竹、大園": 1100,
    "龍潭、新屋、楊梅、大溪、平鎮、觀音": 1200,
    "湖口、新豐、芎林、永安": 1300,
    "新竹、竹北、竹東": 1400,
    "頭份、竹南、香山": 1500,
    "苗栗、通霄、後龍": 1700,
    "三義、宜蘭、羅東": 1800,
    "后里": 1900,
    "台中": 2100,
    "彰化、員林地區": 2300,
    "南投地區": 2400,
    "雲林地區、斗六、斗南": 2600,
    "嘉義地區": 2900,
    "台南地區": 3300,
    "高雄地區": 3700,
    "屏東地區": 3900,
    }

# 建立空字典，用來放一對一的資料
DESTINATION_PRICES = {}
# 自動展開迴圈
# 把群組的地區切開成各個陣列
for grouped_regions, total_price in RAW_DESTINATION_RATES.items():
    individual_regions = grouped_regions.split('、')
    # 把切開後的值存進新字典
    for region in individual_regions:
        DESTINATION_PRICES[region] = total_price

# 定義單趟薪資的函式
def calculate_single_trip(
    region_name, 
    has_freezing_plate=False, 
    has_weighting=False, 
    has_danger_tag=False,
    has_instrument_inspection=False,
    is_night_shift=False,
    is_holiday=False,
    early_shift_type=None,
    unloading_overtime_hours=0
):
    
    # 取得基礎運費
    basic_freight = DESTINATION_PRICES.get(region_name, 0)

    # 計算所有補貼總和
    subsidy_total = 0

    if has_freezing_plate:
        subsidy_total += 300
    if has_weighting:
        subsidy_total += 100
    if has_danger_tag:
        subsidy_total += 100
    if has_instrument_inspection:
        subsidy_total += 100
    
    # 如果兩個都 True 就會加 2000
    if is_night_shift:
        subsidy_total += 1000
    if is_holiday:
        subsidy_total += 1000
        
    if early_shift_type == "03:00":
        subsidy_total += 200
    elif early_shift_type == "05:00":
        subsidy_total += 100
        
    if unloading_overtime_hours > 0:
        subsidy_total += (unloading_overtime_hours * 500)
    # 回傳拆解後的詳細金額字典
    return {
        "basic_freight": basic_freight,
        "subsidy_total": subsidy_total,
        "total_price": basic_freight + subsidy_total
    }


# 定義月薪計算的函式
def calculate_monthly_salary(
    trip_price,             # 月總趟薪資陣列
    full_attendance_bonus,  # 全勤獎金
    safety_bonus,           # 安全獎金
    allowance,              # 補貼
    labor_health_insurance, # 勞健保
    phone_subsidy,          # 電話費補助
    other_deductions,       # 其他扣款
):
    # 計算司機每個月的薪資結算，並回傳明細表
    total_trip_price = sum(trip_price)
    # 計算 6% 出車加給
    trip_price_bonus = int(total_trip_price * 0.06)  # 出車獎金為總 trip_price 的 6%
    total_salary = total_trip_price + trip_price_bonus
    # 計算總加項
    total_additions = full_attendance_bonus + safety_bonus + allowance + labor_health_insurance + phone_subsidy
    # 計算總減項
    total_deductions = other_deductions
    # 最終實領薪資
    final_salary = total_salary + total_additions - total_deductions

    # 將所有明細回傳
    return {
        "月趟次總額": total_trip_price,
        "6%出車加給": trip_price_bonus,
        "全勤獎金": full_attendance_bonus,
        "安全獎金": safety_bonus,
        "補貼": allowance,
        "勞健保": labor_health_insurance,
        "電話費補助": phone_subsidy,
        "其他扣款": other_deductions,
        "實領薪資": final_salary
    }


# 測試區
if __name__ == "__main__":

    # 測試單趟薪資計算
    if_total_price = calculate_single_trip("五股", True, False, False)
    print(f"單趟薪資: {if_total_price} 元")  # 預期輸出: 單趟薪資: 1200 元

    # 測試月薪計算
    if_trip_prices = [1200, 1300, 1400, 1500, 700, 3700, 2300, 900]

    # 呼叫月結算函式，並帶入各項加減款項
    monthly_report = calculate_monthly_salary(
        trip_price=if_trip_prices,
        full_attendance_bonus=2000,
        safety_bonus=1000,
        allowance=1900,               # 照片裡有出現的補貼 1900
        labor_health_insurance=5000,  # 照片裡有出現的勞健保 5000
        phone_subsidy=700,            # 照片裡有出現的電話費補助 700
        other_deductions= 1000
    )
    
    print("【月結算測試明細】")
    # 用迴圈把字典裡的明細一行一行印出來檢查
    for key, value in monthly_report.items():
        print(f"{key}: {value} 元")

=======


# 定義地區與薪資的對應字典 (Key: 地區, Value: 基礎薪資)
RAW_DESTINATION_RATES = {
    "基隆、汐止": 700,
    "南港、內湖、松山、台北市區": 750,
    "士林、北投、新店、深坑、三重": 800,
    "蘆洲、五股、新莊、板橋、泰山、中和、永和、樹林、土城、三芝": 900,
    "龜山、鶯歌、林口、淡水、八里、三峽": 1000,
    "桃園、中壢、蘆竹、大園": 1100,
    "龍潭、新屋、楊梅、大溪、平鎮、觀音": 1200,
    "湖口、新豐、芎林、永安": 1300,
    "新竹、竹北、竹東": 1400,
    "頭份、竹南、香山": 1500,
    "苗栗、通霄、後龍": 1700,
    "三義、宜蘭、羅東": 1800,
    "后里": 1900,
    "台中": 2100,
    "彰化、員林地區": 2300,
    "南投地區": 2400,
    "雲林地區、斗六、斗南": 2600,
    "嘉義地區": 2900,
    "台南地區": 3300,
    "高雄地區": 3700,
    "屏東地區": 3900,
    }

# 建立空字典，用來放一對一的資料
DESTINATION_PRICES = {}
# 自動展開迴圈
# 把群組的地區切開成各個陣列
for grouped_regions, total_price in RAW_DESTINATION_RATES.items():
    individual_regions = grouped_regions.split('、')
    # 把切開後的值存進新字典
    for region in individual_regions:
        DESTINATION_PRICES[region] = total_price

# 定義單趟薪資的函式
def calculate_single_trip(
    region_name, 
    has_freezing_plate=False, 
    has_weighting=False, 
    has_danger_tag=False,
    has_instrument_inspection=False,
    is_night_shift=False,
    is_holiday=False,
    early_shift_type=None,
    unloading_overtime_hours=0
):
    
    # 取得基礎運費
    basic_freight = DESTINATION_PRICES.get(region_name, 0)

    # 計算所有補貼總和
    subsidy_total = 0

    if has_freezing_plate:
        subsidy_total += 300
    if has_weighting:
        subsidy_total += 100
    if has_danger_tag:
        subsidy_total += 100
    if has_instrument_inspection:
        subsidy_total += 100
    
    # 如果兩個都 True 就會加 2000
    if is_night_shift:
        subsidy_total += 1000
    if is_holiday:
        subsidy_total += 1000
        
    if early_shift_type == "03:00":
        subsidy_total += 200
    elif early_shift_type == "05:00":
        subsidy_total += 100
        
    if unloading_overtime_hours > 0:
        subsidy_total += (unloading_overtime_hours * 500)
    # 回傳拆解後的詳細金額字典
    return {
        "basic_freight": basic_freight,
        "subsidy_total": subsidy_total,
        "total_price": basic_freight + subsidy_total
    }


# 定義月薪計算的函式
def calculate_monthly_salary(
    trip_price,             # 月總趟薪資陣列
    full_attendance_bonus,  # 全勤獎金
    safety_bonus,           # 安全獎金
    allowance,              # 補貼
    labor_health_insurance, # 勞健保
    phone_subsidy,          # 電話費補助
    other_deductions,       # 其他扣款
):
    # 計算司機每個月的薪資結算，並回傳明細表
    total_trip_price = sum(trip_price)
    # 計算 6% 出車加給
    trip_price_bonus = int(total_trip_price * 0.06)  # 出車獎金為總 trip_price 的 6%
    total_salary = total_trip_price + trip_price_bonus
    # 計算總加項
    total_additions = full_attendance_bonus + safety_bonus + allowance + labor_health_insurance + phone_subsidy
    # 計算總減項
    total_deductions = other_deductions
    # 最終實領薪資
    final_salary = total_salary + total_additions - total_deductions

    # 將所有明細回傳
    return {
        "月趟次總額": total_trip_price,
        "6%出車加給": trip_price_bonus,
        "全勤獎金": full_attendance_bonus,
        "安全獎金": safety_bonus,
        "補貼": allowance,
        "勞健保": labor_health_insurance,
        "電話費補助": phone_subsidy,
        "其他扣款": other_deductions,
        "實領薪資": final_salary
    }


# 測試區
if __name__ == "__main__":

    # 測試單趟薪資計算
    if_total_price = calculate_single_trip("五股", True, False, False)
    print(f"單趟薪資: {if_total_price} 元")  # 預期輸出: 單趟薪資: 1200 元

    # 測試月薪計算
    if_trip_prices = [1200, 1300, 1400, 1500, 700, 3700, 2300, 900]

    # 呼叫月結算函式，並帶入各項加減款項
    monthly_report = calculate_monthly_salary(
        trip_price=if_trip_prices,
        full_attendance_bonus=2000,
        safety_bonus=1000,
        allowance=1900,               # 照片裡有出現的補貼 1900
        labor_health_insurance=5000,  # 照片裡有出現的勞健保 5000
        phone_subsidy=700,            # 照片裡有出現的電話費補助 700
        other_deductions= 1000
    )
    
    print("【月結算測試明細】")
    # 用迴圈把字典裡的明細一行一行印出來檢查
    for key, value in monthly_report.items():
        print(f"{key}: {value} 元")

>>>>>>> 6dc226a02ff70a5de420748604475cf5f3b56fad
