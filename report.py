import os
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y"
SAVE_DIR = "/storage/emulated/0/2025-07-01Assignment-1"
EXCEL_FILE = os.path.join(SAVE_DIR, "rfq_output.xlsx")

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get(URL)
time.sleep(3)

all_data = []
today = datetime.now().strftime("%d/%m/%Y")

while True:
    rfqs = driver.find_elements(By.CLASS_NAME, "rfq-item")

    for item in rfqs:
        try:
            rfq_id = item.get_attribute("data-rfq-id")
        except:
            rfq_id = ""
        try:
            title = item.find_element(By.CLASS_NAME, "subject").text.strip()
        except:
            title = ""
        try:
            buyer = item.find_element(By.CLASS_NAME, "buyer-name").text.strip()
        except:
            buyer = ""
        try:
            image = item.find_element(By.CLASS_NAME, "buyer-img").get_attribute("src")
        except:
            image = ""
        try:
            country = item.find_element(By.CLASS_NAME, "country-name").text.strip()
        except:
            country = ""
        try:
            inquiry_time = item.find_element(By.CLASS_NAME, "date").text.strip()
        except:
            inquiry_time = ""
        try:
            quotes_left = item.find_element(By.CLASS_NAME, "quote-left").text.strip()
        except:
            quotes_left = ""
        try:
            quantity = item.find_element(By.XPATH, ".//span[contains(text(),'Quantity')]/following-sibling::span").text.strip()
        except:
            quantity = ""
        try:
            email = "Yes" if "Email confirmed" in item.text else "No"
        except:
            email = "No"
        try:
            experienced = "Yes" if "Experienced" in item.text else "No"
        except:
            experienced = "No"
        try:
            complete_order = "Yes" if "Complete order" in item.text else "No"
        except:
            complete_order = "No"
        try:
            reply_time = "Yes" if "Typical reply" in item.text else "No"
        except:
            reply_time = "No"
        try:
            inquiry_url = item.find_element(By.CLASS_NAME, "subject").find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            inquiry_url = ""
        try:
            inquiry_date = item.find_element(By.CLASS_NAME, "date").text.strip()
        except:
            inquiry_date = ""

        all_data.append({
            "RFQ ID": rfq_id,
            "Title": title,
            "Buyer Name": buyer,
            "Buyer Image": image,
            "Country": country,
            "Inquiry Time": inquiry_time,
            "Quotes Left": quotes_left,
            "Quantity Required": quantity,
            "Email Confirmed": email,
            "Experienced": experienced,
            "Complete Order": complete_order,
            "Typical Reply Time": reply_time,
            "Interactive URL": inquiry_url,
            "Inquiry Date": inquiry_date,
            "Scraping Date": today
        })

    try:
        next_btn = driver.find_element(By.XPATH, "//a[contains(@class,'next') and not(contains(@class,'hidden'))]")
        if "disabled" in next_btn.get_attribute("class"):
            break
        next_btn.click()
        time.sleep(2)
    except:
        break

driver.quit()
os.makedirs(SAVE_DIR, exist_ok=True)
df = pd.DataFrame(all_data)
df.to_excel(EXCEL_FILE, index=False, engine="openpyxl")
print(f"✅ Done. {len(all_data)} RFQs saved to {EXCEL_FILE}")
