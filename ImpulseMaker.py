import importlib
import threading
import time
import sys
import os
from pathlib import Path
import numpy as np
from scipy.interpolate import interp1d
import json

from im_classes.CustomTable import CustomTable
from common.Common import Worker, CommonClass
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from ui import IM as ui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, QtWidgets

DEBUG = False


_version_='2.5'
_date_='2023.03.16'

class MplCanvas(FigureCanvasQTAgg):
    '''Canvas for combining matplotlib plots and qt graphics'''

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes_2=self.axes.twinx()
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
         self.conversionFilePath = "."
        
         # Run initialization
         CommonClass.__init__(self)
         ui.Ui_MainWindow.__init__(self)
         self.setupUi(self) 
         self.setWindowTitle("ImpulseMaker V. "+_version_+', date  ' + _date_)
         self.isNotStarted = threading.Event()
         self.isNotStarted.set()        

         self.tableWidget = CustomTable(self.tab)
         self.setupButtons()
         self.setupBox()

         # Start to detect equipment
         if not DEBUG:
            self.threadpool.start(self.worker1)
            self.threadpool.start(self.worker2)

         #define plotы for function generator        
         self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
         toolbar = NavigationToolbar(self.canvas, self)

         layout = QtWidgets.QGridLayout(self.tab_2)
         layout.addWidget(toolbar)
         layout.addWidget(self.canvas)
         
         #define  ERV plot for correction
         self.ERVcanvas = MplCanvas(self, dpi=70)        
         ERVlayout = QtWidgets.QGridLayout(self.ERVView)
         ERVlayout.addWidget(self.ERVcanvas)
         
         #define  correction plot for correction
         self.corCanvas = MplCanvas(self, dpi=70)        
         corLayout = QtWidgets.QGridLayout(self.correctionView)
         corLayout.addWidget(self.corCanvas)
         
         #define interpolation scipy objects for calibration R_eff<->N_shots
         self.N_to_dR=None
         self.dR_to_N=None
         
          

    def update_plot(self):
        '''
        Draw/redraw the function plot in the "N(x)" tab from table located in
        the "Main functions" tab.

        Returns
        -------
        None.

        '''
        if self.tabWidget.currentIndex() == 1 and self.tableWidget.rowCount() > 1:
            try:
                x_data = []
                N_data = []
                dR_data=[]
                num_lines = self.tableWidget.rowCount()
                # if self.
                for i in range(0, num_lines):
                    x_item = self.tableWidget.item(i, 0)
                    n_item = self.tableWidget.item(i, 1)
                    dR_item = self.tableWidget.item(i, 2)
                    x = float(x_item.text())
                    try:
                        n = int(n_item.text())
                    except:
                        n=0
                    try:
                        dR= float(dR_item.text())
                    except:
                        dR=0

    
                    x_data.append(x)
                    N_data.append(n)
                    dR_data.append(dR)
    
                self.canvas.axes.cla()  # Clear the canvas.
                self.canvas.axes_2.cla()  # Clear the canvas.
                self.canvas.axes.plot(x_data, N_data, 'r')
                self.canvas.axes.set_xlabel('x')
                self.canvas.axes.set_ylabel('$N_{shots}$', color='r')
                self.canvas.axes_2.plot(x_data,dR_data,'b')
                self.canvas.axes_2.set_ylabel('$dR$', color='b')
                
                # Trigger the canvas to update and redraw.
                self.canvas.draw()
            except:
                self.logWarningText("Plotting failed: " + str(sys.exc_info()[1]))

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
        self.manualConnectionBox.stateChanged.connect(
            self.manualConnectionClicked)
        self.AutoDetectButton.clicked.connect(self.autoDetectClicked)
        self.manualConnectButton.clicked.connect(self.manualConnectClicked)
        self.StagesToZerosButton.clicked.connect(
            lambda: self.runThread(self.stagesToZerosClicked))
        self.StagesToHomeButton.clicked.connect(
            lambda: self.runThread(self.stagesToHomeClicked))
        self.MoveStagesButton.clicked.connect(
            lambda: self.runThread(self.moveStagesClicked))
        self.startButton.clicked.connect(self.startClicked)
        self.fileButton.clicked.connect(self.fileClicked)
        self.startAnnealButton.clicked.connect(
            lambda: self.runThread(self.startAnneal))
        self.toggleShutterButton.clicked.connect(self.toggleShutter)
        self.saveButton.clicked.connect(self.saveConfig)
        self.tableWidget.cellChanged.connect(self.cellChangeHandler)
        self.tabWidget.currentChanged.connect(self.update_plot)
        self.generateArrayButton.clicked.connect(self.generateArray)
        self.inputERVButton.clicked.connect(self.corLoadERV)
        self.inputIMSButton.clicked.connect(self.corLoadIMS)
        self.zeroLevelBox.valueChanged.connect(self.corrRecalc)
        self.zeroLevelSlider.valueChanged.connect(lambda: self.zeroLevelBox.setValue(float(self.zeroLevelBox.minimum(
        ) + self.zeroLevelSlider.value()*(self.zeroLevelBox.maximum()-self.zeroLevelBox.minimum())/100)))
        self.x0Slider.valueChanged.connect(
            lambda: self.x0Box.setValue(self.x0Slider.value()))
        self.calcCorrectionButton.clicked.connect(self.correct)
        self.x0Box.valueChanged.connect(self.corrRecalc)
        self.radiusButton.toggled.connect(lambda: self.tableWidget.changeMode(
            self.shotsButton.isChecked())) # TODO: rename button to appropriate label
        self.modFileButton.clicked.connect(self.setConversionFile)
        self.conversionButton.clicked.connect(self.startConversion)

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
            self.openSpinBox.setValue(int(params[1]))
            self.periodSpinBox.setValue(int(params[2]))

            params = f.readline()
            params=params.rstrip('\n')   
            self.comboBox_proccesing_type.setCurrentText(str(params))

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
                
                r_item = QTableWidgetItem(None)
                self.tableWidget.setItem(i, 2, r_item)
                

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
            
            self.tableWidget.changeMode(self.shotsButton.isChecked())

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
            
            f.write(str(self.comboBox_proccesing_type.currentText()) + "\n")
            
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

            lines_code = self.codeBowser.toPlainText().split('\n')
            num_lines_code = len(lines_code)
            f.write(str(num_lines_code) + "\n")
            f.write(self.codeBowser.toPlainText())

            f.close()
            self.fileEdit.setText(filename)
            self.logText(
                "Successfully saved the configuration file " + filename)
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
            start_pos = self.annealStartPos.value()
            end_pos = self.annealStopPos.value()
            self.Laser.setPower(self.annealPowerBox.value())
            self.Shutter.setMode(1)
            if self.Shutter.getToggle() == "1":
                self.Shutter.setToggle()

            self.logText("Moving to the start position")
            self.Motor.set_velocity_parameters(0, 10, self.motorDefaultSpeed)
            self.Motor.move_to(start_pos, True)
            self.Motor.set_velocity_parameters(
                0, 10, self.annealSpeedBox.value())

            self.Laser.setOn()
            self.logText("Heating laser...")
            time.sleep(10)
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
            self.logWarningText("Process failed: " + str(sys.exc_info()[1]))
            self.interfaceBlock(False)

    def start(self):
        
        def _create_working_table():
            raw_table=[]
            for i in range(0, self.tableWidget.rowCount()):
                    x_item = self.tableWidget.item(i, 0)
                    n_item = self.tableWidget.item(i, 1)
                    x = (float(x_item.text()))
                    n = (int(n_item.text()))
                    raw_table.append([x,n,False])
            if self.comboBox_proccesing_type.currentText()=='Point by point':
                return raw_table
            elif self.comboBox_proccesing_type.currentText()=='Slice by slice':
                table=[]
                forward_direction=True
                while len(raw_table)>0:
                    temp_table=[]
                    i=0
                    length=len(raw_table)
                    while i<length:
                        t=raw_table[i]
                        if t[1]>1:
                            raw_table[i][1]-=1
                            temp_table.append([t[0],1,False])
                        elif t[1]==1:
                            raw_table.pop(i)
                            temp_table.append([t[0],1,False])
                            length-=1
                            i-=1
                        elif t[1]==0:
                            raw_table.pop(i)
                            length-=1
                            i-=1
                        i+=1
                    if forward_direction:
                        temp_table.sort(key=lambda x:x[0])
                        forward_direction=not forward_direction
                    else:
                        temp_table.sort(key=lambda x:-x[0])
                        forward_direction=not forward_direction
                    temp_table[-1][2]=True
                    table=table+temp_table
                return table
                
        try:
            
            table=_create_working_table()
            print(table)
            self.startBlock(True)

            power = self.powerSpinBox.value()
            Topen = self.openSpinBox.value()
            Tperiod = self.periodSpinBox.value()
            self.isNotStarted.clear()

            self.Laser.setMode('MANCLOSED')
            self.Laser.setPower(power)

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

            for ind,t in enumerate(table):

                if self.isNotStarted.isSet():
                    self.Laser.setOff()
                    self.logWarningText("Interrupted")
                    self.startBlock(False)
                    return

                self.logText("Step "+str(ind)+" of " + str(len(table))+". Processing coordinate "
                             + str(t[0]) + " with " + str(t[1]) + " times")
                self.Motor.move_to(t[0], True)
                if t[1]>0:
                    self.shutUp(t[1], Topen, Tperiod - Topen)
                if t[2]: # in points where direction of processing changes
                    time.sleep(1.5)

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
            self.logWarningText("Process failed: " + str(sys.exc_info()[1]))
            self.isNotStarted.set()
            self.startBlock(False)
            try:
                self.Laser.setOff()
            except:
                pass
        # 
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

            x = x_item.text()
            n = n_item.text()

            if x == "" and n == "" and self.tableWidget.rowCount() != 1:
                self.tableWidget.removeRow(row)
        except ValueError:
            self.logWarningText("Process failed: " + str(sys.exc_info()[1]))

    def generateArray(self):
        try:
            start_pos = self.startPosBox.value()
            end_pos = self.endPosBox.value()
            step = self.stepFuncBox.value()
            num = int((end_pos - start_pos)/step + 1)
            xs = np.linspace(start_pos, end_pos, num)

            lines = self.codeBowser.toPlainText().split('\n')
            with open("temp.py", "w") as f:
                f.write("def func(x):\n")
                for line in lines:
                    f.write("\t" + line + "\n")
                f.write("\treturn round(f,3)")
                f.close()

            if "temp" in sys.modules:
                importlib.reload(self.module)
            else:
                self.module = importlib.import_module("temp")

            self.tableWidget.setRowCount(num)
            if self.radiusButton.isChecked():
                for i in range(0, num):
                    x_item = QTableWidgetItem(str(xs[i]))
                    r_item = QTableWidgetItem(str(self.module.func(xs[i])))
                    self.tableWidget.setItem(i, 0, x_item)
                    self.tableWidget.setItem(i, 2, r_item)
            else:
                for i in range(0, num):
                    x_item = QTableWidgetItem(str(xs[i]))
                    n_item = QTableWidgetItem(str(int(self.module.func(xs[i]))))
                    self.tableWidget.setItem(i, 0, x_item)
                    self.tableWidget.setItem(i, 1, n_item)
            os.remove("temp.py")

            self.logText("Array generated")
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def loadShotsFromIms(self, filename):
        f = open(filename, 'r')

        numLines = int(f.readline())
        shotsArray = np.zeros((numLines, 2))
        f.readline()
        f.readline()
        for i in range(0, numLines):
            line = f.readline().split()
            shotsArray[i, 0] = float(line[0])
            shotsArray[i, 1] = int(line[1])

        f.close()

        return shotsArray

    def corrRecalc(self):
        try:
            ERVarray = np.loadtxt(self.inputERVEdit.text())[
                :, :2]  # scan array

            self.ERVcanvas.axes.cla()  # Clear the canvas.
            self.ERVcanvas.axes.plot(ERVarray[:, 0], ERVarray[:, 1], 'b')
            self.ERVcanvas.axes.axhline(
                self.zeroLevelBox.value(), color='green', ls='--', lw=1)
            self.ERVcanvas.axes.axvline(
                self.x0Box.value(), color='red', ls='--', lw=1)
            self.ERVcanvas.draw()

            if self.inputIMSEdit.text() != "":
                IMSarray = self.loadShotsFromIms(
                    self.inputIMSEdit.text())  # shots array
                # only modified points
                ERVmod = ERVarray[ERVarray[:, 1] > self.zeroLevelBox.value()]
                x_n = (ERVmod[:, 0] * self.stepsInMm) + \
                    (IMSarray[0, 0] - self.x0Box.value() * self.stepsInMm)

                y = np.empty(len(IMSarray))

                for i in range(len(IMSarray)):
                    cor = np.argmin(abs(IMSarray[i, 0] - x_n))
                    # ERV coordinates. corresponding to x points
                    y[i] = ERVmod[cor, 1]

                # ERV Y points in IMS coordinates
                y_n = (y - self.zeroLevelBox.value()) / \
                    np.mean((y-self.zeroLevelBox.value())/IMSarray[:, 1])

                y_new = IMSarray[:, 1] + max(y_n - IMSarray[:, 1])

                y_corr = np.round(y_new-y_n)

                self.corCanvas.axes.cla()  # Clear the canvas.
                self.corCanvas.axes.plot(IMSarray[:, 0], IMSarray[:, 1], 'b')
                self.corCanvas.axes.plot(IMSarray[:, 0], y_n, 'g')
                self.corCanvas.axes.plot(IMSarray[:, 0], y_new, '--g')
                self.corCanvas.draw()

                return (IMSarray[:, 0], y_corr)

        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def IMSredraw(self):
        shotsArray = self.loadShotsFromIms(self.inputIMSEdit.text())

        self.corCanvas.axes.cla()  # Clear the canvas.
        self.corCanvas.axes.plot(shotsArray[:, 0], shotsArray[:, 1], 'b')
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

            ERVarray = np.loadtxt(self.inputERVEdit.text())[:, :2]

            self.x0Slider.setMinimum(ERVarray[0, 0])
            self.x0Box.setMinimum(ERVarray[0, 0])
            self.x0Slider.setMaximum(int(ERVarray[-1, 0]))
            self.x0Box.setMaximum(int(ERVarray[-1, 0]))

            self.x0Slider.setValue(ERVarray[0, 0] + 60/2.5)

            self.zeroLevelBox.setMinimum(np.nanmin(ERVarray[:, 1]))
            self.zeroLevelBox.setMaximum(np.nanmax(ERVarray[:, 1]))

            self.zeroLevelBox.setValue(
                (np.nanmax(ERVarray[:, 1])+np.nanmin(ERVarray[:, 1]))/2)

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
            print(corArray)
            num_lines = len(corArray[0])
            self.tableWidget.setRowCount(num_lines)
            for i in range(0, num_lines):
                x_item = QTableWidgetItem(str(corArray[0][i]))
                n_item = QTableWidgetItem(str(int(corArray[1][i])))
                self.tableWidget.setItem(i, 0, x_item)
                self.tableWidget.setItem(i, 1, n_item)
            self.logText(
                "Array generated successfully. See 'Main features' and 'N(x)' tabs for details")
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
        
    def setConversionFile(self):
        try:
            filepath = QFileDialog.getOpenFileName(self, "Open File", 
                        self.conversionFilePath,"Multiple JEN file (*.mjen)")[0]
            self.modFileEdit.setText(filepath.split('/')[-1])
            self.conversionFilePath = filepath
            
            
        except:
            self.logWarningText("MJEN File path not set: " + str(sys.exc_info()[1]))
        try:
            with open(self.conversionFilePath, 'r') as file:
                conversionFile = json.load(file)
            d = conversionFile["dR_avg(N)"]
            dRtable = np.array([[i['N_shots'],i['dR_avg']] for i in d])
            plt.figure()
            plt.title('Calibration curve, P={} %, T={} ms'.format(conversionFile['laser_power'],conversionFile['open_time']))
            plt.plot(dRtable[:,0],dRtable[:,1],'o')
            plt.xlabel('$N_{shots}$')
            plt.ylabel('$\Delta R_{eff}$, nm')
            self.logText("Calibration successfully set")
            self.N_to_dR = interp1d(dRtable[:,0], dRtable[:,1],fill_value='extrapolate')
            self.dR_to_N = interp1d(dRtable[:,1], dRtable[:,0],fill_value='extrapolate')
            n_array=np.linspace(0,max(dRtable[:,0]),100)
            plt.plot(n_array,self.N_to_dR(n_array))
        except:
            self.logWarningText(f'Wrong calibration file : {str(sys.exc_info()[1])}')
            

    def startConversion(self):
        try:
            if self.radiusButton.isChecked(): # dReff -> N Conversion
                for i in range(self.tableWidget.rowCount()):
                    dR = float(self.tableWidget.item(i, 2).text())
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(int(self.dR_to_N(dR)))))
            else: # N -> dReff conversion
                for i in range(self.tableWidget.rowCount()):
                    N = float(self.tableWidget.item(i, 1).text())
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(np.round(self.N_to_dR(N),3))))
            
            self.tableWidget.changeMode(self.shotsButton.isChecked())
            self.logText("Conversion succeed")
        except:
            self.logWarningText(f'Conversion failed: {str(sys.exc_info()[1])}')
        
        # try:
        #     with open(self.conversionFilePath, 'r') as file:
        #         conversionFile = json.load(file)
                
        # # TODO: laser/file parameters check with a popup warning if needed
        #     d = conversionFile["dR_avg(N)"]
        #     if self.radiusButton.isChecked(): # dReff -> N Conversion
        #         dRtable = np.array([i['dR_avg'] for i in d])
        #         for i in range(self.tableWidget.rowCount()):
        #             dR = float(self.tableWidget.item(i, 2).text())
        #             # find closest to each dr
        #             closestInd = np.argmin(np.abs(dRtable-dR))
        #             #fill the value into the table
        #             nItem = QTableWidgetItem(str(d[closestInd]['N_shots']))
        #             self.tableWidget.setItem(i, 1, nItem)
        #     else: # N -> dReff conversion
        #         Ntable = np.array([i['N_shots'] for i in d])
        #         for i in range(self.tableWidget.rowCount()):
        #             N = float(self.tableWidget.item(i, 1).text())
        #             # find closest to each dr
        #             closestInd = np.argmin(np.abs(Ntable-N))
        #             #fill the value into the table
        #             dRitem = QTableWidgetItem(str(d[closestInd]['dR_avg']))
        #             self.tableWidget.setItem(i, 2, dRitem)
            
        #     self.tableWidget.changeMode(self.shotsButton.isChecked())
        #     self.logText("Conversion succeed")
        # except:
        #     self.logWarningText(f'Conversion failed: {str(sys.exc_info()[1])}')

    def __del__(self): #TODO: change to close event?
        try:
            self.Laser.close()
            self.Shutter.sc._file.close()
            apt._cleanup()
            print("Cleared")
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
    # sys.exit(app.exec()) # Uncomment for inline graphics mode in Spyder
    return main


if __name__ == '__main__':

    m = main()
