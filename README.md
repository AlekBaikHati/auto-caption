# Telegram Bot dengan Telethon

Bot ini menggunakan Telethon untuk berinteraksi dengan API Telegram.

## Cara Deploy ke Koyeb

Anda dapat dengan mudah mendepoy bot ini ke Koyeb dengan mengklik tombol di bawah ini:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/services/deploy?type=git&repository=github.com/AlekBaikHati/REPO_NAME&branch=main&builder=dockerfile&env%5BAPI_ID%5D=api_id&env%5BAPI_HASH%5D=api_hash&env%5BBOT_TOKEN%5D=bot_token)

Gantilah `USERNAME` dan `REPO_NAME` dengan nama pengguna dan nama repositori GitHub Anda.

## Variabel Lingkungan

Anda perlu mengatur variabel lingkungan berikut di Koyeb:

- `API_ID`: ID API Telegram Anda.
- `API_HASH`: Hash API Telegram Anda.
- `BOT_TOKEN`: Token bot Telegram Anda.

## Instalasi

Jika Anda ingin menjalankan bot ini secara lokal, Anda dapat menginstalnya dengan langkah-langkah berikut:

1. Clone repositori ini:
   ```bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan bot:
   ```bash
   python bot.py
   ```

## Lisensi

Proyek ini dilisensikan di bawah MIT License.
