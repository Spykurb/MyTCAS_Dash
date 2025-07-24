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

    # เงื่อนไข: ต้องมีคำว่า "ค่าใช้จ่าย", "ค่าเล่าเรียน", "ต่อเทอม", "ต่อภาค", ฯลฯ
    keywords = ["ค่าใช้จ่าย", "ค่าเล่าเรียน", "ต่อเทอม", "ต่อภาค", "ต่อภาคเรียน"]
    if any(kw in text for kw in keywords):
        # ใช้ regex เพื่อดึงตัวเลขหลักพันขึ้นไป
        numbers = re.findall(r'\d{2,3}(?:,\d{3})*|\d{4,}', text)
        if numbers:
            # เอาเลขตัวแรกและเอา , ออก เช่น '18,000' → 18000
            number_clean = numbers[0].replace(',', '')
            return int(number_clean)
    return None

df['ค่าใช้จ่าย (clean)'] = df['ค่าใช้จ่าย'].apply(extract_numeric_fee)
df = df.dropna(subset=['ค่าใช้จ่าย (clean)'])

# -------------------- แยกตามหลักสูตร --------------------
df_computer = df[df['ชื่อหลักสูตร'].str.contains("วิศวกรรมคอมพิวเตอร์", case=False)]
df_ai = df[df['ชื่อหลักสูตร'].str.contains("วิศวกรรมปัญญาประดิษฐ์", case=False)]

# -------------------- สร้างกราฟ --------------------
fig_computer = px.bar(df_computer, x='University', y='ค่าใช้จ่าย (clean)',
                      title='ค่าใช้จ่าย - วิศวกรรมคอมพิวเตอร์',
                      labels={'ค่าใช้จ่าย (clean)': 'ค่าใช้จ่าย (บาท)'})

fig_ai = px.bar(df_ai, x='University', y='ค่าใช้จ่าย (clean)',
                title='ค่าใช้จ่าย - วิศวกรรมปัญญาประดิษฐ์',
                labels={'ค่าใช้จ่าย (clean)': 'ค่าใช้จ่าย (บาท)'})

# -------------------- Dash App --------------------
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard ค่าใช้จ่ายของหลักสูตรวิศวกรรม"),
    dcc.Graph(figure=fig_computer),
    dcc.Graph(figure=fig_ai)
])

if __name__ == '__main__':
    app.run(debug=True)
