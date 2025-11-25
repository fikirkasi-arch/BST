# JinniBell Pro için Kullanışlılık Önerileri

Aşağıdaki fikirler, okul yönetimlerinin JinniBell Pro'yu daha hızlı ve hatasız kullanmasına yardımcı olacak şekilde planlandı. Her madde, son kullanıcı tarafında gözlenen sık hataları azaltmaya veya günlük akışı hızlandırmaya odaklanır.

## 1. Takvim Tabanlı Program Görünümü
> **Durum:** JinniBell Pro arayüzüne aylık takvim paneli eklendi; seçilen günün tablo hâlindeki
> dersleri sağda açılıyor ve çoklu gün kopyalama diyalogları ile pekiştirildi.
- Haftalık tabloya ek olarak aylık takvim görünümü ekleyip her günün zil sayısını renk kodlarıyla göstermek, yoğun günleri çabucak fark etmeyi sağlar.
- Takvimdeki herhangi bir güne tıklayınca ilgili kayıtlar sağ panelde açılarak tek ekranda düzenleme yapılabilir.

## 2. İlk Kurulum Sihirbazı
- Programı ilk açan kullanıcıya okul tipi (tam gün / ikili eğitim), ders süresi ve toplam ders sayısı gibi soruları soran kısa bir sihirbaz ile başlangıç planı otomatik oluşturulabilir.
- Sihirbaz sonunda "Öğretmen / Öğrenci girişi" seslerini seçme adımı sunulursa kullanıcılar daha sonra ayarlara gitmek zorunda kalmaz.

## 3. Akıllı Kopyalama Şablonları
- "Bir günü diğer günlere aktar" özelliğine ek olarak yarım gün, sınav günü, tören günü gibi hazır şablonlar sunulabilir.
- Şablonlara özel renkli etiketler tanımlanırsa tatil veya sınav programları listede daha rahat ayırt edilir.

## 4. Zaman Girişi İçin Klavye Kısayolları
- Saat spinbox'larında `Ctrl+Yukarı/Aşağı` ile 5 dakikalık adımlar, `Ctrl+Enter` ile bir sonraki satıra geçiş gibi kısayollar sağlanabilir.
- Yanlış girişleri anında vurgulamak için alan kenarlıkları kırmızıya döner; kullanıcı düzeltmeden kayda izin verilmez.

## 5. Ses Kütüphanesi ve Etiketler
> **Durum:** Ses kütüphanesi + etiket sistemi eklendi; dosya seçildiği anda JinniBell klasörüne
> kopyalanıp kitaplığa düşüyor, her satırda "Kitaplıktan ata" menüsü hazır.
- Sık kullanılan ses dosyaları için dahili bir kütüphane ekranı ekleyip etiketleme ("v.1 teneffüs", "uzun siren" gibi) yapılabilir.
- Aynı dosya farklı derslere atanırken sadece etiketi seçmek, her defasında dosya gezgini açma ihtiyacını ortadan kaldırır.

## 6. Tören Çalma Listesi İçin Durum Takibi
> **Durum:** Playlist satırlarına hazır/bekliyor/indiriliyor rozetleri ve hata mesajları eklendi;
> YouTube indirmeleri tamamlandığında satır otomatik güncelleniyor.
- Playlist satırlarına "indirilmiş / bekliyor" gibi durum ikonları eklenerek YouTube bağlantısının hazır olup olmadığı gösterilebilir.
- Her parça için tahmini indirme süresi veya boyutu görüntülenirse büyük dosyalarda kullanıcı bekleme süresini bilir.

## 7. Uzaktan Yönetim ve Bulut Yedekleri
- Program ayarlarını bir JSON dosyasına yedekleyip OneDrive/Google Drive gibi klasörlere otomatik olarak yükleyen arka plan görevi eklenebilir.
- Aynı okulda birden fazla bilgisayar varsa, dosya değiştiğinde diğer istemciye otomatik senkronizasyon yapacak bir izleme mekanizması kurulabilir.

## 8. Zil Testi İçin Simülasyon Modu
> **Durum:** Simülasyon paneli ders programı sekmesine eklendi, günün tamamını hızlandırılmış
> olarak oynatıp olası çakışmaları raporluyor.
- Okul dışı saatlerde programın tüm günü hızlandırılmış şekilde simüle etmesini sağlayan "senaryo" moduyla kullanıcılar planlarını sınayabilir.
- Simülasyon raporu, hangi zilin kaçıncı dakikada çaldığını ve çakışma olup olmadığını göstererek veri girişi hatalarını azaltır.

## 9. Tören Esnasında Sürükle-Bırak Sıralama
> **Durum:** Tören playlisti artık doğrudan sürükle-bırak yöntemiyle sıralanabiliyor; ayrıca
> satır başındaki ok tuşlarıyla da sıralamayı değiştirmek mümkün.
- Playlist öğelerini sürükle-bırak yöntemiyle sıralamak, özellikle dokunmatik ekranlı cihazlarda kullanım kolaylığı sağlar.
- Sürükleme sırasında hedef pozisyonu gösteren görsel bir çizgi ile kullanıcı hata yapmadan sıralamayı tamamlar.

## 10. Bildirim ve Geri Sayım Paneli
> **Durum:** Kontrol sekmesinde canlı geri sayım + tören modu rozeti devrede ve Windows masaüstü
> bildirimleriyle manuel/otomatik tetiklemeler raporlanıyor.
- Kontrol sekmesine "Sonraki zil 03:12 sonra" gibi büyük puntolu bir geri sayım göstergesi eklenebilir.
- Tören modu aktifken ekranın üst kısmında kırmızı bir şerit veya simge gösterilirse öğretmenler otomatik zillerin durdurulduğunu kolayca anlar.

Bu öneriler modüler olarak hayata geçirilebilir; öncelikle veri girişini kolaylaştıran kısayollar ve şablonlar kısa sürede uygulanabilirken, bulut senkronizasyonu gibi özellikler için ek servis planlaması yapılmalıdır.

## 11. Modern ve Dokunmatik Uyumlu UI
- Ana pencerede 14–16 px boşluklu kartlar ve yuvarlatılmış köşeler (8 px) kullanmak, kalabalık hisseyi azaltır; sütun araları 12–16 px tutulursa hem masaüstü hem dokunmatik tıklamalar rahatlar.
- Tablo başlıkları ve satırlar için açık gri arka plan + ince ayırıcı çizgiler (`#e6e6e6`) kullanıp satır hover rengini hafif mavi yaparak seçili satırı öne çıkarabilirsiniz.
- Büyük butonları 36–40 px yüksekliğe küçültüp ikon + kısa etiket (örn. `▶︎ Çal`, `⏸ Duraklat`) kombinasyonuna geçmek göz karmaşasını azaltır.
- Zil saatlerini seçmek için spinbox yerine saat/dakika segmentli butonlar (örn. 05 dakikalık artış butonları) veya dokunmatik dostu saat seçici diyaloğu eklemek giriş hızını yükseltir.

## 12. Karanlık Tema ve Kontrast Ayarı
- Açık/karanlık tema anahtarını ayarlar menüsüne ekleyip Mica/Acrylic benzeri yarı saydam şeritler yerine sade düz renkler kullanmak göz yorgunluğunu azaltır.
- WCAG uyumlu kontrastı tutturmak için metin/zemin renklerini `#1f1f1f` / `#f9f9f9` veya `#0f172a` / `#e2e8f0` gibi çiftlerle sınırlandırın; vurgu rengi tek bir palette (`#2563eb` veya `#22c55e`) kalmalı.

## 13. Form Doğrulama ve Hata İpuçları
- Zil saatleri, dosya yolları ve URL alanlarına anlık doğrulama ekleyerek hatalı girişte kırmızı kenarlık ve küçük ipucu balonu gösterin; kayıt butonunu bu alanlar düzeltilene kadar pasif tutun.
- Ses dosyası seçicisine desteklenmeyen formatlarda uyarı ve "örnek dinle" butonu ekleyip ffplay/ffmpeg bulunamadığında tek tıklamalı yeniden indirme bağlantısı sunabilirsiniz.

## 14. Özelleştirilebilir Kısayol Şeridi
- Kontrol sekmesinin üstüne sık kullanılan eylemler ("Sonraki dersi çal", "Töreni başlat", "Tüm zilleri sustur") için küçük ikonlu bir kısayol şeridi eklemek, kullanıcıların karmaşık menülere girmeden işlem yapmasını sağlar.
- Bu şerit, ayarlar sayfasında sürükle-bırak ile kişiselleştirilebilir olursa farklı okullar kendi akışlarına uyarlayabilir.

## 15. Veri Yoğun Ekranlar İçin Filtreler
- Ders programı tablosuna gün/sınıf filtresi ve metin arama çubuğu ekleyip tabloyu dinamik olarak daraltmak, özellikle çok dersli okullarda kaydırma ihtiyacını azaltır.
- Playlist ve kütüphane listelerinde "sadece favoriler", "indirilmiş" gibi hazır filtre butonları sunarak aranan öğeye ulaşma süresini kısaltabilirsiniz.

## 16. Uzamsal Ses ve Etki Alanları
- Kampüste birden fazla hoparlör hattı varsa "alan" tanımları ekleyip her zil için çıkış hattı seçimi yapılabilir; böylece okulun farklı bloklarında farklı melodiler çalınabilir.
- Çok kanallı hoparlörler için sağ/sol denge ve ses şiddeti önizlemesi sunmak, özellikle törenlerde sahne/seyirci odaklı ses dağıtımını kolaylaştırır.

## 17. Akıllı Program Önerileri (Yapay Zeka Destekli)
- Geçmiş ders programlarını analiz edip tatil, yarım gün veya sınav haftası gibi kalıpları tanıyan bir öneri modu, yeni dönem planını otomatik doldurabilir.
- Çakışma tespitine ek olarak "en az teneffüs kesintisi" veya "blok ders önceliği" gibi optimizasyon hedefleri seçilerek AI destekli zamanlama önerisi sunulabilir.

## 18. Dokunmatik ve Kiosk Modu
- Tam ekran kiosk modu, dokunmatik panellerde büyük butonlu minimal bir kontrol paneliyle temel eylemleri (çal / sustur / tören başlat) tek dokunuşa indirger.
- Kiosk moduna geçildiğinde masaüstü bildirimleri ve uyarı sesleri sadeleştirilebilir; bu, fuar veya duyuru ekranlarında görsel karmaşayı azaltır.

## 19. Erişilebilirlik ve Renk Körlüğü Dostu Tema
- WCAG 2.1 AA kontrastını sağlayan yüksek kontrastlı temaya tek tıkla geçiş ve odak halkalarını belirginleştirmek, görme güçlüğü yaşayan kullanıcılar için kritik.
- Erişilebilirlik modunda ikonlara metin eşlikleri ve klavye odak sırası otomatik gösterilirse screen reader uyumluluğu artar.

## 20. Canlı Analitik ve Aksiyon Kartları
- Panelde "Bugün planlanan zil sayısı", "Manuel çalma sayısı", "Kaçırılan çalma" gibi metrikleri gerçek zamanlı gösteren küçük kartlar eklenebilir.
- Hatalı veya atlanan zil tespit edildiğinde aksiyon kartı üzerinde tek tıkla yeniden çalma veya düzeltme formuna bağlantı sunmak kullanıcıyı yönlendirir.

## 21. QR ve NFC ile Hızlı Komutlar
- Görevliler için "Zili şimdi çal", "Törene geç", "Sustur" gibi komutlara özel QR kodları üretilip panolara asılabilir; mobil cihazla okutulduğunda web tabanlı kısa komut gönderilebilir.
- NFC etiketlerine aynı komutlar yazılarak sahada internet erişimi sınırlı olduğunda bile tek dokunuşla tetikleme yapılabilir.

## 22. YouTube ve Yerel Müzik İçin Sahne Modu
- Tören çalma listesine "Sahne Modu" görünümü eklenip YouTube ve yerel parçalar tek ekranda büyük kapak görselleri ve durum rozetleriyle sunulabilir; dokunmatik sürükle-bırak ile sıralama yapılır.
- YouTube bağlantıları için otomatik kalite/dil filtresi ve çevrimdışı önbellek durumu gösterilerek "hazır / indiriliyor / hata" gibi durumlar tek bakışta anlaşılır.
- Playlist satırlarında çift zamanlama alanı (başlangıç ve vurgu anı) tutularak marş ve konuşmaların belirli kısımlarına hızlı atlama yapılabilir.

## 23. Minimalist ve Satılabilir Arayüz Paketi
- Tema sistemine "Minimal" preset'i eklenerek 12–16 px boşluk, ince ikonlar ve tek renk vurgu paleti (örn. `#2563eb`) ile sade bir görünüm sunulabilir; başlık çubuklarına cam efekti yerine düz şeritler tercih edilir.
- Dokunmatik uyum için tablo satır yüksekliği 36–40 px, buton yükseklikleri 36 px olarak standardize edilir; kart gövdelerinde 8 px köşe yumuşatması kullanılır.
- Kılavuzlu yerleşim (grid) ile ders ve tören kartları aynı genişlikte hizalanır; kritik aksiyonlar (Çal, Sustur, Tören) üstte ikonlu kısayol şeridiyle sabitlenir.

## 24. Zil ve Müzik Kuyruğu Akışları
- Kontrol sekmesine "Şimdi Çal / Sıradaki" kartı eklenerek hem ders zili hem tören müziği aynı zaman çizelgesinde gösterilebilir; sayaç bittiğinde bir sonraki maddeye otomatik geçiş animasyonu yapılır.
- Kuyrukta yer alan her öğe için ses seviyesi, çıkış bölgesi ve çapraz solma süresi tek satırdan düzenlenir; kulaklık simgesi ile anlık ön dinleme yapılabilir.
- Tüm kuyruğu dışa aktarma (JSON/CSV) ve içe alma butonları eklenerek sahne listelerinin paylaşımı kolaylaştırılır.

## 25. Akıllı Form Doğrulama ve Yardım Balonları
- Saat, URL ve dosya yolu alanlarında anlık doğrulama yapılıp hatalı alanlar kırmızı kenarlık ve mikro ipucu balonuyla belirtilir; form kaydı tüm alanlar geçerli olana kadar pasif tutulur.
- YouTube bağlantıları çözümlenirken geçersiz veya yaş kısıtlamalı içerik tespit edilirse önceden uyarı verilir; alternatif indirme önerisi sunulur.
- Kullanıcı ilk kez bir alanı doldururken kısa rehber balonları ("Ses dosyasını .mp3 olarak ekleyin", "Saat formatı 08:30") gösterilerek onboarding hızlandırılır.

## 26. Zil Bölgesi ve Mekânsal Ses Sahneleyici
- Uzamsal ses bölgeleri bir kat planı veya basit blok diyagramı üzerinde gösterilip sürükle-bırak ile hoparlör hattına bağlanabilir; kullanıcı hangi blokta hangi melodinin çaldığını canlı görür.
- Bölge başına gecikme/sönümleme ayarı eklenerek törenlerde sahne-izleyici senaryoları için mekânsal denge sağlanır; test için "sağ/sol dolaşım" önizlemesi sunulur.
- Bölge eşleşmeleri, ders tablosu ve tören listesiyle ilişkilendirilerek "Bu ders sadece Blok B'de çal" gibi kurallar tek tıklamayla uygulanır.

## 27. Günlük Kullanım İçin Mikro İyileştirmeler
- Çalma listesi ve ders tablolarında satır hover vurgusu ve yumuşak geçiş animasyonları eklenerek yoğun ekranlarda göz takibi kolaylaştırılır.
- Geri sayım ve durum rozetlerinde hafif gradient veya cam efekti yerine düz renk mikro dokular kullanılabilir; böylece modern ama dikkat dağıtmayan bir görünüm elde edilir.
- Sık kullanılan ayarlar (ses seviyesi, karanlık tema, dokunmatik modu) başlık çubuğunun sağında hızlı anahtarlar olarak sabitlenerek erişim süresi kısaltılır.
