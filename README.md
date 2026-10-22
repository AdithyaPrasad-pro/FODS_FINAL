# WattWise: Household Energy Recommendation System
### Foundations of Data Science (FODS) — Review 2 Case Study

## 📌 Project Overview
**WattWise** is an empirical energy recommendation engine built on **2,075,259 household power readings** (UCI Machine Learning Repository).

Instead of an opaque machine-learning model, WattWise uses transparent data percentiles to classify household energy use and provide actionable efficiency recommendations:
- **Low Consumption ($\le 0.903\text{ kW}$):** Top 33% most efficient observations — *Maintain current habits.*
- **Normal Consumption ($0.903 - 1.223\text{ kW}$):** Middle 33% median profile — *Standard usage; monitor standby devices.*
- **High Consumption ($> 1.223\text{ kW}$):** Top 33% highest consumption — *High load alert; shift evening appliances.*

---

## 📁 Repository Structure
- **`Household_Electricity_Consumption_FODS.ipynb`** — Complete Jupyter notebook with preprocessing, EDA, 15 research questions, hypothesis testing, and Power BI / WattWise sections.
- **`streamlit_app.py`** — Interactive recommendation web deployment.
- **`powerbi_exports/`** — 9 clean CSV tables generated from the notebook for Power BI and Streamlit.
- **`POWERBI_DASHBOARD_GUIDE.md`** — Power BI Star Schema, DAX measures, and setup instructions.
- **`run_streamlit.bat`** — One-click launcher to run the Streamlit app.
- **`requirements.txt`** — Dependencies (`streamlit`, `pandas`, `plotly`).

---

## 🚀 Execution Instructions
Run via terminal:
```bash
python -m streamlit run streamlit_app.py
```
*(Opens in your browser at `http://localhost:8501`)*

---

## 🔬 Core Empirical Findings
1. **Dataset Coverage:** 2,075,259 continuous minute-level records spanning 47 months.
2. **Quantile Boundaries:**
   - 33rd percentile ($0.903\text{ kW}$) and 67th percentile ($1.223\text{ kW}$) divide days into three balanced categories (481 days each).
3. **Diurnal Concentration:**
   - Peak usage occurs at **8:00 PM** (1.890 kW), which is 4.19× the overnight base load (0.451 kW at 4:00 AM).
4. **Statistical Hypothesis Testing:**
   - Weekend usage surges by **+17.95%** ($p < 0.001$, Welch's t-test, $t = 106.33$).
5. **Recommendation Engine:** WattWise provides customized, data-backed advice targeting peak evening and weekend energy loads.
