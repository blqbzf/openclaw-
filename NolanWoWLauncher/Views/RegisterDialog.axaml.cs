using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using NolanWoWLauncher.ViewModels;

namespace NolanWoWLauncher.Views;

public partial class RegisterDialog : Window
{
    private MainViewModel? _viewModel;

    public RegisterDialog()
    {
        InitializeComponent();
        DataContextChanged += OnDataContextChanged;
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    private void OnDataContextChanged(object? sender, System.EventArgs e)
    {
        _viewModel = DataContext as MainViewModel;
    }

    private async void OnRegisterClick(object? sender, RoutedEventArgs e)
    {
        if (_viewModel == null) return;
        
        // 执行注册命令
        if (_viewModel.RegisterCommand.CanExecute(null))
        {
            _viewModel.RegisterCommand.Execute(null);
        }
        
        // 如果注册成功，关闭对话框
        await Task.Delay(100); // 等待状态更新
        
        if (_viewModel.StatusMessage.Contains("成功"))
        {
            Close();
        }
    }

    private void OnCancelClick(object? sender, RoutedEventArgs e)
    {
        Close();
    }
}
