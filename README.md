# hackerbits

_Web crawler_ dan implementasi beberapa algoritma clustering sederhana pada website [Hacker News](https://news.ycombinator.com/). Dibuat sebagai pemenuhan tugas besar Teknologi Mesin Pencari.

## Instalasi

### Pengembangan

1. _Clone_ repositori ini.
2. Buat sebuah [_virtual environment_](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) dengan mengeksekusi perintah `virtualenv <nama_folder>` pada terminal Anda.
3. Jalankan perintah `pip install -r requirements.txt` pada terminal Anda.
4. Jalankan perintah `source <nama_folder>/bin/activate` pada terminal Anda.
5. Sebelum memulai proses pengembangan, eksekusi `main.py` dengan argumen `init` untuk mengunduh _dependency-dependency_ yang dibutuhkan. Contoh: `py main.py init`
6. Anda dapat memulai proses pengembangan dengan mengeksekusi `py main.py cluster`

> **CATATAN**: Setiap kali Anda menambahkan _dependency_ baru, mohon tambahkan pada `requirements.txt` menggunakan perintah `pip freeze > requirements.txt`

## Penggunaan

Terdapat 3 buah perintah yang tersedia pada program ini:

1. `init`, mengunduh berbagai _dependency_ yang dibutuhkan. Anda **HARUS** melakukan langkah ini terlebih dahulu sebelum memulai menggunakan program ini.
2. `crawl`, melakukan _crawling_ pada website HackerNews kemudian menyimpan hasilnya
3. `cluster`, melakukan _clustering_ pada kumpulan berita. Apabila `crawl` belum dilakukan, maka program akan melakukan `crawl` terlebih dahulu

Urutan eksekusi yang diharapkan adalah: `init` -> `crawl` -> `cluster`

## Kontributor

1. [Stephen Hadi](https://github.com/stephenhadi) — 2017730016
2. [Cristopher](https://github.com/Namchee) —  2017730017
3. [Nicholas Aditya Halim](https://github.com/athlonneo) — 2017730018
