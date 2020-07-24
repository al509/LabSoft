DEBUG = False
import os
from serial import SerialException
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
import serial.tools.list_ports
import sys
from ui import MainWindow as ui
from libs import SynradLaser, SC10Shutter
import time
import threading



class Worker(QtCore.QRunnable):


    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):

        self.fn(*self.args, **self.kwargs)



class MainApp(QMainWindow, ui.Ui_MainWindow):
    def __init__(cls):


         QMainWindow.__init__(cls)
         ui.Ui_MainWindow.__init__(cls)

         cls.threadpool = QtCore.QThreadPool()
         cls.isNotStarted = threading.Event()
         cls.isNotStarted.set()

         global Laser
         global Shutter
         global Motor

         cls.timeToHeat = 30 # sec
         cls.motorDefaultSpeed = 5 ## mm/s


         cls.setupUi(cls)
         cls.setupBox()
         cls.setupButtons()
         cls.setupTable()

         worker1 = Worker(cls.setupMotor)
         cls.threadpool.start(worker1)
         worker2 = Worker(cls.autoDetectClicked)
         cls.threadpool.start(worker2)






    def setupBox(cls):
        cls.laserPortLineEdit.setVisible(False)
        cls.shutterPortLineEdit.setVisible(False)
        cls.manualConnectButton.setVisible(False)

    def setupButtons(cls):
        cls.manualConnectionBox.stateChanged.connect(cls.manualConnectionClicked)
        cls.AutoDetectButton.clicked.connect(cls.autoDetectClicked)
        cls.manualConnectButton.clicked.connect(cls.manualConnectClicked)
        cls.rowsApplyButton.clicked.connect(cls.rowsApplyClicked)
#        cls.rowNumberBox.valueChanged.connect(cls.rowsApplyClicked)
        cls.StagesToZerosButton.clicked.connect(cls.stagesToZerosClicked)
        cls.StagesToHomeButton.clicked.connect(cls.stagesToHomeClicked)
        cls.MoveStagesButton.clicked.connect(cls.moveStagesClicked)
        cls.startButton.clicked.connect(cls.startClicked)
        cls.fileButton.clicked.connect(cls.fileClicked)
        cls.startAnnealButton.clicked.connect(cls.startAnnealClicked)
        cls.toggleShutterButton.clicked.connect(cls.toggleShutter)
        cls.saveButton.clicked.connect(cls.saveConfig)
        cls.tableWidget.cellChanged.connect(cls.cellChangeHandler)

    def setupTable(cls):
        cls.tableWidget.setColumnCount(2)
        cls.tableWidget.setRowCount(12)
        cls.tableWidget.setHorizontalHeaderLabels(["Coordinate", "Number of shots"])

    def setupMotor(cls):
        global Motor 
        try:

             from libs import thorlabs_apt as apt
             Motor = apt.Motor(90864301)
             Motor.set_move_home_parameters(2, 1, 7.0, 0.0001)
             cls.logText("Motor initialized")
             cls.LogField.append("")
        except:
            cls.logWarningText("Motor not initialized :"+str(sys.exc_info()[1]))
            cls.LogField.append("")

    def rowsApplyClicked(cls):
        cls.tableWidget.setRowCount(cls.rowNumberBox.value())

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


    def fileClicked(cls):
        try:
            filepath = QFileDialog.getOpenFileName(cls, "Open File", "saves",
                                        "Impulse Maker savefile (*.ims)")[0]
        
            if filepath == "":
                cls.logText("File load aborted")
                return
            f = open(filepath, 'r')
            filename = filepath.split('/')[-1]
            
            num_lines = int(f.readline())
            cls.rowNumberBox.setValue(num_lines)
            cls.tableWidget.setRowCount(num_lines)
            
            params = f.readline().split()
            cls.powerSpinBox.setValue(float(params[0]))
            cls.openSpinBox.setValue(float(params[1]))
            cls.periodSpinBox.setValue(float(params[2]))
            
            params = f.readline().split() 
            cls.annealPowerBox.setValue(float(params[0]))
            cls.annealSpeedBox.setValue(float(params[1]))
            
            for i in range(0, num_lines):
                line = f.readline()
                columns = line.split()
                x_item = QTableWidgetItem(columns[0])
                n_item = QTableWidgetItem(columns[1])
                cls.tableWidget.setItem(i, 0, x_item)
                cls.tableWidget.setItem(i, 1, n_item)
                
            cls.logText("Successfully loaded configuration file " + filename)
        except:
             cls.logWarningText("File loading failed: "
                                 + str(sys.exc_info()[1]))
             
    def saveConfig(cls):
        try:
            filepath = QFileDialog.getSaveFileName(cls, "Open File", "saves",
                                        "Impulse Maker savefile (*.ims)")[0]
        
            if filepath == "":
                cls.logText("File save aborted")
                return
            f = open(filepath, 'w')
            filename = filepath.split('/')[-1]
            
            num_lines = cls.rowNumberBox.value()
            f.write(str(num_lines) + '\n')
            
            f.write(str(cls.powerSpinBox.value()) + " ")
            f.write(str(cls.openSpinBox.value()) + " ")
            f.write(str(cls.periodSpinBox.value()) + "\n")
            
            f.write(str(cls.annealPowerBox.value()) + " ")
            f.write(str(cls.annealSpeedBox.value()))
            
            
            for i in range(0, num_lines):
                x_item = cls.tableWidget.item(i, 0)
                n_item = cls.tableWidget.item(i, 1)
                f.write("\n" + x_item.text() + '\t' + n_item.text())
             
            f.close()
            cls.logText("Successfully saved configuration file " + filename)
        except AttributeError:
            cls.logWarningText("File saving failed: incorrect number of rows."
                               + " Make sure that all rows filled")
            f.close()
        except:
             cls.logWarningText("File saving failed: "
                                 + str(sys.exc_info()[1]))
             f.close()
    
    def startAnnealClicked(cls):
        try:
            worker = Worker(cls.startAnneal)
            cls.threadpool.start(worker)
        except:
            cls.logWarningText(str(sys.exc_info()[1]))

    def startAnneal(cls):
        try:
            cls.logText("Anneal started")
            cls.startAnnealButton.setEnabled(False)
            start_pos = 53
            end_pos = 75
            Laser. setPower(cls.annealPowerBox.value())
            Shutter.setMode(1)
            if Shutter.getToggle() == "1":
                Shutter.setToggle()

            cls.logText("Moving to start position")
            Motor.set_velocity_parameters(0, 10, cls.motorDefaultSpeed)
            Motor.move_to(start_pos, True)
            Motor.set_velocity_parameters(0, 10, cls.annealSpeedBox.value())

            Laser.setOn()
            cls.logText("Starting to burn")
            Shutter.setToggle()
            Motor.move_to(end_pos, True)
            Shutter.setToggle()
            Laser.setOff()
            cls.logText("Anneal finished")
            cls.startAnnealButton.setEnabled(True)


        except:
            try:
                Laser.setOff()
            except:
                pass
            cls.logWarningText("Process failed: "+ str(sys.exc_info()[1]))
            cls.startAnnealButton.setEnabled(True)


    def start(cls):
        try:
            power = cls.powerSpinBox.value()
            Topen = cls.openSpinBox.value()
            Tperiod = cls.periodSpinBox.value()
            cls.isNotStarted.clear()

            Laser.setPower(power)

            Shutter.setMode(1)
            if Shutter.getToggle() == "1":
                Shutter.setToggle()
            Laser.setOn()
            cls.logText("Heating laser")

            cls.isNotStarted.wait(cls.timeToHeat)
            if cls.isNotStarted.isSet():
                Laser.setOff()
                cls.logWarningText("Interrupted")
                return
            cls.logText("Laser heated. Starting process")

            for i in range(0, cls.rowNumberBox.value()):

                x_item = cls.tableWidget.item(i, 0)
                n_item = cls.tableWidget.item(i, 1)
                x = (float(x_item.text()))
                n = (int(n_item.text()))
                cls.logText("Processing coordinate "
                             + str(x) + " with " + str(n) + " times")

                Motor.move_to(x, True)
                if cls.isNotStarted.isSet():
                    Laser.setOff()
                    cls.logWarningText("Interrupted")
                    return

                cls.shutUp(n, Topen, Tperiod - Topen)

            Laser.setOff()
            cls.logText("Completed")
            cls.isNotStarted.set()
        except AttributeError:
            cls.logWarningText("Looks like there are empty values" +
                               "in coordinates list. Process stopped.")
            Laser.setOff()
            cls.isNotStarted.set()
        except:
            cls.logWarningText("Process failed: "+ str(sys.exc_info()[1]))
            cls.isNotStarted.set()
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
        if collumn == 0:
            pass


    def logText(self, text):
        self.LogField.append(">" + text)


    def logWarningText(self, text):
        self.LogField.append("<span style=\" font-size:8pt; font-weight:600; color:#ff0000;\" >"
                             + ">" + text + "</span>")

    def toggleShutter(cls):
        try:
            Shutter.setMode(1)
            Shutter.setToggle()
        except:
            cls.logWarningText(str(sys.exc_info()[1]))

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