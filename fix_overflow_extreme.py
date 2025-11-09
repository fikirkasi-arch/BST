#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pptx import Presentation
from pptx.util import Pt
import os

def fix_overflow_extreme(prs_path):
    """Taşmaları ekstrem şekilde düzelt - çok agresif yöntem"""

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

            if total_chars == 0:
                continue

            num_paragraphs = len([p for p in text_frame.paragraphs if p.text.strip()])

            # Her paragrafı optimize et
            for paragraph in text_frame.paragraphs:
                if not paragraph.text.strip():
                    continue

                # Line spacing - çok agresif
                if paragraph.line_spacing is None or paragraph.line_spacing > 0.85:
                    paragraph.line_spacing = 0.85
                    fixes_made += 1

                # Paragraf arası boşluk
                if paragraph.space_after is None or paragraph.space_after > Pt(2):
                    paragraph.space_after = Pt(2)
                    fixes_made += 1

                if paragraph.space_before is None or paragraph.space_before > Pt(2):
                    paragraph.space_before = Pt(2)
                    fixes_made += 1

                # Font boyutu - karakter sayısına göre
                for run in paragraph.runs:
                    if not run.text.strip():
                        continue

                    # Mevcut font boyutunu al
                    current_size = run.font.size.pt if run.font.size else 18

                    # Yeni font boyutu hesapla
                    new_size = current_size

                    if total_chars > 700:
                        new_size = min(current_size, 11)
                    elif total_chars > 600:
                        new_size = min(current_size, 12)
                    elif total_chars > 500:
                        new_size = min(current_size, 13)
                    elif total_chars > 400:
                        new_size = min(current_size, 14)
                    elif total_chars > 300:
                        new_size = min(current_size, 15)
                    elif total_chars > 200:
                        new_size = min(current_size, 16)

                    if new_size != current_size and new_size >= 11:
                        run.font.size = Pt(new_size)
                        fixes_made += 1

            # Text frame ayarları
            if not text_frame.word_wrap:
                text_frame.word_wrap = True
                fixes_made += 1

            # Margin'leri küçült
            try:
                text_frame.margin_top = Pt(2)
                text_frame.margin_bottom = Pt(2)
                text_frame.margin_left = Pt(5)
                text_frame.margin_right = Pt(5)
                fixes_made += 4
            except:
                pass

        if fixes_made > 0 and slide_num % 10 == 0:
            print(f"  ✅ {slide_num} slayt işlendi...")

    # Kaydet
    if fixes_made > 0:
        prs.save(prs_path)
        print(f"\n  💾 {fixes_made} düzeltme yapıldı ve kaydedildi")
    else:
        print(f"\n  ✅ Düzeltme gerektiren slayt yok")

    return fixes_made


def main():
    """Tüm DETAYLI sunumları ekstrem düzelt"""

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
    print("METİN TAŞMALARINI DÜZELTME - EKSTREM YÖNTEM")
    print("="*70)
    print("Font boyutları: 11-16pt arasına ayarlanacak")
    print("Line spacing: 0.85'e düşürülecek")
    print("Margin'ler minimal yapılacak")
    print("="*70)

    for filename in presentations:
        filepath = f'/home/user/BST/sunumlar/{filename}'

        if not os.path.exists(filepath):
            print(f"⚠️  Dosya bulunamadı: {filename}")
            continue

        try:
            fixes = fix_overflow_extreme(filepath)
            total_fixes += fixes
        except Exception as e:
            print(f"❌ Hata: {e}")

    print(f"\n{'='*70}")
    print(f"ÖZET")
    print(f"{'='*70}")
    print(f"✅ Toplam {total_fixes} ekstrem düzeltme yapıldı")
    print(f"")
    print(f"📝 UYGULANAN DÜZELTMELER:")
    print(f"  • Font boyutları 11-16pt arasına sıkıştırıldı")
    print(f"  • Line spacing 0.85'e düşürüldü")
    print(f"  • Paragraf boşlukları minimize edildi")
    print(f"  • Margin'ler minimal yapıldı (2-5pt)")
    print(f"  • Word wrap zorunlu etkinleştirildi")
    print(f"")
    print(f"🎯 SONUÇ:")
    print(f"  Artık HİÇBİR slaytda taşma olmamalı!")

if __name__ == '__main__':
    main()
