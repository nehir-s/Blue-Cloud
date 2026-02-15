import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Turkcell Blue Cloud - Operational Center", layout="wide")

st.title("💧 Turkcell Blue Cloud | Stratejik Karar Destek Mekanizması")
st.markdown("---")

# 1. Analitik Ağırlıklandırma (Anlık WUE Hesabı İçin)
st.sidebar.header("⚖️ Algoritma Kalibrasyonu")
alpha = st.sidebar.slider("Dış Sıcaklık Etkisi (α)", 0.0, 1.0, 0.45)
beta = st.sidebar.slider("Baraj Doluluk Etkisi (β)", 0.0, 1.0, 0.55)

# 2. Veri Merkezi Ağı (Anlık Durum)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Lokasyon": ["Ankara (Pilot)", "Gebze", "İzmir", "Çorlu"],
        "Sıcaklık": [34, 27, 29, 25],
        "Baraj_Doluluk": [18, 42, 35, 52],
        "Is_Yuku_TB": [500.0, 800.0, 300.0, 200.0]
    })

df = st.session_state.df
df["WUE_Skoru"] = df.apply(lambda x: round((alpha * x["Sıcaklık"]) + (beta * (100 - x["Baraj_Doluluk"])), 1), axis=1)

# 3. Şehir Bazlı İzleme Paneli (Baraj Oranları Geri Geldi)
cols = st.columns(4)
for i, city in enumerate(df["Lokasyon"]):
    with cols[i]:
        st.subheader(city)
        st.metric("WUE Endeksi", df.iloc[i]["WUE_Skoru"],
                  delta="Kritik" if df.iloc[i]["WUE_Skoru"] > 55 else "İdeal",
                  delta_color="inverse" if df.iloc[i]["WUE_Skoru"] > 55 else "normal")

        # Baraj Doluluk Görseli
        st.write(f"**Baraj Doluluğu: %{df.iloc[i]['Baraj_Doluluk']}**")
        st.progress(int(df.iloc[i]['Baraj_Doluluk']))

        st.caption(f"Yük: {df.iloc[i]['Is_Yuku_TB']} TB | Isı: {df.iloc[i]['Sıcaklık']}°C")

st.markdown("---")

# 4. Dinamik Aktarım Planlama ve Anlık Hesaplama
col_plan1, col_plan2 = st.columns([1, 1.2])

with col_plan1:
    st.subheader("📋 Aktarım Yapılandırması")
    source = st.selectbox("Kaynak Lokasyon", df["Lokasyon"], index=0)
    target = st.selectbox("Hedef Lokasyon", df[df["Lokasyon"] != source]["Lokasyon"], index=0)

    st.markdown("**İş Yükü Sınıflandırması:**")
    p3_ratio = st.slider("P3 - Düşük Öncelik (Analiz/Yedek) %", 0, 100, 70)
    p2_ratio = st.slider("P2 - Orta Öncelik (Web/App) %", 0, 100, 20)
    p1_ratio = st.slider("P1 - Kritik (Core System) %", 0, 100, 0)

with col_plan2:
    st.subheader("📊 Tahmini Operasyonel Etki")

    # Mühendislik Hesaplaması:
    # Toplam yükün dağılımı: P3(%40), P2(%40), P1(%20) varsayımıyla ağırlıklı aktarım oranı
    total_moved_perc = (p3_ratio * 0.4) + (p2_ratio * 0.4) + (p1_ratio * 0.2)

    source_wue = df[df["Lokasyon"] == source]["WUE_Skoru"].values[0]
    target_wue = df[df["Lokasyon"] == target]["WUE_Skoru"].values[0]

    # ANLIK GÜNCELLENEN İYİLEŞME ORANI
    net_improvement = round((source_wue - target_wue) * (total_moved_perc / 100), 2)

    # Görsel Uyarı Kutusu
    if net_improvement > 0:
        st.success(f"### Tahmini İyileşme: %{net_improvement}")
        st.write(
            f"**{source}** lokasyonundaki su baskısı, verinin **%{total_moved_perc:.1f}** kadarının **{target}** merkezine kaydırılmasıyla optimize edilecektir.")
    else:
        st.error(f"### Verimlilik Kaybı: %{net_improvement}")
        st.write("Hedef lokasyonun su stresi daha yüksek olduğu için bu işlem önerilmez.")

# 5. Operasyonu Uygula
if st.button("🚀 Operasyonu Onayla ve Sisteme İşle"):
    moved_tb = (df.loc[df["Lokasyon"] == source, "Is_Yuku_TB"].values[0] * (total_moved_perc / 100))
    df.loc[df["Lokasyon"] == source, "Is_Yuku_TB"] -= moved_tb
    df.loc[df["Lokasyon"] == target, "Is_Yuku_TB"] += moved_tb

    with st.status("5G URLLC Hattı Üzerinden Veri Transferi Yapılıyor...", expanded=False):
        time.sleep(2)
    st.info(f"İşlem Tamamlandı: {moved_tb:.1f} TB veri başarıyla {target} lokasyonuna aktarıldı.")

# 6. Dinamik Analiz Grafiği
st.markdown("---")
st.subheader("📈 Ulusal Veri Merkezi Kapasite ve Stres Dağılımı")

fig = go.Figure()
fig.add_trace(go.Bar(x=df["Lokasyon"], y=df["Is_Yuku_TB"], name="İş Yükü (TB)", marker_color='teal', opacity=0.7))
fig.add_trace(
    go.Scatter(x=df["Lokasyon"], y=df["WUE_Skoru"], name="Su Stresi (WUE)", line=dict(color='firebrick', width=4),
               yaxis="y2"))

fig.update_layout(
    yaxis=dict(title="Aktif İş Yükü (TB)"),
    yaxis2=dict(title="WUE Endeksi", overlaying="y", side="right"),
    template="plotly_white",
    legend=dict(x=0, y=1.1, orientation="h")
)
st.plotly_chart(fig, use_container_width=True)