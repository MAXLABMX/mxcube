"""Element analysis Simple XRF brick"""

import logging

from qt import *
import Qwt5 as qwt

import string

from BlissFramework.BaseComponents import BlissWidget
from SpecClient import SpecScan

import os

__category__ = 'MaxLab'

TESTSCAN=0


class ElementGraph(qwt.QwtPlot):
    def __init__(self,*args):
        qwt.QwtPlot.__init__(self,*args)

    def mouseEvent(self, event):
        print "Mouse event"

    def onSelected(self, point):
        print "clicked on graph"

    def onMouseMoved(self,ev):
        xpixel = ev.pos().x()
        ypixel = ev.pos().y()

        x = self.invTransform(qwt.QwtPlot.xBottom, xpixel)
        y = self.invTransform(qwt.QwtPlot.yLeft, ypixel)

        dict={'event':'MouseAt',
             'x':x,
             'y':y,
             'xpixel':xpixel,
             'ypixel':ypixel}

        self.emit(PYSIGNAL("QtBlissGraphSignal"),(dict,))

class QwtElementAnalysisBrick(BlissWidget):
    def __init__(self, *args):
        BlissWidget.__init__(self, *args)

        self.addProperty('mnemonic','string')

        self.defineSignal('newScan', ())

        self.scanObject = None
        self.xdata = []
        self.ydata = []
        self.lastDataDir=""

        self.printer=QPrinter()

        self.hardwareObject=None

        self.okReadData=0

        self.addProperty('specVersion', 'string', '')
        self.lblTitle = QLabel(self)
        self.lblTitle.setText("<h3>Element Analysis</h3>")
        
        buttonBox = QHBox(self)
        self.lblPosition = QLabel(buttonBox)
        self.lblPosition.setAlignment(Qt.AlignLeft)
        
        self.graphPanel = QWidget(self)
        self.graphPanel.setSpacing = 0
        QHBoxLayout(self.graphPanel)
        self.graph = ElementGraph(self.graphPanel)
        self.graph.setMinimumWidth(800)
        self.graph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        energyBox=QVBox(self.graphPanel)
        self.energiesWindow=QListView(energyBox)
        self.energiesWindow.addColumn("Element")
        self.energiesWindow.addColumn("Edge")
        self.energiesWindow.addColumn("Energy (keV)")
        self.energiesWindow.setSortColumn(2)
        self.energiesWindow.setMaximumWidth(400)
        self.energiesWindow.setColumnWidth(0,80)
        self.energiesWindow.setColumnWidth(1,50)
        self.energiesWindow.setColumnWidth(2,150)
        self.graphPanel.layout().addWidget(self.graph)
        self.graphPanel.layout().addWidget(energyBox)
        QObject.connect(self.energiesWindow,SIGNAL("clicked(QListViewItem)"),self.showEnergyMarker)
        box1=QHBox(self)
        box10=QHGroupBox(box1)
        box10.setTitle("Graph settings")
        box11=QHGroupBox(box1)
        box11.setTitle("Scan parameters")
        box111=QHBox(box11)
        box112=QHBox(box11)



        self.logYCheckBox=QCheckBox("log Y",box10)
        self.doAutoScaleBn=QPushButton("Auto scale", box10)
        self.resetAutoScaleBn=QPushButton("Reset scale", box10)

        QObject.connect(self.logYCheckBox,SIGNAL("toggled(bool)"), self.setYLogScale)
        QObject.connect(self.doAutoScaleBn,SIGNAL("clicked()"), self.doAutoScale)
        QObject.connect(self.resetAutoScaleBn,SIGNAL("clicked()"), self.resetAutoScale)

        lab1=QLabel("ROI (keV) min/max:",box111)
        lab1.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        lab1.setAlignment(Qt.AlignRight)
        self.minEnergy=QLineEdit(box111)
        self.minEnergy.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.minEnergy.setText("0")
        lab2=QLabel("/",box111)
        lab2.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.maxEnergy=QLineEdit(box111)
        self.maxEnergy.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.maxEnergy.setText("15")
        lab3=QLabel("Time (s):",box112)
        lab3.setAlignment(Qt.AlignRight)
        lab3.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.timeInput=QLineEdit(box112)
        self.timeInput.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.timeInput.setText("1")

        box2=QHBox(self)
        #box21=QVBox(box2)
        #box21.setMargin(20)
        #box211=QHBox(box21)
        #box212=QHBox(box21)
        lw1=QWidget(box2)
        gl1=QGridLayout(lw1,3,2,10)
        box22=QVGroupBox(box2)
        box22.setTitle("Scan files")
        
        lab4=QLabel("Fluorescence\ndetector:", lw1)
        self.clfluorButton=QPushButton("??", lw1)
        lab4.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        #self.clfluorButton.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        lab5=QLabel("Start scan:",lw1)
        self.startButton=QPushButton("Start",lw1)
        self.helpBn=QPushButton("Help",lw1)
        QObject.connect(self.helpBn,SIGNAL("clicked()"), self.showHelpDialog)
        self.printBn=QPushButton("Print",lw1)
        QObject.connect(self.printBn,SIGNAL("clicked()"), self.printGraph)
        gl1.addWidget(lab4,0,0)
        gl1.addWidget(self.clfluorButton,0,1)
        gl1.addWidget(lab5,1,0)
        gl1.addWidget(self.startButton,1,1)
        gl1.addWidget(self.helpBn,2,0)
        gl1.addWidget(self.printBn,2,1)
        
        self.saveDataBn=QPushButton("Save",box22)
        self.loadDataBn=QPushButton("Load",box22)
        self.addDataBn=QPushButton("Add",box22)

        QObject.connect(self.clfluorButton, SIGNAL("clicked()"), self.moveCLFluor)
        QObject.connect(self.startButton, SIGNAL("clicked()"), self.getScan)
        QObject.connect(self.saveDataBn, SIGNAL("clicked()"), self.saveData)
        QObject.connect(self.loadDataBn, SIGNAL("clicked()"), self.loadData)
        QObject.connect(self.addDataBn, SIGNAL("clicked()"), self.addData)

        QObject.connect(self.graph, PYSIGNAL('QtBlissGraphSignal'), self.handleBlissGraphSignal)

        self.graph.canvas().setMouseTracking(True)
        #self.graph.enableLegend(True)
        #self.graph.setAutoLegend(True)
        self.setPaletteBackgroundColor(Qt.white)
        self.lblTitle.setAlignment(Qt.AlignHCenter)
        self.lblTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.lblPosition.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        buttonBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.graphPanel.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        QVBoxLayout(self)
        self.layout().addWidget(self.lblTitle)
        self.layout().addWidget(buttonBox)
        self.layout().addWidget(self.graphPanel)
        self.layout().addWidget(box1)
        self.layout().addWidget(box2)

        if TESTSCAN:
            d={}
            d['xlabel']="keV"
            d['ylabel']="Intensity"
            d['title']="TestScan"
            f=file('/home/blissadm/local/MAXBricks/testdata.dat','r')
            x=[]
            y=[]
            for line in f:
                if line[0] == "#" or len(line) == 0:
                    continue
                else:
                    l=line.split()
                    x.append(float(l[0])/1000)
                    y.append(float(l[1]))
            self.drawNewGraph(x,y)

    def propertyChanged(self, property, oldValue, newValue):

        if property == 'mnemonic':
            if self.hardwareObject is not None:
            
                self.disconnect(self.hardwareObject, PYSIGNAL('newDataValues'), self.drawNewGraph)
                self.disconnect(self.hardwareObject, PYSIGNAL('clfluorState'), self.updateCLFluor)
                self.disconnect(self.hardwareObject, PYSIGNAL('specState'), self.handleSpecState)
                self.disconnect(self.hardwareObject, PYSIGNAL('connected'), self.handleConnected)
                self.disconnect(self.hardwareObject, PYSIGNAL('disconnected'), self.handleDisconnected)
                self.disconnect(self.hardwareObject, PYSIGNAL('processEnergiesUpdated'), self.showAnalysis)
                self.disconnect(self.hardwareObject, PYSIGNAL('processElementEdgesUpdated'), self.showElementMarkers)
            self.hardwareObject=self.getHardwareObject(newValue)

            if self.hardwareObject is not None:
                self.lastDataDir=self.hardwareObject.defaultDataDir            
                self.connect(self.hardwareObject, PYSIGNAL('newDataValues'), self.drawNewGraph)
                self.connect(self.hardwareObject, PYSIGNAL('clfluorState'), self.updateCLFluor)
                self.connect(self.hardwareObject, PYSIGNAL('specState'), self.handleSpecState)
                self.connect(self.hardwareObject, PYSIGNAL('connected'), self.handleConnected)
                self.connect(self.hardwareObject, PYSIGNAL('disconnected'), self.handleDisconnected)
                self.connect(self.hardwareObject, PYSIGNAL('processEnergiesUpdated'), self.showAnalysis)
                self.connect(self.hardwareObject, PYSIGNAL('processElementEdgesUpdated'), self.showElementMarkers)

    def showHelpDialog(self):
        ret=QMessageBox.information(self, "Element Analysis", self.hardwareObject.helpText, QMessageBox.Ok)
 

    def printGraph(self):
        self.graph.printps()

    def showEnergyMarker(self, item):
        el=str(item.text(0))
        self.hardwareObject.getElementEdges(el)

    def showElementMarkers(self,data, element):
        print "showElementMarkers"
        p1=QPen(Qt.red,2)
        p2=QPen(Qt.blue,2)
        self.graph.clearmarkers()
        if element=="Selected":
            s="Selected energy"
            self.graph.insertx1marker(self.selectedEnergy,label=s)
            self.graph.replot()
            return
        data=data.split()
        ka=float(data[5])
        kb=float(data[6])
        la=float(data[7])
        lb=float(data[8])
        xmax=float(str(self.maxEnergy.text()))
        if ka != 0 and ka < xmax:
            s="%s %s"% (element,"Ka")
            m=self.graph.insertx1marker(ka,label=s)
            self.graph.setMarkerLinePen(m,p1)
        if kb != 0 and kb < xmax:
            s="%s %s"% (element,"Kb")
            m=self.graph.insertx1marker(kb,label=s)
            self.graph.setMarkerLinePen(m,p1)
        if la != 0 and la < xmax:
            s="%s %s"% (element,"La")
            m=self.graph.insertx1marker(la,label=s)
            self.graph.setMarkerLinePen(m,p2)
        if lb != 0 and lb < xmax:
            s="%s %s"% (element,"Lb")
            m=self.graph.insertx1marker(lb,label=s)
            self.graph.setMarkerLinePen(m,p2)
            
        self.graph.replot()

    def getScan(self):
        s=0
        try:
            minE=float(str(self.minEnergy.text()))
        except:
            s="Min Energy not a number"
        try:
            maxE=float(str(self.maxEnergy.text()))
        except:
            s="Max Energy not a number"
        try:
            t=float(str(self.timeInput.text()))
        except:
            s="Exposure time not a number"
        if s:
            tmp=QMessageBox.critical(self,"NaN error",s,QMessageBox.Ok)
            return

        self.hardwareObject.setCLFluor(0)  
        #self.updateCLFluor(0)
         # move in detector
        ans=QMessageBox.information(self,"Element Analysis","Check fluorescence detector.\nClick 'Ok' when it is raised in the proper position.",QMessageBox.Ok,QMessageBox.Cancel)

        #if ans==QMessageBox.Cancel:
         #   return

        ans=self.hardwareObject.startScan(minE,maxE,t)

        if ans:
            tmp=QMessageBox.warning(self,"Error",ans,QMessageBox.Ok)


    def keyPressEvent(self,e):
        print "----keypressed", e.key()
        #print self.activecurve_index

        if e.key() == Qt.Key_Delete:
            self.graph.delcurve(self.activecurve_key)                
            self.graph.checky1scale()
            self.graph.replot()

    def mousePressEvent(self,e):
        print "----mousePressEvent", e.button()

        #if e.button() == Qt.RightButton:
            #print self.activecurve_key 
#
        #if e.button() == Qt.LeftButton:

        print "Hello"

        xpointer=e.x()
        ypointer=e.y()

        print xpointer

        print ",Hello"

        print "X: %f, Y: %f"% (e.x(),e.y())

        if len(self.xdata) == 0:
           print "X: %f, Y: %f"% (e.x(),e.y())
        else:
           self.selectedEnergy=xpointer
           self.hardwareObject.getEnergies(self.selectedEnergy)


    def handleSpecState(self,state):
        print "Specstate",state

    def handleConnected(self):
        print "connected"

    def handleDisconnected(self):
        print "disconnected"

    def moveCLFluor(self):
        print "EABrick: moveCLFluor(self): moveCLFlour: text=", self.clfluorButton.text()
        
        self.hardwareObject.setCLFluor( not self.hardwareObject.clfluorStateChannel.getValue())
#        if self.hardwareObject.clfluorStateChannel.getValue():
#            self.hardwareObject.setCLFluor(0)
        print "EABrick: moveCLFluor(self): self.hardwareObject.setCLFluor(" , self.hardwareObject.clfluorStateChannel.getValue(), ")"
        #QTimer.sleep(1)
        #print "EABrick: moveCLFluor(self): self.hardwareObject.setCLFluor(" , self.hardwareObject.clfluorStateChannel.getValue(), ")"
#        else:
#            self.hardwareObject.setCLFluor(1)
#            print "-.----- self.hardwareObject.setCLFluor(1)"
        
#        if str(self.clfluorButton.text()) == "In":
#            self.hardwareObject.setCLFluor(1)
#            print "-.-----In: self.hardwareObject.setCLFluor(1)"
#        if str(self.clfluorButton.text()) == "Out":
#            self.hardwareObject.setCLFluor(0)
#            print "--------Out: self.hardwareObject.setCLFluor(0)"

#
#    state == 1 means detector is out, will be moved in
#
    def updateCLFluor(self,state):
        if state:
            self.clfluorButton.setText("Move In")
        else:
            self.clfluorButton.setText("Move Out")


    def drawNewGraph(self,xdata,ydata):
            self.graph.xlabel('keV')
            self.graph.ylabel('Intensity')
            self.xdata=list(xdata)
            self.ydata=[]
            for i in ydata:
                if i < 1:
                    self.ydata.append(1)
                else:
                    self.ydata.append(i)

            xmin=float(str(self.minEnergy.text()))
            xmax=float(str(self.maxEnergy.text()))
            #print "xdata", xdata, len(xdata), type(xdata)
            #print "X",self.xdata, len(self.xdata), type(self.xdata)
            #print "ydata", ydata, len(ydata), type(ydata)
            #print "Y", self.ydata, len(self.ydata), type(self.ydata)
            self.graph.newcurve('Last scan', self.xdata, self.ydata)
            self.graph.curves['Last scan']['x_original']=xdata
            self.graph.curves['Last scan']['y_original']=ydata
            self.graph.setAutoReplot(1)
            self.graph.setAxisScale(qwt.QwtPlot.xBottom,xmin,xmax)

            #
            # Changed to setAxisAutoScale since old did not work, seemed to be for QWt4
            # /JU
            #
            if self.graph.yAutoScale:
                self.graph.setAxisAutoScale(qwt.QwtPlot.yLeft)
                self.graph.setAxisAutoScale(qwt.QwtPlot.yRight)

            self.graph.replot()

    def addGraph(self,xdata,ydata,fn):
        self.graph.newcurve(fn,xdata,ydata)
        self.graph.checky1scale()
        self.graph.curves[fn]['x_original']=xdata
        self.graph.curves[fn]['y_original']=ydata
        self.graph.replot()

    def doAutoScale(self):
        maxVal=0
        for k in self.graph.curves:
            v=(self.graph.curve(self.graph.curves[k]['curve']).maxYValue())
            if v > maxVal:
                maxVal=v
        for k in self.graph.curves:
            y=[]
            x=[]
            curve=self.graph.curve(self.graph.curves[k]['curve'])
            maxRef=curve.maxYValue()
            c=maxVal/maxRef
            for i in range(curve.dataSize()):

                y.append(curve.y(i)*c)
                x.append(curve.x(i))
            y=list(y)
            x=list(x)
            curve.setData(x,y)
        self.graph.replot()
            

    def resetAutoScale(self):
        for k in self.graph.curves:
            curve=self.graph.curve(self.graph.curves[k]['curve'])
            x=self.graph.curves[k]['x_original']
            y=self.graph.curves[k]['y_original']
            x=list(x)
            y=list(y)
            curve.setData(x,y)
        self.graph.replot()
             

    def setYLogScale(self,state):
        if state:
            self.graph.setAxisScale(qwt.QwtPlot.yLeft,1,max(self.ydata))
            self.graph.replot()
        else:
            self.graph.replot()
        

    def handleBlissGraphSignal(self, signalDict):
        
        if signalDict['event'] == 'MouseAt':
            self.lblPosition.setText("(X: %f, Y: %f)" % (signalDict['x'], signalDict['y']))

        if signalDict['event'] == 'MouseClick':
            xpointer=signalDict['x']
            ypointer=signalDict['y']
            if len(self.xdata) == 0:
                print "X: %f, Y: %f"% (signalDict['x'],signalDict['y'])
            else:
                self.selectedEnergy=xpointer
                self.hardwareObject.getEnergies(self.selectedEnergy)

        if signalDict['event'] == 'SetActiveCurveEvent':
            self.activecurve_index=signalDict['index']
            self.activecurve_key=signalDict['legend']

    def showAnalysis_old(self,data):
        s="<b>Selected energy: %.4f keV</b>"% self.selectedEnergy
        s=s+'<p style="font-family: verdana">\n<table>'
        mark_set=0
        for i in data:
            try:
                el, ed, en=i.split()
            except:
                self.energiesWindow.setText(i)
                return
            el=el.ljust(2)
            if ed == "Ka":
                ed="K&#945 "
            if ed == "Kb":
                ed="K&#946 "
            if ed == "La":
                ed="L&#945 "
            if ed == "Lb":
                ed="L&#946 "

            en_tmp=float(en)/1000.0
            en="%.3f keV"% en_tmp
            if en_tmp > self.selectedEnergy:
                if not mark_set:
                    s=s+"</table><hr><table>\n"
                    mark_set=1
            s=s+"<tr>\n"
            data_list=[el,ed,en,""]
            for i in data_list:
                i="<td>%s</td>\n"% i
                s=s+i
            s=s+"</tr>\n"
        s=s+"</table></p>"
        #print s
        self.energiesWindow.setText(s)

    def showAnalysis(self,data):
        print "showAnalysis", data
        self.energiesWindow.clear()
        #s="<b>Selected energy: %.4f keV</b>"% self.selectedEnergy
        #self.selectedEnergyLabel.setText(s)
        mark_set=0
        for i in data:
            try:
                el,ed,en=i.split()
            except:
                print "error reading energies:", i
                return    

            en_tmp=float(en)/1000.0
            en="%.3f"% en_tmp
            if en_tmp > self.selectedEnergy:
                if not mark_set:
                    s="%.4f"% self.selectedEnergy
                    QListViewItem(self.energiesWindow, "Selected", "energy", s)
                    mark_set=1
            QListViewItem(self.energiesWindow, str(el), ed, en)            
            

    def saveData(self):
        if len(self.xdata) != len(self.ydata):
            print "x and y are not equal in length"
            return
        fn=QFileDialog.getSaveFileName("/data","Data files (*.dat)",self,"Save file dialog", "Choose a filename")
        fn=str(fn)
        fn=fn.split(".")
        if len(fn) > 1:
            s=fn[-1]
            if s != "dat":
                fn.append("dat")
            fn=".".join(fn)
        else:
            fn.append("dat")
            fn=".".join(fn)
            
        f=file(str(fn),'w')
        for i in range(len(self.xdata)):
            f.write("%f,%f\n"% (self.xdata[i], self.ydata[i],))
        f.close()
        
    def loadData(self):
        fn=QFileDialog.getOpenFileName(self.lastDataDir,"Data files (*.dat)",self,"Open file dialog", "Choose a filename")
        #Make sure that the filename ends with .dat
        self.lastDataDir=os.path.dirname(str(fn))
        f=file(str(fn),'r')
        xdata=[]
        ydata=[]
        got_line=1
        for line in f:
            try:
                x,y=line.split(',')
                got_line=1
            except:
                got_line=0
            if got_line:
                xdata.append(float(x))
                ydata.append(float(y))
        f.close()
        #print xdata,ydata
        if len(xdata) == len(ydata) and len(xdata) != 0:
            self.drawNewGraph(xdata,ydata)
            self.graph.clearmarkers()
            self.energiesWindow.clear()

    def addData(self):
        fn=QFileDialog.getOpenFileName(self.lastDataDir,"Data files (*.dat)",self,"Open file dialog", "Choose a filename")
        #Make sure that the filename ends with .dat
        self.lastDataDir=os.path.dirname(str(fn))
        f=file(str(fn),'r')
        xdata=[]
        ydata=[]
        got_line=1
        for line in f:
            try:
                x,y=line.split(',')
                got_line=1
            except:
                got_line=0
            if got_line:
                xdata.append(float(x))
                ydata.append(float(y))
        f.close()
        #print xdata,ydata
        if len(xdata) == len(ydata) and len(xdata) != 0:
            print type(fn)
            fname=str(fn).split("/")[-1]
            self.addGraph(xdata,ydata,fname) 
	
