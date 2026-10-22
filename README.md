# WattWise: Household Energy Recommendation System
### Foundations of Data Science (FODS) — Review 2 Case Study

## 📌 Project Overview
This project presents **WattWise**, an empirical energy recommendation engine built on **2,075,259 household power readings** (UCI Machine Learning Repository).

Instead of an opaque machine-learning model, WattWise uses transparent data percentiles to classify household energy use and provide actionable efficiency recommendations:
- **Low Consumption ($\le 0.903\text{ kW}$):** Top 33% most efficient days — *Maintain current habits.*
- **Normal Consumption ($0.903 - 1.223\text{ kW}$):** Middle 33% — *Standard usage; monitor standby devices.*
- **High Consumption ($> 1.223\text{ kW}$):** Top 33% highest consumption — *High load alert; shift evening appliances.*

---

## 📁 Folder Contents
- **`Household_Electricity_Consumption_FODS.ipynb`** — Complete Jupyter notebook with preprocessing, EDA, 15 research questions, hypothesis testing, and Power BI / WattWise sections.
- **`streamlit_app.py`** — Simple, interactive recommendation web deployment.
- **`powerbi_exports/`** — 9 clean CSV tables generated from the notebook for Power BI and Streamlit.
- **`POWERBI_DASHBOARD_GUIDE.md`** — Power BI Star Schema, DAX measures, and setup instructions.
- **`run_streamlit.bat`** — One-click launcher to run the Streamlit app.
- **`requirements.txt`** — Dependencies (`streamlit`, `pandas`, `plotly`).

---

## 🚀 How to Run the Recommendation App
Double-click `run_streamlit.bat`, or in terminal:
```bash
python -m streamlit run streamlit_app.py
```
*(Opens in your browser at `http://localhost:8501`)*

---

## 🎤 How to Explain in Review 2 (1-Minute Pitch)
1. **The Data:** 2,075,259 continuous minute-level records spanning 47 months.
2. **The Problem:** Households need understandable energy feedback rather than complex black-box predictions.
3. **The Data Science Discovery:**
   - 33rd percentile ($0.903\text{ kW}$) and 67th percentile ($1.223\text{ kW}$) divide days into three equal, balanced categories (481 days each).
   - Peak usage occurs at **8:00 PM** (1.890 kW), which is 4.19× the overnight base load (0.451 kW at 4:00 AM).
   - Weekend usage surges by **+17.95%** ($p < 0.001$, Welch's t-test).
4. **The Recommendation System:** WattWise takes any power reading or historical date and gives customized advice targeting peak evening and weekend energy loads.
