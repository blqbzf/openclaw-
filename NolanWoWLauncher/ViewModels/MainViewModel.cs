using System.Threading.Tasks;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using NolanWoWLauncher.Services;

namespace NolanWoWLauncher.ViewModels;

public partial class MainViewModel : ObservableObject
{
    private readonly ClientService _clientService;
    private readonly AccountService _accountService;
    private readonly PatchService _patchService;

    [ObservableProperty] private string _clientPath = "";
    [ObservableProperty] private string _statusMessage = "就绪";
    [ObservableProperty] private int _downloadProgress;
    [ObservableProperty] private string _progressText = "";
    [ObservableProperty] private bool _isDownloading;
    [ObservableProperty] private string _serverUpdateInfo = "正在获取服务器更新信息...";
    
    [ObservableProperty] private string _registerUsername = "";
    [ObservableProperty] private string _registerPassword = "";
    [ObservableProperty] private string _registerEmail = "";
    [ObservableProperty] private bool _isRegisterDialogOpen;

    public MainViewModel()
    {
        _clientService = new ClientService();
        _accountService = new AccountService();
        _patchService = new PatchService();
        
        // 自动获取服务器更新信息
        _ = LoadServerUpdates();
    }

    private async Task LoadServerUpdates()
    {
        var updateInfo = await _patchService.GetServerUpdates();
        if (updateInfo != null)
        {
            var updatesText = $"📅 {updateInfo.Date}\n";
            foreach (var update in updateInfo.Updates)
            {
                updatesText += $"• {update}\n";
            }
            ServerUpdateInfo = updatesText.TrimEnd('\n');
        }
        else
        {
            ServerUpdateInfo = "无法获取服务器更新信息";
        }
    }

    [RelayCommand]
    private void SelectClient()
    {
        // 在视图中处理文件夹选择对话框
        StatusMessage = "请选择 WoW 客户端目录";
    }
    
    [RelayCommand]
    private void OpenRegisterDialog()
    {
        IsRegisterDialogOpen = true;
    }

    [RelayCommand]
    private void ValidateClient()
    {
        if (string.IsNullOrWhiteSpace(ClientPath))
        {
            StatusMessage = "请先选择客户端目录";
            return;
        }

        if (_clientService.ValidateClient(ClientPath))
        {
            StatusMessage = "✅ 客户端文件完整";
        }
        else
        {
            StatusMessage = "❌ 客户端文件不完整";
        }
    }

    [RelayCommand]
    private void FixRealmlist()
    {
        if (string.IsNullOrWhiteSpace(ClientPath))
        {
            StatusMessage = "请先选择客户端目录";
            return;
        }

        var (success, message) = _clientService.FixRealmlist(ClientPath);
        StatusMessage = success ? $"✅ {message}" : $"❌ {message}";
    }

    [RelayCommand]
    private void CleanCache()
    {
        if (string.IsNullOrWhiteSpace(ClientPath))
        {
            StatusMessage = "请先选择客户端目录";
            return;
        }

        var (success, message, _) = _clientService.CleanCache(ClientPath);
        StatusMessage = success ? $"✅ {message}" : $"❌ {message}";
    }

    [RelayCommand]
    private async Task CheckForUpdates()
    {
        if (string.IsNullOrWhiteSpace(ClientPath))
        {
            StatusMessage = "请先选择客户端目录";
            return;
        }

        StatusMessage = "正在检查更新...";
        IsDownloading = true;
        
        var patches = await _patchService.CheckForUpdates();
        
        if (patches == null || patches.Length == 0)
        {
            StatusMessage = "✅ 暂无可用更新";
            IsDownloading = false;
            return;
        }

        StatusMessage = $"发现 {patches.Length} 个补丁需要更新";
        
        // 开始下载
        for (int i = 0; i < patches.Length; i++)
        {
            var patch = patches[i];
            ProgressText = $"正在下载: {patch.Name} ({i + 1}/{patches.Length})";
            
            var progress = new Progress<(int percentage, string status)>(p =>
            {
                DownloadProgress = p.percentage;
                StatusMessage = p.status;
            });

            var success = await _patchService.DownloadPatch(patch, ClientPath, progress);
            
            if (!success)
            {
                StatusMessage = $"❌ {patch.Name} 下载失败";
                break;
            }
        }

        IsDownloading = false;
        DownloadProgress = 0;
        ProgressText = "";
        StatusMessage = "✅ 所有补丁已更新完成";
    }

    [RelayCommand]
    private void LaunchGame()
    {
        if (string.IsNullOrWhiteSpace(ClientPath))
        {
            StatusMessage = "请先选择客户端目录";
            return;
        }

        if (_clientService.LaunchGame(ClientPath))
        {
            StatusMessage = "✅ 游戏已启动";
        }
        else
        {
            StatusMessage = "❌ 启动游戏失败";
        }
    }

    [RelayCommand]
    private void OpenRegisterDialog()
    {
        IsRegisterDialogOpen = true;
    }

    [RelayCommand]
    private async Task Register()
    {
        if (string.IsNullOrWhiteSpace(RegisterUsername) || string.IsNullOrWhiteSpace(RegisterPassword))
        {
            StatusMessage = "请填写用户名和密码";
            return;
        }

        var (success, message) = await _accountService.Register(RegisterUsername, RegisterPassword, RegisterEmail);
        
        StatusMessage = success ? $"✅ {message}" : $"❌ {message}";
        
        if (success)
        {
            IsRegisterDialogOpen = false;
            RegisterUsername = "";
            RegisterPassword = "";
            RegisterEmail = "";
        }
    }

    [RelayCommand]
    private void CloseRegisterDialog()
    {
        IsRegisterDialogOpen = false;
    }
}
