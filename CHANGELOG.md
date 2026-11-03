# Changelog

## 🇹🇷 Türkçe

### 🎨 v2.2.1 — Tema ayarı
- Koyu tema zemin rengi `#181826`; vurgu (buton) rengi daha koyu ve kırmızıya yakın bir tona çekildi (karanlıkta göz almasın diye).

### 🎨 v2.2.0 — KDE Breeze Dark esinli yeni tasarım + klasör geçmişi açılır liste
- Arayüz, paylaşılan görsel (KDE "Application Style" ekranı) ölçülerek yeniden tasarlandı: arduvaz zemin `#2c3746`, kontrol yüzeyi `#323e4f`, ince çerçeve `#606974`, mercan vurgu `#f77067`; düz ve sakin görünüm, gradient şerit kaldırıldı.
- Kenar çubuğunda tam genişlikte düz mercan "seçili" satır; renkli emoji'ler menüden kaldırıldı (tek renkli, sade görünüm).
- iOS tarzı anahtarlar yerine **Breeze tarzı onay kutuları**; ince kaydırıcı (yuvarlak tutamaç), ince ilerleme çubuğu (mercan çerçeveli), ince oklu açılır menüler, ana işlem düğmeleri tek renk (mercan). Açık tema da aynı tasarımın açık karşılığı.
- **Klasör geçmişi artık ayrı pencere değil, açılır liste:** klasör alanının içindeki ▾ oka tıklayınca son klasörler listelenir; tek tıkla seçilir, ✕ ile kaldırılır. İşlem başlatılırken elle yazılan geçerli klasör de geçmişe eklenir.
- Tema ve bileşenler `breeze.py` içinde toplandı (iki uygulamada aynı).

### v2.1.0 — PySide6 (Qt 6): Windows + macOS + Linux
- customtkinter yerine **PySide6**; üç işletim sisteminde aynı modern görünüm (LoRA Librarian ile aynı tasarım: siyah/mavi tema, iOS tarzı anahtarlar, koyu/açık tema, 4 dil, klasör geçmişi).
- Kod ikiye ayrıldı: `engine.py` (ffmpeg bulma, tarama, dönüştürme, ayarlar) ve `main.py` (yalnızca arayüz).
- **ffmpeg bulma iyileştirildi:** PATH'e ek olarak uygulamanın yanındaki `ffmpeg` ve Homebrew / paket yöneticisi konumları (`/opt/homebrew/bin`, `/usr/local/bin` …) aranıyor — macOS'ta Finder'dan açılan uygulamalar kabuk PATH'ini görmediği için eskiden ffmpeg "bulunamadı" hatası alınırdı.
- Ayarlar: Windows'ta eskisi gibi uygulamanın yanında; macOS/Linux'ta kullanıcı yapılandırma klasöründe.
- GitHub Actions üç platform için derliyor: `PreviewSmith-windows.zip`, `-macos.zip`, `-linux.zip`.
- Dönüştürme başlarken log temizleniyor, bitince buton otomatik "Başlat"a dönüyor.

## 🇬🇧 English

### 🎨 v2.2.1 — Theme tweak
- Dark theme background is now `#181826`; the accent (button) colour is darker and redder so it isn't glaring in the dark.

### 🎨 v2.2.0 — KDE Breeze Dark-inspired redesign + folder history dropdown
- The UI was redesigned from a shared reference screenshot (KDE "Application Style" page) using measured colours: slate background `#2c3746`, control surface `#323e4f`, thin border `#606974`, coral accent `#f77067`; a flat, calm look, gradient strip removed.
- Full-width flat coral "selected" row in the sidebar; colourful emoji removed from the menu (monochrome, clean look).
- **Breeze-style checkboxes** instead of iOS toggles; thin slider with round handle, thin progress bar (coral outline), thin-chevron dropdowns, single-colour primary action buttons. The light theme is the matching light variant.
- **Folder history is now a dropdown, not a separate window:** click the ▾ arrow inside the folder field to list recent folders; pick with one click, remove with ✕. A valid folder you typed by hand is added to the history when you start a run.
- Theme and widgets live in `breeze.py` (identical in both apps).

### v2.1.0 — PySide6 (Qt 6): Windows + macOS + Linux
- **PySide6** replaces customtkinter; same modern look on all three OSes (same design as LoRA Librarian: black/blue theme, iOS-style toggles, dark/light theme, 4 languages, folder history).
- Code split into `engine.py` (ffmpeg lookup, scanning, conversion, settings) and `main.py` (UI only).
- **Better ffmpeg discovery:** besides PATH, it now checks for an `ffmpeg` next to the app and Homebrew / package-manager locations (`/opt/homebrew/bin`, `/usr/local/bin` …) — apps launched from Finder on macOS don't see the shell PATH, so ffmpeg used to be reported as missing.
- Settings: next to the app on Windows as before; in the per-user config folder on macOS/Linux.
- GitHub Actions builds for all three platforms: `PreviewSmith-windows.zip`, `-macos.zip`, `-linux.zip`.
- The log is cleared when a conversion starts, and the button returns to "Start" when it ends.
