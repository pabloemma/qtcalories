from PySide6.QtWidgets import (QApplication, QTableView,
                              QWidget,
                             QVBoxLayout, QPushButton)
from PySide6.QtCore import QModelIndex, Qt,QAbstractTableModel

class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def insertRows(self, position, rows=1, parent=QModelIndex(), *args, **kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            self._data.insert(position, [""] * self.columnCount())
        self.endInsertRows()
        return True

    def setData(self, index, value, role=Qt.EditRole):
         if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
         return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class MyTableView(QWidget):
    def __init__(self, data):
        super().__init__()
        self.table_model = MyTableModel(data)
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        layout.addWidget(self.add_row_button)
        self.setLayout(layout)

    def add_row(self):
        row_position = self.table_model.rowCount()
        self.table_model.insertRow(row_position)


if __name__ == "__main__":
    app = QApplication([])
    initial_data = [["Row 1, Column 1", "Row 1, Column 2"],
                    ["Row 2, Column 1", "Row 2, Column 2"]]
    table_widget = MyTableView(initial_data)
    table_widget.show()
    app.exec()