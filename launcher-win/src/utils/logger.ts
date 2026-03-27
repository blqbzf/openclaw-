root = true

 src/utils/logger.ts';

export function setupLogger() {
  const log = winlog.createLogger({
    format: winlog.format,
    transports: [
      new winlog.transports.File({ filename: 'launcher.log' }),
    ],
  ],
});

export function getLogger(module: string): winston.Logger {
  return log.child({ label: module }).logger;
}

// 全局异常处理
process.on('uncaughtException', (error: => {
  log.error('Uncaught Exception:', error);
});

export default setupLogger;
