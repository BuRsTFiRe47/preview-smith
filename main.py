# -*- coding: utf-8 -*-
"""
Preview Smith
=============
Stable Diffusion WebUI / Forge gibi arayüzlerin doğrudan gösteremediği
MP4/MOV/WEBM önizleme videolarını, arayüzlerin kapak resmi gibi
algıladığı hareketli WebP/AVIF dosyalarına toplu olarak dönüştüren
modern, çift dilli masaüstü uygulaması.

A modern, bilingual desktop app that batch-converts MP4/MOV/WEBM
preview videos (which UIs like Stable Diffusion WebUI / Forge can't
show directly) into animated WebP/AVIF files that those UIs treat as
regular cover images.

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

import customtkinter as ctk
from tkinter import filedialog, messagebox

from lang import t

APP_VERSION = "2.0.0"
VIDEO_EXTENSIONS = (".mp4", ".mov", ".webm", ".mkv")

ACCENT = ("#0a6ea6", "#00b4ff")
LOG_BG = ("#f2f2f2", "#121212")
CARD_BG = ("#e8e8e8", "#2b2b2b")


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


SETTINGS_PATH = os.path.join(app_dir(), "ayarlar.json")


def ffmpeg_available():
    return shutil.which("ffmpeg") is not None


class PreviewSmithApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lang = "tr"
        self.theme = "dark"
        self.is_running = False
        self.cancel_event = threading.Event()

        self.folder_path = ctk.StringVar()
        self.scan_subfolders = ctk.BooleanVar(value=False)
        self.delete_source = ctk.BooleanVar(value=True)
        self.output_format = ctk.StringVar(value="webp")
        self.quality = ctk.IntVar(value=60)
        self.max_size = ctk.IntVar(value=384)
        self.workers = ctk.IntVar(value=3)

        self.ayarlari_yukle()
        ctk.set_appearance_mode(self.theme)
        self.geometry(getattr(self, "_pending_geometry", "750x680"))

        self.arayuz_ciz()
        self.protocol("WM_DELETE_WINDOW", self.kapatirken_kaydet)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def arayuz_ciz(self):
        for w in self.winfo_children():
            w.destroy()

        self.title(t("app_title", self.lang))

        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(15, 0))

        theme_values = [t("theme_dark", self.lang), t("theme_light", self.lang)]
        self.theme_seg = ctk.CTkSegmentedButton(top_bar, values=theme_values, command=self._on_theme_change)
        self.theme_seg.set(t("theme_dark", self.lang) if self.theme == "dark" else t("theme_light", self.lang))
        self.theme_seg.pack(side="right", padx=(10, 0))

        lang_values = [t("lang_tr", self.lang), t("lang_en", self.lang)]
        self.lang_seg = ctk.CTkSegmentedButton(top_bar, values=lang_values, command=self._on_lang_change)
        self.lang_seg.set(t("lang_tr", self.lang) if self.lang == "tr" else t("lang_en", self.lang))
        self.lang_seg.pack(side="right")

        # Folder picker
        folder_frame = ctk.CTkFrame(self, fg_color=CARD_BG)
        folder_frame.pack(fill="x", padx=20, pady=(15, 10))
        ctk.CTkLabel(folder_frame, text=t("target_folder_label", self.lang), font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        entry_row = ctk.CTkFrame(folder_frame, fg_color="transparent")
        entry_row.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        folder_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkEntry(entry_row, textvariable=self.folder_path, width=480).pack(side="left", fill="x", expand=True)
        ctk.CTkButton(entry_row, text=t("browse", self.lang), width=90, command=self.browse_folder).pack(side="left", padx=(10, 0))

        # Options
        opts_frame = ctk.CTkFrame(self, fg_color=CARD_BG)
        opts_frame.pack(fill="x", padx=20, pady=(0, 10))

        switches_row = ctk.CTkFrame(opts_frame, fg_color="transparent")
        switches_row.pack(fill="x", padx=10, pady=10)
        ctk.CTkSwitch(switches_row, text=t("switch_subfolders", self.lang), variable=self.scan_subfolders).pack(side="left")
        ctk.CTkSwitch(switches_row, text=t("switch_delete_source", self.lang), variable=self.delete_source).pack(side="left", padx=(30, 0))

        grid_row = ctk.CTkFrame(opts_frame, fg_color="transparent")
        grid_row.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(grid_row, text=t("output_format_label", self.lang)).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        ctk.CTkSegmentedButton(grid_row, values=["WebP", "AVIF"], command=lambda v: self.output_format.set(v.lower()),
                                width=140).grid(row=0, column=1, sticky="w", pady=5)
        self._set_segmented(grid_row.grid_slaves(row=0, column=1)[0], "WebP" if self.output_format.get() == "webp" else "AVIF")

        ctk.CTkLabel(grid_row, text=t("quality_label", self.lang)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        q_frame = ctk.CTkFrame(grid_row, fg_color="transparent")
        q_frame.grid(row=1, column=1, sticky="w", pady=5)
        q_lbl = ctk.CTkLabel(q_frame, text=str(self.quality.get()), width=30)
        ctk.CTkSlider(q_frame, from_=10, to=100, number_of_steps=90, variable=self.quality,
                      command=lambda v: q_lbl.configure(text=str(int(v)))).pack(side="left")
        q_lbl.pack(side="left", padx=(10, 0))

        ctk.CTkLabel(grid_row, text=t("max_size_label", self.lang)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        s_frame = ctk.CTkFrame(grid_row, fg_color="transparent")
        s_frame.grid(row=2, column=1, sticky="w", pady=5)
        s_lbl = ctk.CTkLabel(s_frame, text=str(self.max_size.get()), width=30)
        ctk.CTkSlider(s_frame, from_=128, to=768, number_of_steps=40, variable=self.max_size,
                      command=lambda v: s_lbl.configure(text=str(int(v)))).pack(side="left")
        s_lbl.pack(side="left", padx=(10, 0))

        ctk.CTkLabel(grid_row, text=t("workers_label", self.lang)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=5)
        w_frame = ctk.CTkFrame(grid_row, fg_color="transparent")
        w_frame.grid(row=3, column=1, sticky="w", pady=5)
        w_lbl = ctk.CTkLabel(w_frame, text=str(self.workers.get()), width=30)
        ctk.CTkSlider(w_frame, from_=1, to=8, number_of_steps=7, variable=self.workers,
                      command=lambda v: w_lbl.configure(text=str(int(v)))).pack(side="left")
        w_lbl.pack(side="left", padx=(10, 0))

        # Start / cancel button
        self.btn_start = ctk.CTkButton(self, text=t("btn_start", self.lang), fg_color="#0b5b7a", hover_color="#157199",
                                        command=self.start_conversion_thread)
        self.btn_start.pack(fill="x", padx=20, pady=(0, 10), ipady=5)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, progress_color=ACCENT)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 15))
        self.progress_bar.set(0)

        # Log
        self.log_area = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 11), text_color=ACCENT, fg_color=LOG_BG)
        self.log_area.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        if not ffmpeg_available():
            self.log(t("log_ffmpeg_missing", self.lang))

    def _set_segmented(self, widget, value):
        try:
            widget.set(value)
        except Exception:
            pass

    def _on_lang_change(self, value):
        self.lang = "tr" if value == t("lang_tr", self.lang) else "en"
        self.arayuz_ciz()

    def _on_theme_change(self, value):
        self.theme = "dark" if value == t("theme_dark", self.lang) else "light"
        ctk.set_appearance_mode(self.theme)

    def browse_folder(self):
        folder = filedialog.askdirectory(title=t("browse_dialog_title", self.lang))
        if folder:
            self.folder_path.set(folder)

    # ------------------------------------------------------------------
    # Settings persistence
    # ------------------------------------------------------------------
    def ayarlari_yukle(self):
        if not os.path.exists(SETTINGS_PATH):
            return
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
            self.lang = d.get("lang", "tr")
            self.theme = d.get("theme", "dark")
            self._pending_geometry = d.get("geometry", "750x680")
            self.folder_path.set(d.get("folder", ""))
            self.scan_subfolders.set(d.get("scan_subfolders", False))
            self.delete_source.set(d.get("delete_source", True))
            self.output_format.set(d.get("output_format", "webp"))
            self.quality.set(d.get("quality", 60))
            self.max_size.set(d.get("max_size", 384))
            self.workers.set(d.get("workers", 3))
        except Exception:
            pass

    def kapatirken_kaydet(self):
        d = {
            "lang": self.lang,
            "theme": self.theme,
            "geometry": self.geometry(),
            "folder": self.folder_path.get(),
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
        self.destroy()

    # ------------------------------------------------------------------
    # Logging helpers (thread-safe via .after)
    # ------------------------------------------------------------------
    def log(self, message):
        self.after(0, self._append_log, message)

    def _append_log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.configure(state="disabled")

    def set_progress(self, value):
        self.after(0, self.progress_bar.set, value)

    # ------------------------------------------------------------------
    # Conversion engine
    # ------------------------------------------------------------------
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
        self.after(0, lambda: self.btn_start.configure(text=t("btn_cancel", self.lang), fg_color="#b5261a", hover_color="#d63424"))
        self.log_area.configure(state="normal")
        self.log_area.delete("1.0", "end")
        self.log_area.configure(state="disabled")

        threading.Thread(target=self.process_files, daemon=True).start()

    def _convert_one(self, video_file: Path, fmt: str, quality: int, max_size: int, delete_source: bool):
        out_ext = ".webp" if fmt == "webp" else ".avif"
        out_file = video_file.with_suffix(out_ext)

        scale = f"scale='min({max_size},iw)':'min({max_size},ih)':force_original_aspect_ratio=decrease"
        if fmt == "webp":
            cmd = [
                "ffmpeg", "-y", "-i", str(video_file),
                "-vf", scale,
                "-vcodec", "libwebp", "-lossless", "0", "-q:v", str(quality), "-loop", "0",
                str(out_file),
            ]
        else:  # avif
            cmd = [
                "ffmpeg", "-y", "-i", str(video_file),
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
        folder = Path(self.folder_path.get())
        self.log(t("log_scanning", self.lang, folder=str(folder)))

        files = []
        walker = folder.rglob("*") if self.scan_subfolders.get() else folder.glob("*")
        for p in walker:
            if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS:
                files.append(p)

        total_files = len(files)
        if total_files == 0:
            self.log(t("log_no_files", self.lang))
            self.finish_process()
            return

        self.log(t("log_total_found", self.lang, count=total_files) + "\n" + "=" * 50)

        fmt = self.output_format.get()
        quality = self.quality.get()
        max_size = self.max_size.get()
        delete_source = self.delete_source.get()
        worker_count = max(1, self.workers.get())

        success_count = 0
        fail_count = 0
        done_count = 0

        def task(idx, video_file):
            if self.cancel_event.is_set():
                return None
            self.log(t("log_processing", self.lang, index=idx + 1, total=total_files, name=video_file.name))
            ok, msg = self._convert_one(video_file, fmt, quality, max_size, delete_source)
            return ok, msg

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
                self.set_progress(done_count / total_files)

        if self.cancel_event.is_set():
            self.log(t("log_cancelled", self.lang))

        self.log("=" * 50)
        self.log(t("log_summary_title", self.lang))
        self.log(t("log_summary_success", self.lang, count=success_count))
        self.log(t("log_summary_fail", self.lang, count=fail_count))
        self.log(t("log_all_done", self.lang))

        self.finish_process()

    def finish_process(self):
        self.is_running = False
        self.after(0, lambda: self.btn_start.configure(text=t("btn_start", self.lang), fg_color="#0b5b7a", hover_color="#157199"))


if __name__ == "__main__":
    app = PreviewSmithApp()
    app.mainloop()
