import requests
import json
from datetime import datetime

def fetch_fca():
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://www.idx.co.id/secondary/get/SpecialMonitoringEffects/MonitoringEffectsHistorical?startDate={today}&endDate={today}&View=Table"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://www.idx.co.id/id/perusahaan-tercatat/daftar-efek-pemantauan-khusus",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8"
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()  # pastikan tidak error HTTP
    data = r.json()

    # Simpan data ke fca.json
    with open("fca.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Data FCA tanggal {today} berhasil diambil dan disimpan ke fca.json")

if __name__ == "__main__":
    fetch_fca()
