
# US Mental Health Trends Dashboard (2019–2022)

An interactive data visualization dashboard analyzing mental health trends 
across all 50 U.S. states using CDC public health data. Built with Dash + 
Plotly and deployed on Render.

🔗 **Live App:** [https://mental-health-trends.onrender.com](https://mental-health-trends.onrender.com) 

---

## Project Overview

This project analyzes how mental health conditions changed across the United 
States during the COVID-19 pandemic (2019–2022), using CDC Chronic Disease 
Indicators data covering 300,000+ records across 50 states.

---
## Key Findings

- **West Virginia** had the highest mental health prevalence (~19%) in 2022
- **Females** reported significantly higher distress rates than males across all 50 states
- **Age group 18–44** was the most affected demographic
- **Seniors (65+)** showed the lowest mental health distress rates
- **Multiracial and American Indian/Alaska Native** groups had highest racial disparities
- **Mental health distress increased** during COVID (2020–2022) compared to pre-COVID (2019)
- **Southern and Appalachian states** (TN, AR, LA, WV) consistently showed highest prevalence
- **California and Nebraska** showed lowest prevalence rates nationally

---
##  Data Source
- **Primary Dataset:** [CDC Chronic Disease Indicators](https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators/hksd-2xuw)  
- **Alternate Access:** [CDC Chronic Disease Data Portal](https://www.cdc.gov/chronicdisease/data/index.htm)
- **Records:** 309,215 rows, 34 columns across 50 states
- **Years:** 2019–2022
- **Topic:** Mental Health indicators including depression, frequent mental distress, and postpartum depressive symptoms

---

## Dashboard Features

-  **Interactive Choropleth Map** — state-wise mental health prevalence across 50 states
-  **Trend Line Chart** — year-over-year prevalence for any selected state
- **Demographic Breakdown** — insights by age group, sex, and race/ethnicity
- **Pre vs During COVID Comparison** — visual impact of pandemic on mental health
- **Dynamic Dropdowns** — filter by condition and state instantly

---

## Tech Stack

| Purpose | Tool |
|---|---|
| Dashboard & Visualization | Dash, Plotly |
| Data Processing | Pandas, NumPy |
| Static Visualizations | Matplotlib, Seaborn |
| Deployment | Render |
| Version Control | Git + GitHub |

## 💡 Key Learnings

- Built scalable interactive dashboards using Dash  
- Applied exploratory data analysis on large public datasets (300K+ records)  
- Identified real-world trends and disparities in public health data  
- Strengthened data storytelling and visualization skills  

## Deployment

Deployed on **Render** with:

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn dashboard.app:server`
