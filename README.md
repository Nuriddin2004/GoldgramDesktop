# Goldgram Desktop

Nuriddin2004 uchun Windows x64 Telegram mijozi. Telegram Desktop 7.3.0 asosida.

Windows yig‘ilishi hali sinov bosqichida. Goldgram.exe tayyorligi GitHub Actions natijasi bilan tasdiqlanadi.

## Ishlatish

ZIP faylni alohida papkaga oching va Goldgram.exe ni ishga tushiring. Telefon raqami yoki QR orqali kiring. API ID/hash so‘ralmaydi. Akkaunt ma’lumotlari `%APPDATA%/Goldgram Desktop` ichida saqlanadi. Ilovani rasmiy Telegram papkasiga joylamang.

Boshlang‘ich mavzu qora-oltin. Sozlamalardan mavzu va tilni o‘zgartirish mumkin. Tarjimalar Telegram Desktop til paketlaridan olinadi; to‘liq o‘zbekcha qamrov hali tekshirilmagan.

Menyuning pastidagi Goldgram yozuvi kanalni, versiya raqami esa Goldgram Desktop relizlarini ochadi. Yangilanishni yuklab, ilovani yoping va yangi EXE bilan almashtiring. Bu versiyada avtomatik yangilash yo‘q.

- Kanal: https://t.me/GoldgramTG
- Chat: https://t.me/GoldgramTGChat
- Yuklab olish: https://github.com/Nuriddin2004/GoldgramDesktop/releases

Androiddagi AyuGram imkoniyatlari, yashirin chatlar va alohida chat PIN ushbu dastlabki Windows versiyasiga kiritilmagan. Telegram Premium server imkoniyatlari oddiy akkauntga berilmaydi.

## Manba va yig‘ish

`upstream.json` manbaning aniq commitini belgilaydi. `scripts/apply_branding.py` toza upstream checkoutga Goldgram o‘zgarishlarini qo‘llaydi; mos kelmagan manbada to‘xtaydi. Skriptni bir checkoutga faqat bir marta ishlating. Belgilar mavjud Goldgram Android vektoridan `scripts/generate_assets.py` bilan yaratilgan; u Pillow talab qiladi. Yig‘ish uchun belgilar tayyor holda saqlangan.

`.github/workflows/windows.yml` Windows x64 Debug yig‘ilishini bajaradi. GitHub repository Secrets ichida `TELEGRAM_API_ID` va `TELEGRAM_API_HASH` kerak. Kalitlarni kodga yoki manba arxiviga qo‘shmang. O‘zingiz yig‘sangiz https://my.telegram.org orqali o‘z kalitlaringizni oling.

Mahalliy yig‘ish: upstream `docs/building-win.md` bo‘yicha MSVC 14.44 va Windows SDK 10.0.26100.0 ni tayyorlang; manbani TBuild/tdesktop ichiga submodullari bilan oling; branding skriptini qo‘llang; `win.bat skip-release silent qt6`, so‘ng workflowdagi configure/build buyruqlarini bajaring. Natija: `out/Debug/Goldgram.exe`.

Asl Telegram updateri va crash-report yuborish o‘chirilgan. Windows ilova identifikatori, bildirishnoma CLSID va yorliqlari Goldgram uchun alohida.

## Litsenziya

Goldgram o‘zgarishlari GPL-3.0 litsenziyasida. Telegram Desktop va uning kutubxonalari tegishli mualliflariga tegishli. Asl LICENSE, LEGAL va manbadagi mualliflik qaydlari saqlanadi. Har bir tarqatiladigan EXE uchun o‘zgartirilgan manba, submodullar va yig‘ish skriptlari alohida source.zip bilan beriladi. Goldgram Telegramning rasmiy mahsuloti emas.
