# bazi_core.py
import datetime
import calendar
import math
from solar_terms import find_bazi_year_month, get_solar_term_datetime

# Heavenly Stems and Earthly Branches
HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

# Translation dictionaries
HEAVENLY_STEMS_EN = {
    "甲": "Jia", "乙": "Yi", "丙": "Bing", "丁": "Ding",
    "戊": "Wu", "己": "Ji", "庚": "Geng", "辛": "Xin", 
    "壬": "Ren", "癸": "Gui"
}

EARTHLY_BRANCHES_EN = {
    "子": "Zi", "丑": "Chou", "寅": "Yin", "卯": "Mao",
    "辰": "Chen", "巳": "Si", "午": "Wu", "未": "Wei",
    "申": "Shen", "酉": "You", "戌": "Xu", "亥": "Hai"
}

STEMS_ELEMENTS = {
    "甲": "Wood", "乙": "Wood", "丙": "Fire", "丁": "Fire",
    "戊": "Earth", "己": "Earth", "庚": "Metal", "辛": "Metal",
    "壬": "Water", "癸": "Water"
}

BRANCHES_ANIMALS = {
    "子": "Rat", "丑": "Ox", "寅": "Tiger", "卯": "Rabbit",
    "辰": "Dragon", "巳": "Snake", "午": "Horse", "未": "Goat",
    "申": "Monkey", "酉": "Rooster", "戌": "Dog", "亥": "Pig"
}

# ----------------------
# Solar Time Calculation Functions
# ----------------------
def day_of_year(year, month, day):
    """Calculate day of year (1-366)"""
    date = datetime.date(year, month, day)
    return date.timetuple().tm_yday

def equation_of_time(doy):
    """
    Calculate the Equation of Time using NOAA approximation.
    
    Args:
        doy (int): Day of year (1-366)
        
    Returns:
        float: Equation of time in minutes
    """
    B = 2 * math.pi * (doy - 81) / 364
    eot = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
    return eot

def longitude_correction(longitude, timezone_offset):
    """
    Calculate longitude correction for solar time.
    
    Args:
        longitude (float): Longitude in decimal degrees
        timezone_offset (float): Timezone offset from GMT in hours
        
    Returns:
        float: Correction in minutes
    """
    tz_meridian = timezone_offset * 15.0
    correction_minutes = (longitude - tz_meridian) / 15.0 * 60.0
    return correction_minutes

def civil_to_apparent_solar(dt_civil, longitude, timezone_offset):
    """
    Convert civil (clock) time to apparent solar time.
    
    Args:
        dt_civil (datetime): Civil time
        longitude (float): Longitude in decimal degrees  
        timezone_offset (float): Timezone offset from GMT in hours
        
    Returns:
        tuple: (solar_datetime, longitude_correction_minutes, equation_of_time_minutes)
    """
    doy = day_of_year(dt_civil.year, dt_civil.month, dt_civil.day)
    eot = equation_of_time(doy)
    long_corr = longitude_correction(longitude, timezone_offset)
    total_correction = long_corr + eot
    dt_solar = dt_civil + datetime.timedelta(minutes=total_correction)
    return dt_solar, long_corr, eot

# ----------------------
# Input Validation
# ----------------------
def validate_input(year, month, day, hour, minute, longitude=None):
    """
    Validate birth information input.
    
    Args:
        year, month, day, hour, minute (int): Birth date/time components
        longitude (float, optional): Longitude in decimal degrees
        
    Returns:
        str or None: Error message if validation fails, None if valid
    """
    current_year = datetime.datetime.now().year
    if not (1900 <= year <= current_year):
        return f"Year must be between 1900 and {current_year}"
    if not (1 <= month <= 12):
        return "Month must be between 1 and 12"
    try:
        max_day = calendar.monthrange(year, month)[1]
        if not (1 <= day <= max_day):
            return f"Day must be between 1 and {max_day} for {calendar.month_name[month]}"
    except:
        return "Invalid month/year combination"
    if not (0 <= hour <= 23):
        return "Hour must be between 0 and 23"
    if not (0 <= minute <= 59):
        return "Minute must be between 0 and 59"
    if longitude is not None:
        if not (-180.0 <= longitude <= 180.0):
            return "Longitude must be between -180 and 180 degrees"
    return None

# ----------------------
# Astronomical Calculations
# ----------------------
def gregorian_to_julian_date(year, month, day, hour=0, minute=0, second=0):
    """
    Convert Gregorian date to Julian Date.
    
    Args:
        year, month, day (int): Date components
        hour, minute, second (int): Time components
        
    Returns:
        float: Julian Date
    """
    day_fraction = (hour + minute/60.0 + second/3600.0) / 24.0
    Y = year
    M = month
    D = day + day_fraction
    if M <= 2:
        Y -= 1
        M += 12
    A = Y // 100
    B = 2 - A + (A // 4)
    jd = math.floor(365.25 * (Y + 4716)) + math.floor(30.6001 * (M + 1)) + D + B - 1524.5
    return jd

def julian_day_number_at_noon(jd):
    """Convert Julian Date to Julian Day Number at noon"""
    return int(math.floor(jd + 0.5))

def calculate_day_master_from_solar(dt_solar):
    """
    Calculate Day Master (Day Stem and Branch) from solar time.
    
    Args:
        dt_solar (datetime): Solar time
        
    Returns:
        tuple: (day_stem, day_branch, julian_date, julian_day_number)
    """
    jd = gregorian_to_julian_date(dt_solar.year, dt_solar.month, dt_solar.day, 
                                  dt_solar.hour, dt_solar.minute, dt_solar.second)
    jd_noon = julian_day_number_at_noon(jd)
    stem_idx = ((jd_noon - 1) % 10)
    branch_idx = ((jd_noon + 1) % 12)
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx], jd, jd_noon

# ----------------------
# BaZi Four Pillars Calculation
# ----------------------
def calculate_year_pillar(bazi_year):
    """
    Calculate Year Pillar based on BaZi year.
    
    Args:
        bazi_year (int): BaZi year (considering solar term boundaries)
        
    Returns:
        tuple: (year_stem, year_branch)
    """
    sexagenary_year_index = (bazi_year - 3) % 60
    year_stem = HEAVENLY_STEMS[sexagenary_year_index % 10]
    year_branch = EARTHLY_BRANCHES[sexagenary_year_index % 12]
    return year_stem, year_branch

def calculate_month_pillar(bazi_year, bazi_month):
    """
    Calculate Month Pillar based on BaZi year and month.
    
    Args:
        bazi_year (int): BaZi year
        bazi_month (int): BaZi month (1-12)
        
    Returns:
        tuple: (month_stem, month_branch)
    """
    year_stem, _ = calculate_year_pillar(bazi_year)
    month_branch = EARTHLY_BRANCHES[(bazi_month - 1) % 12]
    month_stem_index = (HEAVENLY_STEMS.index(year_stem) + 2 + (bazi_month - 1)) % 10
    month_stem = HEAVENLY_STEMS[month_stem_index]
    return month_stem, month_branch

def calculate_hour_pillar(day_stem, solar_hour):
    """
    Calculate Hour Pillar based on Day Stem and solar hour.
    
    Args:
        day_stem (str): Day stem character
        solar_hour (int): Hour in solar time (0-23)
        
    Returns:
        tuple: (hour_stem, hour_branch)
    """
    hour_slot = (solar_hour + 1) // 2
    hour_branch = EARTHLY_BRANCHES[hour_slot % 12]
    hour_stem = HEAVENLY_STEMS[(HEAVENLY_STEMS.index(day_stem) + hour_slot) % 10]
    return hour_stem, hour_branch

def create_four_pillars_with_solar_terms(dt_solar):
    """
    Create complete Four Pillars using solar time and solar term boundaries.
    
    Args:
        dt_solar (datetime): Solar time
        
    Returns:
        dict: Complete pillar information including metadata and translations
    """
    # Find correct BaZi year and month using solar terms
    bazi_year, bazi_month, year_start, month_start = find_bazi_year_month(dt_solar)
    
    # Calculate each pillar
    year_stem, year_branch = calculate_year_pillar(bazi_year)
    month_stem, month_branch = calculate_month_pillar(bazi_year, bazi_month)
    day_stem, day_branch, jd, jd_noon = calculate_day_master_from_solar(dt_solar)
    hour_stem, hour_branch = calculate_hour_pillar(day_stem, dt_solar.hour)
    
    # Format pillar strings
    year_pillar = f"{year_stem}{year_branch}"
    month_pillar = f"{month_stem}{month_branch}"
    day_pillar = f"{day_stem}{day_branch}"
    hour_pillar = f"{hour_stem}{hour_branch}"
    
    # Prepare result dictionary with translations
    result = {
        "year": year_pillar,
        "month": month_pillar,
        "day": day_pillar,
        "hour": hour_pillar,
        "day_master": day_stem,
        "year_translations": {
            "pinyin": f"{HEAVENLY_STEMS_EN[year_stem]} {EARTHLY_BRANCHES_EN[year_branch]}",
            "meaning": f"{STEMS_ELEMENTS[year_stem]} {BRANCHES_ANIMALS[year_branch]}"
        },
        "month_translations": {
            "pinyin": f"{HEAVENLY_STEMS_EN[month_stem]} {EARTHLY_BRANCHES_EN[month_branch]}",
            "meaning": f"{STEMS_ELEMENTS[month_stem]} {BRANCHES_ANIMALS[month_branch]}"
        },
        "day_translations": {
            "pinyin": f"{HEAVENLY_STEMS_EN[day_stem]} {EARTHLY_BRANCHES_EN[day_branch]}",
            "meaning": f"{STEMS_ELEMENTS[day_stem]} {BRANCHES_ANIMALS[day_branch]}"
        },
        "hour_translations": {
            "pinyin": f"{HEAVENLY_STEMS_EN[hour_stem]} {EARTHLY_BRANCHES_EN[hour_branch]}",
            "meaning": f"{STEMS_ELEMENTS[hour_stem]} {BRANCHES_ANIMALS[hour_branch]}"
        },
        "jd": jd,
        "jd_noon": jd_noon,
        "bazi_year": bazi_year,
        "bazi_month": bazi_month
    }
    
    # Add solar term boundary information if available
    if year_start:
        result["bazi_year_start"] = year_start.strftime("%B %d, %Y at %H:%M")
    if month_start:
        result["bazi_month_start"] = month_start.strftime("%B %d, %Y at %H:%M")
    
    return result

# ----------------------
# Legacy compatibility function (for transition from old single-file version)
# ----------------------
def create_four_pillars_from_solar(dt_solar):
    """
    Legacy function name for backward compatibility.
    Calls the new create_four_pillars_with_solar_terms function.
    """
    return create_four_pillars_with_solar_terms(dt_solar)
