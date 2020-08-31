from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sys

class Worker(QtCore.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):

        self.fn(*self.args, **self.kwargs)
        
class AbstractGui(QMainWindow):
    
    def __init__(self):
        self.threadpool = QtCore.QThreadPool()
        
        global Laser
        global Shutter
        global Motor
    
    def runThread(self, func):
        worker = Worker(func)
        self.threadpool.start(worker)
        
    
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
        
    def stagesToZerosClicked(self):
        try:
            self.interfaceBlock(True)
            Motor.set_velocity_parameters(0, 3.5, 4.5)

            Motor.move_home(True)
            self.logText('Stages moved to zeros')
            self.interfaceBlock(False)
        except:
            self.logWarningText(str(sys.exc_info()[1]))
            self.interfaceBlock(False)
            
    def stagesToHomeClicked(self):
        try:
            self.interfaceBlock(True)
#            Motor.backlash_distance(0)

            Motor.set_velocity_parameters(0, 3.5, 4.5)

            Home_value2 = 53

            Motor.move_to(Home_value2, True)
            self.logText('Stages moved to start position')
            self.interfaceBlock(False)
        except:
            self.logWarningText(str(sys.exc_info()[1]))
            self.interfaceBlock(False)
            
    def moveStagesClicked(self):
        try:
            self.interfaceBlock(True)
            Motor.set_velocity_parameters(0, 3.5, 4.5)
            Motor.move_by(float(self.MoveStagesField.text()), False)
            self.logText('Stages moved')
            self.interfaceBlock(False)
        except:
            self.logWarningText(str(sys.exc_info()[1]))
            self.interfaceBlock(False)