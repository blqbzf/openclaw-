using System;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace NolanWoWLauncher.Services;

public class ClientService
{
    private static readonly string[] RequiredFiles =
    {
        "Wow.exe",
        "Data/common.MPQ",
        "Data/common-2.MPQ",
        "Data/expansion.MPQ",
        "Data/lichking.MPQ"
    };

    private static readonly string[] CacheDirectories =
    {
        "Cache",
        "WDB",
        "Errors",
        "Logs"
    };

    // 需要修复的 realmlist 路径（相对于游戏根目录）
    private static readonly string[] RealmlistPaths =
    {
        "realmlist.wtf",
        "Data/zhCN/realmlist.wtf",
        "Data/zhTW/realmlist.wtf",
        "Data/enCN/realmlist.wtf",
        "Data/enTW/realmlist.wtf"
    };

    private const string RealmlistContent = "set realmlist 1.14.59.54";

    public bool ValidateClient(string clientPath)
    {
        if (string.IsNullOrWhiteSpace(clientPath) || !Directory.Exists(clientPath))
            return false;

        return RequiredFiles.All(file => File.Exists(Path.Combine(clientPath, file)));
    }

    public (bool success, string message) FixRealmlist(string clientPath)
    {
        try
        {
            int fixedCount = 0;

            foreach (var relPath in RealmlistPaths)
            {
                var fullPath = Path.Combine(clientPath, relPath);
                var dir = Path.GetDirectoryName(fullPath);

                // 确保父目录存在
                if (!Directory.Exists(dir))
                    Directory.CreateDirectory(dir);

                // 备份原文件
                if (File.Exists(fullPath))
                {
                    var backupPath = fullPath + ".backup";
                    if (!File.Exists(backupPath))
                        File.Copy(fullPath, backupPath);
                }

                File.WriteAllText(fullPath, RealmlistContent + "\n");
                fixedCount++;
            }

            return (true, $"已修复 {fixedCount} 个 realmlist 文件\n服务器: {RealmlistContent}");
        }
        catch (Exception ex)
        {
            return (false, $"修复失败: {ex.Message}");
        }
    }

    public (bool success, string message, long bytesCleaned) CleanCache(string clientPath)
    {
        try
        {
            long totalBytes = 0;

            foreach (var dir in CacheDirectories)
            {
                var dirPath = Path.Combine(clientPath, dir);
                if (Directory.Exists(dirPath))
                {
                    var dirInfo = new DirectoryInfo(dirPath);
                    totalBytes += dirInfo.EnumerateFiles("*", SearchOption.AllDirectories).Sum(f => f.Length);
                    Directory.Delete(dirPath, recursive: true);
                }
            }

            var sizeMB = totalBytes / 1024.0 / 1024.0;
            return (true, $"清理完成，释放 {sizeMB:F2} MB", totalBytes);
        }
        catch (Exception ex)
        {
            return (false, $"清理失败: {ex.Message}", 0);
        }
    }

    public bool LaunchGame(string clientPath)
    {
        try
        {
            // 启动前自动修复 realmlist
            FixRealmlist(clientPath);

            var wowExe = Path.Combine(clientPath, "Wow.exe");
            if (!File.Exists(wowExe))
                return false;

            Process.Start(new ProcessStartInfo
            {
                FileName = wowExe,
                WorkingDirectory = clientPath,
                UseShellExecute = true
            });

            return true;
        }
        catch
        {
            return false;
        }
    }
}
