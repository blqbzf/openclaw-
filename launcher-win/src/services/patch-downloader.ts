import { createHash } from 'sha.js';
import * as fs from 'fs';
import * as path from 'path';
import { LogManager } from '../utils/logger';

const logger = LogManager.getLogger('patch-downloader');

export class PatchDownloader {
  
  static async downloadFile(
    url: string,
    outputPath: string,
    expectedSha256: string,
    onProgress?: (progress: number) => void
  ): Promise<{ success: boolean; message: string }> {
    try {
      logger.info(`Downloading ${url} to ${outputPath}`);
      
      // 确保目录存在
      await fs.promises.mkdir(path.dirname(outputPath)!, { recursive: true });
      
      // 下载文件
      const response = await fetch(url);
      if (!response.ok) {
        return { success: false, message: `HTTP ${response.status}` };
      }
      
      const totalSize = parseInt(response.headers.get('content-length') || '0');
      let downloadedSize = 0;
      
      const fileStream = fs.createWriteStream(outputPath);
      
      return new Promise((resolve) => {
        response.body.on('data', (chunk: Buffer) => {
          fileStream.write(chunk);
          downloadedSize += chunk.length;
          
          if (totalSize > 0 && onProgress) {
            const progress = (downloadedSize / totalSize) * 100;
            onProgress(progress);
          }
        });
        
        response.body.on('end', async () => {
          fileStream.end();
          
          // 验证 SHA-256
          const actualSha256 = await this.calculateSha256(outputPath);
          if (actualSha256 !== expectedSha256.toLowerCase()) {
            await fs.promises.unlink(outputPath);
            resolve({ 
              success: false, 
              message: `SHA-256 mismatch (expected: ${expectedSha256}, actual: ${actualSha256})` 
            });
            return;
          }
          
          resolve({ success: true, message: 'Download complete' });
        });
        
        response.body.on('error', (error) => {
          fileStream.destroy();
          resolve({ success: false, message: error.message });
        });
      });
    } catch (error: any) {
      logger.error(`Download failed: ${error.message}`);
      return { success: false, message: error.message };
    }
  }
  
  static async calculateSha256(filePath: string): Promise<string> {
    const hash = createHash('sha256');
    const stream = fs.createReadStream(filePath);
    
    return new Promise((resolve, reject) => {
      stream.on('data', (chunk) => hash.update(chunk));
      stream.on('end', () => resolve(hash.digest('hex')));
      stream.on('error', reject);
    });
  }
}
