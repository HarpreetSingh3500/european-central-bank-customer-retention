import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Bank Retention Analytics",
    layout="wide",
    page_icon="🏦",
    initial_sidebar_state="expanded"
)

# ── Power BI-style CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}
.stApp {
    background-color: #f0f2f5;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1f3a 0%, #12162b 100%);
    border-right: 1px solid #2d3561;
}
[data-testid="stSidebar"] * {
    color: #c8cde8 !important;
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label {
    color: #8b92b8 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
[data-testid="stSidebar"] hr {
    border-color: #2d3561 !important;
}

/* ── Page header ── */
.page-header {
    background: linear-gradient(135deg, #1a1f3a 0%, #243580 100%);
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(26,31,58,0.18);
}
.page-header h1 {
    color: #ffffff !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    letter-spacing: -0.01em;
}
.page-header p {
    color: #8b9bd4 !important;
    font-size: 0.82rem !important;
    margin: 4px 0 0 !important;
}
.header-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 6px 16px;
    color: #ffffff !important;
    font-size: 0.78rem;
    font-weight: 600;
}

/* ── Section titles ── */
.section-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6b7280;
    margin: 28px 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e5e7eb;
}

/* ── KPI cards ── */
.kpi-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 20px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    border-top: 3px solid #3b55e6;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.kpi-card.green  { border-top-color: #16a34a; }
.kpi-card.red    { border-top-color: #dc2626; }
.kpi-card.amber  { border-top-color: #d97706; }
.kpi-card.blue   { border-top-color: #2563eb; }
.kpi-card.purple { border-top-color: #7c3aed; }

.kpi-card::after {
    content: '';
    position: absolute;
    right: -20px; bottom: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    background: rgba(59,85,230,0.05);
}
.kpi-card.green::after  { background: rgba(22,163,74,0.06); }
.kpi-card.red::after    { background: rgba(220,38,38,0.06); }
.kpi-card.amber::after  { background: rgba(217,119,6,0.06); }

.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9ca3af;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #111827;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi-sub {
    font-size: 0.74rem;
    color: #6b7280;
}
.kpi-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.68rem;
    font-weight: 700;
}
.kpi-badge.danger { background: #fee2e2; color: #dc2626; }
.kpi-badge.safe   { background: #dcfce7; color: #16a34a; }

/* ── Chart cards ── */
.chart-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 20px 22px 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}
.chart-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 2px;
}
.chart-subtitle {
    font-size: 0.72rem;
    color: #9ca3af;
    margin-bottom: 14px;
}

/* ── Insight pills ── */
.insight-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 8px;
}
.insight-pill {
    background: #f0f4ff;
    border: 1px solid #c7d3ff;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.72rem;
    color: #3b55e6;
    font-weight: 600;
}
.insight-pill.red   { background:#fff1f1; border-color:#fecaca; color:#dc2626; }
.insight-pill.green { background:#f0fdf4; border-color:#bbf7d0; color:#16a34a; }

/* ── Sidebar logo ── */
.sidebar-logo {
    text-align: center;
    padding: 20px 0 10px;
    margin-bottom: 10px;
}
.sidebar-logo-icon {
    font-size: 2.4rem;
}
.sidebar-logo-text {
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff !important;
    letter-spacing: -0.01em;
}
.sidebar-logo-sub {
    font-size: 0.68rem;
    color: #6b7aad !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── Warning / info box ── */
.info-box {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.8rem;
    color: #78350f;
}
</style>
""", unsafe_allow_html=True)

# ── Plotly base theme ────────────────────────────────────────────────────────
PLOT_BG    = "#ffffff"
GRID_COLOR = "#f3f4f6"
FONT_COLOR = "#374151"
ACCENT1    = "#2563eb"
ACCENT2    = "#16a34a"
ACCENT3    = "#dc2626"
ACCENT4    = "#d97706"
ACCENT5    = "#7c3aed"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=PLOT_BG,
    plot_bgcolor=PLOT_BG,
    font=dict(family="Segoe UI, Helvetica Neue, sans-serif", color=FONT_COLOR, size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    hoverlabel=dict(bgcolor="#1a1f3a", font_color="#ffffff",
                    font_family="Segoe UI", font_size=12,
                    bordercolor="#1a1f3a"),
)

# Base axis style — merge into per-chart axis dicts instead of passing separately
AXIS_BASE = dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                 tickfont=dict(size=10), title_font=dict(size=11))

def axis(title="", **kwargs):
    """Return a clean axis dict merged with base style."""
    return {**AXIS_BASE, "title": title, **kwargs}

LEGEND_DEFAULT = dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(size=10))

# ── Data ────────────────────────────────────────────────────────────────────
@st.cache_data
def get_processed_data():
    df = pd.read_csv('European_Bank.csv')
    high_bal_thresh = df[df['Balance'] > 0]['Balance'].median()

    def assign_profile(row):
        active    = row['IsActiveMember'] == 1
        products  = row['NumOfProducts']
        high_bal  = row['Balance'] > high_bal_thresh
        if active and products > 1:          return 'Active Engaged'
        elif not active and high_bal:        return 'Inactive High-Balance'
        elif active and products == 1:       return 'Active Low-Product'
        elif not active and products == 1:   return 'Inactive Disengaged'
        else:                                return 'Other Inactive'

    df['Engagement_Profile']    = df.apply(assign_profile, axis=1)
    df['Balance_to_Salary_Ratio'] = df['Balance'] / (df['EstimatedSalary'] + 0.01)
    df['Is_MultiProduct']       = df['NumOfProducts'] > 1
    df['RSI']                   = (df['IsActiveMember'] * 0.5) + ((df['NumOfProducts'] / 4) * 0.5)
    return df

try:
    df = get_processed_data()
except Exception:
    st.error("⚠️ Please ensure 'European_Bank.csv' is in the same directory.")
    st.stop()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🏦</div>
        <div class="sidebar-logo-text">RetentionIQ</div>
        <div class="sidebar-logo-sub">Analytics Engine</div>
    </div>
    <hr style="border-color:#2d3561; margin: 0 0 20px;">
    """, unsafe_allow_html=True)

    st.markdown("**ENGAGEMENT STATUS**")
    engagement_filter = st.radio(
        "", ["All Customers", "Active Members", "Inactive Members"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**PRODUCT COUNT RANGE**")
    min_prod, max_prod = st.slider("", min_value=1, max_value=4, value=(1, 4),
                                   label_visibility="collapsed")

    st.markdown("<hr style='border-color:#2d3561;'>", unsafe_allow_html=True)
    st.markdown("**FINANCIAL THRESHOLDS**")
    min_balance = st.number_input("Minimum Balance (€)", min_value=0, value=0, step=10000)
    min_salary  = st.number_input("Minimum Salary (€)",  min_value=0, value=0, step=10000)

    st.markdown("<hr style='border-color:#2d3561;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.68rem; color:#4a5380; text-align:center; padding:10px 0;">
        European Bank Dataset · 10,000 Records<br>
        Churn Analytics v2.0
    </div>""", unsafe_allow_html=True)

# ── Filtering ────────────────────────────────────────────────────────────────
filtered_df = df.copy()
if engagement_filter == "Active Members":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 1]
elif engagement_filter == "Inactive Members":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 0]
filtered_df = filtered_df[
    (filtered_df['NumOfProducts'] >= min_prod) &
    (filtered_df['NumOfProducts'] <= max_prod) &
    (filtered_df['Balance'] >= min_balance) &
    (filtered_df['EstimatedSalary'] >= min_salary)
]

# ── Page header ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-header">
    <div>
        <h1>🏦 Customer Retention Analytics Engine</h1>
        <p>European Bank · Churn Risk Intelligence Dashboard</p>
    </div>
    <div class="header-badge">📊 {len(filtered_df):,} Customers in View</div>
</div>
""", unsafe_allow_html=True)

if len(filtered_df) == 0:
    st.markdown('<div class="info-box">⚠️ No customers match the current filter criteria. Please adjust the sidebar settings.</div>', unsafe_allow_html=True)
    st.stop()

# ── KPI Row ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📌 Key Performance Indicators</div>', unsafe_allow_html=True)

top_quartile_bal = df['Balance'].quantile(0.75)
at_risk_df       = filtered_df[(filtered_df['Balance'] >= top_quartile_bal) & (filtered_df['IsActiveMember'] == 0)]

overall_churn  = filtered_df['Exited'].mean() * 100
active_churn   = filtered_df[filtered_df['IsActiveMember'] == 1]['Exited'].mean() * 100
inactive_churn = filtered_df[filtered_df['IsActiveMember'] == 0]['Exited'].mean() * 100
risk_churn     = at_risk_df['Exited'].mean() * 100 if len(at_risk_df) > 0 else 0
avg_rsi        = filtered_df['RSI'].mean()

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-label">Total Customers</div>
        <div class="kpi-value">{len(filtered_df):,}</div>
        <div class="kpi-sub">In current view</div>
    </div>""", unsafe_allow_html=True)

with k2:
    badge = "danger" if overall_churn > 20 else "safe"
    st.markdown(f"""
    <div class="kpi-card {'red' if overall_churn > 20 else 'green'}">
        <div class="kpi-label">Overall Churn Rate</div>
        <div class="kpi-value">{overall_churn:.1f}%</div>
        <div class="kpi-sub"><span class="kpi-badge {badge}">{'⚠ Above' if overall_churn > 20 else '✓ Below'} 20% threshold</span></div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card red">
        <div class="kpi-label">Premium At-Risk</div>
        <div class="kpi-value">{len(at_risk_df):,}</div>
        <div class="kpi-sub">High-balance · Inactive</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card amber">
        <div class="kpi-label">At-Risk Churn Rate</div>
        <div class="kpi-value">{risk_churn:.1f}%</div>
        <div class="kpi-sub">Premium segment only</div>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card purple">
        <div class="kpi-label">Avg RSI Score</div>
        <div class="kpi-value">{avg_rsi:.2f}</div>
        <div class="kpi-sub">Relationship Strength Index</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Engagement vs Churn | Product Cliff ───────────────────────────────
st.markdown('<div class="section-title">📊 Engagement & Product Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Churn Rate by Engagement Status</div>
        <div class="chart-subtitle">Active vs Inactive member churn comparison</div>
    """, unsafe_allow_html=True)

    eng_churn = filtered_df.groupby('IsActiveMember')['Exited'].mean().reset_index()
    eng_churn['Status'] = eng_churn['IsActiveMember'].map({1: 'Active', 0: 'Inactive'})
    eng_churn['Churn %'] = (eng_churn['Exited'] * 100).round(2)

    fig1 = go.Figure()
    colors = [ACCENT2 if s == 'Active' else ACCENT3 for s in eng_churn['Status']]
    fig1.add_trace(go.Bar(
        x=eng_churn['Status'], y=eng_churn['Churn %'],
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in eng_churn['Churn %']],
        textposition='outside', textfont=dict(size=13, color=FONT_COLOR),
        hovertemplate="<b>%{x}</b><br>Churn Rate: %{y:.2f}%<extra></extra>",
        width=0.45
    ))
    fig1.update_layout(**PLOTLY_LAYOUT, height=300, legend=LEGEND_DEFAULT,
                       xaxis=axis(), yaxis=axis("Churn Rate (%)", range=[0, max(eng_churn['Churn %'])*1.3]))
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    diff = abs(inactive_churn - active_churn)
    st.markdown(f"""
    <div class="insight-row">
        <span class="insight-pill red">Inactive churn {inactive_churn:.1f}%</span>
        <span class="insight-pill green">Active churn {active_churn:.1f}%</span>
        <span class="insight-pill">Δ {diff:.1f}pp gap</span>
    </div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">The "Product Cliff" Analysis</div>
        <div class="chart-subtitle">Churn rate spikes dramatically beyond 2 products</div>
    """, unsafe_allow_html=True)

    prod_churn = filtered_df.groupby('NumOfProducts')['Exited'].mean().reset_index()
    prod_churn['Churn %'] = (prod_churn['Exited'] * 100).round(2)
    global_baseline = df['Exited'].mean() * 100

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=prod_churn['NumOfProducts'], y=prod_churn['Churn %'],
        mode='lines+markers+text',
        line=dict(color=ACCENT1, width=3),
        marker=dict(size=12, color=prod_churn['Churn %'],
                    colorscale=[[0, ACCENT2], [0.4, ACCENT4], [1, ACCENT3]],
                    line=dict(color='white', width=2)),
        text=[f"{v:.0f}%" for v in prod_churn['Churn %']],
        textposition='top center', textfont=dict(size=11, color=FONT_COLOR),
        hovertemplate="<b>%{x} Products</b><br>Churn: %{y:.2f}%<extra></extra>",
        fill='tozeroy', fillcolor='rgba(37,99,235,0.06)'
    ))
    fig2.add_hline(y=global_baseline, line_dash="dot",
                   line=dict(color="#9ca3af", width=1.5),
                   annotation_text=f"Baseline {global_baseline:.1f}%",
                   annotation_position="bottom right",
                   annotation_font=dict(size=10, color="#9ca3af"))
    fig2.update_layout(**PLOTLY_LAYOUT, height=300, legend=LEGEND_DEFAULT,
                       xaxis=axis("Number of Products", tickmode='linear', dtick=1),
                       yaxis=axis("Churn Rate (%)"))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="insight-row">
        <span class="insight-pill green">2 products = safest zone</span>
        <span class="insight-pill red">3–4 products = cliff zone</span>
    </div>
    </div>""", unsafe_allow_html=True)

# ── Row 2: Persona stickiness | RSI distribution ────────────────────────────
st.markdown('<div class="section-title">🛡️ Retention Strength Analysis</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Churn Rate by Engagement Persona</div>
        <div class="chart-subtitle">Which customer profile is most at risk?</div>
    """, unsafe_allow_html=True)

    profile_churn = (filtered_df.groupby('Engagement_Profile')['Exited']
                     .mean().sort_values(ascending=True).reset_index())
    profile_churn['Churn %'] = (profile_churn['Exited'] * 100).round(2)

    colors_bar = []
    for v in profile_churn['Churn %']:
        if v < 15:   colors_bar.append(ACCENT2)
        elif v < 30: colors_bar.append(ACCENT4)
        else:        colors_bar.append(ACCENT3)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=profile_churn['Engagement_Profile'], x=profile_churn['Churn %'],
        orientation='h',
        marker=dict(color=colors_bar, line=dict(width=0)),
        text=[f"{v:.1f}%" for v in profile_churn['Churn %']],
        textposition='outside', textfont=dict(size=11),
        hovertemplate="<b>%{y}</b><br>Churn: %{x:.2f}%<extra></extra>",
    ))
    fig3.update_layout(**PLOTLY_LAYOUT, height=300, legend=LEGEND_DEFAULT,
                       xaxis=axis("Churn Rate (%)", range=[0, max(profile_churn['Churn %']) * 1.25]),
                       yaxis=axis(""))
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="insight-row">
        <span class="insight-pill green">🏆 Active Engaged = stickiest</span>
        <span class="insight-pill red">⚠ Inactive High-Balance = riskiest</span>
    </div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Relationship Strength Index (RSI) Distribution</div>
        <div class="chart-subtitle">RSI = 0.5×Activity + 0.5×(Products/4)</div>
    """, unsafe_allow_html=True)

    fig4 = go.Figure()
    for exited, label, color in [(0, 'Retained', ACCENT2), (1, 'Churned', ACCENT3)]:
        subset = filtered_df[filtered_df['Exited'] == exited]['RSI']
        fig4.add_trace(go.Histogram(
            x=subset, name=label,
            marker_color=color, opacity=0.8,
            nbinsx=15,
            hovertemplate=f"<b>{label}</b><br>RSI: %{{x:.2f}}<br>Count: %{{y}}<extra></extra>"
        ))
    fig4.update_layout(**PLOTLY_LAYOUT, height=300, barmode='group',
                       xaxis=axis("RSI Score"), yaxis=axis("Customer Count"),
                       legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                   xanchor="right", x=1))
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="insight-row">
        <span class="insight-pill green">High RSI → lower churn</span>
        <span class="insight-pill red">RSI = 0 → high churn risk</span>
    </div>
    </div>""", unsafe_allow_html=True)

# ── Row 3: Geography | Balance distribution ──────────────────────────────────
st.markdown('<div class="section-title">🌍 Geographic & Financial Breakdown</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Churn Rate by Country</div>
        <div class="chart-subtitle">Regional churn distribution</div>
    """, unsafe_allow_html=True)

    geo_churn = (filtered_df.groupby('Geography')['Exited']
                 .agg(['mean', 'count']).reset_index())
    geo_churn['Churn %'] = (geo_churn['mean'] * 100).round(2)

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=geo_churn['Geography'], y=geo_churn['Churn %'],
        marker=dict(
            color=geo_churn['Churn %'],
            colorscale=[[0, ACCENT2], [0.5, ACCENT4], [1, ACCENT3]],
            line=dict(width=0)
        ),
        text=[f"{v:.1f}%" for v in geo_churn['Churn %']],
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Churn: %{y:.2f}%<br>Customers: %{customdata:,}<extra></extra>",
        customdata=geo_churn['count'],
        width=0.45
    ))
    fig5.update_layout(**PLOTLY_LAYOUT, height=300, legend=LEGEND_DEFAULT,
                       xaxis=axis(), yaxis=axis("Churn Rate (%)", range=[0, max(geo_churn['Churn %']) * 1.3]))
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">Balance Distribution: Churned vs Retained</div>
        <div class="chart-subtitle">Does a higher balance reduce churn risk?</div>
    """, unsafe_allow_html=True)

    fig6 = go.Figure()
    for exited, label, color in [(0, 'Retained', ACCENT2), (1, 'Churned', ACCENT3)]:
        subset = filtered_df[filtered_df['Exited'] == exited]['Balance']
        fig6.add_trace(go.Violin(
            y=subset, name=label,
            box_visible=True, meanline_visible=True,
            fillcolor=color, opacity=0.7,
            line_color='white',
            hovertemplate=f"<b>{label}</b><br>Balance: €%{{y:,.0f}}<extra></extra>"
        ))
    fig6.update_layout(**PLOTLY_LAYOUT, height=300, legend=LEGEND_DEFAULT,
                       xaxis=axis(), yaxis=axis("Account Balance (€)"),
                       violingap=0.3, violinmode='group')
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""
    <div class="insight-row">
        <span class="insight-pill">High balance ≠ loyalty without engagement</span>
    </div>
    </div>""", unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#d1d5db; font-size:0.72rem; padding:30px 0 10px;">
    RetentionIQ Analytics Engine · European Bank Dataset · 10,000 Records
</div>""", unsafe_allow_html=True)
