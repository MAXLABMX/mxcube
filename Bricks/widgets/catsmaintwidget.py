# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/catsmaintwidget.ui'
#
# Created: Mon Mar 17 16:13:23 2014
#      by: The PyQt User Interface Compiler (pyuic) 3.18.1
#
# WARNING! All changes made in this file will be lost!


from qt import *


class CatsMaintWidget(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("CatsMaintWidget")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding,0,0,self.sizePolicy().hasHeightForWidth()))

        CatsMaintWidgetLayout = QVBoxLayout(self,11,6,"CatsMaintWidgetLayout")
        #CatsMaintWidgetLayout.setAlignment(Qt.AlignTop)
        
        layoutBG = QHBoxLayout(None,0,6,"layoutBG")
        pixmap = QPixmap("/home/blissadm/mxCuBE-V2.0/Bricks/widgets/images/CATS_sample_layout.png")
        tmplabel = QLabel(self,"")
        tmplabel.setPixmap(pixmap)
        tmplabel.setAlignment(QLabel.AlignCenter)
        layoutBG.addWidget(tmplabel)
        CatsMaintWidgetLayout.addLayout(layoutBG)

        self.groupBox5 = QGroupBox(self,"groupBox5")
        self.groupBox5.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.groupBox5.sizePolicy().hasHeightForWidth()))
        self.groupBox5.setColumnLayout(0,Qt.Vertical)
        self.groupBox5.layout().setSpacing(7)
        self.groupBox5.layout().setMargin(20)
        self.groupBox5.setFixedHeight(80)
        groupBox5Layout = QHBoxLayout(self.groupBox5.layout())
        groupBox5Layout.setAlignment(Qt.AlignTop)

        self.lblPowerState = QLabel(self.groupBox5,"lblPowerState")
        self.lblPowerState.setAlignment(QLabel.AlignCenter)
        groupBox5Layout.addWidget(self.lblPowerState)

        self.btPowerOn = QPushButton(self.groupBox5,"btPowerOn")
        self.btPowerOn.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btPowerOn.sizePolicy().hasHeightForWidth()))
        groupBox5Layout.addWidget(self.btPowerOn)

        self.btPowerOff = QPushButton(self.groupBox5,"btPowerOff")
        self.btPowerOff.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btPowerOff.sizePolicy().hasHeightForWidth()))
        groupBox5Layout.addWidget(self.btPowerOff)
        CatsMaintWidgetLayout.addWidget(self.groupBox5)


        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.groupBox2 = QGroupBox(self,"groupBox2")
        self.groupBox2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2.layout().setSpacing(7)
        self.groupBox2.layout().setMargin(20)
        self.groupBox2.setFixedHeight(120)
        groupBox2Layout = QVBoxLayout(self.groupBox2.layout())
        groupBox2Layout.setAlignment(Qt.AlignTop)

        self.btLid1Open = QPushButton(self.groupBox2,"btLid1Open")
        btLid1Open_font = QFont(self.btLid1Open.font())
        self.btLid1Open.setFont(btLid1Open_font)
        groupBox2Layout.addWidget(self.btLid1Open)

        self.btLid1Close = QPushButton(self.groupBox2,"btLid1Close")
        btLid1Close_font = QFont(self.btLid1Close.font())
        self.btLid1Close.setFont(btLid1Close_font)
        groupBox2Layout.addWidget(self.btLid1Close)
        layout7.addWidget(self.groupBox2)

        self.groupBox2_2 = QGroupBox(self,"groupBox2_2")
        self.groupBox2_2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2_2.layout().setSpacing(7)
        self.groupBox2_2.layout().setMargin(20)
        groupBox2_2Layout = QVBoxLayout(self.groupBox2_2.layout())
        groupBox2_2Layout.setAlignment(Qt.AlignTop)

        self.btLid2Open = QPushButton(self.groupBox2_2,"btLid2Open")
        btLid2Open_font = QFont(self.btLid2Open.font())
        self.btLid2Open.setFont(btLid2Open_font)
        groupBox2_2Layout.addWidget(self.btLid2Open)

        self.btLid2Close = QPushButton(self.groupBox2_2,"btLid2Close")
        btLid2Close_font = QFont(self.btLid2Close.font())
        self.btLid2Close.setFont(btLid2Close_font)
        groupBox2_2Layout.addWidget(self.btLid2Close)
        layout7.addWidget(self.groupBox2_2)

        self.groupBox2_2_2 = QGroupBox(self,"groupBox2_2_2")
        self.groupBox2_2_2.setColumnLayout(0,Qt.Vertical)
        self.groupBox2_2_2.layout().setSpacing(7)
        self.groupBox2_2_2.layout().setMargin(20)
        groupBox2_2_2Layout = QVBoxLayout(self.groupBox2_2_2.layout())
        groupBox2_2_2Layout.setAlignment(Qt.AlignTop)

        self.btLid3Open = QPushButton(self.groupBox2_2_2,"btLid3Open")
        btLid3Open_font = QFont(self.btLid3Open.font())
        self.btLid3Open.setFont(btLid3Open_font)
        groupBox2_2_2Layout.addWidget(self.btLid3Open)

        self.btLid3Close = QPushButton(self.groupBox2_2_2,"btLid3Close")
        btLid3Close_font = QFont(self.btLid3Close.font())
        self.btLid3Close.setFont(btLid3Close_font)
        groupBox2_2_2Layout.addWidget(self.btLid3Close)
        layout7.addWidget(self.groupBox2_2_2)
        CatsMaintWidgetLayout.addLayout(layout7)

        self.groupBox6 = QGroupBox(self,"groupBox6")
        self.groupBox6.setColumnLayout(0,Qt.Vertical)
        self.groupBox6.layout().setSpacing(7)
        self.groupBox6.layout().setMargin(20)
        self.groupBox6.setFixedHeight(100)
        groupBox6Layout = QHBoxLayout(self.groupBox6.layout())
        groupBox6Layout.setAlignment(Qt.AlignTop)

        self.lblMessage = QLabel(self.groupBox6,"lblMessage")
        groupBox6Layout.addWidget(self.lblMessage)

        self.btResetError = QPushButton(self.groupBox6,"btResetError")
        self.btResetError.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btResetError.sizePolicy().hasHeightForWidth()))
        btResetError_font = QFont(self.btResetError.font())
        self.btResetError.setFixedWidth(100)
        self.btResetError.setFont(btResetError_font)
        groupBox6Layout.addWidget(self.btResetError)

        CatsMaintWidgetLayout.addWidget(self.groupBox6)

        self.groupBox13 = QGroupBox(self,"groupBox13")
        self.groupBox13.setColumnLayout(0,Qt.Vertical)
        self.groupBox13.setColumnLayout(0,Qt.Horizontal)
        self.groupBox13.layout().setSpacing(7)
        self.groupBox13.layout().setMargin(20)
        self.groupBox13.setFixedHeight(200)
        groupBox13Layout = QHBoxLayout(self.groupBox13.layout())
        groupBox13Layout.setAlignment(Qt.AlignTop)
       
        layout13_a = QVBoxLayout(None,0,6,"layout13_a")
        layout13_a.setSpacing(15)

        layout13_1 = QHBoxLayout(None,0,6,"layout13_1")
  

        self.btBack = QPushButton(self.groupBox13,"btBack")
        self.btBack.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btBack.sizePolicy().hasHeightForWidth()))
        btBack_font = QFont(self.btBack.font())
        btBack_font.setPointSize(11)
        self.btBack.setFont(btBack_font)
        layout13_1.addWidget(self.btBack)

        self.btSafe = QPushButton(self.groupBox13,"btSafe")
        self.btSafe.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btSafe.sizePolicy().hasHeightForWidth()))
        btSafe_font = QFont(self.btSafe.font())
        btSafe_font.setPointSize(11)
        self.btSafe.setFont(btSafe_font)
        layout13_1.addWidget(self.btSafe)

        self.btDryGripper = QPushButton(self.groupBox13,"btDryGripper")
        self.btDryGripper.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btDryGripper.sizePolicy().hasHeightForWidth()))
        btDryGripper_font = QFont(self.btDryGripper.font())
        btDryGripper_font.setPointSize(11)
        self.btDryGripper.setFont(btDryGripper_font)
        layout13_1.addWidget(self.btDryGripper)
        
        layout13_a.addLayout(layout13_1)

        layout13_2 = QHBoxLayout(None,0,6,"layout13_2")
        
        self.ckCATSDB = QCheckBox(self.groupBox13,"ckCATSDB")
        #layout13_2.setFixedWidth(300)
        layout13_2.addWidget(self.ckCATSDB)

        self.btResetMemory = QPushButton(self.groupBox13,"btResetMemory")
        self.btResetMemory.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btResetMemory.sizePolicy().hasHeightForWidth()))
        btResetMemory_font = QFont(self.btResetMemory.font())
        btResetMemory_font.setPointSize(11)
        self.btResetMemory.setFont(btResetMemory_font)
        layout13_2.addWidget(self.btResetMemory)


	self.btSetOnDiff = QPushButton(self.groupBox13,"btSetOnDiff")
        self.btSetOnDiff.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btSetOnDiff.sizePolicy().hasHeightForWidth()))
        btSetOnDiff_font = QFont(self.btSetOnDiff.font())
        btSetOnDiff_font.setPointSize(11)
        self.btSetOnDiff.setFont(btSetOnDiff_font)
        layout13_2.addWidget(self.btSetOnDiff)
        
        layout13_a.addLayout(layout13_2)

        layout13_3 = QHBoxLayout(None,0,6,"layout13_3") 

        self.ckCalGrip = QCheckBox(self.groupBox13,"ckCalGrip")
        layout13_3.addWidget(self.ckCalGrip)

        self.btCalibration = QPushButton(self.groupBox13,"btCalibration")
        self.btCalibration.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btCalibration.sizePolicy().hasHeightForWidth()))
        btCalibration_font = QFont(self.btCalibration.font())
        btCalibration_font.setPointSize(11)
        self.btCalibration.setFont(btCalibration_font)
        layout13_3.addWidget(self.btCalibration)


        self.btOpenTool = QPushButton(self.groupBox13,"btOpenTool")
        self.btOpenTool.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btOpenTool.sizePolicy().hasHeightForWidth()))
        btOpenTool_font = QFont(self.btOpenTool.font())
        btOpenTool_font.setPointSize(11)
        self.btOpenTool.setFont(btOpenTool_font)
        layout13_3.addWidget(self.btOpenTool)        
       
        self.btCloseTool = QPushButton(self.groupBox13,"btCloseTool")
        self.btCloseTool.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btCloseTool.sizePolicy().hasHeightForWidth()))
        btCloseTool_font = QFont(self.btCloseTool.font())
        btCloseTool_font.setPointSize(11)
        self.btCloseTool.setFont(btCloseTool_font)
        layout13_3.addWidget(self.btCloseTool)

        layout13_a.addLayout(layout13_3)
        groupBox13Layout.addLayout(layout13_a)
        CatsMaintWidgetLayout.addWidget(self.groupBox13)

        self.groupBox5_2 = QGroupBox(self,"groupBox5_2")
        self.groupBox5_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.groupBox5_2.sizePolicy().hasHeightForWidth()))
        self.groupBox5_2.setColumnLayout(0,Qt.Vertical)
        self.groupBox5_2.layout().setSpacing(7)
        self.groupBox5_2.layout().setMargin(20)
        self.groupBox5_2.setFixedHeight(80)
        groupBox5_2Layout = QHBoxLayout(self.groupBox5_2.layout())
        groupBox5_2Layout.setAlignment(Qt.AlignTop)

        self.lblRegulationState = QLabel(self.groupBox5_2,"lblRegulationState")
        self.lblRegulationState.setAlignment(QLabel.AlignCenter)
        groupBox5_2Layout.addWidget(self.lblRegulationState)

        self.btRegulationOn = QPushButton(self.groupBox5_2,"btRegulationOn")
        self.btRegulationOn.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btRegulationOn.sizePolicy().hasHeightForWidth()))
        groupBox5_2Layout.addWidget(self.btRegulationOn)

        self.btRegulationOff = QPushButton(self.groupBox5_2,"btRegulationOff")
        self.btRegulationOff.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Fixed,0,0,self.btRegulationOff.sizePolicy().hasHeightForWidth()))
        groupBox5_2Layout.addWidget(self.btRegulationOff)
        CatsMaintWidgetLayout.addWidget(self.groupBox5_2)

        self.languageChange()

        self.resize(QSize(1230,855).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.btPowerOn,self.btPowerOff)
        self.setTabOrder(self.btPowerOff,self.btLid1Open)
        self.setTabOrder(self.btLid1Open,self.btLid1Close)
        self.setTabOrder(self.btLid1Close,self.btLid2Open)
        self.setTabOrder(self.btLid2Open,self.btLid2Close)
        self.setTabOrder(self.btLid2Close,self.btLid3Open)
        self.setTabOrder(self.btLid3Open,self.btLid3Close)
        self.setTabOrder(self.btLid3Close,self.btResetError)
        self.setTabOrder(self.btResetError,self.btBack)
        self.setTabOrder(self.btBack,self.btSafe)
        self.setTabOrder(self.btSafe,self.btDryGripper)

    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.groupBox5.setTitle(self.__tr("Arm Power"))
        self.lblPowerState.setText(self.__tr("Power"))
        self.btPowerOn.setText(self.__tr("Power On"))
        self.btPowerOff.setText(self.__tr("Power Off"))
        self.groupBox2.setTitle(self.__tr("Lid 1"))
        self.btLid1Open.setText(self.__tr("Open"))
        self.btLid1Close.setText(self.__tr("Close"))
        self.groupBox2_2.setTitle(self.__tr("Lid 2"))
        self.btLid2Open.setText(self.__tr("Open"))
        self.btLid2Close.setText(self.__tr("Close"))
        self.groupBox2_2_2.setTitle(self.__tr("Lid 3"))
        self.btLid3Open.setText(self.__tr("Open"))
        self.btLid3Close.setText(self.__tr("Close"))
        self.groupBox6.setTitle(self.__tr("CATS message"))
        self.lblMessage.setText(self.__tr("Dummy message"))
        self.groupBox13.setTitle(self.__tr("Recovery Commands"))
        self.btResetError.setText(self.__tr("Reset Error"))
        self.ckCATSDB.setText(self.__tr(""))
        self.ckCalGrip.setText(self.__tr(""))
        self.btResetMemory.setText(self.__tr("Reset Memory"))
        self.btSetOnDiff.setText(self.__tr("Set Sample On Diff"))
        self.btCalibration.setText(self.__tr("Calibration"))
        self.btOpenTool.setText(self.__tr("Open Gripper"))
        self.btCloseTool.setText(self.__tr("Close Gripper"))
        self.btBack.setText(self.__tr("Back"))
        self.btSafe.setText(self.__tr("Safe"))
        self.btDryGripper.setText(self.__tr("Dry Gripper"))
        self.groupBox5_2.setTitle(self.__tr("LN2 Regulation"))
        self.lblRegulationState.setText(self.__tr("Regulation"))
        self.btRegulationOn.setText(self.__tr("Regulation On"))
        self.btRegulationOff.setText(self.__tr("Regulation Off"))


    def __tr(self,s,c = None):
        return qApp.translate("CatsMaintWidget",s,c)
