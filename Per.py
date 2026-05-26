# ----------------------------------------BY PERPLEXITY --------------------------------------------------


import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import io
import base64

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Auto AI Dashboard (Excel/CSV)", style={'textAlign':'center'}),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload Excel/CSV'),
        multiple=False
    ),
    html.Div(id='output-dashboard')
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename or 'xlsx' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div(['Unsupported file format.'])
    except Exception as e:
        return html.Div([f'Error while reading file: {e}'])

    # Now df is defined, we can proceed to use it safely
    numeric_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include='object').columns

    print("Numeric columns:", numeric_cols)
    print("Categorical columns:", cat_cols)

    charts = []

    if len(numeric_cols) > 0:
        # Histograms for first 3 numeric columns
        for col in numeric_cols[:3]:
            fig = px.histogram(df, x=col, title=f'Distribution of {col}')
            charts.append(dcc.Graph(figure=fig))

        # Scatter plot if at least 2 numeric columns
        if len(numeric_cols) >= 2:
            fig2 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f'Scatter: {numeric_cols[0]} vs {numeric_cols[1]}')
            charts.append(dcc.Graph(figure=fig2))

        # Line chart of all numeric columns
        fig3 = px.line(df[numeric_cols], title="Line Chart of Numeric Columns")
        charts.append(dcc.Graph(figure=fig3))

    if len(cat_cols) > 0:
        # Pie chart of first categorical column
        fig4 = px.pie(df, names=cat_cols[0], title=f'Pie Chart of {cat_cols[0]}')
        charts.append(dcc.Graph(figure=fig4))

    if not charts:
        return html.Div(["No suitable data found for charts. Please upload a different file."])

    return html.Div(charts)


    charts = []
    # Try to auto-detect numeric columns and visualize them
    numeric_cols = df.select_dtypes('number').columns
    if len(numeric_cols) == 0:
        return html.Div(['No numeric data found. Upload a different file.'])

    # Generate some auto-charts (Bar/Line/Pie) using Plotly
    for col in numeric_cols[:3]:  # Limit to first 3 for simplicity
        chart = px.histogram(df, x=col, title=f'Distribution of {col}', nbins=30)
        charts.append(dcc.Graph(figure=chart))

    if len(numeric_cols) >= 2:
        scatter = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f'{numeric_cols[0]} vs {numeric_cols[1]}')
        charts.append(dcc.Graph(figure=scatter))

    # Pie chart for first categorical column
    cat_cols = df.select_dtypes('object').columns
    if len(cat_cols) > 0:
        pie = px.pie(df, names=cat_cols[0], title=f'Distribution of {cat_cols[0]}')
        charts.append(dcc.Graph(figure=pie))

    return html.Div(charts)

@app.callback(
    Output('output-dashboard', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        return parse_contents(contents, filename)
    return html.Div('Upload an Excel or CSV file to generate a dashboard.')

if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run(debug=True)

