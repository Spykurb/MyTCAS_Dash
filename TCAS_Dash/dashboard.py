import pandas as pd
import streamlit as st

# โหลดข้อมูล
df = pd.read_csv('tuition_fees.csv')

st.set_page_config(page_title="Dashboard TCAS", layout="wide")

st.title("📘 Executive Dashboard สำหรับนักเรียนที่สนใจเรียนวิศวกรรม")

st.markdown("### ข้อมูลหลักสูตรที่เกี่ยวข้องกับ วิศวกรรมคอมพิวเตอร์ และ ปัญญาประดิษฐ์")

selected_keyword = st.selectbox("เลือกสาขาที่สนใจ", df['Keyword'].unique())

filtered_df = df[df['Keyword'] == selected_keyword]

for idx, row in filtered_df.iterrows():
    with st.expander(f"🌐 หลักสูตรจาก: {row['Course URL']}"):
        st.markdown(f"📎 [ดูหลักสูตร](https://course.mytcas.com{row['Course URL'].split('.com')[-1]})")
        st.text_area("รายละเอียดจากหน้า Overview", row['Overview Info'], height=200)

st.markdown("---")
st.info("ข้อมูลนี้เก็บจากเว็บไซต์ mytcas.com แบบอัตโนมัติ (Web Scraping) และอาจเปลี่ยนแปลงได้")
