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
