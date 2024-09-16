
import sys
import os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt,QAbstractListModel
from PySide6.QtCore import Qt, QAbstractListModel
from PySide6.QtWidgets import QMainWindow, QApplication

from ToDo import Ui_MainWindow

basedir = os.path.dirname(__file__)
figdir = '/Users/klein/fugue-icons-3.5.6/icons/'
tick = QImage(os.path.join(figdir, "tick-button.png"))


class TodoModel(QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        # the todo is a list of tuples with [boolean, string]
        self.todos = todos or []



    #When subclassing QAbstractListModel, you must provide implementations of the rowCount() and data() functions. 
    # Well behaved models also provide a headerData() implementation.
    # this means we will have to define the data and rowCount
    # see also https://doc.qt.io/qt-6/qabstractlistmodel.html

    def data(self, index, role):
        if role == Qt.DisplayRole:
            status, text = self.todos[index.row()]
            return text
        
        if role == Qt.DecorationRole:
            status, text = self.todos[index.row()] 
            if status:
                return tick

    def rowCount(self, index):
        return len(self.todos)






class MainWindow(QMainWindow, Ui_MainWindow): 
    def __init__(self):
          super().__init__()
          self.setupUi(self)
          self.model = TodoModel([(False,'Get Paper'),(False,'Breakfast')])
          self.todoView.setModel(self.model)
          # nowe the first button, adding todos
          self.addButton.pressed.connect(self.add)
          #
          self.deleteButton.pressed.connect(self.delete)
          #
          self.completeButton.pressed.connect(self.complete)


    def add(self):
        """we get the text from the todoEdit, which we defined in the UI"""
        text = self.todoEdit.text()
        # now we remove white space from end.
        text = text.strip()

        #prevent empty strings:
        if text:
            # we get it from the model , where self.model is the instance and models
            # is a list of the model, as defined by self.todos = todos
            self.model.todos.append([False,text])

            #Here we’re emitting a model signal .layoutChanged to let the view know that the s
            # hape of the data has been altered. This triggers a refresh of the entirety of the view. 
            # If you omit this line, the todo will still be added but the QListView won’t update.
            self.model.layoutChanged.emit()
            # and finally we clear the text buffer
            self.todoEdit.setText("")

    def delete(self):
        """delete an entry"""

        #this took me a while, the selected indexes is a protected function
        # from QAbstractItemViewClass(); this damned inheriting business
        # from the definition: This convenience function returns a 
        # list of all selected and non-hidden item 
        # indexes in the view. The list contains no duplicates, and is not sorted.
        #indexes then returns the row index of the highglighted 
        #item
        indexes = self.todoView.selectedIndexes()
        # as I suspected, we use the first item, selectedInexes is a list
        myindex = indexes[0]

        myposition = myindex.row()  # this only takes the first item in the list
        # now we can remove that item from the list of todos
        del self.model.todos[myposition]
        # now we redraw since the list has changed
        self.model.layoutChanged.emit()
        #and clear the selection
        self.todoView.clearSelection()
    


        

    def complete(self):
 
        indexes = self.todoView.selectedIndexes()
        # as I suspected, we use the first item, selectedInexes is a list
        myindex = indexes[0]

        myposition = myindex.row()  # this only takes the first item in the list

        status, text = self.model.todos[myposition] 
        self.model.todos[myposition] = (True, text)
        # .dataChanged takes top-left and bottom right, which are
        # for a single selection.
        self.model.dataChanged.emit(myindex, myindex)
        # Clear the selection (as it is no longer valid).
        self.todoView.clearSelection()

        basedir = os.path.dirname(__file__)
        #print( 'current directory'  , os.getcwd()) 
        #print('path relative to', basedir) 
        #tick = QImage(os.path.join(figdir, "tick-button.png"))

        

        







app = QtWidgets.QApplication(sys.argv) 
window = MainWindow()
window.show()
app.exec()