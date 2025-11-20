#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5. Sınıf Geliştirilmiş PowerPoint Sunumu
Görsel notları, video linkleri ve şekillerle zenginleştirilmiş
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
import re

# PowerPoint oluştur
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

def add_title_slide(title, subtitle, image_note=""):
    """Başlık slaytı ekle"""
    slide_layout = prs.slide_layouts[0]
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

    # Notlar ekle
    if image_note:
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = image_note

    return slide

def add_section_slide(title, color_rgb=(67, 142, 234)):
    """Bölüm başlığı slaytı ekle"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # Arka plan
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

def add_content_slide(title, content_items, notes="", video_link=""):
    """İçerik slaytı ekle - notlar ve video linkleri ile"""
    slide_layout = prs.slide_layouts[1]
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
        clean_item = re.sub(r'\*\*(.*?)\*\*', r'\1', item)
        p.text = clean_item
        p.level = 0
        p.font.size = Pt(24)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.space_before = Pt(6)

    # Arka plan
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Notlar ekle
    notes_text = ""
    if notes:
        notes_text += f"📝 GÖRSEL ÖNERİSİ: {notes}\n\n"
    if video_link:
        notes_text += f"🎥 VİDEO LİNKİ: {video_link}\n\n"

    if notes_text:
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    return slide

def add_content_slide_with_image(title, content_items, notes="", video_link=""):
    """İçerik + görsel alanı olan slayt"""
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)

    # Başlık
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = Pt(40)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(67, 142, 234)

    # İçerik (sol)
    content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(5.5))
    tf = content_box.text_frame
    tf.word_wrap = True

    for item in content_items:
        p = tf.add_paragraph()
        clean_item = re.sub(r'\*\*(.*?)\*\*', r'\1', item)
        p.text = clean_item
        p.font.size = Pt(20)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.space_before = Pt(4)

    # Görsel placeholder (sağ)
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(5.5), Inches(1.5),
        Inches(4), Inches(5.5)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(230, 240, 255)
    shape.line.color.rgb = RGBColor(67, 142, 234)
    shape.line.width = Pt(3)

    # Görsel placeholder text
    text_frame = shape.text_frame
    text_frame.text = "📷\n\nGÖRSEL\nEKLENECEK"
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    for paragraph in text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        paragraph.font.size = Pt(24)
        paragraph.font.color.rgb = RGBColor(100, 120, 180)

    # Arka plan
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # Notlar ekle
    notes_text = ""
    if notes:
        notes_text += f"📝 GÖRSEL ÖNERİSİ: {notes}\n\n"
    if video_link:
        notes_text += f"🎥 VİDEO LİNKİ: {video_link}\n\n"

    if notes_text:
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    return slide

def add_table_slide(title, table_data, notes=""):
    """Tablo slaytı ekle"""
    slide_layout = prs.slide_layouts[5]
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

    for i, row_data in enumerate(table_data):
        for j, cell_data in enumerate(row_data):
            cell = table.rows[i].cells[j]
            cell.text = cell_data
            cell.text_frame.paragraphs[0].font.size = Pt(18)

            if i == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(67, 142, 234)
                cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
                cell.text_frame.paragraphs[0].font.bold = True

    # Notlar
    if notes:
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes

    return slide

def add_video_slide(title, video_description, video_link):
    """Video slaytı - link ve açıklama ile"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # Başlık
    txBox = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(44)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(67, 142, 234)

    # Video placeholder
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(2), Inches(2),
        Inches(6), Inches(3.5)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(50, 50, 50)

    # Play butonu simgesi
    text_frame = shape.text_frame
    text_frame.text = "▶️\n\nVİDEO"
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    for paragraph in text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        paragraph.font.size = Pt(48)
        paragraph.font.color.rgb = RGBColor(255, 255, 255)

    # Açıklama
    desc_box = slide.shapes.add_textbox(Inches(1), Inches(5.8), Inches(8), Inches(1.2))
    tf = desc_box.text_frame
    tf.text = video_description
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)

    # Arka plan
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 250)

    # Video linki notlara
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = f"🎥 VİDEO LİNKİ:\n{video_link}\n\nBu slayta video eklemek için:\n1. Slayta tıklayın\n2. Ekle > Video > Çevrimiçi Video\n3. Yukarıdaki linki yapıştırın"

    return slide

# ============== SUNUM OLUŞTUR ==============

# Kapak
add_title_slide(
    "5. SINIF BİLİŞİM TEKNOLOJİLERİ",
    "Tam Yıl Sunumu (38 Hafta)\n2025-2026 Eğitim Yılı",
    "Kapak görseli önerisi: Renkli bilgisayar, tablet ve teknoloji görselleri"
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
    ],
    notes="Mutlu öğrencilerin bilgisayar başında çalıştığı fotoğraf",
    video_link="https://www.youtube.com/watch?v=tpIctyqH29Q (Bilişim Teknolojilerine Giriş)"
)

# ÜNİTE 1: Bilişim Temelleri
add_section_slide("📚 ÜNİTE 1: Bilişim Temelleri", (220, 100, 180))

add_content_slide_with_image(
    "Hafta 1: Bilgisayar ve Bileşenleri",
    [
        "💻 Bilgisayar Nedir?",
        "Veri işleyen elektronik cihaz",
        "Giriş → İşlem → Çıkış",
        "",
        "Donanım Bileşenleri:",
        "• Kasa: Ana gövde",
        "• Ekran: Görüntü",
        "• Klavye: Yazı yazma",
        "• Mouse: İmleç kontrolü"
    ],
    notes="Bilgisayar parçalarının görseli (kasa, ekran, klavye, mouse)",
    video_link="https://www.youtube.com/watch?v=HB4I2CgkcCo (Bilgisayar Nedir? - TRT Çocuk)"
)

add_content_slide_with_image(
    "Donanım Detayları",
    [
        "İçeridekiler:",
        "🧠 İşlemci (CPU)",
        "   Bilgisayarın beyni",
        "",
        "💾 RAM",
        "   Hızlı geçici bellek",
        "",
        "💿 Harddisk/SSD",
        "   Kalıcı depolama",
        "",
        "🎮 Ekran Kartı",
        "   Görüntü işleme"
    ],
    notes="Anakart üzerinde CPU, RAM, HDD görseli veya infografik",
    video_link="https://www.youtube.com/watch?v=ExxFxD4OSZ0 (Bilgisayar İçi Donanım)"
)

add_video_slide(
    "🎬 Video: Bilgisayar Nasıl Çalışır?",
    "İşlemci, RAM ve diskin birlikte nasıl çalıştığını gösteren animasyon",
    "https://www.youtube.com/watch?v=cNN_tTXABUA (How Computers Work - Crash Course)"
)

add_content_slide_with_image(
    "Hafta 2: İşletim Sistemleri",
    [
        "💿 İşletim Sistemi Nedir?",
        "Donanım ve yazılım arasındaki köprü",
        "",
        "Popüler İşletim Sistemleri:",
        "🪟 Windows - En yaygın",
        "🍎 macOS - Apple ürünleri",
        "🐧 Linux - Açık kaynak",
        "📱 Android & iOS - Mobil"
    ],
    notes="Windows, macOS, Linux logoları",
    video_link="https://www.youtube.com/watch?v=pTdSs8kQqSA (İşletim Sistemi Nedir?)"
)

add_content_slide(
    "Hafta 3: Dosya Yönetimi",
    [
        "📁 Dosya ve Klasör",
        "• Dosya: Bilgi saklayan birim",
        "• Klasör: Dosyaları düzenler",
        "",
        "İsimlendirme Kuralları:",
        "✅ Anlamlı isim ver",
        "✅ Tarih ekle (2025-01-15_odev)",
        "❌ Özel karakter kullanma (?, *, /)",
        "",
        "Düzen Örnekleri:",
        "Dersler > Bilisim > Odev1.docx"
    ],
    notes="Windows Explorer veya Finder ekran görüntüsü - düzenli klasör yapısı",
    video_link="https://www.youtube.com/watch?v=k-EID5_2D9U (Dosya Yönetimi)"
)

# ÜNİTE 2: Dijital Ürün Tasarımı
add_section_slide("📚 ÜNİTE 2: Dijital Ürün Tasarımı", (100, 180, 220))

add_content_slide_with_image(
    "Hafta 10: Microsoft Word",
    [
        "📝 Word ile Belge Oluşturma",
        "",
        "Temel İşlemler:",
        "• Yazı yazma ve biçimlendirme",
        "• Resim ekleme",
        "• Tablo oluşturma",
        "• Sayfa düzeni",
        "",
        "Kısayollar:",
        "Ctrl + C → Kopyala",
        "Ctrl + V → Yapıştır",
        "Ctrl + Z → Geri al"
    ],
    notes="Word arayüzü ekran görüntüsü - Giriş sekmesi araçları",
    video_link="https://www.youtube.com/watch?v=9WNvhQRqWbY (Microsoft Word Temelleri)"
)

add_content_slide_with_image(
    "Hafta 11: Paint",
    [
        "🎨 Paint ile Çizim",
        "",
        "Araçlar:",
        "🖌️ Fırça",
        "✏️ Kalem",
        "⬜ Şekiller",
        "🅰️ Metin",
        "🌈 Renk seçici",
        "",
        "İpucu:",
        "Shift tuşu ile düzgün şekil çizin!"
    ],
    notes="Paint arayüzü ve örnek çizim",
    video_link="https://www.youtube.com/watch?v=VJ9QCiJ-kJQ (Paint Kullanımı)"
)

add_content_slide_with_image(
    "Hafta 12: PowerPoint Başlangıç",
    [
        "🎬 Sunum Hazırlama",
        "",
        "PowerPoint Nedir?",
        "Görsel sunumlar hazırlama aracı",
        "",
        "Slayt Öğeleri:",
        "• Başlık",
        "• Metin",
        "• Resim",
        "• Video",
        "• Şekiller",
        "• Animasyonlar"
    ],
    notes="PowerPoint arayüzü ve örnek slayt",
    video_link="https://www.youtube.com/watch?v=3LqNiYbRzBM (PowerPoint Başlangıç)"
)

add_content_slide(
    "İyi Sunum Özellikleri",
    [
        "✅ YAPILMASI GEREKENLER:",
        "• Sade ve öz olmalı",
        "• Büyük font kullan (24+ punto)",
        "• Görsellerle destekle",
        "• Uyumlu renkler",
        "• Anahtar kelimeler",
        "",
        "❌ YAPILMAMASI GEREKENLER:",
        "• Çok yazı",
        "• Küçük font",
        "• Karışık renkler",
        "• Okumak zor"
    ],
    notes="İyi ve kötü sunum örnekleri yan yana (Önce/Sonra)"
)

# ÜNİTE 3: Ağlar ve İletişim
add_section_slide("📚 ÜNİTE 3: Ağlar ve İletişim", (180, 220, 100))

add_content_slide_with_image(
    "Hafta 16: İnternet",
    [
        "🌐 İnternet Nedir?",
        "Dünya çapında bilgisayar ağı",
        "",
        "Bağlantı Türleri:",
        "📶 Wi-Fi - Kablosuz",
        "🔌 Ethernet - Kablolu",
        "📱 Mobil Veri - 4G/5G",
        "",
        "Tarayıcılar:",
        "Chrome, Firefox, Edge, Safari"
    ],
    notes="İnternet ağ diyagramı - router, modem, cihazlar",
    video_link="https://www.youtube.com/watch?v=Dxcc6ycZ73M (İnternet Nasıl Çalışır?)"
)

add_content_slide_with_image(
    "Hafta 17: E-posta",
    [
        "📧 E-posta Kullanımı",
        "",
        "E-posta Bileşenleri:",
        "Kime: Alıcı adresi",
        "Konu: Başlık (önemli!)",
        "Gövde: Mesajınız",
        "Ek: Dosya ekleme",
        "",
        "İpuçları:",
        "• Açık konu yazın",
        "• Saygılı dil kullanın",
        "• İmza ekleyin"
    ],
    notes="Gmail veya Outlook arayüzü ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=AEWR5khNNMA (E-posta Nasıl Yazılır?)"
)

# ÜNİTE 4: Etik ve Güvenlik
add_section_slide("📚 ÜNİTE 4: Etik ve Güvenlik", (220, 50, 50))

add_content_slide(
    "Hafta 19: Dijital Etik",
    [
        "🤝 Dijital Etik Kuralları:",
        "",
        "1. Saygılı ol",
        "2. Kişisel bilgi paylaşma",
        "3. Telif hakkına saygı göster",
        "4. Spam yapma",
        "5. Siber zorbalık yapma",
        "",
        "Telif Hakkı:",
        "Başkasının eserini izinsiz kullanma!",
        "Müzik, fotoğraf, yazı, kod..."
    ],
    notes="Dijital etik kuralları infografik",
    video_link="https://www.youtube.com/watch?v=OoqXu-8kW0E (Dijital Vatandaşlık)"
)

add_content_slide(
    "Hafta 20: Güvenlik",
    [
        "🔒 Güçlü Şifre",
        "",
        "Şifre Kuralları:",
        "✅ En az 8-12 karakter",
        "✅ Büyük harf (A-Z)",
        "✅ Küçük harf (a-z)",
        "✅ Rakam (0-9)",
        "✅ Sembol (!@#$%)",
        "",
        "❌ KULLANMAYIN:",
        "123456, password, adınız, doğum tarihi"
    ],
    notes="Güçlü şifre örnekleri ve zayıf şifre örnekleri karşılaştırması",
    video_link="https://www.youtube.com/watch?v=0RCsHJfHL_4 (Şifre Güvenliği)"
)

# ÜNİTE 5: Yapay Zeka
add_section_slide("📚 ÜNİTE 5: Yapay Zeka", (50, 150, 220))

add_content_slide_with_image(
    "Hafta 21: Yapay Zeka Nedir?",
    [
        "🤖 YZ Tanımı",
        "Makinelerin insan gibi",
        "düşünme yeteneği",
        "",
        "Günlük Örnekler:",
        "🎤 Siri / Alexa",
        "🌐 Google Translate",
        "🎬 Netflix önerileri",
        "📸 Yüz tanıma",
        "🎵 Spotify önerileri"
    ],
    notes="Yapay zeka uygulamaları kolajı (Siri, Alexa, Netflix vb.)",
    video_link="https://www.youtube.com/watch?v=mJeNghZXtMo (Yapay Zeka Nedir? - Basit Anlatım)"
)

add_table_slide(
    "İnsan vs Yapay Zeka",
    [
        ["İnsan Zekası", "Yapay Zeka"],
        ["Duygular var", "Duygusuz"],
        ["Yaratıcı", "Öğrenileni yapar"],
        ["Yorulur", "Yorulmaz"],
        ["Esnek", "Kurallara bağlı"],
        ["Öğrenme yavaş", "Öğrenme hızlı"]
    ],
    notes="İnsan beyni ve robot beyni karşılaştırma görseli"
)

add_video_slide(
    "🎬 Video: YZ Nasıl Çalışır?",
    "Yapay zekanın öğrenme sürecini gösteren animasyon",
    "https://www.youtube.com/watch?v=aircAruvnKk (Neural Networks - 3Blue1Brown)"
)

# ÜNİTE 6: Scratch Programlama
add_section_slide("📚 ÜNİTE 6: Scratch Programlama", (220, 150, 50))

add_content_slide_with_image(
    "Hafta 25: Algoritma",
    [
        "🧩 Algoritma Nedir?",
        "Adım adım talimatlar",
        "",
        "Örnek: Çay Yapma",
        "1. Çaydanlığı al",
        "2. Su doldur",
        "3. Ocağa koy",
        "4. Yak",
        "5. Kaynasın",
        "6. Çay koy",
        "7. İç ☕"
    ],
    notes="Akış diyagramı örneği (çay yapma algoritması)",
    video_link="https://www.youtube.com/watch?v=6hfOvs8pY1k (Algoritma Nedir?)"
)

add_content_slide_with_image(
    "Hafta 26: Scratch Tanıtım",
    [
        "💻 Scratch Nedir?",
        "",
        "Blok tabanlı programlama",
        "MIT tarafından geliştirildi",
        "8-16 yaş için ideal",
        "Ücretsiz!",
        "",
        "Web: scratch.mit.edu",
        "",
        "Ne yapılabilir?",
        "🎮 Oyunlar, 🎬 Animasyonlar,",
        "📖 Hikayeler, 🎨 Sanat"
    ],
    notes="Scratch logosu ve arayüz ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=jXUZaf5D12A (Scratch Giriş - Türkçe)"
)

add_content_slide_with_image(
    "Scratch Arayüzü",
    [
        "Bileşenler:",
        "",
        "1️⃣ SAHNE",
        "Karakterlerin oynadığı yer",
        "",
        "2️⃣ SPRITE (Karakter)",
        "Oyundaki nesneler",
        "",
        "3️⃣ BLOKLAR",
        "Komutlar",
        "",
        "4️⃣ KOD ALANI",
        "Blokları birleştirdiğimiz yer"
    ],
    notes="Scratch arayüzü - işaretlenmiş bölümleri gösteren ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=JaMNwHgCoBo (Scratch Arayüzü Tanıtımı)"
)

add_content_slide_with_image(
    "Hafta 27: Hareket Blokları",
    [
        "🏃 Hareket Blokları",
        "",
        "[10 adım git]",
        "İlerle",
        "",
        "[15 derece dön]",
        "Dön",
        "",
        "[x:0 y:0 git]",
        "Konuma git",
        "",
        "Koordinatlar:",
        "x: Sağ-Sol (-240 ~ +240)",
        "y: Yukarı-Aşağı (-180 ~ +180)"
    ],
    notes="Scratch sahne koordinat sistemi görseli",
    video_link="https://www.youtube.com/watch?v=x14G4DCk4nY (Scratch Hareket Blokları)"
)

add_content_slide_with_image(
    "Hafta 29: Döngüler",
    [
        "🔁 Döngü Nedir?",
        "Tekrar tekrar yapma",
        "",
        "Döngü Türleri:",
        "",
        "1. [Sonsuza kadar]",
        "   Hiç durma",
        "",
        "2. [10 kez tekrarla]",
        "   Belirli sayıda",
        "",
        "Örnek: Kare Çiz",
        "[4 kez tekrarla]",
        "  [100 adım git]",
        "  [90 derece dön]"
    ],
    notes="Scratch döngü blokları ve kare çizim örneği",
    video_link="https://www.youtube.com/watch?v=mgooqyWMTxk (Scratch Döngüler)"
)

add_content_slide_with_image(
    "Hafta 30: Koşullar",
    [
        "❓ Koşul (If-Else)",
        "Duruma göre karar ver",
        "",
        "Örnek 1:",
        "<EĞER [kenara değdi?]>",
        "  [geri dön]",
        "",
        "Örnek 2:",
        "<EĞER <puan > 50>>",
        "  [Kazandın! söyle]",
        "<DEĞİLSE>",
        "  [Kaybettin! söyle]"
    ],
    notes="Scratch if-else blok örnekleri ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=m2Ux2PnJe6E (Scratch Koşullar)"
)

add_content_slide_with_image(
    "Hafta 31: Değişkenler",
    [
        "📦 Değişken Nedir?",
        "Bilgi saklayan kutu",
        "",
        "Örnekler:",
        "Puan = 100",
        "Hız = 50",
        "İsim = Ahmet",
        "",
        "İşlemler:",
        "[Puan] değişkenini [10] yap",
        "[Puan] değişkenini [5] arttır",
        "[Puan] göster/gizle"
    ],
    notes="Scratch değişken oluşturma ve kullanma ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=tfXiEP5gbP4 (Scratch Değişkenler)"
)

add_content_slide(
    "Hafta 33: Listeler",
    [
        "📋 Liste Nedir?",
        "Birden fazla değer saklama",
        "",
        "Örnek:",
        "Meyveler = [Elma, Muz, Portakal, Çilek]",
        "",
        "İşlemler:",
        "[Elma] öğesini listeye ekle",
        "Listeden [1] numaralı öğeyi sil",
        "Listeden rastgele öğe seç"
    ],
    notes="Scratch liste oluşturma örneği",
    video_link="https://www.youtube.com/watch?v=m9QT0JJXJpY (Scratch Listeler)"
)

add_content_slide_with_image(
    "Hafta 35: Oyun Projesi",
    [
        "🎮 Platform Oyunu",
        "",
        "Özellikler:",
        "• Karakter kontrolü (WASD)",
        "• Zıplama",
        "• Yer çekimi",
        "• Engeller",
        "• Coin toplama",
        "• Puan sistemi",
        "• Can sistemi"
    ],
    notes="Scratch platform oyunu örnek ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=Sn6jppzxPqc (Scratch Platform Oyunu Yapımı)"
)

# KAPANIŞ
add_section_slide("🎉 Tebrikler!", (67, 142, 234))

add_content_slide(
    "Bu Yıl Öğrendikleriniz",
    [
        "✅ Bilgisayar temelleri ve donanım",
        "✅ İşletim sistemleri",
        "✅ Office programları (Word, Paint, PowerPoint)",
        "✅ İnternet ve iletişim",
        "✅ Dijital etik",
        "✅ Siber güvenlik",
        "✅ Yapay zeka temelleri",
        "✅ Scratch programlama",
        "✅ Oyun geliştirme"
    ],
    notes="Mutlu mezun olan öğrenciler fotoğrafı"
)

add_content_slide(
    "🏆 Artık Bir Programcısınız!",
    [
        "Bilişim Teknolojileri Sertifikanız",
        "",
        "Gelecek Yıl:",
        "• Daha ileri programlama",
        "• Video düzenleme",
        "• Web tasarımı",
        "• Mobil uygulama",
        "• Robotik kodlama",
        "",
        "Kodlamaya devam edin! 🚀"
    ],
    video_link="https://www.youtube.com/watch?v=nKIu9yen5nc (Geleceğin Meslekleri)"
)

add_content_slide(
    "📚 Faydalı Kaynaklar",
    [
        "🌐 Scratch: scratch.mit.edu",
        "🌐 Code.org: code.org",
        "🌐 Khan Academy: tr.khanacademy.org",
        "🌐 TÜBİTAK: tubitak.gov.tr",
        "📺 YouTube: 'Scratch Türkçe' ara",
        "",
        "İyi çalışmalar! 🌟",
        "",
        "Kodlayarak Geleceği Şekillendiriyoruz!"
    ]
)

# Kaydet
prs.save('/home/user/BST/sunumlar/5-SINIF-FULL-SUNUM.pptx')
print("✅ 5. Sınıf Geliştirilmiş PowerPoint sunumu oluşturuldu!")
print(f"📊 Toplam {len(prs.slides)} slayt")
print("📝 Notlar: Her slayta görsel önerileri ve video linkleri eklendi")
print("🎨 Görsel placeholder'lar eklendi")
print("🎥 Video slaytları eklendi")
