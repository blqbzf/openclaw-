import * as fs from 'fs';
import * as path from 'path';
import { LogManager } from '../utils/logger';
import { NewsItem } from '../models/news';

const logger = LogManager.getLogger('news-service');

export class NewsService {
  private static newsPath = path.join(__dirname, '../../data/news.json');

  static async getNews(): Promise<NewsItem[]> {
    try {
      const content = await fs.promises.readFile(this.newsPath, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      logger.error('Failed to read news file', error);
      return [];
    }
  }
}
