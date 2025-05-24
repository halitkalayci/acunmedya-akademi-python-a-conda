import pandas as pd
import numpy as np
import random

# Rastgele tohum ayarlama (tekrarlanabilir sonuçlar için)
np.random.seed(42)
random.seed(42)

# Veri sayısı
n_samples = 1500

# Mahalle listesi
mahalles = ['Beşiktaş', 'Şişli', 'Kadıköy', 'Üsküdar', 'Beylikdüzü', 'Başakşehir', 
           'Maltepe', 'Kartal', 'Pendik', 'Ataşehir', 'Bahçelievler', 'Bakırköy',
           'Zeytinburnu', 'Fatih', 'Beyoğlu', 'Sarıyer', 'Etiler', 'Levent']

# Isıtma türleri
heating_types = ['Doğalgaz', 'Kombi', 'Merkezi', 'Elektrik', 'Kömür', 'Klima']

# Veri seti oluşturma
data = []

for i in range(n_samples):
    # Temel özellikler
    metrekare = np.random.randint(50, 300)  # 50-300 m2 arası
    oda_sayisi = np.random.choice([1, 2, 3, 4, 5, 6], p=[0.05, 0.15, 0.25, 0.30, 0.20, 0.05])
    banyo_sayisi = min(oda_sayisi, np.random.choice([1, 2, 3, 4], p=[0.4, 0.35, 0.20, 0.05]))
    yas = np.random.randint(0, 50)  # 0-50 yaş arası
    kat = np.random.randint(0, 20)  # Zemin kat: 0, 1-19. katlar
    mahalle = random.choice(mahalles)
    garaj = np.random.choice([0, 1], p=[0.6, 0.4])  # 40% garajlı
    bahce = np.random.choice([0, 1], p=[0.7, 0.3])  # 30% bahçeli
    isitma_turu = random.choice(heating_types)
    
    # Fiyat hesaplama (gerçekçi faktörler dahil)
    base_price = metrekare * 15000  # m2 başına temel fiyat
    
    # Mahalle faktörü
    mahalle_multiplier = {
        'Beşiktaş': 1.8, 'Şişli': 1.7, 'Etiler': 2.2, 'Levent': 2.0, 'Sarıyer': 1.6,
        'Kadıköy': 1.5, 'Üsküdar': 1.4, 'Ataşehir': 1.3, 'Beyoğlu': 1.2,
        'Beylikdüzü': 1.1, 'Başakşehir': 1.0, 'Maltepe': 0.9, 'Kartal': 0.8,
        'Pendik': 0.7, 'Bahçelievler': 1.0, 'Bakırköy': 1.2, 'Zeytinburnu': 0.9,
        'Fatih': 1.1
    }
    
    base_price *= mahalle_multiplier.get(mahalle, 1.0)
    
    # Diğer faktörler
    if oda_sayisi >= 4:
        base_price *= 1.1
    if banyo_sayisi >= 3:
        base_price *= 1.05
    if yas < 5:
        base_price *= 1.3  # Yeni ev bonusu
    elif yas > 30:
        base_price *= 0.8  # Eski ev cezası
    if kat >= 5 and kat <= 10:
        base_price *= 1.1  # Optimal kat bonusu
    elif kat > 15:
        base_price *= 0.95  # Çok yüksek kat cezası
    if garaj:
        base_price *= 1.08
    if bahce:
        base_price *= 1.12
    if isitma_turu in ['Doğalgaz', 'Merkezi']:
        base_price *= 1.05
    
    # Rastgele varyasyon ekleme (%±20)
    variation = np.random.uniform(0.8, 1.2)
    final_price = int(base_price * variation)
    
    # Veriyi listeye ekleme
    data.append({
        'metrekare': metrekare,
        'oda_sayisi': oda_sayisi,
        'banyo_sayisi': banyo_sayisi,
        'yas': yas,
        'kat': kat,
        'mahalle': mahalle,
        'garaj': garaj,
        'bahce': bahce,
        'isitma_turu': isitma_turu,
        'fiyat': final_price
    })

# DataFrame oluşturma
df = pd.DataFrame(data)

# CSV dosyasına kaydetme
df.to_csv('house_price_ml_aigenerated/ev_fiyat_dataset.csv', index=False, encoding='utf-8-sig')
