from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import os

def fetch_fca():
    today = datetime.now().strftime("%Y%m%d")
    target_url = f"https://www.idx.co.id/secondary/get/SpecialMonitoringEffects/MonitoringEffectsHistorical?startDate={today}&endDate={today}&View=Table"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        json_data = None

        def handle_response(response):
            nonlocal json_data
            if response.url == target_url and response.status == 200:
                try:
                    json_data = response.json()
                except Exception as e:
                    print(f"Error parsing JSON: {e}")

        page.on("response", handle_response)

        # Buka halaman yang memicu request API
        page.goto("https://www.idx.co.id/id/perusahaan-tercatat/daftar-efek-pemantauan-khusus")

        # Tunggu 5 detik agar request selesai
        page.wait_for_timeout(5000)

        browser.close()

    if json_data is None:
        print("Gagal mengambil data JSON")
        return

    # Simpan ke root folder repo
    with open("fca.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"Data FCA tanggal {today} berhasil diambil dan disimpan ke fca.json")
    print("Current dir:", os.getcwd())
    print("Files:", os.listdir())

if __name__ == "__main__":
    fetch_fca()
