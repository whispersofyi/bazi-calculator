# app.py
import streamlit as st
import datetime
import calendar
from solar_terms import find_bazi_year_month
from bazi_core import create_four_pillars_with_solar_terms, civil_to_apparent_solar, validate_input
from day_master_data import DAY_MASTER_DATA

# Page configuration (no decorative icons)
st.set_page_config(
    page_title="Day Master Calculator - Whispers of YI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal, stable sans-serif override + pillar styling
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .pillar-box {
        text-align: center;
        margin: 10px 0;
    }
    .pillar-chinese {
        font-size: 56px;
        font-weight: 700;
        line-height: 1;
    }
    .pillar-caption {
        font-size: 14px;
        color: #333333;
        margin-top: 6px;
    }
    .small-note {
        color: #555555;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Timezone helpers (half-hour coverage)
# ----------------------
def format_tz_label(offset):
    if offset == 0:
        return "GMT"
    if float(offset).is_integer():
        return f"GMT{int(offset):+d}"
    # show one decimal (e.g., +5.5)
    return f"GMT{offset:+.1f}"

def parse_gmt_offset(label):
    # label like "GMT", "GMT+8", "GMT-3.5"
    if label == "GMT":
        return 0.0
    try:
        val = label.replace("GMT", "")
        return float(val)
    except:
        return 0.0

tz_offsets = [i * 0.5 for i in range(-24, 29)]  # -12.0 .. +14.0 step 0.5
tz_options = [format_tz_label(o) for o in tz_offsets]

# ----------------------
# UI - stable, serious aesthetic
# ----------------------
st.title("Day Master Calculator")
st.caption("A quiet voice in the scrollstorm â€" discover your elemental nature through the ancient wisdom of BaZi")

# Sidebar: longitude toggle outside form for immediate show/hide
with st.sidebar:
    st.header("Birth Information")
    use_longitude = st.checkbox("Enable longitude correction for maximum precision", value=False)
    if use_longitude:
        st.markdown("Enter your longitude in decimal degrees (e.g., Hong Kong = 114.1694Â°E, London = -0.1276Â°W) for the most accurate solar time conversion.")

    with st.form("birth_form"):
        current_year = datetime.datetime.now().year
        b_year = st.number_input("Birth Year", min_value=1900, max_value=current_year, value=1990)
        b_month = st.number_input("Birth Month", min_value=1, max_value=12, value=1)
        b_day = st.number_input("Birth Day", min_value=1, max_value=31, value=1)

        col1, col2 = st.columns(2)
        with col1:
            b_hour = st.number_input("Hour (0-23)", min_value=0, max_value=23, value=12)
        with col2:
            b_minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

        selected_tz = st.selectbox("Time Zone", tz_options, index=tz_options.index("GMT+8"))

        longitude_input = None
        if use_longitude:
            longitude_input = st.number_input(
                "Longitude (decimal degrees)",
                min_value=-180.0,
                max_value=180.0,
                value=114.1694,
                help="Enter longitude only (decimal degrees). Example: Hong Kong = 114.1694; London = -0.1276"
            )

        submit_button = st.form_submit_button("Calculate Day Master")

    st.markdown("---")
    st.markdown("[Back to Whispers of YI](https://whispersofyi.github.io/)")

# Main content
if submit_button:
    # Use selected timezone offset
    tz_offset = parse_gmt_offset(selected_tz)

    # If user didn't enable longitude, approximate using timezone meridian
    longitude_used = longitude_input if use_longitude else tz_offset * 15.0

    # Validate
    validation_error = validate_input(b_year, b_month, b_day, b_hour, b_minute, longitude_used)
    if validation_error:
        st.error(validation_error)
    else:
        try:
            civil_dt = datetime.datetime(b_year, b_month, b_day, b_hour, b_minute, 0)
            solar_dt, long_corr, eot = civil_to_apparent_solar(civil_dt, longitude_used, tz_offset)
            pillars = create_four_pillars_with_solar_terms(solar_dt)
            day_master_key = pillars["day_master"]
            day_master_info = DAY_MASTER_DATA.get(day_master_key)

            st.success("Day Master calculated successfully (solar time + solar terms applied)")

            st.markdown("---")

            # Pillars horizontal: enlarge Chinese characters + add translations
            cA, cB, cC, cD = st.columns(4)
            pillar_data = [
                (cA, "Year Pillar", pillars["year"], "Ancestry & Foundation", pillars["year_translations"]),
                (cB, "Month Pillar", pillars["month"], "Career & Relationships", pillars["month_translations"]),
                (cC, "Day Pillar", pillars["day"], "Self & Spouse", pillars["day_translations"]),
                (cD, "Hour Pillar", pillars["hour"], "Children & Legacy", pillars["hour_translations"]),
            ]
            for col, title, hanzi, caption, translations in pillar_data:
                with col:
                    st.markdown(
                        f"<div class='pillar-box'>"
                        f"<div><strong>{title}</strong></div>"
                        f"<div class='pillar-chinese'>{hanzi}</div>"
                        f"<div class='small-note'>{translations['pinyin']}</div>"
                        f"<div class='small-note'>{translations['meaning']}</div>"
                        f"<div class='pillar-caption'>{caption}</div>"
                        f"</div>", 
                        unsafe_allow_html=True
                    )

            st.markdown("---")

            # Day Master analysis
            if day_master_info:
                st.header(f"Your Day Master is {day_master_info['name']} â€" {day_master_key} ({day_master_info['element']})")
                st.write(day_master_info["description"])

                st.subheader("Natural Strengths & Positive Traits")
                for t in day_master_info["positive_traits"]:
                    st.markdown(f"- {t}")

                st.subheader("Growth Areas & Potential Challenges")
                for t in day_master_info["challenges"]:
                    st.markdown(f"- {t}")

                st.subheader("Elemental Harmony & Compatibility")
                st.write(day_master_info["compatibility"])

                st.subheader("Career Paths & Life Direction")
                st.write(day_master_info["career_paths"])

                st.subheader("Life Philosophy & Core Values")
                st.write(day_master_info["life_philosophy"])
            else:
                st.error("Day Master data unavailable for computed stem.")

            # Consolidated technical expander (single source of truth)
            with st.expander("Birth Details & Technical Information"):
                st.write("**Input (civil clock time):**")
                st.write(f"- Date: {civil_dt.strftime('%B %d, %Y')}")
                st.write(f"- Time: {civil_dt.strftime('%H:%M')} ({selected_tz})")
                st.write(f"**Longitude used for correction:** {longitude_used:+.4f}Â° (decimal degrees)")
                st.write("")
                st.write("**Converted to Apparent Solar Time:**")
                st.write(f"- Apparent Solar Time: {solar_dt.strftime('%B %d, %Y at %H:%M:%S')}")
                st.write("")
                st.write("**Solar Time Corrections Applied:**")
                st.write(f"- Longitude correction: {long_corr:+.2f} minutes")
                st.write(f"- Equation of Time: {eot:+.2f} minutes")
                st.write(f"- Total correction: {(long_corr + eot):+.2f} minutes")
                
                # Solar term boundaries applied
                if 'bazi_year_start' in pillars:
                    st.write("")
                    st.write("**Solar Term Boundaries Applied:**")
                    st.write(f"- BaZi year starts: {pillars['bazi_year_start']}")
                    st.write(f"- BaZi month starts: {pillars['bazi_month_start']}")
                
                # Gentle notices about scale of correction
                total_corr = abs(long_corr + eot)
                if total_corr > 30:
                    st.write("- **Note:** Large time correction applied â€" results may differ significantly from clock-time calculations.")
                elif total_corr > 15:
                    st.write("- **Note:** Moderate time correction applied â€" this improves accuracy for BaZi analysis.")
                
                st.write("")
                st.write("**Four Pillars (based on solar time + solar terms):**")
                st.write(f"- Year: {pillars['year']}")
                st.write(f"- Month: {pillars['month']}")
                st.write(f"- Day: {pillars['day']}")
                st.write(f"- Hour: {pillars['hour']}")
                st.write("")
                st.write("**Julian Date Information:**")
                st.write(f"- JD (fractional): {pillars['jd']:.6f}")
                st.write(f"- JD noon integer: {pillars['jd_noon']}")
                st.markdown("---")
                st.write("About Solar Time + Solar Term Correction:")
                st.write(
                    "This tool converts civil (clock) time to apparent solar time and applies traditional Chinese solar term boundaries for BaZi calculations. "
                    "Three corrections are applied:\n\n"
                    "1. Longitude correction â€" adjusts for difference between your longitude and your timezone meridian.\n"
                    "2. Equation of Time â€" accounts for Earth's orbital eccentricity and axial tilt (seasonal Â± ~16 minutes).\n"
                    "3. Solar Term Boundaries â€" uses traditional Chinese calendar boundaries (e.g., ç«‹æ˜¥ for new year) instead of Western calendar dates.\n\n"
                    "Combined, these provide professional-grade accuracy for calculating all Four Pillars correctly."
                )

            # Privacy + back link
            st.markdown("---")
            st.caption("This calculator does not store or log personal information.")
            st.markdown("[Back to Whispers of YI](https://whispersofyi.github.io/)")

        except Exception as e:
            st.error(f"An error occurred during calculation: {e}")
else:
    # Home / instructions view
    st.markdown("## How to use")
    st.write("Enter your exact birth date and time in the sidebar, select the GMT offset for the birth location, optionally enable precise longitude for improved accuracy, then click 'Calculate Day Master'.")
    st.write("")
    st.markdown("**What you'll get:**")
    st.markdown(
        "- Solar-time conversion using longitude and the Equation of Time\n"
        "- Traditional solar term boundaries for accurate Year and Month pillars\n"
        "- Four Pillars overview based on authentic Chinese calendar system\n"
        "- Day Master personality analysis\n"
        "- Technical diagnostics showing all corrections applied"
    )
    
    st.markdown("## Solar Time Accuracy")
    
    st.markdown("**Longitude Correction**")
    st.write("Adjusts for your distance from your timezone's central meridian. This can range from minutes to over an hour depending on your location within the timezone.")
    
    st.markdown("**Equation of Time**")
    st.write("Corrects for Earth's elliptical orbit and axial tilt, which causes the sun to run fast or slow throughout the year. This seasonal variation ranges from -14 to +16 minutes.")
    
    st.markdown("**Solar Term Boundaries**")
    st.write("Uses traditional Chinese calendar boundaries (like ç«‹æ˜¥ for New Year) instead of Western calendar dates. This ensures your Year and Month pillars reflect the authentic BaZi system.")
    
    st.markdown("**Why precision matters:** These corrections can shift your Hour Pillar and, in edge cases, your Day Master compared to clock-time-only calculators. Most online BaZi tools ignore these astronomical realities and use Western calendar boundaries, potentially giving you incorrect results.")
    
    st.caption("This calculator does not store or log personal information.")
    st.caption("Â© 2025 Whispers of YI â€" Code under MIT, Guides under CC BY-NC-ND 4.0")
