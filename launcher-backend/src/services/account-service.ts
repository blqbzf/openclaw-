import { createConnection } from 'mysql2/promise';
import { LogManager } from '../utils/logger';

const logger = LogManager.getLogger('account-service');

export class AccountService {
  /**
   * 注册新账号
   */
  static async register(data: {
    username: string;
    password: string;
    email: string;
  }): Promise<{ success: boolean; message: string; accountId?: number }> {
    const connection = await createConnection({
      host: process.env.DB_HOST || '127.0.0.1',
      port: parseInt(process.env.DB_PORT || '3306'),
      user: process.env.DB_USER || 'acore',
      password: process.env.DB_PASSWORD || 'Acore123456!',
      database: process.env.DB_NAME || 'acore_auth'
    });

    try {
      // 检查用户名是否存在
      const [existing] = await connection.execute(
        'SELECT id FROM account WHERE username = ?',
        [data.username.toUpperCase()]
      ) as any[];

      if (existing.length > 0) {
        return { success: false, message: '用户名已存在' };
      }

      // 生成 SRP6 凭证
      const { salt, verifier } = await this.generateSRP6Credentials(
        data.username,
        data.password
      );

      // 插入新账号
      const result = await connection.execute(
        `INSERT INTO account 
         (username, salt, verifier, email, expansion, reg_mail)
         VALUES (?, ?, ?, ?, 2, ?)`,
        [
          data.username.toUpperCase(),
          salt,
          verifier,
          data.email || `${data.username.toLowerCase()}@nolan.wow`,
          data.email || `${data.username.toLowerCase()}@nolan.wow`
        ]
      ) as any;

      const accountId = result.insertId;

      logger.info(`Account created: ${data.username} (${accountId})`);

      return {
        success: true,
        message: '注册成功',
        accountId
      };
    } catch (error) {
      logger.error('Register error', error);
      return { success: false, message: '注册失败，请稍后重试' };
    } finally {
      await connection.end();
    }
  }

  /**
   * 检查用户名是否可用
   */
  static async checkUsername(username: string): Promise<boolean> {
    const connection = await createConnection({
      host: process.env.DB_HOST || '127.0.0.1',
      port: parseInt(process.env.DB_PORT || '3306'),
      user: process.env.DB_USER || 'acore',
      password: process.env.DB_PASSWORD || 'Acore123456!',
      database: process.env.DB_NAME || 'acore_auth'
    });

    try {
      const [rows] = await connection.execute(
        'SELECT id FROM account WHERE username = ?',
        [username.toUpperCase()]
      ) as any[];

      return rows.length === 0;
    } finally {
      await connection.end();
    }
  }

  /**
   * 生成 AzerothCore SRP6 凭证
   */
  private static async generateSRP6Credentials(
    username: string,
    password: string
  ): Promise<{ salt: Buffer; verifier: Buffer }> {
    const crypto = require('crypto');
    
    // 生成随机 salt (32 bytes)
    const salt = crypto.randomBytes(32);
    
    // 计算 verifier (简化版本)
    const verifier = crypto.createHash('sha256')
      .update(salt)
      .update(Buffer.from(username.toUpperCase()))
      .update(Buffer.from(password.toUpperCase()))
      .digest();
    
    return { salt, verifier };
  }
}
