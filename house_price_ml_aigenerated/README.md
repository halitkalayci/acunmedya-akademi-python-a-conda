# Ev Fiyat Tahmini Makine Öğrenmesi Projesi

Bu proje, ev özelliklerine dayalı olarak ev fiyatlarını tahmin eden bir makine öğrenmesi uygulamasıdır.

## 📋 Proje İçeriği

- **Veri Seti**: 1500 satırlık sentetik ev verisi (`ev_fiyat_dataset.csv`)
- **Makine Öğrenmesi Modeli**: Random Forest ve Linear Regression karşılaştırması
- **Özellikler**: Metrekare, oda sayısı, banyo sayısı, yaş, kat, mahalle, garaj, bahçe, ısıtma türü

## 🎯 Model Performansı

### Random Forest (En İyi Model)
- **R² Score**: 0.7268
- **RMSE**: 1,192,626 TL
- **MAE**: 822,588 TL

### Linear Regression
- **R² Score**: 0.5621
- **RMSE**: 1,509,962 TL
- **MAE**: 1,094,691 TL

## 📊 Veri Seti Özellikleri

| Özellik | Açıklama | Tip |
|----------|----------|-----|
| metrekare | Evin büyüklüğü (50-300 m²) | Sayısal |
| oda_sayisi | Oda sayısı (1-6) | Sayısal |
| banyo_sayisi | Banyo sayısı (1-4) | Sayısal |
| yas | Binanın yaşı (0-50 yıl) | Sayısal |
| kat | Kat numarası (0-19) | Sayısal |
| mahalle | Mahalle adı (18 farklı mahalle) | Kategorik |
| garaj | Garaj varlığı (0: Yok, 1: Var) | İkili |
| bahce | Bahçe varlığı (0: Yok, 1: Var) | İkili |
| isitma_turu | Isıtma türü (6 farklı tür) | Kategorik |
| fiyat | Ev fiyatı (TL) | Hedef değişken |

## 🔧 Kurulum

1. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Modeli çalıştırın:
```bash
python ev_fiyat_ml_model.py
```

## 📈 Özellik Önem Sıralaması

1. **Metrekare** (55.39%) - En önemli faktör
2. **Mahalle** (16.75%) - Konum önemli
3. **Yaş** (14.20%) - Binanın yaşı kritik
4. **Kat** (4.34%)
5. **Oda Sayısı** (2.93%)
6. **Isıtma Türü** (2.54%)
7. **Banyo Sayısı** (1.51%)
8. **Bahçe** (1.47%)
9. **Garaj** (0.88%)

## 🏡 Örnek Tahmin

150 m², 3+2, 5 yaşında, 8. kat, Kadıköy'de, garajlı, bahçesiz, doğalgazlı ev:
- **Random Forest tahmini**: ~3,895,000 TL
- **Linear Regression tahmini**: ~4,090,000 TL

## 🗂️ Dosya Yapısı

```
house_price_ml_aigenerated/
├── ev_fiyat_dataset.csv       # Veri seti
├── ev_fiyat_ml_model.py      # Ana model dosyası
├── requirements.txt          # Gerekli kütüphaneler
├── README.md                # Bu dosya
└── main.py                  # Proje notları
```

## 🚀 Gelecek Geliştirmeler

- [ ] Görselleştirme grafikleri ekleme
- [ ] Model hiperparametre optimizasyonu
- [ ] Daha fazla algoritma deneme (XGBoost, Neural Networks)
- [ ] Web arayüzü geliştirme
- [ ] Gerçek veri setleri ile test etme

## 📝 Notlar

- Veri seti sentetik olarak oluşturulmuştur
- Mahalle faktörleri İstanbul bölgelerine göre ayarlanmıştır
- Model %72.68 doğruluk oranına sahiptir
- Random Forest modeli Linear Regression'dan daha iyi performans göstermektedir 