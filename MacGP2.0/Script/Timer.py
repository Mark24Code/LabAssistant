#!/usr/bin/env python
# -*- coding:utf-8-*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from time import sleep
import sys

class Windows(QDialog):

    def __init__(self, parent=None):
        super(Windows, self).__init__(parent)

        self.startButton = QPushButton("Start")
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        
        self.statusLable = QLabel("Please click \"start\"")
        self.statusLable.setFrameStyle(QFrame.StyledPanel|
                                         QFrame.Plain)

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.startButton)
        topLayout.addWidget(self.stopButton)
        
        layout = QVBoxLayout()
        layout.addLayout(topLayout)
        layout.addWidget(self.statusLable)
        
        self.timer = Timer()
        self.sec = 0
        
        self.connect(self.startButton, SIGNAL("clicked()")
                        , self.start)
        self.connect(self.stopButton, SIGNAL("clicked()")
                        , self.stop)
        self.connect(self.timer, SIGNAL("updateTime()")
                        , self.updateTime)
        
        self.setLayout(layout)
        self.setWindowTitle("Timer")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        
    def updateTime(self):
        if not self.timer.paused:
            display = "Time: " + QString.number(self.sec/100) + ":" + QString.number(self.sec%100)
            self.statusLable.setText(display)
        self.sec += 1

    def start(self):
        if self.timer.paused:
            #print 'start --- paused = true'
            self.stopButton.setEnabled(True)
            self.startButton.setText("Pause")
            self.timer.start()
            self.timer.paused = False
        else:
            #print 'start --- paused = false'
            self.timer.paused = True
            self.startButton.setText("Start")

    def stop(self):
        self.timer.stop()
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.startButton.setText("Start")
        display = "Time: " + QString.number(self.sec/100) + ":" + QString.number(self.sec%100)
        self.statusLable.setText(display)
        self.sec = 0
        self.timer.paused = True


class Timer(QThread):
    
    def __init__(self, parent=None):
        super(Timer, self).__init__(parent)
        self.stoped = False
        self.paused = True
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        while True:
            if self.stoped:
                return

            self.emit(SIGNAL("updateTime()"))
            sleep(0.01)
    
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True
        
    def isStoped(self):    
        with QMutexLocker(sellf.mutex):
            return self.stoped

app = QApplication(sys.argv)
windows = Windows()
windows.show()
app.exec_()