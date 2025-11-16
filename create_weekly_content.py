#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openpyxl
import json
import re

def sanitize_filename(text):
    """Türkçe karakterleri ve özel karakterleri temizle"""
    tr_map = {
        'ç': 'c', 'Ç': 'C', 'ğ': 'g', 'Ğ': 'G',
        'ı': 'i', 'İ': 'I', 'ö': 'o', 'Ö': 'O',
        'ş': 's', 'Ş': 'S', 'ü': 'u', 'Ü': 'U',
        '/': '-', '\\': '-', ':': '', '?': '', '*': '', '"': '', '<': '', '>': '', '|': ''
    }
    for tr, en in tr_map.items():
        text = text.replace(tr, en)
    text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower().replace(' ', '-')

def read_weekly_plans(excel_file, grade):
    """Excel dosyasından haftalık planları oku"""
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active

    weekly_data = []
    week_counter = 0

    # Satır 4'ten başla (header satırı 3)
    for row in ws.iter_rows(min_row=4, values_only=True):
        # Hafta bilgisi sütun 2'de (index 1)
        week_cell = row[1] if len(row) > 1 else None

        # Tatil veya boş satırları atla
        if not week_cell:
            continue

        week_text = str(week_cell).strip()

        # Tatil satırlarını atla
        if 'TATİL' in week_text.upper() or 'ARİFE' in week_text.upper():
            continue

        # Hafta numarasını bul
        if 'Hafta' in week_text or 'hafta' in week_text:
            week_counter += 1

            # Konu başlığı sütun 5'te (index 4)
            topic = row[4] if len(row) > 4 and row[4] else ""
            topic = str(topic).strip() if topic else ""

            # Ünite/Tema sütun 4'te (index 3)
            unit = row[3] if len(row) > 3 and row[3] else ""
            unit = str(unit).strip() if unit else ""

            # Öğrenme çıktıları sütun 6'da (index 5)
            outcome = row[5] if len(row) > 5 and row[5] else ""
            outcome = str(outcome).strip() if outcome else ""

            if topic or unit:
                weekly_data.append({
                    'week': week_counter,
                    'week_text': week_text,
                    'unit': unit,
                    'topic': topic,
                    'outcome': outcome,
                    'grade': grade
                })

    return weekly_data

# 5. ve 6. sınıf planlarını oku
print("📖 Yıllık planlar okunuyor...")
grade5_data = read_weekly_plans('/home/user/BST/2025-2026 BTY 5. Sınıflar Yeni Yıllık Plan.xlsx', 5)
grade6_data = read_weekly_plans('/home/user/BST/2025-2026 6. Sınıf BTY Yıllık Plan.xlsx', 6)

print(f"✅ 5. Sınıf: {len(grade5_data)} hafta")
print(f"✅ 6. Sınıf: {len(grade6_data)} hafta")

# JSON dosyasına kaydet
all_weeks = {
    'grade5': grade5_data,
    'grade6': grade6_data
}

with open('/home/user/BST/weekly_plans.json', 'w', encoding='utf-8') as f:
    json.dump(all_weeks, f, ensure_ascii=False, indent=2)

print("✅ Haftalık planlar weekly_plans.json dosyasına kaydedildi")
