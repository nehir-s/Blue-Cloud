# 💧 TURKCELL BLUE CLOUD 
**5G Destekli Akıllı Su Yönetimi ve Dinamik Bulut Orkestrasyonu**

Bu proje, Turkcell’in dijital gücünü Google’ın "2030 Water Positive" vizyonuyla birleştirerek, veri merkezlerinin su tüketimini bölgesel su stresine göre optimize eden bir **Karar Destek Sistemi (DSS)** prototipidir.

## 🚀 Öne Çıkan Özellikler
- **Dinamik WUE Analizi:** Ankara, Gebze, İzmir ve Çorlu lokasyonları için anlık su stresi hesaplaması.
- **Seçici Aktarım (Selective Migration):** İş yüklerini P1 (Kritik) - P3 (Esnek) hiyerarşisine göre sınıflandırarak güvenli veri transferi.
- **Tasarruf Simülasyonu:** Operasyonel hamlelerin su stresine etkisini anlık olarak hesaplayan analitik arayüz.

## 🛠️ Teknik Altyapı
- **Backend/Frontend:** Python & Streamlit
- **Veri Görselleştirme:** Plotly (Dinamik Kapasite & Stres Grafikleri)
- **Mimari:** Google Cloud Anthos & 5G URLLC (Simüle edilmiştir)

## 📦 Kurulum
Prototipi çalıştırmak için:
```bash
pip install streamlit pandas plotly
streamlit run app.py
