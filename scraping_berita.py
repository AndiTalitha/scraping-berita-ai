

import csv
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.detik.com/tag/teknologi-ai/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
    )
}


def scraping_berita():
    print("Memulai scraping berita AI dari detik.com...")

    try:
        response = requests.get(
            URL, headers=HEADERS, timeout=30
        )
        response.raise_for_status()
    except requests.RequestException as error:
        print("Gagal mengambil halaman:", error)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    hasil = []
    url_terkumpul = set()

    for link in soup.select("a[href]"):
        judul = link.get_text(" ", strip=True)
        tautan = urljoin(URL, link.get("href", ""))

        # Ambil tautan artikel detik.com dengan pola ID berita
        if not re.search(r"/d-\d+/", tautan):
            continue

        if not judul or len(judul) < 20:
            continue

        if tautan in url_terkumpul:
            continue

        url_terkumpul.add(tautan)

        hasil.append({
            "judul": judul,
            "tanggal": "",
            "ringkasan": "",
            "url": tautan
        })

    if not hasil:
        print("Belum ada artikel yang cocok ditemukan.")
        print("Periksa struktur halaman atau akses situs.")
        return

    with open(
        "data_berita_ai.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        kolom = ["judul", "tanggal", "ringkasan", "url"]
        writer = csv.DictWriter(file, fieldnames=kolom)
        writer.writeheader()
        writer.writerows(hasil)

    print(f"Scraping berhasil. Artikel ditemukan: {len(hasil)}")
    print("File hasil: data_berita_ai.csv")

    for nomor, berita in enumerate(hasil[:10], start=1):
        print(f"{nomor}. {berita['judul']}")
        print(berita["url"])


if __name__ == "__main__":
    scraping_berita()
