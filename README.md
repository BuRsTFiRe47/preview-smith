# 🖼️ Preview Smith

**Stable Diffusion WebUI / Forge gibi arayüzlerin doğrudan gösteremediği MP4/MOV/WEBM önizleme videolarını hareketli WebP/AVIF dosyalarına toplu dönüştüren modern, çift dilli masaüstü uygulaması.**

**A modern, bilingual desktop app that batch-converts MP4/MOV/WEBM preview videos — which UIs like Stable Diffusion WebUI / Forge can't display directly — into animated WebP/AVIF files.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## 🇹🇷 Türkçe

### Neden?

Forge / WebUI gibi arayüzler, LoRA veya checkpoint kapak dosyası olarak `.mp4` videoları doğrudan gösteremez. Çözüm: videoyu hareketli bir `.webp` (veya `.avif`) dosyasına çevirmek — arayüz bunu sıradan bir resim gibi algılar ve animasyonu oynatır.

### Özellikler

- **📦 Toplu Dönüştürme** — Bir klasördeki (isterseniz alt klasörler dahil) tüm `.mp4/.mov/.webm/.mkv` dosyalarını tarar.
- **⚡ Paralel İşlem** — Birden fazla dosyayı aynı anda dönüştürerek (ayarlanabilir işçi sayısı) süreci ciddi ölçüde hızlandırır.
- **🎛️ Ayarlanabilir Kalite/Boyut** — Çıktı formatı (WebP / AVIF), kalite ve maksimum çözünürlük arayüzden kontrol edilir.
- **🌐 4 Dil** — Türkçe / English / 日本語 / 中文 arayüz, açılır menü yerine kaydırmalı (segmented) düğmelerle anında değiştirilir.
- **🎨 Yeni Arayüz (Qt / PySide6)** — Windows, macOS ve Linux'ta aynı görünen modern Qt 6 arayüzü: siyah/mavi degrade vurgulu koyu tema, yuvarlak köşeli kartlar, iOS tarzı anahtarlar (LoRA Librarian ile aynı tasarım). Koyu/açık tema tam destekli.
- **📁 Klasör Geçmişi** — Klasör alanının yanındaki 🕘 simgesiyle son kullanılan klasörler listelenir, her birinin yanında kaldırma (✕) seçeneği vardır.
- **🌗 Karanlık / Aydınlık Tema** — Varsayılan karanlık temayla açılır, tek tıkla aydınlığa geçer.
- **💾 Kalıcı Ayarlar** — Dil, tema, pencere boyutu, en son kullanılan klasör ve tüm dönüştürme tercihleri otomatik hatırlanır.
- **🛑 İptal Desteği** — Devam eden bir dönüştürme işlemini istediğiniz an güvenle durdurabilirsiniz.

### Gereksinimler

- Python 3.10+
- Sisteminizde kurulu **ffmpeg** ([ffmpeg.org](https://ffmpeg.org/download.html)) — PATH'te olması ya da uygulamanın yanına konması yeterli; macOS'ta Homebrew (`brew install ffmpeg`) ve Linux'ta paket yöneticisi kurulumları otomatik bulunur.
- AVIF çıktısı için ffmpeg derlemenizin `libaom-av1` desteği olmalı (çoğu güncel ffmpeg dağıtımında mevcuttur).

### Kurulum

```bash
git clone https://github.com/BuRsTFiRe47/preview-smith.git
cd preview-smith
pip install -r requirements.txt
python main.py
```

Hazır derlemeleri (**Windows / macOS / Linux**) sağdaki **Releases** bölümünden indirebilirsiniz. Ayarlar Windows'ta uygulamanın yanındaki `ayarlar.json` dosyasında, macOS/Linux'ta kullanıcı yapılandırma klasöründe saklanır.

> 🍎 **macOS:** imzasız uygulamayı ilk açışta *sağ tık → Aç* ile başlatın. 🐧 **Linux:** `PreviewSmith/PreviewSmith` dosyasını çalıştırın (gerekirse `chmod +x`).

> ⚠️ **Windows Defender uyarısı hakkında:** PyInstaller ile derlenen Python programları, kendini geçici klasöre açma davranışı yüzünden bazen Defender tarafından yanlışlıkla "Trojan:Win32/Wacatac.B!ml" olarak işaretlenir — bu, PyInstaller tabanlı binlerce açık kaynak projede görülen bilinen bir yanlış pozitiftir, gerçek bir virüs değildir. Kaynak kodun tamamı bu depoda açık; isterseniz kendiniz derleyebilir ya da [dosyayı VirusTotal'da tarayabilirsiniz](https://www.virustotal.com/).

### Kullanım

1. Videoların bulunduğu klasörü seçin.
2. İsterseniz alt klasörleri de taramayı, orijinal dosyayı silmeyi, çıktı formatını, kaliteyi, maksimum boyutu ve paralel işçi sayısını ayarlayın.
3. "DÖNÜŞTÜRMEYİ BAŞLAT" düğmesine basın ve canlı işlem kaydını takip edin.

---

## 🇬🇧 English

### Why?

UIs like Forge / WebUI can't display `.mp4` videos directly as a LoRA or checkpoint cover. The fix: convert the video into an animated `.webp` (or `.avif`) file — the UI treats it as a normal image and plays the animation.

### Features

- **📦 Batch Conversion** — Scans a folder (optionally including subfolders) for all `.mp4/.mov/.webm/.mkv` files.
- **⚡ Parallel Processing** — Converts multiple files at once (configurable worker count), significantly speeding up the process.
- **🎛️ Adjustable Quality/Size** — Output format (WebP / AVIF), quality, and maximum resolution are all controlled from the UI.
- **🌐 4 Languages** — Turkish / English / 日本語 / 中文 interface, switched instantly with segmented buttons instead of a dropdown menu.
- **🎨 Redesigned UI (Qt / PySide6)** — A modern Qt 6 interface that looks the same on Windows, macOS and Linux: black/blue gradient dark theme, rounded cards, iOS-style toggles (same design as LoRA Librarian). Full dark/light theme support.
- **📁 Folder History** — A 🕘 icon next to the folder field lists recently used folders, each with a remove (✕) option.
- **🌗 Dark / Light Theme** — Opens in dark mode by default, switches to light with a single click.
- **💾 Persistent Settings** — Language, theme, window size, the last-used folder, and all conversion preferences are remembered automatically.
- **🛑 Cancel Support** — Safely stop an in-progress conversion at any time.

### Requirements

- Python 3.10+
- **ffmpeg** installed ([ffmpeg.org](https://ffmpeg.org/download.html)) — on your PATH or dropped next to the app; Homebrew (`brew install ffmpeg`) on macOS and package-manager installs on Linux are found automatically.
- For AVIF output, your ffmpeg build needs `libaom-av1` support (present in most modern ffmpeg distributions).

### Installation

```bash
git clone https://github.com/BuRsTFiRe47/preview-smith.git
cd preview-smith
pip install -r requirements.txt
python main.py
```

Ready-made builds for **Windows / macOS / Linux** are in the **Releases** section on the right. Settings live next to the app in `ayarlar.json` on Windows, and in the per-user config folder on macOS/Linux.

> 🍎 **macOS:** if the app isn't signed, use *right-click → Open* the first time. 🐧 **Linux:** run `PreviewSmith/PreviewSmith` (`chmod +x` if needed).

> ⚠️ **About the Windows Defender warning:** Python programs built with PyInstaller are sometimes flagged by Defender as "Trojan:Win32/Wacatac.B!ml" because of how they self-extract to a temp folder at startup - this is a well-known false positive seen across thousands of PyInstaller-based open-source projects, not an actual virus. The full source is right here in this repo; you're welcome to build it yourself, or [scan the file on VirusTotal](https://www.virustotal.com/).

### Usage

1. Select the folder containing your videos.
2. Optionally enable scanning subfolders, deleting the original file, and set the output format, quality, max size, and parallel worker count.
3. Click "START CONVERSION" and follow the live process log.

---

## 📄 License

MIT — free to use, modify, and distribute. See [LICENSE](LICENSE).
