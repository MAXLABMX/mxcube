""" Maxlab Shortcut
20140902 Jie Nan, Maxlab
shortcut for

-IspyB server
-pyCATS server
-CATS LN2 refilling reminder
"""

from BlissFramework.BaseComponents import BlissWidget
#from BlissFramework import Icons
#import BlissFramework
from qt import *
import logging
#import InstanceServer
#import gevent
import os
import time

__category__ = "MaxLab"

class MaxMaintain(BlissWidget):
    def __init__(self, *args):
        BlissWidget.__init__(self, *args)

        self.containerBox=QVGroupBox("Maintenance",self)
        self.containerBox.setInsideMargin(2)
        self.containerBox.setInsideSpacing(15)
        self.containerBox.setAlignment(QLabel.AlignLeft)

        self.ispybBox=QHGroupBox("ISPyB Server",self.containerBox)
        self.ispybBox.setInsideMargin(2)
        self.ispybBox.setInsideSpacing(0)
        self.ispybBox.setAlignment(QLabel.AlignCenter)

        self.ispybStatus=QWidget(self.ispybBox)
        QGridLayout(self.ispybStatus,3,2,7,6)
        self.ispybStatus.setPaletteBackgroundColor(Qt.white)

        labIspyb=QLabel("Current:",self.ispybStatus)
        labIspyb.setAlignment(Qt.AlignLeft)
        self.currentIspyb=QLabel("-------",self.ispybStatus)
        self.currentIspyb.setAlignment(Qt.AlignLeft)
        self.ispybStatus.layout().addWidget(labIspyb,0,0)
        self.ispybStatus.layout().addWidget(self.currentIspyb,0,1)

        self.restartIspybButton = QToolButton(self.ispybBox)
        self.restartIspybButton.setUsesTextLabel(True)
        self.restartIspybButton.setTextLabel("Restart")
        self.restartIspybButton.setEnabled(False)
        self.restartIspybButton.setFixedWidth(60)
        QObject.connect(self.restartIspybButton, SIGNAL('clicked()'), self.restartIspybClicked)

        self.hwrBox=QHGroupBox("Hardware Server",self.containerBox)
        self.hwrBox.setInsideMargin(2)
        self.hwrBox.setInsideSpacing(0)
        self.hwrBox.setAlignment(QLabel.AlignCenter)

        self.hwrStatus=QWidget(self.hwrBox)
        QGridLayout(self.hwrStatus,3,2,7,6)
        self.hwrStatus.setPaletteBackgroundColor(Qt.white)

        labHwr=QLabel("Current:",self.hwrStatus)
        labHwr.setAlignment(Qt.AlignLeft)
        self.currentHwr=QLabel("-------",self.hwrStatus)
        self.currentHwr.setAlignment(Qt.AlignLeft)
        self.hwrStatus.layout().addWidget(labHwr,0,0)
        self.hwrStatus.layout().addWidget(self.currentHwr,0,1)

        self.killHwrButton = QToolButton(self.hwrBox)
        self.killHwrButton.setUsesTextLabel(True)
        self.killHwrButton.setTextLabel("Kill")
        self.killHwrButton.setEnabled(False)
        QObject.connect(self.killHwrButton, SIGNAL('clicked()'), self.killHwrClicked)

        self.startHwrButton = QToolButton(self.hwrBox)
        self.startHwrButton.setUsesTextLabel(True)
        self.startHwrButton.setTextLabel("Start")
        self.startHwrButton.setEnabled(False)
        QObject.connect(self.startHwrButton, SIGNAL('clicked()'), self.startHwrClicked)

         
        self.pycatsBox=QHGroupBox("PyCATS Server",self.containerBox)
        self.pycatsBox.setInsideMargin(2)
        self.pycatsBox.setInsideSpacing(0)
        self.pycatsBox.setAlignment(QLabel.AlignCenter)

        self.pycatsStatus=QWidget(self.pycatsBox)
        QGridLayout(self.pycatsStatus,3,2,7,6)
        self.pycatsStatus.setPaletteBackgroundColor(Qt.white)

        labPycats=QLabel("Current:",self.pycatsStatus)
        labPycats.setAlignment(Qt.AlignLeft)
        self.currentPycats=QLabel("-------",self.pycatsStatus)
        self.currentPycats.setAlignment(Qt.AlignLeft)
        self.pycatsStatus.layout().addWidget(labPycats,0,0)
        self.pycatsStatus.layout().addWidget(self.currentPycats,0,1)

        self.killPycatsButton = QToolButton(self.pycatsBox)
        self.killPycatsButton.setUsesTextLabel(True)
        self.killPycatsButton.setTextLabel("Kill")
        self.killPycatsButton.setEnabled(False)
        QObject.connect(self.killPycatsButton, SIGNAL('clicked()'), self.killPycatsClicked)

        self.startPycatsButton = QToolButton(self.pycatsBox)
        self.startPycatsButton.setUsesTextLabel(True)
        self.startPycatsButton.setTextLabel("Start")
        self.startPycatsButton.setEnabled(False)
        QObject.connect(self.startPycatsButton, SIGNAL('clicked()'), self.startPycatsClicked)

        self.catsReportBox=QHGroupBox("CATS LN2 Refill Monitor",self.containerBox)
        self.catsReportBox.setInsideMargin(2)
        self.catsReportBox.setInsideSpacing(0)
        self.catsReportBox.setAlignment(QLabel.AlignCenter)

        self.catsReportStatus=QWidget(self.catsReportBox)
        QGridLayout(self.catsReportStatus,3,2,7,6)
        self.catsReportStatus.setPaletteBackgroundColor(Qt.white)

        labCatsReport=QLabel("Current:",self.catsReportStatus)
        labCatsReport.setAlignment(Qt.AlignLeft)
        self.currentCatsReport=QLabel("-------",self.catsReportStatus)
        self.currentCatsReport.setAlignment(Qt.AlignLeft)
        self.catsReportStatus.layout().addWidget(labCatsReport,0,0)
        self.catsReportStatus.layout().addWidget(self.currentCatsReport,0,1)

        self.killCatsReportButton = QToolButton(self.catsReportBox)
        self.killCatsReportButton.setUsesTextLabel(True)
        self.killCatsReportButton.setTextLabel("Kill")
        self.killCatsReportButton.setEnabled(False)
        QObject.connect(self.killCatsReportButton, SIGNAL('clicked()'), self.killCatsReportClicked)

        self.startCatsReportButton = QToolButton(self.catsReportBox)
        self.startCatsReportButton.setUsesTextLabel(True)
        self.startCatsReportButton.setTextLabel("Start")
        self.startCatsReportButton.setEnabled(False)
        QObject.connect(self.startCatsReportButton, SIGNAL('clicked()'), self.startCatsReportClicked)

        
        QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.layout().addWidget(self.containerBox)
        
        self.timer=QTimer()     
        
        self.ispyb_status()
        self.hwr_status()
        self.pycats_status()
        self.catsReport_status()  
 

    def run(self):
        self.timer.start(20000)
        self.connect(self.timer,SIGNAL("timeout()"),self.ispyb_status)
        self.connect(self.timer,SIGNAL("timeout()"),self.hwr_status)
        self.connect(self.timer,SIGNAL("timeout()"),self.pycats_status)
        self.connect(self.timer,SIGNAL("timeout()"),self.catsReport_status)
    

    def stop(self):
        self.timer.stop()

    def ispyb_status(self):
        ispyb_status=os.popen("/home/blissadm/Desktop/ispyb_status.sh")
        status_str=ispyb_status.read()
        ispyb_status.close()
        if 'true' in status_str:
           self.currentIspyb.setText("Running")
           self.ispybStatus.setPaletteBackgroundColor(Qt.green)
        else:
           self.currentIspyb.setText("Stopped")
           self.ispybStatus.setPaletteBackgroundColor(Qt.red)
        self.restartIspybButton.setEnabled(True)
 
    def hwr_status(self):
        os.system("screen -dmS shared /home/blissadm/bin/hwrServer_status.sh&")
        status_f = open("/home/blissadm/bin/hwrServer_status.res")
        status_str = status_f.read()
        status_f.close()
        #hwr_status=os.popen("screen -dmS shared \"ps aux| grep hwrServer |awk ' {if ($0!~/grep/ && $0!~/hwrServer_status/) print $0;}'\" ")
        #status_str=hwr_status.read()
        #hwr_status.close()
        if 'hwrServer' in status_str:
           self.currentHwr.setText("Running")
           self.hwrStatus.setPaletteBackgroundColor(Qt.green)
           self.startHwrButton.setEnabled(False)
           self.killHwrButton.setEnabled(True)
        else:
           self.currentHwr.setText("Stopped")
           self.hwrStatus.setPaletteBackgroundColor(Qt.red)
           self.startHwrButton.setEnabled(True)
           self.killHwrButton.setEnabled(False)
   
    def pycats_status(self):
        pycats_status=os.popen("ssh specadm@bli9113-spec '/home/specadm/i911/cats/scripts/PyCATS_status.sh'")
        status_str=pycats_status.read()
        pycats_status.close()
        if len(status_str)>0:
           self.currentPycats.setText("Running")
           self.pycatsStatus.setPaletteBackgroundColor(Qt.green)
           self.startPycatsButton.setEnabled(False)
           self.killPycatsButton.setEnabled(True)
        else:
           self.currentPycats.setText("Stopped")
           self.pycatsStatus.setPaletteBackgroundColor(Qt.red)
           self.startPycatsButton.setEnabled(True)
           self.killPycatsButton.setEnabled(False)
 

    def catsReport_status(self):
        catsReport_status=os.popen("ssh specadm@bli9113-spec '/home/specadm/i911/cats/scripts/PyCATS_refilReport_status.sh'")
        status_str=catsReport_status.read()
        catsReport_status.close()
        if len(status_str)>0:
           self.currentCatsReport.setText("Running")
           self.catsReportStatus.setPaletteBackgroundColor(Qt.green)
           self.killCatsReportButton.setEnabled(True)
           self.startCatsReportButton.setEnabled(False)
        else:
           self.currentCatsReport.setText("Stopped")
           self.catsReportStatus.setPaletteBackgroundColor(Qt.red)
           self.killCatsReportButton.setEnabled(False)
           self.startCatsReportButton.setEnabled(True)

    def restartIspybClicked(self):
        os.system("/home/blissadm/Desktop/ispyb_restart.sh")
        self.currentIspyb.setText("-------")
        self.ispybStatus.setPaletteBackgroundColor(Qt.white)
        time.sleep(120)
        self.restartIspybButton.setEnabled(False)

    def startHwrClicked(self):
        os.system("python /home/blissadm/bin/hwrServer &")
        self.currentHwr.setText("-------")
        self.hwrStatus.setPaletteBackgroundColor(Qt.white)
        self.startHwrButton.setEnabled(False)

    def killHwrClicked(self):
        os.system("screen -dmS shared /home/blissadm/bin/hwrServer_kill.sh")
        self.currentHwr.setText("-------")
        self.hwrStatus.setPaletteBackgroundColor(Qt.white)
        self.killHwrButton.setEnabled(False)

    def startPycatsClicked(self):
        #logging.info("start pycats")
        os.system("ssh -t specadm@bli9113-spec 'screen -dmS shared //home/specadm/i911/cats/scripts/PyCATS '")
        self.currentPycats.setText("-------")
        self.pycatsStatus.setPaletteBackgroundColor(Qt.white)
        self.startPycatsButton.setEnabled(False)
     
    def killPycatsClicked(self):
        #logging.info("kill pycats")
        os.system("ssh specadm@bli9113-spec '/home/specadm/i911/cats/scripts/killPyCATS.sh'")
        self.currentPycats.setText("-------")
        self.pycatsStatus.setPaletteBackgroundColor(Qt.white)
        self.killPycatsButton.setEnabled(False)
    
    def startCatsReportClicked(self):
        os.system("ssh -t specadm@bli9113-spec 'screen -dm /usr/local/bin/python /home/specadm/i911/Python/CATS_Autorefilling_off.py '")
        self.currentCatsReport.setText("-------")
        self.catsReportStatus.setPaletteBackgroundColor(Qt.white)
        self.startCatsReportButton.setEnabled(False)
        

    def killCatsReportClicked(self):
        os.system("ssh specadm@bli9113-spec '/home/specadm/i911/cats/scripts/PyCATS_refilReport_kill.sh'")
        self.currentCatsReport.setText("-------")
        self.catsReportStatus.setPaletteBackgroundColor(Qt.white)
        self.killCatsReportButton.setEnabled(False)
