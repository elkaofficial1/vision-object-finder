# 🔍 Vision Object Finder

<div align="center">

**AI-приложение для поиска и распознавания объектов на изображениях**

LLaMA 3.2 11B Vision • LM Studio • PyQt5 • Русский / English

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?logo=qt&logoColor=white)
![LM Studio](https://img.shields.io/badge/LM%20Studio-Vision%20AI-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

## ✨ Возможности

- 🔎 Найти и описать все объекты
- 🎯 Найти конкретный объект
- 📝 Подробное описание сцены
- 🔢 Подсчёт объектов
- 🔤 OCR (распознавание текста)
- ❓ Произвольный промпт
- 🖱️ Drag & Drop / 📋 Вставка из буфера
- ⚡ Стриминг ответа
- 🌐 Русский / English (без перезапуска)
- 🎨 Тёмная тема (Catppuccin)

## 🛠 Установка

```bash
git clone https://github.com/elkaofficial1/vision-object-finder.git
cd vision-object-finder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Запуск

1. Откройте **LM Studio** → загрузите `llama-3.2-11b-vision`
2. Нажмите **Start Server** (порт 1234)
3. Запустите приложение:

```bash
source venv/bin/activate
python main.py
```

## 📁 Структура

```
vision-object-finder/
├── main.py           # Главное приложение (PyQt5)
├── localization.py   # Русский + English
├── requirements.txt  # Зависимости
├── .gitignore
└── README.md
```

## 📋 Требования

- macOS / Linux / Windows
- Python 3.8+
- [LM Studio](https://lmstudio.ai/) с моделью Vision
- 8+ GB RAM (16 GB рекомендуется)

## 📄 Лицензия

MIT License
