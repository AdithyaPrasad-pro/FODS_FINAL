"""WattWise | Household Energy Recommendation System
Foundations of Data Science (FODS) Review 2 Case Study
Simple & Interactive Streamlit Deployment of the WattWise Recommendation Model.
"""

from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------- Page Setup ----------
st.set_page_config(
    page_title="WattWise | Energy Recommendation System",
    page_icon="⚡",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "powerbi_exports"

# ---------- Custom Styling (Clean & Modern) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; font-size: 16px; }
.stApp { background: #0c1421; color: #f0f4f8; }
.block-container { max-width: 1200px; padding-top: 1.5rem; padding-bottom: 2.5rem; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: #ffffff !important; }
h1 { font-size: 2.3rem !important; }
h2 { font-size: 1.6rem !important; }
.badge { display: inline-block; background: rgba(112,225,193,0.15); color: #70e1c1; border: 1px solid #70e1c1; padding: 4px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
.recommendation-card { border-radius: 14px; padding: 22px; margin: 15px 0 20px 0; border: 1px solid; }
.rec-low { background: rgba(34, 197, 94, 0.12); border-color: #22c55e; }
.rec-normal { background: rgba(59, 130, 246, 0.12); border-color: #3b82f6; }
.rec-high { background: rgba(239, 68, 68, 0.15); border-color: #ef4444; }
.stat-box { background: #132032; border: 1px solid #1f334d; border-radius: 12px; padding: 16px; text-align: center; }
.stat-number { font-size: 1.8rem; font-weight: 700; color: #70e1c1; font-family: 'Space Grotesk', sans-serif; }
.stat-label { font-size: 0.9rem; color: #9fb3c8; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)


# ---------- Load Precomputed Data ----------
@st.cache_data
def load_data():
    daily_file = EXPORT_DIR / "daily_summary.csv"
    hour_file = EXPORT_DIR / "hour_of_day_summary.csv"
    
    daily_df = pd.read_csv(daily_file) if daily_file.exists() else None
    hour_df = pd.read_csv(hour_file) if hour_file.exists() else None
    return daily_df, hour_df

daily_df, hour_df = load_data()

# ---------- Empirical Thresholds from FODS Analysis ----------
# (Calculated from 2,075,259 minute readings grouped by day)
LOW_THRESHOLD = 0.903    # 33rd percentile (kW)
HIGH_THRESHOLD = 1.223   # 67th percentile (kW)

def get_recommendation(power_kw):
    if power_kw <= LOW_THRESHOLD:
        return {
            "class": "Low Consumption",
            "css": "rec-low",
            "badge_color": "#22c55e",
            "icon": "🟢",
            "summary": "Excellent Energy Efficiency!",
            "recommendation": "Maintain your current electricity usage habits. Your consumption is well within the most efficient 33% of household records.",
            "tips": [
                "Continue running heavy appliances during off-peak hours.",
                "Keep base load devices unplugged when not in active use."
            ]
        }
    elif power_kw <= HIGH_THRESHOLD:
        return {
            "class": "Normal Consumption",
            "css": "rec-normal",
            "badge_color": "#3b82f6",
            "icon": "🟡",
            "summary": "Standard Household Usage",
            "recommendation": "Your consumption aligns with typical household patterns. Keep monitoring daily usage to prevent shifting into the high tier.",
            "tips": [
                "Switch off standby electronics and entertainment setups overnight.",
                "Look for flexible appliance tasks that can be shifted away from the 8:00 PM peak."
            ]
        }
    else:
        return {
            "class": "High Consumption",
            "css": "rec-high",
            "badge_color": "#ef4444",
            "icon": "🔴",
            "summary": "High Energy Usage Alert!",
            "recommendation": "Review household activities on high-consumption days and actively look for avoidable electricity usage, especially in heating, cooling, and evening appliances.",
            "tips": [
                "Heavy load detected: Avoid running washing machine, dishwasher, or water heaters during the 7:00 PM - 9:00 PM peak.",
                "Sub-meter 3 (AC/Heater) consumes over 70% of appliance energy—adjust thermostat by 1-2 degrees to save significant energy.",
                "Check for high weekend usage (empirical data shows a +18% weekend surge)."
            ]
        }


# ==============================================================================
# HEADER
# ==============================================================================
st.markdown("<span class='badge'>FODS REVIEW 2 CASE STUDY</span>", unsafe_allow_html=True)
st.title("⚡ WattWise: Energy Recommendation System")
st.markdown(
    "A clean, data-driven recommendation engine based on statistical analysis of **2,075,259 household power readings** (UCI Repository). "
    "Daily usage is classified using data percentiles to provide actionable energy-saving guidance."
)
st.divider()


# ==============================================================================
# SECTION 1: INTERACTIVE RECOMMENDATION ENGINE
# ==============================================================================
st.markdown("## 🎯 Step 1: Check Your Household Consumption")
st.caption("Input an active power value or pick a historical date from the dataset to generate instant recommendations:")

col_input, col_result = st.columns([1.1, 1.4], gap="large")

with col_input:
    mode = st.radio(
        "Choose Input Method:",
        ["Manually Test Power Value (kW)", "Select a Date from Historical Dataset"],
        horizontal=True
    )
    
    selected_power = 1.250
    selected_date_str = ""
    
    if mode == "Manually Test Power Value (kW)":
        selected_power = st.slider(
            "Average Active Power (kW):",
            min_value=0.20,
            max_value=3.50,
            value=1.35,
            step=0.01,
            help="Average active power consumed in kilowatts"
        )
        st.write(f"👉 Current Reading: **{selected_power:.3f} kW**")
        st.caption(f"Thresholds: Low <= **{LOW_THRESHOLD:.2f} kW** | Normal: **{LOW_THRESHOLD:.2f} - {HIGH_THRESHOLD:.2f} kW** | High > **{HIGH_THRESHOLD:.2f} kW**")
    
    else:
        if daily_df is not None and "Date" in daily_df.columns:
            date_col = "Date"
            date_options = daily_df[date_col].dropna().tolist()
            chosen_date = st.selectbox("Select a Date:", date_options[-30:], index=len(date_options[-30:]) - 5)
            row = daily_df[daily_df[date_col] == chosen_date].iloc[0]
            selected_power = float(row["Mean_Active_Power_kW"])
            selected_date_str = f"Date: {chosen_date}"
            st.metric("Recorded Daily Average Power", f"{selected_power:.3f} kW")
        else:
            selected_power = 1.35
            st.info("Loading dataset dates...")

rec_data = get_recommendation(selected_power)

with col_result:
    st.markdown("### 📋 WattWise Recommendation")
    
    st.markdown(f"""
    <div class='recommendation-card {rec_data["css"]}'>
        <div style='font-size: 1.3rem; font-weight: 700; color: {rec_data["badge_color"]}; margin-bottom: 6px;'>
            {rec_data["icon"]} {rec_data["class"]}
        </div>
        <div style='font-size: 1.05rem; font-weight: 600; color: #ffffff; margin-bottom: 8px;'>
            {rec_data["summary"]} {f"({selected_date_str})" if selected_date_str else ""}
        </div>
        <p style='color: #e2e8f0; font-size: 0.98rem; line-height: 1.5; margin-bottom: 12px;'>
            <b>Action Plan:</b> {rec_data["recommendation"]}
        </p>
        <div style='font-weight: 600; font-size: 0.9rem; color: #9fb3c8; margin-bottom: 4px;'>Key Recommendations:</div>
        <ul style='margin-top: 0; padding-left: 20px; color: #cbd5e1;'>
            {''.join([f"<li>{tip}</li>" for tip in rec_data["tips"]])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()


# ==============================================================================
# SECTION 2: WHY THESE RULES? (THE FODS DATA SCIENCE EVIDENCE)
# ==============================================================================
st.markdown("## 🔍 Step 2: The Data Science Evidence Behind the Rules")
st.caption("How exploratory data analysis and hypothesis testing justified these recommendation thresholds:")

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>0.903 kW</div>
        <div class='stat-label'>33rd Percentile (Low Cutoff)</div>
    </div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>1.223 kW</div>
        <div class='stat-label'>67th Percentile (High Cutoff)</div>
    </div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>20:00 (8 PM)</div>
        <div class='stat-label'>Evening Peak Load (1.89 kW)</div>
    </div>
    """, unsafe_allow_html=True)
with s4:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>+17.95%</div>
        <div class='stat-label'>Weekend vs Weekday Surge (p &lt; 0.001)</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Visual comparison: Class distribution and 24-hour diurnal cycle
c_left, c_right = st.columns(2, gap="medium")

with c_left:
    st.markdown("### 📊 Balanced Consumption Classes")
    class_df = pd.DataFrame({
        "Class": ["Low_Consumption (<= 0.90 kW)", "Normal_Consumption (0.90 - 1.22 kW)", "High_Consumption (> 1.22 kW)"],
        "Observed Days": [481, 480, 481],
        "Mean Power (kW)": [0.660, 1.071, 1.543]
    })
    fig_class = px.bar(
        class_df,
        x="Class",
        y="Observed Days",
        color="Class",
        text_auto=True,
        title="Equal 3-Tier Class Distribution (33.3% Each)",
        color_discrete_sequence=["#22c55e", "#3b82f6", "#ef4444"]
    )
    fig_class.update_layout(showlegend=False, height=330, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    fig_class.update_xaxes(showgrid=False)
    fig_class.update_yaxes(gridcolor="rgba(160,185,210,0.1)")
    st.plotly_chart(fig_class, use_container_width=True)
    st.caption("Each tier contains ~481 days, ensuring unbiased, transparent categorization.")

with c_right:
    st.markdown("### ⏰ Daily 24-Hour Diurnal Pattern")
    if hour_df is not None and "Hour" in hour_df.columns:
        fig_h = px.line(
            hour_df.sort_values("Hour"),
            x="Hour",
            y="Mean_Active_Power_kW",
            markers=True,
            title="Hourly Mean Profile: Clear 8:00 PM Peak",
            labels={"Hour": "Hour of Day", "Mean_Active_Power_kW": "Active Power (kW)"}
        )
        fig_h.update_traces(line=dict(color="#70e1c1", width=3))
        fig_h.update_layout(height=330, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        fig_h.update_xaxes(showgrid=False)
        fig_h.update_yaxes(gridcolor="rgba(160,185,210,0.1)")
        st.plotly_chart(fig_h, use_container_width=True)
        st.caption("Peak demand at 20:00 (1.890 kW) is 4.19× the overnight minimum at 04:00 (0.451 kW).")
    else:
        st.info("Hourly summary table loading...")

st.write("")
st.divider()

# ==============================================================================
# FOOTER / PRESENTATION RECAP
# ==============================================================================
st.markdown("### 🎓 How to Explain this Project in Review 2 (1-Minute Pitch)")
st.markdown("""
1. **The Dataset:** We analyzed 2,075,259 minute-level electricity readings from the UCI Machine Learning repository over a 47-month period.
2. **The Problem:** Households need actionable, transparent feedback on when and how they consume energy without relying on black-box predictions.
3. **The Data Science Solution:** Using exploratory data analysis and empirical quantiles, we created the **WattWise Recommendation Engine**:
   - Classifies days into **Low** ($\le 0.90\text{ kW}$), **Normal** ($0.90 - 1.22\text{ kW}$), and **High** ($> 1.22\text{ kW}$) tiers.
   - Triggers targeted advice based on our statistical discovery that evening hours (8 PM) and weekends (+18% surge, Welch's $t=106.33, p<0.001$) drive the bulk of avoidable demand.
""")

st.caption("WattWise | Foundations of Data Science Review 2 | Built with Streamlit & Plotly")
