import sys
from PyQt5.QtWidgets import (
    QShortcut, QMenuBar, QCheckBox, QAction, QApplication,
    QToolBar, QMessageBox, QMainWindow, QVBoxLayout,
    QTextEdit, QPushButton, QWidget, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QTextCursor, QTextListFormat
from database import Database

class UiClass(QMainWindow):
    def __init__(self):
        super().__init__()

        # Current file
        self.current_file = None
        self.db = Database('settings.db')
        self.initUI()
        self.load_dark_mode_setting()

        # Font
        self.font_size = 12

        # Shortcuts
        increase_font_shortcut = QShortcut(QKeySequence("Ctrl+1"), self)
        increase_font_shortcut.activated.connect(self.increase_font)

        decrease_font_shortcut = QShortcut(QKeySequence("Ctrl+2"), self)
        decrease_font_shortcut.activated.connect(self.decrease_font)

    def initUI(self):
        self.dark_mode = False

        # Save shortcut
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_note)

        # Main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('NoteX')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Text
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        # Navbar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        # Save button
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_note)
        toolbar.addWidget(save_button)

        # Dark mode button
        dark_mode_button = QPushButton('Change mode', self)
        dark_mode_button.clicked.connect(self.toggle_dark_mode)
        toolbar.addWidget(dark_mode_button)

        # Navbar menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('Note')

        # New note action
        new_note_action = QAction('New note', self)
        new_note_action.triggered.connect(self.new_note)
        file_menu.addAction(new_note_action)

        # Open note action
        open_note_action = QAction('Open note', self)
        open_note_action.triggered.connect(self.open_note)
        file_menu.addAction(open_note_action)

        # Save note action
        save_note_action = QAction('Save', self)
        save_note_action.triggered.connect(self.save_note)
        file_menu.addAction(save_note_action)

        # Choose main mode
        dark_mode_checkbox = QCheckBox('Automate mode', self)
        dark_mode_checkbox.setChecked(self.dark_mode)
        dark_mode_checkbox.stateChanged.connect(self.toggle_auto_dark_mode)
        toolbar.addWidget(dark_mode_checkbox)

        # List button
        bullet_list_button = QPushButton('Bullet list', self)
        bullet_list_button.clicked.connect(self.insert_bullet_list)
        toolbar.addWidget(bullet_list_button)

    # Save button function
    def save_note(self):
        if self.current_file is None:
            options = QFileDialog.Options()
            options != QFileDialog.DontUseNativeDialog
            file_name, _ = QFileDialog.getSaveFileName(self, "Save file", ".txt", "Text files (*.txt);;All files (*)", options=options)
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(self.text_edit.toPlainText())
                self.current_file = file_name
                self.update_window_title()
        else:
            with open(self.current_file, 'w') as file:
                file.write(self.text_edit.toPlainText())
            self.update_window_title()

    # Alert
    def check_modified_document(self):
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(self, 'Save changes', 'Do you want to save the note?',
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_note()
            elif reply == QMessageBox.Cancel:
                return False
        return True

    def closeEvent(self, event):
        if not self.check_modified_document():
            event.ignore()
        else:
            event.accept()

    # New note
    def new_note(self):
        if not self.check_modified_document():
            return
        self.text_edit.clear()

    # Open note
    def open_note(self):
        if not self.check_modified_document():
            return
        options = QFileDialog.Options()
        options != QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*.txt);;All files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.text_edit.setPlainText(file.read())
                self.current_file = file_name
                self.update_window_title()

    # Dark mode
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        theme = "background-color: black; color: lightgray;" if self.dark_mode else "background-color: white; color: black;"
        self.setStyleSheet(theme)
        self.text_edit.setStyleSheet(theme)

    def update_window_title(self):
        if self.current_file:
            self.setWindowTitle(f'NoteX - {self.current_file}')
        else:
            self.setWindowTitle('NoteX')

    def load_dark_mode_setting(self):
        self.dark_mode = self.db.load_dark_mode_setting()
        self.update_theme()

    def toggle_auto_dark_mode(self, state):
        self.dark_mode = state == Qt.Checked
        self.db.save_dark_mode_setting(self.dark_mode)
        self.update_theme()

    # Font
    # Increase font size
    def increase_font(self):
        self.update_font(3)

    # Decrease font size
    def decrease_font(self):
        self.update_font(-3)

    def update_font(self, num):
        cursor = self.text_edit.textCursor()
        char_format = cursor.charFormat()

        current_size = char_format.fontPointSize()
        new_size = max(1, current_size + num)

        char_format.setFontPointSize(new_size)
        cursor.mergeCharFormat(char_format)

    # Bullet list
    def insert_bullet_list(self):
        cursor = self.text_edit.textCursor()

        # Check if it's on or off
        cursor.movePosition(QTextCursor.StartOfBlock)
        list_format = cursor.blockFormat().toListFormat()

        if list_format.isValid() and list_format.style() == QTextListFormat.ListDisc:
            cursor.movePosition(QTextCursor.EndOfBlock)
            cursor.insertBlock()
        else:
            new_list_format = QTextListFormat()
            new_list_format.setStyle(QTextListFormat.ListDisc)
            cursor.createList(new_list_format)
