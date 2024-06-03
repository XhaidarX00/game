import os
import json

class JSONLoader:
    def __init__(self, directory):
        self.directory = directory
        self.data = self.load_all_json_files()

    def load_all_json_files(self):
        all_data = {}
        for filename in os.listdir(self.directory):
            if filename.endswith('.json'):
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    # Menyimpan data dengan kunci sebagai nama file tanpa ekstensi
                    all_data[os.path.splitext(filename)[0]] = data
        return all_data

    def get_data_by_filename(self, filename):
        # Mengambil data berdasarkan nama file tanpa ekstensi
        return self.data.get(filename, None)

# Contoh penggunaan
directory_games = 'games'  # Ganti dengan path ke direktori yang berisi file JSON Anda
directory_kata_kata = 'kata-kata'

def load_data_json(filename):
    # Membuat instance JSONLoader untuk setiap direktori
    loader_game = JSONLoader(directory_games)
    loader_kata = JSONLoader(directory_kata_kata)

    # Menggabungkan data dari kedua loader
    combined_data = {**loader_game.data, **loader_kata.data}

    # Mengambil data berdasarkan nama file tanpa ekstensi
    data = combined_data.get(filename, None)
    
    return data

# # Contoh penggunaan
# filename = 'caklontong'  # Nama file tanpa ekstensi
# data = load_data_json(filename)

# if data:
#     print(f"Data dari file {filename}.json:")
#     for item in data:
#         print(f"Index: {item['index']}")
#         print(f"Soal: {item['soal']}")
#         print(f"Jawaban: {item['jawaban']}")
#         print(f"Deskripsi: {item['deskripsi']}")
#         print("")
# else:
#     print(f"Tidak ditemukan data untuk file {filename}.json")
