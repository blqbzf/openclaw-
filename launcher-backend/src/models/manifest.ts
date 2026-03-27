export interface Patch {
  id: string;
  path: string;
  size: number;
  sha256: string;
  required: boolean;
  downloadUrl: string;
  description: string;
}

export interface NewsItem {
  id: string;
  title: string;
  content: string;
  date: string;
  author: string;
}

export interface ServerInfo {
  name: string;
  realm: string;
  port: number;
}

export interface ClientInfo {
  minVersion: string;
  build: number;
  exe: string;
  realmlist: string;
}

export interface VersionInfo {
  launcherVersion: string;
  backendVersion: string;
  minClientVersion: string;
}

export interface Manifest {
  version: string;
  lastUpdated: string;
  serverInfo: ServerInfo;
  clientInfo: ClientInfo;
  requiredFiles: string[];
  allowedPatterns: string[];
  patches: Patch[];
  realmlist: {
    content: string;
    encoding: string;
  };
  news: NewsItem[];
  versionInfo: VersionInfo;
}
