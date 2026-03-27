import * as winston from 'winston';
import * as path from 'path';
import * as fs from 'fs';

const logsDir = path.join(__dirname, '../../logs');

// 确保 logs 目录存在
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

const logFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.json()
);

const transports = [
  new winston.transports.Console(),
  new winston.transports.File({
    filename: path.join(logsDir, 'launcher-win.log'),
    maxsize: 5242880, // 5MB
    maxFiles: 5,
  })
];

export class LogManager {
  private static loggers: Map<string, winston.Logger> = new Map();

  static getLogger(module: string): winston.Logger {
    if (!this.loggers.has(module)) {
      this.loggers.set(module, winston.createLogger({
        format: logFormat,
        defaultMeta: { service: module },
        transports: transports
      }));
    }
    return this.loggers.get(module)!;
  }
}

export default LogManager;
