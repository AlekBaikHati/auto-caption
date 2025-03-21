# Gunakan image Python sebagai base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin hanya requirements.txt terlebih dahulu untuk memanfaatkan cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke dalam container
COPY . .

# Perintah untuk menjalankan bot
CMD ["python", "bot.py"]
