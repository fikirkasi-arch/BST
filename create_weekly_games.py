#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

# Weekly content JSON'u oku
with open('/home/user/BST/weekly_content.json', 'r', encoding='utf-8') as f:
    weekly_data = json.load(f)

# Oyun dizinini oluştur
os.makedirs('/home/user/BST/haftalik-oyunlar', exist_ok=True)

# Oyun şablonları
def create_matching_game(week_info):
    """Eşleştirme oyunu oluştur"""
    grade = week_info['grade']
    week = week_info['week']
    topic = week_info['topic']

    # Konuya göre eşleştirme öğeleri
    pairs = []
    if 'donan' in topic.lower() or 'bilgisayar' in topic.lower():
        pairs = [
            ('CPU', 'İşlemci - Bilgisayarın beyni'),
            ('RAM', 'Geçici bellek'),
            ('Hard Disk', 'Kalıcı depolama'),
            ('Klavye', 'Giriş aygıtı'),
            ('Monitör', 'Çıkış aygıtı'),
            ('Mouse', 'Fare - İşaret aygıtı')
        ]
    elif 'yazılım' in topic.lower() or 'işletim' in topic.lower():
        pairs = [
            ('Windows', 'İşletim sistemi'),
            ('Word', 'Kelime işlemci'),
            ('Paint', 'Çizim programı'),
            ('Browser', 'İnternet tarayıcı'),
            ('Antivir', 'Güvenlik yazılımı'),
            ('Excel', 'Hesap tablosu')
        ]
    elif 'ağ' in topic.lower() or 'internet' in topic.lower():
        pairs = [
            ('LAN', 'Yerel alan ağı'),
            ('WAN', 'Geniş alan ağı'),
            ('Router', 'Yönlendirici'),
            ('Modem', 'İnternet bağlantı cihazı'),
            ('Wi-Fi', 'Kablosuz ağ'),
            ('IP', 'İnternet protokol adresi')
        ]
    elif 'güvenlik' in topic.lower() or 'şifre' in topic.lower() or 'etik' in topic.lower():
        pairs = [
            ('Phishing', 'Kimlik avı'),
            ('Firewall', 'Güvenlik duvarı'),
            ('Şifre', 'Giriş parolası'),
            ('Virüs', 'Zararlı yazılım'),
            ('KVKK', 'Kişisel veri koruma'),
            ('Telif', 'Fikri mülkiyet hakkı')
        ]
    elif 'yapay zeka' in topic.lower() or 'ai' in topic.lower():
        pairs = [
            ('AI', 'Yapay Zeka'),
            ('Chatbot', 'Sohbet robotu'),
            ('Makine Öğrenmesi', 'Veriden öğrenme'),
            ('Ses Tanıma', 'Siri, Alexa'),
            ('Görüntü Tanıma', 'Yüz tanıma'),
            ('Öneri Sistemi', 'Netflix, YouTube')
        ]
    elif 'scratch' in topic.lower() or 'program' in topic.lower() or 'kod' in topic.lower():
        pairs = [
            ('Algoritma', 'Adım adım çözüm'),
            ('Değişken', 'Veri saklama'),
            ('Döngü', 'Tekrar eden kod'),
            ('Koşul', 'Karar yapısı'),
            ('Sprite', 'Karakter'),
            ('Sahne', 'Arka plan')
        ]
    elif 'word' in topic.lower() or 'kelime' in topic.lower():
        pairs = [
            ('Bold', 'Kalın yazı'),
            ('Italic', 'İtalik yazı'),
            ('Font', 'Yazı tipi'),
            ('Save', 'Kaydet'),
            ('Print', 'Yazdır'),
            ('Copy', 'Kopyala')
        ]
    elif 'veri' in topic.lower() or 'tablo' in topic.lower():
        pairs = [
            ('Hücre', 'Tablo gözü'),
            ('Satır', 'Yatay sıra'),
            ('Sütun', 'Dikey sıra'),
            ('Formül', 'Hesaplama'),
            ('Grafik', 'Görsel veri'),
            ('Filtre', 'Veri süzme')
        ]
    else:
        # Genel bilişim konuları
        pairs = [
            ('Dosya', 'Veri depolama'),
            ('Klasör', 'Dosya grubu'),
            ('Kaydet', 'Sakla'),
            ('Aç', 'Dosya yükle'),
            ('Kopyala', 'Çoğalt'),
            ('Sil', 'Kaldır')
        ]

    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{grade}. Sınıf - Hafta {week} - Eşleştirme Oyunu</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .header {{
            background: white;
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 800px;
        }}

        h1 {{
            color: #667eea;
            margin-bottom: 10px;
        }}

        .topic {{
            color: #666;
            font-size: 1.2em;
        }}

        .game-container {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            max-width: 900px;
            width: 100%;
        }}

        .score-board {{
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            gap: 20px;
        }}

        .score-item {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 15px;
            text-align: center;
            flex: 1;
        }}

        .score-number {{
            font-size: 2em;
            font-weight: bold;
        }}

        .game-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}

        .column {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .match-item {{
            padding: 20px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 1.1em;
            text-align: center;
            border: 3px solid transparent;
        }}

        .left-item {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}

        .right-item {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }}

        .match-item:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}

        .match-item.selected {{
            border-color: #ffd700;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
        }}

        .match-item.matched {{
            opacity: 0.5;
            cursor: not-allowed;
            background: #4CAF50 !important;
        }}

        .match-item.wrong {{
            animation: shake 0.5s;
            border-color: #f44336;
        }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-10px); }}
            75% {{ transform: translateX(10px); }}
        }}

        .message {{
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-size: 1.2em;
            font-weight: bold;
            display: none;
        }}

        .message.show {{
            display: block;
        }}

        .message.success {{
            background: #4CAF50;
            color: white;
        }}

        .message.error {{
            background: #f44336;
            color: white;
        }}

        .controls {{
            display: flex;
            gap: 15px;
            justify-content: center;
        }}

        button {{
            padding: 15px 40px;
            font-size: 1.1em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }}

        .reset-btn {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}

        .home-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}

        button:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}

        @media (max-width: 768px) {{
            .game-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎮 Eşleştirme Oyunu</h1>
        <p class="topic">{grade}. Sınıf - Hafta {week}: {topic}</p>
    </div>

    <div class="game-container">
        <div class="score-board">
            <div class="score-item">
                <div class="score-number" id="score">0</div>
                <div>Puan</div>
            </div>
            <div class="score-item">
                <div class="score-number" id="matched">0</div>
                <div>Eşleşme</div>
            </div>
            <div class="score-item">
                <div class="score-number" id="total">{len(pairs)}</div>
                <div>Toplam</div>
            </div>
        </div>

        <div class="message" id="message"></div>

        <div class="game-grid">
            <div class="column" id="left-column"></div>
            <div class="column" id="right-column"></div>
        </div>

        <div class="controls">
            <button class="reset-btn" onclick="resetGame()">🔄 Yeniden Başla</button>
            <button class="home-btn" onclick="goHome()">🏠 Ana Sayfa</button>
        </div>
    </div>

    <script>
        const pairs = {json.dumps([{'left': l, 'right': r, 'id': i} for i, (l, r) in enumerate(pairs)], ensure_ascii=False)};

        let selectedLeft = null;
        let selectedRight = null;
        let score = 0;
        let matchedCount = 0;

        function shuffleArray(array) {{
            for (let i = array.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }}
            return array;
        }}

        function initGame() {{
            const leftColumn = document.getElementById('left-column');
            const rightColumn = document.getElementById('right-column');

            const leftItems = shuffleArray([...pairs]);
            const rightItems = shuffleArray([...pairs]);

            leftColumn.innerHTML = '';
            rightColumn.innerHTML = '';

            leftItems.forEach(pair => {{
                const div = document.createElement('div');
                div.className = 'match-item left-item';
                div.textContent = pair.left;
                div.dataset.id = pair.id;
                div.onclick = () => selectLeft(div);
                leftColumn.appendChild(div);
            }});

            rightItems.forEach(pair => {{
                const div = document.createElement('div');
                div.className = 'match-item right-item';
                div.textContent = pair.right;
                div.dataset.id = pair.id;
                div.onclick = () => selectRight(div);
                rightColumn.appendChild(div);
            }});
        }}

        function selectLeft(element) {{
            if (element.classList.contains('matched')) return;

            document.querySelectorAll('.left-item').forEach(item => {{
                item.classList.remove('selected');
            }});

            element.classList.add('selected');
            selectedLeft = element;

            checkMatch();
        }}

        function selectRight(element) {{
            if (element.classList.contains('matched')) return;

            document.querySelectorAll('.right-item').forEach(item => {{
                item.classList.remove('selected');
            }});

            element.classList.add('selected');
            selectedRight = element;

            checkMatch();
        }}

        function checkMatch() {{
            if (!selectedLeft || !selectedRight) return;

            const leftId = selectedLeft.dataset.id;
            const rightId = selectedRight.dataset.id;

            if (leftId === rightId) {{
                // Doğru eşleşme
                selectedLeft.classList.add('matched');
                selectedRight.classList.add('matched');
                selectedLeft.classList.remove('selected');
                selectedRight.classList.remove('selected');

                score += 10;
                matchedCount++;

                document.getElementById('score').textContent = score;
                document.getElementById('matched').textContent = matchedCount;

                showMessage('✅ Harika! Doğru eşleştirme!', 'success');

                if (matchedCount === pairs.length) {{
                    setTimeout(() => {{
                        showMessage(`🎉 Tebrikler! Oyunu tamamladınız! Toplam Puan: ${{score}}`, 'success');
                    }}, 500);
                }}

                selectedLeft = null;
                selectedRight = null;
            }} else {{
                // Yanlış eşleşme
                selectedLeft.classList.add('wrong');
                selectedRight.classList.add('wrong');

                showMessage('❌ Yanlış eşleşme! Tekrar dene.', 'error');

                setTimeout(() => {{
                    selectedLeft.classList.remove('selected', 'wrong');
                    selectedRight.classList.remove('selected', 'wrong');
                    selectedLeft = null;
                    selectedRight = null;
                }}, 1000);
            }}
        }}

        function showMessage(text, type) {{
            const message = document.getElementById('message');
            message.textContent = text;
            message.className = 'message show ' + type;

            setTimeout(() => {{
                message.classList.remove('show');
            }}, 2000);
        }}

        function resetGame() {{
            score = 0;
            matchedCount = 0;
            selectedLeft = null;
            selectedRight = null;

            document.getElementById('score').textContent = score;
            document.getElementById('matched').textContent = matchedCount;
            document.getElementById('message').classList.remove('show');

            initGame();
        }}

        function goHome() {{
            window.location.href = '../index.html';
        }}

        // Oyunu başlat
        initGame();
    </script>
</body>
</html>'''

    return html

# Her hafta için oyun oluştur
total_games = 0

for grade_key in ['grade5', 'grade6']:
    grade_num = 5 if grade_key == 'grade5' else 6
    weeks = weekly_data[grade_key]

    for week_info in weeks:
        week_num = week_info['week']

        # Eşleştirme oyunu oluştur
        game_html = create_matching_game(week_info)

        filename = f'oyun-{grade_num}sinif-hafta{week_num}.html'
        filepath = f'/home/user/BST/haftalik-oyunlar/{filename}'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(game_html)

        total_games += 1
        print(f"✅ {grade_num}. Sınıf - Hafta {week_num} oyunu oluşturuldu")

print(f"\n🎉 Toplam {total_games} oyun oluşturuldu!")
print(f"📁 Klasör: /home/user/BST/haftalik-oyunlar/")
