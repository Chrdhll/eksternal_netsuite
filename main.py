import os
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# 1. BUKA BRANKAS: Load data dari file .env
load_dotenv()

# 2. AMBIL KUNCI: Tarik variabel dari brankas
ACCOUNT_ID = os.getenv('NETSUITE_ACCOUNT_ID')
CONSUMER_KEY = os.getenv('NETSUITE_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('NETSUITE_CONSUMER_SECRET')
TOKEN_ID = os.getenv('NETSUITE_TOKEN_ID')
TOKEN_SECRET = os.getenv('NETSUITE_TOKEN_SECRET')

# 3. RAKIT KUNCI: Setup standar otentikasi NetSuite (OAuth 1.0)
auth = OAuth1(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TOKEN_ID,
    TOKEN_SECRET,
    realm=ACCOUNT_ID,
    signature_method='HMAC-SHA256'
)

# 4. SIAPIN DATA: Array dinamis yang mau kita tembak
data_customers = [
    {
        "companyname": "PT Maju Terus Python",
        "email": "halo@majuterus.id",
        "phone": "08111222333",
        "subsidiary": 10 # ID Japan
    },
    {
        "companyname": "CV Coba Integrasi",
        "email": "admin@cobain.com",
        "phone": "08999888777",
        "subsidiary": 10
    }
]

# 5. FUNGSI UTAMA: Tembak data ke NetSuite Standard REST API
def push_ke_netsuite(record_type, payload_data):
    # Format URL sesuai dokumentasi NetSuite
    url = f"https://{ACCOUNT_ID.lower()}.suitetalk.api.netsuite.com/services/rest/record/v1/{record_type}"
     
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        # Proses nembak API
        response = requests.post(url, auth=auth, json=payload_data, headers=headers)
        
        # NetSuite balikin 204 kalau Create sukses
        if response.status_code == 204:
            print(f"✅ SUKSES: Data '{payload_data['companyname']}' berhasil masuk NetSuite!")
            # Ambil ID yang baru dibikin dari header
            print(f"   => URL/ID Baru: {response.headers.get('Location')}\n")
        else:
            print(f"❌ GAGAL masukin '{payload_data['companyname']}'")
            print(f"   => Detail Error: {response.status_code} - {response.text}\n")
            
    except Exception as e:
        print(f"⚠️ Sistem Error: {str(e)}")

# 6. JALANKAN: Looping array datanya satu-satu
if __name__ == "__main__":
    print("🚀 Memulai proses tembak data ke NetSuite...\n")
    
    # Kita loop isi array data_customers
    for customer in data_customers:
        # Panggil fungsi push, kasih tau tipenya 'customer'
        push_ke_netsuite('customer', customer)
        
    print("🎉 Semua proses selesai!")