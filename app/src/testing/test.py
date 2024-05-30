# Data original dengan karakter non-ASCII
TITLE = [
    "ɴꜱʟᴡ",
    "✘ ᴇʟꜱᴛᴏɴ",
    "𝐈⃯⃖𝐏⃯⃖",
    "𝔡'𝔩𝔬𝔤𝔦𝔠",
    "ɴɪɢʜᴛᴍᴀʀᴇ⍪",
    "No Loser",
    "·❦‌‌͜͡ʟᴛᴄ"
]

GCS = {
    "ɴꜱʟᴡ": "NEVER SURRENDER LONE WOLF",
    "✘ ᴇʟꜱᴛᴏɴ": "FAMILY ELSTON",
    "𝐈⃯⃖𝐏⃯⃖": "IRREPLACEABLE MUTUALAN",
    "𝔡'𝔩𝔬𝔤𝔦𝔠": "DIALOGIC",
    "ɴɪɢʜᴛᴍᴀʀᴇ⍪": "NIGHTMARE",
    "No Loser": "ACADEMI NO LOSER",
    "·❦‌‌͜͡ʟᴛᴄ": "LIL' TWILIGHT"
}

# Fungsi untuk mengonversi string ke dalam kode ASCII
def to_ascii_codes(text):
    ascii_codes = [str(ord(char)) for char in text]
    return ' '.join(ascii_codes)

# Mengonversi setiap judul ke dalam kode ASCII
ascii_titles = {to_ascii_codes(title): title for title in TITLE}

# Fungsi untuk memeriksa pesan baru
def check_titel_gcs(new_message):
    # Memisahkan pesan menjadi karakter dan konversi ke ASCII
    ascii_message = to_ascii_codes(new_message)
    
    for ascii_code in ascii_titles:
        if ascii_code in ascii_message:
            original_title = ascii_titles[ascii_code]
            print(f"Kata '{original_title}' ditemukan dalam pesan baru. {GCS[original_title]}")
            return 
    
    print('Kata Tidak Ditemukan')
    return None


# # Data original dengan karakter non-ASCII
# titles = [
#     "ɴꜱʟᴡ",
#     "✘ ᴇʟꜱᴛᴏɴ",
#     "𝐈⃯⃖𝐏⃯⃖",
#     "𝔡'𝔩𝔬𝔤𝔦𝔠",
#     "ɴɪɢʜᴛᴍᴀʀᴇ⍪",
#     "No Loser",
#     "·❦‌‌͜͡ʟᴛᴄ"
# ]

# # Fungsi untuk mengonversi string ke dalam kode ASCII
# def to_ascii_codes(text):
#     ascii_codes = [str(ord(char)) for char in text]
#     return ' '.join(ascii_codes)

# # Mengonversi setiap judul ke dalam kode ASCII
# ascii_titles = {to_ascii_codes(title): title for title in titles}

# # Menampilkan hasil konversi
# print("List Kata dalam ASCII:")
# for ascii_code, title in ascii_titles.items():
#     print(f"{title} -> {ascii_code}")

# # Fungsi untuk memeriksa pesan baru
# def check_new_message(new_message):
#     # Memisahkan pesan menjadi karakter dan konversi ke ASCII
#     ascii_message = to_ascii_codes(new_message)
    
#     for ascii_code in ascii_titles:
#         if ascii_code in ascii_message:
#             original_title = ascii_titles[ascii_code]
#             print(f"Kata '{original_title}' ditemukan dalam pesan baru.")
#             return True
    
#     print("Tidak ada kata yang cocok ditemukan dalam pesan baru.")
#     return False


# # Contoh penggunaan fungsi dengan pesan baru
new_message = input("Masukkan pesan baru: ")
check_titel_gcs(new_message)
