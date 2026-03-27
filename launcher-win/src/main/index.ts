import { app, BrowserWindow, ipcMain } from 'electron';
import * as path from 'path';
import * as fs from 'fs';
import { LogManager } from './utils/logger';

import { Config } from './config/config';
import { IpcChannels } from './common/ipc-channels';

// 初始化日志
const logger = LogManager.getLogger('main');

// 初始化配置
const config = Config.getInstance();

// 主窗口
let mainWindow: BrowserWindow | null = null;

function createWindow(): void {
  // 创建主窗口
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

  // 加载 React 应用
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../build/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Electron 应用就绪
app.whenReady().then(() => {
  logger.info('Application started', {
    version: app.getVersion(),
    platform: process.platform,
  });

  createWindow();

  // 注册 IPC 处理程序
  registerIpcHandlers();
});

// IPC 处理程序
function registerIpcHandlers(): void {
  // 选择客户端目录
  ipcMain.handle(IpcChannels.SELECTClientDirectory, async () => {
    const result = await require('./services/client-service').selectClientDirectory();
    return result;
  });

  // 扫描客户端
  ipcMain.handle(IpcChannels.scanClient, async (clientPath: string) => {
    const result = await require('./services/client-service').scanClient(clientPath);
    return result;
  });

  // 修复 realmlist
  ipcMain.handle(IpcChannels.fixRealmlist, async (clientPath: string) => {
    const result = await require('./services/client-service').fixRealmlist(clientPath);
    return result;
  });

  // 清理缓存
  ipcMain.handle(IpcChannels.cleanCache, async (clientPath: string) => {
    const result = await require('./services/client-service').cleanCache(clientPath);
    return result;
  });

  // 获取 manifest
  ipcMain.handle(IpcChannels.getManifest, async () => {
    const result = await require('./services/patch-service').getManifest();
    return result;
  });

  // 下载补丁
  ipcMain.handle(IpcChannels.downloadPatch, async (patchId: string, clientPath: string) => {
    const result = await require('./services/patch-service').downloadPatch(patchId, clientPath);
    return result;
  });

  // 注册账号
  ipcMain.handle(IpcChannels.registerAccount, async (data: any) => {
    const result = await require('./services/api-service').registerAccount(data);
    return result;
  });

  // 启动游戏
  ipcMain.handle(IpcChannels.launchGame, async (clientPath: string) => {
    const result = await require('./services/game-service').launchGame(clientPath);
    return result;
  });
}

app.on('window-all-closed', () => {
  app.quit();
});
