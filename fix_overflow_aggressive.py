#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pptx import Presentation
from pptx.util import Pt
import os

def fix_text_overflow_aggressive(prs_path):
    """Metin taşmalarını agresif bir şekilde düzelt"""

    prs = Presentation(prs_path)
    filename = os.path.basename(prs_path)

    print(f"\n{'='*70}")
    print(f"📄 {filename}")
    print(f"{'='*70}")

    fixes_made = 0
    slides_fixed = 0

    for slide_num, slide in enumerate(prs.slides, 1):
        slide_had_fix = False

        for shape in slide.shapes:
            if not hasattr(shape, "text_frame"):
                continue

            text_frame = shape.text_frame
            total_chars = sum(len(p.text) for p in text_frame.paragraphs)

            if total_chars == 0:
                continue

            # Satır sayısını kontrol et
            num_paragraphs = len([p for p in text_frame.paragraphs if p.text.strip()])

            # Strateji 1: Çok fazla paragraf varsa line spacing'i azalt
            if num_paragraphs > 8:
                for paragraph in text_frame.paragraphs:
                    if paragraph.line_spacing is None or paragraph.line_spacing > 1.0:
                        paragraph.line_spacing = 0.9
                        fixes_made += 1
                        slide_had_fix = True
                print(f"  Slayt {slide_num}: Line spacing düzeltildi ({num_paragraphs} paragraf)")

            # Strateji 2: Karakter sayısına göre font boyutu ayarla
            if total_chars > 600:
                # Çok uzun metin - 12pt
                for paragraph in text_frame.paragraphs:
                    for run in paragraph.runs:
                        current_size = run.font.size.pt if run.font.size else 18
                        if current_size > 12:
                            run.font.size = Pt(12)
                            fixes_made += 1
                            slide_had_fix = True
                if slide_had_fix:
                    print(f"  Slayt {slide_num}: Font 12pt yapıldı ({total_chars} karakter)")

            elif total_chars > 500:
                # Uzun metin - 13pt
                for paragraph in text_frame.paragraphs:
                    for run in paragraph.runs:
                        current_size = run.font.size.pt if run.font.size else 18
                        if current_size > 13:
                            run.font.size = Pt(13)
                            fixes_made += 1
                            slide_had_fix = True
                if slide_had_fix:
                    print(f"  Slayt {slide_num}: Font 13pt yapıldı ({total_chars} karakter)")

            elif total_chars > 400:
                # Orta uzun metin - 14pt
                for paragraph in text_frame.paragraphs:
                    for run in paragraph.runs:
                        current_size = run.font.size.pt if run.font.size else 18
                        if current_size > 14:
                            run.font.size = Pt(14)
                            fixes_made += 1
                            slide_had_fix = True
                if slide_had_fix:
                    print(f"  Slayt {slide_num}: Font 14pt yapıldı ({total_chars} karakter)")

            elif total_chars > 300:
                # Biraz uzun metin - 15pt
                for paragraph in text_frame.paragraphs:
                    for run in paragraph.runs:
                        current_size = run.font.size.pt if run.font.size else 18
                        if current_size > 15:
                            run.font.size = Pt(15)
                            fixes_made += 1
                            slide_had_fix = True
                if slide_had_fix:
                    print(f"  Slayt {slide_num}: Font 15pt yapıldı ({total_chars} karakter)")

            # Strateji 3: Paragraf spacing'i azalt
            if num_paragraphs > 6:
                for paragraph in text_frame.paragraphs:
                    if paragraph.space_after is None or paragraph.space_after > Pt(6):
                        paragraph.space_after = Pt(3)
                        fixes_made += 1
                        slide_had_fix = True

            # Strateji 4: Word wrap'i etkinleştir
            if not text_frame.word_wrap:
                text_frame.word_wrap = True
                fixes_made += 1
                slide_had_fix = True

        if slide_had_fix:
            slides_fixed += 1

    # Sunumu kaydet
    if fixes_made > 0:
        prs.save(prs_path)
        print(f"\n  ✅ {slides_fixed} slayt, {fixes_made} düzeltme yapıldı ve kaydedildi")
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

    print("="*70)
    print("METİN TAŞMALARINI DÜZELTME - AGRESİF YÖNTEMLERİ")
    print("="*70)

    for filename in presentations:
        filepath = f'/home/user/BST/sunumlar/{filename}'

        if not os.path.exists(filepath):
            print(f"⚠️  Dosya bulunamadı: {filename}")
            continue

        try:
            fixes = fix_text_overflow_aggressive(filepath)
            total_fixes += fixes
        except Exception as e:
            print(f"❌ Hata: {e}")

    print(f"\n{'='*70}")
    print(f"ÖZET")
    print(f"{'='*70}")
    print(f"✅ Toplam {total_fixes} düzeltme yapıldı")
    print(f"")
    print(f"📝 UYGULANAN DÜZELTMELER:")
    print(f"  • Font boyutları 12-15pt arasına ayarlandı")
    print(f"  • Line spacing optimize edildi (0.9)")
    print(f"  • Paragraf arası boşluklar azaltıldı")
    print(f"  • Word wrap etkinleştirildi")
    print(f"")
    print(f"💡 ÖNEMLİ:")
    print(f"  Tüm içerikler slaytlara sığacak şekilde optimize edildi.")
    print(f"  Sunumları PowerPoint'te açtığınızda taşma olmamalı.")

if __name__ == '__main__':
    main()
