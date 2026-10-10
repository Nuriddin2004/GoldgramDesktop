import colorsys
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1]).resolve()
UPSTREAM = json.loads((ROOT / 'upstream.json').read_text())
assert subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip() == UPSTREAM['commit'], 'Unexpected upstream revision'


def replace(relative, old, new, count=1):
    path = SOURCE / relative
    text = path.read_text(encoding='utf-8')
    assert text.count(old) == count, f'{relative}: expected {count} occurrences of {old!r}'
    path.write_bytes(text.replace(old, new).replace('\n', '\r\n').encode('utf-8'))


CPP = 'Telegram/SourceFiles/'
replace('Telegram/CMakeLists.txt', 'init_non_host_target(Telegram)', 'init_non_host_target(Telegram)\nset_target_properties(Telegram PROPERTIES OUTPUT_NAME Goldgram)')
for old, new in [
    ('{53F49750-6209-4FBF-9CA8-7A333C87D1ED}', '{20B4C804-581E-4EAA-94DC-4DAB9D176EB7}'),
    ('"Telegram Win (Unofficial)"', '"Goldgram Desktop Legacy"'),
    ('"Telegram Desktop"', '"Goldgram Desktop"'),
    ('"Telegram"', '"Goldgram"'),
    ('"7.3"', '"7.3-Goldgram.1"'),
]:
    replace(CPP + 'core/version.h', old, new)

for relative, old, new, count in [
    ('config.h', '{87A94AB0-E370-4cde-98D3-ACC110C5967D}', '{0E347910-7317-41D5-A89B-23B09F501379}', 1),
    ('core/launcher.cpp', 'u"TelegramDesktop"_q', 'u"GoldgramDesktop"_q', 1),
    ('core/launcher.cpp', 'u"TelegramForcePortable"_q', 'u"GoldgramForcePortable"_q', 2),
    ('core/launcher.cpp', 'u"TelegramAlpha_data"_q', 'u"GoldgramAlpha_data"_q', 1),
    ('core/launcher.cpp', 'u"TelegramBeta_data"_q', 'u"GoldgramBeta_data"_q', 1),
    ('intro/intro_start.cpp', 'u"Telegram Desktop"_q', 'u"Goldgram Desktop"_q', 1),
    ('boxes/about_box.cpp', 'u"Telegram Desktop"_q', 'u"Goldgram Desktop"_q', 1),
    ('boxes/about_box.cpp', '"https://github.com/telegramdesktop/tdesktop"', '"https://github.com/Nuriddin2004/GoldgramDesktop"', 1),
    ('core/application.cpp', 'https://telegramdesktop.github.io/tdesktop/changelog/', 'https://github.com/Nuriddin2004/GoldgramDesktop/releases/latest', 1),
    ('window/window_main_menu.cpp', 'u"Telegram Desktop"_q', 'u"Goldgram Desktop"_q', 1),
    ('window/window_main_menu.cpp', 'https://desktop.telegram.org', 'https://t.me/GoldgramTG', 1),
    ('window/main_window.cpp', 'u"Telegram"_q', 'u"Goldgram"_q', 1),
    ('window/window_saved_windows.cpp', 'u"Telegram"_q', 'u"Goldgram"_q', 1),
    ('window/window_restore_shell.cpp', 'u"Telegram"_q', 'u"Goldgram"_q', 1),
    ('window/notifications_manager_default.cpp', 'u"Telegram Desktop"_q', 'u"Goldgram Desktop"_q', 1),
    ('core/crash_report_window.cpp', 'u"Telegram"_q', 'u"Goldgram"_q', 1),
    ('platform/win/windows_app_user_model_id.cpp', 'Telegram.TelegramDesktop', 'Goldgram.GoldgramDesktop', 2),
    ('platform/win/windows_app_user_model_id.cpp', 'Telegram.lnk', 'Goldgram.lnk', 4),
    ('platform/win/windows_app_user_model_id.cpp', 'TelegramAlpha.lnk', 'GoldgramAlpha.lnk', 1),
    ('platform/win/windows_app_user_model_id.cpp', 'u"Telegram Desktop/', 'u"Goldgram Desktop/', 1),
    ('platform/win/windows_app_user_model_id.cpp', 'u"Telegram Win (Unofficial)/', 'u"Goldgram Desktop Legacy/', 1),
    ('platform/win/windows_toast_activator.h', 'F11932D3-6110-4BBC-9B02-B2EC07A1BD19', 'AC942B68-FA3E-4806-ABDB-56D692942D75', 2),
    ('storage/localstorage.cpp', 'const auto NightByDefault = Platform::IsMacStoreBuild();', 'const auto NightByDefault = true;', 1),
]:
    replace(CPP + relative, old, new, count)

replace(CPP + 'logs.cpp', '''#if (!defined Q_OS_WIN && !defined _DEBUG) || defined Q_OS_WINRT || defined OS_WIN_STORE || defined OS_MAC_STORE
		cForceWorkingDir(psAppDataPath());
#else // (!Q_OS_WIN && !_DEBUG) || Q_OS_WINRT || OS_WIN_STORE || OS_MAC_STORE
		cForceWorkingDir(cExeDir());
		if (!LogsData->openMain()) {
			cForceWorkingDir(psAppDataPath());
		}
#endif // (!Q_OS_WIN && !_DEBUG) || Q_OS_WINRT || OS_WIN_STORE || OS_MAC_STORE''', '\t\tcForceWorkingDir(psAppDataPath());')
replace(CPP + 'logs.cpp', '\tMoveOldDataFiles(launcher.initialWorkingDir());', '')

replace('Telegram/Resources/winrc/Telegram.rc', '"Telegram Desktop"', '"Goldgram Desktop"', 2)
replace('Telegram/Resources/winrc/Telegram.rc', '"Telegram FZ-LLC"', '"Goldgram / Nuriddin2004"')

anchor = '\taddText(Text3());'
links = '''

	for (const auto &url : {
		u"https://t.me/GoldgramTG"_q,
		u"https://t.me/GoldgramTGChat"_q,
	}) {
		const auto link = layout->add(
			object_ptr<Ui::LinkButton>(box, url, st::aboutVersionLink),
			st::boxRowPadding);
		link->setClickedCallback([=] { File::OpenUrl(url); });
	}
'''
replace(CPP + 'boxes/about_box.cpp', anchor, anchor + links)

for icon in (ROOT / 'assets').glob('icon*'):
    (SOURCE / 'Telegram/Resources/art' / icon.name).write_bytes(icon.read_bytes())

theme_path = SOURCE / 'Telegram/Resources/night.tdesktop-theme'
with zipfile.ZipFile(theme_path) as archive:
    palette = archive.read('colors.tdesktop-theme').decode('utf-8')


def gold_color(match):
    value = match.group(0)[1:]
    r, g, b = (int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if 0.48 < h < 0.73 and s > 0.14:
        if v < 0.36:
            r, g, b = colorsys.hsv_to_rgb(0.12, min(s, 0.1), v * 0.8)
        else:
            r, g, b = colorsys.hsv_to_rgb(0.12, 0.64, max(v, 0.72))
        return '#' + ''.join(f'{round(c * 255):02x}' for c in (r, g, b)) + value[6:]
    return match.group(0)


palette = re.sub(r'#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b', gold_color, palette)
overrides = {
    'windowBg': '#171717', 'windowBgOver': '#252420',
    'windowBgActive': '#e9bb55', 'windowFgActive': '#171717',
    'windowActiveTextFg': '#e9bb55', 'windowSubTextFg': '#aaa79e',
    'windowSubTextFgOver': '#c6c1b5',
    'activeButtonBg': '#e9bb55', 'activeButtonBgOver': '#f1cb75',
    'activeButtonBgRipple': '#d4a747', 'activeButtonFg': '#171717',
    'activeButtonFgOver': '#171717', 'activeButtonSecondaryFg': '#302711',
    'dialogsBgActive': '#574622', 'dialogsNameFgActive': '#ffffff',
    'dialogsTextFgActive': '#eee8da', 'dialogsDateFgActive': '#eee8da',
    'msgOutBg': '#44391f', 'msgOutBgSelected': '#635127',
    'msgInBg': '#252525', 'msgInBgSelected': '#3b3932',
}
for key, value in overrides.items():
    palette, count = re.subn(rf'^{key}: [^;]+;', f'{key}: {value};', palette, flags=re.M)
    if count != 1:
        raise ValueError(f'Missing palette key: {key}')
with zipfile.ZipFile(theme_path, 'w', zipfile.ZIP_DEFLATED) as archive:
    archive.writestr('colors.tdesktop-theme', palette)
    archive.write(ROOT / 'assets/background.png', 'background.png')
(ROOT / 'assets/Goldgram.tdesktop-theme').write_bytes(theme_path.read_bytes())
print('Goldgram branding, Windows identity, links and default gold theme applied.')
