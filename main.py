"""
Vision Object Finder — поиск объектов на изображениях.
LM Studio + PyQt5 + LLaMA 3.2 Vision.
Локализация: Русский / English.
"""

import sys
import os
import json
import base64
import requests
from io import BytesIO
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog,
    QSplitter, QProgressBar, QComboBox, QMessageBox,
    QGroupBox, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from PIL import Image
from localization import Locale, locale


class LMStudioWorker(QThread):
    chunk_received = pyqtSignal(str)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, image_path, prompt, server_url="http://localhost:1234",
                 temperature=0.3, max_tokens=2048):
        super().__init__()
        self.image_path = image_path
        self.prompt = prompt
        self.server_url = server_url.rstrip("/")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._cancelled = False

    @staticmethod
    def _encode_image(path, max_size=1024):
        img = Image.open(path).convert("RGB")
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            img = img.resize(
                (int(img.size[0] * ratio), int(img.size[1] * ratio)),
                Image.LANCZOS,
            )
        buf = BytesIO()
        img.save(buf, format="JPEG", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            image_url = self._encode_image(self.image_path)
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.prompt},
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    }
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": True,
            }

            resp = requests.post(
                f"{self.server_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                stream=True, timeout=600,
            )
            resp.raise_for_status()

            full = ""
            for line in resp.iter_lines(decode_unicode=True):
                if self._cancelled:
                    break
                if not line or not line.strip().startswith("data:"):
                    continue
                data_str = line.strip()[len("data:"):].strip()
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                except json.JSONDecodeError:
                    continue
                choices = data.get("choices", [])
                if not choices:
                    continue
                token = choices[0].get("delta", {}).get("content", "")
                if token:
                    full += token
                    self.chunk_received.emit(token)
                if choices[0].get("finish_reason"):
                    break
            self.finished_signal.emit(full)

        except requests.ConnectionError:
            self.error_signal.emit(locale.t("err_connection"))
        except requests.HTTPError as e:
            status = e.response.status_code if e.response else "?"
            body = ""
            try:
                body = e.response.text[:500]
            except Exception:
                pass
            self.error_signal.emit(locale.t("err_http", status=status, body=body))
        except Exception as e:
            self.error_signal.emit(locale.t("err_generic", error=f"{type(e).__name__}: {e}"))


class ImageViewer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAcceptDrops(True)
        self.setStyleSheet(
            "QLabel { background:#1e1e2e; border:2px dashed #555;"
            "border-radius:12px; color:#888; font-size:16px; }"
        )
        self._pm = None
        self.update_placeholder()

    def update_placeholder(self):
        if not self._pm:
            self.setText(locale.t("placeholder_dragdrop"))

    def set_image(self, path):
        self._pm = QPixmap(path)
        self._refresh()

    def _refresh(self):
        if self._pm and not self._pm.isNull():
            self.setPixmap(
                self._pm.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._refresh()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        urls = e.mimeData().urls()
        if urls:
            p = urls[0].toLocalFile()
            exts = (".png", ".jpg", ".jpeg", ".bmp", ".webp", ".gif", ".tiff")
            if p.lower().endswith(exts):
                self.set_image(p)
                w = self.window()
                if hasattr(w, "_on_image_dropped"):
                    w._on_image_dropped(p)


class MainWindow(QMainWindow):
    MODE_TYPES = {
        "mode_find_all": "auto",
        "mode_find_specific": "custom",
        "mode_describe": "auto",
        "mode_count": "auto",
        "mode_ocr": "auto",
        "mode_custom": "free",
    }

    def __init__(self):
        super().__init__()
        self._image_path = None
        self._worker = None
        self._mode_keys = locale.get_mode_keys()
        self._apply_theme()
        self._build_ui()
        self._retranslate()

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow { background: #181825; }
            QWidget { color: #cdd6f4; font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; }
            QGroupBox {
                border: 1px solid #45475a; border-radius: 8px;
                margin-top: 12px; padding-top: 16px; font-weight: bold;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 14px; padding: 0 8px; }
            QPushButton {
                background: #45475a; border: none; border-radius: 8px;
                padding: 10px 20px; font-weight: bold;
            }
            QPushButton:hover   { background: #585b70; }
            QPushButton:pressed { background: #6c7086; }
            QPushButton:disabled { background: #313244; color: #585b70; }
            QPushButton#btnRun {
                background: #a6e3a1; color: #1e1e2e;
                font-size: 15px; padding: 12px 30px;
            }
            QPushButton#btnRun:hover { background: #94e2d5; }
            QPushButton#btnRun:disabled { background: #313244; color: #585b70; }
            QLineEdit, QComboBox {
                background: #313244; border: 1px solid #45475a;
                border-radius: 6px; padding: 8px 12px;
            }
            QLineEdit:focus { border: 1px solid #89b4fa; }
            QTextEdit {
                background: #1e1e2e; border: 1px solid #45475a;
                border-radius: 8px; padding: 12px; font-size: 14px;
            }
            QProgressBar {
                border: none; border-radius: 4px;
                background: #313244; height: 6px;
            }
            QProgressBar::chunk { background: #a6e3a1; border-radius: 4px; }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox QAbstractItemView {
                background: #313244; selection-background-color: #45475a;
                border: 1px solid #45475a;
            }
        """)

    def _build_ui(self):
        self.setMinimumSize(1150, 780)
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)

        self.lbl_title = QLabel()
        self.lbl_title.setStyleSheet("font-size:22px; font-weight:bold; color:#a6e3a1;")
        self.lbl_title.setAlignment(Qt.AlignCenter)
        root.addWidget(self.lbl_title)

        splitter = QSplitter(Qt.Horizontal)

        self.grp_image = QGroupBox()
        left_l = QVBoxLayout(self.grp_image)
        self.viewer = ImageViewer()
        left_l.addWidget(self.viewer)
        btn_row = QHBoxLayout()
        self.btn_open = QPushButton()
        self.btn_open.clicked.connect(self._open_file)
        btn_row.addWidget(self.btn_open)
        self.btn_paste = QPushButton()
        self.btn_paste.clicked.connect(self._paste_clipboard)
        btn_row.addWidget(self.btn_paste)
        left_l.addLayout(btn_row)
        self.lbl_info = QLabel("")
        self.lbl_info.setStyleSheet("color:#a6adc8; font-size:12px;")
        left_l.addWidget(self.lbl_info)
        splitter.addWidget(self.grp_image)

        self.grp_result = QGroupBox()
        right_l = QVBoxLayout(self.grp_result)
        self.txt_out = QTextEdit()
        self.txt_out.setReadOnly(True)
        right_l.addWidget(self.txt_out)
        self.btn_copy = QPushButton()
        self.btn_copy.clicked.connect(self._copy_result)
        right_l.addWidget(self.btn_copy)
        splitter.addWidget(self.grp_result)
        splitter.setSizes([500, 500])
        root.addWidget(splitter, stretch=1)

        self.grp_settings = QGroupBox()
        settings_l = QVBoxLayout(self.grp_settings)

        row1 = QHBoxLayout()
        self.lbl_mode = QLabel()
        row1.addWidget(self.lbl_mode)
        self.combo_mode = QComboBox()
        self.combo_mode.setMinimumWidth(320)
        self.combo_mode.currentIndexChanged.connect(self._on_mode_changed)
        row1.addWidget(self.combo_mode, stretch=1)
        row1.addSpacing(20)
        self.lbl_lang = QLabel()
        row1.addWidget(self.lbl_lang)
        self.combo_lang = QComboBox()
        for code, name in Locale.SUPPORTED.items():
            self.combo_lang.addItem(name, code)
        idx = list(Locale.SUPPORTED.keys()).index(locale.lang)
        self.combo_lang.setCurrentIndex(idx)
        self.combo_lang.currentIndexChanged.connect(self._on_language_changed)
        self.combo_lang.setMaximumWidth(180)
        row1.addWidget(self.combo_lang)
        settings_l.addLayout(row1)

        row2 = QHBoxLayout()
        self.lbl_query = QLabel()
        row2.addWidget(self.lbl_query)
        self.txt_query = QLineEdit()
        self.txt_query.returnPressed.connect(self._run_analysis)
        row2.addWidget(self.txt_query, stretch=1)
        settings_l.addLayout(row2)

        row3 = QHBoxLayout()
        self.lbl_url = QLabel()
        row3.addWidget(self.lbl_url)
        self.txt_url = QLineEdit("http://localhost:1234")
        self.txt_url.setMaximumWidth(300)
        row3.addWidget(self.txt_url)
        row3.addStretch()
        settings_l.addLayout(row3)
        root.addWidget(self.grp_settings)

        actions = QHBoxLayout()
        self.btn_run = QPushButton()
        self.btn_run.setObjectName("btnRun")
        self.btn_run.clicked.connect(self._run_analysis)
        actions.addWidget(self.btn_run)
        self.btn_stop = QPushButton()
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self._stop_analysis)
        actions.addWidget(self.btn_stop)
        self.btn_clear = QPushButton()
        self.btn_clear.clicked.connect(self._clear_result)
        actions.addWidget(self.btn_clear)
        root.addLayout(actions)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        self.progress.setFixedHeight(6)
        root.addWidget(self.progress)

        self.statusBar().setStyleSheet(
            "background:#11111b; color:#a6adc8; font-size:12px; padding:4px;"
        )

    def _retranslate(self):
        t = locale.t
        self.setWindowTitle(t("app_title"))
        self.lbl_title.setText(t("header_title"))
        self.grp_image.setTitle(t("group_image"))
        self.grp_result.setTitle(t("group_result"))
        self.grp_settings.setTitle(t("group_settings"))
        self.btn_open.setText(t("btn_open"))
        self.btn_paste.setText(t("btn_paste"))
        self.btn_copy.setText(t("btn_copy"))
        self.btn_run.setText(t("btn_analyze"))
        self.btn_stop.setText(t("btn_stop"))
        self.btn_clear.setText(t("btn_clear"))
        self.lbl_mode.setText(t("label_mode"))
        self.lbl_query.setText(t("label_query"))
        self.lbl_url.setText(t("label_url"))
        self.lbl_lang.setText(t("label_language"))
        self.txt_out.setPlaceholderText(t("placeholder_result"))
        self.viewer.update_placeholder()

        current_idx = self.combo_mode.currentIndex()
        self.combo_mode.blockSignals(True)
        self.combo_mode.clear()
        self.combo_mode.addItems(locale.get_mode_labels())
        if 0 <= current_idx < self.combo_mode.count():
            self.combo_mode.setCurrentIndex(current_idx)
        self.combo_mode.blockSignals(False)
        self._update_query_state()
        self.statusBar().showMessage(t("status_ready"))

    def _on_language_changed(self, index):
        code = self.combo_lang.itemData(index)
        if code and code != locale.lang:
            locale.lang = code
            self._retranslate()
            self.statusBar().showMessage(locale.t("status_lang_changed"))

    def _on_mode_changed(self, index):
        self._update_query_state()

    def _update_query_state(self):
        idx = self.combo_mode.currentIndex()
        if idx < 0 or idx >= len(self._mode_keys):
            return
        mode_key = self._mode_keys[idx]
        mode_type = self.MODE_TYPES.get(mode_key, "auto")
        if mode_type == "custom":
            self.txt_query.setEnabled(True)
            self.txt_query.setPlaceholderText(locale.t("placeholder_query_object"))
        elif mode_type == "free":
            self.txt_query.setEnabled(True)
            self.txt_query.setPlaceholderText(locale.t("placeholder_query_custom"))
        else:
            self.txt_query.setEnabled(False)
            self.txt_query.clear()
            self.txt_query.setPlaceholderText(locale.t("placeholder_query_disabled"))

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, locale.t("dlg_file_title"), "", locale.t("dlg_file_filter"),
        )
        if path:
            self._load_image(path)

    def _paste_clipboard(self):
        img = QApplication.clipboard().image()
        if img.isNull():
            QMessageBox.warning(self, locale.t("dlg_clipboard_empty_title"),
                                locale.t("dlg_clipboard_empty_text"))
            return
        tmp = os.path.join(os.path.expanduser("~"), ".vf_paste.png")
        img.save(tmp, "PNG")
        self._load_image(tmp)

    def _on_image_dropped(self, path):
        self._load_image(path)

    def _load_image(self, path):
        self._image_path = path
        self.viewer.set_image(path)
        sz = os.path.getsize(path) / 1024
        img = Image.open(path)
        self.lbl_info.setText(
            f"{Path(path).name}  •  {img.size[0]}×{img.size[1]}  •  {sz:.0f} KB"
        )
        self.statusBar().showMessage(locale.t("status_loaded", path=path))

    def _build_prompt(self):
        idx = self.combo_mode.currentIndex()
        if idx < 0:
            return None
        mode_key = self._mode_keys[idx]
        mode_type = self.MODE_TYPES.get(mode_key, "auto")
        if mode_type == "custom":
            obj = self.txt_query.text().strip()
            if not obj:
                return None
            return locale.get_prompt_for_mode(mode_key, obj=obj)
        elif mode_type == "free":
            text = self.txt_query.text().strip()
            return text if text else None
        else:
            return locale.get_prompt_for_mode(mode_key)

    def _run_analysis(self):
        if not self._image_path:
            QMessageBox.warning(self, locale.t("dlg_no_image_title"),
                                locale.t("dlg_no_image_text"))
            return
        prompt = self._build_prompt()
        if not prompt:
            QMessageBox.warning(self, locale.t("dlg_empty_query_title"),
                                locale.t("dlg_empty_query_text"))
            return
        self.txt_out.clear()
        self.btn_run.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.progress.setVisible(True)
        self.statusBar().showMessage(locale.t("status_analyzing"))
        self._worker = LMStudioWorker(
            self._image_path, prompt, self.txt_url.text().strip(),
        )
        self._worker.chunk_received.connect(self._on_token)
        self._worker.finished_signal.connect(self._on_done)
        self._worker.error_signal.connect(self._on_error)
        self._worker.start()

    def _on_token(self, token):
        cursor = self.txt_out.textCursor()
        cursor.movePosition(cursor.End)
        self.txt_out.setTextCursor(cursor)
        self.txt_out.insertPlainText(token)

    def _on_done(self, full_text):
        self._set_idle()
        n = len(full_text.split())
        self.statusBar().showMessage(locale.t("status_done", n=n))

    def _on_error(self, msg):
        self._set_idle()
        self.txt_out.setPlainText(msg)
        self.statusBar().showMessage(locale.t("status_error"))

    def _stop_analysis(self):
        if self._worker:
            self._worker.cancel()
            self._worker.quit()
            self._worker.wait(3000)
        self._set_idle()
        self.statusBar().showMessage(locale.t("status_stopped"))

    def _clear_result(self):
        self.txt_out.clear()
        self.statusBar().showMessage(locale.t("status_cleared"))

    def _copy_result(self):
        text = self.txt_out.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage(locale.t("status_copied"))

    def _set_idle(self):
        self.btn_run.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.progress.setVisible(False)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
