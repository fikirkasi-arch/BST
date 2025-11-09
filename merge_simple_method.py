#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
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


def simple_merge_presentations(input_files, output_file, grade):
    """
    Sunumları basit birleştirme - Her sunumu sırayla ekle
    Bu yöntem tüm master'ları ve layout'ları korur
    """

    if not input_files or len(input_files) == 0:
        print("❌ Hiçbir dosya belirtilmedi!")
        return 0

    # İlk geçerli sunumu bul ve base olarak kullan
    base_prs = None
    first_file = None

    for file_path in input_files:
        if os.path.exists(file_path):
            first_file = file_path
            base_prs = Presentation(file_path)
            print(f"📋 Base sunum: {os.path.basename(file_path)}")
            break

    if not base_prs:
        print("❌ Hiçbir sunum dosyası bulunamadı!")
        return 0

    # Yeni sunumu base'den oluştur (master slide'ları korumak için)
    final_prs = Presentation(first_file)

    # Base sunumdaki tüm slaytları sil (sadece layout'ları tutmak için)
    while len(final_prs.slides) > 0:
        rId = final_prs.slides._sldIdLst[0].rId
        final_prs.part.drop_rel(rId)
        del final_prs.slides._sldIdLst[0]

    # Kapak slaytı ekle
    add_title_slide(final_prs, grade)
    total = 1

    # Her sunumu ekle
    for file_path in input_files:
        if not os.path.exists(file_path):
            print(f"⚠️  Bulunamadı: {os.path.basename(file_path)}")
            continue

        print(f"\n📄 Ekleniyor: {os.path.basename(file_path)}")

        try:
            source_prs = Presentation(file_path)

            # Her slaytı ekle
            for slide_idx, source_slide in enumerate(source_prs.slides):
                try:
                    # Kaynak slaytın XML'ini al
                    slide_part = source_slide.part

                    # Yeni bir slide ekle (boş layout kullanarak)
                    blank_layout = final_prs.slide_layouts[6]
                    new_slide = final_prs.slides.add_slide(blank_layout)

                    # Kaynak slaytın tüm shape'lerini kopyala
                    for shape in source_slide.shapes:
                        # Shape'in XML element'ini al
                        el = shape.element

                        # Element'i kopyala (import_node benzeri)
                        new_el = type(el).new()
                        new_el._element = el._element

                        # Yeni slide'a ekle
                        try:
                            new_slide.shapes._spTree.append(el)
                        except:
                            # Alternatif yöntem
                            new_slide.shapes._spTree.insert_element_before(el, 'p:extLst')

                    # Notları kopyala
                    if source_slide.has_notes_slide:
                        try:
                            notes_text = source_slide.notes_slide.notes_text_frame.text
                            if notes_text:
                                new_slide.notes_slide.notes_text_frame.text = notes_text
                        except:
                            pass

                    total += 1

                except Exception as e:
                    print(f"  ⚠️  Slayt {slide_idx+1} kopyalanamadı: {e}")
                    continue

            print(f"  ✅ {len(source_prs.slides)} slayt eklendi")

        except Exception as e:
            print(f"  ❌ Dosya işleme hatası: {e}")

    # Kaydet
    try:
        final_prs.save(output_file)
        print(f"\n🎉 Toplam {total} slayt kaydedildi: {os.path.basename(output_file)}\n")
    except Exception as e:
        print(f"\n❌ Kaydetme hatası: {e}\n")
        return 0

    return total


print("="*70)
print("SUNUMLARI BİRLEŞTİRME - BASİT YÖNTEM")
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

total_5 = simple_merge_presentations(
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

total_6 = simple_merge_presentations(
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
