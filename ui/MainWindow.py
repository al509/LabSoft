# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Александр\Desktop\work\6. Impulse maker\ImpulseMaker\ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ConnectionBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ConnectionBox.setGeometry(QtCore.QRect(10, 20, 211, 121))
        self.ConnectionBox.setObjectName("ConnectionBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.ConnectionBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 19, 181, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.ConnectionLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.ConnectionLayout.setContentsMargins(0, 0, 0, 0)
        self.ConnectionLayout.setObjectName("ConnectionLayout")
        self.AutoDetectButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.AutoDetectButton.setEnabled(True)
        self.AutoDetectButton.setObjectName("AutoDetectButton")
        self.ConnectionLayout.addWidget(self.AutoDetectButton)
        self.ManualConnectionLayout = QtWidgets.QFormLayout()
        self.ManualConnectionLayout.setVerticalSpacing(6)
        self.ManualConnectionLayout.setObjectName("ManualConnectionLayout")
        self.manualConnectionBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.manualConnectionBox.setChecked(False)
        self.manualConnectionBox.setObjectName("manualConnectionBox")
        self.ManualConnectionLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.manualConnectionBox)
        self.laserPortLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.laserPortLabel.setObjectName("laserPortLabel")
        self.ManualConnectionLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.laserPortLabel)
        self.laserPortLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.laserPortLineEdit.setEnabled(True)
        self.laserPortLineEdit.setClearButtonEnabled(False)
        self.laserPortLineEdit.setObjectName("laserPortLineEdit")
        self.ManualConnectionLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.laserPortLineEdit)
        self.shutterPortLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.shutterPortLabel.setObjectName("shutterPortLabel")
        self.ManualConnectionLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.shutterPortLabel)
        self.shutterPortLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.shutterPortLineEdit.setEnabled(True)
        self.shutterPortLineEdit.setObjectName("shutterPortLineEdit")
        self.ManualConnectionLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.shutterPortLineEdit)
        self.manualConnectButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.manualConnectButton.setObjectName("manualConnectButton")
        self.ManualConnectionLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.manualConnectButton)
        self.ConnectionLayout.addLayout(self.ManualConnectionLayout)
        self.LogBox = QtWidgets.QGroupBox(self.centralwidget)
        self.LogBox.setGeometry(QtCore.QRect(10, 440, 771, 131))
        self.LogBox.setObjectName("LogBox")
        self.LogField = QtWidgets.QTextBrowser(self.LogBox)
        self.LogField.setGeometry(QtCore.QRect(10, 20, 741, 101))
        self.LogField.setObjectName("LogField")
        self.ParametersBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ParametersBox.setGeometry(QtCore.QRect(10, 300, 211, 141))
        self.ParametersBox.setObjectName("ParametersBox")
        self.layoutWidget = QtWidgets.QWidget(self.ParametersBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 191, 131))
        self.layoutWidget.setObjectName("layoutWidget")
        self.ParametersLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.ParametersLayout.setContentsMargins(0, 0, 0, 0)
        self.ParametersLayout.setObjectName("ParametersLayout")
        self.fileLabel = QtWidgets.QLabel(self.layoutWidget)
        self.fileLabel.setObjectName("fileLabel")
        self.ParametersLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fileLabel)
        self.coordinatesLayout = QtWidgets.QHBoxLayout()
        self.coordinatesLayout.setObjectName("coordinatesLayout")
        self.fileButtonLayout = QtWidgets.QHBoxLayout()
        self.fileButtonLayout.setObjectName("fileButtonLayout")
        self.fileEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.fileEdit.setEnabled(False)
        self.fileEdit.setObjectName("fileEdit")
        self.fileButtonLayout.addWidget(self.fileEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.fileButtonLayout.addItem(spacerItem)
        self.fileButton = QtWidgets.QToolButton(self.layoutWidget)
        self.fileButton.setEnabled(True)
        self.fileButton.setObjectName("fileButton")
        self.fileButtonLayout.addWidget(self.fileButton)
        self.coordinatesLayout.addLayout(self.fileButtonLayout)
        self.ParametersLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.coordinatesLayout)
        self.powerLabel = QtWidgets.QLabel(self.layoutWidget)
        self.powerLabel.setObjectName("powerLabel")
        self.ParametersLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.powerLabel)
        self.powerLayout = QtWidgets.QHBoxLayout()
        self.powerLayout.setObjectName("powerLayout")
        self.powerSpinBox = QtWidgets.QDoubleSpinBox(self.layoutWidget)
        self.powerSpinBox.setDecimals(1)
        self.powerSpinBox.setSingleStep(0.5)
        self.powerSpinBox.setProperty("value", 10.0)
        self.powerSpinBox.setObjectName("powerSpinBox")
        self.powerLayout.addWidget(self.powerSpinBox)
        self.powerPercentLabel = QtWidgets.QLabel(self.layoutWidget)
        self.powerPercentLabel.setObjectName("powerPercentLabel")
        self.powerLayout.addWidget(self.powerPercentLabel)
        self.powerLayout.setStretch(0, 1)
        self.ParametersLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.powerLayout)
        self.openTimeLabel = QtWidgets.QLabel(self.layoutWidget)
        self.openTimeLabel.setObjectName("openTimeLabel")
        self.ParametersLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.openTimeLabel)
        self.openTimeLayout = QtWidgets.QHBoxLayout()
        self.openTimeLayout.setObjectName("openTimeLayout")
        self.openSpinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.openSpinBox.setMaximum(999999)
        self.openSpinBox.setSingleStep(100)
        self.openSpinBox.setProperty("value", 100)
        self.openSpinBox.setObjectName("openSpinBox")
        self.openTimeLayout.addWidget(self.openSpinBox)
        self.openTimeMsLabel = QtWidgets.QLabel(self.layoutWidget)
        self.openTimeMsLabel.setObjectName("openTimeMsLabel")
        self.openTimeLayout.addWidget(self.openTimeMsLabel)
        self.openTimeLayout.setStretch(0, 1)
        self.ParametersLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.openTimeLayout)
        self.periodLabel = QtWidgets.QLabel(self.layoutWidget)
        self.periodLabel.setObjectName("periodLabel")
        self.ParametersLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.periodLabel)
        self.periodLayout = QtWidgets.QHBoxLayout()
        self.periodLayout.setObjectName("periodLayout")
        self.periodSpinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.periodSpinBox.setMaximum(999999)
        self.periodSpinBox.setSingleStep(100)
        self.periodSpinBox.setProperty("value", 200)
        self.periodSpinBox.setObjectName("periodSpinBox")
        self.periodLayout.addWidget(self.periodSpinBox)
        self.periodMsLabel = QtWidgets.QLabel(self.layoutWidget)
        self.periodMsLabel.setObjectName("periodMsLabel")
        self.periodLayout.addWidget(self.periodMsLabel)
        self.periodLayout.setStretch(0, 1)
        self.ParametersLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.periodLayout)
        self.saveButton = QtWidgets.QPushButton(self.layoutWidget)
        self.saveButton.setEnabled(True)
        self.saveButton.setObjectName("saveButton")
        self.ParametersLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.saveButton)
        self.startButton = QtWidgets.QPushButton(self.layoutWidget)
        self.startButton.setObjectName("startButton")
        self.ParametersLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.startButton)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(230, 30, 551, 411))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 301, 371))
        self.tableWidget.setToolTip("")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.annealBox = QtWidgets.QGroupBox(self.tab)
        self.annealBox.setGeometry(QtCore.QRect(320, 10, 211, 111))
        self.annealBox.setObjectName("annealBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.annealBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 19, 191, 83))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.annealLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.annealLayout.setContentsMargins(0, 0, 0, 0)
        self.annealLayout.setObjectName("annealLayout")
        self.annealPowerLayout = QtWidgets.QHBoxLayout()
        self.annealPowerLayout.setSpacing(6)
        self.annealPowerLayout.setObjectName("annealPowerLayout")
        self.annealPowerLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.annealPowerLabel.setObjectName("annealPowerLabel")
        self.annealPowerLayout.addWidget(self.annealPowerLabel)
        self.annealPowerBox = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.annealPowerBox.setDecimals(1)
        self.annealPowerBox.setSingleStep(0.5)
        self.annealPowerBox.setObjectName("annealPowerBox")
        self.annealPowerLayout.addWidget(self.annealPowerBox)
        self.annealPercentlabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.annealPercentlabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.annealPercentlabel.setTextFormat(QtCore.Qt.AutoText)
        self.annealPercentlabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.annealPercentlabel.setObjectName("annealPercentlabel")
        self.annealPowerLayout.addWidget(self.annealPercentlabel)
        self.annealPowerLayout.setStretch(0, 1)
        self.annealLayout.addLayout(self.annealPowerLayout)
        self.annealVelocityLayout = QtWidgets.QHBoxLayout()
        self.annealVelocityLayout.setObjectName("annealVelocityLayout")
        self.annealVelocityLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.annealVelocityLabel.setObjectName("annealVelocityLabel")
        self.annealVelocityLayout.addWidget(self.annealVelocityLabel)
        self.annealSpeedBox = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.annealSpeedBox.setProperty("value", 5.0)
        self.annealSpeedBox.setObjectName("annealSpeedBox")
        self.annealVelocityLayout.addWidget(self.annealSpeedBox)
        self.annealPercentLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.annealPercentLabel.setObjectName("annealPercentLabel")
        self.annealVelocityLayout.addWidget(self.annealPercentLabel)
        self.annealVelocityLayout.setStretch(0, 1)
        self.annealLayout.addLayout(self.annealVelocityLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toggleShutterButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.toggleShutterButton.setObjectName("toggleShutterButton")
        self.horizontalLayout_2.addWidget(self.toggleShutterButton)
        self.startAnnealButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.startAnnealButton.setObjectName("startAnnealButton")
        self.horizontalLayout_2.addWidget(self.startAnnealButton)
        self.annealLayout.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView.setEnabled(False)
        self.graphicsView.setGeometry(QtCore.QRect(-10, -9, 541, 401))
        self.graphicsView.setObjectName("graphicsView")
        self.tabWidget.addTab(self.tab_2, "")
        self.StagesConrtolBox = QtWidgets.QGroupBox(self.centralwidget)
        self.StagesConrtolBox.setGeometry(QtCore.QRect(10, 180, 211, 111))
        self.StagesConrtolBox.setObjectName("StagesConrtolBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.StagesConrtolBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 181, 83))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.StagesLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.StagesLayout.setContentsMargins(0, 0, 0, 0)
        self.StagesLayout.setObjectName("StagesLayout")
        self.StagesToZerosButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.StagesToZerosButton.setObjectName("StagesToZerosButton")
        self.StagesLayout.addWidget(self.StagesToZerosButton, 0, 0, 1, 2)
        self.MoveStagesField = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.MoveStagesField.setObjectName("MoveStagesField")
        self.StagesLayout.addWidget(self.MoveStagesField, 2, 1, 1, 1)
        self.MoveStagesButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.MoveStagesButton.setObjectName("MoveStagesButton")
        self.StagesLayout.addWidget(self.MoveStagesButton, 2, 0, 1, 1)
        self.StagesToHomeButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.StagesToHomeButton.setObjectName("StagesToHomeButton")
        self.StagesLayout.addWidget(self.StagesToHomeButton, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.AutoDetectButton, self.manualConnectionBox)
        MainWindow.setTabOrder(self.manualConnectionBox, self.shutterPortLineEdit)
        MainWindow.setTabOrder(self.shutterPortLineEdit, self.manualConnectButton)
        MainWindow.setTabOrder(self.manualConnectButton, self.LogField)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Impulse taper maker v0.6 (24.07.2020)"))
        self.ConnectionBox.setTitle(_translate("MainWindow", "Connection"))
        self.AutoDetectButton.setText(_translate("MainWindow", "AutoDetect"))
        self.manualConnectionBox.setText(_translate("MainWindow", "Manual"))
        self.laserPortLabel.setText(_translate("MainWindow", "Laser port:    COM"))
        self.shutterPortLabel.setText(_translate("MainWindow", "Shutter port: COM"))
        self.manualConnectButton.setText(_translate("MainWindow", "Connect"))
        self.LogBox.setTitle(_translate("MainWindow", "Log"))
        self.ParametersBox.setTitle(_translate("MainWindow", "Parameters"))
        self.fileLabel.setText(_translate("MainWindow", "Last used file:"))
        self.fileEdit.setText(_translate("MainWindow", "Select file"))
        self.fileButton.setText(_translate("MainWindow", "..."))
        self.powerLabel.setText(_translate("MainWindow", "Laser power:"))
        self.powerPercentLabel.setText(_translate("MainWindow", "%"))
        self.openTimeLabel.setText(_translate("MainWindow", "Shutter opened:"))
        self.openTimeMsLabel.setText(_translate("MainWindow", "ms"))
        self.periodLabel.setText(_translate("MainWindow", "Shutter period:"))
        self.periodMsLabel.setText(_translate("MainWindow", "ms"))
        self.saveButton.setText(_translate("MainWindow", "Save config"))
        self.startButton.setText(_translate("MainWindow", "Start/stop"))
        self.tableWidget.setStatusTip(_translate("MainWindow", "Enter - create new row; empty rows will be deleted automatically."))
        self.annealBox.setTitle(_translate("MainWindow", "Fiber annealing"))
        self.annealPowerLabel.setText(_translate("MainWindow", "Laser power:"))
        self.annealPercentlabel.setText(_translate("MainWindow", "%     "))
        self.annealVelocityLabel.setText(_translate("MainWindow", "Motor velocity:"))
        self.annealPercentLabel.setText(_translate("MainWindow", "mm/s"))
        self.toggleShutterButton.setText(_translate("MainWindow", "Toggle shutter"))
        self.startAnnealButton.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.StagesConrtolBox.setTitle(_translate("MainWindow", "Stages conrtrolling"))
        self.StagesToZerosButton.setText(_translate("MainWindow", "Stages to zeros"))
        self.MoveStagesButton.setText(_translate("MainWindow", "Move stages"))
        self.StagesToHomeButton.setText(_translate("MainWindow", "Stages to home"))

