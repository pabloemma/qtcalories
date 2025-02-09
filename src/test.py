from PySide6.QtWidgets import QApplication, QListView, QStandardItemModel, QStandardItem
from PySide6.QtCore import QModelIndex
import sys

app = QApplication(sys.argv)

# Create a QListView
list_view = QListView()

# Create a QStandardItemModel
model = QStandardItemModel()

# Add some items to the model
model.appendRow(QStandardItem("Item 1"))
model.appendRow(QStandardItem("Item 2"))
model.appendRow(QStandardItem("Item 3"))

# Set the model to the list view
list_view.setModel(model)

# Replace "Item 2" with "New Item"
index_to_replace = model.index(1, 0)  # Get the index of "Item 2" (row 1, column 0)
new_item = QStandardItem("New Item")
model.setItem(index_to_replace, new_item)

# Show the list view
list_view.show()

app.exec_()
