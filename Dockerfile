# Gunakan image Python sebagai base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke dalam container
COPY . .

# Perintah untuk menjalankan bot
CMD ["python", "bot.py"]