#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# JSON dosyasını oku
with open('/home/user/BST/weekly_content.json', 'r', encoding='utf-8') as f:
    weekly_data = json.load(f)

# JSON'u string olarak hazırla
json_string = json.dumps(weekly_data, ensure_ascii=False, indent=2)

# HTML dosyasını oku
with open('/home/user/BST/haftalik-icerik.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# JSON fetch kısmını bul ve değiştir
old_code = """    <script>
        let weeklyData = null;
        let currentGrade = null;

        // JSON verisini yükle
        fetch('weekly_content.json')
            .then(response => response.json())
            .then(data => {
                weeklyData = data;
                console.log('Haftalık içerikler yüklendi:', data);
            })
            .catch(error => {
                console.error('Veri yükleme hatası:', error);
                alert('İçerikler yüklenirken bir hata oluştu.');
            });"""

new_code = f"""    <script>
        // Haftalık içerik verisi (direkt gömülü)
        let weeklyData = {json_string};
        let currentGrade = null;

        console.log('Haftalık içerikler yüklendi:', weeklyData);"""

# Değiştir
html_content = html_content.replace(old_code, new_code)

# HTML dosyasını kaydet
with open('/home/user/BST/haftalik-icerik.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ JSON verisi HTML'e başarıyla gömüldü!")
print(f"📊 Toplam {len(weekly_data['grade5']) + len(weekly_data['grade6'])} haftalık veri eklendi")
