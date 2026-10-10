import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import zipfile

root = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1]).resolve()
dist = root / 'dist'
dist.mkdir(exist_ok=True)
exe = source / 'out/Debug/Goldgram.exe'
data = exe.read_bytes()
assert data[:2] == b'MZ'
pe = struct.unpack_from('<I', data, 60)[0]
assert data[pe:pe + 4] == b'PE\0\0'
assert struct.unpack_from('<H', data, pe + 4)[0] == 0x8664, 'Expected x64 executable'
version = json.loads((root / 'upstream.json').read_text())['goldgram_version']
with zipfile.ZipFile(dist / f'Goldgram-Windows-{version}-x64.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(exe, 'Goldgram/Goldgram.exe')
    for name in ('LICENSE', 'LEGAL'):
        z.write(source / name, f'Goldgram/{name}')
    z.write(root / 'README.md', 'Goldgram/README.md')
    z.write(root / 'assets/Goldgram.tdesktop-theme', 'Goldgram/Goldgram.tdesktop-theme')
with zipfile.ZipFile(dist / f'Goldgram-Windows-{version}-source.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    repositories = [source]
    status = subprocess.check_output(['git', '-C', str(source), 'submodule', 'status', '--recursive'], text=True)
    for line in status.splitlines():
        assert line[0] == ' ', 'Uninitialized or modified submodule'
        repositories.append(source / line.strip().split()[1])
    for repo in repositories:
        files = subprocess.check_output(['git', '-C', str(repo), 'ls-files', '-z']).decode().split('\0')
        for name in files:
            path = repo / name
            if name and path.is_file():
                z.write(path, 'tdesktop/' + path.relative_to(source).as_posix())
    for name in ('README.md', 'upstream.json', '.github/workflows/windows.yml'):
        z.write(root / name, 'goldgram-build/' + name)
    for directory in ('scripts', 'assets'):
        for path in (root / directory).rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                z.write(path, 'goldgram-build/' + path.relative_to(root).as_posix())
(dist / 'SHA256SUMS.txt').write_text(''.join(
    hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n'
    for p in sorted(dist.glob('*.zip'))), encoding='utf-8')
print('Packaged x64 application, source (including submodules), and SHA256 hashes.')
