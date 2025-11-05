import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { toast } from 'react-hot-toast';
import { authApi } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import { Lock, User } from 'lucide-react';

interface LoginForm {
  username: string;
  password: string;
}

const LoginPage = () => {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>();

  const onSubmit = async (data: LoginForm) => {
    setIsLoading(true);

    try {
      const response = await authApi.login(data.username, data.password);

      if (response.data.success) {
        const { token, user } = response.data.data;
        login(token, user);
        toast.success('Giriş başarılı!');
        navigate('/');
      }
    } catch (error: any) {
      const message =
        error.response?.data?.error || 'Giriş başarısız. Lütfen tekrar deneyin.';
      toast.error(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700 px-4">
      <div className="max-w-md w-full">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Okul SMS Sistemi
          </h1>
          <p className="text-primary-100">
            Toplu SMS ve WhatsApp Yönetim Sistemi
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Giriş Yap</h2>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            {/* Username */}
            <div>
              <label className="label">Kullanıcı Adı</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  {...register('username', {
                    required: 'Kullanıcı adı gerekli',
                  })}
                  type="text"
                  className="input pl-10"
                  placeholder="Kullanıcı adınızı girin"
                  disabled={isLoading}
                />
              </div>
              {errors.username && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.username.message}
                </p>
              )}
            </div>

            {/* Password */}
            <div>
              <label className="label">Şifre</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  {...register('password', {
                    required: 'Şifre gerekli',
                  })}
                  type="password"
                  className="input pl-10"
                  placeholder="Şifrenizi girin"
                  disabled={isLoading}
                />
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.password.message}
                </p>
              )}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full btn btn-primary py-3 text-base"
              disabled={isLoading}
            >
              {isLoading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
            </button>
          </form>
        </div>

        {/* Footer */}
        <p className="mt-6 text-center text-primary-100 text-sm">
          &copy; 2024 Okul SMS Sistemi. Tüm hakları saklıdır.
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
