import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { messageApi } from '../services/api';
import { format } from 'date-fns';

const MessagesPage = () => {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['messages', page],
    queryFn: async () => {
      const response = await messageApi.getMessages({ page, limit: 20 });
      return response.data;
    },
  });

  const getStatusBadge = (status: string) => {
    const badges: Record<string, string> = {
      sent: 'badge-success',
      pending: 'badge-warning',
      failed: 'badge-danger',
      scheduled: 'badge-info',
      sending: 'badge-warning',
    };
    return badges[status] || 'badge-info';
  };

  const getStatusText = (status: string) => {
    const texts: Record<string, string> = {
      sent: 'Gönderildi',
      pending: 'Bekliyor',
      failed: 'Başarısız',
      scheduled: 'Zamanlandı',
      sending: 'Gönderiliyor',
    };
    return texts[status] || status;
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Mesajlar</h1>
        <p className="mt-2 text-gray-600">
          Gönderilen ve zamanlanmış mesajları görüntüleyin
        </p>
      </div>

      {/* Messages Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Mesaj
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tip
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Alıcı Sayısı
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Gönderilen
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Durum
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tarih
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {isLoading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                    Yükleniyor...
                  </td>
                </tr>
              ) : data?.data?.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                    Henüz mesaj bulunmuyor
                  </td>
                </tr>
              ) : (
                data?.data?.map((message: any) => (
                  <tr key={message.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">
                        {message.content.substring(0, 50)}
                        {message.content.length > 50 && '...'}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-900">
                        {message.message_type}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-900">
                        {message.recipient_count}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-900">
                        {message.sent_count}/{message.recipient_count}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`badge ${getStatusBadge(message.status)}`}>
                        {getStatusText(message.status)}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-500">
                        {format(
                          new Date(message.created_at),
                          'dd/MM/yyyy HH:mm'
                        )}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {data?.pagination && (
          <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
            <div className="text-sm text-gray-700">
              Toplam {data.pagination.total} kayıt
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setPage(page - 1)}
                disabled={page === 1}
                className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Önceki
              </button>
              <button
                onClick={() => setPage(page + 1)}
                disabled={page >= data.pagination.totalPages}
                className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Sonraki
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessagesPage;
