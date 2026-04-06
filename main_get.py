import os
import requests
import json # Kita butuh library ini biar hasil datanya rapi pas di-print
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# 1. BUKA BRANKAS & AMBIL KUNCI
load_dotenv()
ACCOUNT_ID = os.getenv('NETSUITE_ACCOUNT_ID')
CONSUMER_KEY = os.getenv('NETSUITE_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('NETSUITE_CONSUMER_SECRET')
TOKEN_ID = os.getenv('NETSUITE_TOKEN_ID')
TOKEN_SECRET = os.getenv('NETSUITE_TOKEN_SECRET')

# 2. RAKIT KUNCI OAUTH 1.0
auth = OAuth1(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TOKEN_ID,
    TOKEN_SECRET,
    realm=ACCOUNT_ID,
    signature_method='HMAC-SHA256'
)

# 3. FUNGSI UTAMA: Narik data dari NetSuite
# record_id diset None sebagai default (kalau nggak diisi, dia narik semua list)
def get_dari_netsuite(record_type, record_id=None):
    
    # URL Dasar
    url = f"https://{ACCOUNT_ID.lower()}.suitetalk.api.netsuite.com/services/rest/record/v1/{record_type}"
    
    # Kalau lu ngirim ID, URL-nya ditambahin ID di ujungnya
    if record_id:
        url = f"{url}/{record_id}"
        
    # Karena GET nggak ngirim data body, kita cuma butuh Accept JSON (nggak perlu Content-Type)
    headers = {
        "Accept": "application/json"
    }

    try:
        # Perhatikan: Di sini kita pakai requests.get (bukan .post lagi)
        # Dan nggak ada parameter json=payload karena kita nggak ngirim data
        response = requests.get(url, auth=auth, headers=headers)
        
        # Kalau statusnya 200 OK (Berhasil ditarik)
        if response.status_code == 200:
            print(f"✅ SUKSES Narik Data {record_type.upper()}!")
            
            # Ubah data mentah jadi bentuk JSON Python (Dictionary)
            data_json = response.json()
            
            # Print datanya biar rapi (indent=4 biar masuk ke dalam kayak di Postman)
            print(json.dumps(data_json, indent=4))
            
            return data_json
        else:
            print(f"❌ GAGAL Narik Data!")
            print(f"   => Detail Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"⚠️ Sistem Error: {str(e)}")
        return None

# 4. JALANKAN EKSEKUSI
if __name__ == "__main__":
    print("🚀 Mencoba narik data spesifik dari NetSuite...\n")
    
    # Contoh 1: Narik Department dengan ID 7 (yang kemarin sukses lu tes)
    get_dari_netsuite('department', 7)
    
    print("\n-------------------------------------------------\n")
    
    # Contoh 2: Narik Customer yang tadi lu bikin pakai POST
    # Ganti angka 15 dengan ID Customer yang dapet dari Location pas lu nge-POST tadi
    # get_dari_netsuite('customer', 15)