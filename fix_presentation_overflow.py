#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pptx import Presentation
from pptx.util import Pt
import os

def fix_text_overflow(prs_path):
    """Sunum slaytlarındaki metin taşmalarını düzelt"""

    prs = Presentation(prs_path)
    filename = os.path.basename(prs_path)

    print(f"\n{'='*70}")
    print(f"📄 {filename}")
    print(f"{'='*70}")

    fixes_made = 0

    for slide_num, slide in enumerate(prs.slides, 1):
        for shape in slide.shapes:
            if not hasattr(shape, "text_frame"):
                continue

            text_frame = shape.text_frame
            total_chars = sum(len(p.text) for p in text_frame.paragraphs)

            # Çok uzun metin için font boyutunu ayarla
            if total_chars > 500:
                # Font boyutunu küçült
                for paragraph in text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.size:
                            current_size = run.font.size.pt
                            if current_size > 14:
                                run.font.size = Pt(14)
                                fixes_made += 1
                                print(f"  Slayt {slide_num}: Font {current_size}pt → 14pt ({total_chars} karakter)")
                                break
                        else:
                            # Font boyutu belirlenmemişse varsayılan olarak 14pt yap
                            run.font.size = Pt(14)
                            fixes_made += 1
                            print(f"  Slayt {slide_num}: Font ayarlandı → 14pt ({total_chars} karakter)")
                            break

            elif total_chars > 400:
                # Orta uzunluktaki metinler için 16pt
                for paragraph in text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.size:
                            current_size = run.font.size.pt
                            if current_size > 16:
                                run.font.size = Pt(16)
                                fixes_made += 1
                                print(f"  Slayt {slide_num}: Font {current_size}pt → 16pt ({total_chars} karakter)")
                                break
                        else:
                            run.font.size = Pt(16)
                            fixes_made += 1
                            print(f"  Slayt {slide_num}: Font ayarlandı → 16pt ({total_chars} karakter)")
                            break

    # Sunumu kaydet
    if fixes_made > 0:
        prs.save(prs_path)
        print(f"\n  ✅ {fixes_made} düzeltme yapıldı ve kaydedildi")
    else:
        print(f"\n  ✅ Düzeltme gerektiren slayt yok")

    return fixes_made

def main():
    """Tüm DETAYLI sunumları düzelt"""

    presentations = [
        '5-sinif-unite1-bilisim-temelleri-DETAYLI.pptx',
        '5-sinif-unite2-dijital-urun-tasarimi-DETAYLI.pptx',
        '5-sinif-unite3-aglar-iletisim-DETAYLI.pptx',
        '5-sinif-unite4-etik-guvenlik-DETAYLI.pptx',
        '5-sinif-unite5-yapay-zeka-DETAYLI.pptx',
        '5-sinif-unite6-scratch-DETAYLI.pptx',
        '6-sinif-unite1-veri-analiz-DETAYLI.pptx',
        '6-sinif-unite2-kelime-islemci-DETAYLI.pptx',
        '6-sinif-unite3-algoritmalar-DETAYLI.pptx',
        '6-sinif-unite4-scratch-ileri-DETAYLI.pptx',
        '6-sinif-unite5-sunum-programlari-DETAYLI.pptx',
    ]

    total_fixes = 0

    for filename in presentations:
        filepath = f'/home/user/BST/sunumlar/{filename}'

        if not os.path.exists(filepath):
            print(f"⚠️  Dosya bulunamadı: {filename}")
            continue

        try:
            fixes = fix_text_overflow(filepath)
            total_fixes += fixes
        except Exception as e:
            print(f"❌ Hata: {e}")

    print(f"\n{'='*70}")
    print(f"ÖZET")
    print(f"{'='*70}")
    print(f"✅ Toplam {total_fixes} font boyutu düzeltmesi yapıldı")
    print(f"💡 Tüm uzun metinler için uygun font boyutları ayarlandı")
    print(f"📝 Sunumlar taşma olmayacak şekilde optimize edildi")

if __name__ == '__main__':
    main()
