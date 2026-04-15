"""
TSMC ESG Analytics Dashboard — Streamlit Edition
SAM 503 · Lab 4 · Stuart Business School, Illinois Tech
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="TSMC ESG Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────

YEARS = [2020, 2021, 2022, 2023, 2024]

data = {
    "scope1":            [2_004_841, 2_151_937, 2_018_789, 1_596_031, 1_825_872],
    "scope2_market":     [7_459_856, 8_152_497, 9_539_765, 10_187_387, 10_957_397],
    "scope2_location":   [8_282_509, 9_196_964, 10_887_145, 11_466_118, 12_674_921],
    "scope3":            [5_511_486, 6_049_256, 7_429_158, 7_616_655, 8_223_173],
    "carbon_intensity":  [197.78, 181.34, 152.32, 170.05, 144.82],
    "total_energy":      [16_919, 19_192, 22_423, 24_775, 27_477],
    "renewable_pct":     [7.6, 9.2, 10.4, 11.2, 14.1],
    "water_withdrawal":  [77.3, 82.8, 105.0, 113.6, 128.8],
    "water_recycled":    [86.4, 85.4, 85.7, 90.3, 88.1],
    "waste_total":       [575_740, 674_703, 744_019, 656_841, 789_208],
    "waste_diversion":   [95.0, 95.0, 96.0, 96.0, 97.0],
    "waste_hazardous":   [298_400, 339_623, 401_215, 371_236, 445_152],
    "employees":         [56_831, 65_152, 73_090, 76_478, 83_825],
    "turnover":          [5.1, 6.7, 6.5, 3.5, 3.4],
    "training_hrs":      [16.3, 48.9, 69.5, 85.4, 100.5],
    "women_workforce":   [37.1, 35.4, 34.4, 34.2, 33.7],
    "women_mgmt":        [10.0, 8.3, 6.1, 5.9, 11.4],
    "women_board":       [10.0, 10.0, 10.0, 10.0, 20.0],
    "trir":              [0.311, 0.252, 0.145, 0.156, 0.133],
    "board_independent": [60, 60, 60, 60, 70],
    "revenue":           [47_855, 57_848, 75_881, 69_295, 88_268],
    "ebitda_margin":     [63.0, 64.0, 69.0, 65.0, 69.0],
    "capex":             [17_186, 30_072, 36_342, 30_442, 29_755],
    "rd_spend":          [3_695, 4_480, 5_469, 5_844, 6_227],
}

df = pd.DataFrame(data, index=YEARS)
df.index.name = "Year"

# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────

C = dict(
    bg       = "#0d1117",
    surface  = "#161b22",
    card     = "#1c2128",
    border   = "#30363d",
    green    = "#3fb950",
    teal     = "#00b4d8",
    blue     = "#58a6ff",
    amber    = "#d29922",
    red      = "#f85149",
    purple   = "#bc8cff",
    text     = "#e6edf3",
    muted    = "#8b949e",
    scope1   = "#f85149",
    scope2   = "#d29922",
    scope3   = "#bc8cff",
    renew    = "#3fb950",
    nonrenew = "#30363d",
)

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, Segoe UI, Arial, sans-serif", color=C["text"], size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(gridcolor=C["border"], tickfont=dict(color=C["muted"])),
    yaxis=dict(gridcolor=C["border"], tickfont=dict(color=C["muted"])),
    hovermode="x unified",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Dark sidebar */
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }

/* Main background */
.main .block-container { padding-top: 1.5rem; max-width: 1400px; }

/* Section headers */
.section-header {
    font-size: 11px; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; color: #58a6ff;
    border-bottom: 1px solid #30363d;
    padding-bottom: 6px; margin: 24px 0 12px 0;
}

/* Insight banner */
.insight-banner {
    background: rgba(88,166,255,0.08);
    border: 1px solid #58a6ff;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 16px;
}
.insight-banner .label {
    color: #58a6ff; font-size: 11px; text-transform: uppercase;
    letter-spacing: 0.06em; margin-bottom: 6px;
}
.insight-banner p { color: #e6edf3; font-size: 13px; line-height: 1.6; margin: 0; }

/* Metric tiles */
[data-testid="stMetric"] {
    background: #1c2128;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 12px 16px;
}
[data-testid="stMetricLabel"] { font-size: 11px !important; color: #8b949e !important; }
[data-testid="stMetricValue"] { font-size: 24px !important; }

/* Governance checklist */
.gov-list { list-style: none; padding: 0; margin: 0; }
.gov-list li { padding: 6px 0; font-size: 13px; color: #e6edf3; }
.gov-list li::before { content: "✓"; color: #3fb950; margin-right: 10px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR CONTROLS
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🌿 TSMC ESG Dashboard")
    st.markdown(
        "<small style='color:#8b949e'>SAM 503 · Lab 4<br>"
        "Stuart Business School · Illinois Tech</small>",
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("### Filters")
    year_range = st.slider(
        "Year Range", min_value=2020, max_value=2024,
        value=(2020, 2024), step=1,
    )

    pillar = st.radio(
        "ESG Pillar",
        options=["All", "Environmental", "Social", "Governance", "Financial"],
        index=0,
    )

    st.divider()
    st.markdown(
        "<small style='color:#8b949e'>"
        "**Data sources**<br>"
        "TSMC 2024 Sustainability Report<br>"
        "Frameworks: GRI · TCFD · SASB<br>"
        "Assurance: DNV Business Assurance<br><br>"
        "**ESG Ratings (2024)**<br>"
        "MSCI ESG: AAA<br>"
        "DJSI World: 25 consecutive years<br>"
        "CDP Climate & Water: B-<br>"
        "ISS ESG: Prime"
        "</small>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────

y0, y1 = year_range
dff = df.loc[y0:y1]
xs  = list(dff.index)

latest = dff.iloc[-1]
prev   = dff.iloc[-2] if len(dff) > 1 else dff.iloc[-1]

show_e = pillar in ("All", "Environmental")
show_s = pillar in ("All", "Social")
show_g = pillar in ("All", "Governance")
show_f = pillar in ("All", "Financial")

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────

st.markdown(
    "<h1 style='font-size:26px; font-weight:800; margin:0; color:#e6edf3;'>"
    "<span style='color:#58a6ff'>TSMC</span>  ESG Analytics Dashboard</h1>"
    "<p style='color:#8b949e; font-size:12px; margin:4px 0 0 0; "
    "letter-spacing:0.04em;'>Taiwan Semiconductor Manufacturing Company · "
    "Reporting Framework: GRI · TCFD · SASB · WEF IBC SCM</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ─────────────────────────────────────────────
# KPI SCORECARDS
# ─────────────────────────────────────────────

ghg_latest = (latest["scope1"] + latest["scope2_market"]) / 1e6
ghg_prev   = (prev["scope1"]   + prev["scope2_market"])   / 1e6
ghg_delta  = ghg_latest - ghg_prev

cols = st.columns(6)
cols[0].metric("GHG Emissions (S1+S2)",
               f"{ghg_latest:.1f} Mt",
               f"{ghg_delta:+.2f} Mt YoY",
               delta_color="inverse")
cols[1].metric("Renewable Energy",
               f"{latest['renewable_pct']:.1f}%",
               f"{latest['renewable_pct'] - prev['renewable_pct']:+.1f}pp YoY",
               delta_color="normal")
cols[2].metric("Safety (TRIR)",
               f"{latest['trir']:.3f}",
               f"{latest['trir'] - prev['trir']:+.3f} YoY",
               delta_color="inverse")
cols[3].metric("Annual Revenue",
               f"${latest['revenue']:,.0f}M",
               f"{(latest['revenue']-prev['revenue'])/prev['revenue']*100:+.1f}% YoY",
               delta_color="normal")
cols[4].metric("Total Employees",
               f"{int(latest['employees']):,}",
               f"{int(latest['employees']-prev['employees']):+,} YoY",
               delta_color="normal")
cols[5].metric("Training Hrs/Employee",
               f"{latest['training_hrs']:.1f} hrs",
               f"{latest['training_hrs']-prev['training_hrs']:+.1f} YoY",
               delta_color="normal")

# ─────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────

def _base(**kwargs):
    layout = {**CHART_LAYOUT, **kwargs}
    return layout

def plot(fig, title="", height=320):
    fig.update_layout(**_base(
        title=dict(text=title, font=dict(size=13, color=C["text"])),
        height=height,
    ))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# ── ENVIRONMENTAL ────────────────────────────
# ─────────────────────────────────────────────

if show_e:
    st.markdown('<div class="section-header">🌿  Environmental</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        fig = go.Figure()
        for values, color, name in [
            (dff["scope1"]/1e6, C["scope1"], "Scope 1"),
            (dff["scope2_market"]/1e6, C["scope2"], "Scope 2 (Market)"),
            (dff["scope3"]/1e6, C["scope3"], "Scope 3"),
        ]:
            fig.add_trace(go.Scatter(
                x=xs, y=list(values), name=name, mode="lines+markers",
                line=dict(width=2, color=color), marker=dict(size=6),
            ))
        target = (data["scope1"][0] + data["scope2_market"][0]) / 1e6
        fig.add_shape(type="line", x0=xs[0], x1=xs[-1], y0=target, y1=target,
                      line=dict(color=C["green"], width=1.5, dash="dot"))
        fig.add_annotation(x=xs[-1], y=target, text="2030 Target",
                           showarrow=False, font=dict(color=C["green"], size=10),
                           xanchor="right", yanchor="bottom")
        fig.update_layout(yaxis_title="Million MT CO₂e")
        plot(fig, "GHG Emissions by Scope (Mt CO₂e)")

    with col_b:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=xs, y=list(dff["carbon_intensity"]),
            name="Carbon Intensity", mode="lines+markers",
            fill="tozeroy", fillcolor="rgba(210,153,34,0.10)",
            line=dict(color=C["amber"], width=2), marker=dict(size=8),
        ))
        fig.update_layout(yaxis_title="MT CO₂e / $M Revenue")
        plot(fig, "Carbon Intensity (MT CO₂e per $M Revenue)")

    col_c, col_d = st.columns(2)

    with col_c:
        renewable_gwh = [e * r / 100 for e, r in zip(dff["total_energy"], dff["renewable_pct"])]
        nonrenew_gwh  = [e - r for e, r in zip(dff["total_energy"], renewable_gwh)]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=xs, y=nonrenew_gwh, name="Non-Renewable",
                              marker_color=C["nonrenew"]), secondary_y=False)
        fig.add_trace(go.Bar(x=xs, y=renewable_gwh, name="Renewable",
                              marker_color=C["renew"]), secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=list(dff["renewable_pct"]),
                                  name="RE %", mode="lines+markers",
                                  line=dict(color=C["teal"], width=2),
                                  marker=dict(size=7)), secondary_y=True)
        fig.add_shape(type="line", x0=xs[0], x1=xs[-1], y0=60, y1=60,
                      line=dict(color=C["teal"], width=1.2, dash="dot"),
                      yref="y2", xref="x")
        fig.add_annotation(x=xs[-1], y=60, text="RE60 (2030)", showarrow=False,
                           font=dict(color=C["teal"], size=10),
                           xanchor="right", yanchor="bottom", yref="y2")
        fig.update_layout(barmode="stack", yaxis_title="GWh", yaxis2_title="RE %")
        plot(fig, "Energy Mix & Renewable % (GWh)")

    with col_d:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=xs, y=list(dff["water_withdrawal"]),
                              name="Withdrawal (M MT)",
                              marker_color=C["blue"]), secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=list(dff["water_recycled"]),
                                  name="Recycling Rate %", mode="lines+markers",
                                  line=dict(color=C["teal"], width=2),
                                  marker=dict(size=7)), secondary_y=True)
        fig.update_layout(yaxis_title="Million MT", yaxis2_title="Recycle %")
        plot(fig, "Water Withdrawal & Recycling Rate")

    non_haz = [t - h for t, h in zip(dff["waste_total"], dff["waste_hazardous"])]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=xs, y=list(dff["waste_hazardous"]),
                          name="Hazardous", marker_color=C["red"]))
    fig.add_trace(go.Bar(x=xs, y=non_haz,
                          name="Non-Hazardous", marker_color=C["amber"]))
    fig.update_layout(barmode="stack", yaxis_title="Metric Tonnes")
    plot(fig, "Waste Generated by Type (MT)", height=280)

# ─────────────────────────────────────────────
# ── SOCIAL ───────────────────────────────────
# ─────────────────────────────────────────────

if show_s:
    st.markdown('<div class="section-header">👥  Social</div>', unsafe_allow_html=True)

    col_e, col_f = st.columns(2)

    with col_e:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=xs, y=list(dff["employees"]),
                              name="Total Employees",
                              marker_color=C["blue"], opacity=0.8), secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=list(dff["turnover"]),
                                  name="Voluntary Turnover %", mode="lines+markers",
                                  line=dict(color=C["amber"], width=2),
                                  marker=dict(size=7)), secondary_y=True)
        fig.update_layout(yaxis_title="Employees", yaxis2_title="Turnover %")
        plot(fig, "Headcount & Voluntary Turnover Rate")

    with col_f:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=xs, y=list(dff["training_hrs"]),
                              name="Training Hrs/Employee",
                              marker_color=C["purple"], opacity=0.8), secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=list(dff["trir"]),
                                  name="TRIR", mode="lines+markers",
                                  line=dict(color=C["red"], width=2),
                                  marker=dict(size=7)), secondary_y=True)
        fig.update_layout(yaxis_title="Avg Hours / Employee", yaxis2_title="TRIR")
        plot(fig, "Safety (TRIR) & Training Hours")

    fig = go.Figure()
    for values, color, name in [
        (dff["women_workforce"], C["teal"],   "Women in Workforce %"),
        (dff["women_mgmt"],     C["purple"],  "Women in Management %"),
        (dff["women_board"],    C["green"],   "Women on Board %"),
    ]:
        fig.add_trace(go.Scatter(x=xs, y=list(values), name=name,
                                  mode="lines+markers",
                                  line=dict(width=2, color=color),
                                  marker=dict(size=7)))
    fig.update_layout(yaxis_title="%")
    plot(fig, "Gender Diversity Across Levels (%)", height=280)

# ─────────────────────────────────────────────
# ── GOVERNANCE ───────────────────────────────
# ─────────────────────────────────────────────

if show_g:
    st.markdown('<div class="section-header">🏛  Governance</div>', unsafe_allow_html=True)

    col_g, col_h = st.columns(2)

    with col_g:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=list(dff["board_independent"]),
                                  name="Board Independence %", mode="lines+markers",
                                  line=dict(color=C["blue"], width=2),
                                  marker=dict(size=7)))
        fig.add_trace(go.Scatter(x=xs, y=list(dff["women_board"]),
                                  name="Women on Board %", mode="lines+markers",
                                  line=dict(color=C["green"], width=2),
                                  marker=dict(size=7)))
        fig.update_layout(yaxis=dict(range=[0, 100], gridcolor=C["border"],
                                     tickfont=dict(color=C["muted"])),
                          yaxis_title="%")
        plot(fig, "Board Composition (%)")

    with col_h:
        st.markdown("**Governance Highlights**")
        highlights = [
            "70% board independence (2024)",
            "20% women on board — doubled YoY",
            "ESG metrics linked to executive compensation",
            "DNV third-party ESG assurance",
            "MSCI ESG Rating: **AAA**",
            "DJSI World Index — **25 consecutive years**",
            "CDP Climate & Water: B-",
            "ISS ESG **Prime** rating",
            "100% Tier-1 suppliers completed sustainability SAQ",
            "100% significant suppliers received RBA audits",
        ]
        for h in highlights:
            st.markdown(f"✅ {h}")

# ─────────────────────────────────────────────
# ── FINANCIAL ────────────────────────────────
# ─────────────────────────────────────────────

if show_f:
    st.markdown('<div class="section-header">💰  Financial Performance</div>', unsafe_allow_html=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=xs, y=list(dff["revenue"]),
                          name="Revenue", marker_color=C["blue"], opacity=0.85), secondary_y=False)
    fig.add_trace(go.Bar(x=xs, y=list(dff["capex"]),
                          name="CapEx", marker_color=C["amber"], opacity=0.85), secondary_y=False)
    fig.add_trace(go.Bar(x=xs, y=list(dff["rd_spend"]),
                          name="R&D Spend", marker_color=C["purple"], opacity=0.85), secondary_y=False)
    fig.add_trace(go.Scatter(x=xs, y=list(dff["ebitda_margin"]),
                              name="EBITDA Margin %", mode="lines+markers",
                              line=dict(color=C["green"], width=2),
                              marker=dict(size=7)), secondary_y=True)
    fig.update_layout(barmode="group",
                      yaxis_title="USD Million", yaxis2_title="EBITDA Margin %")
    plot(fig, "Revenue, CapEx & R&D Spend ($M) with EBITDA Margin", height=340)

# ─────────────────────────────────────────────
# INSIGHT BANNER
# ─────────────────────────────────────────────

st.markdown("---")
st.info(
    "📌 **Key Insight —** TSMC is the indispensable engine of the global chip economy — "
    "delivering record revenue ($88.3B), industry-leading worker safety (TRIR 0.133), and "
    "accelerating renewable energy adoption (14.1%) — yet its absolute GHG emissions grew 8% "
    "in 2024, revealing that the race between capacity expansion and decarbonization remains "
    "the defining ESG challenge investors must monitor."
)
