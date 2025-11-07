import express, { Application } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import compression from 'compression';
import pool from './config/database';
import schedulerService from './services/schedulerService';
import whatsappService from './services/whatsappService';
import { errorHandler, notFound } from './middleware/errorHandler';

// Routes
import authRoutes from './routes/authRoutes';
import messageRoutes from './routes/messageRoutes';
import studentRoutes from './routes/studentRoutes';
import templateRoutes from './routes/templateRoutes';
import reportRoutes from './routes/reportRoutes';

// .env dosyasını yükle
dotenv.config();

const app: Application = express();
const PORT = process.env.PORT || 5000;

// Security Middleware
app.use(helmet({
  contentSecurityPolicy: process.env.NODE_ENV === 'production' ? undefined : false,
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000'), // 15 minutes
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '100'), // limit each IP to 100 requests per windowMs
  message: 'Çok fazla istek gönderdiniz, lütfen daha sonra tekrar deneyin.',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// Compression middleware
app.use(compression());

// CORS
app.use(cors({
  origin: process.env.CORS_ORIGIN?.split(',') || 'http://localhost:3000',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// Body parser
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Ana route
app.get('/', (req, res) => {
  res.json({
    success: true,
    message: 'Okul Toplu SMS/WhatsApp Sistemi API',
    version: '1.0.0',
    endpoints: {
      auth: '/api/auth',
      messages: '/api/messages',
      students: '/api/students',
    },
  });
});

// Health check
app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({
      success: true,
      status: 'healthy',
      database: 'connected',
      whatsapp: whatsappService.isConnected() ? 'connected' : 'disconnected',
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    res.status(503).json({
      success: false,
      status: 'unhealthy',
      error: 'Database connection failed',
    });
  }
});

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/messages', messageRoutes);
app.use('/api/students', studentRoutes);
app.use('/api/templates', templateRoutes);
app.use('/api/reports', reportRoutes);

// 404 handler
app.use(notFound);

// Error handler
app.use(errorHandler);

// Sunucuyu başlat
const startServer = async () => {
  try {
    // Veritabanı bağlantısını test et
    await pool.query('SELECT NOW()');
    console.log('✅ Veritabanı bağlantısı başarılı');

    // WhatsApp servisini başlat (opsiyonel)
    if (process.env.WHATSAPP_ENABLED === 'true') {
      try {
        await whatsappService.initialize();
        console.log('✅ WhatsApp servisi başlatıldı');
      } catch (error) {
        console.log('⚠️  WhatsApp servisi başlatılamadı:', error);
      }
    }

    // Zamanlanmış mesajları başlat
    schedulerService.startScheduledMessagesCheck();
    schedulerService.startAttendanceNotifications();

    // Sunucuyu dinle
    app.listen(PORT, () => {
      console.log('');
      console.log('═══════════════════════════════════════════');
      console.log('  🏫 Okul Toplu SMS/WhatsApp Sistemi');
      console.log('═══════════════════════════════════════════');
      console.log(`  🚀 Sunucu çalışıyor: http://localhost:${PORT}`);
      console.log(`  📊 Ortam: ${process.env.NODE_ENV || 'development'}`);
      console.log('═══════════════════════════════════════════');
      console.log('');
    });
  } catch (error) {
    console.error('❌ Sunucu başlatma hatası:', error);
    process.exit(1);
  }
};

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM sinyali alındı, sunucu kapatılıyor...');
  schedulerService.stopAll();
  await whatsappService.disconnect();
  await pool.end();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('SIGINT sinyali alındı, sunucu kapatılıyor...');
  schedulerService.stopAll();
  await whatsappService.disconnect();
  await pool.end();
  process.exit(0);
});

// Sunucuyu başlat
startServer();

export default app;
