"""Disk Usage Brick

Displays and updates the avaliable disk space

Add the path, as shown with df, in the propeties window
"""

import os

from qt import *
from BlissFramework.BaseComponents import BlissWidget

__category__= "MaxLab"

class MAXDiskUsageBrick(BlissWidget):
    def __init__(self, *args):
        BlissWidget.__init__(self, *args)

        self.addProperty("paths", "string", "")

        self.contentsBox=QHGroupBox("Free disk space",self)

        self.diskDisplay=QLabel("********", self.contentsBox)

        self.timer=QTimer()

        QHBoxLayout(self)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.layout().addWidget(self.contentsBox)

    def run(self):
        self.timer.start(15000)
        self.connect(self.timer,SIGNAL("timeout()"),self.displayUsage)

    def stop(self):
        self.timer.stop()

    def displayUsage(self):
        #print "updating disk usage"
        #return # do nothing, for now..
        #p=os.popen("ls -ld /data/data1")
        #print p
        p=os.popen("df -h ")
        #print p
        line=p.readline()
        disklist={}
        while line != "":
            test=line.split()
            #
            #print "line"
            #print line
            #print "test: ", test
            #print "paths:", self.paths
            #print "\n\n\n\n\n test[0] test[1] test[2] test[3]", test[0], test[1], test[2] , test[3]
            if test[-1] in self.paths:
                disklist[test[-1]]=test[2] + " (" + test[3] + ")"
                #print "\ntestdisklist[test[-1]]", disklist[test[-1]]
            line=p.readline()
        p.close()
        s=""
        for disk in self.paths:
            s=s+disk+"  -  "+disklist[disk]+"\n"
        self.diskDisplay.setText(s)


    def propertyChanged(self,propertyName,oldValue,newValue):
        if propertyName == "paths":
            self.paths=newValue.split()
            print self.paths


            
