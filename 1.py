# # -------------------Smart AI Dashboard Generator-------------------
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import numpy as np

# st.set_page_config(page_title="Smart AI Dashboard", layout="wide")

# st.markdown(
#     "<h1 style='text-align:center; color:#4FC3F7;'>📊 Smart AI Dashboard Generator</h1>", unsafe_allow_html=True
# )
# st.markdown("Upload a CSV or Excel file — the dashboard will generate automatically.")

# uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx"])

# def generate_dashboard(df):
#     df.columns = df.columns.str.strip()
#     df = df.dropna(how="all").dropna(axis=1, how="all")
#     df = df.loc[:, ~df.columns.str.contains("^Unnamed", case=False)]

#     # Try parsing any object columns to datetime
#     for col in df.select_dtypes(include="object").columns:
#         try:
#             # df[col] = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)
#             df[col] = pd.to_datetime(df[col], errors='coerce')

#         except:
#             pass

#     num_cols = df.select_dtypes(include="number").columns.tolist()
#     cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
#     date_cols = df.select_dtypes(include=["datetime"]).columns.tolist()

#     # --- KPIs ---
#     st.markdown("##  Quick Insights")
#     if len(num_cols) > 0:
#         kpi_cols = st.columns(min(4, len(num_cols)))
#         for i, col in enumerate(num_cols[:4]):
#             with kpi_cols[i]:
#                 st.metric(label=col, value=f"{df[col].sum():,.0f}")
#     else:
#         st.info("No numeric columns found for KPI summary.")

#     st.markdown("---")

#     # --- Visualizations ---
#     st.markdown("## 📈 Data Visualizations")

#     # Time series
#     if len(num_cols) >= 1 and len(date_cols) >= 1:
#         st.subheader("📅 Time Series Trend")
#         line_df = df[[date_cols[0]] + num_cols[:1]].dropna()
#         line_df = line_df.sort_values(by=date_cols[0])
#         fig = px.line(line_df, x=date_cols[0], y=num_cols[0], title=f"{num_cols[0]} over time", markers=True)
#         st.plotly_chart(fig, use_container_width=True)

#     # Pie and bar chart
#     col1, col2 = st.columns(2)

#     with col1:
#         if cat_cols:
#             st.subheader("🥧 Donut Chart")
#             pie_df = df[cat_cols[0]].value_counts().reset_index()
#             pie_df.columns = [cat_cols[0], "Count"]
#             fig = px.pie(pie_df, names=cat_cols[0], values="Count", hole=0.4)
#             st.plotly_chart(fig, use_container_width=True)

#     with col2:
#         if cat_cols and num_cols:
#             st.subheader("📊 Bar Chart")
#             bar_df = df.groupby(cat_cols[0])[num_cols[0]].sum().reset_index()
#             fig = px.bar(bar_df, x=cat_cols[0], y=num_cols[0], color=cat_cols[0])
#             st.plotly_chart(fig, use_container_width=True)

#     # Histogram + Scatter
#     col3, col4 = st.columns(2)

#     with col3:
#         if len(num_cols) >= 1:
#             st.subheader("📥 Histogram")
#             fig = px.histogram(df, x=num_cols[0])
#             st.plotly_chart(fig, use_container_width=True)

#     with col4:
#         if len(num_cols) >= 2:
#             st.subheader("⚡ Scatter Plot")
#             fig = px.scatter(df, x=num_cols[0], y=num_cols[1], color=cat_cols[0] if cat_cols else None)
#             st.plotly_chart(fig, use_container_width=True)

#     st.markdown("---")
#     st.markdown("<small>Auto-generated dashboard using Streamlit + Plotly ✨</small>", unsafe_allow_html=True)

# # --- Trigger Dashboard ---
# if uploaded_file:
#     try:
#         df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith("csv") else pd.read_excel(uploaded_file)
#         generate_dashboard(df)
#     except Exception as e:
#         st.error(f"❌ Could not read file: {e}")
# else:
#     st.info("Please upload a CSV or Excel file to begin.")





# ------------------------------------Smart AI Dashboard Generator-------------------


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io


import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')


st.set_page_config(layout="wide")
st.title(" Auto Data Dashboard")



# Upload file:

uploaded_file = st.file_uploader("Upload a CSV or Excel file")
if uploaded_file is not None:
    # Step 1: Load file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Step 2: Try to convert object columns to numeric (where possible)
    for col in df.select_dtypes(include='object').columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')  # skip coercion for now

    # Step 3: Identify numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    # Step 4: Handle KPI Summary safely
    if len(numeric_cols) > 0:
        st.subheader(" KPI Summary")
        st.dataframe(df[numeric_cols].describe().T)
    else:
        st.warning(" No numeric columns found for KPI summary. Displaying full dataset instead.")
        st.dataframe(df)

    # Optional: still show full data regardless
    st.subheader(" Full Dataset")
    st.dataframe(df)


# Function to check if a column is datetime
def try_parse_dates(df):
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"]  # Add more if needed

    for col in df.columns:
        if df[col].dtype == 'object':
            for fmt in date_formats:
                try:
                    parsed = pd.to_datetime(df[col], format=fmt, errors="coerce")
                    if parsed.notna().sum() > 0:
                        df[col] = parsed
                        st.sidebar.success(f"Converted to datetime: {col} using format {fmt}")
                        break
                except Exception:
                    continue
    return df

# Show dashboard if file is uploaded
if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    st.success("File uploaded successfully ")
    df = try_parse_dates(df)

    st.subheader(" Raw Data")
    st.dataframe(df)

    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()

    st.sidebar.header("Chart Settings")

    chart_type = st.sidebar.selectbox("Select Chart Type", ["Pie Chart", "Bar Chart", "Line Chart", "Histogram"])
    
    if chart_type == "Pie Chart" and categorical_cols:
        pie_col = st.sidebar.selectbox("Select Column for Pie Chart", categorical_cols)
        pie_data = df[pie_col].value_counts()
        fig, ax = plt.subplots()
        ax.pie(pie_data.values, labels=pie_data.index, autopct="%1.1f%%")
        ax.set_title(f"Pie Chart: {pie_col}")
        st.pyplot(fig)

    elif chart_type == "Bar Chart" and categorical_cols and numeric_cols:
        cat_col = st.sidebar.selectbox("Select Categorical Column", categorical_cols)
        num_col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)
        bar_data = df.groupby(cat_col)[num_col].mean().sort_values(ascending=False)
        fig, ax = plt.subplots()
        sns.barplot(x=bar_data.values, y=bar_data.index, ax=ax)
        ax.set_title(f"Bar Chart: Avg of {num_col} by {cat_col}")
        st.pyplot(fig)

    elif chart_type == "Line Chart" and datetime_cols and numeric_cols:
        time_col = st.sidebar.selectbox("Select Time Column", datetime_cols)
        value_col = st.sidebar.selectbox("Select Value Column", numeric_cols)
        df_sorted = df.sort_values(by=time_col)
        fig, ax = plt.subplots()
        ax.plot(df_sorted[time_col], df_sorted[value_col])
        ax.set_title(f"Line Chart: {value_col} over Time")
        st.pyplot(fig)

    elif chart_type == "Histogram" and numeric_cols:
        hist_col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[hist_col], kde=True, ax=ax)
        ax.set_title(f"Histogram of {hist_col}")
        st.pyplot(fig)

    else:
        st.warning("Please upload a valid dataset with relevant columns.")


