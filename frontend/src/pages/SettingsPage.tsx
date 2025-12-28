import { Settings as SettingsIcon, Key, Database } from 'lucide-react';

const SettingsPage = () => {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Ayarlar</h1>
        <p className="mt-2 text-gray-600">
          Sistem ayarlarını yapılandırın
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* SMS Sağlayıcı Ayarları */}
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-primary-100 rounded-lg">
              <SettingsIcon className="w-5 h-5 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">
              SMS Sağlayıcı Ayarları
            </h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="label">Sağlayıcı</label>
              <select className="input">
                <option>NetGSM</option>
                <option>Twilio</option>
              </select>
            </div>
            <div>
              <label className="label">API Kullanıcı Adı</label>
              <input type="text" className="input" />
            </div>
            <div>
              <label className="label">API Şifre</label>
              <input type="password" className="input" />
            </div>
            <div>
              <label className="label">Başlık</label>
              <input type="text" className="input" placeholder="OKUL ADI" />
            </div>
            <button className="btn btn-primary w-full">
              Kaydet
            </button>
          </div>
        </div>

        {/* WhatsApp Ayarları */}
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-green-100 rounded-lg">
              <Database className="w-5 h-5 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">
              WhatsApp Ayarları
            </h3>
          </div>
          <div className="space-y-4">
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                WhatsApp'ı kullanmak için QR kod ile giriş yapmanız gerekiyor.
                Sunucu terminalinden QR kodu okutun.
              </p>
            </div>
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <span className="text-sm font-medium text-gray-700">
                Bağlantı Durumu
              </span>
              <span className="badge badge-danger">Bağlı Değil</span>
            </div>
            <button className="btn btn-primary w-full">
              WhatsApp'ı Başlat
            </button>
          </div>
        </div>

        {/* Şifre Değiştirme */}
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Key className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">
              Şifre Değiştir
            </h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="label">Mevcut Şifre</label>
              <input type="password" className="input" />
            </div>
            <div>
              <label className="label">Yeni Şifre</label>
              <input type="password" className="input" />
            </div>
            <div>
              <label className="label">Yeni Şifre (Tekrar)</label>
              <input type="password" className="input" />
            </div>
            <button className="btn btn-primary w-full">
              Şifreyi Güncelle
            </button>
          </div>
        </div>

        {/* Genel Ayarlar */}
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gray-100 rounded-lg">
              <SettingsIcon className="w-5 h-5 text-gray-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">
              Genel Ayarlar
            </h3>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-700">
                  Otomatik Devamsızlık Bildirimi
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Her gün saat 10:00'da otomatik gönderilir
                </p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-700">
                  Sınav Sonuç Bildirimi
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Sınav sonuçları girildiğinde otomatik gönder
                </p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" defaultChecked />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
