import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Output, Input
import re

# -------------------- อ่านและทำความสะอาดข้อมูล --------------------
df = pd.read_csv('tuition_fees.csv')

def extract_numeric_fee(text):
    if pd.isna(text):
        return None
    text = str(text)

    numbers = re.findall(r'\d{2,3}(?:,\d{3})*|\d{4,}', text)
    if not numbers:
        return None

    number_clean = numbers[0].replace(',', '')
    try:
        value = int(number_clean)
    except ValueError:
        return None

    if any(x in text for x in ["ต่อเทอม", "ต่อภาค", "ต่อภาคเรียน"]):
        return value
    elif "ตลอดหลักสูตร" in text:
        return round(value / 8)
    elif not any(x in text for x in ["ต่อเทอม", "ต่อภาค", "ต่อภาคเรียน", "ตลอดหลักสูตร"]):
        if value > 150000:
            return round(value / 8)
        else:
            return value

    return value

df['ค่าใช้จ่าย (clean)'] = df['ค่าใช้จ่าย'].apply(extract_numeric_fee)
df = df.dropna(subset=['ค่าใช้จ่าย (clean)'])

# -------------------- แยกกลุ่มหลักสูตร --------------------
comp_eng_df = df[df['ชื่อหลักสูตร'].str.contains("วิศวกรรมคอมพิวเตอร์", case=False)]
ai_eng_df = df[df['ชื่อหลักสูตร'].str.contains("วิศวกรรมปัญญาประดิษฐ์", case=False)]

# -------------------- สร้าง Dashboard --------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard เปรียบเทียบค่าใช้จ่ายหลักสูตรวิศวกรรม"),

    html.H2("หลักสูตรวิศวกรรมคอมพิวเตอร์"),
    html.Label("เลือกมหาวิทยาลัย:"),
    dcc.Dropdown(
        options=[{"label": u, "value": u} for u in comp_eng_df["University"].unique()],
        value=comp_eng_df["University"].unique().tolist(),
        multi=True,
        id="comp-univ-dropdown"
    ),
    dcc.Graph(id="comp-graph"),

    html.H2("หลักสูตรวิศวกรรมปัญญาประดิษฐ์"),
    html.Label("เลือกมหาวิทยาลัย:"),
    dcc.Dropdown(
        options=[{"label": u, "value": u} for u in ai_eng_df["University"].unique()],
        value=ai_eng_df["University"].unique().tolist(),
        multi=True,
        id="ai-univ-dropdown"
    ),
    dcc.Graph(id="ai-graph")
])

# -------------------- Callbacks --------------------
@app.callback(
    Output("comp-graph", "figure"),
    Input("comp-univ-dropdown", "value")
)
def update_comp_graph(selected_univs):
    filtered_df = comp_eng_df[comp_eng_df["University"].isin(selected_univs)]
    fig = px.bar(
        filtered_df,
        x='University',
        y='ค่าใช้จ่าย (clean)',
        color='ชื่อหลักสูตร',
        barmode='group',
        title='ค่าใช้จ่าย: วิศวกรรมคอมพิวเตอร์',
        labels={'ค่าใช้จ่าย (clean)': 'ค่าใช้จ่าย (บาท)'},
        height=600
    )
    return fig

@app.callback(
    Output("ai-graph", "figure"),
    Input("ai-univ-dropdown", "value")
)
def update_ai_graph(selected_univs):
    filtered_df = ai_eng_df[ai_eng_df["University"].isin(selected_univs)]
    fig = px.bar(
        filtered_df,
        x='University',
        y='ค่าใช้จ่าย (clean)',
        color='ชื่อหลักสูตร',
        barmode='group',
        title='ค่าใช้จ่าย: วิศวกรรมปัญญาประดิษฐ์',
        labels={'ค่าใช้จ่าย (clean)': 'ค่าใช้จ่าย (บาท)'},
        height=600
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
