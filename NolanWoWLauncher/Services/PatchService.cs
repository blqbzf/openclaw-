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
    public bool Required { get; set; }
}

public class ServerUpdateInfo
{
    public string Date { get; set; } = "";
    public string[] Updates { get; set; } = Array.Empty<string>();
}

public class PatchService
{
    private readonly HttpClient _httpClient;
    private readonly string _serverUrl = "http://1.14.59.54:8080";

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
            var response = await _httpClient.GetStringAsync($"{_serverUrl}/api/patches/manifest");
            return JsonConvert.DeserializeObject<PatchInfo[]>(response);
        }
        catch (Exception)
        {
            return null;
        }
    }

    public async Task<ServerUpdateInfo?> GetServerUpdates()
    {
        try
        {
            var response = await _httpClient.GetStringAsync($"{_serverUrl}/api/updates");
            return JsonConvert.DeserializeObject<ServerUpdateInfo>(response);
        }
        catch (Exception)
        {
            return new ServerUpdateInfo
            {
                Date = DateTime.Now.ToString("yyyy-MM-dd"),
                Updates = new[] { "服务器连接失败" }
            };
        }
    }

    public async Task<bool> DownloadPatch(PatchInfo patch, string clientPath,
        IProgress<(int percentage, string status)>? progress = null)
    {
        try
        {
            var fileName = Path.GetFileName(patch.DownloadUrl);
            var localPath = Path.Combine(clientPath, "Data", fileName);

            // 检查文件是否已存在且哈希匹配
            if (File.Exists(localPath))
            {
                var localHash = await CalculateSha256(localPath);
                if (localHash.Equals(patch.Sha256, StringComparison.OrdinalIgnoreCase))
                {
                    progress?.Report((100, "文件已是最新"));
                    return true;
                }
            }

            // 下载文件
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

            // 验证哈希
            progress?.Report((100, "验证文件完整性..."));
            var downloadedHash = await CalculateSha256(localPath);
            
            if (!downloadedHash.Equals(patch.Sha256, StringComparison.OrdinalIgnoreCase))
            {
                File.Delete(localPath);
                progress?.Report((0, "文件校验失败"));
                return false;
            }

            progress?.Report((100, "下载完成"));
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
}
