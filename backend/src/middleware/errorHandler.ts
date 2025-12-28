import { Request, Response, NextFunction } from 'express';

export class AppError extends Error {
  statusCode: number;
  isOperational: boolean;

  constructor(message: string, statusCode: number) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;

    Error.captureStackTrace(this, this.constructor);
  }
}

export const errorHandler = (
  err: Error | AppError,
  _req: Request,
  res: Response,
  _next: NextFunction
): void => {
  if (err instanceof AppError) {
    res.status(err.statusCode).json({
      success: false,
      error: err.message,
    });
    return;
  }

  // Geliştirme ortamında detaylı hata
  if (process.env.NODE_ENV === 'development') {
    console.error('Error:', err);
    res.status(500).json({
      success: false,
      error: err.message,
      stack: err.stack,
    });
    return;
  }

  // Production ortamında genel hata
  console.error('Error:', err);
  res.status(500).json({
    success: false,
    error: 'Sunucu hatası oluştu',
  });
};

export const notFound = (req: Request, res: Response, _next: NextFunction): void => {
  res.status(404).json({
    success: false,
    error: `Endpoint bulunamadı: ${req.originalUrl}`,
  });
};
