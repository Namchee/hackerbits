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

`py main.py <command_name> <optional_arguments>`

### Daftar Perintah Wajib

Nama | Kegunaaan
---- | ---------
`init` | Mengunduh berbagai _dependency_ yang dibutuhkan oleh program. Jalankan perintah ini sebelum menjalankan perintah `cluster`
`crawl` | Melakukan _crawling_ pada website HackerNews, kemudian menyimpan hasilnya pada sebuah berkas JSON.
`cluster` | Melakukan _clustering_ pada kumpulan artikel yang sudah di _crawl_ pada proses sebelumnya. Apabila data belum di*crawl*, maka program akan mengeksekusi perintah `crawl` terlebih dahulu.

Urutan eksekusi perintah yang ideal adalah `init` → `crawl` → `cluster`

### Daftar perintah opsional

Nama | Nilai | Deskripsi | Nilai Anggapan | Perintah
---- | ----- | --------- | -------------- | --------
`-h`, `--help` | `None` | Memunculkan menu bantuan | - | -
`-c <jumlah>`, `--count <jumlah>` | `int` | Menentukan jumlah artikel yang akan diambil pada perintah `crawl` | `200` | `crawl`
`-f <nama>`, `--filename <nama>` | `str` | Menentukan nama berkas tempat penyimpanan artikel | `crawling_result` | [`crawl`, `cluster`]
`-p`, `--polite` | `None` | Menentukan apakah proses _crawling_ dilakukan dengan menghormati nilai-nilai pada `robots.txt` | `False` | `crawl`

## Kontributor

1. [Stephen Hadi](https://github.com/stephenhadi) — 2017730016
2. [Cristopher](https://github.com/Namchee) —  2017730017
3. [Nicholas Aditya Halim](https://github.com/athlonneo) — 2017730018
