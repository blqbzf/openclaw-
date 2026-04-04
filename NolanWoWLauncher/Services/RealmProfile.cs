namespace NolanWoWLauncher.Services;

public class RealmProfile
{
    public string Key { get; set; } = LauncherChannel.Release;
    public string Name { get; set; } = "正式服";
    public string RealmHost { get; set; } = "43.248.129.172";
    public string PatchChannel { get; set; } = LauncherChannel.Release;

    public override string ToString() => Name;
}
