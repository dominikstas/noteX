import sys
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QFileDialog

class UiClass(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
    def initUI(self):

        #main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('NoteX')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        
        #open button
        open_button = QPushButton('Open file', self)
        open_button.clicked.connect(self.open_note)
        layout.addWidget(open_button)

        #save button
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_note)
        layout.addWidget(save_button)
    
    #open button funcion
    def open_note(self):
        options = QFileDialog.Options()
        options != QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text files (*.txt);;All files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.text_edit.setPlainText(file.read())

    #save button function
    def save_note(self):
        options = QFileDialog.Options()
        options != QFileDialog.DontUseNativeDialog 
        file_name, _ = QFileDialog.getSaveFileName(self, "Save file", ".txt", "Text files (*.txt);;All files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())


