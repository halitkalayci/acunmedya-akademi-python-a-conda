"""
EV FİYAT TAHMİNİ API TEST SCRİPTİ
API'nin çalışıp çalışmadığını test eder
"""

import requests
import json
import time

# API adresi
BASE_URL = "http://localhost:8000"

def api_test():
    """API'yi test et"""
    
    print("🏠 EV FİYAT TAHMİNİ API TESTİ")
    print("=" * 50)
    
    # 1. Ana sayfa testi
    try:
        print("\n1️⃣ Ana sayfa testi...")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Ana sayfa başarılı!")
        else:
            print(f"❌ Ana sayfa hatası: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ API'ye bağlanılamıyor. API çalışıyor mu? Hata: {e}")
        print("💡 Önce 'python api.py' komutunu çalıştırın!")
        return
    
    # 2. Model performansı testi
    print("\n2️⃣ Model performansı testi...")
    try:
        response = requests.get(f"{BASE_URL}/model/performans")
        if response.status_code == 200:
            performans = response.json()
            print("✅ Model performansı alındı!")
            print(f"   📊 R² Score: {performans['r2_score']:.4f}")
            print(f"   📊 Doğruluk: %{performans['model_dogrulugu_yuzde']:.2f}")
        else:
            print(f"❌ Performans hatası: {response.status_code}")
    except Exception as e:
        print(f"❌ Performans testi hatası: {e}")
    
    # 3. Mahalle listesi testi
    print("\n3️⃣ Mahalle listesi testi...")
    try:
        response = requests.get(f"{BASE_URL}/mahalleler")
        if response.status_code == 200:
            mahalleler = response.json()
            print(f"✅ {mahalleler['toplam_mahalle_sayisi']} mahalle bulundu!")
            print(f"   📍 İlk 5 mahalle: {', '.join(mahalleler['mahalleler'][:5])}")
        else:
            print(f"❌ Mahalle listesi hatası: {response.status_code}")
    except Exception as e:
        print(f"❌ Mahalle testi hatası: {e}")
    
    # 4. Fiyat tahmini testi
    print("\n4️⃣ Fiyat tahmini testi...")
    
    # Test verileri
    test_evleri = [
        {
            "isim": "Orta Seviye Ev (Kadıköy)",
            "veri": {
                "metrekare": 120,
                "oda_sayisi": 3,
                "banyo_sayisi": 2,
                "yas": 5,
                "kat": 4,
                "mahalle": "Kadıköy",
                "garaj": 1,
                "bahce": 0,
                "isitma_turu": "Doğalgaz"
            }
        },
        {
            "isim": "Lüks Ev (Levent)",
            "veri": {
                "metrekare": 200,
                "oda_sayisi": 4,
                "banyo_sayisi": 2,
                "yas": 10,
                "kat": 8,
                "mahalle": "Levent",
                "garaj": 1,
                "bahce": 1,
                "isitma_turu": "Merkezi"
            }
        },
        {
            "isim": "Ekonomik Ev (Pendik)",
            "veri": {
                "metrekare": 80,
                "oda_sayisi": 2,
                "banyo_sayisi": 1,
                "yas": 15,
                "kat": 2,
                "mahalle": "Pendik",
                "garaj": 0,
                "bahce": 0,
                "isitma_turu": "Kombi"
            }
        }
    ]
    
    for test_ev in test_evleri:
        try:
            print(f"\n   🏡 {test_ev['isim']} test ediliyor...")
            response = requests.post(f"{BASE_URL}/tahmin", json=test_ev['veri'])
            
            if response.status_code == 200:
                sonuc = response.json()
                print(f"   ✅ Tahmin başarılı!")
                print(f"   💰 Tahmini Fiyat: {sonuc['fiyat_formatli']}")
                print(f"   📊 Model Doğruluğu: %{sonuc['model_dogrulugu']*100:.2f}")
            else:
                print(f"   ❌ Tahmin hatası: {response.status_code}")
                print(f"   📝 Hata mesajı: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Test hatası: {e}")
        
        time.sleep(0.5)  # API'ye fazla yük bindirmemek için bekle
    
    # 5. Hatalı veri testi
    print("\n5️⃣ Hatalı veri testi...")
    hatali_veri = {
        "metrekare": 1000,  # Çok yüksek
        "oda_sayisi": 15,   # Çok yüksek
        "banyo_sayisi": 1,
        "yas": 5,
        "kat": 4,
        "mahalle": "Geçersiz_Mahalle",  # Geçersiz mahalle
        "garaj": 1,
        "bahce": 0,
        "isitma_turu": "Doğalgaz"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/tahmin", json=hatali_veri)
        if response.status_code == 422 or response.status_code == 400:
            print("✅ Hatalı veri testi başarılı! API geçersiz verileri reddetti.")
        else:
            print(f"⚠️  Beklenmeyen durum: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Hatalı veri testi hatası: {e}")
    
    # Test özeti
    print("\n" + "=" * 50)
    print("🎉 TEST TAMAMLANDI!")
    print("\n💡 Şimdi tarayıcınızda şu adresi ziyaret edebilirsiniz:")
    print("   📖 API Dokümantasyonu: http://localhost:8000/docs")
    print("   🏠 Ana Sayfa: http://localhost:8000/")

if __name__ == "__main__":
    api_test() 