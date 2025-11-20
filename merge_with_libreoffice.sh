#!/bin/bash

# LibreOffice kullanarak PowerPoint sunumlarını birleştir

SUNUMLAR_DIR="/home/user/BST/sunumlar"

echo "========================================="
echo "LibreOffice ile Sunum Birleştirme"
echo "========================================="

# 5. Sınıf sunumlarını birleştir
echo ""
echo "5. SINIF SUNUMLARINI BİRLEŞTİRİYOR..."
echo "========================================="

# Geçici klasör oluştur
TEMP_DIR=$(mktemp -d)
echo "Geçici klasör: $TEMP_DIR"

# 5. Sınıf sunumlarını kopyala
cp "$SUNUMLAR_DIR/5-sinif-unite1-bilisim-temelleri-DETAYLI.pptx" "$TEMP_DIR/01.pptx"
cp "$SUNUMLAR_DIR/5-sinif-unite2-dijital-urun-tasarimi-DETAYLI.pptx" "$TEMP_DIR/02.pptx"
cp "$SUNUMLAR_DIR/5-sinif-unite3-aglar-iletisim-DETAYLI.pptx" "$TEMP_DIR/03.pptx"
cp "$SUNUMLAR_DIR/5-sinif-unite4-etik-guvenlik-DETAYLI.pptx" "$TEMP_DIR/04.pptx"
cp "$SUNUMLAR_DIR/5-sinif-unite5-yapay-zeka-DETAYLI.pptx" "$TEMP_DIR/05.pptx"
cp "$SUNUMLAR_DIR/5-sinif-unite6-scratch-DETAYLI.pptx" "$TEMP_DIR/06.pptx"

echo "✅ 5. sınıf sunumları kopyalandı"

# Python-pptx kullanarak devam et (LibreOffice headless mode sunum birleştirmeyi desteklemiyor)
echo "⚠️  LibreOffice headless mode sunum birleştirmeyi desteklemiyor"
echo "Python-pptx ile alternatif yöntem kullanılacak"

# Temizlik
rm -rf "$TEMP_DIR"
