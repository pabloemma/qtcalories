from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QPushButton
from PySide6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QAction Example")

        # Create a menu bar
        menu_bar = self.menuBar()

        # Create a "File" menu
        file_menu = menu_bar.addMenu("File")

        # Create a "New" action
        new_action = QAction(QIcon.fromTheme("document-new"), "New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.setStatusTip("Create a new document")
        new_action.triggered.connect(self.new_document)
        file_menu.addAction(new_action)

 
       # Create a "Quit" action
        quitt_action = QAction("MyQuit", self)
        quitt_action.setShortcut("Ctrl+Q")
        quitt_action.setStatusTip("Quit the application")
        quitt_action.triggered.connect(self.quit_app)
        file_menu.addAction(quitt_action)

               # Create an "Open" action
        open_action = QAction(QIcon.fromTheme("document-open"), "Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Open an existing document")
        open_action.triggered.connect(self.open_document)
        file_menu.addAction(open_action)


        # Add a button to trigger an action
        button = QPushButton("Trigger New Action", self)
        button.clicked.connect(new_action.trigger)
        self.setCentralWidget(button)

    def new_document(self):
        print("New document created")

    def open_document(self):
        print("Open document")

    def quit_app(self):
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()