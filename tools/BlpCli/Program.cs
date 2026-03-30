using BlpConverter.BLP;

if (args.Length < 2)
{
    Console.Error.WriteLine("Usage: BlpCli <input.png> <output.blp> [dxt1|dxt3|dxt5] [mipmaps]");
    return 1;
}

var input = args[0];
var output = args[1];
var compression = args.Length >= 3 ? args[2].ToLowerInvariant() : "dxt5";
var mipmaps = args.Length >= 4 && int.TryParse(args[3], out var parsed) ? parsed : 0;

var fmt = compression switch
{
    "raw" or "uncompressed" => BlpCompression.Uncompressed,
    "dxt1" => BlpCompression.DXT1,
    "dxt3" => BlpCompression.DXT3,
    _ => BlpCompression.DXT5,
};

RustBlpConverter.ImageToBlp(input, output, fmt, mipmaps);
Console.WriteLine($"OK {input} -> {output} ({fmt}, mipmaps={mipmaps})");
return 0;
