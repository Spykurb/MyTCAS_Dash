import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import re

# อ่านข้อมูล
df = pd.read_csv('tuition_fees.csv')

# -------------------- CLEAN ค่าใช้จ่าย --------------------
def extract_numeric_fee(text):
    if pd.isna(text):
        return None
    text = str(text)

    # ดึงตัวเลข
    numbers = re.findall(r'\d{2,3}(?:,\d{3})*|\d{4,}', text)
    if not numbers:
        return None

    # ใช้ตัวเลขแรกที่เจอ (สมมติว่าเป็นค่าหลัก)
    number_clean = numbers[0].replace(',', '')
    try:
        value = int(number_clean)
    except ValueError:
        return None

    # ถ้ามีคำว่าต่อเทอม หรือ ต่อภาค ให้ใช้ตามนั้น
    if any(x in text for x in ["ต่อเทอม", "ต่อภาค", "ต่อภาคเรียน"]):
        return value

    # ถ้ามีแค่คำว่า "ตลอดหลักสูตร" ให้หาร 8
    elif "ตลอดหลักสูตร" in text:
        return round(value / 8)

    # ถ้ามีทั้ง "ตลอดหลักสูตร" และ "ต่อเทอม" → ให้ถือว่า "ต่อเทอม" เป็นหลัก
    # แต่เราจัดการในลำดับก่อนหน้าแล้ว

    # ถ้าไม่มีคำอะไรเลย แต่เป็นตัวเลข → ถือว่าเป็นค่าเทอม
    return value



df['ค่าใช้จ่าย (clean)'] = df['ค่าใช้จ่าย'].apply(extract_numeric_fee)
df = df.dropna(subset=['ค่าใช้จ่าย (clean)'])

# -------------------- แยกข้อมูล 2 กลุ่ม --------------------
comp_eng_df = df[df['ชื่อหลักสูตร'].str.contains("วิศวกรรมคอมพิวเตอร์", case=False)]
ai_eng_df = df[df['ชื่อหลักสูตร'].str.contains("วิศวกรรมปัญญาประดิษฐ์", case=False)]

# -------------------- สร้างกราฟ --------------------
fig_comp = px.bar(
    comp_eng_df,
    x='University',
    y='ค่าใช้จ่าย (clean)',
    color='ชื่อหลักสูตร',
    barmode='group',
    title='ค่าใช้จ่าย: วิศวกรรมคอมพิวเตอร์',
    labels={'ค่าใช้จ่าย (clean)': 'ค่าใช้จ่าย (บาท)'},
    height=600
)

fig_ai = px.bar(
    ai_eng_df,
    x='University',
    y='ค่าใช้จ่าย (clean)',
    color='ชื่อหลักสูตร',
    barmode='group',
    title='ค่าใช้จ่าย: วิศวกรรมปัญญาประดิษฐ์',
    labels={'ค่าใช้จ่าย (clean)': 'ค่าใช้จ่าย (บาท)'},
    height=600
)

# -------------------- สร้าง Dashboard --------------------
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard เปรียบเทียบค่าใช้จ่ายหลักสูตรวิศวกรรม"),
    html.H2("หลักสูตรวิศวกรรมคอมพิวเตอร์"),
    dcc.Graph(figure=fig_comp),
    html.H2("หลักสูตรวิศวกรรมปัญญาประดิษฐ์"),
    dcc.Graph(figure=fig_ai)
])

if __name__ == '__main__':
    app.run(debug=True)
