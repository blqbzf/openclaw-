using Avalonia.Controls;
using Avalonia.Markup.Xaml;

namespace NolanWoWLauncher.Views;

public partial class RegisterDialog : Window
{
    public RegisterDialog()
    {
        InitializeComponent();
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }
}
