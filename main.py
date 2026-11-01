# -*- coding: utf-8 -*-
"""
Preview Smith
=============
Stable Diffusion WebUI / Forge gibi arayüzlerin doğrudan gösteremediği
MP4/MOV/WEBM önizleme videolarını, arayüzlerin kapak resmi gibi
algıladığı hareketli WebP/AVIF dosyalarına toplu olarak dönüştüren
modern, çift dilli masaüstü uygulaması. Windows / macOS / Linux
(PySide6 / Qt 6).

A modern, bilingual desktop app that batch-converts MP4/MOV/WEBM
preview videos (which UIs like Stable Diffusion WebUI / Forge can't
show directly) into animated WebP/AVIF files that those UIs treat as
regular cover images. Windows / macOS / Linux (PySide6 / Qt 6).

License: MIT
"""

import sys

from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QSlider, QPlainTextEdit,
    QProgressBar, QScrollArea, QFrame, QButtonGroup,
)

from lang import t
from engine import Engine, APP_VERSION, LANG_CODES, LANG_LABELS, ffmpeg_available
from breeze import build_qss, Check, PathField


class Bridge(QObject):
    log = Signal(str)
    progress = Signal(float)
    running = Signal(bool)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.eng = Engine()
        self.bridge = Bridge()
        self.eng.on_log = self.bridge.log.emit
        self.eng.on_progress = self.bridge.progress.emit
        self.eng.on_running = self.bridge.running.emit
        self.bridge.log.connect(self._append_log)
        self.bridge.progress.connect(self._set_progress)
        self.bridge.running.connect(self._set_running)

        self._log_cache = ""
        try:
            w, h = [int(x) for x in str(self.eng._pending_geometry).lower().split("+")[0].split("x")]
            self.resize(max(640, w), max(560, h))
        except Exception:
            self.resize(750, 720)

        self.apply_theme()
        self.build_ui()

    def apply_theme(self):
        QApplication.instance().setStyleSheet(build_qss(self.eng.theme))

    # ------------------------------------------------------------ UI
    def build_ui(self):
        lang = self.eng.lang
        self.setWindowTitle(t("app_title", lang))
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(self._header())

        page = QWidget()
        page.setObjectName("page")
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 8, 0)
        lay.setSpacing(10)

        # folder card
        card = QFrame()
        card.setObjectName("card")
        g = QGridLayout(card)
        g.setContentsMargins(14, 12, 14, 14)
        g.setColumnStretch(0, 1)
        lbl = QLabel(t("target_folder_label", lang))
        lbl.setObjectName("bold")
        g.addWidget(lbl, 0, 0)
        eng = self.eng
        self.path_field = PathField(
            eng.folder_path.get(), eng.folder_path.set, lambda: eng.klasor_gecmisi, eng._gecmise_ekle,
            lambda p: eng.klasor_gecmisi.remove(p) if p in eng.klasor_gecmisi else None,
            t("browse", lang), t("history_window_title", lang), t("history_empty", lang),
            t("browse_dialog_title", lang),
        )
        g.addWidget(self.path_field, 1, 0)
        lay.addWidget(card)

        # options card
        opts = QFrame()
        opts.setObjectName("card")
        ov = QVBoxLayout(opts)
        ov.setContentsMargins(14, 12, 14, 14)
        ov.addWidget(self._switch(t("switch_subfolders", lang), self.eng.scan_subfolders))
        ov.addWidget(self._switch(t("switch_delete_source", lang), self.eng.delete_source))
        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(8)
        grid.addWidget(QLabel(t("output_format_label", lang)), 0, 0)
        grid.addWidget(self._format_seg(), 0, 1, Qt.AlignLeft)
        self._slider_row(grid, 1, t("quality_label", lang), self.eng.quality, 10, 100)
        self._slider_row(grid, 2, t("max_size_label", lang), self.eng.max_size, 128, 768, step=16)
        self._slider_row(grid, 3, t("workers_label", lang), self.eng.workers, 1, 8)
        grid.setColumnStretch(1, 1)
        ov.addSpacing(6)
        ov.addLayout(grid)
        lay.addWidget(opts)

        self.btn_start = QPushButton(t("btn_start", lang))
        self.btn_start.setObjectName("start")
        self.btn_start.setProperty("role", "action")
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.clicked.connect(self._start)
        lay.addWidget(self.btn_start)

        # log card
        logc = QFrame()
        logc.setObjectName("card")
        lv = QVBoxLayout(logc)
        lv.setContentsMargins(14, 12, 14, 12)
        self.progress = QProgressBar()
        self.progress.setRange(0, 1000)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(14)
        lv.addWidget(self.progress)
        self.log_box = QPlainTextEdit()
        self.log_box.setObjectName("log")
        self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(180)
        lv.addWidget(self.log_box, 1)
        lay.addWidget(logc, 1)

        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setWidget(page)
        wrap = QWidget()
        wl = QVBoxLayout(wrap)
        wl.setContentsMargins(16, 14, 8, 12)
        wl.addWidget(sc)
        outer.addWidget(wrap, 1)

        if self._log_cache:
            self.log_box.setPlainText(self._log_cache)
        elif not ffmpeg_available():
            self._append_log(t("log_ffmpeg_missing", lang))
        self._set_running(self.eng.is_running)

    def _header(self):
        header = QFrame()
        header.setObjectName("header")
        h = QHBoxLayout(header)
        h.setContentsMargins(20, 12, 20, 12)
        tv = QVBoxLayout()
        tv.setSpacing(0)
        a = QLabel("Preview Smith")
        a.setObjectName("title")
        b = QLabel(f"v{APP_VERSION}")
        b.setObjectName("version")
        tv.addWidget(a)
        tv.addWidget(b)
        h.addLayout(tv)
        h.addStretch(1)
        lang = self.eng.lang
        h.addWidget(self._segmented([LANG_LABELS[c] for c in LANG_CODES], LANG_CODES.index(lang) if lang in LANG_CODES else 0, self._on_lang))
        h.addSpacing(10)
        h.addWidget(self._segmented([t("theme_dark", lang), t("theme_light", lang)], 0 if self.eng.theme == "dark" else 1, self._on_theme))
        return header

    def _segmented(self, labels, current, on_click):
        box = QWidget()
        h = QHBoxLayout(box)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        grp = QButtonGroup(box)
        grp.setExclusive(True)
        for i, text in enumerate(labels):
            b = QPushButton(text)
            b.setCheckable(True)
            b.setObjectName("seg")
            b.setCursor(Qt.PointingHandCursor)
            b.setChecked(i == current)
            b.clicked.connect(lambda _=False, idx=i: on_click(idx))
            grp.addButton(b, i)
            h.addWidget(b)
        btns = grp.buttons()
        btns[0].setObjectName("segL")
        btns[-1].setObjectName("segR")
        for b in btns:
            b.style().unpolish(b)
            b.style().polish(b)
        box._grp = grp
        return box

    def _format_seg(self):
        return self._segmented(["WebP", "AVIF"], 0 if self.eng.output_format.get() == "webp" else 1,
                               lambda i: self.eng.output_format.set("webp" if i == 0 else "avif"))

    def _switch(self, text, var):
        s = Check(text)
        s.setChecked(bool(var.get()))
        s.toggled.connect(var.set)
        return s

    def _slider_row(self, grid, row, label, var, lo, hi, step=1):
        grid.addWidget(QLabel(label), row, 0)
        box = QHBoxLayout()
        sl = QSlider(Qt.Horizontal)
        sl.setRange(lo // step, hi // step)
        sl.setValue(max(lo, min(hi, int(var.get()))) // step)
        sl.setMinimumWidth(220)
        val = QLabel(str(int(var.get())))
        val.setObjectName("value")
        val.setFixedWidth(40)

        def on(v):
            var.set(v * step)
            val.setText(str(v * step))
        sl.valueChanged.connect(on)
        box.addWidget(sl, 1)
        box.addWidget(val)
        w = QWidget()
        w.setLayout(box)
        box.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(w, row, 1)

    def _start(self):
        """Remember the typed folder too, then start / cancel."""
        import os
        p = self.path_field.text().strip()
        if p and os.path.isdir(p) and not self.eng.is_running:
            self.eng._gecmise_ekle(p)
        self.eng.start_conversion_thread()

    def _on_lang(self, idx):
        code = LANG_CODES[idx]
        if code == self.eng.lang:
            return
        self.eng.lang = code
        self.build_ui()

    def _on_theme(self, idx):
        self.eng.theme = "dark" if idx == 0 else "light"
        self.apply_theme()

    # ------------------------------------------------------- slots
    def _append_log(self, msg):
        self._log_cache += msg + "\n"
        self.log_box.appendPlainText(msg)
        sb = self.log_box.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _set_progress(self, frac):
        self.progress.setValue(int(max(0.0, min(1.0, frac)) * 1000))

    def _set_running(self, running):
        lang = self.eng.lang
        if running:
            self._log_cache = ""
            self.log_box.clear()
            self.btn_start.setText(t("btn_cancel", lang))
            self.btn_start.setObjectName("cancel")
        else:
            self.btn_start.setText(t("btn_start", lang))
            self.btn_start.setObjectName("start")
        self.btn_start.style().unpolish(self.btn_start)
        self.btn_start.style().polish(self.btn_start)

    def closeEvent(self, ev):
        self.eng.cancel_event.set()
        self.eng.ayarlari_kaydet(f"{self.width()}x{self.height()}")
        super().closeEvent(ev)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
