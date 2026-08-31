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
- **🌗 Karanlık / Aydınlık Tema** — Varsayılan karanlık temayla açılır, tek tıkla aydınlığa geçer.
- **💾 Kalıcı Ayarlar** — Dil, tema, pencere boyutu, en son kullanılan klasör ve tüm dönüştürme tercihleri otomatik hatırlanır.
- **🛑 İptal Desteği** — Devam eden bir dönüştürme işlemini istediğiniz an güvenle durdurabilirsiniz.

### Gereksinimler

- Python 3.10+
- Sisteminizde kurulu ve PATH'e ekli **ffmpeg** ([ffmpeg.org](https://ffmpeg.org/download.html))
- AVIF çıktısı için ffmpeg derlemenizin `libaom-av1` desteği olmalı (çoğu güncel ffmpeg dağıtımında mevcuttur).

### Kurulum

```bash
git clone https://github.com/BuRsTFiRe47/preview-smith.git
cd preview-smith
pip install -r requirements.txt
python main.py
```

Hazır `.exe` dosyasını indirmek isterseniz, sağdaki **Releases** bölümüne bakabilirsiniz.

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
- **🌗 Dark / Light Theme** — Opens in dark mode by default, switches to light with a single click.
- **💾 Persistent Settings** — Language, theme, window size, the last-used folder, and all conversion preferences are remembered automatically.
- **🛑 Cancel Support** — Safely stop an in-progress conversion at any time.

### Requirements

- Python 3.10+
- **ffmpeg** installed and available on your PATH ([ffmpeg.org](https://ffmpeg.org/download.html))
- For AVIF output, your ffmpeg build needs `libaom-av1` support (present in most modern ffmpeg distributions).

### Installation

```bash
git clone https://github.com/BuRsTFiRe47/preview-smith.git
cd preview-smith
pip install -r requirements.txt
python main.py
```

If you'd rather use a ready-made `.exe`, check the **Releases** section on the right.

### Usage

1. Select the folder containing your videos.
2. Optionally enable scanning subfolders, deleting the original file, and set the output format, quality, max size, and parallel worker count.
3. Click "START CONVERSION" and follow the live process log.

---

## 📄 License

MIT — free to use, modify, and distribute. See [LICENSE](LICENSE).
