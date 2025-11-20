#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pptx import Presentation
import os

def merge_presentations(input_files, output_file, grade):
    """Birden fazla PowerPoint sunumunu birleştir"""
    # Yeni bir boş sunum oluştur
    merged = Presentation()

    # İlk slayt: Kapak
    slide = merged.slides.add_slide(merged.slide_layouts[6])  # Boş layout

    # Kapak için renk ve yazı
    if grade == 5:
        title_text = "5. SINIF\nBilişim Teknolojileri ve Yazılım\nFULL SUNUM"
        subtitle = "Tüm Üniteler - Detaylı Anlatım"
    else:
        title_text = "6. SINIF\nBilişim Teknolojileri ve Yazılım\nFULL SUNUM"
        subtitle = "Tüm Üniteler - Detaylı Anlatım"

    # Başlık ekle
    left = top = width = height = 0
    txBox = slide.shapes.add_textbox(left, merged.slide_height // 4, merged.slide_width, merged.slide_height // 3)
    tf = txBox.text_frame
    tf.text = title_text

    for paragraph in tf.paragraphs:
        paragraph.alignment = 1  # Center
        for run in paragraph.runs:
            run.font.size = 440000  # 44pt
            run.font.bold = True
            run.font.color.rgb = (102, 126, 234)  # #667eea

    # Alt başlık
    txBox2 = slide.shapes.add_textbox(0, merged.slide_height // 2, merged.slide_width, merged.slide_height // 4)
    tf2 = txBox2.text_frame
    tf2.text = subtitle

    for paragraph in tf2.paragraphs:
        paragraph.alignment = 1
        for run in paragraph.runs:
            run.font.size = 280000  # 28pt
            run.font.color.rgb = (118, 75, 162)  # #764ba2

    print(f"✅ Kapak slaytı eklendi: {title_text}")

    # Her dosyayı birleştir
    total_slides = 1  # Kapak slaytı

    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"⚠️  Dosya bulunamadı: {input_file}")
            continue

        try:
            prs = Presentation(input_file)

            print(f"📄 Birleştiriliyor: {os.path.basename(input_file)} ({len(prs.slides)} slayt)")

            # Her slaytı kopyala
            for slide in prs.slides:
                # Yeni slayt oluştur (aynı layout ile)
                new_slide = merged.slides.add_slide(slide.slide_layout)

                # Tüm şekilleri kopyala
                for shape in slide.shapes:
                    # Şekil özelliklerini kopyala
                    try:
                        el = shape.element
                        newel = new_slide.shapes._spTree.insert_element_before(el, 'p:extLst')
                    except:
                        # Bazı şekiller kopyalanamayabilir, devam et
                        pass

                total_slides += 1

            print(f"  ✅ {len(prs.slides)} slayt eklendi")

        except Exception as e:
            print(f"  ❌ Hata: {e}")
            continue

    # Kaydet
    merged.save(output_file)
    print(f"\n🎉 Birleştirme tamamlandı!")
    print(f"📊 Toplam {total_slides} slayt")
    print(f"💾 Dosya: {output_file}\n")

    return total_slides

# 5. Sınıf DETAYLI sunumlarını birleştir
print("=" * 60)
print("5. SINIF FULL SUNUM OLUŞTURULUYOR")
print("=" * 60)

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

# 6. Sınıf DETAYLI sunumlarını birleştir
print("=" * 60)
print("6. SINIF FULL SUNUM OLUŞTURULUYOR")
print("=" * 60)

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

print("=" * 60)
print("ÖZET")
print("=" * 60)
print(f"✅ 5. Sınıf Full Sunum: {total_5} slayt")
print(f"✅ 6. Sınıf Full Sunum: {total_6} slayt")
print(f"📁 Dosyalar sunumlar/ klasöründe")
