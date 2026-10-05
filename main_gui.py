#main_gui.py
import sys
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QLineEdit,
    QLabel, QTextEdit, QMessageBox, QDialog, QComboBox,
    QTabWidget, QFileDialog, QCheckBox
)
from PyQt6.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont

from models import Task
from repository import DataRepository
from task_validation import TaskValidator
from task_manager import TaskManager

task_manager = TaskManager()

class AddEditTaskDialog(QDialog):
    def __init__(self, parent=None, task: Task = None):
        super().__init__(parent)
        self.task = task
        self.current_theme = parent.current_theme if parent else "dark"
        self.setup_ui()

        if task:
            self.setWindowTitle("Edit Task")
            self.load_task_data()
        else:
            self.setWindowTitle("Add New Task")

    def setup_ui(self):
        self.setMinimumSize(450, 700)
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cba6f7;
                font-size: 13px;
                font-weight: bold;
                margin-top: 10px;
                margin-bottom: 5px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #2a2a3a;
                border: 1px solid #313244;
                border-radius: 12px;
                padding: 10px;
                color: #cdd6f4;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #cba6f7;
            }
            QPushButton {
                background-color: #cba6f7;
                color: #1e1e2e;
                border: none;
                border-radius: 25px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton#cancel {
                background-color: #313244;
                color: #cdd6f4;
            }
            QPushButton#cancel:hover {
                background-color: #45475a;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        title_label = QLabel("✨ Add New Task" if not self.task else "✏️ Edit Task")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #cba6f7; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        layout.addWidget(QLabel("Title *"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title...")
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Description"))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Enter description (optional)...")
        self.desc_input.setMaximumHeight(80)
        layout.addWidget(self.desc_input)

        layout.addWidget(QLabel("Priority *"))
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["low", "medium", "high"])
        layout.addWidget(self.priority_combo)

        layout.addWidget(QLabel("Tag"))
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Enter tag (optional)...")
        layout.addWidget(self.tag_input)

        layout.addWidget(QLabel("Due Date (YYYY-MM-DD)"))
        self.due_input = QLineEdit()
        self.due_input.setPlaceholderText("e.g., 2025-12-31")
        layout.addWidget(self.due_input)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        self.update_theme(self.current_theme)
    
    def update_theme(self, theme):
        self.current_theme = theme
        if theme == "dark":
            self.setStyleSheet("""
                QDialog {
                    background-color: #1e1e2e;
                }
                QLabel {
                    color: #cba6f7;
                    font-size: 13px;
                    font-weight: bold;
                    margin-top: 10px;
                    margin-bottom: 5px;
                }
                QLineEdit, QTextEdit, QComboBox {
                    background-color: #2a2a3a;
                    border: 1px solid #313244;
                    border-radius: 12px;
                    padding: 10px;
                    color: #cdd6f4;
                    font-size: 13px;
                }
                QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                    border: 1px solid #cba6f7;
                }
                QPushButton {
                    background-color: #cba6f7;
                    color: #1e1e2e;
                    border: none;
                    border-radius: 25px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: bold;
                    margin-top: 20px;
                }
                QPushButton:hover {
                    background-color: #b4befe;
                }
                QPushButton#cancel {
                    background-color: #313244;
                    color: #cdd6f4;
                }
                QPushButton#cancel:hover {
                    background-color: #45475a;
                }
            """)
        else:  # light mode
            self.setStyleSheet("""
                QDialog {
                    background-color: #faf5ff;
                }
                QLabel {
                    color: #b87cff;
                    font-size: 13px;
                    font-weight: bold;
                    margin-top: 10px;
                    margin-bottom: 5px;
                }
                QLineEdit, QTextEdit, QComboBox {
                    background-color: #ffffff;
                    border: 1px solid #e0d0ff;
                    border-radius: 12px;
                    padding: 10px;
                    color: #4a4a6a;
                    font-size: 13px;
                }
                QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                    border: 1px solid #b87cff;
                }
                QPushButton {
                    background-color: #b87cff;
                    color: white;
                    border: none;
                    border-radius: 25px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: bold;
                    margin-top: 20px;
                }
                QPushButton:hover {
                    background-color: #d4a5ff;
                }
                QPushButton#cancel {
                    background-color: #f0e6ff;
                    color: #b87cff;
                }
                QPushButton#cancel:hover {
                    background-color: #e0d0ff;
                }
            """)

    def load_task_data(self):
        if self.task:
            self.title_input.setText(self.task.title)
            if self.task.description:
                self.desc_input.setPlainText(self.task.description)
            self.priority_combo.setCurrentText(self.task.priority)
            if self.task.tag:
                self.tag_input.setText(self.task.tag)
            if self.task.due_date:
                self.due_input.setText(self.task.due_date)

    def get_task_data(self):
        title = self.title_input.text().strip()
        title , b = TaskValidator.get_valid_title(title)
        if not b:
            QMessageBox.warning(self, "Error", title)
            return None

        description = self.desc_input.toPlainText().strip()
        description = description if description else None

        priority = self.priority_combo.currentText()
        tag = self.tag_input.text().strip()
        tag = tag if tag else None

        due_date = self.due_input.text().strip()
        due_date, check = TaskValidator.get_valid_due_date(due_date)
        if not check:  
            QMessageBox.warning(self, "Error", due_date)
            return None

        return {
            'title': title,
            'description': description,
            'priority': priority,
            'tag': tag,
            'due_date': due_date
        }


class TaskItemWidget(QWidget):
    
    def __init__(self, task: Task, parent=None, on_edit=None, on_delete=None):
        super().__init__(parent)
        self.task = task
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.theme = "dark"
        self.setup_ui()

    def set_theme(self, theme):
        # Update the widget's theme (dark/light mode)
        self.theme = theme
        self.update_styles()

    def update_styles(self):
        # Apply color styles based on current theme
        if self.theme == "dark":
            bg_color = "#1e1e2e"
            bg_hover = "#2a2a3a"
            border_color = "#313244"
            tag_bg = "#313244"
            status_active_color = "#a6e3a1"
            status_inactive_color = "#f38ba8"
        else:
            bg_color = "#ffffff"
            bg_hover = "#faf5ff"
            border_color = "#d9c9ff"
            tag_bg = "#f0e6ff"
            status_active_color = "#b87cff"
            status_inactive_color = "#d9c9ff"

        self.setStyleSheet(f"""
            TaskItemWidget {{
                background-color: {bg_color};
                border-radius: 16px;
                border: 1px solid {border_color};
            }}
            TaskItemWidget:hover {{
                background-color: {bg_hover};
                border: 1px solid #b87cff;
            }}
        """)

    def setup_ui(self):
        # Create and arrange all visual components of the task item
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)

        # Top row with status, title, priority, and action buttons
        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        # Status indicator
        status_text = "●" if not self.task.active else "○"
        status_label = QLabel(status_text)
        if self.task.active:
            status_label.setStyleSheet("color: #a6e3a1; font-size: 20px; font-weight: bold;")
        else:
            status_label.setStyleSheet("color: #f38ba8; font-size: 20px; font-weight: bold;")
        top_row.addWidget(status_label)

        # Task title
        title_label = QLabel(self.task.title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        if self.task.active:
            title_label.setStyleSheet("color: #cdd6f4;")
        else:
            title_label.setStyleSheet("color: #6c7086; text-decoration: line-through;")
        top_row.addWidget(title_label)

        top_row.addStretch()

        # Priority badge with gradient colors
        priority_colors = {
            "high": ("#f38ba8", "#e64553"),
            "medium": ("#fab387", "#f9a06e"),
            "low": ("#a6e3a1", "#89dceb")
        }
        color1, color2 = priority_colors.get(self.task.priority, ("#6c7086", "#585b70"))
        priority_badge = QLabel(self.task.priority.upper())
        priority_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        priority_badge.setFixedSize(70, 24)
        priority_badge.setStyleSheet(f"""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {color1}, stop:1 {color2});
            color: #1e1e2e;
            border-radius: 45px;
            font-size: 10px;
            font-weight: bold;
        """)
        top_row.addWidget(priority_badge)

        # Edit button
        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setFixedSize(32, 32)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cba6f7;
                border: none;
                border-radius: 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #cba6f7;
                color: #1e1e2e;
            }
        """)
        self.edit_btn.clicked.connect(lambda: self.on_edit(self.task) if self.on_edit else None)

        # Delete button
        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setFixedSize(32, 32)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #f38ba8;
                border: none;
                border-radius: 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f38ba8;
                color: #1e1e2e;
            }
        """)
        self.delete_btn.clicked.connect(lambda: self.on_delete(self.task) if self.on_delete else None)

        top_row.addWidget(self.edit_btn)
        top_row.addWidget(self.delete_btn)
        layout.addLayout(top_row)

        # Description
        if self.task.description:
            desc_label = QLabel(self.task.description)
            desc_label.setStyleSheet("color: #a6adc8; font-size: 12px; padding-left: 28px;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        # Bottom row with tag and due date
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(15)

        if self.task.tag:
            tag_label = QLabel(f"🏷️ {self.task.tag}")
            tag_label.setStyleSheet("""
                background-color: #313244;
                color: #cba6f7;
                padding: 4px 12px;
                border-radius: 15px;
                font-size: 11px;
            """)
            bottom_row.addWidget(tag_label)

        if self.task.due_date:
            date_label = QLabel(f"📅 {self.task.due_date}")
            date_label.setStyleSheet("color: #6c7086; font-size: 11px;")
            bottom_row.addWidget(date_label)

        bottom_row.addStretch()
        layout.addLayout(bottom_row)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load saved theme from file
        try:
            with open("theme.txt", "r") as f:
                self.current_theme = f.read().strip()
                if self.current_theme not in ["dark", "light"]:
                    self.current_theme = "dark"   # Default to dark mode
        except:
            self.current_theme = "dark"

        self.data_repo = DataRepository()
        self.tasks = []
        self.load_tasks()
        self.setup_ui()

    def load_tasks(self):
        self.tasks = self.data_repo.load_from_json()

    def save_tasks(self):
        self.data_repo.save_to_json(self.tasks)

    def toggle_theme(self):
        # Close any open dialogs to prevent theme inconsistency
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QDialog):
                widget.reject()

        if self.current_theme == "dark":
            new_theme = "light"
        else:
            new_theme = "dark"

        with open("theme.txt", "w") as f:
            f.write(new_theme)

        subprocess.Popen([sys.executable, __file__])
        sys.exit(0)

    def on_add_task_clicked(self):
        dialog = AddEditTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_task_data()
            if data:
                task_manager.add_task(data['title'],data['description'],data['priority'],data['due_date'],data['tag'], self.tasks)
                self.load_tasks()
                self.sort_combo.setCurrentIndex(0)
                self.refresh_list()
                self.show_temp_message("Task saved!")

    def on_import_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select json File", "", "json Files (*.json)")
        if file_path:
            self.json_file_path = file_path
            text , check = task_manager.import_tasks(self.json_file_path) 
            if check:
                self.load_tasks()
                self.sort_combo.setCurrentIndex(0)
                self.refresh_list()
                self.show_temp_message("Successfully imported!")
            else:
                QMessageBox.warning(self, "Error", text)
                 
    def on_export_clicked(self):
        text , check = task_manager.export_tasks()
        if not check:
            QMessageBox.warning(self, "Error", text)     
        else:  
            self.show_temp_message("Successfully exported! check export.json")     

    def setup_ui(self):
        # Build the entire user interface layout and styling
        self.setWindowTitle("Task Manager")
        self.setFixedSize(500, 800)

        # Apply theme
        if self.current_theme == "dark":
            # Dark mode styles
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #181825, stop:1 #1e1e2e);
                }
                QListWidget {
                    background-color: transparent;
                    border: none;
                    outline: none;
                }
                QListWidget::item {
                    background-color: transparent;
                    padding: 8px;
                    border-radius: 16px;
                }
                QScrollBar:vertical {
                    background-color: #1e1e2e;
                    width: 8px;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical {
                    background-color: #cba6f7;
                    border-radius: 4px;
                }
                QLineEdit, QComboBox {
                    background-color: #2a2a3a;
                    color: #cdd6f4;
                    border: 1px solid #313244;
                    border-radius: 12px;
                    padding: 10px 15px;
                    font-size: 13px;
                }
                QLineEdit:focus, QComboBox:focus {
                    border: 1px solid #cba6f7;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: #2a2a3a;
                    color: #cdd6f4;
                    selection-background-color: #cba6f7;
                    border-radius: 8px;
                }
                QLabel#time_label {
                    color: #a6adc8;
                    background-color: #2a2a3a;
                    padding: 5px 15px;
                    border-radius: 20px;
                }
                QLabel {
                    background-color: transparent;
                }
            """)
            theme_icon = "☀️"
            theme_btn_style = """
                QPushButton {
                    background-color: #2a2a3a;
                    border: none;
                    border-radius: 22px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background-color: #cba6f7;
                }
            """
            search_frame_style = """
                QWidget {
                    background-color: #2a2a3a;
                    border-radius: 20px;
                }
            """
            sort_widget_style = "background-color: #2a2a3a; border-radius: 20px;"
            search_btn_style = """
                QPushButton {
                    background-color: #cba6f7;
                    border: none;
                    border-radius: 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #b4befe;
                }
            """
            sort_combo_style = """
                background-color: transparent;
                border: 1px solid #585b70; 
                border-radius: 8px; 
                padding: 5px;
                color: #cba6f7;
                padding-bottom: 7px;
                padding-top: 7px;
                margin-left: 2px;
                margin-right: 2px;
            """
            fab_style = """
                QPushButton {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #cba6f7, stop:1 #b4befe);
                    color: #1e1e2e;
                    border: none;
                    border-radius: 32px;
                    font-size: 32px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #b4befe, stop:1 #cba6f7);
                }
            """
            status_style = """
                QLabel {
                    background-color: #2a2a3a;
                    color: #a6e3a1;
                    padding: 8px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                }
            """
            name_label_color = "#cba6f7"

        else:  # Light mode
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #faf5ff;
                }
                QMainWindow {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #f5f0ff, stop:1 #faf5ff);
                }
                QListWidget {
                    background-color: transparent;
                    border: none;
                    outline: none;
                }
                QListWidget::item {
                    background-color: transparent;
                    padding: 8px;
                    border-radius: 16px;
                }
                QScrollBar:vertical {
                    background-color: #f0e6ff;
                    width: 8px;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical {
                    background-color: #b87cff;
                    border-radius: 4px;
                }
                QLineEdit, QComboBox {
                    background-color: #ffffff;
                    color: #4a4a6a;
                    border: 1px solid #e0d0ff;
                    border-radius: 12px;
                    padding: 10px 15px;
                    font-size: 13px;
                }
                QLineEdit:focus, QComboBox:focus {
                    border: 1px solid #b87cff;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: #ffffff;
                    color: #4a4a6a;
                    selection-background-color: #b87cff;
                    border-radius: 8px;
                }
                QLabel#time_label {
                    color: #6a5acd;
                    background-color: #f5f0ff;
                    padding: 5px 15px;
                    border-radius: 20px;
                }
                QLabel {
                    background-color: transparent;
                }
            """)
            theme_icon = "🌙"
            theme_btn_style = """
                QPushButton {
                    background-color: #f5f0ff;
                    border: none;
                    border-radius: 22px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background-color: #b87cff;
                }
            """
            search_frame_style = """
                QWidget {
                    background-color: #f5f0ff;
                    border-radius: 20px;
                }
            """
            sort_widget_style = "background-color: #f5f0ff; border-radius: 20px;"
            search_btn_style = """
                QPushButton {
                    background-color: #b87cff;
                    border: none;
                    border-radius: 20px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #d4a5ff;
                }
            """
            sort_combo_style = """
                QComboBox {
                    background-color: transparent;
                    border: none;
                    padding: 5px;
                    color: #b87cff;
                }
            """
            fab_style = """
                QPushButton {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #b87cff, stop:1 #d4a5ff);
                    color: white;
                    border: none;
                    border-radius: 32px;
                    font-size: 32px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #d4a5ff, stop:1 #b87cff);
                }
            """
            status_style = """
                QLabel {
                    background-color: #f5f0ff;
                    color: #b87cff;
                    padding: 8px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: bold;
                }
            """
            name_label_color = "#b87cff"

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ----- HEADER -----
        header = QHBoxLayout()

        # App title
        name_label = QLabel("TaskFlow")
        name_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        name_label.setStyleSheet(f"color: {name_label_color};")
        header.addWidget(name_label)

        header.addStretch()

        # Theme toggle button
        self.theme_btn = QPushButton(theme_icon)
        self.theme_btn.setFixedSize(45, 45)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setStyleSheet(theme_btn_style)
        self.theme_btn.clicked.connect(self.toggle_theme)
        header.addWidget(self.theme_btn)

        # Live clock display
        self.time_label = QLabel()
        self.time_label.setObjectName("time_label")
        self.time_label.setFont(QFont("Segoe UI", 14))
        header.addWidget(self.time_label)

        main_layout.addLayout(header)

        # ----- SEARCH & SORT -----
        search_frame = QWidget()
        search_frame.setStyleSheet(search_frame_style)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 5, 5, 5)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search tasks...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                padding: 8px 0;
            }
        """)

        self.search_btn = QPushButton("🔍")
        self.search_btn.setFixedSize(40, 40)
        self.search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_btn.setStyleSheet(search_btn_style)
        self.search_btn.clicked.connect(self.on_search_clicked)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)

        sort_widget = QWidget()
        sort_widget.setStyleSheet(sort_widget_style)
        sort_layout = QHBoxLayout(sort_widget)
        sort_layout.setContentsMargins(15, 5, 10, 5)

        sort_label = QLabel("Sort by:")
        sort_label.setStyleSheet("color: #a6adc8; font-size: 12px;")

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["-", "status", "priority"])
        self.sort_combo.setStyleSheet(sort_combo_style)
        self.sort_combo.currentIndexChanged.connect(self.on_sort_changed)

        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)

        # Combine search and sort horizontally
        top_layout = QHBoxLayout()
        top_layout.addWidget(search_frame, 2)
        top_layout.addWidget(sort_widget, 1)
        main_layout.addLayout(top_layout)

        # ----- TASK LIST -----
        self.task_list = QListWidget()
        self.task_list.setSpacing(15)
        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: transparent;
                padding: 5px;
                border-radius: 16px;
            }
        """)
        main_layout.addWidget(self.task_list)

        # ----- FAB BUTTON -----
        self.fab_button = QPushButton("+")
        self.fab_button.setFixedSize(65, 65)
        self.fab_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fab_button.setStyleSheet(fab_style)
        self.fab_button.clicked.connect(self.show_fab_menu)

        fab_layout = QHBoxLayout()
        fab_layout.addStretch()
        fab_layout.addWidget(self.fab_button)
        main_layout.addLayout(fab_layout)

        # ----- STATUS LABEL -----
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(status_style)
        main_layout.addWidget(self.status_label)

        # Start clock update timer
        self.update_time()
        self.refresh_list()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
 
    def update_time(self):
        now = datetime.now().strftime("%H:%M")
        self.time_label.setText(now)

    def refresh_list(self, tasks = None):
        # Refresh the task list display
        if tasks == None:
            tasks = self.tasks
            
        self.task_list.clear()
        
        # Show empty state message if no tasks
        if not tasks:
            empty_label = QLabel("No tasks yet!\nTap + to add your first task")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("color: #6c7086; font-size: 14px; padding: 50px;")
            empty_item = QListWidgetItem()
            empty_item.setSizeHint(QSize(400, 150))
            self.task_list.addItem(empty_item)
            self.task_list.setItemWidget(empty_item, empty_label)
            return
        
        # Create widget for each task
        for task in tasks:
            item = QListWidgetItem()
            item.setSizeHint(QSize(400, 100))
            
            widget = TaskItemWidget(task, self, self.on_edit_clicked, self.on_delete_clicked)
            widget.mouseDoubleClickEvent = lambda e, t=task: self.on_status_clicked(t)

            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, widget)

    def show_context_menu(self, task):
        from PyQt6.QtWidgets import QMenu
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #2D2D2D;
                color: white;
                border: 1px solid #404040;
            }
            QMenu::item:selected {
                background-color: #9C27B0;
            }
        """)

        edit_action = menu.addAction("✏️")
        delete_action = menu.addAction("🗑️")

        action = menu.exec(self.cursor().pos())

        if action == edit_action:
            self.on_edit_clicked(task)
        elif action == delete_action:
            self.on_delete_clicked(task)

    def on_status_clicked(self, task):
        task.active = not task.active
        self.save_tasks()
        self.load_tasks()
        self.refresh_list()
        self.show_temp_message("Task status updated!")

    def on_edit_clicked(self, task):
        # Handle edit button click
        dialog = AddEditTaskDialog(self, task)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_task_data()
            if data:
                text , check = task_manager.edit_task(task.id , data['title'],data['description'],data['priority'],data['due_date'],data['tag'], self.tasks)
                if not check:
                    QMessageBox.warning(self, "Error", text)   
                else:
                    self.load_tasks()
                    self.refresh_list()
                    self.show_temp_message("Task updated!")

    def on_delete_clicked(self, task):
        # Handle delete button click - show confirmation dialog then delete
        msg_box  = QMessageBox(
            QMessageBox.Icon.Question, 
            "Confirm Delete", 
            f"Delete '{task.title}'?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            self
        )
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QMessageBox QLabel {
                color: #cdd6f4;
            }
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
        """)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            task_manager.delete_task(task, self.tasks)
            self.load_tasks()
            self.refresh_list()
            self.show_temp_message("Task deleted!")

    def on_search_clicked(self):
        # Filter tasks based on search input
        search_text = self.search_input.text().strip()
        # Clear search to show all tasks
        if not search_text:
            self.load_tasks()
            self.sort_combo.setCurrentIndex(0)
            self.refresh_list()
            self.sort_combo.clearEditText()
        else:
            # Filter tasks by title or tag
            filtered_tasks = task_manager.search_task(self.tasks, search_text)
            self.refresh_list(filtered_tasks)
            
    def on_sort_changed(self, index: int):
        # Sort tasks based on selected criteria (status or priority)
        sort_key = self.sort_combo.currentText()
        self.tasks = task_manager.sort_tasks(sort_key, self.tasks)
        
        self.refresh_list()
               
    def show_temp_message(self, message):
        # Display temporary status message for 2 seconds
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.setText(""))

    def show_fab_menu(self):
        # Show floating action button menu with additional options
        if hasattr(self, "fab_overlay") and self.fab_overlay.isVisible():
            self.fab_overlay.hide()
            return

        # Create semi-transparent overlay
        self.fab_overlay = QWidget(self)
        self.fab_overlay.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.fab_overlay.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.7);
            }
        """)
        self.fab_overlay.setGeometry(0, 0, self.width(), self.height())
        self.fab_overlay.show()
        self.fab_overlay.mousePressEvent = lambda event: self.fab_overlay.hide()

        # Menu container
        container = QWidget(self.fab_overlay)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(12)

        # Menu buttons
        btn_add = QPushButton("➕ Add Task")
        btn_import = QPushButton("📥 Import")
        btn_export = QPushButton("📤 Export")

        for btn in (btn_add, btn_import, btn_export):
            btn.setFixedHeight(50)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a3a;
                    color: #cdd6f4;
                    border-radius: 25px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: bold;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #cba6f7;
                    color: #1e1e2e;
                }
            """)
            container_layout.addWidget(btn)

        # Position menu at bottom-right
        overlay_layout = QVBoxLayout(self.fab_overlay)
        overlay_layout.setContentsMargins(0, 0, 25, 100)
        overlay_layout.addWidget(container, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        # Connect buttons to their functions
        btn_add.clicked.connect(self.on_add_task_clicked)
        btn_import.clicked.connect(self.on_import_clicked)
        btn_export.clicked.connect(self.on_export_clicked)

        # Hide overlay when any button is clicked
        for btn in (btn_add, btn_import, btn_export):
            btn.clicked.connect(lambda *_: self.fab_overlay.hide())



def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()