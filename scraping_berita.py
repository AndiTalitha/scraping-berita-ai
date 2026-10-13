
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.detik.com/tag/teknologi-ai/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"
}


def scraping_berita():
    print("Memulai scraping berita AI...")

    try:
        response = requests.get(URL, headers=headers, timeout=20)
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

        if len(judul) < 15:
            continue

        if not tautan.startswith("https://www.detik.com/"):
            continue

        if "/tag/" in tautan or "/foto/" in tautan:
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
        print("Tidak ada berita ditemukan. Periksa akses situs.")
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

    print("Scraping selesai!")
    print("Jumlah data:", len(hasil))
    print("Hasil tersimpan di data_berita_ai.csv")

    for nomor, berita in enumerate(hasil[:5], start=1):
        print(f"{nomor}. {berita['judul']}")
        print(berita["url"])


if __name__ == "__main__":
    scraping_berita()
