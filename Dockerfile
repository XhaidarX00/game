FROM python:3.10

# Update dan upgrade sistem serta bersihkan cache apt
RUN apt update && apt upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Salin semua file ke dalam direktori kerja di dalam container
COPY . /app/
WORKDIR /app/

# Berikan izin eksekusi pada start.sh
RUN chmod +x start.sh

# Instal dependencies yang ada di requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Jalankan skrip start.sh saat container dijalankan
CMD ["bash", "start.sh"]
