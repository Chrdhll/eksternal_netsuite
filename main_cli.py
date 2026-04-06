import os
import requests
import json
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# ==========================================
# 1. SETUP OTENTIKASI
# ==========================================
load_dotenv()
ACCOUNT_ID = os.getenv('NETSUITE_ACCOUNT_ID')
CONSUMER_KEY = os.getenv('NETSUITE_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('NETSUITE_CONSUMER_SECRET')
TOKEN_ID = os.getenv('NETSUITE_TOKEN_ID')
TOKEN_SECRET = os.getenv('NETSUITE_TOKEN_SECRET')

auth = OAuth1(
    CONSUMER_KEY, CONSUMER_SECRET, TOKEN_ID, TOKEN_SECRET,
    realm=ACCOUNT_ID, signature_method='HMAC-SHA256'
)

# ==========================================
# 2. FUNGSI GET ALL (PAKAI SUITEQL - CEPAT)
# ==========================================
def tarik_semua_data(record_type):
    url = f"https://{ACCOUNT_ID.lower()}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql"
    headers = {"Content-Type": "application/json", "Prefer": "transient"}
    
    query_sql = f"SELECT id, name as nama FROM Department" if record_type == 'department' else f"SELECT id, companyname as nama FROM Customer"
    payload = {"q": query_sql}
    
    print(f"\n narik semua data {record_type}...")
    try:
        response = requests.post(url, auth=auth, json=payload, headers=headers)
        if response.status_code == 200:
            print("\n✅ DAFTAR DATA:")
            print(json.dumps(response.json().get('items', []), indent=4))
        else:
            print(f"❌ GAGAL: {response.text}")
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")

# ==========================================
# 3. FUNGSI GET BY ID (BARU - DETAIL)
# ==========================================
def tarik_data_by_id(record_type, record_id):
    # Menggunakan Standard Record API untuk ambil detail 1 record
    url = f"https://{ACCOUNT_ID.lower()}.suitetalk.api.netsuite.com/services/rest/record/v1/{record_type}/{record_id}"
    headers = {"Accept": "application/json"}
    
    print(f"\n🔍 Mencari detail {record_type} dengan ID: {record_id}...")
    try:
        response = requests.get(url, auth=auth, headers=headers)
        if response.status_code == 200:
            print("\n✅ DETAIL DATA DITEMUKAN:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"❌ DATA TIDAK ADA: {response.status_code} - ID {record_id} mungkin salah.")
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")

# ==========================================
# 4. FUNGSI POST (CREATE)
# ==========================================
def bikin_data(record_type, payload):
    url = f"https://{ACCOUNT_ID.lower()}.suitetalk.api.netsuite.com/services/rest/record/v1/{record_type}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    try:
        response = requests.post(url, auth=auth, json=payload, headers=headers)
        if response.status_code == 204:
            url_baru = response.headers.get('Location')
            id_baru = url_baru.split('/')[-1] if url_baru else "Tidak diketahui"
            print(f"✅ SUKSES! Data berhasil dibuat dengan ID: {id_baru}")
        else:
            print(f"❌ GAGAL: {response.text}")
    except Exception as e:
        print(f"⚠️ Error: {str(e)}")

# ==========================================
# 5. MENU UTAMA (CLI INTERAKTIF)
# ==========================================
def main():
    while True:
        print("\n" + "="*45)
        print("🚀 NETSUITE PYTHON CLI V2 - BY FADHIL")
        print("="*45)
        print("1. Tarik Semua Data (Get All)")
        print("2. Cari Data Spesifik (Get by ID)")
        print("3. Bikin Data Baru (Post)")
        print("4. Keluar (Exit)")
        
        pilihan = input("\n👉 Pilih menu (1/2/3/4): ")
        
        if pilihan == '1':
            tipe = input("📦 Tipe data? (department/customer): ").strip().lower()
            tarik_semua_data(tipe)
                
        elif pilihan == '2':
            tipe = input("📦 Tipe data? (department/customer): ").strip().lower()
            id_data = input("🆔 Masukkan ID yang dicari: ").strip()
            tarik_data_by_id(tipe, id_data)

        elif pilihan == '3':
            tipe = input("📦 Tipe data? (department/customer): ").strip().lower()
            if tipe == 'department':
                nama = input("📝 Nama Dept: ")
                bikin_data(tipe, {"name": nama})
            elif tipe == 'customer':
                nama = input("📝 Nama PT: ")
                bikin_data(tipe, {"companyname": nama, "subsidiary": 10})
                
        elif pilihan == '4':
            print("👋 Bye!")
            break
        else:
            print("❌ Pilihan salah!")

if __name__ == "__main__":
    main()