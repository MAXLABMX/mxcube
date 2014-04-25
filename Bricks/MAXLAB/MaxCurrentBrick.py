"""MAX-current display Brick

Displays the ring and 911 wiggler current

"""

from qt import *
from qtnetwork import *
from BlissFramework.BaseComponents import BlissWidget
import string

__category__= "MaxLab"

class MaxCurrentBrick(BlissWidget):
    def __init__(self, *args):
        BlissWidget.__init__(self,*args)

        self.setPaletteBackgroundColor(Qt.white)

        self.addProperty("current_update", "int", "")

        self.BS3=0
        self.ring_current=0
        self.wiggler_current=0

        self.contentsBox=QVGroupBox("Max-status",self)

        lw1=QWidget(self.contentsBox)
        QGridLayout(lw1,3,2,7,6)
        lw1.setPaletteBackgroundColor(Qt.white)

        lab1=QLabel("MAX current",lw1)
        lab1.setAlignment(Qt.AlignLeft)
        self.currentLCD=QLCDNumber(lw1)
        self.currentLCD.setSegmentStyle(QLCDNumber.Filled)
        self.currentLCD.setFrameShape(QFrame.StyledPanel)
        self.currentLCD.setFrameShadow(QFrame.Sunken)
        self.currentLCD.display("-----")
        lw1.layout().addWidget(lab1,0,0)
        lw1.layout().addWidget(self.currentLCD,0,1)

        lab2=QLabel("911 Wiggler",lw1)
        lab1.setAlignment(Qt.AlignLeft)
        self.wigglerLCD=QLCDNumber(lw1)
        self.wigglerLCD.setSegmentStyle(QLCDNumber.Filled)
        self.wigglerLCD.setFrameShape(QFrame.StyledPanel)
        self.wigglerLCD.setFrameShadow(QFrame.Sunken)
        self.wigglerLCD.display("-----")
        lw1.layout().addWidget(lab2,1,0)
        lw1.layout().addWidget(self.wigglerLCD,1,1)

        self.statuslabel=QLabel("******",lw1)
        self.statuslabel.setAlignment(Qt.AlignCenter)
        lw1.layout().addMultiCellWidget(self.statuslabel,2,2,0,1)


        QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.layout().addWidget(self.contentsBox)

        self.ring_connection=QSocket()
        self.wiggler_connection=QSocket()
        QObject.connect(self.ring_connection, SIGNAL("error(int)"), self.ringError)
        QObject.connect(self.wiggler_connection, SIGNAL("error(int)"), self.wigglerError)

        QObject.connect(self,PYSIGNAL("ringupdate"),self.currentLCD,SLOT("display(double)"))
        QObject.connect(self,PYSIGNAL("wigglerupdate"),self.wigglerLCD,SLOT("display(double)"))
        QObject.connect(self,PYSIGNAL("ringupdate"), self.updateColor)
        QObject.connect(self,PYSIGNAL("wigglerupdate"), self.updateColor)

        self.ringTimeout=QTimer()
        self.wigglerTimeout=QTimer()
        QObject.connect(self.ringTimeout,SIGNAL("timeout()"), self.resetRingConnection)
        QObject.connect(self.wigglerTimeout,SIGNAL("timeout()"), self.resetWigglerConnection)

        self.run()

    def run(self):
        self.ring_connection.connectToHost('maxsun5.maxlab.lu.se',37337)
        QObject.connect(self.ring_connection,SIGNAL("connected()"), self.connectRing)

        self.wiggler_connection.connectToHost('maxsun5.maxlab.lu.se',37338)
        QObject.connect(self.wiggler_connection, SIGNAL("connected()"), self.connectWiggler)

    def connectRing(self):
        self.ring_connection.writeBlock('update 1 0\n')
        QObject.connect(self.ring_connection, SIGNAL("readyRead()"), self.getRing)
        self.ringTimeout.start(30000)

    def connectWiggler(self):
        self.connect(self.wiggler_connection, SIGNAL("readyRead()"), self.getWiggler)
        self.wigglerTimeout.start(30000)

    def resetRingConnection(self):
        print "resetting ring connection"
        self.currentLCD.display("-----")
        self.ring_connection.clearPendingData()
        self.ring_connection.close()
        self.ring_connection.connectToHost('maxsun5.maxlab.lu.se',37337)
        self.ring_connection.writeBlock('update 1 0\n')

    def resetWigglerConnection(self):
        print "resetting wiggler connection"
        self.wigglerLCD.display("-----")
        self.wiggler_connection.clearPendingData()
        self.ring_connection.close()
        self.wiggler_connection.connectToHost('maxsun5.maxlab.lu.se',37338)

    def ringError(self, error):
        print "ring error",error

    def wigglerError(self, error):
        print "wiggler error",error

    def updateColor(self):
        #Should update the lcd color. Black when stored beam with wiggler, red otherwise
        if self.BS3 > 0:
            if self.ring_current > 1.0:
                if self.wiggler_current > 199.0:
                    self.currentLCD.setPaletteForegroundColor(Qt.black)
                    self.wigglerLCD.setPaletteForegroundColor(Qt.black)
                    self.statuslabel.setPaletteBackgroundColor(Qt.green)
                    self.statuslabel.setText("Stored beam")
                else:
                    self.currentLCD.setPaletteForegroundColor(Qt.red)
                    self.wigglerLCD.setPaletteForegroundColor(Qt.red)
                    self.statuslabel.setPaletteBackgroundColor(Qt.yellow)
                    self.statuslabel.setText("Wiggler down")
            else:
                self.currentLCD.setPaletteForegroundColor(Qt.red)
                self.wigglerLCD.setPaletteForegroundColor(Qt.red)
                self.statuslabel.setPaletteBackgroundColor(Qt.red)
                self.statuslabel.setText("No beam")
        else:
            self.currentLCD.setPaletteForegroundColor(Qt.red)
            self.wigglerLCD.setPaletteForegroundColor(Qt.red)
            if self.ring_current > 1.0:
                self.statuslabel.setPaletteBackgroundColor(Qt.yellow)
                self.statuslabel.setText("Injection")
            else:
                self.statuslabel.setPaletteBackgroundColor(Qt.red)
                self.statuslabel.setText("No beam")

    def getRing(self):
        if self.ring_connection.canReadLine():
            raw_data=str(self.ring_connection.readBlock(1024))
            lines=string.split(raw_data, '\n')
            for line in lines:
                if not len(line) <= 1:
                    try:
                      if int(line[0]) == 2:
                        try:
                           tmp=string.split(line,'\t')
                           self.ring_current=float(tmp[2])
                           self.BS3=int(tmp[5])
                           self.emit(PYSIGNAL("ringupdate"),(self.ring_current,))
                           self.ringTimeout.start(30000)
                        except IndexError:
                           pass
                    except ValueError:
                       pass
                      

    def getWiggler(self):
        if self.wiggler_connection.canReadLine():
            raw_data=str(self.wiggler_connection.readBlock(1024))
            lines=string.split(raw_data, '\n')
            for line in lines:
                if not len(line) <= 1:
                    if line[0] != 'V' and line[0] != 'H':
                        try:
                           tmp=string.split(line)
                           self.wiggler_current=float(tmp[9])*400.0/65536
                           self.emit(PYSIGNAL("wigglerupdate"),(self.wiggler_current,))
                           self.wigglerTimeout.start(30000)
                        except IndexError:
                           pass

    def closeEvent(self,ev):
        self.ring_connection.close()
        self.wiggler_connection.close()

    def propertyChanged(self,propertyName,oldValue,newValue):
        if propertyName == "current_update":
            self.currentupdate=newValue
