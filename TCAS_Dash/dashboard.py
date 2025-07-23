import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# อ่านไฟล์ CSV
df = pd.read_csv("tuition_fees.csv")  # ใช้ชื่อไฟล์จริงของคุณ

# เลือกเฉพาะหลักสูตรที่ต้องการ
df = df[df['ชื่อหลักสูตร'].str.contains("วิศวกรรมคอมพิวเตอร์|วิศวกรรมปัญญาประดิษฐ์", case=False)]

# สร้าง grouped bar chart โดยใช้ University เป็นสี
fig = px.bar(df, 
             x="University", 
             y="ค่าใช้จ่าย", 
             color="University",
             barmode="group",
             facet_col="ชื่อหลักสูตร",
             title="เปรียบเทียบค่าใช้จ่ายตามหลักสูตรและมหาวิทยาลัย",
             labels={"ค่าใช้จ่าย": "ค่าใช้จ่าย (บาท)", "University": "มหาวิทยาลัย"})

# สร้าง Dash App
app = Dash(__name__)
app.layout = html.Div([
    html.H2("Dashboard: เปรียบเทียบค่าใช้จ่ายของหลักสูตรวิศวกรรม"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
