# Katkıda Bulunma Rehberi

Okul SMS Sistemi projesine katkıda bulunmak istediğiniz için teşekkürler! 🎉

Bu doküman, projeye nasıl katkıda bulunabileceğinizi açıklar.

## 📋 İçindekiler

1. [Davranış Kuralları](#davranış-kuralları)
2. [Nasıl Katkıda Bulunabilirim?](#nasıl-katkıda-bulunabilirim)
3. [Geliştirme Ortamını Kurma](#geliştirme-ortamını-kurma)
4. [Pull Request Süreci](#pull-request-süreci)
5. [Kodlama Standartları](#kodlama-standartları)
6. [Commit Mesajları](#commit-mesajları)

---

## Davranış Kuralları

Bu proje katılımcı davranış kurallarına tabidir. Projeye katılarak bu kuralları kabul etmiş sayılırsınız.

### Beklentilerimiz

✅ **Yapalım:**
- Saygılı ve kapsayıcı bir dil kullanalım
- Farklı görüşlere açık olalım
- Yapıcı eleştiri kabul edelim
- Topluluk için en iyi olana odaklanalım

❌ **Yapmayalım:**
- Saldırgan veya aşağılayıcı dil kullanmayalım
- Troling veya hakaret etmeyelim
- Kişisel saldırılarda bulunmayalım
- İzinsiz kişisel bilgi paylaşmayalım

---

## Nasıl Katkıda Bulunabilirim?

### 🐛 Hata Bildirimi

Bir hata buldunuz mu?

1. **GitHub Issues**'a gidin
2. Benzer bir issue olmadığını kontrol edin
3. Yeni issue açın ve şunları ekleyin:
   - **Hata açıklaması**: Ne oldu?
   - **Beklenen davranış**: Ne olması gerekiyordu?
   - **Adımlar**: Hatayı nasıl tekrar üretebiliriz?
   - **Ekran görüntüleri**: Varsa ekleyin
   - **Ortam**: OS, Node.js versiyonu, vb.

**Örnek Hata Raporu:**

```markdown
## Hata Açıklaması
Excel dosyası yüklenirken 500 hatası alıyorum.

## Beklenen Davranış
Excel dosyası yüklenmeli ve öğrenciler sisteme eklenmeli.

## Tekrar Üretme Adımları
1. Öğrenciler sayfasına git
2. "İçe Aktar" butonuna tıkla
3. 1000 satırlık Excel dosyası seç
4. Hata görünüyor

## Ekran Görüntüsü
[ekran görüntüsü ekle]

## Ortam
- OS: Windows 11
- Node.js: v18.17.0
- Docker: 24.0.5
```

### ✨ Yeni Özellik Önerisi

Yeni bir özellik mi öneriyorsunuz?

1. **GitHub Issues**'da "Feature Request" açın
2. Şunları açıklayın:
   - **Özellik açıklaması**: Ne istiyorsunuz?
   - **Motivasyon**: Neden gerekli?
   - **Alternatifler**: Başka çözümler düşündünüz mü?
   - **Ekstra**: Varsa mockup veya tasarım

### 📝 Dokümantasyon

Dokümantasyon her zaman geliştirilebilir!

- Yazım hataları düzeltin
- Örnekler ekleyin
- Eksik kısımları tamamlayın
- Çeviriler ekleyin

### 💻 Kod Katkısı

Pull request göndermek için [Pull Request Süreci](#pull-request-süreci) bölümüne bakın.

---

## Geliştirme Ortamını Kurma

### 1. Repository'yi Fork Edin

GitHub'da repository'yi fork edin.

### 2. Clone Edin

```bash
git clone https://github.com/KULLANICI_ADINIZ/BST.git
cd BST
```

### 3. Upstream Remote Ekleyin

```bash
git remote add upstream https://github.com/fikirkasi-arch/BST.git
```

### 4. Bağımlılıkları Yükleyin

#### Backend:

```bash
cd backend
npm install
```

#### Frontend:

```bash
cd frontend
npm install
```

### 5. Veritabanını Kurun

```bash
# Docker ile
docker-compose up -d postgres

# Veya manuel
createdb okul_sms_db
psql -d okul_sms_db -f database/schema.sql
```

### 6. .env Dosyasını Oluşturun

```bash
cd backend
cp .env.example .env
# .env dosyasını düzenleyin
```

### 7. Development Modda Çalıştırın

**Backend:**
```bash
cd backend
npm run dev
```

**Frontend:**
```bash
cd frontend
npm run dev
```

---

## Pull Request Süreci

### 1. Yeni Branch Oluşturun

```bash
git checkout -b feature/ozellik-adi
```

Branch isimlendirme:
- `feature/` - Yeni özellik
- `fix/` - Hata düzeltmesi
- `docs/` - Dokümantasyon
- `refactor/` - Kod yeniden yapılandırma
- `test/` - Test ekleme

### 2. Değişikliklerinizi Yapın

- Kodlama standartlarına uyun
- Test yazın (varsa)
- Dokümantasyonu güncelleyin

### 3. Test Edin

```bash
# Backend testleri
cd backend
npm test

# Frontend testleri
cd frontend
npm test

# Tüm sistemi test edin
docker-compose up
```

### 4. Commit Edin

```bash
git add .
git commit -m "feat: yeni özellik eklendi"
```

[Commit Mesajları](#commit-mesajları) bölümüne bakın.

### 5. Push Edin

```bash
git push origin feature/ozellik-adi
```

### 6. Pull Request Açın

1. GitHub'da fork'unuza gidin
2. "Compare & pull request" butonuna tıklayın
3. Açıklama yazın:
   - Ne değiştirdiniz?
   - Neden değiştirdiniz?
   - Nasıl test edilebilir?
4. "Create pull request" tıklayın

### PR Açıklama Şablonu:

```markdown
## Değişiklik Açıklaması
[Kısa açıklama]

## Motivasyon
[Neden bu değişiklik gerekli?]

## Test Planı
- [ ] Backend testleri geçti
- [ ] Frontend testleri geçti
- [ ] Manuel test yapıldı
- [ ] Dokümantasyon güncellendi

## Ekran Görüntüleri (varsa)
[ekran görüntüleri]

## Checklist
- [ ] Kodlama standartlarına uydum
- [ ] Test yazdım
- [ ] Dokümantasyonu güncelledim
- [ ] CHANGELOG.md'yi güncelledim
```

---

## Kodlama Standartları

### TypeScript/JavaScript

#### Formatlamak

```bash
# Prettier kullanın (otomatik formatla)
npm run format

# ESLint kullanın (kod kalitesi)
npm run lint
```

#### Stil Kuralları

```typescript
// ✅ İyi
const getUserById = async (id: number): Promise<User> => {
  const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
  return user.rows[0];
};

// ❌ Kötü
async function getUserById(id) {
  return await db.query('SELECT * FROM users WHERE id = $1', [id]).rows[0];
}
```

**Kurallar:**
- Arrow function kullanın
- Type annotation ekleyin
- async/await kullanın (promise.then yerine)
- Anlamlı değişken isimleri
- Single responsibility principle

### React/Frontend

```tsx
// ✅ İyi
interface Props {
  name: string;
  onSubmit: (data: FormData) => void;
}

export const UserForm: React.FC<Props> = ({ name, onSubmit }) => {
  return (
    <form onSubmit={handleSubmit}>
      {/* ... */}
    </form>
  );
};

// ❌ Kötü
export default function UserForm(props) {
  return <form>{/* ... */}</form>;
}
```

**Kurallar:**
- Functional components kullanın
- Props için interface tanımlayın
- Named export kullanın
- Hooks doğru kullanın

### API Route'ları

```typescript
// ✅ İyi
router.post(
  '/students',
  authenticate,
  authorize('admin', 'manager'),
  validate([
    body('name').trim().notEmpty(),
  ]),
  studentController.create
);

// ❌ Kötü
router.post('/students', (req, res) => {
  // validation yok, auth yok
  db.query(/* ... */);
});
```

---

## Commit Mesajları

[Conventional Commits](https://www.conventionalcommits.org/) standardını kullanıyoruz.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type'lar

- **feat**: Yeni özellik
- **fix**: Hata düzeltmesi
- **docs**: Dokümantasyon
- **style**: Formatla (kod mantığı değişmez)
- **refactor**: Yeniden yapılandırma
- **test**: Test ekleme
- **chore**: Build, bağımlılık güncellemeleri

### Örnekler

```bash
# Yeni özellik
git commit -m "feat(students): add Excel import functionality"

# Hata düzeltmesi
git commit -m "fix(auth): resolve token expiration issue"

# Dokümantasyon
git commit -m "docs(readme): add installation instructions"

# Detaylı commit
git commit -m "feat(messages): add message templates

- Add template CRUD operations
- Add template controller and routes
- Update database schema with templates table
- Add API documentation for templates

Closes #123"
```

---

## Test Yazma

### Backend Test (Jest)

```typescript
describe('Student Controller', () => {
  it('should create a new student', async () => {
    const studentData = {
      student_number: '12345',
      first_name: 'Ahmet',
      last_name: 'Yılmaz',
    };

    const response = await request(app)
      .post('/api/students')
      .send(studentData)
      .expect(201);

    expect(response.body.success).toBe(true);
    expect(response.body.data.student_number).toBe('12345');
  });
});
```

### Frontend Test (React Testing Library)

```tsx
describe('LoginPage', () => {
  it('should render login form', () => {
    render(<LoginPage />);

    expect(screen.getByLabelText(/kullanıcı adı/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/şifre/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /giriş/i })).toBeInTheDocument();
  });
});
```

---

## Sorularınız mı Var?

- 💬 **Discussions**: Genel sorular için
- 🐛 **Issues**: Hata raporları ve özellik istekleri için
- 📧 **Email**: Gizli konular için

---

## Teşekkürler! 🎉

Katkılarınız için şimdiden teşekkür ederiz! Her katkı, projeyi daha iyi hale getirir.

**Happy Coding!** 🚀
