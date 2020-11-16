DEBUG = False
from PyQt5 import QtCore, QtWidgets
from serial import SerialException
from PyQt5.QtWidgets import QMainWindow
import sys
from libs import SynradLaser, SC10Shutter
import serial.tools.list_ports

class Worker(QtCore.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self):

        self.fn(*self.args, **self.kwargs)
        
class CommonClass(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.threadpool = QtCore.QThreadPool()
        
        self.timeToHeat = 30 # sec
        self.motorDefaultSpeed = 5 ## mm/s
        
        self.worker1 = Worker(self.setupMotor)
        self.worker2 = Worker(self.autoDetectClicked)
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
 # Закончил тут 
        
  
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



    def logText(self, text):
           self.LogField.append(">" + text)


    def logWarningText(self, text):
            self.LogField.append("<span style=\" font-size:8pt; font-weight:600; color:#ff0000;\" >"
                                 + ">" + text + "</span>")