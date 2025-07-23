from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

keywords = ['วิศวกรรมคอมพิวเตอร์', 'วิศวกรรมปัญญาประดิษฐ์']
base_url = "https://course.mytcas.com/"
all_data = []

for keyword in keywords:
    print(f"\nเริ่มค้นหา keyword: {keyword}")
    driver.get(base_url)

    # รอช่อง search และพิมพ์ทีละตัว
    search_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
    search_input.clear()
    for ch in keyword:
        search_input.send_keys(ch)
        time.sleep(0.2)

    # รอผลลัพธ์
    wait.until(EC.visibility_of_element_located((By.ID, "results")))
    time.sleep(1)

    # ดึงจำนวนหลักสูตรทั้งหมด
    li_elements = driver.find_elements(By.XPATH, '//*[@id="results"]/ul/li')
    total_courses = len(li_elements)
    print(f"พบ {total_courses} หลักสูตรสำหรับ '{keyword}'")

    for i in range(1, total_courses + 1):
        # หา element ใหม่เสมอ
        course_xpath = f'//*[@id="results"]/ul/li[{i}]/a'
        link_element = wait.until(EC.element_to_be_clickable((By.XPATH, course_xpath)))
        href = link_element.get_attribute('href')
        print(f"[{i}/{total_courses}] เข้าไปดึงข้อมูลหลักสูตร: {href}")

        # คลิกเข้าไปดูรายละเอียด
        ActionChains(driver).move_to_element(link_element).click().perform()

        # ดึงข้อมูลภายในหน้า overview
        try:
            # รอโหลดข้อมูล overview
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="overview"]/dl')))
            time.sleep(1)

            # ✅ ดึงชื่อมหาวิทยาลัย
            uni_name = driver.find_element(By.XPATH, '//*[@id="root"]/main/div[2]/div/span/span/a').text

            overview_dl_html = driver.find_element(By.XPATH, '//*[@id="overview"]/dl').get_attribute('innerHTML')
            soup = BeautifulSoup(overview_dl_html, 'html.parser')

            # สร้าง dictionary สำหรับข้อมูลแต่ละหลักสูตร
            data = {'Keyword': keyword, 'Course URL': href, 'University': uni_name}
            dts = soup.find_all('dt')
            dds = soup.find_all('dd')
            for dt, dd in zip(dts, dds):
                key = dt.get_text(strip=True)
                val = dd.get_text(strip=True)
                data[key] = val
            all_data.append(data)
            print("✅ เก็บข้อมูลหลักสูตรเสร็จ")

        except:
            print("❌ ไม่สามารถดึงข้อมูลจากหน้าหลักสูตร")

        # กลับไปหน้าเดิม
        driver.back()

        # ✅ พิมพ์ keyword ใหม่อีกครั้งเพื่อให้ results แสดง
        search_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
        search_input.clear()
        for ch in keyword:
            search_input.send_keys(ch)
            time.sleep(0.2)

        wait.until(EC.visibility_of_element_located((By.ID, "results")))
        time.sleep(1)

print("\n📦 ดึงข้อมูลครบทุกหลักสูตรแล้ว")
driver.quit()

# บันทึกลงไฟล์ CSV
df = pd.DataFrame(all_data)
df.to_csv("tuition_fees.csv", index=False, encoding="utf-8-sig")
print("📁 บันทึกข้อมูลเสร็จที่: tuition_fees.csv")