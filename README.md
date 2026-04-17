# 🏦 European Bank Customer Retention & Churn Analytics Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75)

## 📌 Project Overview
Despite having vast amounts of data on customer engagement and product usage, retail banks often struggle with generic and misaligned retention strategies. This project provides a quantitative, data-driven analytical engine to uncover exactly which behaviors drive retention, pinpointing the threshold where product depth becomes a liability, and proving whether high account balances truly ensure loyalty.

This repository contains both a rigorous **5-Step Analytical Pipeline** (Jupyter Notebook) and an **Interactive Web Dashboard** (Streamlit) designed for business stakeholders to explore customer churn risks dynamically.

---

## 🎯 Problem Statement & Objectives

### The Problem
Banks frequently lack:
* Quantitative insight into which behaviors drive retention.
* Clarity on whether product depth reduces churn.
* Evidence on whether high balances alone ensure loyalty.

### Primary Objectives
* Evaluate the relationship between engagement and churn.
* Measure the retention impact of product count and product mix.
* Identify disengaged yet high-value customers.

### Secondary Objectives
* Support engagement-driven retention strategies.
* Improve product bundling decisions.
* Reduce "silent churn" among premium customers.

---

## 💡 Key Business Insights Discovered

1. **The "More is Better" Myth is False:** Data proves that holding 3 or 4 products exponentially increases churn (82% - 100%). Aggressive cross-selling past 2 products is a massive retention risk.
2. **The Premium At-Risk Segment:** Over 1,200 high-balance customers were identified as completely inactive, churning at over 30%. A high balance does *not* guarantee loyalty without active engagement.
3. **Engagement is the Ultimate Moat:** Inactive customers are drastically more likely to churn than active ones, generating an "Engagement Retention Ratio" that proves existing customer activation is more valuable than new customer acquisition.
4. **The "Sticky" Persona:** The most loyal segment is the "Active Engaged" group (Active members holding exactly 2 products), featuring a churn rate safely below 10%.

---

## 🔬 Analytical Methodology
The analysis was conducted using a strict 5-step data science methodology:

1. **Data Ingestion & Validation:** Loaded dataset, validated engagement/product fields, ensured binary variables consistency, and confirmed churn labeling accuracy.
2. **Engagement Classification:** Engineered specific customer personas: *Active Engaged, Inactive Disengaged, Active Low-Product, and Inactive High-Balance*.
3. **Product Utilization Analysis:** Calculated churn rates by product depth, revealing the single-product vs. multi-product retention cliff.
4. **Financial Commitment vs. Engagement:** Conducted balance vs. activity cross-analysis and detected salary-balance mismatches to identify "at-risk premium customers."
5. **Retention Strength Assessment:** Defined sticky customer profiles and measured churn stability across all engagement tiers.

---

## 🖥️ Streamlit Dashboard Features
The included `app.py` file powers an interactive web application featuring:
* **High-Value Disengaged Customer Detector:** Real-time calculation of premium users at risk of churning.
* **Product Utilization Impact:** Interactive visual of the "Product Cliff."
* **Retention Strength Scoring:** Breakdown of custom KPIs including the engineered *Relationship Strength Index (RSI)*.
* **Dynamic User Capabilities:** Global sidebar filters for Engagement Status, Product Count, Minimum Balance, and Minimum Salary thresholds.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn, Plotly Express
* **Web App Framework:** Streamlit
* **Environment:** Jupyter Notebook

---

### 📁 Repository Structure
├── analysis.ipynb          # Comprehensive EDA, KPI engineering, and modeling notebook <br>
├── app.py                  # Streamlit dashboard application <br>
├── European_Bank.csv       # Raw dataset (10,000 records) <br>
├── requirements.txt        # Python dependencies <br>
└── README.md               # Project documentation <br>

## 🚀 Installation & Usage

### 1. Clone the repository
git clone https://github.com/HarpreetSingh3500/european-central-bank-customer-retention/tree/main

cd customer-retention-dashboard

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the Jupyter Notebook (For Data Scientists)
jupyter notebook analysis.ipynb

### 4.Launch the Streamlit Dashboard (For Business Users)
streamlit run app.py

### Conclusion
This project reframes customer churn from a behavioral and relationship-strength perspective. By focusing on engagement and product utilization rather than demographics, it provides actionable insights for retention strategy design, product optimization, and customer loyalty enhancement.
