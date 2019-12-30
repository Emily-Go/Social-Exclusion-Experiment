from PyQt5 import QtWidgets,QtCore,QtGui, QtWebEngineWidgets, QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
import sys, time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from os import path, listdir
import platform
from AssessmentThreePython import *


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)

window = QMainWindow()

ui=Ui_MainWindow()
ui.setupUi(window)



