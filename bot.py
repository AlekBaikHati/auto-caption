from telethon import TelegramClient, events
import asyncio
import logging
import os
from aiohttp import web
import threading

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ganti dengan API ID dan API Hash Anda
api_id = os.getenv('API_ID')  # Mengambil dari variabel lingkungan
api_hash = os.getenv('API_HASH')  # Mengambil dari variabel lingkungan

# Ganti dengan token bot Anda
bot_token = os.getenv('BOT_TOKEN')  # Mengambil dari variabel lingkungan

# Dictionary untuk menyimpan caption per chat
user_captions = {}

class HTTPServer:
    def __init__(self, host: str, port: int):
        self.app = web.Application()
        self.host = host
        self.port = port
        self.app.router.add_get('/', self.health_check)

    async def health_check(self, request):
        return web.Response(text="OK")

    async def run_server(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

def start_http_server():
    port = int(os.getenv('PORT', 8080))
    http_server = HTTPServer(host='0.0.0.0', port=port)
    asyncio.run(http_server.run_server())

async def main():
    logger.info("Starting HTTP server...")
    port = int(os.getenv('PORT', 8080))
    http_server = HTTPServer(host='0.0.0.0', port=port)
    asyncio.create_task(http_server.run_server())  # Jalankan server HTTP sebagai task

    logger.info("Connecting to Telegram...")
    async with TelegramClient('bot', api_id, api_hash) as client:
        await client.start(bot_token=bot_token)  # Gunakan token bot dari variabel lingkungan
        logger.info("Bot connected to Telegram.")
        
        @client.on(events.NewMessage)
        async def handler(event):
            logger.info(f"Received message: {event.message.message}")  # Tambahkan log ini
            # Mendapatkan file yang diterima
            if event.video:
                file_name = f"video_{event.video.id}.mp4"  # Menggunakan ID video sebagai nama file
                original_caption = event.message.message if event.message.message else ""
            elif event.photo:
                file_name = f"photo_{event.photo.id}.jpg"  # Menggunakan ID foto sebagai nama file
                original_caption = event.message.message if event.message.message else ""
            else:
                return  # Jika bukan video atau foto, keluar dari fungsi

            # Mengambil caption yang diatur oleh pengguna, jika ada
            custom_caption = user_captions.get(event.chat_id, "")
            if custom_caption:
                # Menggunakan caption yang diatur oleh pengguna
                new_caption = custom_caption.replace("{ori_caption}", original_caption)
            else:
                # Jika belum diatur, gunakan caption default
                new_caption = f"✨ Upload by <a href='http://t.me/Zerozerozoro'>Mimin</a> | <a href='https://sociabuzz.com/firnandaszz/tribe'>Donasi</a> | <a href='http://t.me/Anime_Bahasa_Indonesia'>List Anime</a>\n📌 {original_caption}"

            # Mengirim kembali file dengan caption yang baru
            if event.video:
                await client.send_file(event.chat_id, event.video, caption=new_caption, parse_mode='html')
            elif event.photo:
                await client.send_file(event.chat_id, event.photo, caption=new_caption, parse_mode='html')

        @client.on(events.NewMessage(pattern='/caption ?(.*)'))
        async def set_caption(event):
            if event.is_reply:
                # Jika membalas pesan, gunakan teks dari pesan yang dibalas
                reply_message = await event.get_reply_message()
                user_caption = reply_message.message
            else:
                # Jika tidak membalas, ambil caption dari argumen perintah
                user_caption = event.pattern_match.group(1)

            user_captions[event.chat_id] = user_caption

            # Menampilkan caption yang diterima dan preview caption
            caption_diterima = user_caption
            preview_caption = user_caption.replace("{ori_caption}", "Caption Asli")  # Ganti dengan placeholder
            await event.reply(f"Caption diterima:\n{caption_diterima}", disable_web_page_preview=True)
            await event.reply(f"Preview Caption:\n{preview_caption}", parse_mode='html')

        @client.on(events.NewMessage(pattern='/help'))
        async def help_command(event):
            help_text = (
                "Berikut adalah cara menggunakan bot ini:\n\n"
                "<b>/caption [caption]</b> - Mengatur caption untuk file yang akan dikirim.\n"
                "Anda dapat menggunakan format HTML untuk caption:\n\n"
                "<b>Teks Tebal</b>: <b>Contoh</b> → <b>Ini adalah teks tebal</b>\n"
                "<i>Teks Miring</i>: <i>Contoh</i> → <i>Ini adalah teks miring</i>\n"
                "<u>Teks Garis Bawah</u>: <u>Contoh</u> → <u>Ini adalah teks garis bawah</u>\n"
                "<a href='https://example.com'>Tautan yang Dapat Diklik</a>: <a href='https://example.com'>Contoh</a> → <a href='https://example.com'>Kunjungi Example</a>\n"
                "<code>Teks Monospace</code>: <code>Contoh</code> → <code>Ini adalah teks monospace</code>\n"
                "<code>Ini adalah kutipan yang ingin saya sampaikan.</code> → <code>Ini adalah kutipan yang ingin saya sampaikan.</code>\n\n"
                "Contoh penggunaan:\n"
                "<b>✨ Upload by <a href='http://t.me/Zerozerozoro'>Mimin</a></b> → <b>✨ Upload by <a href='http://t.me/Zerozerozoro'>Mimin</a></b>\n"
                "Gunakan <code>{ori_caption}</code> untuk menyertakan caption asli.\n"
                "Balas pesan dengan /caption untuk menggunakan teks pesan sebagai caption."
            )
            await event.reply(help_text, parse_mode='html')

        logger.info("Bot sudah berjalan...")
        await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if 'This event loop is already running' in str(e):
            print("Event loop sudah berjalan. Coba jalankan di lingkungan yang mendukung asyncio.")
        else:
            raise e
