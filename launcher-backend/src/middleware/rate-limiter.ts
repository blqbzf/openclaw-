import rateLimit from 'express-rate-limit';
import { LogManager } from '../utils/logger';

const logger = LogManager.getLogger('rate-limiter');

export function rateLimiter(options: { windowMs?: number; max?: number }) {
  return rateLimit({
    windowMs: options.windowMs || 60000, // 默认1分钟
    max: options.max || 3, // 默认最多3次请求
    standardHeaders: true,
    legacyHeaders: false,
    handler: (req: any, res: any) => {
      logger.warn(`Rate limit exceeded for IP: ${req.ip}`);
      res.status(429).json({
        success: false,
        message: '请求过于频繁,请稍后再试'
      });
    }
  });
}
