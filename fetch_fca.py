from playwright.sync_api import sync_playwright
import json
from datetime import datetime

def fetch_fca():
    today = datetime.now().strftime("%Y%m%d")
    target_url = f"https://www.idx.co.id/secondary/get/SpecialMonitoringEffects/MonitoringEffectsHistorical?startDate={today}&endDate={today}&View=Table"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        json_data = None

        # Pasang listener untuk tangkap response dari target_url
        def handle_response(response):
            nonlocal json_data
            if response.url == target_url and response.status == 200:
                try:
                    json_data = response.json()
                except:
                    pass

        page.on("response", handle_response)

        # Buka halaman yang memicu request API (daftar efek pemantauan khusus)
        page.goto("https://www.idx.co.id/id/perusahaan-tercatat/daftar-efek-pemantauan-khusus")

        # Tunggu beberapa detik agar request API selesai dan data tertangkap
        page.wait_for_timeout(5000)  # tunggu 5 detik

        browser.close()

    if json_data is None:
        print("Gagal mengambil data JSON")
        return

    with open("fca.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"Data FCA tanggal {today} berhasil diambil dan disimpan ke fca.json")

if __name__ == "__main__":
    fetch_fca()
