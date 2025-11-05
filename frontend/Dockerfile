FROM node:18-alpine

# Çalışma dizinini ayarla
WORKDIR /app

# Package dosyalarını kopyala
COPY package*.json ./

# Bağımlılıkları yükle
RUN npm install

# Uygulama dosyalarını kopyala
COPY . .

# Port'u aç
EXPOSE 3000

# Uygulamayı başlat
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
