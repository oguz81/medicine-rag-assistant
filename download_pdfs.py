## MEDICINE INFO RAG ASSISTANT 
## Oguz Demirtas
## 15.01.2026

## This script is developed to download leaflets from titck.gov.tr

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import re

def download_pdf(url, medicine_name, leaflet_no):
    # 1. Create a folder to keep things organized
    #if not os.path.exists("titck_downloads"):
        #os.makedirs("titck_downloads")

    # 2. Clean the medicine name to make it a valid filename
    # This removes characters like / \ : * ? " < > | that Windows/Linux hate
    clean_name = re.sub(r'[\\/*?:"<>|]', "_", medicine_name)
    file_path = f"/home/oguz/MLProjects/medicine-rag-assistant/data/leaflets/{clean_name}_{leaflet_no}"

    # 3. Download the file
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Success: Saved {url}")
        else:
            print(f"❌ Failed: Server returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error downloading {medicine_name}: {e}")




# 1. Initialize the driver
driver = webdriver.Chrome()
driver.get("https://www.titck.gov.tr/kubkt")

try:
    # 2. Define the 'Wait' (Wait up to 10 seconds)
    wait = WebDriverWait(driver, 10)

    # 3. Find the search box using a CSS Selector
    # On TİTCK, the search box is usually a standard 'search' type input
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))

    print("Search box found successfully!")

    # 4. Interact with it
    input_medicine_name = "Augmentin"
    search_box.send_keys(input_medicine_name)
    print("Sleeping for 3 seconds...")
    time.sleep(3)
except Exception as e:
    print(f"Could not find the search box: {e}")



# 1. Wait for the rows to appear
wait = WebDriverWait(driver, 10)
rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.table-row")))

i = 1 # counter for leaflet_no
for row in rows:
    try:
        # 2. Find all <a> tags with class 'badge' inside THIS specific row
        # These are the "PDF" buttons you see on the screen
        pdf_buttons = row.find_elements(By.CSS_SELECTOR, "a.badge")

        # 3. Logic to get the KT (usually the second link)
        # Index 0 = KÜB, Index 1 = KT
        if len(pdf_buttons) >= 2:
            kt_link_element = pdf_buttons[1] # This targets the second "PDF" badge
            pdf_url = kt_link_element.get_attribute("href")
            
            print(f"Found KT PDF URL: {pdf_url}")
            download_pdf(pdf_url, input_medicine_name, i)
            # 4. Click to download (if browser is configured)
            # kt_link_element.click()
        else:
            print("Only one PDF (or none) found in this row.")
                
    except Exception as e:
        print(f"Skip row due to error: {e}")
    i+=1