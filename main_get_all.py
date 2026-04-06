import os
import requests
import json
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

# 1. BUKA BRANKAS & AMBIL KUNCI
load_dotenv()
ACCOUNT_ID = os.getenv('NETSUITE_ACCOUNT_ID')
CONSUMER_KEY = os.getenv('NETSUITE_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('NETSUITE_CONSUMER_SECRET')
TOKEN_ID = os.getenv('NETSUITE_TOKEN_ID')
TOKEN_SECRET = os.getenv('NETSUITE_TOKEN_SECRET')

auth = OAuth1(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    TOKEN_ID,
    TOKEN_SECRET,
    realm=ACCOUNT_ID,
    signature_method='HMAC-SHA256'
)

# 2. FUNGSI NARIK & NGERAPIIN DATA
def get_semua_data_rapi(record_type):
    url = f"https://{ACCOUNT_ID.lower()}.suitetalk.api.netsuite.com/services/rest/record/v1/{record_type}"
    headers = {"Accept": "application/json"}

    try:
        # Step A: Tarik "Buku Menu" (List ID)
        response = requests.get(url, auth=auth, headers=headers)
        
        if response.status_code == 200:
            data_json = response.json()
            list_items = data_json.get('items', [])
            
            print(f"⏳ Menunggu... sedang memproses {len(list_items)} data {record_type} dari NetSuite...\n")
            
            # --- INI KUNCINYA: Kita bikin Array kosong buat nampung data rapi ---
            array_data_rapi = []
            
            # Step B: Looping tarik detailnya
            for item in list_items:
                record_id = item.get('id')
                url_detail = f"{url}/{record_id}"
                
                res_detail = requests.get(url_detail, auth=auth, headers=headers)
                
                if res_detail.status_code == 200:
                    detail_data = res_detail.json()
                    
                    # Step C: Kita "Mapping" (Pilih field yang mau ditampilin aja)
                    # Kalau type-nya department, ambil 'name'. Kalau customer, ambil 'companyname'
                    nama_field = detail_data.get('name') if record_type == 'department' else detail_data.get('companyname')
                    
                    objek_rapi = {
                        "id": record_id,
                        "nama": nama_field
                    }
                    
                    # Masukin ke dalam Array
                    array_data_rapi.append(objek_rapi)

            # Step D: Bungkus semua pakai format JSON kustom kita
            hasil_akhir = {
                "success": True,
                "type": record_type,
                "count": len(array_data_rapi),
                "data": array_data_rapi
            }
            
            # Step E: Print JSON-nya ke terminal dengan indentasi 4 spasi biar cantik
            print(json.dumps(hasil_akhir, indent=4))
            
            # Return datanya biar bisa dipakai sama fungsi Python lain kalau butuh
            return hasil_akhir
            
        else:
            print(f"❌ GAGAL: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"⚠️ Sistem Error: {str(e)}")
        return None

# 3. JALANKAN EKSEKUSI
if __name__ == "__main__":
    # Panggil fungsinya untuk nampilin data department yang udah rapi
    get_semua_data_rapi('department')