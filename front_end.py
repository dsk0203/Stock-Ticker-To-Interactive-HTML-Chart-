# Main imports
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QToolTip, QPushButton, QMessageBox, QDesktopWidget, QDialog, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QLineEdit, QCheckBox
from PySide2.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PySide2.QtCore import Qt
import sys
import pandas as pd
import datetime
from datetime import date
from pandas_datareader import data
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components

#create a class, inherits from QWidget ### 
class Window(QWidget):
    def __init__(self):
        
        #initialize base class
        super().__init__()

        # set the window title
        self.setWindowTitle("Build Interactive Charts")

        #use this to create a grid layout
        self.createGrid()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

        # set the icon for taskbar and the top left
        self.setIcon() 

        # center the widget
        self.center()

    # set the icon from a pictures
    def setIcon(self):
        appIcon = QIcon("stock.png")
        self.setWindowIcon(appIcon)

    # center the gui app in the middle of the screen
    def center(self):
        
        # create frame of screen
        qRect = self.frameGeometry()
        # find the center point
        centerPoint = QDesktopWidget().availableGeometry().center()
        # moveCenter to the center point
        qRect.moveCenter(centerPoint)
        # from the top left??
        self.move(qRect.topLeft())

    # create the layout of the gui on the screen
    def createGrid(self):
        
        # top groupbox quote
        self.groupBox = QGroupBox("Search a Stock ------> Downloadable Interactive Chart")
        # font
        self.groupBox.setFont(QFont("Monospace",13))
        # initialize
        gridLayout = QGridLayout()

        # send call to func from search button
        new_gui = QPushButton("Graph CSV", self)
        new_gui.setIcon(QIcon("csv.png"))
        new_gui.setMinimumHeight(10)
        new_gui.clicked.connect(self.new_GUI_link)
        gridLayout.addWidget(new_gui, 0,1)

        #input own data
        self.input_owndata_label = QLabel(self)
        self.input_owndata_label.setText("Input own data: ")
        gridLayout.addWidget(self.input_owndata_label,0,0)

        #input exit destination file path
        self.input_filepath_line = QLineEdit(self)
        self.input_filepath_label = QLabel(self)
        self.input_filepath_label.setText("Enter Destination File Path: ")
        gridLayout.addWidget(self.input_filepath_line,2,1)
        gridLayout.addWidget(self.input_filepath_label,2,0)

        #input text for ticker
        self.input_ticker = QLineEdit(self)
        self.input_ticker_label = QLabel(self)
        self.input_ticker_label.setText("Input Ticker to search: ")
        gridLayout.addWidget(self.input_ticker,1,1)
        gridLayout.addWidget(self.input_ticker_label,1,0)

        # search button
        search_Button = QPushButton("Search", self)
        search_Button.setIcon(QIcon("search.png"))
        search_Button.setMinimumHeight(40)
        search_Button.clicked.connect(self.get_Ticker)
        gridLayout.addWidget(search_Button, 4,1)

        #quit button
        quit_Button = QPushButton("Quit", self)
        quit_Button.setIcon(QIcon("exit.png"))
        quit_Button.setMinimumHeight(40)
        quit_Button.clicked.connect(self.quitApp)
        gridLayout.addWidget(quit_Button, 4,0)

        # set the layout once called 
        self.groupBox.setLayout(gridLayout)

    #quit app when called
    def quitApp(self):

        #Yes or No check box for quitting
        userInfo = QMessageBox.question(self, "Confirmation", "Leave the application?",
            QMessageBox.Yes | QMessageBox.No)

        # if yes quit
        if userInfo == QMessageBox.Yes:
            myApp.quit()

    # get ticker information, and graph
    def get_Ticker(self):

        # create start and end times (5 years)
        today = date.today()
        start = datetime.datetime(today.year-5, today.month, today.day)
        end = datetime.datetime(today.year, today.month, today.day)

        # create local variable from class obj
        ticker_name = self.input_ticker.text()

        # DataReader to pull from yahoo source
        try:
            df = data.DataReader(name=ticker_name,data_source="yahoo",start=start,end=end)
        except:
            return print('Ticker not available')

        # create the figure (sizing_mode='scale_width' makes it take up the whole page)
        p = figure(width=500,height=250,x_axis_type="datetime")

        # table formatting, use ticker name as title
        p.title.text = ticker_name
        p.title.align = "right"
        p.title.text_color = "navy"
        p.title.text_font_size = "25px"

        # create line chart, utilizing the close col from the API
        p.line(df.index, df["Close"], color="Navy", line_width=2, alpha=0.5)

        # name file, will do basedir if not specified
        if not self.input_filepath_line.text():
            print("This will push a file to the base directory")
        else:
            #push file, utilize the ticker name and the destination filepath
            file_attempt = str(self.input_filepath_line.text() + "/" + ticker_name + ".html")

        try:
            output_file(file_attempt)
            print('File saved to: ' + file_attempt)
        except:
            print('Please fix the directory')

        # show the figure
        show(p)


    def new_GUI_link(self):

        # initialize second window
        second_window = Window_csv()

        # recolor
        p = QPalette()
        p.setColor(QPalette.Background, QColor("white"))
        second_window.setPalette(p)
        
        #show and exec (on click)
        second_window.show()
        second_window.exec_()
        



# second widget QDialog inherit since only 1 widget per run
class Window_csv(QDialog):
    def __init__(self):
        #initialize from base class of Qdialog also with own __init__
        super().__init__()


        #window title
        self.setWindowTitle("Create from CSV")

        # intialized grid layout settings
        self.createGrid()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

        #window title
        self.setWindowTitle("Create from CSV")

        #icon
        self.setIcon()

        # center, call last
        self.center()


    def createGrid(self):
        
        # top groupbox quote
        self.groupBox = QGroupBox("Make sure file is .csv")
        # font
        self.groupBox.setFont(QFont("Monospace",13))
        # initialize
        gridLayout = QGridLayout()

        # file path outward
        self.input_filepath_line = QLineEdit(self)
        self.input_filepath_label = QLabel(self)
        self.input_filepath_label.setText("Enter Destination Filepath: ")
        gridLayout.addWidget(self.input_filepath_line,3,1)
        gridLayout.addWidget(self.input_filepath_label,3,0)

        #check box
        self.check = QCheckBox("Yes", self)
        self.input_checkbox_label = QLabel(self)
        self.input_checkbox_label.setText("Headers on CSV?")
        self.check.stateChanged.connect(self.checkbox)
        self.check.toggle()
        gridLayout.addWidget(self.check,2,1)
        gridLayout.addWidget(self.input_checkbox_label,2,0)

        #file path inward
        self.input_ticker = QLineEdit(self)
        self.input_ticker_label = QLabel(self)
        self.input_ticker_label.setText("Enter Incoming Filepath: ")
        gridLayout.addWidget(self.input_ticker,1,1)
        gridLayout.addWidget(self.input_ticker_label,1,0)

        #search button, calls graph function from inputs
        search_Button = QPushButton("Graph", self)
        search_Button.setIcon(QIcon("search.png"))
        search_Button.setMinimumHeight(40)
        search_Button.clicked.connect(self.graph_csv)
        gridLayout.addWidget(search_Button, 4,1)

        #quit button calls quit function
        quit_Button = QPushButton("Quit", self)
        quit_Button.setIcon(QIcon("exit.png"))
        quit_Button.setMinimumHeight(40)
        quit_Button.clicked.connect(self.quitApp)
        gridLayout.addWidget(quit_Button, 4,0)

        # final for display and setting
        self.groupBox.setLayout(gridLayout)


    def checkbox(self,state):
        
        # check if checkbox is clicked
        if state == Qt.Checked:

            # create object to utilize in graphing functino (we need to know if it has headers)
            self.is_checked = True
        
        else:

            # create object to utilize in graphing functino (we need to know if it has headers)
            self.is_checked = False

    def graph_csv(self):
        
        # local copy of checked from previous object
        checked = self.is_checked

        # if checked is true
        if checked:
            
            # if this document has headers, try to let pandas infer them, and create the x,y graph then plot it 
            try:
                
                # read in the text from the checkbox
                csv = self.input_ticker.text()
                
                # utilize pandas to read in the dataframe
                csv_pd = pd.read_csv(csv, index_col=0)
                
                # check column length
                check_list = csv_pd.columns
                       
                # currently application is only useful for plotting two columns, if .column returns more than we won't be able to use it
                if len(check_list) > 2:
                    return "Please pass a file that isn't greater than two columns"

            except:
                # on error return that the file wasn't recongized and was unreadable
                return print("Incoming file path not recognized (possibly not a csv file?)")
        
        else:
            # this document doesn't have headers, create some false headers (so data isn't lost in intial row call these col1 and col2)
            try:
                
                # read in the text from the checkbox
                csv = self.input_ticker.text()

                # read in the dataframe, set the index to the first column.
                csv_pd = pd.read_csv(csv, names=["col1","col2"], index_col=0)
                
                # get a list of the column for check
                check_list = csv_pd.columns
                
                # currently application is only useful for plotting two rows, if .column returns more than we won't be able to use it
                if len(check_list) > 2:
                    return "Please pass a file that isn't greater than two columns"
            
            except:
                # on error return that the file wasn't recongized and was unreadable
                return print("Incoming file path not recognized (possibly not a csv file?) or header error")


        # initialize a figure
        p = figure(width=500,height=250)

        #table formatting
        p.title.text = "My Graph"
        p.title.align = "right"
        p.title.text_color = "navy"
        p.title.text_font_size = "25px"


        #plot the values, use the index and the first col
        p.line(csv_pd.index, csv_pd.iloc[:,0], color="Navy", line_width=2, alpha=0.5)

        # name file, will do basedir if not specified
        if not self.input_filepath_line.text():
            print("This will push a file to the base directory")
        else:
            #destination file path with My_Graph.html name
            file_attempt = str(self.input_filepath_line.text() + "/" + "My_Graph.html")

        # try to push the file to the name described, if not go base dir instead
        try:
            output_file(file_attempt)
            print('File saved to: ' + file_attempt)
        except:
            print('Please fix or add a the directory, pushed to local dir')

        # show the figure
        show(p)

    # set the icon of the gui app
    def setIcon(self):
        appIcon = QIcon("csv.png")
        self.setWindowIcon(appIcon)

    # center the applciation in the middle of the screen
    def center(self):
        # create frame of screen
        qRect = self.frameGeometry()
        # find the center point
        centerPoint = QDesktopWidget().availableGeometry().center()
        # moveCenter to the center point
        qRect.moveCenter(centerPoint)
        # from the top left??
        self.move(qRect.topLeft())

    # quit when called
    def quitApp(self):
        userInfo = QMessageBox.question(self, "Confirmation", "Leave the application?",
            QMessageBox.Yes | QMessageBox.No)

        if userInfo == QMessageBox.Yes:
            myApp.quit()
        else:
            pass


# basic run
if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    window = Window()
    
    p = QPalette()
    p.setColor(QPalette.Background, QColor("white"))
    window.setPalette(p)
    
    window.show()
    myApp.exec_()
    sys.exit(0)
    # icons were downloaded from Freepik :)
    # Dylan Kaplan
