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
    "scope3":            [5_511_486, 6_049_256, 7_429_158, 7_616_655, 8_223_173],
    "carbon_intensity":  [197.78, 181.34, 152.32, 170.05, 144.82],
    "total_energy":      [16_919, 19_192, 22_423, 24_775, 27_477],
    "renewable_pct":     [7.6, 9.2, 10.4, 11.2, 14.1],
    "water_withdrawal":  [77.3, 82.8, 105.0, 113.6, 128.8],
    "water_recycled":    [86.4, 85.4, 85.7, 90.3, 88.1],
    "waste_total":       [575_740, 674_703, 744_019, 656_841, 789_208],
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
# COLOURS
# ─────────────────────────────────────────────

C = dict(
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
    nonrenew = "#30363d",
)

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=C["text"], size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    xaxis=dict(gridcolor=C["border"], tickfont=dict(color=C["muted"])),
    yaxis=dict(gridcolor=C["border"], tickfont=dict(color=C["muted"])),
    hovermode="x unified",
)

# ─────────────────────────────────────────────
# CSS  — no external font requests
# ─────────────────────────────────────────────

st.markdown("""
<style>
[data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #30363d; }
[data-testid="stMetric"]  { background: #1c2128; border: 1px solid #30363d;
                             border-radius: 10px; padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🌿 TSMC ESG Dashboard")
    st.caption("SAM 503 · Lab 4 · Stuart Business School · Illinois Tech")
    st.divider()

    year_range = st.slider("Year Range", 2020, 2024, (2020, 2024), step=1)

    pillar = st.radio(
        "ESG Pillar",
        ["All", "Environmental", "Social", "Governance", "Financial"],
    )

    st.divider()
    st.caption(
        "**Data:** TSMC 2024 Sustainability Report\n\n"
        "**Frameworks:** GRI · TCFD · SASB\n\n"
        "**Assurance:** DNV Business Assurance\n\n"
        "**Ratings:** MSCI AAA · DJSI World (25 yrs) · CDP B- · ISS Prime"
    )

# ─────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────

y0, y1 = year_range
dff    = df.loc[y0:y1]
xs     = list(dff.index)
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
    "## TSMC ESG Analytics Dashboard\n"
    "*Taiwan Semiconductor Manufacturing Company · GRI · TCFD · SASB · WEF IBC SCM*"
)
st.divider()

# ─────────────────────────────────────────────
# KPI SCORECARDS
# ─────────────────────────────────────────────

ghg_now  = (latest["scope1"] + latest["scope2_market"]) / 1e6
ghg_prev = (prev["scope1"]   + prev["scope2_market"])   / 1e6

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("GHG S1+S2 (Mt CO₂e)",   f"{ghg_now:.1f}",
          f"{ghg_now - ghg_prev:+.2f} Mt",       delta_color="inverse")
c2.metric("Renewable Energy",       f"{latest['renewable_pct']:.1f}%",
          f"{latest['renewable_pct']-prev['renewable_pct']:+.1f}pp", delta_color="normal")
c3.metric("Safety TRIR",            f"{latest['trir']:.3f}",
          f"{latest['trir']-prev['trir']:+.3f}",  delta_color="inverse")
c4.metric("Revenue ($M)",           f"${latest['revenue']:,.0f}",
          f"{(latest['revenue']-prev['revenue'])/prev['revenue']*100:+.1f}%", delta_color="normal")
c5.metric("Employees",              f"{int(latest['employees']):,}",
          f"{int(latest['employees']-prev['employees']):+,}", delta_color="normal")
c6.metric("Training Hrs/Employee",  f"{latest['training_hrs']:.1f}",
          f"{latest['training_hrs']-prev['training_hrs']:+.1f} hrs", delta_color="normal")

# ─────────────────────────────────────────────
# CHART UTILITY
# ─────────────────────────────────────────────

def show(fig, title, height=320):
    fig.update_layout(**BASE_LAYOUT,
                      title=dict(text=title, font=dict(size=13)),
                      height=height)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def dual_axis():
    return make_subplots(specs=[[{"secondary_y": True}]])

# ─────────────────────────────────────────────
# ENVIRONMENTAL
# ─────────────────────────────────────────────

if show_e:
    st.markdown("### 🌿 Environmental")

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        for vals, color, name in [
            (dff["scope1"]/1e6,        C["scope1"], "Scope 1"),
            (dff["scope2_market"]/1e6, C["scope2"], "Scope 2 (Market)"),
            (dff["scope3"]/1e6,        C["scope3"], "Scope 3"),
        ]:
            fig.add_trace(go.Scatter(x=xs, y=list(vals), name=name,
                                     mode="lines+markers",
                                     line=dict(width=2, color=color),
                                     marker=dict(size=6)))
        target = (data["scope1"][0] + data["scope2_market"][0]) / 1e6
        fig.add_hline(y=target, line_dash="dot", line_color=C["green"],
                      annotation_text="2030 Target",
                      annotation_font_color=C["green"])
        fig.update_layout(yaxis_title="Million MT CO₂e")
        show(fig, "GHG Emissions by Scope (Mt CO₂e)")

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=list(dff["carbon_intensity"]),
                                  name="Carbon Intensity", mode="lines+markers",
                                  fill="tozeroy",
                                  fillcolor="rgba(210,153,34,0.10)",
                                  line=dict(color=C["amber"], width=2),
                                  marker=dict(size=8)))
        fig.update_layout(yaxis_title="MT CO₂e / $M Revenue")
        show(fig, "Carbon Intensity (MT CO₂e per $M Revenue)")

    col3, col4 = st.columns(2)

    with col3:
        ren  = [e * r / 100 for e, r in zip(dff["total_energy"], dff["renewable_pct"])]
        nren = [e - r for e, r in zip(dff["total_energy"], ren)]
        fig  = dual_axis()
        fig.add_trace(go.Bar(x=xs, y=nren,  name="Non-Renewable", marker_color=C["nonrenew"]), secondary_y=False)
        fig.add_trace(go.Bar(x=xs, y=ren,   name="Renewable",     marker_color=C["green"]),    secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=list(dff["renewable_pct"]),
                                  name="RE %", mode="lines+markers",
                                  line=dict(color=C["teal"], width=2),
                                  marker=dict(size=7)), secondary_y=True)
        fig.add_hline(y=60, line_dash="dot", line_color=C["teal"],
                      annotation_text="RE60 Target (2030)",
                      annotation_font_color=C["teal"], secondary_y=True)
        fig.update_layout(barmode="stack",
                          yaxis_title="GWh", yaxis2_title="RE %")
        show(fig, "Energy Mix & Renewable % (GWh)")

    with col4:
        fig = dual_axis()
        fig.add_trace(go.Bar(x=xs, y=list(dff["water_withdrawal"]),
                              name="Withdrawal (M MT)", marker_color=C["blue"]), secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=list(dff["water_recycled"]),
                                  name="Recycling Rate %", mode="lines+markers",
                                  line=dict(color=C["teal"], width=2),
                                  marker=dict(size=7)), secondary_y=True)
        fig.update_layout(yaxis_title="Million MT", yaxis2_title="Recycle %")
        show(fig, "Water Withdrawal & Recycling Rate")

    non_haz = [t - h for t, h in zip(dff["waste_total"], dff["waste_hazardous"])]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=xs, y=list(dff["waste_hazardous"]), name="Hazardous",     marker_color=C["red"]))
    fig.add_trace(go.Bar(x=xs, y=non_haz,                       name="Non-Hazardous", marker_color=C["amber"]))
    fig.update_layout(barmode="stack", yaxis_title="Metric Tonnes")
    show(fig, "Waste Generated by Type (MT)", height=280)

# ─────────────────────────────────────────────
# SOCIAL
# ─────────────────────────────────────────────

if show_s:
    st.markdown("### 👥 Social")

    col1, col2 = st.columns(2)

    with col1:
        fig = dual_axis()
        fig.add_trace(go.Bar(x=xs, y=list(dff["employees"]),
                              name="Employees", marker_color=C["blue"], opacity=0.8), secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=list(dff["turnover"]),
                                  name="Turnover %", mode="lines+markers",
                                  line=dict(color=C["amber"], width=2),
                                  marker=dict(size=7)), secondary_y=True)
        fig.update_layout(yaxis_title="Headcount", yaxis2_title="Turnover %")
        show(fig, "Headcount & Voluntary Turnover Rate")

    with col2:
        fig = dual_axis()
        fig.add_trace(go.Bar(x=xs, y=list(dff["training_hrs"]),
                              name="Training Hrs/Emp", marker_color=C["purple"], opacity=0.8), secondary_y=False)
        fig.add_trace(go.Scatter(x=xs, y=list(dff["trir"]),
                                  name="TRIR", mode="lines+markers",
                                  line=dict(color=C["red"], width=2),
                                  marker=dict(size=7)), secondary_y=True)
        fig.update_layout(yaxis_title="Avg Hours / Employee", yaxis2_title="TRIR")
        show(fig, "Safety (TRIR) & Training Hours")

    fig = go.Figure()
    for vals, color, name in [
        (dff["women_workforce"], C["teal"],   "Women in Workforce %"),
        (dff["women_mgmt"],      C["purple"], "Women in Management %"),
        (dff["women_board"],     C["green"],  "Women on Board %"),
    ]:
        fig.add_trace(go.Scatter(x=xs, y=list(vals), name=name,
                                  mode="lines+markers",
                                  line=dict(width=2, color=color),
                                  marker=dict(size=7)))
    fig.update_layout(yaxis_title="%")
    show(fig, "Gender Diversity Across Levels (%)", height=280)

# ─────────────────────────────────────────────
# GOVERNANCE
# ─────────────────────────────────────────────

if show_g:
    st.markdown("### 🏛 Governance")

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=list(dff["board_independent"]),
                                  name="Board Independence %", mode="lines+markers",
                                  line=dict(color=C["blue"], width=2), marker=dict(size=7)))
        fig.add_trace(go.Scatter(x=xs, y=list(dff["women_board"]),
                                  name="Women on Board %", mode="lines+markers",
                                  line=dict(color=C["green"], width=2), marker=dict(size=7)))
        fig.update_layout(yaxis=dict(range=[0, 100], gridcolor=C["border"],
                                     tickfont=dict(color=C["muted"])),
                          yaxis_title="%")
        show(fig, "Board Composition (%)")

    with col2:
        st.markdown("**Governance Highlights**")
        for item in [
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
        ]:
            st.markdown(f"✅  {item}")

# ─────────────────────────────────────────────
# FINANCIAL
# ─────────────────────────────────────────────

if show_f:
    st.markdown("### 💰 Financial Performance")
    fig = dual_axis()
    fig.add_trace(go.Bar(x=xs, y=list(dff["revenue"]),  name="Revenue",   marker_color=C["blue"],   opacity=0.85), secondary_y=False)
    fig.add_trace(go.Bar(x=xs, y=list(dff["capex"]),    name="CapEx",     marker_color=C["amber"],  opacity=0.85), secondary_y=False)
    fig.add_trace(go.Bar(x=xs, y=list(dff["rd_spend"]), name="R&D Spend", marker_color=C["purple"], opacity=0.85), secondary_y=False)
    fig.add_trace(go.Scatter(x=xs, y=list(dff["ebitda_margin"]),
                              name="EBITDA Margin %", mode="lines+markers",
                              line=dict(color=C["green"], width=2),
                              marker=dict(size=7)), secondary_y=True)
    fig.update_layout(barmode="group",
                      yaxis_title="USD Million", yaxis2_title="EBITDA Margin %")
    show(fig, "Revenue, CapEx & R&D ($M) with EBITDA Margin", height=340)

# ─────────────────────────────────────────────
# INSIGHT BANNER
# ─────────────────────────────────────────────

st.divider()
st.info(
    "📌 **Key Insight —** TSMC is the indispensable engine of the global chip economy — "
    "delivering record revenue ($88.3B), industry-leading worker safety (TRIR 0.133), and "
    "accelerating renewable energy adoption (14.1%) — yet its absolute GHG emissions grew 8% "
    "in 2024, revealing that the race between capacity expansion and decarbonization remains "
    "the defining ESG challenge investors must monitor."
)
