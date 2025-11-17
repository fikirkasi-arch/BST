# Okul Zil ve Tören Asistanı

Windows 7 ve üzeri bilgisayarlarda çalışacak şekilde tasarlanan Tk tabanlı uygulama ile
haftanın her günü için farklı ders giriş/çıkış saatleri ayarlayabilir, teneffüslerde müzik
çalabilir ve tören sırasında manuel olarak İstiklal Marşı / saygı duruşu akışlarını
başlatabilirsiniz.

## Özellikler
- Her gün için sınırsız sayıda zil olayı ekleme/silme
- Öğrenci girişi, öğretmen girişi, ders sonu ve teneffüs müziği için ayrı ses dosyaları
- İstiklal Marşı, siren ve saygı duruşu kombinasyonları için tek tuşlu manuel tetikleme
- Tören programı için bilgisayardan veya YouTube bağlantısından müzik listesi oluşturma
  - Seçilen müzikleri istenen dakikadan itibaren başlatma
  - Müziğin toplam süresini gösterme
- Teneffüslerde otomatik müzik yayını
- Belirlenen saatte bilgisayarı otomatik kapatma
- Tek tuşla gün programını farklı günlere kopyalama
- Tatil günlerini tanımlayıp belirtilen tarihlerde zilleri otomatik devre dışı bırakma
- Kontrol sekmesinde bugünkü tatil durumu ve sıradaki zil bilgisini görme
- Tören moduna alınca otomatik zilleri geçici olarak kapatma
- Ses seviyesi ayarı ve tek tuşla zili susturma

## Kurulum
```bash
python -m venv .venv
source .venv/bin/activate  # Windows için .venv\Scripts\activate
pip install -r requirements.txt
```

> **Not:** `pydub` kütüphanesi MP3 gibi dosyaları çalabilmek için FFmpeg gerektirir.
Bilgisayarınızda FFmpeg kurulu olduğundan emin olun. YouTube bağlantılarından ses almak
isterseniz `yt-dlp` paketinin kurulması gerekir (requirements dosyasında mevcuttur).

## Çalıştırma
```bash
python main.py
```

Uygulama arka plana alınsa bile (simge durumuna küçültülerek) ziller çalışmaya devam eder.
Manuel butonlar aynı anda zil çalıyor olsa bile öncelik kazanır ve çalarken otomatik zilleri
durdurur.

## Windows için EXE Paketleme
1. Windows 10/11 üzerinde bir komut istemcisi açın ve projeyi içeren klasöre gidin.
2. Gerekli bağımlılıkları yükleyip tek dosyalık çalıştırılabilir oluşturmak için `packaging/build_exe.bat`
   dosyasını çalıştırın:
   ```bat
   packaging\build_exe.bat
   ```
   > İsterseniz komutu `packaging\build_exe.bat C:\Python311\python.exe` şeklinde belirli bir
   > Python yolu vererek de çalıştırabilirsiniz.
3. İşlem sonunda `dist/OkulZilAsistani/OkulZilAsistani.exe` dosyası oluşturulur. Bu klasörü tek
   başına başka bilgisayarlara kopyalayarak da uygulamayı taşıyabilirsiniz.

## Kurulum Dosyası (Setup EXE) Oluşturma
1. Yukarıdaki PyInstaller adımlarını tamamlayarak `dist/OkulZilAsistani` klasörünü üretin.
2. [Inno Setup](https://jrsoftware.org/isinfo.php) kurun ve uygulamayı başlatın.
3. `packaging/installer.iss` dosyasını açın; gerekirse `MyAppVersion` satırını güncelleyin.
4. Inno Setup içinden **Build ➜ Compile** seçeneğini çalıştırın. Oluşan `Output/OkulZilAsistani-Setup.exe`
   dosyası, istediğiniz bilgisayarlara kurulabilir bir sihirbaz sunar.
5. Kurulum dosyasını dağıttığınızda program `C:\Program Files\OkulZilAsistani` klasörüne kurulur ve
   Başlat menüsüne kısayol ekler.

## Geliştirici Bilgisi
Bu uygulama 2026 yılında **Emre Esen** tarafından kodlanmıştır. Program arayüzünün sol alt köşesindeki
imza bölümü de bu bilgiyi gösterir.
