#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random

# Weekly plans JSON dosyasını oku
with open('/home/user/BST/weekly_plans.json', 'r', encoding='utf-8') as f:
    weekly_plans = json.load(f)

# Meraklısına içerikleri için şablonlar
fun_facts_templates = {
    'bilgisayar': [
        "İlk bilgisayar ENIAC 1946'da yapıldı ve tam 30 ton ağırlığındaydı!",
        "Dünyanın ilk bilgisayar programcısı Ada Lovelace adında bir kadındır (1843).",
        "İlk fare 1964'te Douglas Engelbart tarafından ahşaptan yapılmıştır.",
        "QWERTY klavye düzeni 1873'te tasarlandı ve bugün hala kullanılıyor!",
        "İlk hard disk 1956'da yapıldı ve sadece 5 MB veri saklayabiliyordu ama buzdolabı boyutundaydı!"
    ],
    'internet': [
        "İlk e-posta 1971'de gönderildi ve mesaj sadece 'QWERTYUIOP' idi.",
        "İlk web sitesi 1991'de Tim Berners-Lee tarafından yayınlandı ve bugün hala aktif!",
        "Dünyada her saniye 2.5 milyon GB veri üretiliyor!",
        "İlk emoji 1999'da Japonya'da kullanıldı ve kalp şeklindeydi.",
        "YouTube'a her dakika 500 saatten fazla video yükleniyor!"
    ],
    'yazilim': [
        "İlk bilgisayar virüsü 1983'te yazıldı ve ismiydi 'Elk Cloner'.",
        "Google'ın adı aslında 'Googol' kelimesinden geliyor (10^100 sayısı).",
        "İlk video oyunu 'Pong' 1972'de çıktı ve sadece bir top ve iki raket vardı!",
        "Scratch programı 2007'de MIT'de geliştirildi ve 60 milyondan fazla proje yapıldı.",
        "Python programlama dili adını 'Monty Python' komedi grubundan alıyor!"
    ],
    'yapay_zeka': [
        "İlk yapay zeka programı 1956'da yazıldı ve satranç oynayabiliyordu.",
        "Siri, Alexa gibi sesli asistanlar doğal dil işleme teknolojisi kullanıyor.",
        "Yapay zeka, sanat eserleri yapabiliyor! Bazıları milyonlarca dolara satıldı.",
        "Netflix önerilerinin %75'i yapay zeka algoritmaları tarafından yapılıyor.",
        "Google Translate günde 100 milyardan fazla kelime çeviriyor!"
    ],
    'guvenlik': [
        "Dünyanın en çok kullanılan şifresi hala '123456'!",
        "Her gün 300 milyardan fazla e-posta gönderiliyor ve %85'i spam!",
        "İki faktörlü doğrulama kullanmak hesap güvenliğini %99 artırıyor.",
        "İlk siber saldırı 1988'de yapıldı ve 6000 bilgisayarı etkiledi.",
        "Bir hacker, 8 karakterlik bir şifreyi ortalama 8 saatte kırabilir!"
    ]
}

riddles = [
    {"soru": "Hangi bilgisayar parçası 'bilgisayarın beyni' olarak bilinir?", "cevap": "İşlemci (CPU)"},
    {"soru": "Internette gezinmek için kullandığımız programa ne denir?", "cevap": "Tarayıcı (Browser)"},
    {"soru": "1 GB kaç MB'dir?", "cevap": "1024 MB"},
    {"soru": "HTML açılımı nedir?", "cevap": "HyperText Markup Language"},
    {"soru": "Bilgisayarın geçici hafızasına ne denir?", "cevap": "RAM"},
    {"soru": "Mouse'u Türkçe'ye çevirelim. Ne olur?", "cevap": "Fare"},
    {"soru": "Siber zorbalığa İngilizce ne denir?", "cevap": "Cyberbullying"},
    {"soru": "Scratch'te kullandığımız renkli komutlara ne denir?", "cevap": "Blok"},
]

jokes = [
    "Öğretmen: 'Bilgisayarın kalbi var mı?'\nÖğrenci: 'Hayır ama faresi var!'",
    "İki bilgisayar sokakta karşılaşır.\nBiri diğerine: 'Nasılsın?'\nÖteki: 'Güncelleme yapıyorum, sonra kapanacağım!'",
    "Neden bilgisayarlar üşümez?\nÇünkü pencereleri (Windows) var!",
    "Robot öğretmene ne denir?\nCTRL + ALT + DELETE yapamayan öğretmen!",
    "Bilgisayar virüsü hastaneye gitse doktor ne der?\n'Antivirüs alın, hemen geçer!'",
]

def generate_game_content(week_data):
    """Haftalık oyun içeriği oluştur"""
    topic = week_data['topic']
    unit = week_data['unit']
    grade = week_data['grade']

    # Oyun türünü konuya göre belirle
    game_types = ['quiz', 'matching', 'memory', 'sorting']
    game_type = random.choice(game_types)

    return {
        'type': game_type,
        'title': f"{topic} - Eğlenceli Oyun",
        'description': f"Bu haftanın konusu '{topic}' ile ilgili eğlenceli bir {game_type} oyunu!",
        'topic': topic,
        'unit': unit
    }

def generate_homework_content(week_data):
    """Haftalık ödev içeriği oluştur"""
    topic = week_data['topic']
    unit = week_data['unit']
    outcome = week_data['outcome']
    grade = week_data['grade']

    # Ödev türlerini belirle
    homework_types = [
        {
            'type': 'research',
            'title': f'{topic} Araştırması',
            'tasks': [
                f"'{topic}' konusu hakkında araştırma yapın.",
                "En az 3 kaynak kullanın (kitap, internet, dergi).",
                "Bulgularınızı 1 sayfalık bir rapor halinde yazın.",
                "Görseller ekleyin.",
                "Kaynakçanızı belirtin."
            ]
        },
        {
            'type': 'practical',
            'title': f'{topic} Uygulaması',
            'tasks': [
                f"Bu hafta öğrendiğiniz '{topic}' konusunu uygulayın.",
                "Pratik bir çalışma yapın.",
                "Yaptığınız çalışmayı fotoğraflayın veya ekran görüntüsü alın.",
                "Çalışmanızda karşılaştığınız zorlukları not edin.",
                "Öğrendiklerinizi 5-10 cümle ile özetleyin."
            ]
        },
        {
            'type': 'creative',
            'title': f'{topic} Yaratıcı Proje',
            'tasks': [
                f"'{topic}' konusu ile ilgili yaratıcı bir proje hazırlayın.",
                "Poster, sunum veya video hazırlayabilirsiniz.",
                "Konuyu arkadaşlarınıza anlatabileceğiniz şekilde anlatın.",
                "Renkli ve görsel öğeler kullanın.",
                "Hazırladığınız materyali sınıfta sunmaya hazır olun."
            ]
        }
    ]

    homework = random.choice(homework_types)

    return {
        'type': homework['type'],
        'title': homework['title'],
        'tasks': homework['tasks'],
        'duration': '1 hafta',
        'topic': topic
    }

def get_fun_fact_category(topic):
    """Konuya göre ilginç bilgi kategorisi seç"""
    topic_lower = topic.lower()

    if 'bilgisayar' in topic_lower or 'donanım' in topic_lower or 'yazılım' in topic_lower:
        return 'bilgisayar'
    elif 'internet' in topic_lower or 'ağ' in topic_lower or 'iletişim' in topic_lower:
        return 'internet'
    elif 'program' in topic_lower or 'kod' in topic_lower or 'scratch' in topic_lower:
        return 'yazilim'
    elif 'yapay zeka' in topic_lower or 'ai' in topic_lower:
        return 'yapay_zeka'
    elif 'güvenlik' in topic_lower or 'şifre' in topic_lower or 'etik' in topic_lower:
        return 'guvenlik'
    else:
        return random.choice(['bilgisayar', 'internet', 'yazilim', 'yapay_zeka', 'guvenlik'])

def generate_fun_content(week_data, week_num):
    """Meraklısına içeriği oluştur"""
    topic = week_data['topic']

    # Kategoriye göre ilginç bilgi seç
    category = get_fun_fact_category(topic)
    fun_fact = random.choice(fun_facts_templates[category])

    # Bulmaca seç
    riddle = riddles[week_num % len(riddles)]

    # Fıkra seç
    joke = jokes[week_num % len(jokes)]

    return {
        'fun_fact': fun_fact,
        'riddle': riddle,
        'joke': joke,
        'category': category
    }

# Her hafta için içerik oluştur
weekly_content = {
    'grade5': [],
    'grade6': []
}

print("🎮 Haftalık içerikler oluşturuluyor...")

for grade_key in ['grade5', 'grade6']:
    grade_num = 5 if grade_key == 'grade5' else 6
    weeks = weekly_plans[grade_key]

    for week_data in weeks:
        week_num = week_data['week']

        content = {
            'week': week_num,
            'grade': grade_num,
            'week_text': week_data['week_text'],
            'unit': week_data['unit'],
            'topic': week_data['topic'],
            'outcome': week_data['outcome'],
            'game': generate_game_content(week_data),
            'homework': generate_homework_content(week_data),
            'fun': generate_fun_content(week_data, week_num)
        }

        weekly_content[grade_key].append(content)
        print(f"✅ {grade_num}. Sınıf - Hafta {week_num}: {week_data['topic']}")

# JSON dosyasına kaydet
with open('/home/user/BST/weekly_content.json', 'w', encoding='utf-8') as f:
    json.dump(weekly_content, f, ensure_ascii=False, indent=2)

print(f"\n✅ Toplam {len(weekly_content['grade5'])} + {len(weekly_content['grade6'])} = {len(weekly_content['grade5']) + len(weekly_content['grade6'])} haftalık içerik oluşturuldu!")
print("📁 Dosya: weekly_content.json")
