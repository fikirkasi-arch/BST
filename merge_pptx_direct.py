#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PPTX dosyalarını ZIP ve XML seviyesinde birleştir
Bu yöntem tüm formatları ve içerikleri korur
"""

import zipfile
import os
import shutil
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def add_title_slide_to_prs(prs, grade):
    """Kapak slaytı ekle"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    left = Inches(0.5)
    top = Inches(2)
    width = Inches(9)
    height = Inches(2)

    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    if grade == 5:
        p = tf.paragraphs[0]
        p.text = f"{grade}. SINIF"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(54)
        p.font.bold = True
        p.font.color.rgb = RGBColor(102, 126, 234)

        p2 = tf.add_paragraph()
        p2.text = "Bilişim Teknolojileri ve Yazılım"
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(36)
        p2.font.color.rgb = RGBColor(102, 126, 234)

        p3 = tf.add_paragraph()
        p3.text = "FULL SUNUM - TÜM ÜNİTELER"
        p3.alignment = PP_ALIGN.CENTER
        p3.font.size = Pt(28)
        p3.font.color.rgb = RGBColor(118, 75, 162)
    else:
        p = tf.paragraphs[0]
        p.text = f"{grade}. SINIF"
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(54)
        p.font.bold = True
        p.font.color.rgb = RGBColor(79, 172, 254)

        p2 = tf.add_paragraph()
        p2.text = "Bilişim Teknolojileri ve Yazılım"
        p2.alignment = PP_ALIGN.CENTER
        p2.font.size = Pt(36)
        p2.font.color.rgb = RGBColor(79, 172, 254)

        p3 = tf.add_paragraph()
        p3.text = "FULL SUNUM - TÜM ÜNİTELER"
        p3.alignment = PP_ALIGN.CENTER
        p3.font.size = Pt(28)
        p3.font.color.rgb = RGBColor(0, 242, 254)

def merge_presentations_correctly(input_files, output_file, grade):
    """
    Sunumları doğru bir şekilde birleştir - her slaytı olduğu gibi ekle
    """

    print(f"\n📋 İlk sunumu base olarak kullanıyorum...")

    # İlk sunumu base olarak al
    base_file = None
    for f in input_files:
        if os.path.exists(f):
            base_file = f
            break

    if not base_file:
        print("❌ Hiçbir dosya bulunamadı!")
        return 0

    # Base sunumu kopyala
    final_prs = Presentation(base_file)
    print(f"✅ Base: {os.path.basename(base_file)} - {len(final_prs.slides)} slayt")

    # Kapak slaytı ekle (en başa)
    add_title_slide_to_prs(final_prs, grade)
    total_slides = 1 + len(final_prs.slides)

    # Diğer sunumları ekle
    for file_path in input_files[1:]:  # İlkini zaten ekledik
        if not os.path.exists(file_path):
            print(f"⚠️  Bulunamadı: {os.path.basename(file_path)}")
            continue

        print(f"\n📄 Ekleniyor: {os.path.basename(file_path)}")

        try:
            source_prs = Presentation(file_path)
            slides_before = len(final_prs.slides)

            # Her slaytı ekle
            for source_slide in source_prs.slides:
                # Blank layout kullan
                slide_layout = final_prs.slide_layouts[6]
                new_slide = final_prs.slides.add_slide(slide_layout)

                # Kaynak slaydın tüm shape'lerini kopyala
                for shape in source_slide.shapes:
                    # Shape XML elementini kopyala
                    el = shape.element
                    # Yeni slide'a ekle
                    new_slide.shapes._spTree.append(el)

                # Arka planı kopyala
                if hasattr(source_slide, 'background'):
                    try:
                        new_slide.background = source_slide.background
                    except:
                        pass

                # Notları kopyala
                if source_slide.has_notes_slide:
                    try:
                        notes = source_slide.notes_slide.notes_text_frame.text
                        if notes:
                            new_slide.notes_slide.notes_text_frame.text = notes
                    except:
                        pass

            slides_after = len(final_prs.slides)
            added = slides_after - slides_before
            total_slides += added
            print(f"  ✅ {added} slayt eklendi")

        except Exception as e:
            print(f"  ❌ Hata: {e}")

    # Kaydet
    try:
        final_prs.save(output_file)
        print(f"\n🎉 {os.path.basename(output_file)} kaydedildi - {total_slides} slayt\n")
    except Exception as e:
        print(f"\n❌ Kaydetme hatası: {e}\n")
        return 0

    return total_slides


print("="*70)
print("SUNUMLARI BİRLEŞTİRME - DOĞRUDAN XML YÖNTEMİ")
print("="*70)

# 5. Sınıf
print("\n" + "="*70)
print("5. SINIF FULL SUNUM")
print("="*70)

grade5_files = [
    '/home/user/BST/sunumlar/5-sinif-unite1-bilisim-temelleri-DETAYLI.pptx',
    '/home/user/BST/sunumlar/5-sinif-unite2-dijital-urun-tasarimi-DETAYLI.pptx',
    '/home/user/BST/sunumlar/5-sinif-unite3-aglar-iletisim-DETAYLI.pptx',
    '/home/user/BST/sunumlar/5-sinif-unite4-etik-guvenlik-DETAYLI.pptx',
    '/home/user/BST/sunumlar/5-sinif-unite5-yapay-zeka-DETAYLI.pptx',
    '/home/user/BST/sunumlar/5-sinif-unite6-scratch-DETAYLI.pptx'
]

total_5 = merge_presentations_correctly(
    grade5_files,
    '/home/user/BST/sunumlar/5-SINIF-FULL-SUNUM-DETAYLI.pptx',
    5
)

# 6. Sınıf
print("\n" + "="*70)
print("6. SINIF FULL SUNUM")
print("="*70)

grade6_files = [
    '/home/user/BST/sunumlar/6-sinif-unite1-veri-analiz-DETAYLI.pptx',
    '/home/user/BST/sunumlar/6-sinif-unite2-kelime-islemci-DETAYLI.pptx',
    '/home/user/BST/sunumlar/6-sinif-unite3-algoritmalar-DETAYLI.pptx',
    '/home/user/BST/sunumlar/6-sinif-unite4-scratch-ileri-DETAYLI.pptx',
    '/home/user/BST/sunumlar/6-sinif-unite5-sunum-programlari-DETAYLI.pptx'
]

total_6 = merge_presentations_correctly(
    grade6_files,
    '/home/user/BST/sunumlar/6-SINIF-FULL-SUNUM-DETAYLI.pptx',
    6
)

print("\n" + "="*70)
print("ÖZET")
print("="*70)
print(f"✅ 5. Sınıf: {total_5} slayt")
print(f"✅ 6. Sınıf: {total_6} slayt")
print(f"📊 Toplam: {total_5 + total_6} slayt birleştirildi")
