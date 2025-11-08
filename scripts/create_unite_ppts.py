#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5. Sınıf Ünite 1: Bilişim Temelleri PowerPoint Sunumu
9 haftalık içerik
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

def add_title_slide(title, subtitle):
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title_shape = slide.shapes.title
    subtitle_shape = slide.placeholders[1]
    title_shape.text = title
    subtitle_shape.text = subtitle
    title_shape.text_frame.paragraphs[0].font.size = Pt(54)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(220, 100, 180)
    subtitle_shape.text_frame.paragraphs[0].font.size = Pt(32)
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 245, 250)
    return slide

def add_section_slide(title, color_rgb=(220, 100, 180)):
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

def add_content_slide(title, content_items):
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title_shape = slide.shapes.title
    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(40)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(220, 100, 180)
    body_shape = slide.placeholders[1]
    tf = body_shape.text_frame
    tf.clear()
    for item in content_items:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(24)
        p.space_before = Pt(6)
    return slide

# Kapak
add_title_slide(
    "ÜNİTE 1: BİLİŞİM TEMELLERİ",
    "5. Sınıf - 9 Haftalık İçerik"
)

add_section_slide("📚 Hafta 1: Bilgisayar ve Bileşenleri", (220, 100, 180))

add_content_slide(
    "Bilgisayar Nedir?",
    [
        "💻 Veri işleyen elektronik cihaz",
        "Giriş → İşlem → Çıkış",
        "",
        "Donanım Bileşenleri:",
        "• Kasa (Tower)",
        "• Ekran (Monitor)",
        "• Klavye",
        "• Mouse"
    ]
)

add_content_slide(
    "İç Donanım",
    [
        "🧠 İşlemci (CPU) - Bilgisayarın beyni",
        "💾 RAM - Geçici hızlı bellek",
        "💿 Harddisk/SSD - Kalıcı depolama",
        "🎮 Ekran Kartı - Görüntü işleme",
        "🔌 Anakart - Tüm parçaları birleştirir"
    ]
)

add_section_slide("📚 Hafta 2: İşletim Sistemleri", (180, 120, 200))

add_content_slide(
    "İşletim Sistemi Nedir?",
    [
        "Donanım ve yazılım arasındaki köprü",
        "Bilgisayarı yöneten ana program",
        "",
        "Popüler İşletim Sistemleri:",
        "🪟 Windows - En yaygın",
        "🍎 macOS - Apple bilgisayarlar",
        "🐧 Linux - Açık kaynak",
        "📱 Android & iOS - Mobil"
    ]
)

add_section_slide("📚 Hafta 3: Dosya Yönetimi", (150, 180, 220))

add_content_slide(
    "Dosya ve Klasör",
    [
        "📁 Klasör: Dosyaları gruplar",
        "📄 Dosya: Bilgi saklayan birim",
        "",
        "Dosya Türleri:",
        "📝 .docx - Word belgesi",
        "📊 .xlsx - Excel tablosu",
        "🖼️ .jpg, .png - Resim",
        "🎬 .mp4, .avi - Video",
        "🎵 .mp3 - Müzik"
    ]
)

add_content_slide(
    "Dosya İsimlendirme",
    [
        "✅ DOĞRU:",
        "• Anlamlı isimler (matematik_odevi.docx)",
        "• Tarih ekle (2025-01-15_sunum.pptx)",
        "• Küçük harf kullan",
        "",
        "❌ YANLIŞ:",
        "• Özel karakterler (?, *, /)",
        "• Çok uzun isimler",
        "• Anlamsız isimler (asdasd.docx)"
    ]
)

# Daha fazla slayt ekle...
add_section_slide("📚 Hafta 4-5: Office Programları", (220, 180, 100))

add_content_slide(
    "Microsoft Office Nedir?",
    [
        "Ofis uygulamaları paketi",
        "",
        "Programlar:",
        "📝 Word - Belge oluşturma",
        "📊 Excel - Tablo ve hesaplamalar",
        "📺 PowerPoint - Sunumlar",
        "📧 Outlook - E-posta",
        "📔 OneNote - Not alma"
    ]
)

add_section_slide("🎉 Ünite 1 Tamamlandı!", (67, 142, 234))

add_content_slide(
    "Öğrendiklerimiz",
    [
        "✅ Bilgisayar bileşenleri",
        "✅ İşletim sistemleri",
        "✅ Dosya yönetimi",
        "✅ Office programları temelleri",
        "",
        "Bir sonraki ünite:",
        "🎨 Dijital Ürün Tasarımı"
    ]
)

prs.save('/home/user/BST/sunumlar/5-sinif-unite1-bilisim-temelleri.pptx')
print("✅ 5. Sınıf Ünite 1 sunumu oluşturuldu!")
print(f"📊 Toplam {len(prs.slides)} slayt")
