def convert_to_ascii(text):
    ascii_text = []
    for char in text:
        ascii_value = ord(char)
        ascii_text.append(ascii_value)
    return ascii_text

def check_keyword(text, keywords):
    for keyword in keywords:
        found_key = keyword
        ascii_text = convert_to_ascii(text.lower())
        keyword_ascii = convert_to_ascii(keyword.lower())
        for i in range(len(ascii_text) - len(keyword_ascii) + 1):
            if ascii_text[i:i + len(keyword_ascii)] == keyword_ascii:
                # print(keyword_ascii)
                # print(ascii_text[i:i + len(keyword_ascii)])
                return found_key
    return False

kata_kunci =  ["˹ᴅɪꜰλᴍꜱ", "ᴛᴇʀᴀᴛᴀɪ⁸⁸⁸", "ғᴇʀɴɪɢ"]

point = {}


opsi = 'y'
while(True):
    text = '\n\n๏๏ Daftar Kata Kunci :\n'
    for key in kata_kunci:
        text += f"◉ {key}\n"
        
    print(text)
    kalimat = input("Masukkan Nama Akun: ")
    found_key = check_keyword(kalimat, kata_kunci)
    if found_key:
        print(f"\nKata kunci '{found_key}' ditemukan dalam kalimat.")
        if found_key in point:
            point[found_key] += 1
        else:
            point[found_key] = 1
    else:
        print(f"Kata kunci '{kata_kunci}' tidak ditemukan dalam kalimat.")
    
    text = '\n\n๏๏ Daftar Point :\n'
    for key, value in point.items():
        text += f" ◉ {key} : {value}\n"
        
    print(text)
    opsi = input("\nUlang Lagi ga Dar? ")
    if opsi == 't':
        print("Program Selesai ...")
        break