# this controls the database interactions in pyside6
import sys
import os
import platform
from loguru import logger

import numpy as np #for pyinstaller
import config_mycal as CM
import IngredientTable as INTA

from Recipe1 import Ui_MainWindow

from missing_ingredient import Ui_MissingIngredient
from missing_ingredient_dialog import Ui_missing_ingredient_dialog
from pick_swiss_ingreds import Ui_Dialog
import pandas as PD # to pack the recipe information into a pandas dataframe
from IngredientTable import IngredientTable


from PySide6.QtCore import (QSize, Qt ,QRect,
QCoreApplication,Slot,Signal,QAbstractListModel,QAbstractTableModel,QMetaObject,QModelIndex)
from PySide6.QtGui import QAction,QDoubleValidator,QFont

from PySide6.QtUiTools import QUiLoader

from PySide6.QtSql import QSqlDatabase , QSql,QSqlTableModel,QSqlQueryModel,QSqlQuery
 
from PySide6.QtWidgets import (
QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDialog,
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
    QWidget,
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

            #here we stor the index of the field which has been clicked.
            self.clicked_row = index.row()
            self.clicked_column = index.column()
    
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

class MyMissIngWindow1(QMainWindow,Ui_MissingIngredient):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class MyMissingIngredientDialog(QDialog,Ui_missing_ingredient_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    #def accept(self):
    #    """overwrite the accept function"""
    #    #print("custom func")
    #   super().accept()







class ContrlDB_new(QMainWindow):

    def __init__(self,Title=None,db_name=None,db_user=None,db_system=None,db_pwd = None,config_file = None):
        super().__init__()
        self.db_name = db_name
        self.db_user = db_user
        self.db_system = db_system
        self.config_file = config_file
        if db_pwd == None:
        
            temp = '/Users/klein/git/qt_exercises/config/pw.txt'
            if os.path.exists(temp):
                with open(temp, 'r') as file:
                    password = file.read().rstrip()
                    self.db_pwd = password
        else:
            self.db_pwd = db_pwd

        self.init_variables()
        self.SetupLogger()
        #self.CreateIngredientsForm()
        self.SetupConfig()
        self.ingredients_suppress_columns = self.CM.ingredients_suppress_columns 
            
        self.recipes_suppress_columns = self.CM.recipes_suppress_columns
        self.swiss_food_suppress_columns = self.CM.swiss_food_suppress_columns

        self.version = '2.0'
        logger.info('******************************************************************************************************** \n\n\n')

        logger.info(' This is version %s' % self.version)
        logger.info('\n\n\n***************************************************************************************************** \n')

        #instantiate the IngredientTable
        #table_name = '/Users/klein/git/qt_exercises/nutrition_databases/swiss_food.csv'
        #if we are using the swiss_food table we need to get the IngredienTable class
        self.swiss_food = False
        if(self.CM.ingred_table == "swiss_food"):
            self.swiss_food = True
            logger.warning("nned work, pass the table")
            self.InTa  = IngredientTable(table_name=self.CM.ingred_table,ingredients = None)

    def SetupConfig(self):

        # get the config filename
        # here we do a filedialog
        if(self.config_file == None or not os.path.isfile(self.config_file)):
            self.config_file , filter = QFileDialog.getOpenFileName(self,
                                self.tr("Open Config file"), "~", self.tr("*.json"))
           
            
        logger.info("config file %s" % self.config_file)


 
        self.CM = CM.MyConfig(self.config_file)
        self.log_level = self.CM.log_level
        self.log_output = self.CM.log_output


    def  init_variables(self):
        """ initialize some variable to None"""

        self.missing_ingredient = None
        self.new_recipe_name = None
    
    def ConnectDataBase(self,temp_db = None,db_name=None,db_user=None,db_pwd =None):
        ''' establish contact to database'''
        if(temp_db != None):
            self.CM.db_address = temp_db
        if(db_name != None):
            self.CM.db_name = db_name
        if(db_user != None):
            self.CM.db_user = db_user
        if(temp_db != None):
            self.CM.db_pwd = db_pwd
        

        #instantiate the connection
        self.mycal_db  = QSqlDatabase.addDatabase(self.db_system)
        self.mycal_db.setHostName(self.CM.db_address)
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
            logger.error('database problem %s' % self.mycal_db.lastError().text())
            logger.error('connection failed, exciting')
            sys.exit(0)

    def SetupLogger(self):


        #logger.remove(0)
        #now we add color to the terminal output
        logger.add(sys.stdout,
                colorize = True,format="<green>{time}</green>    {function}   {line}    {level}     <level>{message}</level>" ,
                level = "DEBUG")



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

        # Now sort them alphabetically
        self.sort_mybox()

        # create independent window
       
        #self.setCentralWidget(self.mybox)


        return
    def sort_mybox(self):
        items = [self.mybox.itemText(i) for i in range(self.mybox.count())]
        items.sort()
        self.mybox.clear()
        self.mybox.addItems(items)

    def ViewTable(self,table,suppress_columns=[],editmode=True,columnwidth=[],Title = None, showTable = True):
        self.table_view = QTableView()
        self.table_view.setSortingEnabled(True)
        #self.table_view.sortByColumn(2,Qt.AscendingOrder)

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
 
        self.setMinimumSize(QSize(600, 300)) 
        
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
        #fill with ingredients if called from missing ingredients
        if(  self.missing_ingredient != None or self.missing_ingredient != ''):
            self.name_label      = QLineEdit(self.missing_ingredient)
            # find position in table where missing ingredient

        else:
            self.name_label        =QLineEdit()
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
        """ this inserts a record into the chosen table
        I will use the query function to do this.
        The record contains the info to be added
        record=[name,energy,fat,carbohydrate,protein]
        
        This is the same for ingredients and receipes"""

        #Create table view
        if(table == "ingredients"):
                
            self.ViewTable(table = table,suppress_columns=self.ingredients_suppress_columns,showTable= False)
        elif(table == "recipes"):
            self.ViewTable(table = table,suppress_columns=self.recipes_suppress_columns)
        elif(table =="swiss_food"):
             self.ViewTable(table = table,suppress_columns=self.swiss_food_suppress_columns)
        else:
            logger.error("no table given")
            sys.exit(0)
           

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
        
        # check if entry exists. if yes modify table otherwise insert
        sql = ' select exists (select true from '+table+' where name='+temp+');'

        response = self.do_sql(sql)
        temp1=response.next()
        print(temp1)
        print(type(temp1))
        if( temp1):
            sql = 'INSERT INTO '+table+' (name,energy,carbohydrate,fat,protein) VALUES ('+temp+','+str(self.record[1])+','+str(self.record[2])+','+str(self.record[3])+','+str(self.record[4])+');'
       

        
            self.do_sql(sql)
            logger.info(' inserted record %s into table  %s' % (self.record[0],table))
 
        else:
            #record = self.pack_record(self.myrecord)
            record = self.pack_record(self.record)
            self.update_record('recipes','ingredients',record,self.record[0])


        return
 
    

    def MyMissingIngredients(self):
        """ form if ingredient is missing"""
        if(not self.swiss_food):
        
            self.MMI1 = MyMissingIngredientDialog()
            self.MMI1.IngredLine.setText(self.missing_ingredient)
            self.MMI1.EditButton.clicked.connect(self.show_ingred_form)
        #self.MMI1.CloseButton.clicked.connect(self.Cancel(self.MMI1))

 
            self.MMI1.move(100,50)
            t = self.MMI1.exec()
        
        #if t == QDialog.Accepted:
        #    self.show_ingred_form()
        #    #self.MMI1.close()


            self.MMI1.show()
        else:
            self.InTa.find_pattern(self.missing_ingredient[0:5])
            self.InTa.get_ingredient()
            #self.InTa.get_ingred_selection()
            # here we put the misssing ingredient back into the form
            self.RecipeModel.recipes[self.stor_row][self.stor_column] = self.InTa.ingredient_name
            self.InTa_name = self.InTa.ingredient_name
            self.InTa_energy = self.InTa.energy
            self.InTa_carbohydrate = self.InTa.carbohydrate
            self.InTa_protein = self.InTa.protein
            self.InTa_fiber = self.InTa.fiber
            self.InTa_sugar = self.InTa.sugar
            self.InTa_salt  =   self.InTa.salt
            self.InTa_fat = self.InTa.fat


        return

    
    
    def show_ingred_form(self):
        # destrory dialog give action back
        try:
            self.MMI1.destroy()
        except:
            logger.debug("nothing to destroy")

 #       window.CreateIngredientsForm1()
        self.CreateIngredientsForm1()



    def MyRecipes_new(self):
        """using the QTdesigner"""
        self.MRD = MyRecipeWindow()
        self.MRD.show()

        # Load the model
        #self.header_labels = header_labels = ["weight", "unit","ingredient"]

        self.RecipeModel = RecipeModel()
        self.MRD.RecipeTableView.setModel(self.RecipeModel)

        # now working self.RecipeModel.setEditStrategy(QSqlTableModel.setEditStrategy.OnFieldChange)

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
        
        #close button 
        self.MRD.CloseButton.clicked.connect(lambda : self.Cancel(self.MRD))

        #add row button
        self.MRD.AddRowButton.clicked.connect(self.add_row)
       
       #new recipe button
        #self.MRD.NewRecipeButton.clicked.connect(self.create_new_recipe) 

        #if line has change
        self.MRD.NewRecipeName.returnPressed.connect(self.create_new_recipe)   
        #self.MRD.NewRecipeName.textChanged.connect(self.create_new_recipe)   

        # here we fill first label
        self.MRD.version_line.setText(self.version)

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

    def create_pandas_frame(self,name=None):
        """This routine creates the pandas frames which then get passed to CalculateCalories class"""
        #collect the information
        logger.info(" name %s and record %s for recipes" % (name,self.panda_ingredients))
        
        # now we need to get the different quantities for each ingredient
        # at the same time we need to check if the ingredient is in the list available
        #if not we have to deal with this
        number_column = 4
        energy,protein,carbohydrate,fat = range(number_column) # for referencing the query values

        logger.debug('recipes ingredient : %s' % self.RecipeModel.recipes)

        #example sql statement:
        # SELECT energy,protein,carbohydrate,fat FROM ingredients where name = 'Butter';
 
 
        energy_v,protein_v,carbohydrate_v,fat_v =([] for i in range(number_column))
        print(self.RecipeModel.recipes)
 
        # loop over all ingredients
        Total_calories_per_gm = 0. # cacluated calories/g
        Total_protein_per_gm = 0.
        Total_fat_per_gm = 0.
        Total_carbs_per_gram = 0.
        temp_weight = 0.
        Total_weight = 0.
        print(self.panda_ingredients)
        #remove empty rows
        temp_buf=[]
        for k in range(len(self.panda_ingredients)):
            if self.panda_ingredients[k][2] != ' ':
                temp_buf.append(self.panda_ingredients[k])
        
        self.panda_ingredients= temp_buf

        for k in range(len(self.panda_ingredients)):
            sql ='SELECT energy,protein,carbohydrate,fat FROM '+self.CM.ingred_table+' where name ILIKE \'' + self.panda_ingredients[k][2] +'\';'
            #sql ='SELECT energy,protein,carbohydrate,fat FROM ingredients where name ILIKE \'' + self.panda_ingredients[k][2] +'\';'
            logger.debug('the query string %s ' % sql)
 
            query = self.do_sql(sql)
        
            logger.debug('value of query.first %s ' % query.first())
            while query.next():

                temp_value = ((query.value(0)))

        #model = QSqlQueryModel()
 
            if( not query.first()):
                logger.info('this ingredient %s is missing '%self.panda_ingredients[k][2])
                self.missing_ingredient = self.panda_ingredients[k][2]
                # here we stor the index of the missing ingredient:
                self.stor_row = self.RecipeModel.clicked_row = k
                self.stor_column = self.RecipeModel.clicked_column = 2

                self.MyMissingIngredients()
            else:
                #fill variables
                energy_v.append(float(query.value(energy)))
                protein_v.append(float(query.value(protein)))
                carbohydrate_v.append(float(query.value(carbohydrate)))
                fat_v.append(float(query.value(fat)))
                temp_weight = float(self.RecipeModel.recipes[k][0])/100.  # all is normalized to per 100 g

                Total_calories_per_gm   = Total_calories_per_gm+temp_weight*energy_v[k]
                Total_protein_per_gm    = Total_protein_per_gm + temp_weight*protein_v[k]
                Total_fat_per_gm        = Total_fat_per_gm + temp_weight*fat_v[k]
                Total_carbs_per_gram    = Total_carbs_per_gram +  temp_weight*carbohydrate_v[k]

                Total_weight = Total_weight+temp_weight*100.

                print(self.RecipeModel.recipes[k][0],'     ', Total_calories_per_gm)
                logger.debug('ingredient : %s' % self.panda_ingredients[k][2])
                logger.debug('energy : %f' % energy_v[k])
                logger.debug('protein : %f' % protein_v[k])
                logger.debug('carbohydrate : %f' % carbohydrate_v[k])
                logger.debug('fat : %f' % fat_v[k])
        if(Total_weight == 0.):
            return
        temp_cal    = Total_calories_per_gm/Total_weight
        temp_fat    = Total_fat_per_gm/Total_weight
        temp_prot   = Total_protein_per_gm/Total_weight
        temp_carb   = Total_carbs_per_gram/Total_weight
        logger.debug('total calories per gram : %f' % temp_cal)
        logger.debug('total carbs per gram : %f' % temp_carb)
        logger.debug('total protein per gram : %f' % temp_prot)
        logger.debug('total fat per gram : %f' % temp_fat)

        # convert to string
        string_cal = f"{temp_cal:.2f}"
        string_fat = f"{temp_fat:.2f}"
        string_prot = f"{temp_prot:.2f}"
        string_carb = f"{temp_carb:.2f}"


        #Update the values on the form
        self.MRD.cal_line.setText(string_cal)
        self.MRD.fat_line.setText(string_fat)
        self.MRD.prot_line.setText(string_prot)
        self.MRD.carb_line.setText(string_carb)

        # put values onto form


       
        self.new_recipe_record=(self.new_recipe_name,string_cal,string_prot,string_carb,string_fat,self.pack_record(self.panda_ingredients))
        return

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
        self.myrecord = record = self.RecipeModel.StoreValue()
        logger.info("ingredients %s "% record)
        #create original string
        record = self.pack_record(record)
       # Now update the record

        #check if this is a new recipe or an updated one
        if self.new_recipe_name != None:
            self.rec_name = rec_name =self.new_recipe_name
            self.create_pandas_frame(name=rec_name)
 
            self.insert_record()
        else: 
            self.rec_name = rec_name = self.selected_recipe
            self.create_pandas_frame(name=rec_name)

            self.update_record('recipes','ingredients',record,rec_name)

        #self.new_recipe_name = None  # reset recipe name
        #here we call create_pandas_frame tframe for CalculateCalories start producing the 
 
        #remove window
        #self.MRD.close()
 

        return
    def insert_record(self):
        """inserts new recipe into table
        columname is a list of all the columns
        record is a corresponding list"""
        # create sql statement

        record =self.new_recipe_record

        # since ID is a non-zero number we need to find the highest number and then add one for the next reipce
        sql ='SELECT id from recipes ;'
        ID_number=[]
        myquery = self.do_sql(sql)
        while myquery.next():

            ID_number.append(int(myquery.value(0)))
        #find the highest numer in the list
        imax = max(ID_number)
        new_recipe_id = str(imax+1)


        b= new_recipe_id+',\''+record[0]+'\','+record[1]+','+record[2]+','+record[3]+','+record[4]+',\''+record[5]+'\''

        # check if entry exists. if yes modify table otherwise insert
        sql = ' select exists (select true from recipes where name= \''+record[0]+'\');'

        response = self.do_sql(sql)
        #print(response.next())
        if( response.next() != True):
            sql = 'INSERT INTO recipes (id,name,energy,protein,carbohydrate,fat,ingredients) VALUES ('+b+');'
            logger.debug("insert recipe %s" % sql)
            #finally exceute the sql
            self.do_sql(sql)
        else:
            #record = self.pack_record(self.myrecord)
            record = self.pack_record(self.myrecord)

            self.update_record('recipes','ingredients',record,self.rec_name)

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
        #self.panda_ingredients are the correct list for creating the panda frame
        self.panda_ingredients = a =record




        #b=a[0]
        print(len(a))
        if(self.is_nested_list(a)): # determine if nested list
            for k in range(len(a)):
                print(a[k][0])
                if(str(a[k][0])==''): break
                b.append(str(a[k][0])+' '+str(a[k][1])+' '+str(a[k][2])+' ')
        else:
             for k in range(len(a)):

                if(str(a[k])==''): break
                b.append(str(a[k])+' ')


        for k in range(0,len(b)):
            c = c+ b[k]
   
        # remove last space
        d = c[0:len(c)-1]
        return(d)

    def is_nested_list(self,data):
        """helps with pack record, deals with ingredient record not a nested list"""
        return any(isinstance(i,list)for i in data)
    

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
        model = QSqlQueryModel()
        logger.info("query in do_sql %s" % sql)
        model.setQuery(query)
        if query.lastError().isValid():
            logger.error(f"Query error: {query.lastError().text()}")
            # if this is a inserty error try replace.
 
        

        return query


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
            temp_newvalue = temp_value.replace('  ',' ') #deal with emty ingredients in recipes
            temp_new = temp_newvalue.split(' ')
            for k in range(0,len(temp_new),3):
                if(temp_new[k] != '0'): # deal with the empty entries
                    try:
                        temp_new1.append([temp_new[k],temp_new[k+1],temp_new[k+2]])
                    except:
                        logger.error('error in ingredient list at position %i ' %k)
                        break
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
            print(self.recipe_ingredients[k])
            
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
 

        # now sort them alphabetically
        items = [recipe_list[i] for i in range(len(recipe_list))]
        items.sort(key=str.lower) #this way no diff between upper and lower case
 
        return (items)





    def ModifyRecipe(self):
        pass

  
    def SizeWindow(self,window,myposit,mysize):
        """resizes the specified window ,where the parameters are two integer lists"""
        window.setGeometry(myposit[0],myposit[1],mysize[0],mysize[1])
        return
 
    def calculate_portion_calory(self,myrecipe=None,myportion=0.):
        """ this calucaltes the calories of a portion for  given recipe, 
        where the portion size is given in grams."""

        # sql statement: SELECT enegry FROM recipes WHERE NAME = 'raspberry_tart';
        sql = 'SELECT energy FROM recipes WHERE NAME = \'' +myrecipe +'\';'
        query = self.do_sql(sql)
        while query.next():

            cal_per_gram = ((query.value(0)))
        portion_calory = float(cal_per_gram)*myportion
        logger.info("your total calories are %.1f " % portion_calory)
        return portion_calory





##########################################################################
    # section for signals and slots

    
    def Cancel(self,window):
        """ closes window without anything"""
        window.close()
        
 
 

    def SaveIngredients(self):
        """saving the ingredients"""
        if( not self.swiss_food):
            Ing_name    = self.name_label.text()
            Ing_calory  = float(self.calory_label.text())
            Ing_carb    = float(self.carb_label.text())       
            Ing_fat     = float(self.fat_label.text())
            Ing_prot    = float(self.prot_label.text())
        else:
            Ing_name    = self.InTa_name
            Ing_calory  = self.InTa_energy
            Ing_carb    = self.InTa_carbohydrate     
            Ing_fat     = self.InTa_fat
            Ing_prot    = self.InTa_protein
           

        #  this is the record we got from the form input

        #Check all fields are filled out
        if(Ing_calory !="" and Ing_carb !="" and Ing_fat!=""  and Ing_prot !=""):
            self.Inform.destroy() # destrorys the window.
            #self.Inform.close() # 

        #now we need to add the values to the ingredients table
        # first load table

        
        self.ViewTable(self.CM.ingred_table,suppress_columns=self.ingredients_suppress_columns)
        self.model = QSqlQueryModel()
        self.table_view.setModel(self.model)
        #next we check we don't have an entry yet

        
        #sql = "SELECT name from ingredients WHERE ingredients.name LIKE 'Almond%' ; "
        sql = 'SELECT name from ingredients WHERE '+self.CM.ingred_table+'.name LIKE '"+Ing_name+"' ; '
        query = QSqlQuery(sql,db=self.mycal_db)
        
        self.model.setQuery(query)
        while query.next():
            logger.error(' entry name already exists, try again %s' % query.value(0))
            self.CreateIngredientsForm1()
            #myvalue = query.value(0)
        # Now we need to add this ingredient to the table

        self.record = [Ing_name,Ing_calory,Ing_carb,Ing_fat,Ing_prot]
        self.InsertRecord(table = self.CM.ingred_table)
        return
    

if __name__ == '__main__':    
    app = QApplication(sys.argv) 

    Title=None
    db_name='recipe_ak'
    db_user='klein'
    db_system='QPSQL'
    config_file = '/Users/klein/git/qt_exercises/config/config_mycal.json'

    with open('/Users/klein/git/qt_exercises/config/pw.txt', 'r') as file:
                    db_pwd = file.read().rstrip()
                    



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

    window = ContrlDB_new(Title = "ControlDB",
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
    #window.calculate_portion_calory(myrecipe = 'raspberry_tart',myportion=200.)
    #window.ViewTable('recipes',suppress_columns=suppress_columns,columnwidth=columnwidth)

    window.MyRecipes_new()
#window.CreateIngredientsForm1()

# now run the app
    app.exec()