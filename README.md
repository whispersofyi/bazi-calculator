# Day Master Calculator - Whispers of YI

A precise BaZi (Four Pillars of Destiny) calculator that converts civil time to apparent solar time and applies traditional Chinese solar term boundaries for authentic calculations.

## Features

- **Solar Time Accuracy**: Converts clock time to apparent solar time using longitude correction and Equation of Time
- **Solar Term Boundaries**: Uses traditional Chinese calendar boundaries (立春 for New Year) instead of Western dates
- **Four Pillars Display**: Shows Year, Month, Day, and Hour pillars with Chinese characters, pinyin, and English translations
- **Day Master Analysis**: Comprehensive personality insights based on your Day Master element
- **Technical Transparency**: Detailed breakdown of all astronomical corrections applied

## Live Demo

[Try the calculator](https://your-streamlit-app-url.com)

## Installation & Local Development

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
git clone https://github.com/yourusername/bazi-day-master-calculator.git
cd bazi-day-master-calculator
pip install -r requirements.txt
streamlit run app.py
```

The calculator will open in your browser at `http://localhost:8501`

## How It Works

### Solar Time Conversion
Most BaZi calculators use clock time directly, which can be inaccurate. This calculator applies:

1. **Longitude Correction**: Adjusts for your distance from your timezone's central meridian
2. **Equation of Time**: Accounts for Earth's elliptical orbit and axial tilt (±16 minutes seasonal variation)
3. **Solar Term Boundaries**: Uses authentic Chinese calendar transitions

### Why Precision Matters
These corrections can shift your Hour Pillar and, in edge cases, your Day Master compared to simplified calculators. The difference can be significant for people born:
- Far from their timezone's central meridian
- During solar term transition periods
- At hour boundaries (23:00-01:00, 01:00-03:00, etc.)

## File Structure

```
├── app.py                    # Main Streamlit application
├── bazi_core.py             # Core BaZi calculation functions
├── day_master_data.py       # Day Master personality database
├── solar_terms.py           # Solar term data and lookup functions
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Privacy

This calculator:
- Does not store or log personal information
- Processes all calculations locally in your browser session
- Does not transmit birth data to external servers

## Accuracy & Limitations

- **Accurate for**: 1900-2025 (Gregorian calendar years)
- **Solar term data**: Based on astronomical calculations
- **Time precision**: Accounts for longitude and seasonal variations
- **Not included**: Daylight saving time adjustments (use standard time)

## Technical Details

The calculator implements professional-grade astronomical formulas:
- Julian Date calculations for consistent day counting
- NOAA Equation of Time approximation
- Traditional Chinese solar term boundaries
- Sexagenary cycle calculations for Four Pillars

## Contributing

This is a focused tool for accurate BaZi calculations. Contributions welcome for:
- Bug fixes and accuracy improvements
- Additional Day Master personality insights
- Solar term data corrections
- Translation improvements

## License

MIT License - see [LICENSE](LICENSE) file for details.

Code is open source. Day Master personality content is provided for educational purposes.

## About Whispers of YI

This calculator is part of the Whispers of YI project - exploring the quiet intersections of Daoist thought, time, and elemental cycles.

- **Free guides**: [whispersofyi.github.io](https://whispersofyi.github.io/)
- **YouTube**: [@whispersofyi](https://youtube.com/@whispersofyi)
- **Deeper companions**: [Gumroad](https://whispersofyi.gumroad.com/)

---

*"Time is not a straight road. It bends and pools, carrying you whether you swim or rest."*
