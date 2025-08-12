from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import os

def fetch_fca():
    today = datetime.now().strftime("%Y%m%d")
    target_url_part = "/secondary/get/SpecialMonitoringEffects/MonitoringEffectsHistorical"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless dimatikan untuk debug
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://www.idx.co.id/id/perusahaan-tercatat/daftar-efek-pemantauan-khusus",
                "Origin": "https://www.idx.co.id"
            }
        )
        page = context.new_page()

        json_data = None

        def handle_response(response):
            url = response.url
            if target_url_part in url and response.status == 200:
                print(f"Got response from: {url}")
                try:
                    text = response.text()
                    print("Response text preview:", text[:200])
                    nonlocal json_data
                    json_data = response.json()
                except Exception as e:
                    print(f"Error parsing JSON: {e}")

        page.on("response", handle_response)

        print("Buka halaman FCA IDX...")
        page.goto("https://www.idx.co.id/id/perusahaan-tercatat/daftar-efek-pemantauan-khusus")

        print("Ambil screenshot halaman untuk cek challenge...")
        page.screenshot(path="page_debug.png")

        print("Tunggu 15 detik untuk interaksi manual jika perlu...")
        page.wait_for_timeout(15000)

        browser.close()

    if json_data is None:
        print("Gagal mengambil data JSON, buat file dummy kosong")
        with open("fca.json", "w", encoding="utf-8") as f:
            f.write("[]")
        return

    with open("fca.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"Data FCA tanggal {today} berhasil diambil dan disimpan ke fca.json")
    print("Current dir:", os.getcwd())
    print("Files:", os.listdir())

if __name__ == "__main__":
    fetch_fca()
