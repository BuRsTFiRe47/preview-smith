# -*- coding: utf-8 -*-
"""
Preview Smith - engine
======================
UI'dan bağımsız (Qt içermeyen) dönüştürme mantığı: ffmpeg bulma, video
tarama, WebP/AVIF dönüştürme, ayar kaydı.

UI-independent (Qt-free) conversion logic: locating ffmpeg, scanning for
videos, WebP/AVIF conversion, settings persistence.

License: MIT
"""

import os
import sys
import json
import shutil
import subprocess
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from lang import t

APP_VERSION = "2.1.0"
VIDEO_EXTENSIONS = (".mp4", ".mov", ".webm", ".mkv")

LANG_CODES = ["tr", "en", "ja", "zh"]
LANG_LABELS = {"tr": "Türkçe", "en": "English", "ja": "日本語", "zh": "中文"}


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def data_dir():
    """Settings folder. Windows (or an existing ayarlar.json next to the
    app): next to the app, as before. macOS / Linux: per-user config
    folder, since the app folder is often read-only there."""
    d = app_dir()
    if os.path.exists(os.path.join(d, "ayarlar.json")) or sys.platform.startswith("win"):
        return d
    if sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    p = os.path.join(base, "PreviewSmith")
    try:
        os.makedirs(p, exist_ok=True)
    except Exception:
        return d
    return p


SETTINGS_PATH = os.path.join(data_dir(), "ayarlar.json")

# GUI apps launched from Finder / a desktop launcher don't inherit the
# shell PATH, so Homebrew / package-manager ffmpeg installs are invisible.
_EXTRA_PATHS = ["/opt/homebrew/bin", "/usr/local/bin", "/opt/local/bin", "/usr/bin", "/snap/bin"]


def find_ffmpeg():
    exe = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
    local = os.path.join(app_dir(), exe)          # ffmpeg dropped next to the app
    if os.path.isfile(local):
        return local
    found = shutil.which("ffmpeg")
    if found:
        return found
    for d in _EXTRA_PATHS:
        cand = os.path.join(d, exe)
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    return None


def ffmpeg_available():
    return find_ffmpeg() is not None


class StringVar:
    def __init__(self, value=""):
        self._v = value
    def get(self):
        return self._v
    def set(self, v):
        self._v = v


class BooleanVar(StringVar):
    def set(self, v):
        self._v = bool(v)


class IntVar(StringVar):
    def set(self, v):
        self._v = int(v)


class Engine:
    def __init__(self):
        # callbacks (UI replaces these)
        self.on_log = lambda msg: None
        self.on_progress = lambda frac: None
        self.on_running = lambda running: None

        self.lang = "tr"
        self.theme = "dark"
        self.is_running = False
        self.cancel_event = threading.Event()

        self.folder_path = StringVar()
        self.klasor_gecmisi = []
        self.scan_subfolders = BooleanVar(False)
        self.delete_source = BooleanVar(True)
        self.output_format = StringVar("webp")
        self.quality = IntVar(60)
        self.max_size = IntVar(384)
        self.workers = IntVar(3)
        self._pending_geometry = "750x720"
        self.ayarlari_yukle()

    # ------------------------------------------------------------ settings
    def ayarlari_yukle(self):
        if not os.path.exists(SETTINGS_PATH):
            return
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
            self.lang = d.get("lang", "tr")
            self.theme = d.get("theme", "dark")
            self._pending_geometry = d.get("geometry", "750x720")
            self.folder_path.set(d.get("folder", ""))
            self.klasor_gecmisi = d.get("recent_folders", [])
            self.scan_subfolders.set(d.get("scan_subfolders", False))
            self.delete_source.set(d.get("delete_source", True))
            self.output_format.set(d.get("output_format", "webp"))
            self.quality.set(d.get("quality", 60))
            self.max_size.set(d.get("max_size", 384))
            self.workers.set(d.get("workers", 3))
        except Exception:
            pass

    def ayarlari_kaydet(self, geometry=""):
        d = {
            "lang": self.lang,
            "theme": self.theme,
            "geometry": geometry,
            "folder": self.folder_path.get(),
            "recent_folders": self.klasor_gecmisi,
            "scan_subfolders": self.scan_subfolders.get(),
            "delete_source": self.delete_source.get(),
            "output_format": self.output_format.get(),
            "quality": self.quality.get(),
            "max_size": self.max_size.get(),
            "workers": self.workers.get(),
        }
        try:
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def _gecmise_ekle(self, yol):
        if not yol:
            return
        if yol in self.klasor_gecmisi:
            self.klasor_gecmisi.remove(yol)
        self.klasor_gecmisi.insert(0, yol)
        self.klasor_gecmisi = self.klasor_gecmisi[:12]

    # ---------------------------------------------------------- conversion
    def log(self, message):
        self.on_log(message)

    def start_conversion_thread(self):
        if self.is_running:
            self.cancel_event.set()
            return
        if not self.folder_path.get():
            self.log(t("log_no_folder", self.lang))
            return
        if not ffmpeg_available():
            self.log(t("log_ffmpeg_missing", self.lang))
            return

        self.is_running = True
        self.cancel_event.clear()
        self.on_running(True)
        threading.Thread(target=self.process_files, daemon=True).start()

    def _convert_one(self, video_file: Path, fmt: str, quality: int, max_size: int, delete_source: bool):
        out_ext = ".webp" if fmt == "webp" else ".avif"
        out_file = video_file.with_suffix(out_ext)
        ffmpeg = find_ffmpeg() or "ffmpeg"

        scale = f"scale='min({max_size},iw)':'min({max_size},ih)':force_original_aspect_ratio=decrease"
        if fmt == "webp":
            cmd = [
                ffmpeg, "-y", "-i", str(video_file),
                "-vf", scale,
                "-vcodec", "libwebp", "-lossless", "0", "-q:v", str(quality), "-loop", "0",
                str(out_file),
            ]
        else:  # avif
            cmd = [
                ffmpeg, "-y", "-i", str(video_file),
                "-vf", scale,
                "-c:v", "libaom-av1", "-crf", str(max(0, 63 - int(quality * 0.6))), "-b:v", "0",
                str(out_file),
            ]

        try:
            kwargs = {}
            if os.name == "nt":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                kwargs["startupinfo"] = startupinfo

            result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)

            if result.returncode == 0 and out_file.exists():
                size_kb = out_file.stat().st_size / 1024
                if delete_source:
                    os.remove(video_file)
                    return True, t("log_converted", self.lang, size=f"{size_kb:.0f} KB")
                return True, t("log_converted_kept", self.lang, size=f"{size_kb:.0f} KB")
            return False, t("log_error_kept", self.lang)
        except Exception as e:
            return False, t("log_system_error", self.lang, error=str(e))

    def process_files(self):
        try:
            self._process_files()
        finally:
            self.is_running = False
            self.on_running(False)

    def _process_files(self):
        folder = Path(self.folder_path.get())
        self.on_progress(0.0)
        self.log(t("log_scanning", self.lang, folder=str(folder)))

        files = []
        walker = folder.rglob("*") if self.scan_subfolders.get() else folder.glob("*")
        for p in walker:
            if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS:
                files.append(p)

        total_files = len(files)
        if total_files == 0:
            self.log(t("log_no_files", self.lang))
            return

        self.log(t("log_total_found", self.lang, count=total_files) + "\n" + "=" * 50)

        fmt = self.output_format.get()
        quality = self.quality.get()
        max_size = self.max_size.get()
        delete_source = self.delete_source.get()
        worker_count = max(1, self.workers.get())

        success_count = fail_count = done_count = 0

        def task(idx, video_file):
            if self.cancel_event.is_set():
                return None
            self.log(t("log_processing", self.lang, index=idx + 1, total=total_files, name=video_file.name))
            return self._convert_one(video_file, fmt, quality, max_size, delete_source)

        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = {executor.submit(task, i, f): f for i, f in enumerate(files)}
            for future in as_completed(futures):
                if self.cancel_event.is_set():
                    break
                result = future.result()
                if result is None:
                    continue
                ok, msg = result
                self.log(msg)
                if ok:
                    success_count += 1
                else:
                    fail_count += 1
                done_count += 1
                self.on_progress(done_count / total_files)

        if self.cancel_event.is_set():
            self.log(t("log_cancelled", self.lang))

        self.log("=" * 50)
        self.log(t("log_summary_title", self.lang))
        self.log(t("log_summary_success", self.lang, count=success_count))
        self.log(t("log_summary_fail", self.lang, count=fail_count))
        self.log(t("log_all_done", self.lang))
