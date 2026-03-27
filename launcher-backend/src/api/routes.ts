import express, { Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { LogManager } from '../utils/logger';
import { ManifestService } from '../services/manifest-service';
import { NewsService } from '../services/news-service';
import { setupRegisterRoutes } from './register';

const logger = LogManager.getLogger('api');
const app = express();

// 中间件
app.use(helmet());
app.use(cors());
app.use(express.json());

// 请求日志
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.path} - ${req.ip}`);
  next();
});

// 注册路由
setupRegisterRoutes(app);

// Manifest API
app.get('/api/manifest', async (req: Request, res: Response) => {
  try {
    const manifest = await ManifestService.getManifest();
    res.json(manifest);
  } catch (error) {
    logger.error('Failed to get manifest', error);
    res.status(500).json({
      success: false,
      message: '获取清单失败'
    });
  }
});

// News API
app.get('/api/news', async (req: Request, res: Response) => {
  try {
    const news = await NewsService.getNews();
    res.json(news);
  } catch (error) {
    logger.error('Failed to get news', error);
    res.status(500).json({
      success: false,
      message: '获取公告失败'
    });
  }
});

// Version API
app.get('/api/version', (req: Request, res: Response) => {
  res.json({
    success: true,
    data: {
      launcherVersion: '1.0.0',
      backendVersion: '1.0.0',
      minClientVersion: '3.3.5'
    }
  });
});

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

export default app;
