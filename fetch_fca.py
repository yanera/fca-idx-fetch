from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def fetch_fca():
    today = datetime.now().strftime("%Y%m%d")
    target_url_part = "/secondary/get/SpecialMonitoringEffects/MonitoringEffectsHistorical"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        json_data = None

        def handle_response(response):
            url = response.url
            if target_url_part in url and response.status == 200:
                print(f"Got response from: {url}")
                try:
                    text = response.text()
                    print("Response text preview:", text[:200])
                    json_data_local = response.json()
                    nonlocal json_data
                    json_data = json_data_local
                except Exception as e:
                    print(f"Error parsing JSON: {e}")

        page.on("response", handle_response)

        page.goto("https://www.idx.co.id/id/perusahaan-tercatat/daftar-efek-pemantauan-khusus")
        page.wait_for_timeout(7000)  # tambah waktu tunggu supaya data sempat dimuat

        browser.close()

    if json_data is None:
        print("Gagal mengambil data JSON")
        return

    with open("fca.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"Data FCA tanggal {today} berhasil diambil dan disimpan ke fca.json")

if __name__ == "__main__":
    fetch_fca()
