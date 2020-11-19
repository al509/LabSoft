# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IM.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setToolTip("")
        MainWindow.setStatusTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ConnectionBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ConnectionBox.setGeometry(QtCore.QRect(10, 20, 211, 121))
        self.ConnectionBox.setObjectName("ConnectionBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.ConnectionBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 19, 191, 131))
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
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 191, 139))
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
        self.tabWidget.setGeometry(QtCore.QRect(240, 40, 541, 401))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 301, 371))
        self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tableWidget.setAcceptDrops(False)
        self.tableWidget.setToolTip("")
        self.tableWidget.setProperty("showDropIndicator", True)
        self.tableWidget.setDragDropOverwriteMode(True)
        self.tableWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.tableWidget.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(12)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.annealBox = QtWidgets.QGroupBox(self.tab)
        self.annealBox.setGeometry(QtCore.QRect(320, 40, 211, 111))
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
        self.sortingBox = QtWidgets.QCheckBox(self.tab)
        self.sortingBox.setGeometry(QtCore.QRect(320, 10, 101, 17))
        self.sortingBox.setObjectName("sortingBox")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.codeBowser = QtWidgets.QTextBrowser(self.tab_3)
        self.codeBowser.setGeometry(QtCore.QRect(10, 90, 511, 291))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.codeBowser.setFont(font)
        self.codeBowser.setReadOnly(False)
        self.codeBowser.setOverwriteMode(False)
        self.codeBowser.setObjectName("codeBowser")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab_3)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 159, 80))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.generatorParamsLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.generatorParamsLayout.setContentsMargins(0, 0, 0, 0)
        self.generatorParamsLayout.setObjectName("generatorParamsLayout")
        self.startPosLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.startPosLabel.setObjectName("startPosLabel")
        self.generatorParamsLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.startPosLabel)
        self.endPosLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.endPosLabel.setObjectName("endPosLabel")
        self.generatorParamsLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.endPosLabel)
        self.stepBox = QtWidgets.QLabel(self.formLayoutWidget)
        self.stepBox.setObjectName("stepBox")
        self.generatorParamsLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.stepBox)
        self.startPosLayout = QtWidgets.QHBoxLayout()
        self.startPosLayout.setObjectName("startPosLayout")
        self.startPosBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.startPosBox.setDecimals(3)
        self.startPosBox.setProperty("value", 2.0)
        self.startPosBox.setObjectName("startPosBox")
        self.startPosLayout.addWidget(self.startPosBox)
        self.startmmLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.startmmLabel.setObjectName("startmmLabel")
        self.startPosLayout.addWidget(self.startmmLabel)
        self.generatorParamsLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.startPosLayout)
        self.endPosLayout = QtWidgets.QHBoxLayout()
        self.endPosLayout.setObjectName("endPosLayout")
        self.endPosBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.endPosBox.setDecimals(3)
        self.endPosBox.setProperty("value", 3.0)
        self.endPosBox.setObjectName("endPosBox")
        self.endPosLayout.addWidget(self.endPosBox)
        self.endmmLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.endmmLabel.setObjectName("endmmLabel")
        self.endPosLayout.addWidget(self.endmmLabel)
        self.generatorParamsLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.endPosLayout)
        self.stepLayout = QtWidgets.QHBoxLayout()
        self.stepLayout.setObjectName("stepLayout")
        self.stepFuncBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.stepFuncBox.setDecimals(3)
        self.stepFuncBox.setProperty("value", 0.25)
        self.stepFuncBox.setObjectName("stepFuncBox")
        self.stepLayout.addWidget(self.stepFuncBox)
        self.stepmmLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.stepmmLabel.setObjectName("stepmmLabel")
        self.stepLayout.addWidget(self.stepmmLabel)
        self.generatorParamsLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.stepLayout)
        self.generateArrayButton = QtWidgets.QPushButton(self.tab_3)
        self.generateArrayButton.setGeometry(QtCore.QRect(180, 60, 131, 23))
        self.generateArrayButton.setObjectName("generateArrayButton")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.correctionView = QtWidgets.QGraphicsView(self.tab_4)
        self.correctionView.setGeometry(QtCore.QRect(210, 240, 321, 131))
        self.correctionView.setObjectName("correctionView")
        self.ERVView = QtWidgets.QGraphicsView(self.tab_4)
        self.ERVView.setGeometry(QtCore.QRect(230, 10, 301, 191))
        self.ERVView.setObjectName("ERVView")
        self.zeroLevelSlider = QtWidgets.QSlider(self.tab_4)
        self.zeroLevelSlider.setEnabled(True)
        self.zeroLevelSlider.setGeometry(QtCore.QRect(200, 10, 22, 191))
        self.zeroLevelSlider.setAutoFillBackground(False)
        self.zeroLevelSlider.setMinimum(0)
        self.zeroLevelSlider.setMaximum(100)
        self.zeroLevelSlider.setSingleStep(1)
        self.zeroLevelSlider.setProperty("value", 50)
        self.zeroLevelSlider.setOrientation(QtCore.Qt.Vertical)
        self.zeroLevelSlider.setInvertedAppearance(False)
        self.zeroLevelSlider.setObjectName("zeroLevelSlider")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.tab_4)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 187, 133))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.correctionLayout = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.correctionLayout.setContentsMargins(0, 0, 0, 0)
        self.correctionLayout.setObjectName("correctionLayout")
        self.InputERVLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.InputERVLabel.setObjectName("InputERVLabel")
        self.correctionLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.InputERVLabel)
        self.loadERVLayout = QtWidgets.QHBoxLayout()
        self.loadERVLayout.setObjectName("loadERVLayout")
        self.inputERVEdit = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.inputERVEdit.setEnabled(True)
        self.inputERVEdit.setObjectName("inputERVEdit")
        self.loadERVLayout.addWidget(self.inputERVEdit)
        self.inputERVButton = QtWidgets.QToolButton(self.formLayoutWidget_2)
        self.inputERVButton.setObjectName("inputERVButton")
        self.loadERVLayout.addWidget(self.inputERVButton)
        self.correctionLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.loadERVLayout)
        self.loadIMSLayout = QtWidgets.QHBoxLayout()
        self.loadIMSLayout.setObjectName("loadIMSLayout")
        self.inputIMSEdit = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.inputIMSEdit.setEnabled(True)
        self.inputIMSEdit.setObjectName("inputIMSEdit")
        self.loadIMSLayout.addWidget(self.inputIMSEdit)
        self.inputIMSButton = QtWidgets.QToolButton(self.formLayoutWidget_2)
        self.inputIMSButton.setObjectName("inputIMSButton")
        self.loadIMSLayout.addWidget(self.inputIMSButton)
        self.correctionLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.loadIMSLayout)
        self.ZeroLevelLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.ZeroLevelLabel.setObjectName("ZeroLevelLabel")
        self.correctionLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.ZeroLevelLabel)
        self.zeroLevelBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget_2)
        self.zeroLevelBox.setDecimals(3)
        self.zeroLevelBox.setMinimum(1540.9)
        self.zeroLevelBox.setMaximum(1555.1)
        self.zeroLevelBox.setSingleStep(0.001)
        self.zeroLevelBox.setProperty("value", 1549.95)
        self.zeroLevelBox.setObjectName("zeroLevelBox")
        self.correctionLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.zeroLevelBox)
        self.calcCorrectionButton = QtWidgets.QPushButton(self.formLayoutWidget_2)
        self.calcCorrectionButton.setObjectName("calcCorrectionButton")
        self.correctionLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.calcCorrectionButton)
        self.inputIMSLabel = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.inputIMSLabel.setObjectName("inputIMSLabel")
        self.correctionLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.inputIMSLabel)
        self.x0Label = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.x0Label.setObjectName("x0Label")
        self.correctionLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.x0Label)
        self.x0Box = QtWidgets.QSpinBox(self.formLayoutWidget_2)
        self.x0Box.setSingleStep(5)
        self.x0Box.setObjectName("x0Box")
        self.correctionLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.x0Box)
        self.x0Slider = QtWidgets.QSlider(self.tab_4)
        self.x0Slider.setGeometry(QtCore.QRect(210, 210, 321, 21))
        self.x0Slider.setOrientation(QtCore.Qt.Horizontal)
        self.x0Slider.setObjectName("x0Slider")
        self.tabWidget.addTab(self.tab_4, "")
        self.StagesConrtolBox = QtWidgets.QGroupBox(self.centralwidget)
        self.StagesConrtolBox.setGeometry(QtCore.QRect(10, 180, 211, 111))
        self.StagesConrtolBox.setObjectName("StagesConrtolBox")
        self.gridLayoutWidget = QtWidgets.QWidget(self.StagesConrtolBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 191, 83))
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
        self.StagesToHomeButton.setEnabled(False)
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
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.AutoDetectButton, self.manualConnectionBox)
        MainWindow.setTabOrder(self.manualConnectionBox, self.shutterPortLineEdit)
        MainWindow.setTabOrder(self.shutterPortLineEdit, self.manualConnectButton)
        MainWindow.setTabOrder(self.manualConnectButton, self.LogField)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Impulse maker v0.81 (19.11.2020)"))
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
        self.tabWidget.setStatusTip(_translate("MainWindow", "Current stage position:"))
        self.tableWidget.setStatusTip(_translate("MainWindow", "Enter - create new row; empty rows will be deleted automatically."))
        self.tableWidget.setSortingEnabled(False)
        self.annealBox.setTitle(_translate("MainWindow", "Fiber annealing"))
        self.annealPowerLabel.setText(_translate("MainWindow", "Laser power:"))
        self.annealPercentlabel.setText(_translate("MainWindow", "%     "))
        self.annealVelocityLabel.setText(_translate("MainWindow", "Motor velocity:"))
        self.annealPercentLabel.setText(_translate("MainWindow", "mm/s"))
        self.toggleShutterButton.setText(_translate("MainWindow", "Toggle shutter"))
        self.startAnnealButton.setText(_translate("MainWindow", "Start"))
        self.sortingBox.setText(_translate("MainWindow", "Enable sorting"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Main features"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "N(x)"))
        self.codeBowser.setStatusTip(_translate("MainWindow", "\'def()\': and \'return\' parts not necessary. Indentation starts from zero level"))
        self.codeBowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"># Write n(x) function here in Python-stye. For example:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\">if x &gt; 60:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\">    n = 1</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\">else:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\">    n = 0</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\"># Consider that you are just writing some func(x) that returns n value.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\">#Note that n truncates to int in the end; x can be float.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\"># Be careful, python-injections are posiible as this code interpreting</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#000000;\"># in program without any checks and changes.</span></p></body></html>"))
        self.startPosLabel.setText(_translate("MainWindow", "Start position:"))
        self.endPosLabel.setText(_translate("MainWindow", "End position:"))
        self.stepBox.setText(_translate("MainWindow", "Step:"))
        self.startmmLabel.setText(_translate("MainWindow", "mm"))
        self.endmmLabel.setText(_translate("MainWindow", "mm"))
        self.stepmmLabel.setText(_translate("MainWindow", "mm"))
        self.generateArrayButton.setText(_translate("MainWindow", "Generate array"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Function generator"))
        self.InputERVLabel.setText(_translate("MainWindow", "Input ERV file: "))
        self.inputERVButton.setText(_translate("MainWindow", "..."))
        self.inputIMSButton.setText(_translate("MainWindow", "..."))
        self.ZeroLevelLabel.setText(_translate("MainWindow", "Zero level (λ₀):"))
        self.calcCorrectionButton.setText(_translate("MainWindow", "Generate array"))
        self.inputIMSLabel.setText(_translate("MainWindow", "Input IMS file: "))
        self.x0Label.setText(_translate("MainWindow", "First variation (x₀):"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Correction"))
        self.StagesConrtolBox.setTitle(_translate("MainWindow", "Stages conrtrolling"))
        self.StagesToZerosButton.setText(_translate("MainWindow", "Stages to zeros"))
        self.MoveStagesButton.setText(_translate("MainWindow", "Move stages"))
        self.StagesToHomeButton.setText(_translate("MainWindow", "Stages to home"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

