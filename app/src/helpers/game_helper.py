from datetime import datetime, timedelta


# periksa sisa waktu
def countdown_timer(end_time):
    current_time = datetime.now()
    remaining_time = end_time - current_time
    
    mins, secs = divmod(remaining_time.seconds, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    
    return timer


import json

# Membaca file JSON
def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    
    return data