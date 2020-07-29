DEBUG = False
#import os
from pathlib import Path
from serial import SerialException
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
import serial.tools.list_ports
import sys
from ui import MainWindow as ui
from libs import SynradLaser, SC10Shutter
import time
import threading


import matplotlib
import random
matplotlib.use('Qt5Agg')


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):

        self.fn(*self.args, **self.kwargs)


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)



class MainApp(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
         QMainWindow.__init__(self)
         ui.Ui_MainWindow.__init__(self)

         self.threadpool = QtCore.QThreadPool()
         self.isNotStarted = threading.Event()
         self.isNotStarted.set()

         global Laser
         global Shutter
         global Motor

         self.timeToHeat = 30 # sec
         self.motorDefaultSpeed = 5 ## mm/s
         self.filedir = "saves"

         self.setupUi(self)
         self.setupBox()
         self.setupButtons()
         self.setupTable()

         worker1 = Worker(self.setupMotor)
         self.threadpool.start(worker1)
         worker2 = Worker(self.autoDetectClicked)
         self.threadpool.start(worker2)


         self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
         toolbar = NavigationToolbar(self.canvas, self)
         
         layout = QtWidgets.QGridLayout(self.tab_2)
         layout.addWidget(toolbar)
         layout.addWidget(self.canvas)

    def update_plot(self):
        if self.tabWidget.currentIndex() == 1:
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
    

    def setupBox(self):
        self.laserPortLineEdit.setVisible(False)
        self.shutterPortLineEdit.setVisible(False)
        self.manualConnectButton.setVisible(False)

    def setupButtons(self):
        self.manualConnectionBox.stateChanged.connect(self.manualConnectionClicked)
        self.AutoDetectButton.clicked.connect(self.autoDetectClicked)
        self.manualConnectButton.clicked.connect(self.manualConnectClicked)
        self.StagesToZerosButton.clicked.connect(self.stagesToZerosClicked)
        self.StagesToHomeButton.clicked.connect(self.stagesToHomeClicked)
        self.MoveStagesButton.clicked.connect(self.moveStagesClicked)
        self.startButton.clicked.connect(self.startClicked)
        self.fileButton.clicked.connect(self.fileClicked)
        self.startAnnealButton.clicked.connect(self.startAnnealClicked)
        self.toggleShutterButton.clicked.connect(self.toggleShutter)
        self.saveButton.clicked.connect(self.saveConfig)
        self.tableWidget.cellChanged.connect(self.cellChangeHandler)
        self.tableWidget.cellActivated.connect(self.insertRow)
        self.tabWidget.currentChanged.connect(self.update_plot)
        self.sortingBox.stateChanged.connect(self.toggleSort)

    def setupTable(self):
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Coordinate", "Number of shots"])

    def setupMotor(self):
        global Motor 
        try:

             import thorlabs_apt as apt
             Motor = apt.Motor(90864301)
             Motor.set_move_home_parameters(2, 1, 7.0, 0.0001)
             self.logText("Motor initialized")
             self.LogField.append("")
        except:
            self.logWarningText("Motor not initialized :"+str(sys.exc_info()[1]))
            self.LogField.append("")


    def manualConnectionClicked(self):
        if self.manualConnectionBox.isChecked() == True:
            self.laserPortLineEdit.setVisible(True)
            self.shutterPortLineEdit.setVisible(True)
            self.manualConnectButton.setVisible(True)
            self.AutoDetectButton.setEnabled(False)
            self.ConnectionBox.setGeometry(QtCore.QRect(20, 20, 201, 161))
        else:
            self.laserPortLineEdit.setVisible(False)
            self.shutterPortLineEdit.setVisible(False)
            self.manualConnectButton.setVisible(False)
            self.AutoDetectButton.setEnabled(True)
            self.ConnectionBox.setGeometry(QtCore.QRect(20, 20, 201, 121))


    def autoDetectClicked(self):


        self.logText("Autodetect started")
        isShutterConnected = False
        isLaserConnected = False

        ports = list(serial.tools.list_ports.comports())

        global Shutter
        global Laser


        for p in ports:

            if not (isLaserConnected):
                try:
                    Laser = SynradLaser.Laser(p.device)

                    Laser.getStatus()

                    isLaserConnected = True
                    self.laserPortLabel.setText("Laser port:    " + p.device)
                    self.logText("Laser connected")
                    continue
                except SerialException:
                    if DEBUG:
                        self.logWarningText("Laser can't open, port is busy:"+p.device)
                except:
                    if DEBUG:
                        self.logWarningText("Laser was not connected on "+p.device+": "+str(sys.exc_info()[1]))
                    Laser.close()
                    pass

            if not (isShutterConnected):
                try:
                    Shutter = SC10Shutter.Shutter(p.device)
                    Shutter.getID()
                    isShutterConnected = True
                    self.shutterPortLabel.setText("Shutter port: "+p.device)
                    self.logText("Shutter connected")
                    continue
                except SerialException:
                    if DEBUG:
                        self.logWarningText("Shutter can't open, port is busy:"+p.device)
                except:
                    if DEBUG:
                        self.logWarningText("Shutter was not connected on "+p.device+": "+str(sys.exc_info()[1]))
                    Shutter.sc._file.close()
                    pass

        if not (isShutterConnected):
            self.logWarningText("Shutter not found")
            self.shutterPortLabel.setText("Shutter port: COM")
        if not (isLaserConnected):
            self.logWarningText("Laser not found")
            self.laserPortLabel.setText("Laser port:    COM")

        self.LogField.append("")

    def stagesToZerosClicked(self):
        try:

            Motor.set_velocity_parameters(0, 3.5, 4.5)

            Motor.move_home(True)
            self.logText('Stages moved to zeros')
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def stagesToHomeClicked(self):
        try:
            Motor.backlash_distance(0)

            Motor.set_velocity_parameters(0, 3.5, 4.5)

            Home_value2 = 53

            Motor.move_to(Home_value2, True)
            self.logText('Stages moved to start position')
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def moveStagesClicked(self):
        try:
            Motor.set_velocity_parameters(0, 3.5, 4.5)
            Motor.move_by(float(self.ui.MoveStagesField.text()), False)
            self.logText('Stages moved')
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def manualConnectClicked(self):
        global Laser
        global Shutter

        try:
            Laser.close()
            Shutter.sc._file.close()
        except:
            if DEBUG:
                self.logWarningText("Laser disconnect: " + str(sys.exc_info()[1]))
            pass

        self.logText("Manual connection started")
        try:
            Laser = SynradLaser.Laser("COM"+self.laserPortLineEdit.text())
            Laser.getStatus()
            self.logText("Laser connected")
            self.shutterPortLabel.setText("Laser port:    COM" + self.laserPortLineEdit.text())

        except SerialException:
            self.logWarningText("Laser connection failed: "+ str(sys.exc_info()[1]))
            self.laserPortLabel.setText("Laser port:    COM")
        except:
            self.logWarningText("Laser connection failed: "+ str(sys.exc_info()[1]))
            self.laserPortLabel.setText("Laser port:    COM")
            Laser.close()

        try:
            Shutter = SC10Shutter.Shutter("COM" + self.shutterPortLineEdit.text())
            Shutter.getID()
            self.logText("Shutter connected")
            self.shutterPortLabel.setText("Shutter port: COM" + self.shutterPortLineEdit.text())
        except SerialException:
            self.logWarningText("Shuter connection failed: "+ str(sys.exc_info()[1]))
            self.shutterPortLabel.setText("Shutter port: COM")
        except:
            self.logWarningText("Shuter connection failed: "+ str(sys.exc_info()[1]))
            self.shutterPortLabel.setText("Shutter port: COM")
            Shutter.sc._file.close()

        self.LogField.append("")


    def fileClicked(self):
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
                
            self.fileEdit.setText(filename)
            self.logText("Successfully loaded configuration file " + filename)
        except:
             self.logWarningText("File loading failed: "
                                 + str(sys.exc_info()[1]))
             
    def saveConfig(self):
        try:
            filepath = QFileDialog.getSaveFileName(self, "Open File", self.filedir,
                                        "Impulse Maker savefile (*.ims)")[0]
            
            self.filedir = str(Path(filepath).parent)
        
            if filepath == "":
                self.logText("File save aborted")
                return
            f = open(filepath, 'w')
            filename = filepath.split('/')[-1]
            
            num_lines = self.tableWidget.rowCount() - 1
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
             
            f.close()
            self.fileEdit.setText(filename)
            self.logText("Successfully saved configuration file " + filename)
        except AttributeError:
            self.logWarningText("File saving failed: incorrect number of rows."
                               + " Make sure that all rows filled")
            f.close()
        except:
             self.logWarningText("File saving failed: "
                                 + str(sys.exc_info()[1]))
             f.close()
    
    def startAnnealClicked(self):
        try:
            worker = Worker(self.startAnneal)
            self.threadpool.start(worker)
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def startAnneal(self):
        try:
            self.logText("Anneal started")
            self.startAnnealButton.setEnabled(False)
            start_pos = 53
            end_pos = 75
            Laser. setPower(self.annealPowerBox.value())
            Shutter.setMode(1)
            if Shutter.getToggle() == "1":
                Shutter.setToggle()

            self.logText("Moving to start position")
            Motor.set_velocity_parameters(0, 10, self.motorDefaultSpeed)
            Motor.move_to(start_pos, True)
            Motor.set_velocity_parameters(0, 10, self.annealSpeedBox.value())

            Laser.setOn()
            self.logText("Starting to burn")
            Shutter.setToggle()
            Motor.move_to(end_pos, True)
            Shutter.setToggle()
            Laser.setOff()
            self.logText("Anneal finished")
            self.startAnnealButton.setEnabled(True)


        except:
            try:
                Laser.setOff()
            except:
                pass
            self.logWarningText("Process failed: "+ str(sys.exc_info()[1]))
            self.startAnnealButton.setEnabled(True)


    def start(self):
        try:
            power = self.powerSpinBox.value()
            Topen = self.openSpinBox.value()
            Tperiod = self.periodSpinBox.value()
            self.isNotStarted.clear()

            Laser.setPower(power)

            Shutter.setMode(1)
            if Shutter.getToggle() == "1":
                Shutter.setToggle()
            Laser.setOn()
            self.logText("Heating laser")

            self.isNotStarted.wait(self.timeToHeat)
            if self.isNotStarted.isSet():
                Laser.setOff()
                self.logWarningText("Interrupted")
                return
            self.logText("Laser heated. Starting process")

            for i in range(0, self.tableWidget.rowCount() - 1):
                    
                x_item = self.tableWidget.item(i, 0)
                n_item = self.tableWidget.item(i, 1)
                x = (float(x_item.text()))
                n = (int(n_item.text()))
                self.logText("Processing coordinate "
                             + str(x) + " with " + str(n) + " times")

                Motor.move_to(x, True)
                if self.isNotStarted.isSet():
                    Laser.setOff()
                    self.logWarningText("Interrupted")
                    return

                self.shutUp(n, Topen, Tperiod - Topen)

            Laser.setOff()
            self.logText("Completed")
            self.isNotStarted.set()
        except AttributeError:
            self.logWarningText("Looks like there are empty values" +
                               "in coordinates list. Process stopped.")
            Laser.setOff()
            self.isNotStarted.set()
        except:
            self.logWarningText("Process failed: "+ str(sys.exc_info()[1]))
            self.isNotStarted.set()
            try:
                Laser.setOff()
            except:
                pass

    def startClicked(self):
        try:
            if self.isNotStarted.isSet() == False:
                self.isNotStarted.set()
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
            
#            if row + 1 == self.tableWidget.rowCount():
#                self.tableWidget.insertRow(self.tableWidget.rowCount())
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

    def toggleSort(self):
        if self.sortingBox.isChecked():
            self.tableWidget.setSortingEnabled(True)
        else:
            self.tableWidget.setSortingEnabled(False)

    def logText(self, text):
        self.LogField.append(">" + text)


    def logWarningText(self, text):
        self.LogField.append("<span style=\" font-size:8pt; font-weight:600; color:#ff0000;\" >"
                             + ">" + text + "</span>")

    def toggleShutter(self):
        try:
            Shutter.setMode(1)
            Shutter.setToggle()
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def shutUp(self, N, Topen, Tclose):
        Shutter.setMode(4)
        Shutter.setRepeat(N)
        Shutter.setOpenTime(Topen)
        Shutter.setCloseTime(Tclose)
        Shutter.setToggle()
        time.sleep(N * (Topen + Tclose)/1000)

    def __del__(self):
        try:
            Laser.close()
            Shutter.sc._file.close()
            apt._cleanup()
            print ("Cleared")
        except NameError:
            pass
        except:
            print(str(sys.exc_info()[1]))




def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    main = MainApp()
    main.show()
    app.exec()
    del(main)
    sys.exit()
    return main


if __name__ == '__main__':

    m = main()