import * as fs from 'fs';
import * as path from 'path';
import { LogManager } from '../utils/logger';
import { Manifest } from '../models/manifest';

const logger = LogManager.getLogger('manifest-service');

export class ManifestService {
  private static manifestPath = path.join(__dirname, '../../data/manifest.json');
  private static manifest: Manifest | null = null;

  static async getManifest(): Promise<Manifest> {
    if (!this.manifest) {
      await this.loadManifest();
    }
    return this.manifest!;
  }

  static async loadManifest(): Promise<void> {
    try {
      const content = await fs.promises.readFile(this.manifestPath, 'utf-8');
      this.manifest = JSON.parse(content);
      logger.info('Manifest loaded successfully');
    } catch (error) {
      logger.error(`Failed to load manifest: ${error.message}`);
      throw error;
    }
  }

  static async reloadManifest(): Promise<void> {
    this.manifest = null;
    await this.loadManifest();
  }
}
