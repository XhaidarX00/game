import redis
import ast

class RedisCRUD:
    def __init__(self, host, port, password):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True  # Ini agar data yang diambil langsung dalam bentuk string
        )
    
    def create(self, key, value):
        if not self.redis_client.exists(key):
            self.redis_client.set(key, value)
            return True
        else:
            return None
    
    def read(self, key):
        value = self.redis_client.get(key)
        if value is not None:
            return value
        else:
            return None
        
    def mread(self, data):
        value = self.redis_client.mget(data)
        if value is not None:
            return value
        else:
            return None
        
    def update(self, key, new_value):
        if self.redis_client.exists(key):
            self.redis_client.set(key, new_value)
            return True
        else:
            return None
        
    def delete(self, key):
        if self.redis_client.exists(key):
            self.redis_client.delete(key)
            return True
        else:
            return None
        
    def append_key(self, key):
        return self.redis_client.append(key)
    
    def exsist(self, key):
        return self.redis_client.exists(key)

    def mexsist(self, data):
        return [(keyy if self.redis_client.exists(keyy) else None) for keyy in data]

    def incr(self, key):
        return self.redis_client.incr(key)
    
    def decr(self, key):
        return self.redis_client.decr(key)
    
    def incrby(self, key, value):
        return self.redis_client.incrby(key, value)
    
    def decrby(self, key, value):
        return self.redis_client.decrby(key, value)
    
    def expire(self, key, time):
        durasi = self.redis_client.expire(key, time)
        if durasi > 0:
            return durasi
        # Jika durasi <= 0, tidak perlu menggunakan else, karena nilai default adalah None
    
    def setexpire(self, key, value, time):
        return self.redis_client.setex(key, time, value)
    
    def time_exp_key(self, key):
        return self.redis_client.ttl(key)
    
    def keys_pattern(self, pattern):
        return self.redis_client.keys(f"{pattern}*")
    
    def keys_all(self):
        return self.redis_client.keys("*")
    
    def info_server(self):
        return self.redis_client.info()
    
    def delete_ubot(self, user_id):
        patterns = self.keys_pattern(f"{user_id}*")
        for key in patterns:
            self.redis_client.delete(key)
        
        return True
    
    def ping(self):
        return self.redis_client.ping()
    
    def del_all_key_one_db(self):
        return self.redis_client.flushdb()
    
    def get_userbots(self):
        ubot_ = []
        data = self.read("UBOT")
        if data:
            data = ast.literal_eval(data)
            for key, value in data.items():
                api_id = value["api_id"]
                api_hash = value["api_hash"]
                session_string = value["session_string"]
                ubot_.append(
                    dict(
                    name=str(key),
                    api_id=api_id,
                    api_hash=api_hash,
                    session_string=session_string,
                )
            )
            
        return ubot_
    
    def get_userbots_backup(self):
        ubot_ = []
        data = self.read("UBOT")
        if data:
            data = ast.literal_eval(data)
            for key, value in data.items():
                api_id = value["api_id"]
                api_hash = value["api_hash"]
                session_string = value["session_string_backup"]
                ubot_.append(
                    dict(
                    name=str(key),
                    api_id=api_id,
                    api_hash=api_hash,
                    session_string=session_string,
                )
            )
            
        return ubot_
    
    def get_userbotss(self):
        data = self.read("UBOT")
            
        return data


# Ganti nilai host, port, dan password sesuai dengan konfigurasi Redis Anda
redis_host = 
redis_port = 
# redis-14475.c1.asia-northeast1-1.gce.redns.redis-cloud.com:14475
redis_password = 

# Buat objek RedisCRUD dengan koneksi Redis
dbredis = RedisCRUD(redis_host, redis_port, redis_password)
