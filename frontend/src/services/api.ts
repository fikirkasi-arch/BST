import axios from 'axios';
import { useAuthStore } from '../stores/authStore';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - token ekle
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - hata yönetimi
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),

  register: (data: any) =>
    api.post('/auth/register', data),

  getCurrentUser: () =>
    api.get('/auth/me'),

  updatePassword: (currentPassword: string, newPassword: string) =>
    api.put('/auth/password', { currentPassword, newPassword }),
};

// Message API
export const messageApi = {
  sendBulk: (data: any) =>
    api.post('/messages/bulk', data),

  getMessages: (params?: any) =>
    api.get('/messages', { params }),

  getMessageById: (id: number) =>
    api.get(`/messages/${id}`),

  cancelScheduled: (id: number) =>
    api.delete(`/messages/${id}/cancel`),
};

// Student API
export const studentApi = {
  getStudents: (params?: any) =>
    api.get('/students', { params }),

  getStudentById: (id: number) =>
    api.get(`/students/${id}`),

  createStudent: (data: any) =>
    api.post('/students', data),

  updateStudent: (id: number, data: any) =>
    api.put(`/students/${id}`, data),

  deleteStudent: (id: number) =>
    api.delete(`/students/${id}`),

  addParent: (data: any) =>
    api.post('/students/parents', data),
};

export default api;
