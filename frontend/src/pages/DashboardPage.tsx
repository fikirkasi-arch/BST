import { Send, MessageSquare, Users, CheckCircle } from 'lucide-react';

const DashboardPage = () => {
  const stats = [
    {
      name: 'Toplam Mesaj',
      value: '1,234',
      icon: MessageSquare,
      color: 'bg-blue-500',
    },
    {
      name: 'Gönderilen',
      value: '1,180',
      icon: CheckCircle,
      color: 'bg-green-500',
    },
    {
      name: 'Bugün Gönderilen',
      value: '45',
      icon: Send,
      color: 'bg-purple-500',
    },
    {
      name: 'Toplam Öğrenci',
      value: '856',
      icon: Users,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Ana Sayfa</h1>
        <p className="mt-2 text-gray-600">
          Okul SMS sistemine hoş geldiniz. İstatistiklerinizi buradan takip edebilirsiniz.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <div key={stat.name} className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">
                  {stat.name}
                </p>
                <p className="mt-2 text-3xl font-bold text-gray-900">
                  {stat.value}
                </p>
              </div>
              <div className={`p-3 rounded-lg ${stat.color}`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Son Mesajlar */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Son Gönderilen Mesajlar
          </h3>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    Veli Toplantısı Duyurusu
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    150 alıcı • 2 saat önce
                  </p>
                </div>
                <span className="badge badge-success">Gönderildi</span>
              </div>
            ))}
          </div>
        </div>

        {/* Hızlı İşlemler */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Hızlı İşlemler
          </h3>
          <div className="space-y-3">
            <button className="w-full btn btn-primary justify-start">
              <Send className="w-5 h-5 mr-2" />
              Yeni Mesaj Gönder
            </button>
            <button className="w-full btn btn-secondary justify-start">
              <Users className="w-5 h-5 mr-2" />
              Öğrenci Ekle
            </button>
            <button className="w-full btn btn-secondary justify-start">
              <MessageSquare className="w-5 h-5 mr-2" />
              Mesaj Şablonu Oluştur
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
