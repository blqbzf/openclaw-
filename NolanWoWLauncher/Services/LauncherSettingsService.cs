using System;
using System.IO;
using Newtonsoft.Json;

namespace NolanWoWLauncher.Services;

public class LauncherSettings
{
    public string ClientPath { get; set; } = string.Empty;
}

public class LauncherSettingsService
{
    private readonly string _settingsPath;

    public LauncherSettingsService()
    {
        var appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
        var settingsDir = Path.Combine(appData, "NolanWoWLauncher");
        Directory.CreateDirectory(settingsDir);
        _settingsPath = Path.Combine(settingsDir, "settings.json");
    }

    public LauncherSettings Load()
    {
        try
        {
            if (!File.Exists(_settingsPath))
                return new LauncherSettings();

            var json = File.ReadAllText(_settingsPath);
            return JsonConvert.DeserializeObject<LauncherSettings>(json) ?? new LauncherSettings();
        }
        catch
        {
            return new LauncherSettings();
        }
    }

    public void Save(LauncherSettings settings)
    {
        var json = JsonConvert.SerializeObject(settings, Formatting.Indented);
        File.WriteAllText(_settingsPath, json);
    }
}
