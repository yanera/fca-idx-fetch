from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def fetch_fca():
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://www.idx.co.id/secondary/get/SpecialMonitoringEffects/MonitoringEffectsHistorical?startDate={today}&endDate={today}&View=Table"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Buka url API
        response = page.goto(url)
        # Tunggu respon selesai dan ambil json
        json_data = response.json()

        browser.close()

    with open("fca.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"Data FCA tanggal {today} berhasil diambil dan disimpan ke fca.json")

if __name__ == "__main__":
    fetch_fca()
