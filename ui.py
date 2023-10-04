import sys
import typing
from database import Database 
from PyQt5.QtWidgets import  QMenuBar, QCheckBox, QAction, QApplication, QToolBar, QMessageBox,  QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QFileDialog
from PyQt5.QtCore import Qt

class UiClass(QMainWindow):
    def __init__(self):
        super().__init__()

        #current file
        self.current_file = None
        self.db = Database('settings.db')

        self.initUI()

        self.load_dark_mode_setting()
    def initUI(self):

        self.dark_mode = False  

        #main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('NoteX')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        #text
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)


        #navbar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)
        

        #save button
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_note)
        toolbar.addWidget(save_button)

        #dark mode
        dark_mode_button = QPushButton('Change mode', self)
        dark_mode_button.clicked.connect(self.toggle_dark_mode)
        toolbar.addWidget(dark_mode_button)


        #navbar menu
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('note')


        #menu - new file
        new_note_action = QAction('New note', self)
        new_note_action.triggered.connect(self.new_note)
        file_menu.addAction(new_note_action)


        #menu - open file
        open_note_action = QAction('Open note', self)
        open_note_action.triggered.connect(self.open_note)
        file_menu.addAction(open_note_action)


        #menu - save file
        save_note_action = QAction('Save', self)
        save_note_action.triggered.connect(self.save_note)
        file_menu.addAction(save_note_action)

        #choose main mode
        dark_mode_checkbox = QCheckBox('Automate mode', self)
        dark_mode_checkbox.setChecked(self.dark_mode)
        dark_mode_checkbox.stateChanged.connect(self.toggle_auto_dark_mode)
        toolbar.addWidget(dark_mode_checkbox)

    #save button function
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
    
    

    ### Alert ### 

    #check document
    def check_modified_document(self):
        if self.text_edit.document().isModified():

        # Alert
            reply = QMessageBox.question(self, 'Save changes', 'Do you want to save the note?', 
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        # Save
            if reply == QMessageBox.Yes:
                self.save_note()
        # Cancel
            elif reply == QMessageBox.Cancel:
                return False
        return True


    def closeEvent(self, event):
        if not self.check_modified_document():
            event.ignore()
        else:
            event.accept()

#new note
    def new_note(self):
        if not self.check_modified_document():
            return
        self.text_edit.clear()

#open note
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

#dark mode
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        if self.dark_mode:
            self.setStyleSheet("background-color: black; color: lightgray;")
            self.text_edit.setStyleSheet("background-color: black; color: lightgray;")
        else:
            self.setStyleSheet("background-color: white; color: black;")
            self.text_edit.setStyleSheet("background-color: white; color: black;")

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