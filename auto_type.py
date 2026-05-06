import sys
import time
import pyautogui
import pyperclip
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread, Signal

FONT_FAMILY = "微软雅黑"
COLOR_PRIMARY = "#4a69bd"
COLOR_SUCCESS = "#4CAF50"
COLOR_DANGER = "#f44336"
COLOR_TEXT = "#333333"
COLOR_TEXT_SECONDARY = "#555555"
COLOR_TEXT_HINT = "#666666"

INPUT_STYLE = """
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 5px 8px;
    background: #fafafa;
}}
{widget}:focus {{
    border-color: {primary};
    background: white;
"""

TEXT_EDIT_STYLE = INPUT_STYLE.format(widget="QTextEdit", primary=COLOR_PRIMARY) + "}"
LINE_EDIT_STYLE = INPUT_STYLE.format(widget="QLineEdit", primary=COLOR_PRIMARY) + "}"

BUTTON_STYLES = {
    "primary": f"""
        QPushButton {{
            background-color: {COLOR_SUCCESS};
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
        }}
        QPushButton:hover {{ background-color: #45a049; }}
        QPushButton:pressed {{ background-color: #3d8b40; }}
        QPushButton:disabled {{ background-color: #cccccc; }}
    """,
    "danger": f"""
        QPushButton {{
            background-color: {COLOR_DANGER};
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
        }}
        QPushButton:hover {{ background-color: #da190b; }}
        QPushButton:pressed {{ background-color: #b91408; }}
    """,
}


def create_label(text, size=11, bold=False, color=COLOR_TEXT):
    label = QLabel(text)
    label.setFont(QFont(FONT_FAMILY, size, QFont.Bold if bold else QFont.Normal))
    label.setStyleSheet(f"color: {color};")
    return label


def create_line_edit(default_text="", width=90):
    edit = QLineEdit()
    edit.setText(default_text)
    edit.setFixedWidth(width)
    edit.setFont(QFont(FONT_FAMILY, 11))
    edit.setAlignment(Qt.AlignCenter)
    edit.setStyleSheet(LINE_EDIT_STYLE)
    return edit


def create_button(text, style_type="primary", width=160, height=45):
    btn = QPushButton(text)
    btn.setFixedSize(width, height)
    btn.setFont(QFont(FONT_FAMILY, 11, QFont.Bold))
    btn.setStyleSheet(BUTTON_STYLES[style_type])
    return btn


class TypingWorker(QThread):
    finished = Signal()

    def __init__(self, text, delay, interval):
        super().__init__()
        self.text = text
        self.delay = delay
        self.interval = interval

    def run(self):
        time.sleep(self.delay)

        lines = self.text.split('\n')
        for i, line in enumerate(lines):
            if not line.strip():
                pyautogui.press('enter')
                time.sleep(0.1)
                continue

            pyperclip.copy(line)
            time.sleep(0.05)
            pyautogui.hotkey('ctrl', 'v')

            if i < len(lines) - 1:
                pyautogui.press('enter')

            time.sleep(self.interval)

        self.finished.emit()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.worker = None
        self._setup_window()
        self._build_ui()
        self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("键盘自动输入工具")
        self.setGeometry(100, 100, 700, 550)
        self.setFixedSize(700, 550)

    def _build_ui(self):
        central = QWidget()
        central.setStyleSheet("background: #f5f7fa;")
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._create_header())
        layout.addWidget(self._create_content())

    def _create_header(self):
        frame = QWidget()
        frame.setFixedHeight(80)
        frame.setStyleSheet(f"background: {COLOR_PRIMARY};")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(30, 0, 0, 0)
        layout.setSpacing(5)

        title = create_label("键盘自动输入工具", size=20, bold=True, color="white")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(title)

        subtitle = create_label("自动输入文本到目标窗口", size=11, color="rgba(255,255,255,0.8)")
        subtitle.setAlignment(Qt.AlignLeft)
        layout.addWidget(subtitle)

        return frame

    def _create_content(self):
        frame = QWidget()
        frame.setStyleSheet("background: white;")

        layout = QVBoxLayout(frame)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 25, 30, 25)

        layout.addWidget(create_label("输入文本内容", size=12, bold=True))
        layout.addWidget(self._create_text_input())
        layout.addLayout(self._create_settings())
        layout.addLayout(self._create_buttons())
        layout.addLayout(self._create_hints())

        return frame

    def _create_text_input(self):
        self.text_input = QTextEdit()
        self.text_input.setFixedHeight(160)
        self.text_input.setFont(QFont(FONT_FAMILY, 11))
        self.text_input.setPlaceholderText("请在此输入需要自动输入的文本内容...")
        self.text_input.setStyleSheet(TEXT_EDIT_STYLE)
        return self.text_input

    def _create_settings(self):
        settings = QHBoxLayout()
        settings.setSpacing(50)

        for label_text, default, key in [
            ("准备时间（秒）", "3", "delay"),
            ("输入间隔（秒）", "0.3", "interval"),
        ]:
            group = QVBoxLayout()
            group.setSpacing(8)
            group.addWidget(create_label(label_text, bold=True, color=COLOR_TEXT_SECONDARY))
            setattr(self, f"{key}_input", create_line_edit(default))
            group.addWidget(getattr(self, f"{key}_input"))
            settings.addLayout(group)

        settings.addStretch()
        return settings

    def _create_buttons(self):
        buttons = QHBoxLayout()
        buttons.setSpacing(25)

        self.submit_btn = create_button("开始输入", "primary")
        self.exit_btn = create_button("退出", "danger")

        buttons.addWidget(self.submit_btn)
        buttons.addWidget(self.exit_btn)
        buttons.addStretch()

        return buttons

    def _create_hints(self):
        hints = QVBoxLayout()
        hints.setSpacing(5)

        hint1 = create_label("💡 提示：点击开始后，请快速切换到目标输入窗口", size=10, color=COLOR_TEXT_HINT)
        hint2 = create_label("⚠️ 紧急停止：将鼠标快速移到屏幕四角即可中断", size=10, color="#e53935")
        hints.addWidget(hint1)
        hints.addWidget(hint2)

        return hints

    def _connect_signals(self):
        self.submit_btn.clicked.connect(self.execute_typing)
        self.exit_btn.clicked.connect(self.close)

    def _validate_number(self, value_str, min_val, max_val, field_name):
        try:
            value = float(value_str)
            if min_val <= value <= max_val:
                return value
        except (ValueError, TypeError):
            pass
        QMessageBox.warning(
            self, "警告",
            f"{field_name}必须在 {min_val}-{max_val} 秒之间！"
        )
        return None

    def execute_typing(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "警告", "请先输入文本内容！")
            return

        delay = self._validate_number(self.delay_input.text(), 0, 10, "准备时间")
        if delay is None:
            return

        interval = self._validate_number(self.interval_input.text(), 0, 5, "输入间隔")
        if interval is None:
            return

        self.submit_btn.setEnabled(False)
        QMessageBox.information(self, "提示", f"{delay}秒后开始输入，请立即切换到目标窗口！")
        self.showMinimized()

        self._disconnect_worker()
        self.worker = TypingWorker(text, delay, interval)
        self.worker.finished.connect(self.on_typing_finished)
        self.worker.start()

    def _disconnect_worker(self):
        if self.worker is not None:
            try:
                self.worker.finished.disconnect(self.on_typing_finished)
            except RuntimeError:
                pass

    def on_typing_finished(self):
        self.showNormal()
        self.submit_btn.setEnabled(True)
        QMessageBox.information(self, "完成", "输入完成！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())