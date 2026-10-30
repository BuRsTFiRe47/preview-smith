# Changelog

## 🇹🇷 Türkçe

### v2.1.0 — PySide6 (Qt 6): Windows + macOS + Linux
- customtkinter yerine **PySide6**; üç işletim sisteminde aynı modern görünüm (LoRA Librarian ile aynı tasarım: siyah/mavi tema, iOS tarzı anahtarlar, koyu/açık tema, 4 dil, klasör geçmişi).
- Kod ikiye ayrıldı: `engine.py` (ffmpeg bulma, tarama, dönüştürme, ayarlar) ve `main.py` (yalnızca arayüz).
- **ffmpeg bulma iyileştirildi:** PATH'e ek olarak uygulamanın yanındaki `ffmpeg` ve Homebrew / paket yöneticisi konumları (`/opt/homebrew/bin`, `/usr/local/bin` …) aranıyor — macOS'ta Finder'dan açılan uygulamalar kabuk PATH'ini görmediği için eskiden ffmpeg "bulunamadı" hatası alınırdı.
- Ayarlar: Windows'ta eskisi gibi uygulamanın yanında; macOS/Linux'ta kullanıcı yapılandırma klasöründe.
- GitHub Actions üç platform için derliyor: `PreviewSmith-windows.zip`, `-macos.zip`, `-linux.zip`.
- Dönüştürme başlarken log temizleniyor, bitince buton otomatik "Başlat"a dönüyor.

## 🇬🇧 English

### v2.1.0 — PySide6 (Qt 6): Windows + macOS + Linux
- **PySide6** replaces customtkinter; same modern look on all three OSes (same design as LoRA Librarian: black/blue theme, iOS-style toggles, dark/light theme, 4 languages, folder history).
- Code split into `engine.py` (ffmpeg lookup, scanning, conversion, settings) and `main.py` (UI only).
- **Better ffmpeg discovery:** besides PATH, it now checks for an `ffmpeg` next to the app and Homebrew / package-manager locations (`/opt/homebrew/bin`, `/usr/local/bin` …) — apps launched from Finder on macOS don't see the shell PATH, so ffmpeg used to be reported as missing.
- Settings: next to the app on Windows as before; in the per-user config folder on macOS/Linux.
- GitHub Actions builds for all three platforms: `PreviewSmith-windows.zip`, `-macos.zip`, `-linux.zip`.
- The log is cleared when a conversion starts, and the button returns to "Start" when it ends.
