##########
## V.2
##########
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


from libs import SynradLaser
import sys
import numpy as np
import threading
import winsound
from ui import TM as ui
import math
import time
from common.Common import Worker, CommonClass
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem



class MainApp(CommonClass, ui.Ui_MainWindow):
    def __init__(self):
        CommonClass.__init__(self)
        ui.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.isNotStarted = threading.Event()
        self.isNotStarted.set()
        self.isChecking = False

        self.timeToHeatUpTube=10 # seconds, calculated by Daria

        self.frequency = 1500  # Set Frequency To 2500 Hertz
        self.duration = 1500  # Set Duration To 1000 ms == 1 second
    


        self.v1 = 0.32
        self.v2 = 0.24
        self.a1 = 2.0
        self.a2 = 1.5
        self.s1 = 4 ## mm
        self.s2 = 3 ## mm
        self.t_stop = 0.12
        self.stretchButtonClickedN = 0

        self.LaserPowerListName="Laser Power Script.txt"

        self.setupButtons()
        self.setupBox()
        
        self.worker1 = Worker(self.stagesButtonClicked)
        self.threadpool.start(self.worker1)
        self.threadpool.start(self.worker2)
        
        
        
    def setupButtons(self):
        ########## Button conections ##########
        # self.ConnectionLaserButton.clicked.connect(self.laserButtonClicked)
        # self.ConnectionStagesButton.clicked.connect(self.stagesButtonClicked)
        self.StagesToZerosButton.clicked.connect(self.stagesToZerosClicked)
        self.StagesToHomeButton.clicked.connect(self.stagesToHomeClicked)
        self.MoveStagesButton.clicked.connect(self.moveStagesClicked)
        self.StartStopButton.clicked.connect(self.startStopButtonClicked)
        self.StretchButton.clicked.connect(self.stretchButtonClicked)
        self.FileBox.clicked.connect(self.fileBoxClicked)
        self.SetToTenButton.clicked.connect(self.SetToTenClicked)
        self.MoveOutButton.clicked.connect(self.moveOutClicked)

        self.MoveLeftStageLeftButton.clicked.connect(lambda :self.moveSingleStage(motor1,-float(self.MoveLeftStageField.text())))
        self.MoveLeftStageRightButton.clicked.connect(lambda :self.moveSingleStage(motor1,float(self.MoveLeftStageField.text())))
        self.MoveRightStageLeftButton.clicked.connect(lambda :self.moveSingleStage(motor2,float(self.MoveRightStageField.text())))
        self.MoveRightStageRightButton.clicked.connect(lambda :self.moveSingleStage(motor2,-float(self.MoveRightStageField.text())))
        
        self.manualConnectionBox.stateChanged.connect(self.manualConnectionClicked)
        self.AutoDetectButton.clicked.connect(self.autoDetectClicked)
        self.manualConnectButton.clicked.connect(self.manualConnectClicked)
        #######################################


    def manualConnectionClicked(self):
        if self.manualConnectionBox.isChecked() == True:
            self.laserPortLineEdit.setVisible(True)
            self.shutterPortLineEdit.setVisible(True)
            self.manualConnectButton.setVisible(True)
            self.AutoDetectButton.setEnabled(False)
            self.ConnectionBox.setGeometry(QtCore.QRect(50, 10, 211, 161))
        else:
            self.laserPortLineEdit.setVisible(False)
            self.shutterPortLineEdit.setVisible(False)
            self.manualConnectButton.setVisible(False)
            self.AutoDetectButton.setEnabled(True)
            self.ConnectionBox.setGeometry(QtCore.QRect(50, 40, 211, 121))


    def laserButtonClicked(self):
        try:
            Laser=SynradLaser.Laser("COM" + self.PortField.text())
            self.logText('The laser was connected')
            # номер COM  порта
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def stagesButtonClicked(self):
        global motor1
        global motor2
        from libs import thorlabs_apt as apt
        try:
            motor1 = apt.Motor(90864300)
            motor2 = apt.Motor(90864301)
            motor1.set_move_home_parameters(2, 1, 7.0, 0.0001)
            motor2.set_move_home_parameters(2, 1, 7.0, 0.0001)
            self.logText('Stages connected successfully')
        except:
            self.logWarningText(str(sys.exc_info()[1]))

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
            motor1.move_by(-1*float(self.MoveStagesField.text()), False)
            motor2.move_by(float(self.MoveStagesField.text()), False)
            self.logText('Stages moved')
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def moveSingleStage(self,motor,distance):
        try:
            motor.set_velocity_parameters(0, 3.5, 4.5)
            motor.move_by(distance, True)
            self.logText('Stage moved')
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def start(self):
        try:
            self.Shutter.setMode(1)
            if self.Shutter.getToggle() == "0":
                self.Shutter.setToggle()
            self.Laser.setOn()

            
            self.stretchButtonClickedN = 0
            self.logText("Laser taper making started")
            self.PowerArray=np.array(np.loadtxt(self.LaserPowerListName)[:,1])
            self.isNotStarted.clear()
            self.Laser.setPower(self.PowerArray[0])
            self.Laser.setOn()
            self.NumberOfCycleField.setText("Heating up the tube")
            self.isNotStarted.wait(self.timeToHeatUpTube)
            if self.isNotStarted.isSet():
                self.Laser.setOff()
                self.isNotStarted.set()
                self.NumberOfCycleField.setText("Interrupted")
                self.logWarningText("Interrupted")
                return
            i = 1
            while(i <= int(self.NumberOfCyclesField.text()) * 2):
                self.Laser.setPower(self.PowerArray[i-1])
                self.NumberOfCycleField.setText(str(math.floor(i/ 2 + 1)))
#                if (i>int(self.NumberOfCyclesField.text())*2 - 4): winsound.Beep(self.frequency, self.duration)
                motor1.set_velocity_parameters(0, self.a1, self.v1)
                motor2.set_velocity_parameters(0, self.a2, self.v2)
                motor1.move_by(-self.s1, False)
                motor2.move_by(self.s2, True)
                time.sleep(self.t_stop)
                if self.isNotStarted.isSet():
                    self.Laser.setOff()
                    self.isNotStarted.set()
                    self.isNotStartedNumberOfCycleField.setText("Interrupted")
                    self.logWarningText("Interrupted")
                    return
                self.NumberOfCycleField.setText(str(math.floor(i/ 2 + 1)) + " half")
                i+=1
                self.Laser.setPower(self.PowerArray[i-1])
                motor1.set_velocity_parameters(0, self.a2, self.v2)
                motor2.set_velocity_parameters(0, self.a1, self.v1)
                motor1.move_by(self.s2, False)
                motor2.move_by(-self.s1, True)
                time.sleep(self.t_stop)
                if self.isNotStarted.isSet():
                    self.Laser.setOff()
                    self.NumberOfCycleField.setText("Interrupted")
                    self.logWarningText("Interrupted")
                    return
                i += 1
            self.Laser.setOff()
            self.NumberOfCycleField.setText("Completed")
            self.logText("Completed")
            self.isNotStarted.set()
            winsound.Beep(self.frequency, 2*self.duration)

        except:
            self.logWarningText(str(sys.exc_info()[1]))
            self.Laser.setOff()
            return

    def startStopButtonClicked(self):
        try:
            if self.isNotStarted.isSet() == False:
                self.isNotStarted.set()
                return

            else:
                worker = Worker(self.start)
                self.threadpool.start(worker)
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def stretchButtonClicked(self):
         try:
            motor1.move_by(-0.01,True)
            self.stretchButtonClickedN += 1
            self.logText('Stretched (' + str(self.stretchButtonClickedN) + ' time(s))')
         except:
            self.logWarningText(str(sys.exc_info()[1]))

    def fileBoxClicked(self):
        try:
            fname = QtWidgets.QFileDialog().getOpenFileName()[0]
            self.LaserPowerListName = fname
            self.logText("Opened: " + fname)
        except:
            self.logWarningText(str(sys.exc_info()[1]))


    def LaserForTestClicked(self):
        try:
            self.Laser.setPower(10)
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def SetToTenClicked(self):
        try:
            if self.isChecking == True:
                self.Laser.setOff()
                self.logText("Laser turned off")
                self.isChecking = False
                self.Laser.setPower(10)
            else:
                self.Laser.setOn()
                self.logText("Laser set to 10%")
                self.isChecking = True
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def moveOutClicked(self):
        try:
            motor1.set_velocity_parameters(0, 1.0, 0.3)
            motor2.set_velocity_parameters(0, 1.0, 0.3)
            motor1.move_by(-1*70, False)
            motor2.move_by(70, True)
            self.logText('Stages moved out')
        except:
            self.logWarningText(str(sys.exc_info()[1]))


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