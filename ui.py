import sys
import typing
from PyQt5.QtWidgets import  QToolBar, QMessageBox,  QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QFileDialog

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

        #text
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)


        #navbar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)
        
        #open button
        open_button = QPushButton('Open file', self)
        open_button.clicked.connect(self.open_note)
        toolbar.addWidget(open_button)

        #save button
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_note)
        toolbar.addWidget(save_button)

        #create new file button
        new_button = QPushButton('New', self)
        new_button.clicked.connect(self.new_note)
        toolbar.addWidget(new_button)
    
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

    #create button function
    def new_note(self):
        self.text_edit.clear()

    
    #Check if user save his file before quit
    def closeEvent(self, event):
        
        #check if document is modified
        if self.text_edit.document().isModified():
            
            #Alert
            reply = QMessageBox.question(self, 'Save changes', 'Do you want to save the note?', 
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            #Save
            if reply == QMessageBox.Yes:
                self.save_note()
            #Cancel
            elif reply == QMessageBox.Cancel:
                event.ignore()
            #Discard
            elif reply == QMessageBox.No:
                sys.exit()