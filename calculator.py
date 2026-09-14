
# 用於計算單趟派車費用與月薪的模組

# 定義地區與薪資的對應字典
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

# 將地區與薪資的對應字典轉換為單一地區對應薪資的字典
DESTINATION_PRICES = {}
for grouped_regions, total_price in RAW_DESTINATION_RATES.items():
    individual_regions = grouped_regions.split('、')
    for region in individual_regions:
        DESTINATION_PRICES[region] = total_price

# 計算單趟派車的函數
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
    # 取得基本運費與補貼總額
    basic_freight = DESTINATION_PRICES.get(region_name, 0)
    subsidy_total = 0
    # 計算各種補貼
    if has_freezing_plate: subsidy_total += 300
    if has_weighting: subsidy_total += 100
    if has_danger_tag: subsidy_total += 100
    if has_instrument_inspection: subsidy_total += 100
    # 夜間出車與假日出車補貼
    if is_night_shift: subsidy_total += 1000
    if is_holiday: subsidy_total += 1000
    # 早班出車補貼與時段薪資
    if early_shift_type == "03:00": subsidy_total += 200
    elif early_shift_type == "05:00": subsidy_total += 100
    # 加班卸貨超時補貼
    if unloading_overtime_hours > 0:
        subsidy_total += (unloading_overtime_hours * 500)
    # 回傳計算結果的字典
    return {
        "basic_freight": basic_freight,
        "subsidy_total": subsidy_total,
        "total_price": basic_freight + subsidy_total
    }

# 計算月薪的函數
def calculate_monthly_salary(
    trip_price,             
    full_attendance_bonus,  
    safety_bonus,           
    allowance,              
    labor_health_insurance, 
    phone_subsidy,          
    other_deductions,       
):
    total_trip_price = sum(trip_price)
    trip_price_bonus = int(total_trip_price * 0.06)
    total_salary = total_trip_price + trip_price_bonus
    total_additions = full_attendance_bonus + safety_bonus + allowance + labor_health_insurance + phone_subsidy
    total_deductions = other_deductions
    final_salary = total_salary + total_additions - total_deductions

    # 回傳計算結果的字典
    return {
        "月趟次總額": total_trip_price,
        "6%出車加給": trip_price_bonus,
        "全勤獎金": full_attendance_bonus,
        "安全獎金": safety_bonus,
        "其他補貼": allowance,
        "勞健保補貼": labor_health_insurance,
        "電話費補助": phone_subsidy,
        "其他扣款": other_deductions,
        "實領薪資": final_salary
    }