using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Avalonia.Platform.Storage;
using NolanWoWLauncher.ViewModels;

namespace NolanWoWLauncher.Views;

public partial class MainWindow : Window
{
    private MainViewModel? _viewModel;

    public MainWindow()
    {
        InitializeComponent();
#if DEBUG
        this.AttachDevTools();
#endif
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
        DataContextChanged += OnDataContextChanged;
    }

    private void OnDataContextChanged(object? sender, System.EventArgs e)
    {
        _viewModel = DataContext as MainViewModel;
    }

    // 选择目录按钮点击事件
    private async void OnSelectClientClick(object? sender, RoutedEventArgs e)
    {
        if (_viewModel == null) return;

        var topLevel = TopLevel.GetTopLevel(this);
        if (topLevel == null) return;

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
                _viewModel.FixRealmlistCommand.Execute(null);
            }
            else
            {
                _viewModel.StatusMessage = "❌ 无效的WoW客户端目录，请选择包含Wow.exe或Data文件夹的目录";
            }
        }
    }

    // 注册账号按钮点击事件
    private async void OnRegisterClick(object? sender, RoutedEventArgs e)
    {
        if (_viewModel == null) return;

        var dialog = new RegisterDialog
        {
            DataContext = _viewModel
        };

        await dialog.ShowDialog(this);
    }
}
