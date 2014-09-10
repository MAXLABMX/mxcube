""" Maxlab Shortcut
20140902 Jie Nan, Maxlab
shortcut for
-spec optimise
-wiki
-stac
-detector beamstop

-IspyB server
-pyCATS server

"""

from BlissFramework.BaseComponents import BlissWidget
#from BlissFramework import Icons
#import BlissFramework
from qt import *
import logging
#import InstanceServer
#import gevent
import os

__category__ = "MaxLab"

class MaxShortcut(BlissWidget):
    def __init__(self, *args):
        BlissWidget.__init__(self, *args)

        self.addProperty('mnemonic', 'string', '')

        self.specShell = None

        self.containerBox=QVGroupBox("Shortcut",self)
        self.containerBox.setInsideMargin(4)
        self.containerBox.setInsideSpacing(4)
        self.containerBox.setAlignment(QLabel.AlignLeft)

        self.optimiseButton = QToolButton(self.containerBox)
        self.optimiseButton.setUsesTextLabel(True)
        self.optimiseButton.setTextLabel("Optimise Beam")
        self.optimiseButton.setFixedWidth(130)
        self.optimiseButton.setEnabled(False)
        QObject.connect(self.optimiseButton, SIGNAL('clicked()'), self.optimiseClicked)


        self.wikiButton = QToolButton(self.containerBox)
        self.wikiButton.setUsesTextLabel(True)
        self.wikiButton.setTextLabel("MAXlab Wiki")
        self.wikiButton.setEnabled(True)
        self.wikiButton.setFixedWidth(130)
        QObject.connect(self.wikiButton, SIGNAL('clicked()'), self.wikiClicked)

        self.stacButton = QToolButton(self.containerBox)
        self.stacButton.setUsesTextLabel(True)
        self.stacButton.setTextLabel("Run STAC")
        self.stacButton.setFixedWidth(130)
        self.stacButton.setEnabled(True)
        QObject.connect(self.stacButton, SIGNAL('clicked()'), self.stacClicked)
        
        
        self.detBeamstopBox=QHGroupBox("Detector Beamstop",self.containerBox)
        self.detBeamstopBox.setInsideMargin(4)
        self.detBeamstopBox.setInsideSpacing(0)
        self.detBeamstopBox.setAlignment(QLabel.AlignCenter)


        self.dbsInButton = QToolButton(self.detBeamstopBox)
        self.dbsInButton.setUsesTextLabel(True)
        self.dbsInButton.setTextLabel("In")
        self.dbsInButton.setEnabled(True)
        QObject.connect(self.dbsInButton, SIGNAL('clicked()'), self.dbsInClicked)

        self.dbsOutButton = QToolButton(self.detBeamstopBox)
        self.dbsOutButton.setUsesTextLabel(True)
        self.dbsOutButton.setTextLabel("Out")
        self.dbsOutButton.setEnabled(True)
        QObject.connect(self.dbsOutButton, SIGNAL('clicked()'), self.dbsOutClicked)


        QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.layout().addWidget(self.containerBox)

    def propertyChanged(self, propertyName, oldValue, newValue):
        if propertyName == 'mnemonic':
            if self.specShell is not None:
                self.disconnect(self.specShell,'busy',self.specBusy)
                self.disconnect(self.specShell,'ready',self.specReady)
                self.disconnect(self.specShell,'started',self.commandStarted)
                self.disconnect(self.specShell,'finished',self.commandFinished)
                self.disconnect(self.specShell,'aborted',self.commandAborted)
                self.disconnect(self.specShell,'failed',self.commandFailed)
            self.specShell = self.getHardwareObject(newValue)
            if self.specShell is not None:
                self.connect(self.specShell,'busy',self.specBusy)
                self.connect(self.specShell,'ready',self.specReady)
                self.connect(self.specShell,'started',self.commandStarted)
                self.connect(self.specShell,'finished',self.commandFinished)
                self.connect(self.specShell,'aborted',self.commandAborted)
                self.connect(self.specShell,'failed',self.commandFailed)

                if self.specShell.isConnected():
                   self.specConnected()
                else:
                    self.specDisconnected()
            else:
                self.specDisconnected()  
 
        elif propertyName == 'icons':
            pass
        elif propertyName == 'alwaysReadonly':
            pass
        else:
            BlissWidget.propertyChanged(self,propertyName,oldValue,newValue)


    def optimiseClicked(self):
        #logging.info("optimise beam")
        self.specShell.executeCommand("optimise")

    def dbsInClicked(self):
        self.specShell.executeCommand("dbs_in")

    def dbsOutClicked(self):
        self.specShell.executeCommand("dbs_out")

    def specBusy(self):
        self.optimiseButton.setEnabled(False)
        #logging.info("Spec Busy")

    def specReady(self):
        self.optimiseButton.setEnabled(True)
        #logging.info("Spec Ready")   
 
    def commandStarted(self):
        self.optimiseButton.setEnabled(False)
        #logging.info("command Started")
    
    def commandFinished(self,result):
        self.optimiseButton.setEnabled(True)    
        #logging.info("command Finished")
    
    def commandAborted(self):
        self.optimiseButton.setEnabled(True)

    def commandFailed(self,result):
        #logging.info("command Failed %s", str(result))
        self.optimiseButton.setEnabled(True)
    
    def specConnected(self):
        self.optimiseButton.setEnabled(True)
        #logging.info("Spec connected")

    def specDisconnected(self):
        self.optimiseButton.setEnabled(False)
        #logging.info("Spec disconnected")

    def stacClicked(self):
        #logging.info("Start STAC")
        os.system("cd /data/data1/visitor/;/home/blissadm/STAC/scripts/runstac.sh")

    def wikiClicked(self):
        #logging.info("Open Wiki")
        os.system("firefox -new-window http://wiki/index.php/I911-3 &")
