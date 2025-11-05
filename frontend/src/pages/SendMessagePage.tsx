import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-hot-toast';
import { Send } from 'lucide-react';
import { messageApi } from '../services/api';

interface MessageForm {
  message_type: 'SMS' | 'WhatsApp';
  content: string;
  recipient_type: 'class' | 'student_numbers' | 'parents' | 'staff' | 'custom';
  class_ids?: string;
  student_numbers?: string;
  phone_numbers?: string;
  scheduled_at?: string;
}

const SendMessagePage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [charCount, setCharCount] = useState(0);

  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors },
  } = useForm<MessageForm>({
    defaultValues: {
      message_type: 'SMS',
      recipient_type: 'parents',
    },
  });

  const recipientType = watch('recipient_type');
  const content = watch('content');

  // Karakter sayacı
  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setCharCount(e.target.value.length);
  };

  const onSubmit = async (data: MessageForm) => {
    setIsLoading(true);

    try {
      // Recipients nesnesini oluştur
      const recipients: any = {
        type: data.recipient_type,
      };

      if (data.recipient_type === 'class' && data.class_ids) {
        recipients.class_ids = data.class_ids.split(',').map((id) => parseInt(id.trim()));
      }

      if (data.recipient_type === 'student_numbers' && data.student_numbers) {
        recipients.student_numbers = data.student_numbers.split(',').map((n) => n.trim());
      }

      if (data.recipient_type === 'custom' && data.phone_numbers) {
        recipients.phone_numbers = data.phone_numbers.split(',').map((p) => p.trim());
      }

      const payload = {
        message_type: data.message_type,
        content: data.content,
        recipients,
        scheduled_at: data.scheduled_at || undefined,
      };

      const response = await messageApi.sendBulk(payload);

      if (response.data.success) {
        toast.success(
          data.scheduled_at
            ? 'Mesaj başarıyla zamanlandı!'
            : 'Mesaj gönderiliyor!'
        );
        reset();
        setCharCount(0);
      }
    } catch (error: any) {
      const message =
        error.response?.data?.error || 'Mesaj gönderilemedi. Lütfen tekrar deneyin.';
      toast.error(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Mesaj Gönder</h1>
        <p className="mt-2 text-gray-600">
          Toplu SMS veya WhatsApp mesajı gönderin
        </p>
      </div>

      <div className="max-w-4xl">
        <form onSubmit={handleSubmit(onSubmit)} className="card">
          {/* Mesaj Tipi */}
          <div className="mb-6">
            <label className="label">Mesaj Tipi</label>
            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  {...register('message_type')}
                  type="radio"
                  value="SMS"
                  className="mr-2"
                />
                <span>SMS</span>
              </label>
              <label className="flex items-center">
                <input
                  {...register('message_type')}
                  type="radio"
                  value="WhatsApp"
                  className="mr-2"
                />
                <span>WhatsApp</span>
              </label>
            </div>
          </div>

          {/* Alıcı Tipi */}
          <div className="mb-6">
            <label className="label">Alıcı Grubu</label>
            <select
              {...register('recipient_type')}
              className="input"
            >
              <option value="parents">Tüm Veliler</option>
              <option value="class">Sınıflara Göre</option>
              <option value="student_numbers">Öğrenci Numaralarına Göre</option>
              <option value="staff">Personel</option>
              <option value="custom">Elle Numara Gir</option>
            </select>
          </div>

          {/* Sınıf ID'leri */}
          {recipientType === 'class' && (
            <div className="mb-6">
              <label className="label">Sınıf ID'leri (virgülle ayırın)</label>
              <input
                {...register('class_ids', {
                  required: 'Sınıf ID\'leri gerekli',
                })}
                type="text"
                className="input"
                placeholder="Örn: 1, 2, 3"
              />
              {errors.class_ids && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.class_ids.message}
                </p>
              )}
            </div>
          )}

          {/* Öğrenci Numaraları */}
          {recipientType === 'student_numbers' && (
            <div className="mb-6">
              <label className="label">
                Öğrenci Numaraları (virgülle ayırın)
              </label>
              <input
                {...register('student_numbers', {
                  required: 'Öğrenci numaraları gerekli',
                })}
                type="text"
                className="input"
                placeholder="Örn: 1001, 1002, 1003"
              />
              {errors.student_numbers && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.student_numbers.message}
                </p>
              )}
            </div>
          )}

          {/* Telefon Numaraları */}
          {recipientType === 'custom' && (
            <div className="mb-6">
              <label className="label">
                Telefon Numaraları (virgülle ayırın)
              </label>
              <textarea
                {...register('phone_numbers', {
                  required: 'Telefon numaraları gerekli',
                })}
                className="input"
                rows={3}
                placeholder="Örn: 05551234567, 05559876543"
              />
              {errors.phone_numbers && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.phone_numbers.message}
                </p>
              )}
            </div>
          )}

          {/* Mesaj İçeriği */}
          <div className="mb-6">
            <label className="label">Mesaj İçeriği</label>
            <textarea
              {...register('content', {
                required: 'Mesaj içeriği gerekli',
                minLength: {
                  value: 10,
                  message: 'Mesaj en az 10 karakter olmalı',
                },
              })}
              className="input"
              rows={6}
              placeholder="Mesajınızı yazın...

Değişkenler:
{ad} - Alıcının adı
{soyad} - Alıcının soyadı
{tam_ad} - Alıcının tam adı"
              onChange={handleContentChange}
            />
            <div className="flex justify-between mt-1">
              {errors.content && (
                <p className="text-sm text-red-600">{errors.content.message}</p>
              )}
              <p className="text-sm text-gray-500 ml-auto">
                {charCount} karakter
              </p>
            </div>
          </div>

          {/* Zamanlama */}
          <div className="mb-6">
            <label className="label">
              Zamanlama (Opsiyonel - boş bırakırsanız hemen gönderilir)
            </label>
            <input
              {...register('scheduled_at')}
              type="datetime-local"
              className="input"
            />
          </div>

          {/* Örnek Mesaj */}
          {content && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <p className="text-sm font-medium text-gray-700 mb-2">
                Örnek Önizleme:
              </p>
              <p className="text-sm text-gray-900">
                {content
                  .replace(/{ad}/g, 'Ahmet')
                  .replace(/{soyad}/g, 'Yılmaz')
                  .replace(/{tam_ad}/g, 'Ahmet Yılmaz')}
              </p>
            </div>
          )}

          {/* Gönder Butonu */}
          <button
            type="submit"
            className="w-full btn btn-primary py-3"
            disabled={isLoading}
          >
            <Send className="w-5 h-5 mr-2" />
            {isLoading ? 'Gönderiliyor...' : 'Mesaj Gönder'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default SendMessagePage;
