using System.IO;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Avalonia.Platform.Storage;
using NolanWoWLauncher.ViewModels;

namespace NolanWoWLauncher.Views;

public partial class MainWindow : Window
{
    private readonly MainViewModel _viewModel;

    public MainWindow()
    {
        InitializeComponent();

        _viewModel = new MainViewModel();
        DataContext = _viewModel;

#if DEBUG
        this.AttachDevTools();
#endif
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

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

            if (folders.Count <= 0)
                return;

            var folderPath = folders[0].Path.LocalPath;
            var hasWowExe = File.Exists(Path.Combine(folderPath, "Wow.exe"));
            var hasDataDir = Directory.Exists(Path.Combine(folderPath, "Data"));

            if (!hasWowExe && !hasDataDir)
            {
                _viewModel.StatusMessage = "❌ 无效的WoW客户端目录，请选择包含Wow.exe或Data文件夹的目录";
                return;
            }

            _viewModel.ClientPath = folderPath;
            _viewModel.StatusMessage = $"✅ 已选择: {folderPath}";
            _viewModel.FixRealmlistCommand.Execute(null);
        }
        catch (System.Exception ex)
        {
            _viewModel.StatusMessage = $"❌ 选择目录失败: {ex.Message}";
        }
    }

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
}
