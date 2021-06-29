import sys
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QColor


class CustomTable(QTableWidget):
    '''A table with keyPressEvent support'''
    def __init__(self, parent=None, rows=1, cols=3):
        super(CustomTable,self).__init__(parent)
        
        self.setGeometry(QRect(10, 10, 301, 371))
        self.setColumnCount(cols)
        self.setColumnWidth(2, 75)
        self.changeMode() #  launch to get onShots value
        self.addRows([-1]*rows) # minus one because line inserted below given number
        self.setHorizontalHeaderLabels(["Coordinate","Number of shots",'ΔR effective'])
        self.setStatusTip("Click on the number of the row — select line (hold «Ctrl» " +
                          "— multiple choice); «Enter» — add line(s) "
                           + "below selected; «Delete» — remove line(s).")
        
    def keyPressEvent(self, event):
        try:
            key = event.key()
            mod = event.modifiers()
            if key == Qt.Key_Delete :
                self.deleteRows(self.selectedLines())
                
            elif key == Qt.Key_Z and (mod == Qt.ControlModifier):
                print("Ctrl+Z pressed")
                
            elif key == Qt.Key_Return or key==Qt.Key_Enter:
                self.addRows(self.selectedLines())
            else:
                super(CustomTable, self).keyPressEvent(event)
        except:
            print("KeyPress failed: " + str(sys.exc_info()[1]))
            
    def selectedLines(self):
        '''Return a list of selected lines'''
        li = self.selectedIndexes()
        rows = [] # all row indices
        s = [] # selected line indices
        for l in li:
            row = l.row() # take row from all indices
            rows.append(row)
            if rows.count(row) == 2:
                s.append(row)
        return sorted(s)
        
    def addRows(self, lines):
        '''Add one or multiple rows to selected lines'''
        try:
            for line in lines:
                self.insertRow(line+1)
    
                x_item = QTableWidgetItem("0")
                n_item = QTableWidgetItem("0")
                r_item = QTableWidgetItem("0")
                if not self.onShots:
                    n_item.setBackground(QColor(230,230,230))
                    n_item.setFlags(Qt.ItemIsEnabled)
                else:
                    r_item.setBackground(QColor(230,230,230))
                    r_item.setFlags(Qt.ItemIsEnabled)
                self.setItem(line+1, 0, x_item)
                self.setItem(line+1, 1, n_item)
                self.setItem(line+1, 2, r_item)
        except:
            print(sys.exc_info()[1])

    def deleteRows(self,lines):
         for r in lines[::-1]: # delete rows from bottom to top
             if self.rowCount() != 1:    
                 self.removeRow(r)
            
    def changeMode(self, onShots=False):
        try:
            self.onShots = onShots
            if onShots:
                block_row = 2
                unblock_row = 1
            else:
                block_row = 1
                unblock_row = 2
            rows = self.rowCount()
            for i in range(rows):
                block_item = self.item(i, block_row)
                unblock_item = self.item(i, unblock_row)
                # execute the line below to every item you need locked
                block_item.setFlags(Qt.ItemIsEnabled)
                unblock_item.setFlags(Qt.ItemIsSelectable |Qt.ItemIsEditable | Qt.ItemIsEnabled)
                block_item.setBackground(QColor(230,230,230))
                unblock_item.setBackground(QColor('white'))
                self.setItem(i, block_row, block_item)
                self.setItem(i, unblock_row, unblock_item)
        except:
            print("Table change failed: " + str(sys.exc_info()[1]))