import rateLimit from 'express-rate-limit';
import { LogManager } from '../utils/logger';

const logger = LogManager.getLogger('rate-limiter');

// IP 频率限制中间件
export function rateLimiter(options: { windowMs: number; max: number }) {
  const limiter = rateLimit({
    windowMs: options.windowMs || 60000, // 默认1分钟
    max: options.max || 3 // 默认最多3次请求
    standardHeaders: true,
    handler: (req: any, res: any) => {
      const ip = req.ip || req.headers['x-forwarded-for'] || 'unknown';
      const key = `${ip}:${req.path}`;

      const current = limiter.get(key) || { count: 0, firstRequest: 0 };

      if (current.count === 0) {
        current.firstRequest = Date.now();
      }

      if (current.count >= limiter.max) {
        logger.warn(`Rate limit exceeded for IP: ${ip}`);
        res.status(429).json({
          success: false,
          message: '请求过于频繁,请稍后再试'
        });
        return;
      }

      current.count++;
      limiter.set(key, current);
      req.next();
    },
    keyGenerator: (req: any) => `${req.ip}:${req.path}`
  });

  // 定期清理过期记录
  setInterval(() => {
    const now = Date.now();
    for (const [key, value] of limiter) {
      if (now - value.firstRequest > limiter.windowMs) {
        limiter.delete(key);
      }
    }
  }, limiter.windowMs);
}

