FROM node:18-alpine

# Çalışma dizinini ayarla
WORKDIR /app

# Package dosyalarını kopyala
COPY package*.json ./

# Bağımlılıkları yükle
RUN npm install

# Uygulama dosyalarını kopyala
COPY . .

# Upload ve log klasörlerini oluştur
RUN mkdir -p uploads logs whatsapp-session

# Port'u aç
EXPOSE 5000

# Uygulamayı başlat
CMD ["npm", "run", "dev"]
