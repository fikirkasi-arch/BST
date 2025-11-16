# Dinamik Bulmaca Atölyesi

Bu depo, öğretmen ve öğrencilerin birkaç satırlık metinle erişilebilir bulmacalar hazırlayıp PDF çıktısı almasını sağlayan web uygulamasını içerir. Arayüz; klavye dostu kontroller, yüksek kontrastlı tema ve her mod için oynanabilir bileşenlerle güncellenmiştir.

## Özellikler

1. **Erişilebilirlik odaklı tasarım**  
   - WCAG uyumlu renk paleti ve belirgin `:focus-visible` durumları  
   - Form etiketleri, durum mesajlarında `aria-live` ve gridler için anlamlı rol/etiketler
2. **Modüler mimari**  
   - `src/puzzles/` altında her bulmaca türü için bağımsız oluşturucu  
   - `state.js` ile merkezi durum yönetimi ve yerel depolama desteği  
   - Paylaşılan yardımcılar (`utils/`, `ui/`) sayesinde test edilebilir fonksiyonlar
3. **Yeni bulmaca türleri**  
   - Akrostiş / Kripto Akrani  
   - Şifreli Alfabe (Cryptogram)  
   - Söz Zinciri / Kelime Merdiveni  
   - Güncellenmiş Kare Bulmaca (interaktif grid, otomatik yön değişimi)
4. **PDF çıktısı**  
   - Her modda tek tıkla yazdırma/PDF aktarımı  
   - Boş/çözümlü görseller veya HTML bölümleri yazdırma alanında hazırlanır
5. **Oynanabilirlik geliştirmeleri**  
   - DOM tabanlı hücreler, yön tuşları ve otomatik ilerleme  
   - Yerel depolamada ilerleme saklama ve temizleme butonu  
   - İpucu listeleri ve yardım paneli ile kullanıcı rehberliği

## Kurulum

```bash
npm install # bağımlılık yoksa atlanabilir
```

Uygulama düz HTML/JS olduğu için herhangi bir sunucuya gerek yoktur; statik dosyaları hizmete almak yeterlidir. Örneğin:

```bash
npx serve .
```

## Geliştirme

- Yeni puzzle modları `src/puzzles/` içine eklenir ve `src/main.js` içinde kayıt edilir.  
- PDF çıktısı için `renderPrintable` fonksiyonuna ilgili HTML/kanvas görsellerini sağlayın.  
- Erişilebilirlik için yeni bileşenler eklerken `aria` etiketlerini unutmayın.

## Test

Tarayıcıda `index.html` dosyasını açın, örnek veriyi yükleyip tüm modlarda çıktı alın. Ekstra otomasyon gerekmiyorsa manuel kontrol yeterlidir.
