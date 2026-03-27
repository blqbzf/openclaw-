import * as path from 'path';
import * as fs from 'fs';

export class ClientScanner {
  private wowPath: string;
  private requiredFiles: string[] = [
    'Wow.exe',
    'realmlist.wtf',
    'Data/common-2.MPQ',
    'Data/expansion1.MPQ',
    'Data/expansion2.MPQ',
    'Data/expansion3.MPQ',
    'Data/lichking.MPQ',
  ];

  constructor(wowPath: string) {
    this.wowPath = wowPath;
  }

  async scan(): Promise<ScanResult> {
    const result: ScanResult = {
      wowPath: this.wowPath,
      wowExe: false,
      realmlist: false,
      requiredFiles: {} as Record<string, boolean>,
      patches: [],
      conflicts: [],
      isValid: false,
    };

    try {
      // 检查 Wow.exe
      const wowExe = path.join(this.wowPath, 'Wow.exe');
      result.wowExe = await this.fileExists(wowExe);

      // 检查 realmlist.wtf
      const realmlist = path.join(this.wowPath, 'realmlist.wtf');
      result.realmlist = await this.fileExists(realmlist);

      // 检查必需文件
      for (const file of this.requiredFiles) {
        const filePath = path.join(this.wowPath, file);
        result.requiredFiles[file] = await this.fileExists(filePath);
      }

      // 扫描 Data 目录中的 MPQ 文件
      const dataPath = path.join(this.wowPath, 'Data');
      if (await this.directoryExists(dataPath)) {
        const mpqFiles = await this.scanMPQFiles(dataPath);
        result.patches = mpqFiles;
      }

      // 验证客户端有效性
      result.isValid = result.wowExe && result.realmlist;

      return result;
    } catch (error) {
      throw error;
    }
  }

  private async fileExists(filePath: string): Promise<boolean> {
    try {
      await fs.promises.access(filePath, fs.constants.F_OK);
      return true;
    } catch {
      return false;
    }
  }

  private async directoryExists(dirPath: string): Promise<boolean> {
    try {
      const stats = await fs.promises.stat(dirPath);
      return stats.isDirectory();
    } catch {
      return false;
    }
  }

  private async scanMPQFiles(dataPath: string): Promise<string[]> {
    const files: string[] = [];
    const items = await fs.promises.readdir(dataPath);

    for (const item of items) {
      if (item.endsWith('.MPQ') || item.endsWith('.mpq')) {
        files.push(item);
      }
    }

    return files;
  }
}

export interface ScanResult {
  wowPath: string;
  wowExe: boolean;
  realmlist: boolean;
  requiredFiles: Record<string, boolean>;
  patches: string[];
  conflicts: string[];
  isValid: boolean;
}
