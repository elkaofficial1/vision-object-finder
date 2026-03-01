"""
Система локализации для Vision Object Finder.
Поддержка: Русский (ru), English (en).
"""

from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {

    "app_title": {
        "ru": "🔍 Поиск объектов — LM Studio Vision",
        "en": "🔍 Object Finder — LM Studio Vision",
    },
    "header_title": {
        "ru": "🔍  Поиск объектов — LM Studio Vision AI",
        "en": "🔍  Object Finder — LM Studio Vision AI",
    },

    "group_image": {
        "ru": "Изображение",
        "en": "Image",
    },
    "group_result": {
        "ru": "Результат анализа",
        "en": "Analysis Result",
    },
    "group_settings": {
        "ru": "Параметры",
        "en": "Settings",
    },

    "btn_open": {
        "ru": "📂  Открыть файл",
        "en": "📂  Open File",
    },
    "btn_paste": {
        "ru": "📋  Из буфера",
        "en": "📋  From Clipboard",
    },
    "btn_copy": {
        "ru": "📋  Копировать результат",
        "en": "📋  Copy Result",
    },
    "btn_analyze": {
        "ru": "🚀  Анализировать",
        "en": "🚀  Analyze",
    },
    "btn_stop": {
        "ru": "⛔  Стоп",
        "en": "⛔  Stop",
    },
    "btn_clear": {
        "ru": "🗑  Очистить",
        "en": "🗑  Clear",
    },

    "label_mode": {
        "ru": "Режим:",
        "en": "Mode:",
    },
    "label_query": {
        "ru": "Запрос:",
        "en": "Query:",
    },
    "label_url": {
        "ru": "URL сервера:",
        "en": "Server URL:",
    },
    "label_language": {
        "ru": "Язык / Lang:",
        "en": "Lang / Язык:",
    },

    "mode_find_all": {
        "ru": "🔎 Найти и описать все объекты",
        "en": "🔎 Find and describe all objects",
    },
    "mode_find_specific": {
        "ru": "🎯 Найти конкретный объект",
        "en": "🎯 Find specific object",
    },
    "mode_describe": {
        "ru": "📝 Подробное описание сцены",
        "en": "📝 Detailed scene description",
    },
    "mode_count": {
        "ru": "🔢 Подсчитать объекты",
        "en": "🔢 Count objects",
    },
    "mode_ocr": {
        "ru": "🔤 Распознать текст (OCR)",
        "en": "🔤 Recognize text (OCR)",
    },
    "mode_custom": {
        "ru": "❓ Свой промпт",
        "en": "❓ Custom prompt",
    },

    "placeholder_result": {
        "ru": "Ответ модели появится здесь…",
        "en": "Model response will appear here…",
    },
    "placeholder_query_object": {
        "ru": "Введите объект для поиска (кошка, машина, человек…)",
        "en": "Enter object to find (cat, car, person…)",
    },
    "placeholder_query_custom": {
        "ru": "Введите свой промпт…",
        "en": "Enter your custom prompt…",
    },
    "placeholder_query_disabled": {
        "ru": "(не требуется в этом режиме)",
        "en": "(not needed in this mode)",
    },
    "placeholder_dragdrop": {
        "ru": "📷  Перетащите изображение сюда\nили нажмите «Открыть файл»",
        "en": "📷  Drag & drop image here\nor click 'Open File'",
    },

    "prompt_find_all": {
        "ru": (
            "Внимательно проанализируй это изображение. Перечисли каждый отдельный "
            "объект, который ты видишь. Для каждого объекта укажи: 1) название, "
            "2) примерное расположение на изображении (верх-лево, центр, низ-право и т.д.), "
            "3) цвет, 4) краткое описание. Будь тщательным. Отвечай на русском языке."
        ),
        "en": (
            "Carefully analyze this image. List every distinct object you can see. "
            "For each object provide: 1) name, 2) approximate location in the image "
            "(top-left, center, bottom-right etc.), 3) color, 4) brief description. "
            "Be thorough and systematic."
        ),
    },
    "prompt_find_specific": {
        "ru": (
            'Найди объект "{obj}" на этом изображении. '
            "Если ты его видишь — опиши точно, где он расположен "
            "(верх-лево, центр, низ-право и т.д.), его размер относительно "
            "изображения, цвет и другие детали. "
            "Если объект НЕ найден — скажи об этом чётко. "
            "Отвечай на русском языке."
        ),
        "en": (
            'Find the object "{obj}" in this image. '
            "If you see it — describe exactly where it is located "
            "(top-left, center, bottom-right etc.), its size relative "
            "to the image, color and details. "
            "If the object is NOT present, say so clearly."
        ),
    },
    "prompt_describe": {
        "ru": (
            "Опиши это изображение максимально подробно. Упомяни все объекты, "
            "людей, цвета, освещение, настроение, фон, передний план. "
            "Отвечай на русском языке."
        ),
        "en": (
            "Describe this image in great detail. Mention all objects, people, "
            "colors, lighting, mood, background, foreground elements."
        ),
    },
    "prompt_count": {
        "ru": (
            "Подсчитай все отдельные объекты на этом изображении. "
            "Сгруппируй их по категориям. Укажи количество для каждой "
            "категории и общее число. Отвечай на русском языке."
        ),
        "en": (
            "Count all distinct objects in this image. Group by category. "
            "Provide the total count per category and grand total."
        ),
    },
    "prompt_ocr": {
        "ru": (
            "Извлеки и перечисли ВЕСЬ текст, видимый на этом изображении. "
            "Сохрани оригинальный язык текста. Добавь перевод на русский, "
            "если текст на другом языке."
        ),
        "en": (
            "Extract and list ALL text visible in this image. "
            "Preserve the original language of the text."
        ),
    },

    "status_ready": {
        "ru": "Готово. Запустите LM Studio → загрузите модель → Start Server.",
        "en": "Ready. Start LM Studio → load model → Start Server.",
    },
    "status_loaded": {
        "ru": "Загружено: {path}",
        "en": "Loaded: {path}",
    },
    "status_analyzing": {
        "ru": "⏳ Анализ изображения…",
        "en": "⏳ Analyzing image…",
    },
    "status_done": {
        "ru": "✅ Готово — {n} слов в ответе.",
        "en": "✅ Done — {n} words in response.",
    },
    "status_error": {
        "ru": "❌ Ошибка",
        "en": "❌ Error",
    },
    "status_stopped": {
        "ru": "⛔ Остановлено.",
        "en": "⛔ Stopped.",
    },
    "status_copied": {
        "ru": "📋 Скопировано в буфер обмена!",
        "en": "📋 Copied to clipboard!",
    },
    "status_cleared": {
        "ru": "Очищено.",
        "en": "Cleared.",
    },
    "status_lang_changed": {
        "ru": "Язык изменён на русский.",
        "en": "Language changed to English.",
    },

    "dlg_no_image_title": {
        "ru": "Нет изображения",
        "en": "No Image",
    },
    "dlg_no_image_text": {
        "ru": "Сначала загрузите изображение.",
        "en": "Please load an image first.",
    },
    "dlg_empty_query_title": {
        "ru": "Пустой запрос",
        "en": "Empty Query",
    },
    "dlg_empty_query_text": {
        "ru": "Введите текст запроса.",
        "en": "Please enter a query.",
    },
    "dlg_clipboard_empty_title": {
        "ru": "Буфер пуст",
        "en": "Clipboard Empty",
    },
    "dlg_clipboard_empty_text": {
        "ru": "В буфере обмена нет изображения.",
        "en": "No image found in clipboard.",
    },
    "dlg_file_filter": {
        "ru": "Изображения (*.png *.jpg *.jpeg *.bmp *.webp *.gif *.tiff);;Все файлы (*)",
        "en": "Images (*.png *.jpg *.jpeg *.bmp *.webp *.gif *.tiff);;All Files (*)",
    },
    "dlg_file_title": {
        "ru": "Выберите изображение",
        "en": "Select Image",
    },

    "err_connection": {
        "ru": (
            "❌ Не удалось подключиться к LM Studio.\n\n"
            "Проверьте:\n"
            "1) LM Studio запущена\n"
            "2) Модель загружена (llama-3.2-11b-vision)\n"
            "3) Local Server запущен\n"
            "4) URL: http://localhost:1234"
        ),
        "en": (
            "❌ Cannot connect to LM Studio.\n\n"
            "Check:\n"
            "1) LM Studio is running\n"
            "2) Model is loaded (llama-3.2-11b-vision)\n"
            "3) Local Server is started\n"
            "4) URL: http://localhost:1234"
        ),
    },
    "err_http": {
        "ru": "❌ HTTP ошибка {status}\n\n{body}",
        "en": "❌ HTTP error {status}\n\n{body}",
    },
    "err_generic": {
        "ru": "❌ Ошибка: {error}",
        "en": "❌ Error: {error}",
    },
}


class Locale:
    SUPPORTED = {"ru": "🇷🇺 Русский", "en": "🇬🇧 English"}
    DEFAULT = "ru"

    def __init__(self, lang=None):
        self._lang = lang if lang in self.SUPPORTED else self.DEFAULT

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        if value in self.SUPPORTED:
            self._lang = value

    def t(self, key, **kwargs):
        entry = TRANSLATIONS.get(key)
        if not entry:
            return f"[{key}]"
        text = entry.get(self._lang, entry.get("en", f"[{key}]"))
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                pass
        return text

    def get_mode_keys(self):
        return [
            "mode_find_all", "mode_find_specific", "mode_describe",
            "mode_count", "mode_ocr", "mode_custom",
        ]

    def get_mode_labels(self):
        return [self.t(k) for k in self.get_mode_keys()]

    def get_prompt_for_mode(self, mode_key, **kwargs):
        prompt_map = {
            "mode_find_all": "prompt_find_all",
            "mode_describe": "prompt_describe",
            "mode_count": "prompt_count",
            "mode_ocr": "prompt_ocr",
        }
        prompt_key = prompt_map.get(mode_key)
        if prompt_key:
            return self.t(prompt_key)
        if mode_key == "mode_find_specific":
            return self.t("prompt_find_specific", **kwargs)
        return ""


locale = Locale("ru")
