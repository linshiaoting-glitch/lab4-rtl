import streamlit as st
import plotly.graph_objects as go

st.title("TSMC ESG Dashboard — Test")
st.success("✅ App is working!")

fig = go.Figure()
fig.add_trace(go.Bar(x=[2020, 2021, 2022, 2023, 2024],
                     y=[47855, 57848, 75881, 69295, 88268],
                     name="Revenue ($M)"))
st.plotly_chart(fig, use_container_width=True)
