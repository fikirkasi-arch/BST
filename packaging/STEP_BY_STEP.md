# Kod yazmadan EXE ve Kurulum Dosyası Hazırlama Rehberi

Aşağıdaki adımlar, programlama bilmeyen kullanıcıların bile bütün bağımlılıkları EXE içerisine
paketleyip kurulabilir bir `Setup.exe` dosyası çıkarmasını sağlar.

## 1. Hazırlık
1. [python.org](https://www.python.org/downloads/windows/) adresinden **Python 3.11 (64-bit)** sürümünü indirin.
2. Kurulum penceresinde **"Add python.exe to PATH"** kutucuğunu işaretleyip **Install Now** seçin.
3. [GitHub projesinin ZIP arşivini](https://github.com/) indirin veya size verilen proje klasörünü bir
   klasöre çıkarın. Örnek klasör adı `C:\OkulZilAsistani` olabilir.

## 2. Tüm paketleri EXE içine gömmek
1. Başlat menüsünden **"Command Prompt"** (veya "Komut İstemi") uygulamasını açın.
2. Komutta aşağıdaki satırı yazıp Enter'a basın. Bu satır sizi proje klasörüne götürür:
   ```bat
   cd /d C:\OkulZilAsistani
   ```
3. Ardından şu komutu yazın:
   ```bat
   packaging\build_exe.bat
   ```
4. Betik otomatik olarak
   - `pip`i günceller,
   - `requirements.txt` içindeki **mutagen, pydub, simpleaudio, yt_dlp** gibi tüm paketleri indirir,
   - Eksikse güncel **FFmpeg** ve **FFprobe** dosyalarını download edip `packaging\ffmpeg-bin`
     klasörüne çıkarır,
   - PyInstaller'ı çağırarak program dosyalarını, bağımlılıkları ve `ffmpeg` klasörünü
     `dist/OkulZilAsistani` klasörünün içine kopyalar.
5. Komut isteminde `BUILDING EXE` benzeri satırlar bittikten sonra `dist/OkulZilAsistani/OkulZilAsistani.exe`
   dosyası oluşur. Klasörde ayrıca `ffmpeg` isimli bir alt klasör göreceksiniz; burada gömülü gelen
   `ffmpeg.exe` ve `ffprobe.exe` dosyaları bulunur. Bu klasörü tek başına USB belleğe atıp başka
   bilgisayarda çalıştırabilirsiniz.

## 3. Kurulum sihirbazı (Setup.exe) üretmek
1. [Inno Setup](https://jrsoftware.org/isdl.php) programını indirin ve varsayılan ayarlarla kurun.
2. Inno Setup'ı açıp **File ➜ Open** menüsünden proje klasöründeki `packaging/installer.iss` dosyasını seçin.
3. Üst kısımdaki `#define MyAppVersion "1.0"` satırını gerekirse güncelleyin.
4. Menüden **Build ➜ Compile** seçeneğine tıklayın. Derleme bittikten sonra `packaging\Output` klasöründe
   `OkulZilAsistani-Setup.exe` oluşur.
5. Bu kurulum dosyası, PyInstaller klasörünün içindeki bütün bağımlılıkları ve ses dosyalarını otomatik olarak
   içerir; hedef bilgisayarda Python veya ek paket kurmanıza gerek kalmaz.

## 4. Son kontrol
- Kurulum dosyasını test amaçlı başka bir klasöre kurun. Kurulum sihirbazı varsayılan olarak
  `C:\Program Files\OkulZilAsistani` dizinini kullanır ve Başlat menüsüne kısayol ekler.
- Masaüstündeki veya Başlat menüsündeki kısayola çift tıklayıp programı çalıştırarak her şeyin doğru
  paketlendiğini doğrulayın.

Bu adımları izlediğinizde, programlama bilmeden bile tüm paketleri içinde barındıran taşınabilir bir
EXE ve kurulabilir bir Setup dosyası elde etmiş olursunuz.
