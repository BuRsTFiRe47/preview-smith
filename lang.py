# -*- coding: utf-8 -*-
"""
Preview Smith - Language / Dil / 言語 / 语言 Module
Merkezi çok dilli (TR/EN/JA/ZH) metin sözlüğü.
Central multilingual (TR/EN/JA/ZH) text dictionary.
中央集約された多言語（TR/EN/JA/ZH）テキスト辞書。
中央多语言（TR/EN/JA/ZH）文本字典。
"""

TRANSLATIONS = {
    "app_title": {
        "tr": "Preview Smith - Önizleme Dönüştürücü",
        "en": "Preview Smith - Preview Converter",
        "ja": "Preview Smith - プレビュー変換ツール",
        "zh": "Preview Smith - 预览转换工具",
    },

    "lang_tr": {"tr": "Türkçe", "en": "Turkish", "ja": "トルコ語", "zh": "土耳其语"},
    "lang_en": {"tr": "İngilizce", "en": "English", "ja": "英語", "zh": "英语"},
    "lang_ja": {"tr": "Japonca", "en": "Japanese", "ja": "日本語", "zh": "日语"},
    "lang_zh": {"tr": "Çince", "en": "Chinese", "ja": "中国語", "zh": "中文"},
    "theme_dark": {"tr": "Koyu", "en": "Dark", "ja": "ダーク", "zh": "深色"},
    "theme_light": {"tr": "Açık", "en": "Light", "ja": "ライト", "zh": "浅色"},

    "target_folder_label": {"tr": "Hedef Klasör:", "en": "Target Folder:", "ja": "対象フォルダ：", "zh": "目标文件夹："},
    "browse": {"tr": "Gözat", "en": "Browse", "ja": "参照", "zh": "浏览"},

    "switch_subfolders": {"tr": "Alt klasörleri de tara", "en": "Also scan subfolders", "ja": "サブフォルダもスキャンする", "zh": "同时扫描子文件夹"},
    "switch_delete_source": {"tr": "Başarılı dönüşümde orijinal dosyayı sil", "en": "Delete original file after a successful conversion", "ja": "変換成功後に元のファイルを削除する", "zh": "转换成功后删除原始文件"},

    "output_format_label": {"tr": "Çıktı Formatı:", "en": "Output Format:", "ja": "出力形式：", "zh": "输出格式："},
    "quality_label": {"tr": "Kalite:", "en": "Quality:", "ja": "品質：", "zh": "质量："},
    "max_size_label": {"tr": "Maks. Boyut (px):", "en": "Max Size (px):", "ja": "最大サイズ（px）：", "zh": "最大尺寸（px）："},
    "workers_label": {"tr": "Aynı Anda İşlenecek Dosya:", "en": "Parallel Conversions:", "ja": "同時処理ファイル数：", "zh": "并行转换数量："},

    "btn_start": {"tr": "DÖNÜŞTÜRMEYİ BAŞLAT", "en": "START CONVERSION", "ja": "変換を開始", "zh": "开始转换"},
    "btn_cancel": {"tr": "İPTAL ET", "en": "CANCEL", "ja": "キャンセル", "zh": "取消"},

    "log_scanning": {"tr": ">> Hedef dizin taranıyor: {folder}", "en": ">> Scanning target directory: {folder}", "ja": ">> 対象ディレクトリをスキャン中：{folder}", "zh": ">> 正在扫描目标目录：{folder}"},
    "log_no_files": {"tr": ">> Dönüştürülecek video dosyası bulunamadı.", "en": ">> No video files found to convert.", "ja": ">> 変換対象の動画ファイルが見つかりませんでした。", "zh": ">> 未找到可转换的视频文件。"},
    "log_total_found": {"tr": ">> Toplam {count} adet video bulundu.", "en": ">> Found {count} video(s) in total.", "ja": ">> 合計{count}件の動画が見つかりました。", "zh": ">> 共找到 {count} 个视频。"},
    "log_processing": {"tr": "İşleniyor ({index}/{total}): {name}", "en": "Processing ({index}/{total}): {name}", "ja": "処理中（{index}/{total}）：{name}", "zh": "正在处理（{index}/{total}）：{name}"},
    "log_converted": {"tr": "  [✓] Çevrildi ({size}). Orijinal dosya silindi.", "en": "  [✓] Converted ({size}). Original file deleted.", "ja": "  [✓] 変換完了（{size}）。元のファイルは削除されました。", "zh": "  [✓] 转换完成（{size}）。原始文件已删除。"},
    "log_converted_kept": {"tr": "  [✓] Çevrildi ({size}). Orijinal dosya korundu.", "en": "  [✓] Converted ({size}). Original file kept.", "ja": "  [✓] 変換完了（{size}）。元のファイルは保持されました。", "zh": "  [✓] 转换完成（{size}）。原始文件已保留。"},
    "log_error_kept": {"tr": "  [X] HATA! Orijinal dosya korundu.", "en": "  [X] ERROR! Original file kept.", "ja": "  [X] エラー！元のファイルは保持されました。", "zh": "  [X] 错误！原始文件已保留。"},
    "log_system_error": {"tr": "  [!] Sistem Hatası: {error}", "en": "  [!] System Error: {error}", "ja": "  [!] システムエラー：{error}", "zh": "  [!] 系统错误：{error}"},
    "log_cancelled": {"tr": ">> İşlem kullanıcı tarafından iptal edildi.", "en": ">> Operation cancelled by the user.", "ja": ">> ユーザーによって処理がキャンセルされました。", "zh": ">> 操作已被用户取消。"},
    "log_summary_title": {"tr": "İŞLEM ÖZETİ:", "en": "OPERATION SUMMARY:", "ja": "処理概要：", "zh": "操作摘要："},
    "log_summary_success": {"tr": "  Başarılı: {count} adet", "en": "  Successful: {count}", "ja": "  成功：{count}件", "zh": "  成功：{count} 个"},
    "log_summary_fail": {"tr": "  Hatalı  : {count} adet", "en": "  Failed  : {count}", "ja": "  失敗：{count}件", "zh": "  失败：{count} 个"},
    "log_all_done": {"tr": "Tüm işlemler tamamlandı.", "en": "All operations completed.", "ja": "すべての処理が完了しました。", "zh": "所有操作已完成。"},
    "log_no_folder": {"tr": ">> HATA: Lütfen önce bir klasör seçin.", "en": ">> ERROR: Please select a folder first.", "ja": ">> エラー：先にフォルダを選択してください。", "zh": ">> 错误：请先选择一个文件夹。"},
    "log_ffmpeg_missing": {"tr": ">> HATA: ffmpeg bulunamadı. Lütfen ffmpeg'i kurup PATH'e ekleyin.", "en": ">> ERROR: ffmpeg was not found. Please install ffmpeg and add it to PATH.", "ja": ">> エラー：ffmpegが見つかりません。ffmpegをインストールしてPATHに追加してください。", "zh": ">> 错误：未找到 ffmpeg。请安装 ffmpeg 并将其添加到 PATH。"},

    "browse_dialog_title": {"tr": "LoRA / Model Önizleme Klasörünü Seçin", "en": "Select the LoRA / Model Preview Folder", "ja": "LoRA/モデルのプレビューフォルダを選択", "zh": "选择 LoRA / 模型预览文件夹"},
}


def t(key: str, lang: str = "tr", **kwargs) -> str:
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("en", entry.get("tr", key)))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
