import sys
import PyQt4
from PyQt4 import QtCore, QtGui, uic

import json as j
import unicodecsv
import time
from collections import OrderedDict



qtCreatorFile = "converter.ui" # Enter file here.


Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('AINA CONVERT')
        self.progress.setValue(0)
        self.directory=""
        self.convert.clicked.connect(self.csvConversion)
        self.setWindowIcon(QtGui.QIcon('C:/Users/DJAN DENNIS MINTAH/Desktop/work/ui/ico.png'))

        self.clear.clicked.connect(self.clearField)
        self.filebrowser.clicked.connect(self.getFile)
        self.content=""
        self.fileconvert.clicked.connect(self.fileConvert)
        self.location.clicked.connect(self.getDirectory)

    def flatten(self,structure, key="", path="", flattened=None): 
        if flattened is None:
            flattened = OrderedDict()    
        if type(structure) not in(OrderedDict, list):
            flattened[((path + "/") if path else "") + key] = structure    
        elif isinstance(structure, list):
            for i, item in enumerate(structure):
                self.flatten(item, "", path+ key, flattened)    
        else:
            for new_key, value in structure.items():
                self.flatten(value, new_key, path + key, flattened)    
        return flattened  

    def csvConversion(self):
        errortext=""


        self.progress.setValue(0)
        json_string=self.json.toPlainText()
    
        try:
            data=j.loads(json_string, object_pairs_hook=OrderedDict)
        except:
            errortext=errortext+"Error Parsing JSON....Please Verify JSON"
            data=""
        self.progress.setValue(5)
        filename=self.file.toPlainText()
        if str(filename)=="":
            file=str(self.directory)+"/no_name.csv"
        else:
            file=str(self.directory)+"/"+str(filename)+".csv"

        if self.append.isChecked()==True:
            writemode="ab"
        else:
            writemode="wb"
        
        

        
        try:
            outfile = open(file, writemode)
            self.progress.setValue(10)
        except:
            errortext=errortext+"\nCould not Open CSV file............................."

        if errortext=="":
            errortext=errortext+"Loaded JSON Successfully.................\nOpened CSV File Successfully............................ "
        self.error.setText(errortext)
        
        writer = unicodecsv.writer(outfile, delimiter=",")
        fields = []
        for result in data:
            flattened = self.flatten(result)
            for k, v in flattened.items():
                if k not in fields:
                    fields.append(k)
        writer.writerow(fields)

        self.progress.setValue(30)
        
        for result in data:
            flattened = self.flatten(result)
            row = []
            for field in fields:
                if field in flattened.keys():
                    row.append(flattened[field])
                else:
                    row.append("")
            writer.writerow(row)
        self.progress.setValue(100)
        self.reset()
        
        

    def clearField(self):
        self.json.clear()

    def reset(self):
        time.sleep(5)
        self.progress.setValue(0)
        self.error.clear()

    def getFile(self):

        filepath=QtGui.QFileDialog.getOpenFileName(self,'Single File','~/Desktop/','*.json')
        
        try:
            self.content = j.load(open(filepath), object_pairs_hook=OrderedDict)
            


        except:
            raise

    def getDirectory(self):

        self.directory=QtGui.QFileDialog.getExistingDirectory(self,"Open Directory",'~/Destop/')
    

    def fileConvert(self):
        errortext=""
        
        self.progress.setValue(0)

        data=[]
    
        try:
            data=self.content
            
        except:
            errortext=errortext+"Error Parsing JSON....Please Verify JSON"
            
        self.progress.setValue(5)
        filename=self.file.toPlainText()
        if str(filename)=="":
            file=str(self.directory)+"/no_name.csv"
        else:
            file=str(self.directory)+"/"+str(filename)+".csv"

        if self.append.isChecked()==True:
            writemode="ab"
        else:
            writemode="wb"
        
        

        
        try:
            outfile = open(file, writemode)
            self.progress.setValue(10)
        except:
            errortext=errortext+"\nCould not Open CSV file............................."

        if errortext=="":
            errortext=errortext+"Loaded JSON Successfully.................\nOpened CSV File Successfully............................ "
        self.error.setText(errortext)
        
        writer = unicodecsv.writer(outfile, delimiter=",")
        fields = []
        for result in data:
            flattened = self.flatten(result)
            for k, v in flattened.items():
                if k not in fields:
                    fields.append(k)
        writer.writerow(fields)

        self.progress.setValue(30)
        
        for result in data:
            flattened = self.flatten(result)
            row = []
            for field in fields:
                if field in flattened.keys():
                    row.append(flattened[field])
                else:
                    row.append("")
            writer.writerow(row)
        self.progress.setValue(100)
        self.reset()
        


        

        
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

