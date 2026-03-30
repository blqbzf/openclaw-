using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Avalonia.Platform.Storage;
using NolanWoWLauncher.Services;
using NolanWoWLauncher.ViewModels;

namespace NolanWoWLauncher.Views;

public partial class MainWindow : Window
{
    private readonly MainViewModel _viewModel;

    public MainWindow()
    {
        InitializeComponent();

        try
        {
            var cacheDir = Path.Combine(_viewModel.ClientPath, "Cache");
            var wdbDir = Path.Combine(_viewModel.ClientPath, "WDB");
            var errorsDir = Path.Combine(_viewModel.ClientPath, "Errors");
            var logsDir = Path.Combine(_viewModel.ClientPath, "Logs");

            long totalBytes = 0;
            var dirsCleaned = 0;

            if (Directory.Exists(cacheDir))
            {
                totalBytes += GetDirectorySize(cacheDir);
                Directory.Delete(cacheDir, true);
                dirsCleaned++;
            }
            if (Directory.Exists(wdbDir))
            {
                totalBytes += GetDirectorySize(wdbDir);
                Directory.Delete(wdbDir, true);
                dirsCleaned++;
            }
            if (Directory.Exists(errorsDir))
            {
                totalBytes += GetDirectorySize(errorsDir);
                Directory.Delete(errorsDir, true);
                dirsCleaned++;
            }
            if (Directory.Exists(logsDir))
            {
                totalBytes += GetDirectorySize(logsDir);
                Directory.Delete(logsDir, true);
                dirsCleaned++;
            }

            var sizeMB = totalBytes / 1024.0 / 1024.0;
            _viewModel.StatusMessage = $"✅ 已清理 {dirsCleaned} 个目录，释放 {sizeMB:F2} MB 空间";
        }
        catch (System.Exception ex)
        {
            _viewModel.StatusMessage = $"❌ 清理缓存失败: {ex.Message}";
        }
    }

        _viewModel.StatusMessage = "🔄 正在连接服务器检查更新...";
        _viewModel.IsDownloading = true;
        _viewModel.DownloadProgress = 0;

        try
        {

        try
        {
            var wowExe = Path.Combine(_viewModel.ClientPath, "Wow.exe");
            
            if (!File.Exists(wowExe))
            {
                _viewModel.StatusMessage = "❌ 找不到 Wow.exe，请确认客户端目录是否正确";
                return;
            }

            System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo
            {
                FileName = wowExe,
                WorkingDirectory = _viewModel.ClientPath,
                UseShellExecute = true
            });

            _viewModel.StatusMessage = "✅ 游戏已启动，祝您游戏愉快！";
        }
        catch (System.Exception ex)
        {
            _viewModel.StatusMessage = $"❌ 启动游戏失败: {ex.Message}";
        }
    }

    // 获取目录大小
    private static long GetDirectorySize(string path)
    {
        if (!Directory.Exists(path)) return 0;
        
        var dirInfo = new DirectoryInfo(path);
        return dirInfo.EnumerateFiles("*", SearchOption.AllDirectories).Sum(f => f.Length);
    }
}
