# this controls the database interactions in pyside6
import sys
import os
import platform
from loguru import logger


import config_mycal
from Recipe1 import Ui_MainWindow


from PySide6.QtCore import (QSize, Qt ,QRect,
QCoreApplication,Slot,Signal,QAbstractListModel,QAbstractTableModel,QMetaObject,QModelIndex)
from PySide6.QtGui import QAction,QDoubleValidator,QFont
from PySide6.QtWidgets import QWidget 
from PySide6.QtUiTools import QUiLoader

from PySide6.QtSql import QSqlDatabase , QSql,QSqlTableModel,QSqlQueryModel,QSqlQuery

from PySide6.QtWidgets import (
QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFileDialog,
    QFontComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListView,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QStatusBar,
    QTimeEdit,
    QTableView,
    QMenuBar,
    QVBoxLayout,
    QAbstractItemView,
    QGridLayout,
    QTextEdit
    
)

class NewWindow(QMainWindow):
        def __init__(self,Title =  None):
            super().__init__()
            layout = QVBoxLayout()

            self.label = QLabel("Another Window")
            if(Title == None):
                self.setWindowTitle("MyCal")
            else:
                self.setWindowTitle(Title)
        
            layout.addWidget(self.label)
            self.setLayout(layout)


class RecipeModel(QAbstractTableModel):

    def __init__(self,recipes=None,header_labels=None):
        super().__init__()

    #When subclassing QAbstractListModel, you must provide implementations of the rowCount() and data() functions. 
    # Well behaved models also provide a headerData() implementation.
    # this means we will have to define the data and rowCount
    # see also https://doc.qt.io/qt-6/qabstractlistmodel.html

        self.recipes = recipes or [[]] #recipes will be a 2d array or a nested list
        self.header_labels = header_labels = ["weight", "unit","ingredient"]
    def data(self, index, role):
        if role == Qt.DisplayRole or Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            value = self.recipes[index.row()][index.column()]
            # check for type
            if isinstance(value,float):
                
                return "%.2f" % value

            if isinstance(value,str):
                return "%s" % value

 
            return value
       
           
 
    def rowCount(self,  parent=QModelIndex()):
        return len(self.recipes)
    
    def columnCount(self,parent=QModelIndex()):
        return len(self.recipes[0])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
         if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
         return None
    
    def insertRows(self, position, rows=1,parent=QModelIndex(),*args,**kwargs):
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            self.recipes.insert(position, [""] * self.columnCount())
        self.endInsertRows()
        return True

    def setData(self, index, value, role ):
        if role == Qt.ItemDataRole.EditRole:
            self.recipes[index.row()][index.column()] = value
            return True
        return False
    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def StoreValue(self):
        return self.recipes


class MyRecipeWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ContrlDB(QMainWindow):

    def __init__(self,Title=None,db_name=None,db_user=None,db_system=None,db_pwd = None):
        super().__init__()
        self.db_name = db_name
        self.db_user = db_user
        self.db_system = db_system
        if db_pwd == None:
        
            temp = '/Users/klein/git/qt_exercises/config/pw.txt'
            if os.path.exists(temp):
                with open(temp, 'r') as file:
                    password = file.read().rstrip()
                    self.db_pwd = password
            else:
                self.db_pwd = db_pwd


        self.SetupLogger()
        #self.CreateIngredientsForm()
        self.ingredients_suppress_columns = ['Sugar',
                    'Portion_size',
                    'Saturated',
                    'Fiber',
                    'Salt',
                    'Sodium',
                    'Product_source'
                    ]
            
        self.recipe_suppress_columns = ['Sugar',
                    'Portions',
                    'Description',
                    'Saturated_fat',
                    'Fiber',
                    'Salt',
                    'Sodium',
                    'Ingredients',
                    'Time',
                    'Images',
                    'vegetarian']

        self.version = '0.3'
        logger.info('******************************************************************************************************** \n\n\n')

        logger.info(' This is version %s' % self.version)
        logger.info('\n\n\n***************************************************************************************************** \n')


        
    
    def ConnectDataBase(self):
        ''' establish contact to database'''


        #instantiate the connection
        self.mycal_db  = QSqlDatabase.addDatabase(self.db_system)
        self.mycal_db.setHostName("localhost")
        self.mycal_db.setDatabaseName(self.db_name)
        self.mycal_db.setUserName(self.db_user)
        self.mycal_db.setPassword(self.db_pwd)
        

 #       self.mycal_db.setPassword(self.CM.pwd)

        result = self.mycal_db.open()
        if(result):
            logger.info('connection succsessful')
            # here we get the connection name
            # will be needed when we want to close the connection
            self.connection_name = self.mycal_db.connectionName()
            logger.info(' database connection name %s' % self.connection_name)
            #self.ShowTables()
        else:
            logger.error('connection failed, exciting')
            sys.exit(0)

    def SetupLogger(self):


        logger.remove(0)
        #now we add color to the terminal output
        logger.add(sys.stdout,
                colorize = True,format="<green>{time}</green>    {function}   {line}    {level}     <level>{message}</level>" ,
                level = "INFO")



        fmt =  "{time} - {name}-   {function} -{line}- {level}    - {message}"
        logger.add('info.log', format = fmt , level = 'INFO',rotation="1 day")


        # set the colors of the different levels
        logger.level("INFO",color ='<black>')
        logger.level("WARNING",color='<green>')
        logger.level("ERROR",color='<red>')
        logger.level("DEBUG",color = '<blue>')
 
        return



    def ShowTables(self):
        '''prints all the tables in the databe'''
        self.table_list = self.mycal_db.tables(type=QSql.Tables)
        for k in range(0,len(self.table_list)):
            print(self.table_list[k])

        #Create list box
        self.mybox = QComboBox()
        #Insert at index 0 the whole list
        self.mybox.insertItems(0,self.table_list)
        # create independent window
       
        #self.setCentralWidget(self.mybox)


        return

    def ViewTable(self,table,suppress_columns=[],editmode=True,columnwidth=[],Title = None, showTable = True):
        self.table_view = QTableView()
        

        self.model = QSqlTableModel(db = self.mycal_db) 

 

        self.table_view.setModel(self.model)
        #prevent editing
        if(not editmode):
            self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.model.setTable(table)

        # get rid of columns
        columns_to_remove = suppress_columns
        for cn in columns_to_remove:
            idx = self.model.fieldIndex(cn) 
            self.model.removeColumns(idx, 1)


        self.model.select()
        # change column width
        for k in range(0,len(columnwidth)):
            self.table_view.setColumnWidth(k, columnwidth[k])
 
        self.setMinimumSize(QSize(300, 300)) 
        
        self.setCentralWidget(self.table_view)
        
        self.SetPosition(10,10)
        if(showTable):
            self.show()
        #self.setCentralWidget(table)


    def SetPosition(self,pos_x,pos_y):
        self.move(pos_x,pos_y)

    def CreateIngredientsForm1(self):
        """uses the form layout"""
    
       #always use self so window wll be persistent
        self.Inform = NewWindow(Title = "Add New Ingredient")
        self.Inform.setStyleSheet("background-color: yellow;")
     
        # setup geometry
        mysize=[400,300]
        myposit = [800,100]
    
        self.SizeWindow(self.Inform,myposit,mysize)

        # Create widgets
        self.name_label      = QLineEdit()
        self.name_label.setStyleSheet("background-color: rgb(3, 252, 227)")
        # force valid entr
        double_validator = QDoubleValidator(0, 500.0, 2)
 
        self.calory_label    = QLineEdit()
        self.calory_label.setStyleSheet("background-color: white")
        self.calory_label.setValidator(double_validator)
        
        self.carb_label      = QLineEdit()
        self.carb_label.setStyleSheet("background-color: white")
        self.carb_label.setValidator(double_validator)
        self.fat_label       = QLineEdit()
        self.fat_label.setStyleSheet("background-color: white")
        self.fat_label.setValidator(double_validator)
        self.prot_label      = QLineEdit() 
        self.prot_label.setStyleSheet("background-color: white")
        self.prot_label.setValidator(double_validator)
 
        SaveButton = QPushButton("Save")
        SaveButton.setStyleSheet("background-color: white")
        CancelButton = QPushButton("Cancel")
        CancelButton.setStyleSheet("background-color: red")

 
        # Create layout
        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_label)
        form_layout.addRow("Calories/100g", self.calory_label)
        form_layout.addRow("Fat", self.fat_label)
        form_layout.addRow("Carbohydrates", self.carb_label)
        form_layout.addRow("Protein", self.prot_label)
        form_layout.addRow(SaveButton)
        form_layout.addRow(CancelButton)

        mylayout = QVBoxLayout()
        mylayout.addLayout(form_layout)
        self.setLayout(mylayout)

        # Connect submit button
        SaveButton.clicked.connect(self.SaveIngredients)
        CancelButton.clicked.connect(lambda : self.Cancel(self.Inform))

        widget = QWidget()
        widget.setLayout(mylayout)
         




        self.Inform.setCentralWidget(widget)

        #for label in MyLabel:
        #    widget = QWidget()
        #    widget.setLayout(layout)
        #self.setCentralWidget(widget)


        # create the form

        self.Inform.show()
 

    def InsertRecord(self,table = None):
        """ this inserts a record into the cosen table
        I will use the query function to do this.
        The record contains the info to be added
        record=[name,energy,fat,carbohydrate,protein]
        
        This is the same for ingredients and receipes"""

        #Create table view
        if(table == "ingredients"):
                
            self.ViewTable(table = table,suppress_columns=self.ingredients_suppress_columns,showTable= False)
        else:
            self.ViewTable(table = table,suppress_columns=self.recipe_suppress_columns)

        self.model = QSqlQueryModel()
        self.table_view.setModel(self.model)
        #next we check we don't have an entry yet

        #Form the sql INSERT statement
        #       self.record = [Ing_name,Ing_calory,Ing_carb,Ing_fat,Ing_prot]
        #INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', 9.99);
        #INSERT INTO table (name,energy,carbohydrate,fat,protein) VALUES (self.record[0],
        #                                                               self.record[1],   
        #                                                               self.record[2],
        #                                                               self.record[3],
        #                                                               self.record[4]);
        temp = "'"+self.record[0]+"'"
        sql = 'INSERT INTO '+table+' (name,energy,carbohydrate,fat,protein) VALUES ('+temp+','+str(self.record[1])+','+str(self.record[2])+','+str(self.record[3])+','+str(self.record[4])+');'
        print(sql)

        query = QSqlQuery(sql,db=self.mycal_db)
        
        self.model.setQuery(query)
        logger.info(' inserted record %s into table  %s' % (self.record[0],table))
 
 

        return

    def MyRecipes_new(self):
        """using the QTdesigner"""
        self.MRD = MyRecipeWindow()
        self.MRD.show()

        # Load the model
        #self.header_labels = header_labels = ["weight", "unit","ingredient"]

        self.RecipeModel = RecipeModel()
        self.MRD.RecipeTableView.setModel(self.RecipeModel)


        #label the columns
        header = self.MRD.RecipeTableView.horizontalHeader()
         

        #poulate the combo box
        self.MRD.RecipeListCombo.setObjectName(u"RecipeListCombo")
        self.MRD.RecipeListCombo.addItems(self.GetRecipeList())


        #here we define the actions
        self.MRD.RecipeListCombo.currentTextChanged.connect(self.getSelectedRecipe)

        self.MRD.RecipeTableView.clicked.connect(self.on_item_click)

        # save button
        self.MRD.SaveRecipe.clicked.connect(self.save_recipe)

        #cancel button
        self.MRD.CancelButton.clicked.connect(lambda : self.Cancel(self.MRD))

        #add row button
        self.MRD.AddRowButton.clicked.connect(self.add_row)
       
       #new recipe button
        #self.MRD.NewRecipeButton.clicked.connect(self.create_new_recipe) 

        #if line has change
        self.MRD.NewRecipeName.returnPressed.connect(self.create_new_recipe)   
        #self.MRD.NewRecipeName.textChanged.connect(self.create_new_recipe)   

    def create_new_recipe(self):
        """creates new recipe"""
        #first get name
        self.new_recipe_name = self.MRD.NewRecipeName.text()
        logger.info("new recipe name %s" % self.new_recipe_name)
        #let's create a default starter table
        #first create the data list for the model
        self.RecipeModel.recipes = []

        self.recipe_ingredients=[['0','g',' '],['0','g',' '],['0','g',' '],['0','g',' '],['0','g',' ']]
        self.DisplayRecipeList()
        self.RecipeModel.layoutChanged.emit()


        return

    def calculate_values(self):
        """This routine calculates derived values like calories/100 g, protein etc."""
        pass

    def add_row(self):
        """ adds row to reipe table"""
        row_position = self.RecipeModel.rowCount()
        self.RecipeModel.insertRows(row_position)

        return

    def on_item_click(self, index):

        #columns and rows start from 0
        item_text = index.data()
        item_row = index.row()
        item_column = index.column()
        return
        

        #print(f"Clicked item: {item_text}")
        #print(index.row())

    def save_recipe(self):
        """gets called from clicking the save button"""
        record = self.RecipeModel.StoreValue()
        logger.info("ingredients %s "% record)
        #create original string
        record = self.pack_record(record)
        # Now update the record
        self.update_record('recipes','ingredients',record,self.selected_recipe)

        #remove window
        self.MRD.close()
 

        return
    
    def update_record(self,table,column_name,record,row_name):
        """ updates record for name in table
        example SQL statement 
        UPDATE recipes SET ingredients = '30 g almonds 60 g dry_tomatoes 517 g tenderloin' WHERE name='basil_tenderloin';
        """

        sql = 'UPDATE '+table+' SET '+column_name+' = \''+record+'\' WHERE name = \''+row_name+'\';'
        self.do_sql(sql)

        return

    def pack_record(self,record):
        """ put record back into original form for ingredients, which is just one string"""
        b=[]
        c=''
        a=record
        for k in range(len(a)):
            if(a[k][0]==''): break
            b.append(a[k][0]+' '+a[k][1]+' '+a[k][2]+' ')

        for k in range(0,len(b)):
            c = c+ b[k]
   
        # remove last space
        d = c[0:len(c)-1]
        return(d)


    def getSelectedText(self,s):
        self.selected_text = s
        logger.info("You have selected %s text" % self.selected_text)
        return


    def getSelectedRecipe(self,s):
        #Clear Buffer of recipes

              
        self.RecipeModel.recipes = []

        self.selected_recipe = s
        logger.info("You have selected %s recipe" % self.selected_recipe)

        # now we populate the listview
        self.FillRecipeIngredientList()

        # Now fill qlist
        self.DisplayRecipeList()

        # send signal list has been updated
        self.RecipeModel.layoutChanged.emit()

 

        return
    
    def do_sql(self,sql):
        """executes a sql statement"""
        query = QSqlQuery(sql,db=self.mycal_db)
        #model = QSqlQueryModel()
        return


    def FillRecipeIngredientList(self):
        # here we get the ingredients from the Recipe database
        # this is done with a query



        sql =' SELECT ingredients from recipes WHERE recipes.name LIKE \''+self.selected_recipe +'\' ;'
        query = QSqlQuery(sql,db=self.mycal_db)
        model = QSqlQueryModel()

        model.setQuery(query)
        while query.next():

            temp_value = ((query.value(0)))
        # now we have to work with string
        # the old database still had *u000a in front of the number
        # need first to strip this
        #check if temp contains *u000a 
        mask = 'u000a'
        if(mask in temp_value):
            temp_new = self.StripUnicode(temp_value,mask)
            #temp_new = self.StripUnicode(temp_new,'*')
        

            

        else:
            #already the new entry way
            temp_new1 = []
            temp_new = temp_value.split(' ')
            for k in range(0,len(temp_new),3):
                temp_new1.append([temp_new[k],temp_new[k+1],temp_new[k+2]])
            self.recipe_ingredients = temp_new1
            return

        
        delimiter = " g "
        result = temp_new.replace('u000a','')
        

        result1 = self.split_and_keep(result, delimiter)
        #  strip last *
        result11= result1[0]
        result2 = result11[:len(result1[0])-1].split('*')
        # we know that a string with underscores has a max of three spaces. Any number larger than this means words with spaces.
        #in other words 4 spaces means the 3rd has to be replaced with _ 5 spaces mean the 3rd and 4th
        result3 =[]
        for a in result2:
            space_indices = []
            for i, char in enumerate(a):
                if char == ' ':
                    space_indices.append(i)
    
            if len(space_indices) == 4:
                na = a[:space_indices[2]] + '_' + a[space_indices[2] + 1:]
             
                result3.append(na)

            elif len(space_indices) == 5:
                na = a[:space_indices[2]] + '_' + a[space_indices[2]+1:space_indices[3]] + '_' + a[space_indices[3] + 1:]
                result3.append(na)

            else:
                result3.append(a)


        recipe_string = result3
        #finally split every field up into 3 '10 g bean' -> [10,'g','bean]
        result4 =[]
        for i in range(len(result3)):
            temp = (result3[i].split(' '))
            result4.append(temp[0:3])
        self.recipe_ingredients = result4
        return

    def DisplayRecipeList(self):
        """loop through ingredient list and add"""
        

        for k in range(len(self.recipe_ingredients)):
            self.RecipeModel.recipes.append(self.recipe_ingredients[k])
        return


    def split_and_keep(self,text, delimiter):
        """deals with spaces instead of underscores"""
        result = []
        temp = ""
        for char in text:
            if char == delimiter:
                result.append(temp + char)
                temp = ""
            else:
                temp += char
        if temp:
            result.append(temp)
        return result




    def StripUnicode(self,mystring,mask):
        newstring =mystring.replace(mask,'')
        return newstring


    def GetRecipeList(self):
        """sql query to get all the names of the recpies
        will be used to popolate the recipe qlistbox"""
        sql = 'SELECT name from recipes ; '
        query = QSqlQuery(sql,db=self.mycal_db)
        model = QSqlQueryModel()

        model.setQuery(query)
        recipe_list = []
        while query.next():
            recipe_list.append(str(query.value(0)))

        return (recipe_list)





    def ModifyRecipe(self):
        pass

  
    def SizeWindow(self,window,myposit,mysize):
        """resizes the specified window ,where the parameters are two integer lists"""
        window.setGeometry(myposit[0],myposit[1],mysize[0],mysize[1])
        return
 

##########################################################################
    # section for signals and slots

    
    def Cancel(self,window):
        """ closes window without anything"""
        window.close()
        
 
 

    def SaveIngredients(self):
        """saving the ingredients"""
        Ing_name    = self.name_label.text()
        Ing_calory  = float(self.calory_label.text())
        Ing_carb    = float(self.carb_label.text())       
        Ing_fat     = float(self.fat_label.text())
        Ing_prot    = float(self.prot_label.text())

        #  this is the record we got from the form input

        #Check all fields are filled out
        if(Ing_calory !="" and Ing_carb !="" and Ing_fat!=""  and Ing_prot !=""):
            self.Inform.destroy() # destrorys the window.
            #self.Inform.close() # 

        #now we need to add the values to the ingredients table
        # first load table
        table_name = 'ingredients'
        self.ViewTable(table_name,suppress_columns=self.ingredients_suppress_columns)
        self.model = QSqlQueryModel()
        self.table_view.setModel(self.model)
        #next we check we don't have an entry yet

        
        #sql = "SELECT name from ingredients WHERE ingredients.name LIKE 'Almond%' ; "
        sql = "SELECT name from ingredients WHERE ingredients.name LIKE '"+Ing_name+"' ; "
        query = QSqlQuery(sql,db=self.mycal_db)
        
        self.model.setQuery(query)
        while query.next():
            logger.error(' entry name already exists, try again %s' % query.value(0))
            self.CreateIngredientsForm1()
            #myvalue = query.value(0)
        # Now we need to add this ingredient to the table

        self.record = [Ing_name,Ing_calory,Ing_carb,Ing_fat,Ing_prot]
        self.InsertRecord(table = table_name)
        return
    

app = QApplication(sys.argv) 

Title=None
db_name='recipe_ak'
db_user='klein'
db_system='QPSQL'
db_pwd = None

suppress_columns = ['Sugar',
                    'Portions',
                    'Description',
                    'Saturated_fat',
                    'Fiber',
                    'Salt',
                    'Sodium',
                    'Ingredients',
                    'Time',
                    'Images',
                    'vegetarian']
columnwidth = [40,200,200,200,200,200]

window = ContrlDB(Title = "ControlDB",
                  db_name=db_name,
                  db_user=db_user,
                  db_system=db_system)
#window.SetSize(800,500)
#window.SetPosition(100,500)

window.setStyleSheet("background-color: white;")
#window.CreateCalendar()



#window.show()
window.ConnectDataBase()
window.ShowTables()
#window.ViewTable('Recipes',suppress_columns=suppress_columns,columnwidth=columnwidth)
window.MyRecipes_new()
#window.CreateIngredientsForm1()

# now run the app
app.exec()