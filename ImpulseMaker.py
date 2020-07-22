DEBUG = False
from serial import SerialException
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import serial.tools.list_ports
import sys
from ui import MainWindow as ui
from libs import SynradLaser, SC10Shutter
import time



class MainApp(QMainWindow, ui.Ui_MainWindow):
    def __init__(cls):
         QMainWindow.__init__(cls)
         ui.Ui_MainWindow.__init__(cls)

         cls.setupUi(cls)
         cls.setupBox()
         cls.setupButtons()
         cls.setupTable()
         cls.setupMotor()

         cls.autoDetectClicked()

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
        cls.startButton.clicked.connect(cls.start)
        cls.fileButton.clicked.connect(cls.fileClicked)
        cls.startAnnealButton.clicked.connect(cls.startAnneal)

    def setupTable(cls):
        cls.tableWidget.setColumnCount(2)
        cls.tableWidget.setRowCount(12)
        cls.tableWidget.setHorizontalHeaderLabels(["Coordinate", "Number of shots"])

    def setupMotor(cls):
         try:
             global motor1
             global motor2

             from libs import thorlabs_apt as apt
             motor1 = apt.Motor(90864300)
             motor2 = apt.Motor(90864301)
             motor1.set_move_home_parameters(2, 1, 7.0, 0.0001)
             motor2.set_move_home_parameters(2, 1, 7.0, 0.0001)
             if DEBUG:
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

            motor1.set_velocity_parameters(0, 3.5, 4.5)
            motor2.set_velocity_parameters(0, 3.5, 4.5)

            motor1.move_home(False)
            motor2.move_home(True)
            self.logText('Stages moved to zeros')
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def stagesToHomeClicked(self):
        try:
            motor1.backlash_distance(0)
            motor2.backlash_distance(0)

            motor1.set_velocity_parameters(0, 3.5, 4.5)
            motor2.set_velocity_parameters(0, 3.5, 4.5)

            Home_value1 = 95
            Home_value2 = 30

            motor1.move_to(Home_value1, False)
            motor2.move_to(Home_value2, True)
            self.logText('Stages moved to start position')
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def moveStagesClicked(self):
        try:
            motor1.set_velocity_parameters(0, 3.5, 4.5)
            motor2.set_velocity_parameters(0, 3.5, 4.5)
            motor1.move_by(-1*float(self.ui.MoveStagesField.text()), False)
            motor2.move_by(float(self.ui.MoveStagesField.text()), False)
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
        num_lines = sum(1 for line in open('setup'))
        cls.rowNumberBox.setValue(num_lines)
        cls.tableWidget.setRowCount(num_lines)

        i = 0
        f = open('setup', 'r')
        for line in f:
            line = line.strip()
            columns = line.split()
            x_item = QTableWidgetItem(columns[0])
            n_item = QTableWidgetItem(columns[1])
            cls.tableWidget.setItem(i, 0, x_item)
            cls.tableWidget.setItem(i, 1, n_item)
            i+=1
            
    def startAnneal(cls):
        try:
            cls.logText("Anneal started")
            start_pos = 55
            end_pos = 75
            timeToHeat = 30
            motor = motor2
            
            motor.set_velocity_parameters(0, 10, cls.annealValueBox.value())
            Laser. setPower(cls.doubleSpinBox.value())
            Shutter.setMode(3)
            if Shutter.getToggle == "1":
                Shutter.setToggle()
            
            cls.logText("Moving to start position")
            motor.move_to(start_pos, True)
            Laser.setOn()  
            cls.logText("Heating laser")
            time.sleep(timeToHeat)
            cls.logText("Laser heated. Starting to burn")
            Shutter.setToggle()
            motor.move_to(end_pos, True)
            Shutter.setToggle()
            Laser.setOff()
            cls.logText("Anneal finished")
        except:
            try:
                Laser.setOff()
            except:
                pass
            cls.logWarningText("Process failed: "+ str(sys.exc_info()[1]))
        

    def startAnneal(cls):
        try:
            cls.logText("Anneal started")
            start_pos = 55
            end_pos = 75
            timeToHeat = 30
            motor = motor2

            motor.set_velocity_parameters(0, 10, cls.annealValueBox.value())
            Laser. setPower(cls.doubleSpinBox.value())
            Shutter.setMode(3)
            if Shutter.getToggle == "1":
                Shutter.setToggle()

            cls.logText("Moving to start position")
            motor.move_to(start_pos, True)
            Laser.setOn()
            cls.logText("Heating laser")
            time.sleep(timeToHeat)
            cls.logText("Laser heated. Starting to burn")
            Shutter.setToggle()
            motor.move_to(end_pos, True)
            Shutter.setToggle()
            Laser.setOff()
            cls.logText("Anneal finished")
        except:
            try:
                Laser.setOff()
            except:
                pass
            cls.logWarningText("Process failed: "+ str(sys.exc_info()[1]))


    def start(self):
        try:
            motor = motor2

            power = self.powerSpinBox.value()
            Topen = self.openSpinBox.value()
            Tperiod = self.periodSpinBox.value()

            Laser.setPower(power)
            Laser.setOn()
            for i in range(0, self.rowNumberBox.value()):


                x_item = self.tableWidget.item(i, 0)
                n_item = self.tableWidget.item(i, 1)
                x = (float(x_item.text()))
                n = (int(n_item.text()))
                self.logText("Processing coordinate "
                             + str(x) + " with " + str(n) + " times")

                motor.move_to(x, True)
                self.shutUp(n, Topen, Tperiod - Topen)

            Laser.setOff()
            self.logText("Completed")
        except:
            self.logWarningText("Process failed: "+ str(sys.exc_info()[1]))

            try:
                Laser.setOff()
            except:
                pass

    def logText(self, text):
        self.LogField.append(">" + text)


    def logWarningText(self, text):
        self.LogField.append("<span style=\" font-size:8pt; font-weight:600; color:#ff0000;\" >"
                             + ">" + text + "</span>")


    def __del__(self):
        try:
            Laser.close()
            Shutter.sc._file.close()
        except NameError:
            pass
        except:
            print(str(sys.exc_info()[1]))

    def shutUp(self, N, Topen, Tclose):
        Shutter.setMode(4)
        Shutter.setRepeat(N)
        Shutter.setOpenTime(Topen)
        Shutter.setCloseTime(Tclose)
        Shutter.setToggle()
        time.sleep(N * (Topen + Tclose)/1000)

def main():

    app = QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()