#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from copy import deepcopy
import os

def add_title_slide(prs, grade):
    """Kapak slaytı ekle"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Başlık kutusu
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

    print(f"✅ Kapak slaytı eklendi")


def copy_slide_proper(source_prs, dest_prs, slide_index):
    """Bir slaytı tam içeriğiyle kopyala - geliştirilmiş yöntem"""
    try:
        source_slide = source_prs.slides[slide_index]

        # Kaynak slaytın layout'unu al
        source_layout = source_slide.slide_layout

        # Hedef sunumda aynı index'teki layout'u kullan (varsayılan olarak blank)
        try:
            dest_layout = dest_prs.slide_layouts[source_layout._element.get('type', 6)]
        except:
            dest_layout = dest_prs.slide_layouts[6]  # Blank layout

        # Yeni slayt oluştur
        dest_slide = dest_prs.slides.add_slide(dest_layout)

        # Tüm shape'leri kopyala
        for shape in source_slide.shapes:
            try:
                # XML elementini deep copy ile kopyala
                el = shape.element
                newel = deepcopy(el)
                dest_slide.shapes._spTree.insert_element_before(newel, 'p:extLst')
            except Exception as e:
                print(f"    ⚠️  Shape kopyalanamadı: {e}")
                continue

        # Notları kopyala
        try:
            if source_slide.has_notes_slide:
                notes_text = source_slide.notes_slide.notes_text_frame.text
                if notes_text:
                    dest_slide.notes_slide.notes_text_frame.text = notes_text
        except Exception as e:
            print(f"    ⚠️  Notlar kopyalanamadı: {e}")

        # Arka plan kopyala
        try:
            if source_slide.background:
                dest_slide.background.fill.solid()
        except:
            pass

        return True
    except Exception as e:
        print(f"    ❌ Slayt kopyalama hatası: {e}")
        return False


def merge_presentations(input_files, output_file, grade):
    """Sunumları birleştir - geliştirilmiş yöntem"""

    # İlk sunumu base olarak al (layout'ları korumak için)
    base_prs = None
    for file_path in input_files:
        if os.path.exists(file_path):
            base_prs = Presentation(file_path)
            print(f"📋 Base sunum: {os.path.basename(file_path)}")
            break

    if not base_prs:
        print("❌ Hiçbir sunum dosyası bulunamadı!")
        return 0

    # Yeni sunum oluştur (base'in layout'larını kullanarak)
    prs = Presentation()

    # Base'den layout'ları kopyala
    try:
        # Slide master'ı kopyala
        for master in base_prs.slide_master:
            prs.slide_master = master
    except:
        pass

    # Kapak ekle
    add_title_slide(prs, grade)
    total = 1

    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"⚠️  Bulunamadı: {os.path.basename(file_path)}")
            continue

        print(f"\n📄 Ekleniyor: {os.path.basename(file_path)}")

        try:
            source_prs = Presentation(file_path)
            slides_added = 0

            for i in range(len(source_prs.slides)):
                if copy_slide_proper(source_prs, prs, i):
                    total += 1
                    slides_added += 1
                else:
                    print(f"  ⚠️  Slayt {i+1} kopyalanamadı")

            print(f"  ✅ {slides_added}/{len(source_prs.slides)} slayt başarıyla eklendi")

        except Exception as e:
            print(f"  ❌ Dosya işleme hatası: {e}")

    # Kaydet
    try:
        prs.save(output_file)
        print(f"\n🎉 Toplam {total} slayt kaydedildi: {os.path.basename(output_file)}\n")
    except Exception as e:
        print(f"\n❌ Kaydetme hatası: {e}\n")
        return 0

    return total


print("="*70)
print("SUNUMLARI BİRLEŞTİRME - GELİŞTİRİLMİŞ YÖNTEM")
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

total_5 = merge_presentations(
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

total_6 = merge_presentations(
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
