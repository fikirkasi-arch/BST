#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
import re

# PowerPoint oluştur
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

def add_title_slide(title, subtitle):
    """Başlık slaytı ekle"""
    slide_layout = prs.slide_layouts[0]  # Title Slide
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.title
    subtitle_shape = slide.placeholders[1]

    title_shape.text = title
    subtitle_shape.text = subtitle

    # Başlık formatı
    title_shape.text_frame.paragraphs[0].font.size = Pt(54)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(67, 142, 234)

    # Alt başlık formatı
    subtitle_shape.text_frame.paragraphs[0].font.size = Pt(32)
    subtitle_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)

    # Arka plan rengi
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 250, 255)

    return slide

def add_section_slide(title, color_rgb=(67, 142, 234)):
    """Bölüm başlığı slaytı ekle"""
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)

    # Arka plan gradient benzeri
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*color_rgb)

    # Büyük başlık ekle
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(2))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(60)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    return slide

def add_content_slide(title, content_items, bullet_level=0):
    """İçerik slaytı ekle"""
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.title
    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(40)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(67, 142, 234)

    # İçerik ekle
    body_shape = slide.placeholders[1]
    tf = body_shape.text_frame
    tf.clear()

    for item in content_items:
        p = tf.add_paragraph()
        # Emoji ve markdown işaretlerini temizle
        clean_item = re.sub(r'\*\*(.*?)\*\*', r'\1', item)  # **bold** -> bold
        p.text = clean_item
        p.level = bullet_level
        p.font.size = Pt(24)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.space_before = Pt(6)

    # Arka plan
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    return slide

def add_table_slide(title, table_data):
    """Tablo slaytı ekle"""
    slide_layout = prs.slide_layouts[5]  # Title Only
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.title
    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(40)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(67, 142, 234)

    # Tablo ekle
    rows = len(table_data)
    cols = len(table_data[0]) if rows > 0 else 0

    left = Inches(1.5)
    top = Inches(2)
    width = Inches(7)
    height = Inches(4)

    table = slide.shapes.add_table(rows, cols, left, top, width, height).table

    # Tablo verilerini doldur
    for i, row_data in enumerate(table_data):
        for j, cell_data in enumerate(row_data):
            cell = table.rows[i].cells[j]
            cell.text = cell_data
            cell.text_frame.paragraphs[0].font.size = Pt(18)

            # Başlık satırı
            if i == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(67, 142, 234)
                cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
                cell.text_frame.paragraphs[0].font.bold = True

    return slide

# ANA SUNUM OLUŞTUR

# Kapak slaytı
add_title_slide(
    "5. SINIF BİLİŞİM TEKNOLOJİLERİ",
    "Tam Yıl Sunumu (38 Hafta)\n2025-2026 Eğitim Yılı"
)

# Hoş Geldiniz
add_content_slide(
    "🎯 Hoş Geldiniz!",
    [
        "5. Sınıf Bilişim Teknolojileri Dersine Hoş Geldiniz!",
        "",
        "Bu yıl neler öğreneceğiz?",
        "💻 Bilgisayar nasıl çalışır?",
        "🎨 Dijital ürünler nasıl yapılır?",
        "🤖 Yapay zeka nedir?",
        "💻 Scratch ile oyun yapımı!"
    ]
)

# ÜNİTE 1: Bilişim Temelleri
add_section_slide("📚 ÜNİTE 1: Bilişim Temelleri", (220, 100, 180))

add_content_slide(
    "Hafta 1: Bilgisayar ve Bileşenleri",
    [
        "💻 Bilgisayar Nedir?",
        "Veri işleyen elektronik cihaz",
        "Giriş → İşlem → Çıkış",
        "",
        "Donanım Bileşenleri:",
        "Kasa: Ana gövde",
        "Ekran: Görüntü",
        "Klavye: Yazı yazma",
        "Mouse: İmleç kontrolü"
    ]
)

add_content_slide(
    "Donanım Detayları",
    [
        "İçeridekiler:",
        "🧠 İşlemci (CPU): Bilgisayarın beyni",
        "💾 RAM: Hızlı bellek",
        "💿 Harddisk/SSD: Kalıcı depolama",
        "🎮 Ekran Kartı: Görüntü işleme"
    ]
)

add_content_slide(
    "Hafta 2: Yazılım ve İşletim Sistemleri",
    [
        "💿 Yazılım Nedir?",
        "Bilgisayara ne yapacağını söyleyen programlar",
        "",
        "Yazılım Türleri:",
        "1. Sistem Yazılımları: Windows, macOS, Linux",
        "2. Uygulama Yazılımları: Word, Chrome, Oyunlar"
    ]
)

add_content_slide(
    "İşletim Sistemleri",
    [
        "Windows:",
        "En yaygın işletim sistemi",
        "Kullanıcı dostu",
        "Oyunlar ve programlar çok",
        "",
        "Linux:",
        "Açık kaynak",
        "Güvenli",
        "Ücretsiz"
    ]
)

add_content_slide(
    "Hafta 3: Dosya Yönetimi",
    [
        "📁 Dosya ve Klasör",
        "Dosya: Bilgi saklayan birim (resim, belge, video)",
        "Klasör: Dosyaları düzenler",
        "",
        "İsimlendirme Kuralları:",
        "✅ Anlamlı isim ver",
        "❌ Özel karakter kullanma (?, *, /)",
        "✅ Tarih ekle (2025-01-15_odev)"
    ]
)

# ÜNİTE 2: Dijital Ürün Tasarımı
add_section_slide("📚 ÜNİTE 2: Dijital Ürün Tasarımı", (100, 180, 220))

add_content_slide(
    "Hafta 10: Microsoft Word",
    [
        "📝 Word Nedir?",
        "Kelime işlemci",
        "Belge oluşturma",
        "",
        "Temel İşlemler:",
        "Yazı yazma",
        "Biçimlendirme (kalın, italik, renk)",
        "Resim ekleme",
        "Tablo oluşturma"
    ]
)

add_content_slide(
    "Word İpuçları",
    [
        "Kısayollar:",
        "Ctrl + C → Kopyala",
        "Ctrl + V → Yapıştır",
        "Ctrl + Z → Geri al",
        "Ctrl + S → Kaydet"
    ]
)

add_content_slide(
    "Hafta 11: Paint",
    [
        "🎨 Paint ile Çizim",
        "Basit çizim programı",
        "Ücretsiz ve kolay",
        "",
        "Araçlar:",
        "Fırça",
        "Kalem",
        "Şekiller (daire, kare...)",
        "Metin"
    ]
)

add_content_slide(
    "Hafta 12-14: PowerPoint",
    [
        "🎬 Sunum Hazırlama",
        "",
        "PowerPoint nedir?",
        "Sunum programı",
        "Slaytlar oluşturma",
        "",
        "Slayt Öğeleri:",
        "Başlık, Metin, Resim, Video"
    ]
)

add_content_slide(
    "İyi Sunum Özellikleri",
    [
        "✅ Sade ve öz",
        "✅ Görsellerle desteklenmiş",
        "✅ Büyük font (en az 24 punto)",
        "❌ Çok yazı yok",
        "❌ Karışık renkler yok"
    ]
)

# ÜNİTE 3: Ağlar ve İletişim
add_section_slide("📚 ÜNİTE 3: Ağlar ve İletişim", (180, 220, 100))

add_content_slide(
    "Hafta 16: İnternet ve Ağlar",
    [
        "🌐 İnternet Nedir?",
        "Dünya çapında bilgisayar ağı",
        "Bilgi paylaşımı",
        "",
        "Nasıl Bağlanırız?",
        "Wi-Fi",
        "Kablo (Ethernet)",
        "Mobil veri"
    ]
)

add_content_slide(
    "İnternet Tarayıcıları",
    [
        "Tarayıcı Nedir?",
        "Web sitelerine erişim programı",
        "",
        "Örnekler:",
        "Google Chrome",
        "Mozilla Firefox",
        "Microsoft Edge",
        "Safari"
    ]
)

add_content_slide(
    "Hafta 17: E-posta",
    [
        "📧 E-posta Nedir?",
        "Elektronik mektup",
        "Hızlı iletişim",
        "",
        "E-posta Bileşenleri:",
        "Kime: Alıcı",
        "Konu: Başlık",
        "Gövde: Mesaj",
        "Ek: Dosya"
    ]
)

# ÜNİTE 4: Etik ve Güvenlik
add_section_slide("📚 ÜNİTE 4: Etik ve Güvenlik", (220, 50, 50))

add_content_slide(
    "Hafta 19: Bilişim Etiği",
    [
        "🤝 Dijital Etik Kuralları:",
        "1. Saygılı ol",
        "2. Kişisel bilgi paylaşma",
        "3. Telif hakkına saygı göster",
        "4. Spam yapma",
        "5. Zorbalık yapma"
    ]
)

add_content_slide(
    "Hafta 20: Siber Güvenlik",
    [
        "🔒 Güçlü Şifre",
        "",
        "Olması gerekenler:",
        "En az 8 karakter",
        "Büyük harf (A-Z)",
        "Küçük harf (a-z)",
        "Rakam (0-9)",
        "Sembol (!@#$)",
        "",
        "Olmaması gerekenler:",
        "❌ 123456",
        "❌ password",
        "❌ Adınız"
    ]
)

# ÜNİTE 5: Yapay Zeka
add_section_slide("📚 ÜNİTE 5: Yapay Zeka", (50, 150, 220))

add_content_slide(
    "Hafta 21: Yapay Zeka Nedir?",
    [
        "🤖 YZ Tanımı",
        "Makinelerin insan gibi düşünmesi",
        "Öğrenme ve karar verme",
        "",
        "Örnekler:",
        "Siri / Alexa",
        "Google Translate",
        "Netflix önerileri",
        "Yüz tanıma"
    ]
)

add_table_slide(
    "İnsan vs Yapay Zeka",
    [
        ["İnsan Zekası", "Yapay Zeka"],
        ["Duygular var", "Duygusuz"],
        ["Yaratıcı", "Öğrenileni yapar"],
        ["Yorulur", "Yorulmaz"],
        ["Esnek", "Kurallara bağlı"]
    ]
)

add_content_slide(
    "Hafta 22: YZ Uygulamaları",
    [
        "Günlük Hayatta YZ:",
        "🎵 Müzik önerileri (Spotify)",
        "🎬 Film önerileri (Netflix)",
        "🗺️ Navigasyon (Google Maps)",
        "📸 Fotoğraf düzenleme",
        "🎮 Oyun AI"
    ]
)

# ÜNİTE 6: Scratch Programlama
add_section_slide("📚 ÜNİTE 6: Scratch Programlama", (220, 150, 50))

add_content_slide(
    "Hafta 25: Algoritma ve Programlama",
    [
        "🧩 Algoritma Nedir?",
        "Adım adım talimatlar",
        "Problem çözme yöntemi",
        "",
        "Örnek: Çay Yapma",
        "1. Çaydanlığı al",
        "2. Su doldur",
        "3. Yak",
        "4. Kayna",
        "5. Çay koy",
        "6. İç"
    ]
)

add_content_slide(
    "Hafta 26: Scratch ile Tanışma",
    [
        "💻 Scratch Nedir?",
        "Görsel programlama dili",
        "MIT tarafından geliştirildi",
        "Ücretsiz!",
        "",
        "Web: scratch.mit.edu"
    ]
)

add_content_slide(
    "Scratch Arayüzü",
    [
        "Bileşenler:",
        "1. Sahne: Karakterlerin oynadığı yer",
        "2. Sprite: Karakterler",
        "3. Bloklar: Komutlar",
        "4. Kod Alanı: Blokları birleştir"
    ]
)

add_content_slide(
    "Hafta 27: Hareket Blokları",
    [
        "🏃 Hareket",
        "[10 adım git] → İlerle",
        "[15 derece dön] → Dön",
        "[x:0 y:0 git] → Konuma git",
        "",
        "Koordinatlar:",
        "x: Sağ-Sol (-240 ile +240)",
        "y: Yukarı-Aşağı (-180 ile +180)"
    ]
)

add_content_slide(
    "Hafta 28: Ses ve Olaylar",
    [
        "🔊 Ses Blokları:",
        "[pop sesi çal]",
        "[müzik başlat]",
        "",
        "⚡ Olay Blokları:",
        "(Yeşil bayrak tıklandığında)",
        "(boşluk tuşuna basıldığında)",
        "(Bu sprite tıklandığında)"
    ]
)

add_content_slide(
    "Hafta 29: Döngüler",
    [
        "🔁 Döngü Nedir?",
        "Tekrar tekrar yapma",
        "",
        "İki Tür:",
        "1. Sonsuza kadar: Hiç durma",
        "2. N kez tekrarla: Belirli sayıda",
        "",
        "Örnek: Kare Çizme",
        "[4 kez tekrarla]",
        "  [100 adım git]",
        "  [90 derece dön]"
    ]
)

add_content_slide(
    "Hafta 30: Koşullar (If-Else)",
    [
        "❓ Koşul Nedir?",
        "Duruma göre karar verme",
        "",
        "Örnek: Kenara Çarpma",
        "<EĞER [kenara değdi mi?]>",
        "  [180 derece dön]",
        "",
        "Örnek: Puan Kontrolü",
        "<EĞER <[puan] > [50]>>",
        "  [Kazandın! söyle]",
        "<DEĞİLSE>",
        "  [Kaybettin! söyle]"
    ]
)

add_content_slide(
    "Hafta 31: Değişkenler",
    [
        "📦 Değişken Nedir?",
        "Bilgi saklayan kutu",
        "İsimli hafıza",
        "",
        "Örnekler:",
        "Puan = 100",
        "İsim = Ahmet",
        "Hız = 50"
    ]
)

add_content_slide(
    "Hafta 32: Operatörler",
    [
        "➕➖✖️➗ Matematik",
        "< [5] + [3] > → 8",
        "< [10] - [4] > → 6",
        "< [7] * [6] > → 42",
        "< [20] / [4] > → 5",
        "",
        "🎲 Rastgele",
        "< [1] ile [10] arası rastgele >"
    ]
)

add_content_slide(
    "Hafta 33: Listeler",
    [
        "📋 Liste Nedir?",
        "Birden fazla değer saklama",
        "",
        "Örnek:",
        "Meyveler = [Elma, Muz, Portakal]",
        "",
        "İşlemler:",
        "Eleman ekle",
        "Eleman sil",
        "Rastgele seç"
    ]
)

add_content_slide(
    "Hafta 34: Klonlama",
    [
        "👥 Klon Nedir?",
        "Sprite'ın kopyası",
        "Çok obje yaratma",
        "",
        "Kullanım Alanları:",
        "Düşmanlar",
        "Mermi/ateş",
        "Yıldızlar",
        "Partikül efektleri"
    ]
)

add_content_slide(
    "Hafta 35-36: İleri Projeler",
    [
        "🎮 Projeler",
        "",
        "1. Platform Oyunu:",
        "   Zıplama, Yer çekimi, Coin toplama",
        "",
        "2. Quiz Oyunu:",
        "   Sorular, Puan sistemi, Geri bildirim"
    ]
)

add_content_slide(
    "Hafta 37: Proje Sunumu",
    [
        "🎤 Sunum Zamanı!",
        "",
        "Ne sunuyoruz:",
        "Projem ne yapar?",
        "Hangi blokları kullandım?",
        "En zorlandığım yer?",
        "En beğendiğim özellik?"
    ]
)

# KAPANIŞ
add_section_slide("🎉 Tebrikler!", (67, 142, 234))

add_content_slide(
    "Bu Yıl Öğrendikleriniz",
    [
        "✅ Bilgisayar temelleri",
        "✅ Office programları",
        "✅ İnternet ve iletişim",
        "✅ Siber güvenlik",
        "✅ Yapay zeka",
        "✅ Scratch programlama"
    ]
)

add_content_slide(
    "🏆 Sertifika Zamanı!",
    [
        "Artık bir programcısınız!",
        "",
        "Gelecek yıl:",
        "Daha ileri programlama",
        "Video düzenleme",
        "Web tasarımı",
        "Ve çok daha fazlası!"
    ]
)

add_content_slide(
    "📚 KAYNAKLAR",
    [
        "Scratch: scratch.mit.edu",
        "Code.org: code.org",
        "Khan Academy: tr.khanacademy.org",
        "TÜBİTAK: tubitak.gov.tr"
    ]
)

add_content_slide(
    "📧 İletişim",
    [
        "Öğretmeninizle iletişime geçin!",
        "",
        "İyi çalışmalar! 🚀",
        "",
        "🌟 Kodlayarak Geleceği Şekillendiriyoruz! 🌟"
    ]
)

# Kaydet
prs.save('/home/user/BST/sunumlar/5-SINIF-FULL-SUNUM.pptx')
print("✅ 5. Sınıf PowerPoint sunumu başarıyla oluşturuldu!")
print(f"📊 Toplam {len(prs.slides)} slayt eklendi.")
