import { Request, Response } from 'express';
import { AccountService } from '../services/account-service';
import { validateRegister } from '../utils/validator';
import { rateLimiter } from '../middleware/rate-limiter';
import { LogManager } from '../utils/logger';

const logger = LogManager.getLogger('register-api');

export function setupRegisterRoutes(app: any) {
  app.post('/api/register',
    rateLimiter({ windowMs: 60000, max: 3 }), // 1分钟内最多3次请求
    validateRegister,
    async (req: Request, res: Response) => {
      try {
        const { username, password, email } = req.body;

        const result = await AccountService.register({
          username,
          password,
          email
        });

        logger.info(`Registration attempt: ${username} from ${req.ip}`);

        res.json(result);
      } catch (error) {
        logger.error('Registration error', error);
        res.status(500).json({
          success: false,
          message: '注册失败，请稍后重试'
        });
      }
    }
  );

  // 检查用户名是否可用
  app.get('/api/check-username/:username',
    rateLimiter({ windowMs: 60000, max: 10 }),
    async (req: Request, res: Response) => {
      try {
        const { username } = req.params;
        const available = await AccountService.checkUsername(username);

        res.json({ available });
      } catch (error) {
        logger.error('Check username error', error);
        res.status(500).json({
          success: false,
          message: '检查失败'
        });
      }
    }
  );
}
