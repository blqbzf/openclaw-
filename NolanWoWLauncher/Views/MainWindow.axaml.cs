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
    private readonly PatchService _patchService;

    public MainWindow()
    {
        InitializeComponent();
        
        // 直接创建并设置 ViewModel
        _viewModel = new MainViewModel();
        DataContext = _viewModel;
        
        // 创建补丁服务
        _patchService = new PatchService();
        
#if DEBUG
        this.AttachDevTools();
#endif
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    // 选择目录按钮点击事件
    private async void OnSelectClientClick(object? sender, RoutedEventArgs e)
    {
        var topLevel = TopLevel.GetTopLevel(this);
        if (topLevel == null)
        {
            _viewModel.StatusMessage = "❌ 无法打开文件选择对话框";
            return;
        }

        try
        {
            var folders = await topLevel.StorageProvider.OpenFolderPickerAsync(new FolderPickerOpenOptions
            {
                Title = "选择 WoW 3.3.5a 客户端目录",
                AllowMultiple = false
            });

            if (folders.Count > 0)
            {
                var folderPath = folders[0].Path.LocalPath;

                // 验证是否是有效的WoW目录
                var hasWowExe = File.Exists(Path.Combine(folderPath, "Wow.exe"));
                var hasDataDir = Directory.Exists(Path.Combine(folderPath, "Data"));

                if (hasWowExe || hasDataDir)
                {
                    _viewModel.ClientPath = folderPath;
                    _viewModel.StatusMessage = $"✅ 已选择: {folderPath}";

                    // 自动修复realmlist
                    OnFixRealmlistClick(sender, e);
                }
                else
                {
                    _viewModel.StatusMessage = "❌ 无效的WoW客户端目录，请选择包含Wow.exe或Data文件夹的目录";
                }
            }
        }
        catch (System.Exception ex)
        {
            _viewModel.StatusMessage = $"❌ 选择目录失败: {ex.Message}";
        }
    }

    // 注册账号按钮点击事件
    private async void OnRegisterClick(object? sender, RoutedEventArgs e)
    {
        try
        {
            var dialog = new RegisterDialog
            {
                DataContext = _viewModel
            };

            await dialog.ShowDialog(this);
        }
        catch (System.Exception ex)
        {
            _viewModel.StatusMessage = $"❌ 打开注册对话框失败: {ex.Message}";
        }
    }

    // 清除缓存按钮点击事件
    private void OnCleanCacheClick(object? sender, RoutedEventArgs e)
    {
        if (string.IsNullOrWhiteSpace(_viewModel.ClientPath))
        {
            _viewModel.StatusMessage = "⚠️ 请先选择客户端目录";
            return;
        }

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

    // 检查更新按钮点击事件 - 真正调用服务器API
    private async void OnCheckUpdatesClick(object? sender, RoutedEventArgs e)
    {
        if (string.IsNullOrWhiteSpace(_viewModel.ClientPath))
        {
            _viewModel.StatusMessage = "⚠️ 请先选择客户端目录";
            return;
        }

        _viewModel.StatusMessage = "🔄 正在连接服务器检查更新...";
        _viewModel.IsDownloading = true;
        _viewModel.DownloadProgress = 0;

        try
        {
            // 调用真正的补丁服务检查更新
            var patches = await _patchService.CheckForUpdates();
            
            if (patches == null || patches.Length == 0)
            {
                _viewModel.StatusMessage = "✅ 客户端已是最新版本，无需更新";
                _viewModel.IsDownloading = false;
                return;
            }

            _viewModel.StatusMessage = $"📥 发现 {patches.Length} 个补丁需要下载";
            _viewModel.ProgressText = "准备下载...";

            // 下载每个补丁
            for (int i = 0; i < patches.Length; i++)
            {
                var patch = patches[i];
                _viewModel.ProgressText = $"正在下载: {patch.Name} ({i + 1}/{patches.Length})";
                
                var progress = new Progress<(int percentage, string status)>(p =>
                {
                    _viewModel.DownloadProgress = p.percentage;
                    _viewModel.StatusMessage = $"📥 {p.status}";
                });

                var success = await _patchService.DownloadPatch(patch, _viewModel.ClientPath, progress);
                
                if (!success)
                {
                    _viewModel.StatusMessage = $"❌ {patch.Name} 下载失败";
                    break;
                }
                
                _viewModel.StatusMessage = $"✅ {patch.Name} 下载完成 ({i + 1}/{patches.Length})";
            }

            _viewModel.StatusMessage = "✅ 所有补丁已更新完成！";
        }
        catch (System.Exception ex)
        {
            _viewModel.StatusMessage = $"❌ 检查更新失败: {ex.Message}";
        }
        finally
        {
            _viewModel.IsDownloading = false;
            _viewModel.DownloadProgress = 0;
            _viewModel.ProgressText = "";
        }
    }

    // 修复Realmlist
    private void OnFixRealmlistClick(object? sender, RoutedEventArgs e)
    {
        if (string.IsNullOrWhiteSpace(_viewModel.ClientPath))
        {
            _viewModel.StatusMessage = "⚠️ 请先选择客户端目录";
            return;
        }

        try
        {
            var realmlistPath = Path.Combine(_viewModel.ClientPath, "realmlist.wtf");
            
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
            
            _viewModel.StatusMessage = "✅ Realmlist 已修复: set realmlist 1.14.59.54";
        }
        catch (System.Exception ex)
        {
            _viewModel.StatusMessage = $"❌ 修复失败: {ex.Message}";
        }
    }

    // 启动游戏按钮点击事件
    private void OnLaunchGameClick(object? sender, RoutedEventArgs e)
    {
        if (string.IsNullOrWhiteSpace(_viewModel.ClientPath))
        {
            _viewModel.StatusMessage = "⚠️ 请先选择客户端目录";
            return;
        }

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
