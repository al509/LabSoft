# добавить остальные функции
import serial
import winsound
import time

frequency = 750  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second


class Laser(serial.Serial):
    def __init__(self,COMPort):
        super().__init__(port=COMPort,
             baudrate=9600,
             parity=serial.PARITY_NONE,
             stopbits=serial.STOPBITS_ONE,
             bytesize=serial.EIGHTBITS,
             timeout = 0.4)
        self.pause=0.01
        self.repeat=0.1
        self. maxAttempts = 10;
        self.setMode('MANCLOSED')

    def writeP(self, byte):
        time.sleep(self.pause)
        self.write(byte)

    def readP(self):
        time.sleep(self.pause)
        return self.read(1)

    def checkACK(self):
        time.sleep(self.pause)
        ack = self.read(1)
        if ack == b'\xAA':
            return True
        elif ack == b'\x3F':
            return False
        else:
            raise ValueError("ValueError: Inappropriate acknowledge value: " + str(ack))

    def getStatus(self):
        stat = []
        self.writeP(b'\x7E')
        self.checkACK()
        for i in range(0,5):
            stat.append(self.readP())
#        print (stat)
        return stat


    def setOn(self):
        winsound.Beep(frequency, duration)
        attempt = 0
        print('Turning on laser')
        while True:
            attempt+=1
            self.writeP(b'\x5B')
            self.writeP(b'\x75')
            self.writeP(b'\x8A')
            time.sleep(self.repeat)
            if self.checkACK():
                print('Laser is on (',attempt,')')
                break
            if attempt == self.maxAttempts:
                print('WARNING!!! Could not set the laser on; PLEASE TURN OFF THE LASER MANUALLY')
                break
            time.sleep(self.repeat)

    def setOff(self):
        winsound.Beep(frequency*2, duration)
        attempt = 0
        print('Turning off laser')
        while True:
            attempt+=1
            self.writeP(b'\x5B')
            self.writeP(b'\x76')
            self.writeP(b'\x89')
            if self.checkACK():
                print('Laser is off (', attempt, ')')
                break
            if attempt == self.maxAttempts:
                print('WARNING!!! COULD NOT TURN THE LASER OFF; PLEASE TURN OFF MANUALLY')
                break
            time.sleep(self.repeat)


    def setOnForShort(self,PulseDuration):
        self.SetOn()
        time.sleep(PulseDuration)
        self.SetOff()
        print('Laser pulse was applied')

    def setMode(self,ModeKey):
        ModeKeys={
                'Manual':0x70,
                'ANC':0x71,
                'ANV':0x72,
                'MANCLOSED':0x73,
                'ANVCLOSED':0x74}

        Command=ModeKeys[ModeKey]
        CheckSumCommand=(255-int(Command))
        attempt = 0
        print('Changing mode of laser')
        while True:
            attempt+=1
            self.writeP(b'\x5B')
            self.writeP(Command.to_bytes(1,byteorder='big'))
            self.writeP(CheckSumCommand.to_bytes(1,byteorder='big'))
            if self.checkACK():
                print('Laser operation mode changed ( ', attempt, ')')
                break
            if attempt == self.maxAttempts:
                print('WARNING!!! COULD NOT CHANGE THE STATE; PLEASE TURN OFF THE LASER MANUALLY')
                break
            time.sleep(self.repeat)

    def setPower(self,Power):


        Command = int(Power*2)
        attempt = 0
        print('Setting power of laser')
        while True:
            attempt+=1
            CheckSumCommand=(255-(0x7F + Command) & (2**8 - 1))
            self.writeP(b'\x5B')
            self.writeP(b'\x7F')
            self.writeP(Command.to_bytes(1,byteorder='big'))
            self.writeP(CheckSumCommand.to_bytes(1,byteorder='big'))
            if self.checkACK():
                print('Laser power is set to ',Power, '% (', attempt, ')')
                break
            if attempt == self.maxAttempts:
                print('WARNING!!! COULD NOT CHANGE THE POWER; PLEASE TURN OFF THE LASER MANUALLY')
                break
            time.sleep(self.repeat)