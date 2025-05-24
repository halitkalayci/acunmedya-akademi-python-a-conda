# 🏠 Ev Fiyat Tahmini API Kullanım Kılavuzu

Bu API, Decision Tree algoritması kullanarak ev fiyat tahmini yapan bir web servisidir.

## 📋 Kurulum

### 1. Gereksinimler
```bash
pip install -r requirements.txt
```

### 2. API'yi Başlatma
```bash
python api.py
```

API varsayılan olarak `http://localhost:8000` adresinde çalışacaktır.

## 🚀 API Endpoint'leri

### 1. Ana Sayfa
**GET /** 
- API hakkında genel bilgi alın

### 2. Fiyat Tahmini
**POST /tahmin**
- Ev bilgilerine göre fiyat tahmini yapın

**Örnek İstek:**
```json
{
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
```

**Örnek Yanıt:**
```json
{
  "tahmini_fiyat": 3850000.0,
  "fiyat_formatli": "3.85 Milyon TL",
  "model_dogrulugu": 0.8234,
  "tahmin_tarihi": "2024-01-15 14:30:25"
}
```

### 3. Model Performansı
**GET /model/performans**
- Model performans metriklerini görüntüleyin

**Örnek Yanıt:**
```json
{
  "mae": 542890.25,
  "mse": 658942150000.0,
  "rmse": 811764.82,
  "r2_score": 0.8234,
  "model_dogrulugu_yuzde": 82.34,
  "toplam_test_sayisi": 300
}
```

### 4. Özellik Önem Dereceleri
**GET /model/ozellik-onem**
- Hangi özelliklerin fiyat tahmininde daha önemli olduğunu gösterir

### 5. Model Yeniden Eğitimi
**POST /model/yeniden-egit**
- Modeli yeniden eğitir

### 6. Kullanılabilir Mahalleler
**GET /mahalleler**
- Tahmin yapabileceğiniz mahalle listesini alın

### 7. Kullanılabilir Isıtma Türleri
**GET /isitma-turleri**
- Geçerli ısıtma türlerini listeleyin

### 8. Örnek Veriler
**GET /ornek-tahmin**
- Test için kullanabileceğiniz örnek verileri alın

## 📊 Desteklenen Mahalleler
- Ataşehir
- Bahçelievler
- Bakırköy
- Başakşehir
- Beşiktaş
- Beylikdüzü
- Beyoğlu
- Etiler
- Fatih
- Kadıköy
- Kartal
- Levent
- Maltepe
- Pendik
- Sarıyer
- Şişli
- Üsküdar
- Zeytinburnu

## 🔥 Desteklenen Isıtma Türleri
- Doğalgaz
- Elektrik
- Klima
- Kombi
- Kömür
- Merkezi

## 📝 Parametre Açıklamaları

| Parametre | Tip | Açıklama | Min | Max |
|-----------|-----|----------|-----|-----|
| metrekare | int | Evin metrekaresi | 30 | 500 |
| oda_sayisi | int | Oda sayısı | 1 | 10 |
| banyo_sayisi | int | Banyo sayısı | 1 | 5 |
| yas | int | Evin yaşı (yıl) | 0 | 50 |
| kat | int | Kat numarası | 0 | 30 |
| mahalle | string | Mahalle adı | - | - |
| garaj | int | Garaj (0: Yok, 1: Var) | 0 | 1 |
| bahce | int | Bahçe (0: Yok, 1: Var) | 0 | 1 |
| isitma_turu | string | Isıtma türü | - | - |

## 🌐 Swagger UI
API'yi test etmek için tarayıcınızda şu adresi ziyaret edin:
```
http://localhost:8000/docs
```

## 📱 Python ile Kullanım Örneği

```python
import requests
import json

# API adresi
BASE_URL = "http://localhost:8000"

# Ev bilgileri
ev_verisi = {
    "metrekare": 150,
    "oda_sayisi": 4,
    "banyo_sayisi": 2,
    "yas": 8,
    "kat": 6,
    "mahalle": "Levent",
    "garaj": 1,
    "bahce": 1,
    "isitma_turu": "Merkezi"
}

# Tahmin isteği gönder
response = requests.post(f"{BASE_URL}/tahmin", json=ev_verisi)

if response.status_code == 200:
    sonuc = response.json()
    print(f"Tahmini Fiyat: {sonuc['fiyat_formatli']}")
    print(f"Model Doğruluğu: %{sonuc['model_dogrulugu']*100:.2f}")
else:
    print(f"Hata: {response.text}")
```

## 📝 JavaScript ile Kullanım Örneği

```javascript
const evVerisi = {
    metrekare: 150,
    oda_sayisi: 4,
    banyo_sayisi: 2,
    yas: 8,
    kat: 6,
    mahalle: "Levent",
    garaj: 1,
    bahce: 1,
    isitma_turu: "Merkezi"
};

fetch('http://localhost:8000/tahmin', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(evVerisi)
})
.then(response => response.json())
.then(data => {
    console.log('Tahmini Fiyat:', data.fiyat_formatli);
    console.log('Model Doğruluğu:', (data.model_dogrulugu * 100).toFixed(2) + '%');
})
.catch(error => {
    console.error('Hata:', error);
});
```

## ⚠️ Önemli Notlar

1. **Model Dosyası**: İlk çalıştırmada model otomatik olarak eğitilir ve `ev_fiyat_modeli.pkl` olarak kaydedilir.

2. **Veri Doğrulama**: API, gönderilen verileri otomatik olarak doğrular. Geçersiz değerler için hata mesajı döner.

3. **Performans**: Model R² score değeri yaklaşık %82 doğruluk oranında tahmin yapmaktadır.

4. **CORS**: Farklı domain'lerden erişim için CORS ayarları gerekebilir.

## 🔧 Gelişmiş Ayarlar

### Farklı Port Kullanma
```python
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)
```

### CORS Ekleme
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📞 Destek

API ile ilgili sorunlar için lütfen proje yöneticisiyle iletişime geçin. 