"""
EV FİYAT TAHMİNİ API
FastAPI kullanarak Decision Tree modeli ile ev fiyat tahmini servisi
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import pickle
import os
from datetime import datetime
import uvicorn

# FastAPI uygulaması oluşturma
app = FastAPI(
    title="Ev Fiyat Tahmini API",
    description="Decision Tree algoritması kullanarak ev fiyat tahmini yapan API servisi",
    version="1.0.0"
)

# Global değişkenler
model = None
le_mahalle = None
le_isitma = None
model_metrics = {}

# Pydantic modelleri
class EvBilgileri(BaseModel):
    metrekare: int = Field(..., ge=30, le=500, description="Evin metrekaresi (30-500 m²)")
    oda_sayisi: int = Field(..., ge=1, le=10, description="Oda sayısı (1-10)")
    banyo_sayisi: int = Field(..., ge=1, le=5, description="Banyo sayısı (1-5)")
    yas: int = Field(..., ge=0, le=50, description="Evin yaşı (0-50 yıl)")
    kat: int = Field(..., ge=0, le=30, description="Kat numarası (0-30)")
    mahalle: str = Field(..., description="Mahalle adı")
    garaj: int = Field(..., ge=0, le=1, description="Garaj var mı? (0: Hayır, 1: Evet)")
    bahce: int = Field(..., ge=0, le=1, description="Bahçe var mı? (0: Hayır, 1: Evet)")
    isitma_turu: str = Field(..., description="Isıtma türü")

class TahminSonucu(BaseModel):
    tahmini_fiyat: float
    fiyat_formatli: str
    model_dogrulugu: float
    tahmin_tarihi: str

class ModelPerformans(BaseModel):
    mae: float
    mse: float  
    rmse: float
    r2_score: float
    model_dogrulugu_yuzde: float
    toplam_test_sayisi: int

class OzellikOnem(BaseModel):
    ozellik: str
    onem_derecesi: float
    onem_yuzde: float

# Yardımcı fonksiyonlar
def model_yukle_veya_egit():
    """Model dosyası varsa yükle, yoksa eğit"""
    global model, le_mahalle, le_isitma, model_metrics
    
    model_dosyasi = "ev_fiyat_modeli.pkl"
    
    if os.path.exists(model_dosyasi):
        # Mevcut modeli yükle
        with open(model_dosyasi, 'rb') as f:
            model_data = pickle.load(f)
            model = model_data['model']
            le_mahalle = model_data['le_mahalle']
            le_isitma = model_data['le_isitma']
            model_metrics = model_data['metrics']
        print("✅ Mevcut model başarıyla yüklendi!")
    else:
        # Yeni model eğit
        egit_model()

def egit_model():
    """Modeli eğit ve kaydet"""
    global model, le_mahalle, le_isitma, model_metrics
    
    try:
        # Veri setini yükle
        df = pd.read_csv('ev_fiyat_dataset.csv')
        
        # Kategorik değişkenleri encode et
        le_mahalle = LabelEncoder()
        le_isitma = LabelEncoder()
        
        df['mahalle_encoded'] = le_mahalle.fit_transform(df['mahalle'])
        df['isitma_encoded'] = le_isitma.fit_transform(df['isitma_turu'])
        
        # Özellik ve hedef değişkenleri belirle
        features = ['metrekare', 'oda_sayisi', 'banyo_sayisi', 'yas', 'kat', 
                   'garaj', 'bahce', 'mahalle_encoded', 'isitma_encoded']
        
        X = df[features]
        y = df['fiyat']
        
        # Veriyi böl
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Model oluştur ve eğit
        model = DecisionTreeRegressor(
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Model performansını hesapla
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        model_metrics = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2_score': r2,
            'test_size': len(y_test)
        }
        
        # Modeli kaydet
        model_data = {
            'model': model,
            'le_mahalle': le_mahalle,
            'le_isitma': le_isitma,
            'metrics': model_metrics
        }
        
        with open('ev_fiyat_modeli.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✅ Model başarıyla eğitildi! R² Score: {r2:.4f}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model eğitimi sırasında hata: {str(e)}")

def fiyat_formatla(fiyat: float) -> str:
    """Fiyatı okunabilir formatta göster"""
    if fiyat >= 1_000_000:
        return f"{fiyat/1_000_000:.2f} Milyon TL"
    elif fiyat >= 1_000:
        return f"{fiyat/1_000:.0f}.{int((fiyat%1_000)/100)} Bin TL"
    else:
        return f"{fiyat:.0f} TL"

# API Endpoint'leri
@app.on_event("startup")
async def startup_event():
    """Uygulama başlatıldığında model yükle"""
    model_yukle_veya_egit()

@app.get("/")
async def ana_sayfa():
    """API ana sayfa bilgileri"""
    return {
        "mesaj": "Ev Fiyat Tahmini API'sine Hoş Geldiniz! 🏠",
        "versiyon": "1.0.0",
        "kullanilabilir_endpoint_ler": {
            "POST /tahmin": "Ev fiyat tahmini yap",
            "GET /model/performans": "Model performans bilgileri",
            "GET /model/ozellik-onem": "Özellik önem dereceleri",
            "POST /model/yeniden-egit": "Modeli yeniden eğit",
            "GET /mahalleler": "Kullanılabilir mahalle listesi",
            "GET /isitma-turleri": "Kullanılabilir ısıtma türleri"
        }
    }

@app.post("/tahmin", response_model=TahminSonucu)
async def fiyat_tahmini(ev_bilgileri: EvBilgileri):
    """Ev bilgilerine göre fiyat tahmini yap"""
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model henüz yüklenmedi")
    
    try:
        # Mahalle kontrolü
        if ev_bilgileri.mahalle not in le_mahalle.classes_:
            mevcut_mahalleler = ", ".join(le_mahalle.classes_)
            raise HTTPException(
                status_code=400, 
                detail=f"Geçersiz mahalle: {ev_bilgileri.mahalle}. Geçerli mahalleler: {mevcut_mahalleler}"
            )
        
        # Isıtma türü kontrolü
        if ev_bilgileri.isitma_turu not in le_isitma.classes_:
            mevcut_isitma = ", ".join(le_isitma.classes_)
            raise HTTPException(
                status_code=400,
                detail=f"Geçersiz ısıtma türü: {ev_bilgileri.isitma_turu}. Geçerli türler: {mevcut_isitma}"
            )
        
        # Kategorik değerleri encode et
        mahalle_encoded = le_mahalle.transform([ev_bilgileri.mahalle])[0]
        isitma_encoded = le_isitma.transform([ev_bilgileri.isitma_turu])[0]
        
        # Tahmin için veri hazırla
        tahmin_verisi = np.array([[
            ev_bilgileri.metrekare,
            ev_bilgileri.oda_sayisi,
            ev_bilgileri.banyo_sayisi,
            ev_bilgileri.yas,
            ev_bilgileri.kat,
            ev_bilgileri.garaj,
            ev_bilgileri.bahce,
            mahalle_encoded,
            isitma_encoded
        ]])
        
        # Tahmin yap
        tahmini_fiyat = model.predict(tahmin_verisi)[0]
        
        return TahminSonucu(
            tahmini_fiyat=float(tahmini_fiyat),
            fiyat_formatli=fiyat_formatla(tahmini_fiyat),
            model_dogrulugu=model_metrics.get('r2_score', 0.0),
            tahmin_tarihi=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin yapılırken hata: {str(e)}")

@app.get("/model/performans", response_model=ModelPerformans)
async def model_performans():
    """Model performans metriklerini döndür"""
    
    if not model_metrics:
        raise HTTPException(status_code=500, detail="Model metrikleri bulunamadı")
    
    return ModelPerformans(
        mae=model_metrics['mae'],
        mse=model_metrics['mse'],
        rmse=model_metrics['rmse'],
        r2_score=model_metrics['r2_score'],
        model_dogrulugu_yuzde=model_metrics['r2_score'] * 100,
        toplam_test_sayisi=model_metrics['test_size']
    )

@app.get("/model/ozellik-onem", response_model=List[OzellikOnem])
async def ozellik_onem_dereceleri():
    """Model özellik önem derecelerini döndür"""
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model henüz yüklenmedi")
    
    feature_names = ['metrekare', 'oda_sayisi', 'banyo_sayisi', 'yas', 'kat', 
                    'garaj', 'bahce', 'mahalle', 'isitma_turu']
    
    onem_listesi = []
    for i, importance in enumerate(model.feature_importances_):
        onem_listesi.append(OzellikOnem(
            ozellik=feature_names[i],
            onem_derecesi=float(importance),
            onem_yuzde=float(importance * 100)
        ))
    
    # Önem derecesine göre sırala
    onem_listesi.sort(key=lambda x: x.onem_derecesi, reverse=True)
    
    return onem_listesi

@app.post("/model/yeniden-egit")
async def modeli_yeniden_egit():
    """Modeli yeniden eğit"""
    
    try:
        egit_model()
        return {
            "mesaj": "Model başarıyla yeniden eğitildi! ✅",
            "r2_score": model_metrics['r2_score'],
            "mae": model_metrics['mae'],
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model eğitimi hatası: {str(e)}")

@app.get("/mahalleler")
async def kullanilabilir_mahalleler():
    """Kullanılabilir mahalle listesini döndür"""
    
    if le_mahalle is None:
        raise HTTPException(status_code=500, detail="Label encoder henüz yüklenmedi")
    
    return {
        "mahalleler": sorted(le_mahalle.classes_.tolist()),
        "toplam_mahalle_sayisi": len(le_mahalle.classes_)
    }

@app.get("/isitma-turleri")
async def kullanilabilir_isitma_turleri():
    """Kullanılabilir ısıtma türlerini döndür"""
    
    if le_isitma is None:
        raise HTTPException(status_code=500, detail="Label encoder henüz yüklenmedi")
    
    return {
        "isitma_turleri": sorted(le_isitma.classes_.tolist()),
        "toplam_tür_sayisi": len(le_isitma.classes_)
    }

@app.get("/ornek-tahmin")
async def ornek_tahmin_verileri():
    """Örnek tahmin verileri döndür"""
    return {
        "ornek_1": {
            "metrekare": 120,
            "oda_sayisi": 3,
            "banyo_sayisi": 2,
            "yas": 5,
            "kat": 4,
            "mahalle": "Kadıköy",
            "garaj": 1,
            "bahce": 0,
            "isitma_turu": "Doğalgaz"
        },
        "ornek_2": {
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
    }

# Uygulama çalıştırma
if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 