"""Module that allows to operate Thorllabs SC10 shutter controller.

This module is a wrapper for convenient use of Thorlabs SC10 Shutter module.
It has all documented SC10 functions according to it's manual and
docmentation for them. More detailed info about this shutter can be found in
program's libs folder.
For work "instrumentkit" module required. It can be installed from pip.


How to use this modude (examples):
    >>>import SC10Shutter
    >>>Shut = SC10Shutter.Shutter('COM10') # connect to serial port
    ...
    >>>Shut.setRepeat(20) # set repeat count to 20
    >>>print(Shut.getRepeat()) # should be '20'
    ...
    >>>Shut.setToggle() # turn the shutter on
    ...
    >>>Shut.saveConf() # save configs to EEPROM

"""

import instruments as ik

class Shutter:
    """
    Object used to control SC10 shutter.

    Parameters
    ----------
    **sc:** Serial
        Serial port connection pointer to shutter.

    Methods (for further information see method's docstrings):
    -------
    getID() - Get ID.\n
    setToggle() - Toggle enable.\n
    getToggle() - Get enable.\n
    setRepeat(n:0..99) - Set repeat count.\n
    getRepeat() - Get repeat count.\n
    setMode(n:1..5) -  Set operating mode.\n
    getMode() - Get operating mode.\n
    setTrig(0..1) - Set trigger mode.\n
    getTrig() - Get trigger mode.\n
    setExTrig(n:0..1) - Set ex-trigger mode.\n
    getExTrig() - Get ex-trigger mode.\n
    setOpenTime(n:0..999999) - Set open duration.\n
    getOpenTime() - Get open duration.\n
    setCloseTime(n:0..999999) -  Set close duration.\n
    getCloseTime() - Set close duration.\n
    getInterlock() - Get Interlock tripped.\n
    setBaudRate(n:0..1) - Set baud rate.\n
    getBaudRate() - Get baud rate.\n
    saveMode() - Save mode information.\n
    saveConf() - Store configuration.\n
    loadConf() - Load configuration.\n
    """
    def __init__(self, ShutterCOMPort:str=None):
        """
        Iinitialize shutter object.

        Parameters
        ----------
        **ShutterCOMPort:**
            Shutter serial port (usually it's 'COMx' where x is some number.
            In Windows you can see it in the device manager.)

        """

        self.sc = ik.thorlabs.SC10.open_serial(ShutterCOMPort, 9600, timeout=0.2)

    def getID(self) -> str:
        """Return the model number and firmware revision."""
        return self.sc.query("id?")

    def setToggle(self):
        """Enable/Disable the shutter."""
        self.sc.sendcmd("ens")

    def getToggle(self) -> str:
        """Return “0” if the shutter is disabled (closed) and “1” if enabled (opened)."""
        return self.sc.query("ens?")

    def setRepeat(self, n:int):
        """
        Set repeat count.

        Parameters:
        -----------
        **n:** Set repeat count n for repeat mode.
            The value *n* must be from 1 to 99.
        """
        self.sc.sendcmd("rep="+str(n))

    def getRepeat(self) -> str:
        """Return the repeat count."""
        return self.sc.query("rep?")

    def setMode(self, mode:int):
        """
        Set operating mode.

        Parameters:
        -----------
        **mode:** equals an associated mode —
            *mode=1*: Sets the unit to Manual Mode;\n
            *mode=2:* Sets the unit to Auto Mode;\n
            *mode=3:* Sets the unit to Single Mode;\n
            *mode=4:* Sets the unit to Repeat Mode;\n
            *mode=5:* Sets the unit to the External Gate Mode.\n
        """
        self.sc.sendcmd("mode="+str(mode))

    def getMode(self) -> str:
        """Return the operating mode value."""
        return self.sc.query("mode?")

    def setTrig(self, trig: int):
        """
        Set trigger mode.

        Parameters:
        -------
        **trig** : denotes trigger mode (see user manual for more details) —
            *trig=0:* Internal trigger mode\n
            *trig=1:* External trigger mode.\n
        """
        self.sc.sendcmd("trig="+str(trig))

    def getTrig(self) -> str:
        """Return the trigger mode."""
        return self.sc.query("trig?")

    def setExTrig(self, xto: int):
        """
        Set ex-trigger mode.

        Parameters:
        -----------
        **xto:** denotes ex-trigger mode —
            *xto=0:* Trigger Out TTL follows shutter output.\n
            *xto=1:* Trigger Out TTL follows controller output.\n
        """
        self.sc.sendcmd("xto="+str(xto))

    def getExTrig(self) -> str: # В каком виде возращается?
        """Returns the ex-trigger mode."""
        return self.sc.query("xto?")

    def setOpenTime(self, n: int):
        """
        Set open duration.

        Prameters:
        ----------
        **n:** Set the shutter open time in ms.
            The value *n* must have 6 digits or less.
        """
        self.sc.sendcmd("open="+str(n))

    def getOpenTime(self) -> str:
        """Return the shutter close time in ms."""
        return self.sc.query("open?")

    def setCloseTime(self, n: int):
        """
        Set close duration.

        Parameters:
        -----------
        **n:** Set the shutter close time in ms.
            The value *n* must have 6 digits or less.
        """
        self.sc.sendcmd("shut="+str(n))

    def getCloseTime(self) -> str:
        """Return the shutter close time in ms."""
        return self.sc.query("shut?")

    def getInterlock(self) -> str:
        """Return “1” if interlock is tripped, otherwise “0”."""
        return self.sc.query("interlock?")

    def setBaudRate(self, baud: int):
        """
        Set baud rate.

        Parameters:
        -------
        **baud:** denotes option for baud rate —\n
            *baud=0:* Sets the SC10 serial baud rate to 9.6 K;\n
            *baud=1:* Sets the SC10 serial baud rate to 115 K.\n
        """
        self.sc.sendcmd("baud="+str(baud))

    def getBaudRate(self) -> str:
      """Returns “0” for 9.6 K or “1” for 115 K"""
      return self.sc.query("baud?")

    def saveMode(self):
        """Save baud rate and output trigger mode."""
        self.sc.sendcmd("save")

    def saveConf(self):
        """
        Store configuration.

        Save current settings (ex. mode, open time, closed time)
        into EEPROM.
        """
        self.sc.sendcmd("savp")

    def loadConf(self):
        """Load settings from EEPROM."""
        self.sc.sendcmd("resp")