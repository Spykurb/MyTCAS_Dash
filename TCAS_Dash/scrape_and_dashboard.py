from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# ตั้งค่า ChromeDriver
options = Options()
# options.add_argument("--headless")  # ลอง comment ออกเพื่อดู browser ทำงาน
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

keywords = ['วิศวกรรมคอมพิวเตอร์', 'วิศวกรรมปัญญาประดิษฐ์']
base_url = "https://course.mytcas.com/"
all_data = []

for keyword in keywords:
    driver.get(base_url)
    try:
        # รอให้ช่อง search โหลดเสร็จ
        search_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
        search_input.clear()

        # พิมพ์ทีละตัวเหมือนคนพิมพ์
        for ch in keyword:
            search_input.send_keys(ch)
            time.sleep(0.2)  # หน่วงเวลา 0.2 วินาที/ตัวอักษร

        # รอให้ div#result ปรากฏ
        wait.until(EC.visibility_of_element_located((By.ID, "result")))
        time.sleep(1)  # รอให้ผลลัพธ์ขึ้นเต็มที่

        # ดึงลิงก์หลักสูตรจากผลลัพธ์
        # รอให้ ul.t-programs ปรากฏ
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.t-programs')))
        time.sleep(1)  # รอเสริมให้โหลด DOM เสร็จสมบูรณ์

        program_links = driver.find_elements(By.CSS_SELECTOR, 'ul.t-programs li a')

        print(f"พบหลักสูตรทั้งหมด: {len(program_links)} รายการ")
        course_links = []
        for a in program_links:
            href = a.get_attribute('href')
            print(href)
            if href:
                course_links.append(href)


    except Exception as e:
        print(f"❌ หา input หรือผลลัพธ์ไม่เจอ: {e}")
        continue

    # ดึงข้อมูลแต่ละหลักสูตร
    for link in course_links:
        try:
            driver.get(link)
            wait.until(EC.presence_of_element_located((By.ID, "overview")))
            time.sleep(1)

            overview_html = driver.find_element(By.ID, "overview").get_attribute("innerHTML")
            soup = BeautifulSoup(overview_html, 'html.parser')
            items = soup.find_all(['dt', 'dd'])

            data = {'Keyword': keyword, 'Course URL': link}
            last_dt = None
            for tag in items:
                if tag.name == 'dt':
                    last_dt = tag.get_text(strip=True)
                elif tag.name == 'dd' and last_dt:
                    data[last_dt] = tag.get_text(strip=True)
                    last_dt = None

            all_data.append(data)
            print(f"✅ ดึงข้อมูลจาก {link}")

        except Exception as e:
            print(f"❌ ดึงข้อมูลไม่ได้จาก {link}: {e}")
            continue

driver.quit()

# บันทึกข้อมูลเป็น CSV
df = pd.DataFrame(all_data)
df.to_csv("tuition_fees.csv", index=False, encoding="utf-8-sig")
print("📁 บันทึกข้อมูลสำเร็จใน tuition_fees.csv")
