#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import random

# Weekly content JSON'u oku
with open('/home/user/BST/weekly_content.json', 'r', encoding='utf-8') as f:
    weekly_data = json.load(f)

# Çalışma sayfası dizinini oluştur
os.makedirs('/home/user/BST/haftalik-calisma-sayfalari', exist_ok=True)

def create_matching_worksheet(week_info):
    """Eşleştirme çalışma sayfası"""
    grade = week_info['grade']
    week = week_info['week']
    topic = week_info['topic']

    # Konuya göre eşleştirme öğeleri
    if 'donan' in topic.lower() or 'bilgisayar' in topic.lower():
        items = [
            ('CPU', 'İşlemci'),
            ('RAM', 'Geçici bellek'),
            ('Hard Disk', 'Kalıcı depolama'),
            ('Klavye', 'Giriş aygıtı'),
            ('Ekran', 'Çıkış aygıtı'),
            ('Fare', 'İşaret aygıtı')
        ]
    elif 'ağ' in topic.lower() or 'internet' in topic.lower():
        items = [
            ('LAN', 'Yerel alan ağı'),
            ('WAN', 'Geniş alan ağı'),
            ('Router', 'Yönlendirici'),
            ('Modem', 'Bağlantı cihazı'),
            ('Wi-Fi', 'Kablosuz ağ'),
            ('IP Adresi', 'Cihaz kimliği')
        ]
    elif 'güvenlik' in topic.lower() or 'şifre' in topic.lower():
        items = [
            ('Phishing', 'Kimlik avı'),
            ('Virüs', 'Zararlı yazılım'),
            ('Firewall', 'Güvenlik duvarı'),
            ('Şifre', 'Giriş parolası'),
            ('KVKK', 'Veri koruma'),
            ('Telif', 'Fikri hakkı')
        ]
    elif 'scratch' in topic.lower() or 'kod' in topic.lower():
        items = [
            ('Sprite', 'Karakter'),
            ('Sahne', 'Arka plan'),
            ('Döngü', 'Tekrar'),
            ('Koşul', 'Karar'),
            ('Değişken', 'Veri saklama'),
            ('Blok', 'Komut')
        ]
    elif 'yapay zeka' in topic.lower():
        items = [
            ('AI', 'Yapay Zeka'),
            ('Chatbot', 'Sohbet robotu'),
            ('Ses Tanıma', 'Siri, Alexa'),
            ('Yüz Tanıma', 'Görüntü tanıma'),
            ('Öneri Sistemi', 'Netflix'),
            ('Makine Öğr.', 'Veriden öğrenme')
        ]
    else:
        items = [
            ('Dosya', 'Bilgi saklama'),
            ('Klasör', 'Dosya grubu'),
            ('Kaydet', 'Sakla'),
            ('Aç', 'Yükle'),
            ('Kopyala', 'Çoğalt'),
            ('Sil', 'Kaldır')
        ]

    # Sol ve sağ kısımları karıştır
    left_items = [item[0] for item in items]
    right_items = [item[1] for item in items]
    random.shuffle(right_items)

    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{grade}. Sınıf - Hafta {week} - Eşleştirme Çalışması</title>
    <style>
        @media print {{
            body {{
                margin: 0;
                padding: 20px;
            }}
            .no-print {{
                display: none !important;
            }}
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 30px;
            background: white;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }}

        .header h1 {{
            color: #667eea;
            margin-bottom: 10px;
        }}

        .badges {{
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 15px 0;
        }}

        .badge {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}

        .instructions {{
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }}

        .matching-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
        }}

        .column h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}

        .item {{
            padding: 12px;
            margin-bottom: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: white;
        }}

        .item-number {{
            display: inline-block;
            width: 30px;
            height: 30px;
            background: #667eea;
            color: white;
            text-align: center;
            line-height: 30px;
            border-radius: 50%;
            margin-right: 10px;
            font-weight: bold;
        }}

        .answer-box {{
            display: inline-block;
            width: 30px;
            height: 30px;
            border: 2px solid #667eea;
            border-radius: 5px;
            margin-left: 10px;
            background: white;
        }}

        .student-info {{
            margin: 30px 0;
            padding: 20px;
            border: 2px dashed #667eea;
            border-radius: 10px;
        }}

        .info-row {{
            margin: 10px 0;
            display: flex;
            align-items: center;
        }}

        .info-label {{
            font-weight: bold;
            margin-right: 10px;
            min-width: 80px;
        }}

        .info-line {{
            flex: 1;
            border-bottom: 1px solid #333;
            height: 1px;
            margin-left: 10px;
        }}

        .controls {{
            text-align: center;
            margin: 30px 0;
        }}

        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            cursor: pointer;
            margin: 0 10px;
            font-weight: bold;
        }}

        button:hover {{
            transform: scale(1.05);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📝 Eşleştirme Çalışma Sayfası</h1>
        <div class="badges">
            <span class="badge">{grade}. SINIF</span>
            <span class="badge">HAFTA {week}</span>
            <span class="badge">EŞLEŞTİRME</span>
        </div>
        <p style="margin-top: 10px; color: #666;">{topic}</p>
    </div>

    <div class="student-info">
        <div class="info-row">
            <span class="info-label">Adı Soyadı:</span>
            <span class="info-line"></span>
        </div>
        <div class="info-row">
            <span class="info-label">Sınıfı:</span>
            <span class="info-line"></span>
        </div>
        <div class="info-row">
            <span class="info-label">Numarası:</span>
            <span class="info-line"></span>
        </div>
    </div>

    <div class="instructions">
        <strong>📌 Yönerge:</strong> Sol sütundaki kavramları, sağ sütundaki açıklamalarla eşleştirin. Doğru eşleştirme numarasını kutucuklara yazın.
    </div>

    <div class="matching-container">
        <div class="column">
            <h3>Kavramlar</h3>
            {''.join([f'<div class="item"><span class="item-number">{i+1}</span>{item}</div>' for i, item in enumerate(left_items)])}
        </div>
        <div class="column">
            <h3>Açıklamalar</h3>
            {''.join([f'<div class="item">{item}<span class="answer-box"></span></div>' for item in right_items])}
        </div>
    </div>

    <div class="controls no-print">
        <button onclick="window.print()">🖨️ Yazdır / PDF Kaydet</button>
        <button onclick="window.location.href='../index.html'">🏠 Ana Sayfa</button>
    </div>

    <div style="margin-top: 40px; padding: 15px; background: #f0f0f0; border-radius: 8px;">
        <strong>💯 Notlandırma:</strong> Doğru sayısı: _____ / {len(items)} &nbsp;&nbsp; Not: _____
    </div>
</body>
</html>'''

    return html

# Toplam sayfa sayacı
total_worksheets = 0

# Her hafta için çalışma sayfası oluştur
for grade_key in ['grade5', 'grade6']:
    grade_num = 5 if grade_key == 'grade5' else 6
    weeks = weekly_data[grade_key]

    for week_info in weeks:
        week_num = week_info['week']

        # Eşleştirme çalışma sayfası oluştur
        worksheet_html = create_matching_worksheet(week_info)

        filename = f'calisma-{grade_num}sinif-hafta{week_num}.html'
        filepath = f'/home/user/BST/haftalik-calisma-sayfalari/{filename}'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(worksheet_html)

        total_worksheets += 1
        print(f"✅ {grade_num}. Sınıf - Hafta {week_num} çalışma sayfası oluşturuldu")

print(f"\n🎉 Toplam {total_worksheets} çalışma sayfası oluşturuldu!")
print(f"📁 Klasör: /home/user/BST/haftalik-calisma-sayfalari/")
