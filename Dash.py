# Project: Dynamic Neon AI Dashboard:

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
 
# ----------- Page Config -------------
st.set_page_config(layout="wide", page_title=" Dynamic Neon AI Dashboard")
 
# ----------- Styling -------------
st.markdown("""
    <style>
    body {
        background-color: #1e1e2f;
        color: white;
    }
    .main {
        background-color: #1e1e2f;
    }
    </style>
""", unsafe_allow_html=True)
 
st.title("🟣 Dynamic AI Dashboard")
st.markdown("Upload your **Excel** or **CSV** file to get started...")
 
# ----------- Theme Selection -------------
theme = st.radio("Choose Theme", ["Light", "Dark"], horizontal=True)
 
if theme == "Light":
    palette = px.colors.qualitative.Set1
    bg_color = "white"
    text_color = "black"
    template = "plotly_white"
else:
    palette = px.colors.qualitative.Dark2
    bg_color = "#1e1e2f"
    text_color = "white"
    template = "plotly_dark"
 
# ----------- File Upload -------------
uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "xls", "csv"])
 
if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1]
 
    try:
        if file_ext in ["xlsx", "xls"]:
            df = pd.read_excel(uploaded_file)
        elif file_ext == "csv":
            df = pd.read_csv(uploaded_file)
        else:
            st.error("Unsupported file format.")
            st.stop()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
 
    st.subheader(" Data Preview")
    st.dataframe(df.head(10))
 
    # ----------- Column Selection -------------
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
 
    if len(numeric_cols) < 2:
        st.warning(" Please upload a file with at least 2 numeric columns.")
        st.stop()
 
    col1 = st.selectbox("Select X-axis Column", numeric_cols, index=0)
    col2 = st.selectbox("Select Y-axis Column", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
 
    # Drop rows with NaN for scatter plot
    scatter_df = df[[col1, col2]].dropna()
 
    if scatter_df.empty:
        st.warning(" Not enough valid data for scatter plot.")
    else:
        st.subheader(" Scatter Plot")
        fig = px.scatter(scatter_df, x=col1, y=col2, size=col2,
                         color_discrete_sequence=palette,
                         template=template,
                         title=f"Scatter Plot: {col1} vs {col2}")
        st.plotly_chart(fig, use_container_width=True)
 
    # ----------- Pie Chart (Optional if column categorical or grouped)
    st.subheader(" Pie Chart")
    pie_col = st.selectbox("Select column for Pie Chart", df.columns)
    pie_df = df[pie_col].value_counts().reset_index()
    pie_df.columns = [pie_col, 'Count']
    fig2 = px.pie(pie_df, names=pie_col, values='Count', template=template)
    st.plotly_chart(fig2, use_container_width=True)
 
    # ----------- Bar Chart
    st.subheader(" Bar Chart")
    if len(numeric_cols) > 0:
        selected_bar_col = st.selectbox("Select column for Bar Chart", numeric_cols)
        fig3 = px.histogram(df, x=selected_bar_col, nbins=30, template=template)
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.info(" Upload a CSV or Excel file to start analyzing.")
 
