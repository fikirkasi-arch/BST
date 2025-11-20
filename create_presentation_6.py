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
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)

    # Alt başlık formatı
    subtitle_shape.text_frame.paragraphs[0].font.size = Pt(32)
    subtitle_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)

    # Arka plan rengi
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 240, 255)

    return slide

def add_section_slide(title, color_rgb=(118, 75, 162)):
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
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)

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
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)

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
                cell.fill.fore_color.rgb = RGBColor(118, 75, 162)
                cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
                cell.text_frame.paragraphs[0].font.bold = True

    return slide

# ANA SUNUM OLUŞTUR

# Kapak slaytı
add_title_slide(
    "6. SINIF BİLİŞİM TEKNOLOJİLERİ",
    "Tam Yıl Sunumu (40 Hafta)\n2025-2026 Eğitim Yılı"
)

# Hoş Geldiniz
add_content_slide(
    "🎯 Hoş Geldiniz!",
    [
        "6. Sınıf Bilişim Teknolojileri Dersine Hoş Geldiniz!",
        "",
        "Bu yıl neler öğreneceğiz?",
        "🛡️ Dijital güvenlik uzmanı ol!",
        "🎬 Video ve animasyon yap!",
        "🌐 Web sitesi oluştur!",
        "💻 İleri seviye programlama!"
    ]
)

# ÜNİTE 1: Bilişim Teknolojileri (4 hafta - önceden tamamlanmış)
add_section_slide("📚 ÜNİTE 1: Bilişim Teknolojileri", (220, 100, 180))

add_content_slide(
    "Hafta 1-2: Donanım ve Yazılım",
    [
        "💻 Temel Kavramlar",
        "Donanım: Fiziksel parçalar",
        "Yazılım: Programlar",
        "İşletim Sistemi: Bilgisayarı yöneten yazılım",
        "",
        "Yeni Teknolojiler:",
        "SSD (Hızlı disk)",
        "Cloud (Bulut depolama)",
        "AI (Yapay zeka entegrasyonu)"
    ]
)

# ÜNİTE 2: Etik ve Güvenlik
add_section_slide("📚 ÜNİTE 2: Etik ve Güvenlik", (220, 50, 50))

add_content_slide(
    "Hafta 5: Dijital Etik",
    [
        "🤝 Etik Kuralları:",
        "1. Saygılı dil kullan",
        "2. Başkasının eserini çalma",
        "3. Gizliliğe saygı",
        "4. Spam yapma",
        "5. Sorumluluk al",
        "",
        "Telif Hakkı:",
        "Yaratıcının eseri koruma hakkı",
        "Müzik, video, yazılım..."
    ]
)

add_table_slide(
    "Lisans Türleri",
    [
        ["Lisans", "Ücret", "Kaynak Kodu", "Değiştirme"],
        ["Ticari", "Evet", "Kapalı", "Hayır"],
        ["Freeware", "Hayır", "Kapalı", "Hayır"],
        ["Açık Kaynak", "Hayır", "Açık", "Evet"]
    ]
)

add_content_slide(
    "Hafta 6: Kişisel Veri ve Gizlilik",
    [
        "🔐 Kişisel Veri Nedir?",
        "Sizi tanımlayan her bilgi",
        "İsim, TC, telefon, e-posta, fotoğraf...",
        "",
        "KVKK (2016):",
        "Kişisel Verilerin Korunması Kanunu",
        "",
        "Haklarınız:",
        "Verilerini öğrenme",
        "Düzeltme",
        "Silme (Unutulma hakkı)"
    ]
)

add_content_slide(
    "Hafta 7: Siber Tehditler",
    [
        "🦠 Zararlı Yazılımlar:",
        "1. Virüs: Kendini kopyalar",
        "2. Truva Atı: Zararlı ama yararlı gibi",
        "3. Fidye Yazılımı: Dosyaları şifreler, para ister",
        "4. Casus Yazılım: Seni izler"
    ]
)

add_content_slide(
    "Phishing (Kimlik Avı)",
    [
        "🎣 Phishing Nedir?",
        "Sahte mesajla bilgi çalma",
        "",
        "Nasıl Anlaşılır?",
        "✉️ Yazım hataları",
        "⚠️ ACİL! HEMEN!",
        "🔗 Şüpheli link",
        "💰 Hediye/para vaadi",
        "",
        "ASLA tıklama! Sil!"
    ]
)

add_content_slide(
    "Hafta 8: Güvenli İnternet",
    [
        "🔒 Güçlü Şifre Kuralları:",
        "En az 12 karakter",
        "Büyük/küçük harf + sayı + sembol",
        "Her site için FARKLI şifre",
        "",
        "İki Faktörlü Doğrulama (2FA):",
        "Şifre + Telefon kodu",
        "%99.9 daha güvenli!"
    ]
)

add_content_slide(
    "HTTPS ve VPN",
    [
        "🔐 HTTPS:",
        "Güvenli web sitesi",
        "Kilit simgesi 🔒",
        "Bilgileriniz şifrelenir",
        "",
        "🛡️ VPN:",
        "İnterneti şifreler",
        "Özellikle açık WiFi'da kullan"
    ]
)

# ÜNİTE 3: İletişim ve İşbirliği
add_section_slide("📚 ÜNİTE 3: İletişim ve İşbirliği", (100, 180, 220))

add_content_slide(
    "Hafta 11: E-posta ve İletişim",
    [
        "📧 Profesyonel E-posta Yapısı:",
        "Konu: [Açık ve öz]",
        "Sayın [Alıcı],",
        "[Giriş]",
        "[Ana mesaj]",
        "[Kapanış]",
        "Saygılarımla, [İsim]"
    ]
)

add_content_slide(
    "Netiquette (İnternet Görgüsü)",
    [
        "Kurallar:",
        "❌ BÜYÜK HARF KULLANMA (bağırmak gibi)",
        "✅ Kısa ve öz yaz",
        "✅ Yazım kurallarına dikkat",
        "✅ Saygılı ol",
        "❌ Spam yapma"
    ]
)

add_content_slide(
    "Hafta 12: Araştırma ve Bilgi Okuryazarlığı",
    [
        "🔍 Etkili Araştırma:",
        "Gelişmiş Arama:",
        '"tam ifade" → Tırnak içinde ara',
        "-kelime → Hariç tut",
        "site:edu.tr → Sadece .edu.tr sitelerinde"
    ]
)

add_content_slide(
    "CRAAP Testi",
    [
        "Currency: Güncel mi?",
        "Relevance: İlgili mi?",
        "Authority: Yazar uzman mı?",
        "Accuracy: Doğru mu?",
        "Purpose: Amacı ne?",
        "",
        "Güvenilir Kaynaklar:",
        ".gov.tr, .edu.tr",
        "Üniversite siteleri",
        "Bilimsel dergiler"
    ]
)

add_content_slide(
    "Atıf (Kaynak Gösterme)",
    [
        "Neden Gerekli?",
        "Dürüstlük (intihal değil)",
        "Saygı",
        "Güvenilirlik",
        "",
        "Format:",
        'Yazar Adı, "Başlık", Site, Tarih, URL',
        "",
        "❌ Kopyala-yapıştır YAPMA!",
        "✅ Kendi cümlelerinle yaz + kaynak göster"
    ]
)

# ÜNİTE 4: Ürün Oluşturma
add_section_slide("📚 ÜNİTE 4: Ürün Oluşturma", (180, 100, 220))

add_content_slide(
    "Hafta 13: Grafik Tasarım",
    [
        "🎨 Tasarım İlkeleri:",
        "1. Denge: Dengeli dağılım",
        "2. Hiyerarşi: Önemli büyük olmalı",
        "3. Kontrast: Zıt renkler dikkat çeker",
        "4. Boşluk: Kalabalık olmasın",
        "",
        "Canva:",
        "Web: canva.com",
        "Ücretsiz!",
        "Şablonlar, görseller, fontlar"
    ]
)

add_content_slide(
    "Hafta 14: Çoklu Ortam",
    [
        "🎬 Multimedia Bileşenleri:",
        "Metin",
        "Görsel",
        "Ses",
        "Video",
        "Animasyon",
        "",
        "PowerPoint İleri:",
        "Animasyonlar",
        "Geçiş efektleri",
        "Ses/video ekleme",
        "Etkileşim (butonlar, linkler)"
    ]
)

add_content_slide(
    "Hafta 15: Video Düzenleme",
    [
        "🎥 Video Editing Yazılımları:",
        "Shotcut (PC - ücretsiz)",
        "CapCut (Mobil/PC)",
        "Windows Video Editor",
        "",
        "Temel İşlemler:",
        "Kırpma (Trim)",
        "Birleştirme",
        "Geçişler",
        "Müzik ekleme"
    ]
)

add_content_slide(
    "Hafta 16: Animasyon",
    [
        "🎞️ Animasyon Türleri:",
        "1. 2D Animasyon: Scratch",
        "2. 3D Animasyon: Blender",
        "3. Stop Motion: Fotoğraflarla",
        "",
        "FPS (Frame Per Second):",
        "24 fps → Sinema",
        "30 fps → TV",
        "60 fps → Oyunlar"
    ]
)

add_content_slide(
    "Hafta 17: Podcast",
    [
        "🎙️ Podcast Nedir?",
        "Ses tabanlı yayın",
        "Eğitim, hikaye, röportaj...",
        "",
        "Audacity (Ücretsiz):",
        "Ses kaydı",
        "Düzenleme",
        "Gürültü giderme",
        "Müzik ekleme"
    ]
)

add_content_slide(
    "Hafta 18: Web Sitesi",
    [
        "🌐 Google Sites",
        "Web: sites.google.com",
        "",
        "Sayfalar:",
        "1. Ana Sayfa",
        "2. Hakkımda",
        "3. İçerik sayfaları",
        "4. İletişim",
        "",
        "Özellikler:",
        "Sürükle-bırak (kolay!)",
        "Resim, video ekleme",
        "Yayınlama"
    ]
)

add_content_slide(
    "Hafta 19: Ünite Değerlendirme",
    [
        "🎨 Dijital Portfolyo",
        "",
        "Tüm çalışmalarınızı sergileyin:",
        "Grafik tasarımlar",
        "Videolar",
        "Animasyonlar",
        "Podcast",
        "Web sitesi",
        "",
        "Artık bir Dijital İçerik Üreticisisiniz!"
    ]
)

# ÜNİTE 5: Problem Çözme ve Programlama
add_section_slide("📚 ÜNİTE 5: Problem Çözme ve Programlama", (220, 150, 50))

add_content_slide(
    "Hafta 20: Problem Çözme",
    [
        "🧩 Problem Çözme Adımları:",
        "1. Anla: Problemi anla",
        "2. Planla: Çözüm yolu bul",
        "3. Uygula: Çözümü yap",
        "4. Kontrol: Doğru mu?",
        "",
        "Algoritmik Düşünme:",
        "Adım adım düşünme",
        "Mantıksal sıralama"
    ]
)

add_content_slide(
    "Hafta 21-25: Scratch İleri",
    [
        "💻 İleri Scratch Konuları:",
        "Karmaşık oyunlar",
        "Fizik simülasyonu",
        "Yapay zeka entegrasyonu",
        "Multiplayer oyunlar",
        "3D efektler"
    ]
)

add_content_slide(
    "Hafta 26-30: Python Giriş (Opsiyonel)",
    [
        "🐍 Python Nedir?",
        "Profesyonel programlama dili",
        "Öğrenmesi kolay",
        "AI, web, oyun, veri bilimi...",
        "",
        'İlk Program:',
        'print("Merhaba Dünya!")'
    ]
)

add_table_slide(
    "Python vs Scratch",
    [
        ["Scratch", "Python"],
        ["Bloklar", "Kod yazma"],
        ["Görsel", "Metin"],
        ["Başlangıç", "İleri seviye"],
        ["Çocuklar", "Profesyoneller"]
    ]
)

add_content_slide(
    "Hafta 31-35: İleri Projeler",
    [
        "🎮 Büyük Projeler:",
        "1. Platform Oyunu: Gelişmiş",
        "2. Quiz Sistemi: Veritabanı",
        "3. Simülasyon: Fizik",
        "4. AI Oyunu: Akıllı düşman",
        "5. Sosyal Ağ: Mini uygulama"
    ]
)

add_content_slide(
    "Hafta 36-39: Final Projesi",
    [
        "🚀 Final Projesi",
        "Kendi projenizi yapın!",
        "",
        "Gereksinimler:",
        "Tüm öğrenilenleri kullan",
        "Yaratıcı ol",
        "Kullanışlı olsun",
        "Sunum hazırla"
    ]
)

# KAPANIŞ
add_section_slide("🎉 Tebrikler!", (118, 75, 162))

add_content_slide(
    "Bu Yıl Öğrendikleriniz",
    [
        "✅ Dijital Etik ve KVKK",
        "✅ Siber Güvenlik (Phishing, 2FA, VPN)",
        "✅ Bilgi Okuryazarlığı",
        "✅ Grafik Tasarım",
        "✅ Video Düzenleme",
        "✅ Animasyon",
        "✅ Podcast",
        "✅ Web Sitesi",
        "✅ İleri Programlama"
    ]
)

add_content_slide(
    "🏆 Sertifika Zamanı!",
    [
        "Artık bir Bilişim Uzmanısınız!",
        "",
        "Gelecek:",
        "7. Sınıfta robotik kodlama",
        "Mobil uygulama",
        "3D modelleme",
        "Veri bilimi"
    ]
)

add_content_slide(
    "💼 Gelecek Kariyerler",
    [
        "Bilişim sektöründe:",
        "Yazılım Geliştirici",
        "Web Tasarımcı",
        "Oyun Geliştiricisi",
        "Siber Güvenlik Uzmanı",
        "Veri Bilimci",
        "AI Mühendisi",
        "YouTuber / İçerik Üreticisi"
    ]
)

add_content_slide(
    "📚 KAYNAKLAR",
    [
        "Scratch: scratch.mit.edu",
        "Code.org: code.org",
        "Python: python.org",
        "Canva: canva.com",
        "Google Sites: sites.google.com",
        "Khan Academy: tr.khanacademy.org"
    ]
)

add_content_slide(
    "🎓 Son Söz",
    [
        '"Öğrendiklerinizi paylaşın,',
        'başkalarına öğretin,',
        'projeler yapın!"',
        "",
        "Dijital dünyada bir iz bırakın!",
        "",
        "Başarılar! 💪💻🌟"
    ]
)

# Kaydet
prs.save('/home/user/BST/sunumlar/6-SINIF-FULL-SUNUM.pptx')
print("✅ 6. Sınıf PowerPoint sunumu başarıyla oluşturuldu!")
print(f"📊 Toplam {len(prs.slides)} slayt eklendi.")
