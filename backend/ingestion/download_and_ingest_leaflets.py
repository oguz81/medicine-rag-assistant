## ILAC ASISTANI
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

from pathlib import Path
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


def download_pdf(url, medicine_name, leaflet_no):

    # This removes characters like / \ : * ? " < > | that Windows/Linux hate
    clean_name = re.sub(r'[\\/*?:"<>|]', "_", medicine_name)
    file_path = f"/home/oguz/MLProjects/medicine-rag-assistant/data/leaflets/{clean_name}_{leaflet_no}.pdf"

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



def web_scraping(medicine_name_input):
    # 1. Initialize the driver
    driver = webdriver.Chrome()
    driver.get("https://www.titck.gov.tr/kubkt")

    try:
        # 2. Define the 'Wait' (Wait up to 10 seconds)
        wait = WebDriverWait(driver, 10)

        # 3. Find the search box using a CSS Selector
        # On TİTCK, the search box is usually a standard 'search' type input
        search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))

        print("Sayfadaki arama kutusu bulundu!")

        # 4. Interact with it
        input_medicine_name = medicine_name_input
        search_box.send_keys(input_medicine_name)
        print("Sleeping for 3 seconds...")
        time.sleep(3)
    except Exception as e:
        print(f"Sayfadaki arama kutusu bulunamadi.: {e}")



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
            
                print(f"PDF URL bulundu: {pdf_url}")
                download_pdf(pdf_url, input_medicine_name, i)
                # 4. Click to download (if browser is configured)
                # kt_link_element.click()
            else:
                print("Bu satirda bir ya da sifir pdf var.")
                
        except Exception as e:
            print(f"Skip row due to error: {e}")
        i+=1


# ingestion/ingest_leaflets.py

def initialize():
    load_dotenv()

    
    

def load_documents():
    DATA_DIR = Path("/home/oguz/MLProjects/medicine-rag-assistant/data/leaflets")
    docs = []
    for pdf_path in DATA_DIR.glob("*.pdf"):
        print("PDF:", pdf_path)
        loader = PyPDFLoader(str(pdf_path))
        pdf_docs = loader.load()
        # Add metadata: which file
        for d in pdf_docs:
            d.metadata["source"] = pdf_path.name
        docs.extend(pdf_docs)
    return docs

def download_and_ingest(medicine_name_input: str):
    DB_DIR = "chroma_db_med"
    web_scraping(medicine_name_input)
    initialize()
    print("Loading PDFs...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents from PDFs.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    embeddings = OpenAIEmbeddings()  # uses OPENAI_API_KEY from env

    print("Creating Chroma DB...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    vectordb.persist()
    print(f"Saved vector DB to {DB_DIR}")
