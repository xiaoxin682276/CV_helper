import sys
import time
import pyperclip
import keyboard
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
)
from PyQt5.QtCore import QTimer, Qt
"""
复制粘贴助手（v1.0）
作者：昕染
日期：2025-09-25
"""


class CopyPasteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.countdown = 0
        self.current_action = None
        self.btn_text = ""

    def initUI(self):
        self.setWindowTitle("复制粘贴助手(v1.0)")
        self.setGeometry(600, 300, 400, 300)

        # 保持窗口在最前端
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()

        self.info_label = QLabel(
            "点击按钮开始倒计时后进行复制/粘贴操作\n"
            "提示：请使用系统默认美式键盘输入中文"
        )
        layout.addWidget(self.info_label)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("这里可以修改要粘贴的内容")
        layout.addWidget(self.text_edit)

        # 复制按钮
        self.btn_copy = QPushButton("复制选中内容", self)
        self.btn_copy.clicked.connect(lambda: self.start_countdown("copy"))
        layout.addWidget(self.btn_copy)

        # 粘贴按钮
        self.btn_paste = QPushButton("粘贴内容", self)
        self.btn_paste.clicked.connect(lambda: self.start_countdown("paste"))
        layout.addWidget(self.btn_paste)

        self.setLayout(layout)

    def start_countdown(self, action):
        """开始 5 秒倒计时"""
        if self.timer.isActive():
            # 防止重复点击
            return

        self.countdown = 5
        self.current_action = action
        self.info_label.setText(f"⏳ {self.countdown} 秒后执行 {action}")

        # 保存按钮原文字并更新显示倒计时
        if action == "copy":
            self.btn_text = self.btn_copy.text()
            self.btn_copy.setText(f"{self.btn_text} ({self.countdown})")
            self.btn_copy.setEnabled(False)
            self.btn_paste.setEnabled(False)
        else:
            self.btn_text = self.btn_paste.text()
            self.btn_paste.setText(f"{self.btn_text} ({self.countdown})")
            self.btn_copy.setEnabled(False)
            self.btn_paste.setEnabled(False)

        self.timer.start(1000)  # 每秒触发一次

    def update_countdown(self):
        self.countdown -= 1
        if self.countdown > 0:
            self.info_label.setText(f"⏳ {self.countdown} 秒后执行 {self.current_action}")
            if self.current_action == "copy":
                self.btn_copy.setText(f"{self.btn_text} ({self.countdown})")
            else:
                self.btn_paste.setText(f"{self.btn_text} ({self.countdown})")
        else:
            self.timer.stop()
            self.info_label.setText(f"✅ 开始执行 {self.current_action}")
            # 恢复按钮状态
            self.btn_copy.setEnabled(True)
            self.btn_paste.setEnabled(True)
            if self.current_action == "copy":
                self.btn_copy.setText(self.btn_text)
                self.force_copy()
            else:
                self.btn_paste.setText(self.btn_text)
                self.force_paste()

    def force_copy(self):
        """复制鼠标选中内容"""
        try:
            keyboard.press_and_release("ctrl+c")
            time.sleep(0.1)
            text = pyperclip.paste()
            if text.strip():
                self.text_edit.setPlainText(text)
                self.info_label.setText(f"✅ 已复制内容：{text[:30]}...")
            else:
                self.info_label.setText("⚠️ 没有检测到可复制的内容")
        except Exception as e:
            self.info_label.setText(f"❌ 复制出错：{e}")

    def force_paste(self):
        """从 QTextEdit 粘贴到光标位置（支持中文）"""
        try:
            text = self.text_edit.toPlainText()
            if not text.strip():
                self.info_label.setText("⚠️ 没有内容可粘贴")
                return
            pyperclip.copy(text)
            time.sleep(0.1)
            keyboard.press_and_release("ctrl+v")
            self.info_label.setText("✅ 已粘贴（支持中文）")
        except Exception as e:
            self.info_label.setText(f"❌ 粘贴出错：{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CopyPasteApp()
    window.show()
    sys.exit(app.exec_())
