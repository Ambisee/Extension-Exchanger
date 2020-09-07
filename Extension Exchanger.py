# --- Modules --- #
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
import sys
import os

# --- Classes --- #
# Combo Box
class Combobox(QWidget):
    def __init__(self, master, text):
        super().__init__(master)
        b_size = QtCore.QRect(0, 0, 150, 100)
        self.setGeometry(b_size)

        self.label = QLabel(text, self)
        self.label.setGeometry(0, 0, 150, 20)
        self.label.setStyleSheet('font: Courier; font-size: 10pt')
        
        self.cbox = QComboBox(self)
        self.cbox.setGeometry(0, 30, 150, 30)
        self.cbox.setStyleSheet('font: Courier; font-size: 10pt')
        self.cbox.addItems(['None', '.txt', '.html','.jpg', '.png', '.py', 'jpeg'])
        self.cbox.setEditable(True)

        pal = self.cbox.palette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(255,255,255))
        self.cbox.setPalette(pal)
    
    def getEx(self):
        extension = self.cbox.currentText()
        return extension

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        screen = QApplication.desktop().screenGeometry()
        self.w_width = 500
        self.w_height = 500
        
        self.setGeometry(screen.width()//2 - self.w_width//2, screen.height()//2 - self.w_height//2, self.w_width, self.w_height)
        self.setFixedSize(self.w_width, self.w_height)
        self.setWindowTitle('Extension Exchanger')

        self.initUi()
        self.moveUi()

    def initUi(self):
        b_size = QtCore.QRect(0, 0, 250, 50)
        font1 = QtGui.QFont('Baskerville Old Face', 20)
        font2 = QtGui.QFont('comicsans', 13)
        font3 = QtGui.QFont('arrus bt', 12)

        self.title_l = QLabel('Extension Exchanger', self)
        self.title_l.setFont(font1)
        self.title_l.setStyleSheet('border-style: outset; border-color: purple; background-color: green; border-width: 5px; border-radius: 5px; color: white')
        self.title_l.adjustSize()

        self.description1 = QLabel("---Function---", self)
        self.description1.setFont(font2)
        self.description1.setStyleSheet("color: red")
        self.description1.adjustSize()
        self.description1.setAlignment(QtCore.Qt.AlignCenter)

        self.description2 = QLabel(self)
        self.description2.setFont(font2)
        self.description2.setText("Changes all instances of a file\nthat has the designated extension\nwithin a directory.")
        self.description2.adjustSize()
        self.description2.setAlignment(QtCore.Qt.AlignCenter)
        
        self.fromc = Combobox(self, 'From :')
        self.toc = Combobox(self, "To :")

        self.proceed_b = QPushButton(self)
        self.proceed_b.setFont(font3)
        self.proceed_b.setText("Change Extension")
        self.proceed_b.adjustSize()
        self.proceed_b.setGeometry(b_size)
        self.proceed_b.setShortcut("Return")
        self.proceed_b.clicked.connect(self.chext)

        self.quit_b = QPushButton(self)
        self.quit_b.setFont(font3)
        self.quit_b.setText("Quit")
        self.quit_b.adjustSize()
        self.quit_b.setGeometry(b_size)
        self.quit_b.clicked.connect(self.close)

    def moveUi(self):
        self.title_l.move(self.w_width//2 - self.title_l.width()//2, 5)
        self.description1.move(self.w_width//2 - self.description1.width()//2, self.title_l.y() + self.title_l.height() + 10)
        self.description2.move(self.w_width//2 - self.description2.width()//2, self.description1.y() + self.description1.height() + 20)
        self.fromc.move(self.w_width//2 - self.fromc.width()//2 - self.w_width//4, 250)
        self.toc.move(self.w_width//2 - self.toc.width()//2 + self.w_width//4, 250)
        self.quit_b.move(self.w_width//2 - self.quit_b.width()//2, self.w_height - self.quit_b.height() - 10)
        self.proceed_b.move(self.w_width//2 - self.proceed_b.width()//2, self.quit_b.y() - self.proceed_b.height() - 10)
        
    def chext(self):
        fromex = self.fromc.getEx()
        toex = self.toc.getEx()
        dir_name = QFileDialog.getExistingDirectory(self, 'Open Directory',os.path.join(os.path.expanduser("~"), "Desktop"), QFileDialog.ShowDirsOnly)
        
        if dir_name == '' or 'None' in [fromex, toex]:
            return
        
        yes_no = QMessageBox.question(self,"Confirmation", f'Do you wish to change all files with the extensions :\n"{fromex}" into "{toex}" ?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if yes_no == QMessageBox.Yes:
            
            for root, dirs, files in os.walk(dir_name, topdown=True):
                for item in files:
                    if item.endswith(fromex):
                        x = os.path.splitext(item)
                        new = x[0] + toex
                        os.chdir(root)
                        os.rename(item, new)
        else:
            return
        
        msg = QMessageBox()
        msg.setWindowTitle("Process Completed")
        msg.setIcon(QMessageBox.Information)
        msg.setText(f'All files with the extension "{fromex}" has been changed to the extension "{toex}"')
        msg.exec_()

    def closeEvent(self, event):
        self.close()

# --- Initialization --- #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    app.quit()
