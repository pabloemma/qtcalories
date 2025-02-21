from PySide6.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        self.combo_box.currentIndexChanged.connect(self.on_changed)

        layout = QVBoxLayout(self)
        layout.addWidget(self.combo_box)

    def on_changed(self, index):
         print(f"Selected index: {index}, Text: {self.combo_box.currentText()}")

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()