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
        "realmlist.wtf",
        "Data/common.MPQ",
        "Data/common-2.MPQ",
        "Data/expansion.MPQ",
        "Data/lichking.MPQ",
        "Data/patch.MPQ"
    };

    private static readonly string[] CacheDirectories =
    {
        "Cache",
        "WDB",
        "Errors",
        "Logs"
    };

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
            var realmlistPath = Path.Combine(clientPath, "realmlist.wtf");
            
            // 备份原文件
            if (File.Exists(realmlistPath))
            {
                var backupPath = $"{realmlistPath}.backup";
                if (!File.Exists(backupPath))
                {
                    File.Copy(realmlistPath, backupPath);
                }
            }

            // 写入新的 realmlist
            File.WriteAllText(realmlistPath, "set realmlist 1.14.59.54\n");
            
            return (true, "Realmlist 已修复为: set realmlist 1.14.59.54");
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
