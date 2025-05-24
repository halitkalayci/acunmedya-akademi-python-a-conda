# Indexing => Projenizin dosyalarının ilgili AI'a aktarılması. 

# Context => Sizin belirlediğiniz proje dosyalarının ilgili prompt ile aktarılması.

# Back Tick => `` ``

# Clean Tree => Githuba göndereceğim hiç bir değişiklik olmaması.

# Kural 1 -> Her prompt öncesi clean tree çalış!

# ===============================================
# EV FİYAT TAHMİNİ - DECISION TREE MODELİ
# ===============================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# Veri setini yükleme
df = pd.read_csv('ev_fiyat_dataset.csv')

print("=== EV FİYAT TAHMİNİ - DECISION TREE ALGORİTMASI ===")
print(f"Veri seti boyutu: {df.shape}")
print(f"Sütunlar: {list(df.columns)}")

# Veri ön işleme - Kategorik değişkenleri sayısal değerlere dönüştürme
le_mahalle = LabelEncoder()
le_isitma = LabelEncoder()

df['mahalle_encoded'] = le_mahalle.fit_transform(df['mahalle'])
df['isitma_encoded'] = le_isitma.fit_transform(df['isitma_turu'])

# Özellik ve hedef değişkenleri belirleme
features = ['metrekare', 'oda_sayisi', 'banyo_sayisi', 'yas', 'kat', 
           'garaj', 'bahce', 'mahalle_encoded', 'isitma_encoded']

X = df[features]
y = df['fiyat']

# Veriyi eğitim ve test setlerine ayırma (%80 eğitim, %20 test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nEğitim seti boyutu: {X_train.shape}")
print(f"Test seti boyutu: {X_test.shape}")

# Decision Tree Regressor modeli oluşturma ve eğitme
dt_model = DecisionTreeRegressor(
    max_depth=10,           # Ağacın maksimum derinliği
    min_samples_split=5,    # Bir düğümün bölünmesi için gereken minimum örnek sayısı
    min_samples_leaf=2,     # Yaprak düğümde olması gereken minimum örnek sayısı
    random_state=42
)

# Modeli eğitme
dt_model.fit(X_train, y_train)

# Tahmin yapma
y_pred = dt_model.predict(X_test)

# Model performansını değerlendirme
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Sonuçları yazdırma
print("\n=== DECISION TREE MODEL PERFORMANSI ===")
print(f"Mean Absolute Error (MAE): {mae:,.0f} TL")
print(f"Mean Squared Error (MSE): {mse:,.0f} TL²")
print(f"Root Mean Square Error (RMSE): {rmse:,.0f} TL")
print(f"R² Score (Belirleyicilik Katsayısı): {r2:.4f}")
print(f"Model Doğruluğu: %{r2*100:.2f}")

# Özellik önem derecelerini gösterme
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': dt_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n=== ÖZELLİK ÖNEM DERECELERİ ===")
for idx, row in feature_importance.iterrows():
    print(f"{row['feature']}: {row['importance']:.4f} ({row['importance']*100:.2f}%)")

# Örnek tahminler gösterme
print("\n=== ÖRNEK TAHMİNLER ===")
sample_indices = [0, 1, 2, 3, 4]  # İlk 5 test örneği

for i, idx in enumerate(sample_indices):
    gerçek = y_test.iloc[idx]
    tahmin = y_pred[idx]
    hata_oranı = abs(gerçek - tahmin) / gerçek * 100
    
    print(f"\nÖrnek {i+1}:")
    print(f"  Gerçek fiyat: {gerçek:,.0f} TL")
    print(f"  Tahmini fiyat: {tahmin:,.0f} TL")
    print(f"  Fark: {abs(gerçek - tahmin):,.0f} TL")
    print(f"  Hata oranı: %{hata_oranı:.2f}")

# Modelin genel değerlendirmesi
print("\n=== MODEL DEĞERLENDİRMESİ ===")
if r2 >= 0.8:
    print("🟢 ÇOK İYİ: Model çok yüksek doğrulukla tahmin yapıyor.")
elif r2 >= 0.7:
    print("🟡 İYİ: Model iyi seviyede tahmin yapıyor.")
elif r2 >= 0.5:
    print("🟠 ORTA: Model orta seviyede tahmin yapıyor.")
else:
    print("🔴 ZAYIF: Model zayıf performans gösteriyor.")

print(f"\nOrtalama tahmin hatası: {mae/1000000:.1f} Milyon TL")
print(f"Modelin açıklayabildiği varyans: %{r2*100:.1f}")