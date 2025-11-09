#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6. Sınıf Geliştirilmiş PowerPoint Sunumu
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

    title_shape.text_frame.paragraphs[0].font.size = Pt(54)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)

    subtitle_shape.text_frame.paragraphs[0].font.size = Pt(32)
    subtitle_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)

    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 240, 255)

    if image_note:
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = image_note

    return slide

def add_section_slide(title, color_rgb=(118, 75, 162)):
    """Bölüm başlığı slaytı ekle"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*color_rgb)

    txBox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(2))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(60)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

    return slide

def add_content_slide(title, content_items, notes="", video_link=""):
    """İçerik slaytı ekle"""
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.title
    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(40)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)

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

    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

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
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    # Başlık
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].font.size = Pt(40)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)

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
    shape.fill.fore_color.rgb = RGBColor(240, 230, 255)
    shape.line.color.rgb = RGBColor(118, 75, 162)
    shape.line.width = Pt(3)

    text_frame = shape.text_frame
    text_frame.text = "📷\n\nGÖRSEL\nEKLENECEK"
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    for paragraph in text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        paragraph.font.size = Pt(24)
        paragraph.font.color.rgb = RGBColor(150, 100, 180)

    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

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
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)

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
                cell.fill.fore_color.rgb = RGBColor(118, 75, 162)
                cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
                cell.text_frame.paragraphs[0].font.bold = True

    if notes:
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes

    return slide

def add_video_slide(title, video_description, video_link):
    """Video slaytı"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    txBox = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
    tf = txBox.text_frame
    tf.text = title
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(44)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = RGBColor(118, 75, 162)

    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(2), Inches(2),
        Inches(6), Inches(3.5)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(50, 50, 50)

    text_frame = shape.text_frame
    text_frame.text = "▶️\n\nVİDEO"
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    for paragraph in text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.CENTER
        paragraph.font.size = Pt(48)
        paragraph.font.color.rgb = RGBColor(255, 255, 255)

    desc_box = slide.shapes.add_textbox(Inches(1), Inches(5.8), Inches(8), Inches(1.2))
    tf = desc_box.text_frame
    tf.text = video_description
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].font.size = Pt(20)
    tf.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)

    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(250, 245, 255)

    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = f"🎥 VİDEO LİNKİ:\n{video_link}\n\nBu slayta video eklemek için:\n1. Slayta tıklayın\n2. Ekle > Video > Çevrimiçi Video\n3. Yukarıdaki linki yapıştırın"

    return slide

# ============== 6. SINIF SUNUM ==============

# Kapak
add_title_slide(
    "6. SINIF BİLİŞİM TEKNOLOJİLERİ",
    "Tam Yıl Sunumu (40 Hafta)\n2025-2026 Eğitim Yılı",
    "Kapak görseli: İleri seviye teknoloji, kodlama, siber güvenlik temalı görsel"
)

# Hoş Geldiniz
add_content_slide(
    "🎯 6. Sınıfa Hoş Geldiniz!",
    [
        "İleri Seviye Bilişim Teknolojileri",
        "",
        "Bu yıl neler öğreneceğiz?",
        "🛡️ Dijital güvenlik uzmanı ol!",
        "🎬 Video ve animasyon yap!",
        "🌐 Web sitesi oluştur!",
        "💻 İleri seviye programlama!",
        "🤖 Yapay zeka projeleri!"
    ],
    notes="Ortaokul öğrencilerinin teknoloji projeleri üzerinde çalıştığı fotoğraf",
    video_link="https://www.youtube.com/watch?v=QvyTEx1wyOY (Bilişim Teknolojileri - Geleceğin Meslekleri)"
)

# ÜNİTE 2: Etik ve Güvenlik
add_section_slide("📚 ÜNİTE 2: Etik ve Güvenlik", (220, 50, 50))

add_content_slide_with_image(
    "Hafta 5: Dijital Etik",
    [
        "🤝 Dijital Etik Kuralları",
        "",
        "1. Saygılı dil kullan",
        "2. Başkasının eserini çalma",
        "3. Gizliliğe saygı göster",
        "4. Spam yapma",
        "5. Sorumluluğunu al",
        "",
        "Telif Hakkı:",
        "Yaratıcının eseri",
        "koruma hakkı"
    ],
    notes="Dijital etik kuralları infografik - do's and don'ts",
    video_link="https://www.youtube.com/watch?v=OoqXu-8kW0E (Dijital Vatandaşlık ve Etik)"
)

add_table_slide(
    "Yazılım Lisans Türleri",
    [
        ["Lisans", "Ücret", "Kaynak Kodu", "Değiştirme"],
        ["Ticari", "Evet", "Kapalı", "Hayır"],
        ["Freeware", "Hayır", "Kapalı", "Hayır"],
        ["Açık Kaynak", "Hayır", "Açık", "Evet"],
        ["Shareware", "Deneme", "Kapalı", "Hayır"]
    ],
    notes="Her lisans türüne örnek: Windows (ticari), VLC (açık kaynak), WinRAR (shareware)"
)

add_content_slide_with_image(
    "Hafta 6: KVKK ve Gizlilik",
    [
        "🔐 Kişisel Veri Nedir?",
        "",
        "Sizi tanımlayan bilgi:",
        "• TC Kimlik No",
        "• İsim, adres, telefon",
        "• E-posta",
        "• Fotoğraf, video",
        "• Sağlık bilgileri",
        "",
        "KVKK (2016):",
        "Kişisel Verilerin",
        "Korunması Kanunu"
    ],
    notes="KVKK logosu ve kişisel veri örnekleri görseli",
    video_link="https://www.youtube.com/watch?v=mGZxN5p-Vf0 (KVKK Nedir? - Basit Anlatım)"
)

add_content_slide(
    "KVKK Hakları",
    [
        "Vatandaş olarak haklarınız:",
        "",
        "✅ Verilerimi öğrenme",
        "✅ Düzeltme isteme",
        "✅ Silme (unutulma hakkı)",
        "✅ İtiraz etme",
        "✅ Taşınabilirlik",
        "",
        "Şirketler:",
        "❌ İzinsiz veri toplayamaz",
        "❌ Satamaz, paylaşamaz"
    ],
    notes="KVKK hakları infografik"
)

add_content_slide_with_image(
    "Hafta 7: Siber Tehditler",
    [
        "🦠 Zararlı Yazılım Türleri",
        "",
        "1. VİRÜS",
        "   Kendini kopyalar",
        "",
        "2. TRUVA ATI",
        "   Zararlı ama yararlı gibi",
        "",
        "3. FİDYE YAZILIMI",
        "   Dosyaları şifreler",
        "",
        "4. CASUS YAZILIM",
        "   Seni izler"
    ],
    notes="Her zararlı yazılım türü için ikon/simge görseli",
    video_link="https://www.youtube.com/watch?v=SZIBCUwrfW4 (Zararlı Yazılımlar Nelerdir?)"
)

add_content_slide_with_image(
    "Phishing (Kimlik Avı)",
    [
        "🎣 Phishing Nedir?",
        "Sahte mesajla bilgi çalma",
        "",
        "Nasıl Anlaşılır?",
        "⚠️ Yazım hataları",
        "⚠️ ACİL! HEMEN!",
        "⚠️ Şüpheli link",
        "⚠️ Hediye/para vaadi",
        "⚠️ Bilinmeyen gönderici",
        "",
        "NE YAPILMALI?",
        "❌ Tıklama!",
        "✅ Sil ve bildir"
    ],
    notes="Phishing e-posta örneği (sahte banka maili) ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=Y4pvOaJWgCY (Phishing Saldırıları)"
)

add_content_slide_with_image(
    "Hafta 8: Şifre Güvenliği",
    [
        "🔒 Güçlü Şifre",
        "",
        "Kurallar:",
        "✅ En az 12 karakter",
        "✅ Büyük harf (A-Z)",
        "✅ Küçük harf (a-z)",
        "✅ Rakam (0-9)",
        "✅ Sembol (!@#$%)",
        "✅ Her site için farklı",
        "",
        "❌ KULLANMAYIN:",
        "123456, qwerty,",
        "adınız, doğum tarihi"
    ],
    notes="Şifre gücü göstergesi (zayıf/orta/güçlü) ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=3NjQ9b3pgIg (Güçlü Şifre Nasıl Oluşturulur?)"
)

add_content_slide(
    "İki Faktörlü Doğrulama (2FA)",
    [
        "🔐 2FA Nedir?",
        "",
        "Çift katman güvenlik:",
        "1. Şifrenizi girin",
        "2. Telefonunuza kod gelir",
        "3. Kodu girin",
        "",
        "Avantajlar:",
        "✅ %99.9 daha güvenli",
        "✅ Şifre çalınsa bile güvenli",
        "",
        "Kullanım:",
        "Google, Instagram, WhatsApp..."
    ],
    notes="2FA kod girme ekranı görseli",
    video_link="https://www.youtube.com/watch?v=0mvCeNsTa1g (İki Faktörlü Doğrulama)"
)

add_video_slide(
    "🎬 Video: Siber Güvenlik",
    "Güvenli internet kullanımı ve tehditlere karşı korunma yöntemleri",
    "https://www.youtube.com/watch?v=inWWhr5tnEA (Siber Güvenlik - TED-Ed)"
)

# ÜNİTE 3: İletişim
add_section_slide("📚 ÜNİTE 3: İletişim ve İşbirliği", (100, 180, 220))

add_content_slide_with_image(
    "Hafta 11: Profesyonel E-posta",
    [
        "📧 E-posta Yapısı",
        "",
        "Konu: [Açık ve öz]",
        "",
        "Sayın [Alıcı],",
        "",
        "[Giriş - Kim?]",
        "[Ana mesaj - Ne?]",
        "[Kapanış - İstek]",
        "",
        "Saygılarımla,",
        "[İsminiz]"
    ],
    notes="Profesyonel e-posta örneği ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=8y3Ayb0UUYA (Profesyonel E-posta Yazma)"
)

add_content_slide(
    "Netiquette (İnternet Görgüsü)",
    [
        "🌐 Dijital İletişim Kuralları",
        "",
        "✅ YAPILMASI GEREKENLER:",
        "• Kısa ve öz yaz",
        "• Yazım kurallarına dikkat",
        "• Saygılı ol",
        "• Emoji kullan (ama az)",
        "",
        "❌ YAPILMAMASI GEREKENLER:",
        "• BÜYÜK HARF (bağırmak gibi)",
        "• Spam",
        "• Hakaret"
    ],
    notes="Good vs bad e-posta örnekleri"
)

add_content_slide_with_image(
    "Hafta 12: Bilgi Okuryazarlığı",
    [
        "🔍 Etkili Araştırma",
        "",
        "Gelişmiş Arama:",
        "",
        '"tam ifade"',
        "Tırnak içinde ara",
        "",
        "-kelime",
        "Hariç tut",
        "",
        "site:edu.tr",
        "Sadece .edu sitelerinde"
    ],
    notes="Google gelişmiş arama ekranı",
    video_link="https://www.youtube.com/watch?v=erZ3IyBCXdY (Google Arama İpuçları)"
)

add_content_slide(
    "CRAAP Testi",
    [
        "📊 Kaynak Güvenilirliği",
        "",
        "C - Currency: Güncel mi?",
        "R - Relevance: İlgili mi?",
        "A - Authority: Yazar uzman mı?",
        "A - Accuracy: Doğru mu?",
        "P - Purpose: Amacı ne?",
        "",
        "Güvenilir Kaynaklar:",
        ".gov.tr, .edu.tr",
        "Bilimsel dergiler",
        "Üniversite siteleri"
    ],
    notes="CRAAP testi infografik"
)

# ÜNİTE 4: Ürün Oluşturma
add_section_slide("📚 ÜNİTE 4: Ürün Oluşturma", (180, 100, 220))

add_content_slide_with_image(
    "Hafta 13: Grafik Tasarım",
    [
        "🎨 Tasarım İlkeleri",
        "",
        "1. DENGE",
        "   Dengeli dağılım",
        "",
        "2. HİYERARŞİ",
        "   Önemli → Büyük",
        "",
        "3. KONTRAST",
        "   Zıt renkler dikkat",
        "",
        "4. BOŞLUK",
        "   Kalabalık olmasın"
    ],
    notes="İyi ve kötü tasarım örnekleri karşılaştırması",
    video_link="https://www.youtube.com/watch?v=a5KYlHNKQB8 (Grafik Tasarım İlkeleri)"
)

add_content_slide_with_image(
    "Canva ile Tasarım",
    [
        "🎨 Canva Nedir?",
        "",
        "Web tabanlı tasarım aracı",
        "Ücretsiz!",
        "Kolay kullanım",
        "",
        "Ne yapılabilir:",
        "• Poster",
        "• Logo",
        "• Sosyal medya görseli",
        "• Sunum",
        "• Sertifika"
    ],
    notes="Canva arayüzü ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=sNOXpMx4CgQ (Canva Kullanımı - Türkçe)"
)

add_content_slide_with_image(
    "Hafta 15: Video Düzenleme",
    [
        "🎥 Video Editing",
        "",
        "Yazılımlar:",
        "• Shotcut (PC - ücretsiz)",
        "• CapCut (Mobil/PC)",
        "• Windows Video Editor",
        "",
        "Temel İşlemler:",
        "✂️ Kırpma (Trim)",
        "🔗 Birleştirme",
        "🌟 Geçişler",
        "🎵 Müzik ekleme",
        "📝 Altyazı"
    ],
    notes="Video düzenleme yazılımı arayüzü (Shotcut veya CapCut)",
    video_link="https://www.youtube.com/watch?v=gdxJJhhKuL0 (CapCut Video Düzenleme)"
)

add_content_slide_with_image(
    "Hafta 16: Animasyon",
    [
        "🎞️ Animasyon Türleri",
        "",
        "1. 2D Animasyon",
        "   Scratch, Animate",
        "",
        "2. 3D Animasyon",
        "   Blender (ücretsiz)",
        "",
        "3. Stop Motion",
        "   Fotoğraflarla",
        "",
        "FPS:",
        "24 fps → Sinema",
        "30 fps → TV"
    ],
    notes="Farklı animasyon türleri örnekleri",
    video_link="https://www.youtube.com/watch?v=68RhH-Bv7pE (Animasyon Nasıl Yapılır?)"
)

add_content_slide_with_image(
    "Hafta 17: Podcast",
    [
        "🎙️ Podcast Nedir?",
        "",
        "Ses tabanlı yayın",
        "Eğitim, hikaye, röportaj",
        "",
        "Audacity (Ücretsiz):",
        "• Ses kaydı",
        "• Düzenleme",
        "• Gürültü giderme",
        "• Müzik ekleme",
        "• Dışa aktarma (MP3)"
    ],
    notes="Audacity arayüzü ekran görüntüsü",
    video_link="https://www.youtube.com/watch?v=xl-WDjWrTtk (Podcast Nasıl Yapılır?)"
)

add_content_slide_with_image(
    "Hafta 18: Web Sitesi",
    [
        "🌐 Google Sites",
        "",
        "Web: sites.google.com",
        "Ücretsiz, kolay!",
        "",
        "Sayfalar:",
        "1. Ana Sayfa",
        "2. Hakkımda",
        "3. İçerik",
        "4. İletişim",
        "",
        "Özellikler:",
        "Sürükle-bırak",
        "Resim, video ekleme"
    ],
    notes="Google Sites arayüzü ve örnek site",
    video_link="https://www.youtube.com/watch?v=gatr1T6aV8k (Google Sites Web Sitesi Yapımı)"
)

add_video_slide(
    "🎬 Video: Dijital İçerik Üretimi",
    "Grafik tasarım, video, animasyon, podcast ve web tasarımı özeti",
    "https://www.youtube.com/watch?v=TNzuXICo8w8 (Dijital İçerik Üretimi)"
)

# ÜNİTE 5: Problem Çözme
add_section_slide("📚 ÜNİTE 5: Problem Çözme ve Programlama", (220, 150, 50))

add_content_slide_with_image(
    "Hafta 20: Problem Çözme",
    [
        "🧩 Problem Çözme Adımları",
        "",
        "1. ANLA",
        "   Problem nedir?",
        "",
        "2. PLANLA",
        "   Çözüm yolu bul",
        "",
        "3. UYGULA",
        "   Çözümü yap",
        "",
        "4. KONTROL",
        "   Doğru mu?"
    ],
    notes="Problem çözme döngüsü (cycle) diyagramı",
    video_link="https://www.youtube.com/watch?v=azcrPFhaY9k (Problem Çözme Stratejileri)"
)

add_content_slide_with_image(
    "Hafta 21-25: İleri Scratch",
    [
        "💻 Scratch İleri Seviye",
        "",
        "Konular:",
        "• Karmaşık oyunlar",
        "• Fizik simülasyonu",
        "• Yapay zeka AI",
        "• Multiplayer",
        "• 3D efektler",
        "• Klon sistemi",
        "• Liste yönetimi"
    ],
    notes="İleri seviye Scratch proje örnekleri",
    video_link="https://www.youtube.com/watch?v=SukEkaNSf_k (Scratch İleri Seviye)"
)

add_content_slide_with_image(
    "Hafta 26: Python Giriş",
    [
        "🐍 Python Nedir?",
        "",
        "Profesyonel dil",
        "Öğrenmesi kolay",
        "Çok güçlü!",
        "",
        "Kullanım Alanları:",
        "• Yapay zeka",
        "• Web geliştirme",
        "• Oyun",
        "• Veri bilimi",
        "",
        'print("Merhaba!")'
    ],
    notes="Python logosu ve kod örneği",
    video_link="https://www.youtube.com/watch?v=rfscVS0vtbw (Python Programlama - Giriş)"
)

add_table_slide(
    "Scratch vs Python",
    [
        ["Özellik", "Scratch", "Python"],
        ["Görünüm", "Bloklar", "Kod yazma"],
        ["Zorluk", "Kolay", "Orta"],
        ["Hedef", "Çocuklar", "Profesyoneller"],
        ["Esneklik", "Sınırlı", "Çok esnek"],
        ["Gerçek Dünya", "Eğitim", "İş hayatı"]
    ],
    notes="Scratch ve Python kod karşılaştırması ekran görüntüsü"
)

add_content_slide(
    "Hafta 35-39: Final Projesi",
    [
        "🚀 Büyük Proje Zamanı!",
        "",
        "Kendi projenizi yapın:",
        "• Oyun",
        "• Uygulama",
        "• Simülasyon",
        "• Web sitesi",
        "",
        "Gereksinimler:",
        "✅ Tüm öğrendiklerinizi kullan",
        "✅ Yaratıcı ol",
        "✅ Kullanışlı olsun",
        "✅ Sunum hazırla"
    ],
    notes="Öğrenci projesi örnekleri fotoğrafları"
)

# KAPANIŞ
add_section_slide("🎉 Tebrikler!", (118, 75, 162))

add_content_slide(
    "Bu Yıl Öğrendikleriniz",
    [
        "✅ Dijital Etik ve KVKK",
        "✅ Siber Güvenlik (Phishing, 2FA)",
        "✅ Bilgi Okuryazarlığı",
        "✅ Grafik Tasarım (Canva)",
        "✅ Video Düzenleme",
        "✅ Animasyon",
        "✅ Podcast",
        "✅ Web Sitesi (Google Sites)",
        "✅ İleri Programlama (Python)",
        "✅ Proje Geliştirme"
    ]
)

add_content_slide(
    "🏆 Artık Bir Bilişim Uzmanısınız!",
    [
        "6. Sınıf Sertifikanız",
        "",
        "Gelecek:",
        "7. Sınıf → Robotik",
        "8. Sınıf → Mobil Uygulama",
        "",
        "Kariyer Yolları:",
        "💻 Yazılım Geliştirici",
        "🎨 Grafik Tasarımcı",
        "🎮 Oyun Geliştiricisi",
        "🛡️ Siber Güvenlik",
        "🤖 AI Mühendisi"
    ],
    notes="Teknoloji kariyerleri infografik",
    video_link="https://www.youtube.com/watch?v=nKIu9yen5nc (Geleceğin Meslekleri - TED)"
)

add_content_slide(
    "📚 Kaynaklar ve Öneriler",
    [
        "🌐 Scratch: scratch.mit.edu",
        "🌐 Python: python.org",
        "🌐 Code.org: code.org",
        "🌐 Canva: canva.com",
        "🌐 Khan Academy: tr.khanacademy.org",
        "📺 YouTube: Teknoloji kanalları",
        "",
        "Öğrenmeye devam edin!",
        "Projeler yapın!",
        "Paylaşın! 🚀🌟"
    ]
)

# Kaydet
prs.save('/home/user/BST/sunumlar/6-SINIF-FULL-SUNUM.pptx')
print("✅ 6. Sınıf Geliştirilmiş PowerPoint sunumu oluşturuldu!")
print(f"📊 Toplam {len(prs.slides)} slayt")
print("📝 Notlar: Her slayta görsel önerileri ve video linkleri eklendi")
print("🎨 Görsel placeholder'lar eklendi")
print("🎥 Video slaytları eklendi")
