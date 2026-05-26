# # Works with any data type, handles missing or messy values automatically,
# # feels clean, dynamic, and resilient.


# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.set_page_config(page_title="Dynamic AI Dashboard", layout="wide")

# st.title(" Dynamic AI Dashboard")
# st.markdown("Upload an Excel or CSV file to get started.")

# # Upload
# uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

# if uploaded_file:
#     try:
#         if uploaded_file.name.endswith(".csv"):
#             df = pd.read_csv(uploaded_file)
#         else:
#             df = pd.read_excel(uploaded_file)
#     except Exception as e:
#         st.error(f"Error loading file: {e}")
#         st.stop()

#     # Clean
#     df.columns = df.columns.str.strip()
#     df = df.dropna(how="all")
#     df = df.dropna(axis=1, how="all")
#     df = df.loc[:, ~df.columns.str.contains("^Unnamed", case=False)]

#     # Fix object columns
#     for col in df.select_dtypes(include=["object"]).columns:
#         df[col] = df[col].astype(str)

#     st.subheader(" Data Preview")
#     st.dataframe(df.head(20), use_container_width=True)

#     numeric_cols = df.select_dtypes(include="number").columns.tolist()
#     non_numeric_cols = df.select_dtypes(exclude="number").columns.tolist()

#     # Scatter Plot
#     if len(numeric_cols) >= 2:
#         st.subheader(" Scatter Plot")
#         col1, col2 = st.columns(2)
#         with col1:
#             x_axis = st.selectbox("X-Axis", numeric_cols, key="scatter_x")
#         with col2:
#             y_axis = st.selectbox("Y-Axis", numeric_cols, key="scatter_y")

#         if x_axis and y_axis:
#             scatter_df = df[[x_axis, y_axis]].dropna()
#             if not scatter_df.empty:
#                 fig = px.scatter(scatter_df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}",
#                                  template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Bold)
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.warning("Not enough data for scatter plot.")

#     # Histogram
#     if numeric_cols:
#         st.subheader(" Histogram")
#         hist_col = st.selectbox("Select numeric column", numeric_cols, key="hist")
#         hist_data = df[hist_col].dropna()
#         if not hist_data.empty and hist_data.nunique() > 1:
#             fig = px.histogram(df, x=hist_col, nbins=30, template="plotly_dark")
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.warning("Not enough unique values to plot histogram.")

#     # Pie Chart
#     if non_numeric_cols:
#         st.subheader(" Pie Chart")
#         pie_col = st.selectbox("Select categorical column", non_numeric_cols, key="pie")

#         if pie_col:
#             pie_df = df[pie_col].dropna()
#             if not pie_df.empty and pie_df.nunique() > 1:
#                 pie_summary = pie_df.value_counts().reset_index()
#                 pie_summary.columns = [pie_col, "Count"]
#                 fig = px.pie(pie_summary, names=pie_col, values="Count", template="plotly_dark")
#                 st.plotly_chart(fig, use_container_width=True)
#             else:
#                 st.warning("Not enough categories to show pie chart.")
# else:
#     st.info("Please upload a CSV or Excel file to begin.")

# save this as dashboard.py and run with: streamlit run dashboard.py




# ----------------------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Auto Dashboard", layout="wide")
st.title(" AI-Powered Data Dashboard")



uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Fix function
def force_object_columns_to_string(df):
    obj_cols = df.select_dtypes(include=["object"]).columns
    for col in obj_cols:
        df[col] = df[col].astype(str)
    return df

if uploaded_file:
    df = load_data(uploaded_file)

    # Clean basic
    df.columns = df.columns.str.strip()
    df = df.dropna(how="all")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed", case=False)]

    # 🔧 CRUCIAL FIX HERE
    df = force_object_columns_to_string(df)

    st.subheader(" Cleaned Data Preview")
    st.dataframe(df.head(10), use_container_width=True)


# uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

# @st.cache_data
# def load_data(file):
#     if file.name.endswith(".csv"):
#         return pd.read_csv(file)
#     else:
#         return pd.read_excel(file)

# if uploaded_file:
#     df = load_data(uploaded_file)

#     # CLEAN: basic strip + remove unnamed
#     df.columns = df.columns.str.strip()
#     df = df.dropna(how="all")
#     df = df.loc[:, ~df.columns.str.contains("^Unnamed", case=False)]

#     #  ADD this function earlier in your code
#     def fix_arrow_issues(df):
#         for col in df.columns:
#             try:
#                 pd.Series(df[col])
#             except Exception:
#                 df[col] = df[col].astype(str)
#         return df

    #  Apply it here
    # df = fix_arrow_issues(df)

    # #  Now safe to display
    # st.subheader(" Data Preview")
    # st.dataframe(df.head(10), use_container_width=True)


    # Analyze data types
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    st.sidebar.header(" Analysis Options")
    selected_col = st.sidebar.selectbox("Choose a column to analyze", df.columns)

    st.subheader(f" Automatic Charts for `{selected_col}`")

    # PIE CHART for Categorical Columns
    if selected_col in cat_cols:
        value_counts = df[selected_col].value_counts().nlargest(10)
        fig = px.pie(values=value_counts.values, names=value_counts.index, title=f"Pie Chart of {selected_col}")
        st.plotly_chart(fig, use_container_width=True)

        fig_bar = px.bar(x=value_counts.index, y=value_counts.values,
                         labels={'x': selected_col, 'y': 'Count'},
                         title=f"Bar Chart of {selected_col}")
        st.plotly_chart(fig_bar, use_container_width=True)

    # HISTOGRAM / BOX PLOT for Numerical Columns
    elif selected_col in num_cols:
        col1, col2 = st.columns(2)

        with col1:
            fig_hist = px.histogram(df, x=selected_col, nbins=20, title=f"Histogram of {selected_col}")
            st.plotly_chart(fig_hist, use_container_width=True)

        with col2:
            fig_box = px.box(df, y=selected_col, title=f"Boxplot of {selected_col}")
            st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")

    # Optional: Correlation Heatmap
    if len(num_cols) >= 2:
        st.subheader("🔗 Correlation Heatmap")
        corr = df[num_cols].corr()
        fig_corr, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig_corr)

    st.markdown(" Select different columns in the sidebar to explore more charts.")
else:
    st.info(" Upload a file from the sidebar to get started.")
    
st.dataframe()