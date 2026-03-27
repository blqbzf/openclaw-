import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import { LogManager } from '../utils/logger';

const logger = LogManager.getLogger('main');

let mainWindow: BrowserWindow | null = null;

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true
    },
    icon: path.join(__dirname, '../assets/icon.png'),
    title: '诺兰时光魔兽 - 登录器',
  });

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../build/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  logger.info('Application started', {
    version: app.getVersion(),
    platform: process.platform,
  });

  createWindow();
  registerIpcHandlers();
});

function registerIpcHandlers(): void {
  ipcMain.handle('select-client-directory', async () => {
    // TODO: 实现选择目录对话框
    return { success: true, path: '' };
  });

  ipcMain.handle('scan-client', async (event, clientPath: string) => {
    // TODO: 实现客户端扫描
    return { success: true, result: {} };
  });

  ipcMain.handle('fix-realmlist', async (event, clientPath: string) => {
    // TODO: 实现 realmlist 修复
    return { success: true };
  });

  ipcMain.handle('clean-cache', async (event, clientPath: string) => {
    // TODO: 实现缓存清理
    return { success: true, cleanedSize: 0 };
  });

  ipcMain.handle('get-manifest', async () => {
    // TODO: 实现 manifest 获取
    return { success: true, manifest: {} };
  });

  ipcMain.handle('download-patch', async (event, patchId: string, clientPath: string) => {
    // TODO: 实现补丁下载
    return { success: true };
  });

  ipcMain.handle('register-account', async (event, data: any) => {
    // TODO: 实现账号注册
    return { success: true };
  });

  ipcMain.handle('launch-game', async (event, clientPath: string) => {
    // TODO: 实现游戏启动
    return { success: true };
  });
}

app.on('window-all-closed', () => {
  app.quit();
});
