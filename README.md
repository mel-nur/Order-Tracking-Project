# Çotak Manav - Sipariş Takip Uygulaması

Bu küçük Flask uygulaması, manav siparişlerini şirket bazında takip etmek için hazırlanmıştır.

## İçerik
- `app.py` - Flask uygulaması ve SQLite veritabanı erişimi
- `templates/index.html` - Ana HTML şablonu
- `orders.db` - Uygulama çalıştırıldığında otomatik oluşturulan SQLite veritabanı (aynı dizinde)

## Hızlı Başlangıç (Windows, PowerShell)
Aşağıdaki adımlar proje kökünde (`d:\ManavSiparişTakipProjesi\git`) çalıştırılmalıdır.

1) Sanal ortam oluştur ve etkinleştir

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

2) Gerekli paketleri yükle

```powershell
.\.venv\Scripts\python.exe -m pip install flask
```

3) Uygulamayı çalıştır

```powershell
.\.venv\Scripts\python.exe app.py
```

Varsayılan olarak Flask, `127.0.0.1:5000` üzerinde çalışır. Tarayıcıda şu adresi açın:

http://127.0.0.1:5000

Ctrl+C ile sunucuyu durdurabilirsiniz.

## Önemli Endpointler
- GET `/` - Ana sayfa ve sipariş listesi
- POST `/add` - Tek bir sipariş ekleme (form aracılığıyla)
  - Form alanları: `company`, `product`, `quantity`, `unit`
- POST `/bulk_add` - Toplu sipariş ekleme (her satır: `Ürün Adı miktar birim`)
  - Form alanları: `company`, `bulk_list`
- POST `/delete/<id>` - Belirli siparişi sil
- POST `/reset` - Tüm siparişleri sil (veritabanını temizler)

> Not: Veritabanı dosyası (`orders.db`) aynı dizinde otomatik oluşturulur. Eğer veritabanını sıfırlamak isterseniz `/reset` formunu kullanabilirsiniz.

## Karşılaşabileceğiniz Hatalar / Çözümleri
- `Import "flask" could not be resolved` veya `ModuleNotFoundError: No module named 'flask'`
  - Sanal ortamın aktif olduğundan ve `flask` paketini yüklediğinizden emin olun. Yukarıdaki pip yükleme adımlarını tekrar çalıştırın.

- `OperationalError: unable to open database file`
  - Uygulamayı çalıştırdığınız dizinde yazma izniniz olduğundan emin olun.

- Port çakışması (5000 kullanılıyor)
  - Farklı bir portta çalıştırmak için `app.run(debug=True, port=5001)` gibi `app.py` içinde port numarasını değiştirebilirsiniz.

---
