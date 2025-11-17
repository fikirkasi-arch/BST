# JinniBell Pro - Okul Zil ve Tören Asistanı

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
Bilgisayarınızda FFmpeg kurulu olduğundan emin olun. Windows için hazırladığınız EXE/kurulum
paketlerinde FFmpeg ve FFprobe dosyaları otomatik olarak gömüldüğünden, başka bilgisayarlarda
ayrıca kurulmasına gerek kalmaz. YouTube bağlantılarından ses almak isterseniz `yt-dlp`
paketinin kurulması gerekir (requirements dosyasında mevcuttur).

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
   > Betik hata verirse pencere kapanmasın diye otomatik olarak `pause` komutunu uygular. Scripti
   > otomatik süreçlerde kullanmak isterseniz `set NOPAUSE=1` deyip ardından çalıştırabilirsiniz.
3. Betik, `requirements.txt` içindeki bütün paketleri indirir ve eksikse Python ile çalışan
   `packaging/get_ffmpeg.py` yardımcı programını kullanarak FFmpeg/FFprobe ikililerini indirip
   `packaging\ffmpeg-bin` klasörüne çıkarır. Böylece PowerShell erişimi kısıtlı sistemlerde bile
   indirme işlemi sorunsuz yürür.
   - Bilgisayar internete çıkamıyorsa betik sırasıyla `ffmpeg-7.0.1-essentials_build.zip`,
     `ffmpeg-7.0-essentials_build.zip`, `ffmpeg-release-essentials.zip` ve
     `ffmpeg-master-latest-win64-gpl.zip` paketlerini deneyecek; bu dosyalardan herhangi birini
     [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) ya da
     [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases) sayfasından indirip
     `packaging` klasörüne `ffmpeg-offline.zip` (veya `FFMPEG_ZIP_PATH` ile gösterdiğiniz herhangi
     bir isim) olarak kopyalarsanız indirme adımı atlanır.
4. Betik tüm komutların çıktısını `packaging\build_exe.log` dosyasına yazar. Konsolda hata
   mesajı görürseniz ayrıntılı sebebi bu logda bulabilirsiniz.
5. PyInstaller çağrısı, program kodu ile birlikte bu FFmpeg dosyalarını da `dist/JinniBellPro/ffmpeg`
   klasörüne gömerek tek başına çalışabilen bir çıktı üretir; hedef bilgisayarda ek DLL veya modül
   kurmanıza gerek kalmaz.
6. İşlem sonunda `dist/JinniBellPro/JinniBellPro.exe` dosyası oluşturulur. Bu klasörü tek
   başına başka bilgisayarlara kopyalayarak da uygulamayı taşıyabilirsiniz.

## Kurulum Dosyası (Setup EXE) Oluşturma
1. Yukarıdaki PyInstaller adımlarını tamamlayarak `dist/JinniBellPro` klasörünü üretin.
2. [Inno Setup](https://jrsoftware.org/isinfo.php) kurun ve uygulamayı başlatın.
3. `packaging/installer.iss` dosyasını açın; gerekirse `MyAppVersion` satırını güncelleyin.
4. Inno Setup içinden **Build ➜ Compile** seçeneğini çalıştırın. Oluşan `Output/JinniBellPro-Setup.exe`
   dosyası, istediğiniz bilgisayarlara kurulabilir bir sihirbaz sunar.
5. Kurulum dosyası, PyInstaller'ın çıkardığı tüm paketleri, `bell_app` klasörünü ve
   `dist/JinniBellPro/ffmpeg` altındaki FFmpeg/FFprobe dosyalarını otomatik olarak
   içerdiğinden ek bağımlılık kurulumu istemez.
6. Kurulum dosyasını dağıttığınızda program `C:\Program Files\JinniBellPro` klasörüne kurulur ve
   Başlat menüsüne kısayol ekler.

## Programlama bilmeyenler için adım adım paketleme
Kurulum scriptlerini hiç kod yazmadan kullanmak için ayrıntılı yönergeler `packaging/STEP_BY_STEP.md`
dosyasında anlatılmıştır. Tüm bağımlılıkların EXE içerisine gömülü geldiğini doğrulamak ve farklı
bilgisayarlara kurulabilir bir setup üretmek için bu rehberdeki ekran görüntülü (metin içi) adımları
izleyebilirsiniz.

## Geliştirici Bilgisi
Bu uygulama 2026 yılında **Emre Esen** tarafından kodlanmıştır. Program arayüzünün sol alt köşesindeki
imza bölümü de bu bilgiyi gösterir.
