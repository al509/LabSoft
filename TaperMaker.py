from PyQt5 import QtCore, QtWidgets


import sys
import numpy as np
import threading
import winsound
from ui import TM as ui
import json
import math
import time
from common.Common import Worker, CommonClass
from packaging import version
from conda import __version__ as condaVersion

_version_='Test 2.14'
_date_='18.06.21'

class MainApp(CommonClass, ui.Ui_MainWindow):
    def __init__(self):
        CommonClass.__init__(self)
        ui.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("TaperMaker V. "+_version_+', date  ' + _date_)
        
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
        
        self.Home_value1 = 95
        self.Home_value2 = 30

        self.ParametersFileName="Parameters_standard.txt"

        self.setupButtons()
        self.setupBox()
        
        self.worker1 = Worker(self.stagesButtonClicked)
        self.threadpool.start(self.worker1)
        self.threadpool.start(self.worker2)
        
        try:
            if self.Shutter.getToggle()=='1':
                self.OpenShutter.setChecked(True)
        except: pass 
        
    def calculateStageSpeed(self,delta_S,aver_S,t_1):
        S_1=aver_S-delta_S/2
        S_11=1*S_1/100 # way with acceleration
        S_12=99*S_1/100 # way without acceleration

        S_2=aver_S+delta_S/2
        S_21=1*S_2/100 # way with acceleration
        #S_22=95*S_2/100 # way without acceleration

        # I suppose part of the way with the accelerate is smaller than part of the way without accelerate
        V_1=S_12/t_1
        a_1=(V_1*V_1)/(2*S_11) #at now the accelerate is agreed with constant speed
        t_a=np.sqrt(2*S_11/a_1) # found time to accelerate    
        #at now find a_2 
        a_2 = 2*S_21/(t_a*t_a) #at now the accelerate is agreed with accelerate time
        V_2 = a_2*t_a #at now the speed is agreed with acceleration
        S_22= V_2*t_1
        S_2=S_22+S_21
        return a_1,V_1,S_1, a_2,V_2,S_2
        
        
    def setupButtons(self):
        ########## Button conections ##########
        self.StagesToZerosButton.clicked.connect(self.stagesToZerosClicked)
        self.StagesToHomeButton.clicked.connect(self.stagesToHomeClicked)
        self.MoveStagesButton.clicked.connect(self.moveStagesClicked)
        self.StartStopButton.clicked.connect(self.startStopButtonClicked)
        self.StretchButton.clicked.connect(self.stretchButtonClicked)
        self.FileBox.clicked.connect(self.fileBoxClicked)
        self.TurnLaserOnButton.clicked.connect(self.TurnLaserOnClicked)
        self.MoveOutButton.clicked.connect(self.moveOutClicked)
        self.OpenShutter.clicked.connect(self.OpenShutterClicked)

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



            motor1.move_to(self.Home_value1, False)
            motor2.move_to(self.Home_value2, True)
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
                
            self.stretchButtonClickedN = 0
            if len(self.PowerArray)<(int(self.NumberOfCyclesField.text())*2):
                self.logText("Number of cycles is larger than powers specified in the Parameters files")
                return
            self.isNotStarted.clear()
            self.Laser.setPower(self.PowerArray[0])
            self.logText("Laser taper making started")
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
                motor1.set_velocity_parameters(0, self.a1, self.v1)
                motor2.set_velocity_parameters(0, self.a2, self.v2)
                motor1.move_by(-self.s1, False)
                motor2.move_by(self.s2, True)
                time.sleep(self.t_stop)
                if self.isNotStarted.isSet():
                    self.Laser.setOff()
                    self.isNotStarted.set()
                    self.NumberOfCycleField.setText("Interrupted")
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
            self.ParametersFileName = fname
            self.logText("Opened: " + fname)
            with open(self.ParametersFileName,'r') as f:
                Dict=json.load(f)
                self.Home_value1,self.Home_value2,number_of_cycles,delta_S, aver_S, t_1,self.PowerArray =Dict['left_stage_home'],Dict['right_stage_home'],Dict['number_of_cycles'],Dict['delta_S'],Dict['aver_S'],Dict['t_1'],np.array(Dict['PowerArray'])
                self.logText('Loaded: '+ str(Dict))
            self.NumberOfCyclesField.setText(str(number_of_cycles))
            self.a2,self.v2,self.s2,self.a1,self.v1,self.s1=self.calculateStageSpeed(delta_S, aver_S, t_1)
            #Аркадий здесь поменял местами индексы, так как в калкуляторе нарушено соответсвие, что первому индексу соответсвует большая скорость
        except:
            self.logWarningText(str(sys.exc_info()[1]))


    def LaserForTestClicked(self):
        try:
            self.Laser.setPower(10)
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def TurnLaserOnClicked(self):
        try:
            if self.isChecking == True:
                self.Laser.setOff()
                self.logText("Laser turned off")
                self.isChecking = False
                self.TurnLaserOnButton.setChecked(False)
                #self.Laser.setPower()
            else:
                self.Laser.setPower(int(self.LaserPower.text()))
                time.sleep(0.1)
                self.Laser.setOn()
                self.logText("Laser set on")
                self.isChecking = True
                self.TurnLaserOnButton.setChecked(True)
        except:
            self.logWarningText(str(sys.exc_info()[1]))

    def moveOutClicked(self):
        try:
            motor1.set_velocity_parameters(0, 1.0, 0.3)
            motor2.set_velocity_parameters(0, 1.0, 0.3)
            distanceToMove=min(motor1.position-2,(100-motor2.position)-2)
            motor1.move_by(-distanceToMove, False)
            motor2.move_by(distanceToMove, True)
            self.logText('Stages moved out')
        except:
            self.logWarningText(str(sys.exc_info()[1]))
            
    def OpenShutterClicked(self):
        if self.Shutter.getToggle() == "0":
            self.Shutter.setToggle()
            self.OpenShutter.setChecked(True)
        else:
            self.Shutter.setToggle()
            self.OpenShutter.setChecked(False)

# def main():

#     return main


if __name__ == '__main__':
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
             
    
    main = MainApp()
    main.show()
    if (version.parse(condaVersion) > version.parse("4.9.0")):
        sys.exit(app.exec())