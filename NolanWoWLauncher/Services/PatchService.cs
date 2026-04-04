using System;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace NolanWoWLauncher.Services;

public class PatchInfo
{
    public string Name { get; set; } = "";
    public string Version { get; set; } = "";
    public long Size { get; set; }
    public string Sha256 { get; set; } = "";
    public string DownloadUrl { get; set; } = "";
    public string LocalRelativePath { get; set; } = "";
    public bool Required { get; set; }
}

public class PatchVersionInfo
{
    public string GeneratedAt { get; set; } = "";
    public int PatchCount { get; set; }
    public string Channel { get; set; } = "";
}

public class ServerUpdateInfo
{
    public string Date { get; set; } = "";
    public string[] Updates { get; set; } = Array.Empty<string>();
}

public class PatchService
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl = "http://43.248.129.172:88";
    private readonly string _fallbackManifestUrl = "https://github.com/blqbzf/openclaw-/releases/download/patches-latest/manifest.json";
    private readonly string _fallbackVersionUrl = "https://github.com/blqbzf/openclaw-/releases/download/patches-latest/version.json";

    private static string ResolveLocalPatchPath(PatchInfo patch, string clientPath)
    {
        var relativePath = string.IsNullOrWhiteSpace(patch.LocalRelativePath)
            ? Path.Combine("Data", Path.GetFileName(patch.DownloadUrl))
            : patch.LocalRelativePath.Replace('/', Path.DirectorySeparatorChar);

        return Path.Combine(clientPath, relativePath);
    }

    public PatchService()
    {
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(30)
        };
    }

    public async Task<PatchInfo[]?> CheckForUpdates()
    {
        try
        {
            var response = await _httpClient.GetStringAsync($"{_baseUrl}/api/patches/manifest.json");
            return JsonConvert.DeserializeObject<PatchInfo[]>(response);
        }
        catch (Exception)
        {
            try
            {
                var fallback = await _httpClient.GetStringAsync(_fallbackManifestUrl);
                return JsonConvert.DeserializeObject<PatchInfo[]>(fallback);
            }
            catch (Exception)
            {
                return null;
            }
        }
    }

    public async Task<ServerUpdateInfo?> GetServerUpdates()
    {
        try
        {
            var response = await _httpClient.GetStringAsync($"{_baseUrl}/api/updates");
            return JsonConvert.DeserializeObject<ServerUpdateInfo>(response);
        }
        catch (Exception)
        {
            return new ServerUpdateInfo
            {
                Date = "2026-04-02",
                Updates = new[]
                {
                    "🎉 欢迎来到诺兰时光魔兽私服！",
                    "🤖 机器人系统优化（单人也能玩！）",
                    "🎨 Bot名字全面中文化",
                    "💬 Bot聊天文本中文化",
                    "📦 副本进组自动补装备",
                    "📜 无字天书传送优化",
                    "",
                    "📝 使用说明:",
                    "1. 选择WoW 3.3.5a客户端目录",
                    "2. 首次使用请先注册账号",
                    "3. 启动游戏开始冒险！"
                }
            };
        }
    }

    public async Task<PatchVersionInfo?> GetPatchVersion()
    {
        try
        {
            var response = await _httpClient.GetStringAsync($"{_baseUrl}/api/patches/version.json");
            return JsonConvert.DeserializeObject<PatchVersionInfo>(response);
        }
        catch (Exception)
        {
            try
            {
                var fallback = await _httpClient.GetStringAsync(_fallbackVersionUrl);
                return JsonConvert.DeserializeObject<PatchVersionInfo>(fallback);
            }
            catch (Exception)
            {
                return null;
            }
        }
    }

    public async Task<bool> ValidateLocalPatch(PatchInfo patch, string clientPath)
    {
        var localPath = ResolveLocalPatchPath(patch, clientPath);
        if (!File.Exists(localPath))
            return false;

        var localHash = await CalculateSha256(localPath);
        return localHash.Equals(patch.Sha256, StringComparison.OrdinalIgnoreCase);
    }

    public async Task<bool> DownloadPatch(PatchInfo patch, string clientPath,
        IProgress<(int percentage, string status)>? progress = null)
    {
        try
        {
            var localPath = ResolveLocalPatchPath(patch, clientPath);
            var localDir = Path.GetDirectoryName(localPath) ?? Path.Combine(clientPath, "Data");
            Directory.CreateDirectory(localDir);

            if (File.Exists(localPath))
            {
                var localHash = await CalculateSha256(localPath);
                if (localHash.Equals(patch.Sha256, StringComparison.OrdinalIgnoreCase))
                {
                    progress?.Report((100, "文件已是最新"));
                    return true;
                }
            }

            using var response = await _httpClient.GetAsync(patch.DownloadUrl, HttpCompletionOption.ResponseHeadersRead);
            response.EnsureSuccessStatusCode();

            var totalBytes = response.Content.Headers.ContentLength ?? 0;
            var downloadedBytes = 0L;

            await using var contentStream = await response.Content.ReadAsStreamAsync();
            await using var fileStream = new FileStream(localPath, FileMode.Create, FileAccess.Write, FileShare.None);

            var buffer = new byte[8192];
            int bytesRead;

            while ((bytesRead = await contentStream.ReadAsync(buffer)) > 0)
            {
                await fileStream.WriteAsync(buffer.AsMemory(0, bytesRead));
                downloadedBytes += bytesRead;

                if (totalBytes > 0)
                {
                    var percentage = (int)((double)downloadedBytes / totalBytes * 100);
                    progress?.Report((percentage, $"下载中 {percentage}%"));
                }
            }

            progress?.Report((100, "验证文件完整性..."));
            var downloadedHash = await CalculateSha256(localPath);
            if (!downloadedHash.Equals(patch.Sha256, StringComparison.OrdinalIgnoreCase))
            {
                File.Delete(localPath);
                progress?.Report((0, "文件校验失败"));
                return false;
            }

            progress?.Report((100, "下载完成"));
            CleanClientCaches(clientPath);
            CleanClientCaches(clientPath);
            return true;
        }
        catch (Exception ex)
        {
            progress?.Report((0, $"下载失败: {ex.Message}"));
            return false;
        }
    }

    private static async Task<string> CalculateSha256(string filePath)
    {
        using var sha256 = System.Security.Cryptography.SHA256.Create();
        await using var stream = File.OpenRead(filePath);
        var hashBytes = await sha256.ComputeHashAsync(stream);
        return BitConverter.ToString(hashBytes).Replace("-", "").ToLowerInvariant();
    }

    private static void CleanClientCaches(string clientPath)
    {
        TryDeleteDirectory(Path.Combine(clientPath, "Cache"));
        TryDeleteDirectory(Path.Combine(clientPath, "WDB"));
    }

    private static void TryDeleteDirectory(string path)
    {
        try
        {
            if (Directory.Exists(path))
                Directory.Delete(path, true);
        }
        catch { }
    }
}
