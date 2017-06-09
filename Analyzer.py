# Tool created by Aditya Varshney and Shrey Samdani


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, os
from all import run
# from PyQt5.QtGui import QIcon


class Button(QPushButton):

    def __init__(self, title, parent):
        self.p = parent  
        super().__init__(title, parent)
    

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)


    def mousePressEvent(self, e):
      
        QPushButton.mousePressEvent(self, e)
        
        if e.button() == Qt.LeftButton:
            self.p.openFileNameDialog()


class Example(QWidget):
  
    def __init__(self):
        super().__init__()

        self.initUI()
        
        
    def initUI(self):

        self.setAcceptDrops(True)

        button = Button("Open File", self)
        button.move(90,60)

        label = QLabel(self)
        label.setText("Drag and drop a file here or open file")
        label.move(30,40)

        self.setWindowTitle('Seed/Key Analyzer')
        self.setGeometry(300, 300, 280, 150)
        

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
        

    def dropEvent(self, event):
            for url in event.mimeData().urls():
                path = url.toLocalFile()
            if os.path.isfile(path):
                print(path)
                run(path)
                self.close
                sys.exit()

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            run(fileName)
            self.close
            sys.exit()
            
  

if __name__ == '__main__':
  
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_() 


