# -*- coding: utf-8 -*-
"""
Preview Smith - Language / Dil Module
Merkezi çift dilli (TR/EN) metin sözlüğü.
Central bilingual (TR/EN) text dictionary.
"""

TRANSLATIONS = {
    "app_title": {"tr": "Preview Smith - Önizleme Dönüştürücü", "en": "Preview Smith - Preview Converter"},

    "lang_tr": {"tr": "Türkçe", "en": "Turkish"},
    "lang_en": {"tr": "İngilizce", "en": "English"},
    "theme_dark": {"tr": "Koyu", "en": "Dark"},
    "theme_light": {"tr": "Açık", "en": "Light"},

    "target_folder_label": {"tr": "Hedef Klasör:", "en": "Target Folder:"},
    "browse": {"tr": "Gözat", "en": "Browse"},

    "switch_subfolders": {"tr": "Alt klasörleri de tara", "en": "Also scan subfolders"},
    "switch_delete_source": {"tr": "Başarılı dönüşümde orijinal dosyayı sil", "en": "Delete original file after a successful conversion"},

    "output_format_label": {"tr": "Çıktı Formatı:", "en": "Output Format:"},
    "quality_label": {"tr": "Kalite:", "en": "Quality:"},
    "max_size_label": {"tr": "Maks. Boyut (px):", "en": "Max Size (px):"},
    "workers_label": {"tr": "Aynı Anda İşlenecek Dosya:", "en": "Parallel Conversions:"},

    "btn_start": {"tr": "DÖNÜŞTÜRMEYİ BAŞLAT", "en": "START CONVERSION"},
    "btn_cancel": {"tr": "İPTAL ET", "en": "CANCEL"},

    "log_scanning": {"tr": ">> Hedef dizin taranıyor: {folder}", "en": ">> Scanning target directory: {folder}"},
    "log_no_files": {"tr": ">> Dönüştürülecek video dosyası bulunamadı.", "en": ">> No video files found to convert."},
    "log_total_found": {"tr": ">> Toplam {count} adet video bulundu.", "en": ">> Found {count} video(s) in total."},
    "log_processing": {"tr": "İşleniyor ({index}/{total}): {name}", "en": "Processing ({index}/{total}): {name}"},
    "log_converted": {"tr": "  [✓] Çevrildi ({size}). Orijinal dosya silindi.", "en": "  [✓] Converted ({size}). Original file deleted."},
    "log_converted_kept": {"tr": "  [✓] Çevrildi ({size}). Orijinal dosya korundu.", "en": "  [✓] Converted ({size}). Original file kept."},
    "log_error_kept": {"tr": "  [X] HATA! Orijinal dosya korundu.", "en": "  [X] ERROR! Original file kept."},
    "log_system_error": {"tr": "  [!] Sistem Hatası: {error}", "en": "  [!] System Error: {error}"},
    "log_cancelled": {"tr": ">> İşlem kullanıcı tarafından iptal edildi.", "en": ">> Operation cancelled by the user."},
    "log_summary_title": {"tr": "İŞLEM ÖZETİ:", "en": "OPERATION SUMMARY:"},
    "log_summary_success": {"tr": "  Başarılı: {count} adet", "en": "  Successful: {count}"},
    "log_summary_fail": {"tr": "  Hatalı  : {count} adet", "en": "  Failed  : {count}"},
    "log_all_done": {"tr": "Tüm işlemler tamamlandı.", "en": "All operations completed."},
    "log_no_folder": {"tr": ">> HATA: Lütfen önce bir klasör seçin.", "en": ">> ERROR: Please select a folder first."},
    "log_ffmpeg_missing": {"tr": ">> HATA: ffmpeg bulunamadı. Lütfen ffmpeg'i kurup PATH'e ekleyin.", "en": ">> ERROR: ffmpeg was not found. Please install ffmpeg and add it to PATH."},

    "browse_dialog_title": {"tr": "LoRA / Model Önizleme Klasörünü Seçin", "en": "Select the LoRA / Model Preview Folder"},
}


def t(key: str, lang: str = "tr", **kwargs) -> str:
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("tr", key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
