param([string]$GoldgramBuildRoot = (Join-Path $env:USERPROFILE 'TBuild'))

$ErrorActionPreference = 'Stop'
$buildRoot = [IO.Path]::GetFullPath($GoldgramBuildRoot)
$libraryRoot = (Resolve-Path -LiteralPath (Join-Path $buildRoot 'Libraries/win64')).Path
$expectedRoot = [IO.Path]::GetFullPath((Join-Path $buildRoot 'Libraries/win64'))
if (-not $libraryRoot.Equals($expectedRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Unexpected dependency directory; refusing cleanup.'
}
$prefix = $libraryRoot.TrimEnd('\') + '\'
$keepExtensions = @('.lib', '.a', '.exe', '.dll', '.h', '.hpp', '.inc', '.cmake', '.pc', '.rs', '.toml', '.lock', '.json', '.prl', '.pri')
$removedBytes = [long]0
$removedFiles = 0
Get-ChildItem -LiteralPath $libraryRoot -Recurse -File | ForEach-Object {
    $filePath = [IO.Path]::GetFullPath($_.FullName)
    if (-not $filePath.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "File outside dependency directory: $filePath"
    }
    if ($_.Attributes -band [IO.FileAttributes]::ReparsePoint) { return }
    $relative = $filePath.Substring($prefix.Length).Replace('\', '/')
    $keep = $keepExtensions -contains $_.Extension.ToLowerInvariant()
    $keep = $keep -or $relative -match '(^|/)(include|objects-[^/]+|cache_keys|patches|nv-codec-headers)/'
    if (-not $keep) {
        $removedBytes += $_.Length
        Remove-Item -LiteralPath $filePath -Force
        $removedFiles++
    }
}
Write-Host ('Removed {0} temporary dependency files, freed {1:N2} GiB.' -f $removedFiles, ($removedBytes / 1GB))
Get-PSDrive -Name C, D -ErrorAction SilentlyContinue | Select-Object Name, Used, Free
