import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="European Bank Retention", layout="wide", page_icon="🏦")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def get_processed_data():
    df = pd.read_csv('European_Bank.csv')
    
    high_bal_thresh = df[df['Balance'] > 0]['Balance'].median()
    
    def assign_profile(row):
        active = row['IsActiveMember'] == 1
        products = row['NumOfProducts']
        high_bal = row['Balance'] > high_bal_thresh
        if active and products > 1: return 'Active Engaged'
        elif not active and high_bal: return 'Inactive High-Balance'
        elif active and products == 1: return 'Active Low-Product'
        elif not active and products == 1: return 'Inactive Disengaged'
        else: return 'Other Inactive'
    
    df['Engagement_Profile'] = df.apply(assign_profile, axis=1)
    df['Balance_to_Salary_Ratio'] = df['Balance'] / (df['EstimatedSalary'] + 0.01)
    df['Is_MultiProduct'] = df['NumOfProducts'] > 1
    df['RSI'] = (df['IsActiveMember'] * 0.5) + ((df['NumOfProducts']/4) * 0.5)
    
    return df

try:
    df = get_processed_data()
except Exception as e:
    st.error("Please ensure 'European_Bank.csv' is in the same directory.")
    st.stop()

st.sidebar.title("⚙️ Global Filters")
st.sidebar.markdown("Adjust parameters to dynamically filter the dashboard.")

engagement_filter = st.sidebar.radio(
    "Engagement Status", 
    ["All Customers", "Active Members", "Inactive Members"]
)

min_prod, max_prod = st.sidebar.slider(
    "Product Count Range", 
    min_value=1, max_value=4, value=(1, 4)
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Financial Thresholds**")
min_balance = st.sidebar.number_input("Minimum Balance (€)", min_value=0, value=0, step=10000)
min_salary = st.sidebar.number_input("Minimum Salary (€)", min_value=0, value=0, step=10000)

filtered_df = df.copy()

if engagement_filter == "Active Members":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 1]
elif engagement_filter == "Inactive Members":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 0]

filtered_df = filtered_df[
    (filtered_df['NumOfProducts'] >= min_prod) & 
    (filtered_df['NumOfProducts'] <= max_prod)
]
filtered_df = filtered_df[filtered_df['Balance'] >= min_balance]
filtered_df = filtered_df[filtered_df['EstimatedSalary'] >= min_salary]

st.title("🏦 Advanced Retention Analytics Engine")
st.markdown("Dynamically analyze customer behaviors, product impact, and retention strengths.")

if len(filtered_df) == 0:
    st.warning("No customers match the current filter criteria. Please adjust your sidebar settings.")
    st.stop()

st.header("🚨 High-Value Disengaged Detector")
top_quartile_bal = df['Balance'].quantile(0.75) # Use global Q3 for benchmark
at_risk_df = filtered_df[(filtered_df['Balance'] >= top_quartile_bal) & (filtered_df['IsActiveMember'] == 0)]

c1, c2, c3 = st.columns(3)
c1.metric("Total Customers in View", f"{len(filtered_df):,}")
c2.metric("Premium At-Risk Customers", f"{len(at_risk_df):,}", "Requires Intervention", delta_color="inverse")

if len(at_risk_df) > 0:
    risk_churn = at_risk_df['Exited'].mean() * 100
    c3.metric("At-Risk Segment Churn Rate", f"{risk_churn:.2f}%")
else:
    c3.metric("At-Risk Segment Churn Rate", "N/A")

st.markdown("---")

colA, colB = st.columns(2)

with colA:
    st.header("📊 Engagement vs Churn")
    eng_churn = filtered_df.groupby('IsActiveMember')['Exited'].mean().reset_index()
    eng_churn['IsActiveMember'] = eng_churn['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})
    eng_churn['Exited'] *= 100
    
    fig1 = px.bar(eng_churn, x='IsActiveMember', y='Exited', color='IsActiveMember',
                  title="Churn Rate by Activity Status", 
                  labels={'Exited': 'Churn Rate (%)', 'IsActiveMember': 'Status'},
                  color_discrete_map={'Active': '#2ca02c', 'Inactive': '#d62728'})
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.header("📦 Product Utilization Impact")
    prod_churn = filtered_df.groupby('NumOfProducts')['Exited'].mean().reset_index()
    prod_churn['Exited'] *= 100
    
    fig2 = px.line(prod_churn, x='NumOfProducts', y='Exited', markers=True,
                   title="The 'Product Cliff' Analysis", 
                   labels={'Exited': 'Churn Rate (%)', 'NumOfProducts': 'Number of Products Held'})
    fig2.update_traces(line_color='#1B3A6B', marker=dict(size=12, color='#D4A843'))
    # Add baseline annotation
    fig2.add_hline(y=df['Exited'].mean()*100, line_dash="dot", annotation_text="Global Baseline")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.header("🛡️ Retention Strength Scoring")
colC, colD = st.columns(2)

with colC:
    st.write("#### Profile Stickiness")
    profile_churn = filtered_df.groupby('Engagement_Profile')['Exited'].mean().sort_values(ascending=False).reset_index()
    profile_churn['Exited'] *= 100
    
    fig3 = px.bar(profile_churn, y='Engagement_Profile', x='Exited', orientation='h',
                  color='Exited', color_continuous_scale='RdYlGn_r',
                  title="Churn Rate by Engagement Persona",
                  labels={'Exited': 'Churn Rate (%)', 'Engagement_Profile': ''})
    st.plotly_chart(fig3, use_container_width=True)

with colD:
    st.write("#### Relationship Strength Index (RSI)")
    fig4 = px.histogram(filtered_df, x='RSI', color='Exited', barmode='group',
                        title="Distribution of RSI Scores",
                        color_discrete_map={0: '#2ca02c', 1: '#d62728'},
                        labels={'Exited': 'Churned (1) / Retained (0)'},
                        nbins=15)
    st.plotly_chart(fig4, use_container_width=True)