DEBUG = False
import os, sys, time, threading, importlib
from pathlib import Path
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
from ui import IM as ui
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from common.Common import Worker, CommonClass

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainApp(CommonClass, ui.Ui_MainWindow):

    def __init__(self):
         ''''Class initialization'''
        
         # Define constants
         self.sliderZero  = 1548.195
         self.stepsInMm = 2.5/1000   
         self.filedir = "saves"
         self.ERVdir = "."
         self.IMSdir = "."
        
         # Run initialization
         CommonClass.__init__(self)
         ui.Ui_MainWindow.__init__(self)
         self.setupUi(self) 
         self.isNotStarted = threading.Event()
         self.isNotStarted.set()        

         self.setupButtons()
         self.setupBox()
         self.setupTable()


         # Start to detect equipment
         self.threadpool.start(self.worker1)
         self.threadpool.start(self.worker2)

         #define plot for function generator        
         self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
         toolbar = NavigationToolbar(self.canvas, self)

         layout = QtWidgets.QGridLayout(self.tab_2)
         layout.addWidget(toolbar)
         layout.addWidget(self.canvas)
         
         #definie  ERV plot for correction
         self.ERVcanvas = MplCanvas(self, dpi=70)        
         ERVlayout = QtWidgets.QGridLayout(self.ERVView)
         ERVlayout.addWidget(self.ERVcanvas)
         
         #define  correction plot for correction
         self.corCanvas = MplCanvas(self, dpi=70)        
         corLayout = QtWidgets.QGridLayout(self.correctionView)
         corLayout.addWidget(self.corCanvas)

    def update_plot(self):
        '''
        Draw/redraw the function plot in the "N(x)" tab from table located in
        the "Main functions" tab.

        Returns
        -------
        None.

        '''
        if self.tabWidget.currentIndex() == 1 and self.tableWidget.rowCount() > 1:
            xdata = []
            ydata = []
            num_lines = self.tableWidget.rowCount()
            for i in range(0, num_lines):
                x_item = self.tableWidget.item(i, 0)
                n_item = self.tableWidget.item(i, 1)
                x = float(x_item.text())
                n = int(n_item.text())

                xdata.append(x)
                ydata.append(n)

            self.canvas.axes.cla()  # Clear the canvas.
            self.canvas.axes.plot(xdata, ydata, 'r')
            # Trigger the canvas to update and redraw.
            self.canvas.draw()


    def interfaceBlock(self, flag):
        '''Block the interface while the shooting proccess running'''
        blk = not flag
        self.ConnectionBox.setEnabled(blk)
        self.StagesConrtolBox.setEnabled(blk)
        self.ParametersBox.setEnabled(blk)
        self.annealBox.setEnabled(blk)

    def startBlock(self, flag):
        self.interfaceBlock(flag)
        blk = not flag
        self.ParametersBox.setEnabled(True)
        self.fileButton.setEnabled(blk)
        self.powerSpinBox.setEnabled(blk)
        self.openSpinBox.setEnabled(blk)
        self.periodSpinBox.setEnabled(blk)
        self.saveButton.setEnabled(blk)
        if (flag == False):
            self.startButton.setEnabled(True)

    def setupButtons(self):
        '''Connect all buttons to their functions'''
        self.manualConnectionBox.stateChanged.connect(self.manualConnectionClicked)
        self.AutoDetectButton.clicked.connect(self.autoDetectClicked)
        self.manualConnectButton.clicked.connect(self.manualConnectClicked)
        self.StagesToZerosButton.clicked.connect(lambda: self.runThread(self.stagesToZerosClicked))
        self.StagesToHomeButton.clicked.connect(lambda: self.runThread(self.stagesToHomeClicked))
        self.MoveStagesButton.clicked.connect(lambda: self.runThread(self.moveStagesClicked))
        self.startButton.clicked.connect(self.startClicked)
        self.fileButton.clicked.connect(self.fileClicked)
        self.startAnnealButton.clicked.connect(lambda: self.runThread(self.startAnneal))
        self.toggleShutterButton.clicked.connect(self.toggleShutter)
        self.saveButton.clicked.connect(self.saveConfig)
        self.tableWidget.cellChanged.connect(self.cellChangeHandler)
        self.tableWidget.cellActivated.connect(self.insertRow)
        self.tabWidget.currentChanged.connect(self.update_plot)
        self.generateArrayButton.clicked.connect(self.generateArray)   
        self.inputERVButton.clicked.connect(self.corLoadERV)
        self.inputIMSButton.clicked.connect(self.corLoadIMS)
        self.zeroLevelBox.valueChanged.connect(self.corrRecalc)
        self.zeroLevelSlider.valueChanged.connect(lambda: self.zeroLevelBox.setValue(float(self.zeroLevelBox.minimum() + self.zeroLevelSlider.value()*(self.zeroLevelBox.maximum()-self.zeroLevelBox.minimum())/100)))
        self.x0Slider.valueChanged.connect(lambda: self.x0Box.setValue(self.x0Slider.value()))
        self.calcCorrectionButton.clicked.connect(self.correct)
        self.x0Box.valueChanged.connect(self.corrRecalc)


    def setupTable(self):
        '''Setup the table in the "Main features" tab'''
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Coordinate", "Number of shots"])

    def manualConnectionClicked(self):
        '''Change the "Conection" box when the "Manual connection" (un)checked'''
        if self.manualConnectionBox.isChecked() == True:
            self.laserPortLineEdit.setVisible(True)
            self.shutterPortLineEdit.setVisible(True)
            self.manualConnectButton.setVisible(True)
            self.AutoDetectButton.setEnabled(False)
            self.ConnectionBox.setGeometry(QtCore.QRect(10, 20, 211, 161))
        else:
            self.laserPortLineEdit.setVisible(False)
            self.shutterPortLineEdit.setVisible(False)
            self.manualConnectButton.setVisible(False)
            self.AutoDetectButton.setEnabled(True)
            self.ConnectionBox.setGeometry(QtCore.QRect(10, 20, 211, 121))

    def fileClicked(self):
        '''Load all parameters from the file''' 
        try:

            filepath = QFileDialog.getOpenFileName(self, "Open File", self.filedir,
                                        "Impulse Maker savefile (*.ims)")[0]

            self.filedir = str(Path(filepath).parent)
            if filepath == "":
                self.logText("File load aborted")
                return
            f = open(filepath, 'r')
            filename = filepath.split('/')[-1]

            num_lines = int(f.readline())
            self.tableWidget.setRowCount(num_lines)

            params = f.readline().split()
            self.powerSpinBox.setValue(float(params[0]))
            self.openSpinBox.setValue(float(params[1]))
            self.periodSpinBox.setValue(float(params[2]))

            params = f.readline().split()
            self.annealPowerBox.setValue(float(params[0]))
            self.annealSpeedBox.setValue(float(params[1]))

            for i in range(0, num_lines):
                line = f.readline()
                columns = line.split()
                x_item = QTableWidgetItem(columns[0])
                n_item = QTableWidgetItem(columns[1])
                self.tableWidget.setItem(i, 0, x_item)
                self.tableWidget.setItem(i, 1, n_item)

            params = f.readline().split()
            self.startPosBox.setValue(float(params[0]))
            self.endPosBox.setValue(float(params[1]))
            self.stepFuncBox.setValue(float(params[2]))

            num_lines = int(f.readline())
            code = ""
            for i in range(0, num_lines):
                code = code + f.readline()
            self.codeBowser.setFontPointSize(12)
            self.codeBowser.setPlainText(code)

            f.close()
            self.fileEdit.setText(filename)
            self.logText("Successfully loaded configuration file " + filename)
        except:
             self.logWarningText("File loading failed: "
                                 + str(sys.exc_info()[1]))

    def saveConfig(self):
        '''Save all parameters to the file'''
        try:
            filepath = QFileDialog.getSaveFileName(self, "Open File", self.filedir,
                                        "Impulse Maker savefile (*.ims)")[0]

            self.filedir = str(Path(filepath).parent)

            if filepath == "":
                self.logText("File save aborted")
                return
            f = open(filepath, 'w')
            filename = filepath.split('/')[-1]

            num_lines = self.tableWidget.rowCount()
            f.write(str(num_lines) + '\n')

            f.write(str(self.powerSpinBox.value()) + " ")
            f.write(str(self.openSpinBox.value()) + " ")
            f.write(str(self.periodSpinBox.value()) + "\n")

            f.write(str(self.annealPowerBox.value()) + " ")
            f.write(str(self.annealSpeedBox.value()))


            for i in range(0, num_lines):
                x_item = self.tableWidget.item(i, 0)
                n_item = self.tableWidget.item(i, 1)
                f.write("\n" + x_item.text() + '\t' + n_item.text())
            f.write("\n")

            f.write(str(self.startPosBox.value()) + " ")
            f.write(str(self.endPosBox.value()) + " ")
            f.write(str(self.stepFuncBox.value()) + "\n")

            lines_code =  self.codeBowser.toPlainText().split('\n')
            num_lines_code = len(lines_code)
            f.write(str(num_lines_code) + "\n")
            f.write(self.codeBowser.toPlainText())

            f.close()
            self.fileEdit.setText(filename)
            self.logText("Successfully saved the configuration file " + filename)
        except AttributeError:
            self.logWarningText("File saving failed: incorrect number of rows."
                               + " Make sure that all rows filled")
            f.close()
        except:
             self.logWarningText("File saving failed: "
                                 + str(sys.exc_info()[1]))
             f.close()

    def startAnneal(self):
        try:
            self.logText("Anneal started")
            self.interfaceBlock(True)
            self.startButton.setEnabled(True)
            start_pos = 53
            end_pos = 75
            self.Laser.setPower(self.annealPowerBox.value())
            self.Shutter.setMode(1)
            if self.Shutter.getToggle() == "1":
                self.Shutter.setToggle()

            self.logText("Moving to the start position")
            self.Motor.set_velocity_parameters(0, 10, self.motorDefaultSpeed)
            self.Motor.move_to(start_pos, True)
            self.Motor.set_velocity_parameters(0, 10, self.annealSpeedBox.value())

            self.Laser.setOn()
            self.logText("Starting to burn")
            self.Shutter.setToggle()
            self.Motor.move_to(end_pos, True)
            self.Shutter.setToggle()
            self.Laser.setOff()
            self.logText("Anneal finished")
            self.interfaceBlock(False)
        except:
            try:
                self.Laser.setOff()
            except:
                pass
            self.logWarningText("Process failed: "+ str(sys.exc_info()[1]))
            self.interfaceBlock(False)


    def start(self):
        try:
            self.startBlock(True)

            power = self.powerSpinBox.value()
            Topen = self.openSpinBox.value()
            Tperiod = self.periodSpinBox.value()
            self.isNotStarted.clear()

            Laser.setMode('MANCLOSED')
            Laser.setPower(power)

            self.Shutter.setMode(1)
            if self.Shutter.getToggle() == "1":
                self.Shutter.setToggle()
            self.Laser.setOn()
            self.logText("Heating laser")

            self.isNotStarted.wait(self.timeToHeat)
            if self.isNotStarted.isSet():
                self.Laser.setOff()
                self.logWarningText("Interrupted")
                self.startBlock(False)
                self.startButton.setEnabled(True)
                return
            self.logText("Laser heated. Starting process")

            for i in range(0, self.tableWidget.rowCount()):

                if self.isNotStarted.isSet():
                    self.Laser.setOff()
                    self.logWarningText("Interrupted")
                    self.startBlock(False)
                    return

                x_item = self.tableWidget.item(i, 0)
                n_item = self.tableWidget.item(i, 1)
                x = (float(x_item.text()))
                n = (int(n_item.text()))
                self.logText("Processing coordinate "
                             + str(x) + " with " + str(n) + " times")
                self.Motor.move_to(x, True)
                self.shutUp(n, Topen, Tperiod - Topen)

            self.Laser.setOff()
            self.logText("Completed")
            self.isNotStarted.set()
            self.startBlock(False)
        except AttributeError:
            self.logWarningText("Looks like there are empty values" +
                               "in coordinates list. Process stopped.")
            self.Laser.setOff()
            self.interfaceBlock(False)
            self.isNotStarted.set()
        except:
            self.logWarningText("Process failed: "+ str(sys.exc_info()[1]))
            self.isNotStarted.set()
            self.startBlock(False)
            try:
                self.Laser.setOff()
            except:
                pass

    def startClicked(self):
        try:
            if self.isNotStarted.isSet() == False:
                self.isNotStarted.set()
                self.startButton.setEnabled(False)
                return

            else:
                worker = Worker(self.start)
                self.threadpool.start(worker)
        except:
            self.logWarningText(str(sys.exc_info()[1]))


    def cellChangeHandler(self, row, collumn):
        try:

            x_item = self.tableWidget.item(row, 0)
            n_item = self.tableWidget.item(row, 1)

            if x_item is None:
                self.tableWidget.setItem(row, 0, QTableWidgetItem(""))
                return
            if n_item is None:
                self.tableWidget.setItem(row, 1, QTableWidgetItem(""))
                return

            x =x_item.text()
            n = n_item.text()

            if x == "" and n == "" and self.tableWidget.rowCount() != 1:
                self.tableWidget.removeRow(row)
        except ValueError:
            self.logWarningText("Process failed: "+ str(sys.exc_info()[1]))

    def insertRow(self, row, collumn):
        self.tableWidget.insertRow(row+1)

        x_item = QTableWidgetItem("0")
        n_item = QTableWidgetItem("0")
        self.tableWidget.setItem(row+1, 0, x_item)
        self.tableWidget.setItem(row+1, 1, n_item)


    def generateArray(self):
        try:
            start_pos = self.startPosBox.value()
            end_pos = self.endPosBox.value()
            step = self.stepFuncBox.value()
            num = int((end_pos - start_pos)/step + 1)
            xs = np.linspace(start_pos, end_pos, num)

            lines =  self.codeBowser.toPlainText().split('\n')
            with open("temp.py", "w") as f:
                f.write("def func(x):\n")
                for line in lines:
                    f.write("\t" + line + "\n")
                f.write("\treturn int(n)")
                f.close()

            if "temp" in sys.modules:
                importlib.reload(self.module)
            else:
                self.module = importlib.import_module("temp")

            self.tableWidget.setRowCount(num)
            for i in range(0, num):
                x_item = QTableWidgetItem(str(xs[i]))
                n_item = QTableWidgetItem(str(self.module.func(xs[i])))
                self.tableWidget.setItem(i, 0, x_item)
                self.tableWidget.setItem(i, 1, n_item)
            os.remove("temp.py")

            self.logText("Array generated")
        except ValueError:
             self.logWarningText(str(sys.exc_info()[1]))
             
             
    def loadShotsFromIms(self, filename):
        f = open(filename, 'r')
    
        numLines = int(f.readline())
        shotsArray = np.zeros((numLines, 2))
        f.readline()
        f.readline()
        for i in range(0, numLines):
            line = f.readline().split()
            shotsArray[i,0]=float(line[0]) 
            shotsArray[i,1]=int(line[1])
        
        f.close()
    
        return shotsArray
    
    def corrRecalc(self):
        try:    
            ERVarray = np.loadtxt(self.inputERVEdit.text())[:,:2]    #   scan array
            

            
            
            self.ERVcanvas.axes.cla()  # Clear the canvas.
            self.ERVcanvas.axes.plot(ERVarray[:,0],ERVarray[:,1], 'b')
            self.ERVcanvas.axes.axhline(self.zeroLevelBox.value(),color='green', ls='--', lw=1)
            self.ERVcanvas.axes.axvline(self.x0Box.value(),color='red',ls='--', lw = 1)
            self.ERVcanvas.draw()
            
            if self.inputIMSEdit.text() != "":
                
                IMSarray = self.loadShotsFromIms(self.inputIMSEdit.text())  # shots array
                ERVmod = ERVarray[ERVarray[:,1] > self.zeroLevelBox.value()]    # only modified points
                x_n = (ERVmod[:,0] * self.stepsInMm) + (IMSarray[0,0] - self.x0Box.value()* self.stepsInMm)


                y = np.empty(len(IMSarray))

                for i in range(len(IMSarray)):
                    cor = np.argmin(abs(IMSarray[i,0] - x_n))
                    y[i] = ERVmod[cor,1]    # ERV coordinates. corresponding to x points

                y_n = (y - self.zeroLevelBox.value())/np.mean((y-self.zeroLevelBox.value())/IMSarray[:,1]) # ERV Y points in IMS coordinates
                
                y_new= IMSarray[:,1] + max(y_n - IMSarray[:,1])

                y_corr = np.round(y_new-y_n)

                            
                self.corCanvas.axes.cla()  # Clear the canvas.
                self.corCanvas.axes.plot(IMSarray[:,0],IMSarray[:,1], 'b')
                self.corCanvas.axes.plot(IMSarray[:,0],y_n, 'g')
                self.corCanvas.axes.plot(IMSarray[:,0],y_new, '--g')
                self.corCanvas.draw()
                
                return (IMSarray[:,0],y_corr)
            
        except:
            self.logWarningText(str(sys.exc_info()[1]))
        
    def IMSredraw(self):        
        shotsArray = self.loadShotsFromIms(self.inputIMSEdit.text())
        
        self.corCanvas.axes.cla()  # Clear the canvas.
        self.corCanvas.axes.plot(shotsArray[:,0],shotsArray[:,1], 'b')
        self.corCanvas.draw()
        
        if self.inputERVEdit.text() != "":
            self.corrRecalc()
        
    def corLoadERV(self):
        try:
            filepath = QFileDialog.getOpenFileName(self, "Open File", self.ERVdir,
                                        "ERV data file (*.txt)")[0]

            self.ERVdir = str(Path(filepath).parent)
            if filepath == "":
                self.logText("File load aborted")
                return
            self.inputERVEdit.setText(filepath)
            
            ERVarray = np.loadtxt(self.inputERVEdit.text())[:,:2]
            
            self.x0Slider.setMinimum(ERVarray[0,0])
            self.x0Box.setMinimum(ERVarray[0,0])
            self.x0Slider.setMaximum(int(ERVarray[-1,0]))
            self.x0Box.setMaximum(int(ERVarray[-1,0]))
            
            self.x0Slider.setValue(ERVarray[0,0] + 60/2.5)
            
    
           
            self.zeroLevelBox.setMinimum(np.nanmin(ERVarray[:,1]))                                 
            self.zeroLevelBox.setMaximum(np.nanmax(ERVarray[:,1]))
            
            self.zeroLevelBox.setValue((np.nanmax(ERVarray[:,1])+np.nanmin(ERVarray[:,1]))/2)
            
            
            self.corrRecalc()
        except:
             self.logWarningText(str(sys.exc_info()[1]))
             
    def corLoadIMS(self):
        try:
            filepath = QFileDialog.getOpenFileName(self, "Open File", self.IMSdir,
                                        "IMS data file (*.ims)")[0]

            self.IMSdir = str(Path(filepath).parent)
            if filepath == "":
                self.logText("File load aborted")
                return
            self.inputIMSEdit.setText(filepath)
            
            self.IMSredraw()
        except:
             self.logWarningText(str(sys.exc_info()[1]))
             
        
    def correct(self):
        try:
            corArray = self.corrRecalc()
            num_lines = len(corArray[0])
            self.tableWidget.setRowCount(num_lines)
            for i in range(0, num_lines):
                x_item = QTableWidgetItem(str(corArray[0][i]))
                n_item = QTableWidgetItem(str(int(corArray[1][i])))
                self.tableWidget.setItem(i, 0, x_item)
                self.tableWidget.setItem(i, 1, n_item)
            self.logText("Array generated successfully. See 'Main features' and 'N(x)' tabs for details")
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def toggleShutter(self):
        try:
            self.Shutter.setMode(1)
            self.Shutter.setToggle()
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def shutUp(self, N, Topen, Tclose):
        self.Shutter.setMode(4)
        self.Shutter.setRepeat(N)
        self.Shutter.setOpenTime(Topen)
        self.Shutter.setCloseTime(Tclose)
        self.Shutter.setToggle()
        time.sleep(N * (Topen + Tclose)/1000)

    def __del__(self):
        try:
            self.Laser.close()
            self.Shutter.sc._file.close()
            apt._cleanup()
            print ("Cleared")
        except NameError:
            pass
        except:
            print(str(sys.exc_info()[1]))



def main():
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()


    main = MainApp()
    main.show()
    ####################
#    sys.exit(app.exec())
    ####################
    return main


if __name__ == '__main__':

    m = main()
