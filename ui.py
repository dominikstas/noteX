import sys
import typing
from PyQt5.QtWidgets import  QMenuBar, QAction, QApplication, QToolBar, QMessageBox,  QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QFileDialog

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
        

        #save button
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_note)
        toolbar.addWidget(save_button)


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
    
    #save button function
    def save_note(self):
        options = QFileDialog.Options()
        options != QFileDialog.DontUseNativeDialog 
        file_name, _ = QFileDialog.getSaveFileName(self, "Save file", ".txt", "Text files (*.txt);;All files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())
    
    

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
