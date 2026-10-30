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

from PySide6.QtCore import Qt, QObject, Signal, QSize, QRectF
from PySide6.QtGui import QColor, QPainter, QLinearGradient, QBrush
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QSlider, QPlainTextEdit,
    QProgressBar, QScrollArea, QFrame, QFileDialog, QDialog, QButtonGroup,
)

from lang import t
from engine import Engine, APP_VERSION, LANG_CODES, LANG_LABELS, ffmpeg_available

ACCENT = "#2f7bff"
ACCENT_HOVER = "#2569e0"
GRADIENT_STOPS = ["#050814", "#1e3a8a", "#38bdf8"]

PALETTES = {
    "dark": {
        "bg": "#05070c", "header": "#0a0e16", "card": "#0d1119", "hover": "#131a26",
        "text": "#e6ebf5", "side_text": "#a8b3c4", "border": "#1c2432", "log_bg": "#04060a",
        "muted": "#7d8aa0", "input": "#0a0e16", "btn_border": "#2a3547",
    },
    "light": {
        "bg": "#f1f4f9", "header": "#ffffff", "card": "#ffffff", "hover": "#dbe3f1",
        "text": "#16202f", "side_text": "#31435c", "border": "#dde3ee", "log_bg": "#eaeef5",
        "muted": "#5c6b81", "input": "#ffffff", "btn_border": "#ffffff",
    },
}


def build_qss(theme):
    p = PALETTES.get(theme, PALETTES["dark"])
    return f"""
    QWidget {{ color: {p['text']}; font-size: 13px; }}
    QMainWindow, QWidget#root {{ background: {p['bg']}; }}
    QScrollArea {{ border: none; background: transparent; }}
    QScrollArea > QWidget > QWidget {{ background: transparent; }}
    QWidget#page {{ background: transparent; }}
    QFrame#header {{ background: {p['header']}; border: none; }}
    QFrame#card {{ background: {p['card']}; border: 1px solid {p['border']}; border-radius: 14px; }}
    QFrame#card QLabel, QLabel {{ background: transparent; }}
    QLabel#title {{ font-size: 18px; font-weight: 700; }}
    QLabel#version {{ color: {p['muted']}; font-size: 11px; }}
    QLabel#bold {{ font-weight: 700; }}
    QLabel#value {{ color: {ACCENT}; font-weight: 700; }}

    QLineEdit, QPlainTextEdit {{
        background: {p['input']}; border: 1px solid {p['border']}; border-radius: 8px; padding: 7px 10px;
        selection-background-color: {ACCENT}; selection-color: white;
    }}
    QLineEdit:focus, QPlainTextEdit:focus {{ border: 1px solid {ACCENT}; }}
    QPlainTextEdit#log {{
        background: {p['log_bg']}; color: {ACCENT}; font-family: Consolas, Menlo, "DejaVu Sans Mono", monospace;
        font-size: 12px;
    }}

    QPushButton {{
        background: transparent; border: 1px solid {p['border']}; border-radius: 12px; padding: 7px 14px;
        color: {p['side_text']};
    }}
    QPushButton:hover {{ background: {p['hover']}; }}
    QPushButton#seg, QPushButton#segL, QPushButton#segR {{ border: 1px solid {p['border']}; border-radius: 0; padding: 6px 12px; color: {p['side_text']}; margin-left: -1px; }}
    QPushButton#seg:checked, QPushButton#segL:checked, QPushButton#segR:checked {{ background: {ACCENT}; color: white; border: 1px solid {ACCENT}; }}
    QPushButton#segL {{ border-top-left-radius: 12px; border-bottom-left-radius: 12px; margin-left: 0; }}
    QPushButton#segR {{ border-top-right-radius: 12px; border-bottom-right-radius: 12px; }}
    QPushButton#accent {{ background: {ACCENT}; color: white; border: 2px solid {p['btn_border']}; font-weight: 600; }}
    QPushButton#accent:hover {{ background: {ACCENT_HOVER}; }}
    QPushButton#start {{
        background: {ACCENT}; color: white; font-size: 14px; font-weight: 700; border: 2px solid {p['btn_border']};
        border-radius: 14px; padding: 13px 20px;
    }}
    QPushButton#start:hover {{ background: {ACCENT_HOVER}; }}
    QPushButton#cancel {{
        background: #b5261a; color: white; font-size: 14px; font-weight: 700; border: 2px solid {p['btn_border']};
        border-radius: 14px; padding: 13px 20px;
    }}
    QPushButton#cancel:hover {{ background: #d63424; }}
    QPushButton#danger {{ background: #b5261a; color: white; border: none; padding: 5px 10px; }}
    QPushButton#danger:hover {{ background: #d63424; }}
    QPushButton#histitem {{ text-align: left; border: none; }}

    QProgressBar {{ background: {p['log_bg']}; border: 1px solid {p['border']}; border-radius: 8px; color: transparent; }}
    QProgressBar::chunk {{ background: {ACCENT}; border-radius: 7px; }}
    QSlider::groove:horizontal {{ height: 6px; background: {p['border']}; border-radius: 3px; }}
    QSlider::sub-page:horizontal {{ background: {ACCENT}; border-radius: 3px; }}
    QSlider::handle:horizontal {{ background: {ACCENT}; width: 16px; height: 16px; margin: -6px 0; border-radius: 8px; }}
    QScrollBar:vertical {{ background: transparent; width: 10px; margin: 0; }}
    QScrollBar::handle:vertical {{ background: {p['border']}; border-radius: 5px; min-height: 30px; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QDialog {{ background: {p['bg']}; }}
    """


class GradientStrip(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(4)

    def paintEvent(self, _e):
        g = QLinearGradient(0, 0, self.width(), 0)
        n = len(GRADIENT_STOPS) - 1
        for i, c in enumerate(GRADIENT_STOPS):
            g.setColorAt(i / n, QColor(c))
        QPainter(self).fillRect(self.rect(), QBrush(g))


class Switch(QCheckBox):
    W, H = 40, 22

    def __init__(self, text="", theme_getter=lambda: "dark"):
        super().__init__(text)
        self._theme = theme_getter
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(30)

    def sizeHint(self):
        s = super().sizeHint()
        return QSize(self.W + 12 + self.fontMetrics().horizontalAdvance(self.text()) + 4, max(30, s.height()))

    def hitButton(self, pos):
        return self.rect().contains(pos)

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        y = (self.height() - self.H) / 2
        track = QRectF(1, y, self.W, self.H)
        on = self.isChecked()
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(ACCENT) if on else QColor(120, 130, 150, 120))
        p.drawRoundedRect(track, self.H / 2, self.H / 2)
        d = self.H - 6
        x = track.right() - d - 3 if on else track.left() + 3
        p.setBrush(QColor("white"))
        p.drawEllipse(QRectF(x, y + 3, d, d))
        p.setPen(QColor(PALETTES[self._theme()]["text"]))
        p.drawText(QRectF(self.W + 12, 0, self.width() - self.W - 12, self.height()),
                   Qt.AlignVCenter | Qt.AlignLeft, self.text())


class Bridge(QObject):
    log = Signal(str)
    progress = Signal(float)
    running = Signal(bool)


class HistoryDialog(QDialog):
    def __init__(self, win, edit):
        super().__init__(win)
        self.win, self.edit = win, edit
        self.setWindowTitle(t("history_window_title", win.eng.lang))
        self.resize(560, 400)
        self.outer = QVBoxLayout(self)
        self.outer.setContentsMargins(14, 14, 14, 14)
        self._fill()

    def _fill(self):
        while self.outer.count():
            it = self.outer.takeAt(0)
            if it.widget():
                it.widget().deleteLater()
        eng = self.win.eng
        if not eng.klasor_gecmisi:
            lbl = QLabel(t("history_empty", eng.lang))
            lbl.setAlignment(Qt.AlignCenter)
            self.outer.addWidget(lbl)
            return
        for yol in list(eng.klasor_gecmisi):
            row = QFrame()
            row.setObjectName("card")
            h = QHBoxLayout(row)
            h.setContentsMargins(6, 4, 6, 4)
            b = QPushButton(yol)
            b.setObjectName("histitem")
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, y=yol: self._pick(y))
            d = QPushButton("✕")
            d.setObjectName("danger")
            d.clicked.connect(lambda _=False, y=yol: self._remove(y))
            h.addWidget(b, 1)
            h.addWidget(d)
            self.outer.addWidget(row)
        self.outer.addStretch(1)

    def _pick(self, yol):
        self.edit.setText(yol)
        self.win.eng._gecmise_ekle(yol)
        self.accept()

    def _remove(self, yol):
        if yol in self.win.eng.klasor_gecmisi:
            self.win.eng.klasor_gecmisi.remove(yol)
        self._fill()


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
        outer.addWidget(GradientStrip())
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
        g.addWidget(lbl, 0, 0, 1, 3)
        self.folder_edit = QLineEdit(self.eng.folder_path.get())
        self.folder_edit.textChanged.connect(self.eng.folder_path.set)
        hist = QPushButton("🕘")
        hist.setFixedWidth(40)
        hist.setCursor(Qt.PointingHandCursor)
        hist.clicked.connect(lambda: HistoryDialog(self, self.folder_edit).exec())
        browse = QPushButton(t("browse", lang))
        browse.setObjectName("accent")
        browse.setCursor(Qt.PointingHandCursor)
        browse.clicked.connect(self._browse)
        g.addWidget(self.folder_edit, 1, 0)
        g.addWidget(hist, 1, 1)
        g.addWidget(browse, 1, 2)
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
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.clicked.connect(self.eng.start_conversion_thread)
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
        s = Switch(text, lambda: self.eng.theme)
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

    def _on_lang(self, idx):
        code = LANG_CODES[idx]
        if code == self.eng.lang:
            return
        self.eng.lang = code
        self.build_ui()

    def _on_theme(self, idx):
        self.eng.theme = "dark" if idx == 0 else "light"
        self.apply_theme()

    def _browse(self):
        folder = QFileDialog.getExistingDirectory(self, t("browse_dialog_title", self.eng.lang), self.folder_edit.text() or "")
        if folder:
            self.folder_edit.setText(folder)
            self.eng._gecmise_ekle(folder)

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
