#This module contains the code for the Cyberball game class and ColouredLabel extension of QLabel
from GUI import *

#This class creates a custom widget, a blinking label
class ColouredLabel(QLabel):
    def setColour(self, colorString):
        self.setAutoFillBackground(True)
        myPalette = self.palette()
        myPalette.setColor(QPalette.Window, QColor(colorString))
        self.setPalette(myPalette)
        newFont = QFont("Calibri", 16)
        self.setFont(newFont)
    def blink(self, color1, color2):
        self.blinkColour1 = color1
        self.blinkColour2 = color2
        self.currentColour = color1
        self.blinkTimer = QTimer()
        self.blinkTimer.timeout.connect(self.onBlink)
        self.blinkTimer.start(500)
    def onBlink(self):
        if self.currentColour == self.blinkColour1:
            self.currentColour = self.blinkColour2
        else:
            self.currentColour = self. blinkColour1
        self.setColour(self.currentColour)

#This class sets up the Cyberball game
class throwBallExclusive():
    def __init__(self):
        self.OverallTimer=QTimer() #This timer times the whole game
        self.timer1=QTimer() #This timer times the the actions of Player 1
        self.timer2=QTimer() #This timer times the actions of Player 2
        self.timer=QTimer() #This timer is used for the initial throw of the game
        self.myTime=QTimer() #This timer times the actions of the "me" player
    def endGame(self): #This method ends the game and shows the Next button and end of game prompt
        ui.ballLabel.hide()
        ui.thxforplayingLbl.show()
        ui.EndGameNextBtn.show()
        self.timer1.stop() #Stops all timers so that animations stop once game ends
        self.timer2.stop()
        self.timer.stop()
        self.myTime.stop()
    def buttonCounter(self):#This method shows the "Call for Ball" label and, depending on which character the user clicked, throws them the ball once
        ui.callForBallBtn.show()
        self.OverallTimer.singleShot(40000, self.endGame) #This sets the overall game length. To adjust, change the number of milliseconds in this line
        ui.myHand.hide()
        if window.sender() == ui.Player1Btn: #If the user clicked Player 1 as the first throw recipient
            ui.thrownleft.show() #Show the appropriate animation image on the "Me" character
            self.myTime.timeout.connect(self.throwDiagonalLeft) #Connects to ThrowDiagonalLeft method
        elif window.sender() == ui.Player2Btn: #If the user clicked Player 2 as the first throw recipient
            ui.thrownright.show() #Show the appropriate animation image on the "Me" character
            self.myTime.timeout.connect(self.throwDiagonalRight)#Sets the interval at which the "throwDiagonalLeft" method is called
        self.myTime.start(50) #Sets interval at which the appropriate ThrowDiagonal method is called
    def throwball1(self): #Will be called if user throws to Player 1 on the left to begin the game
        ui.Player1Btn.disconnect()#These lines disconnect the Player1 and Player2 buttons so that the user cannot throw to them again
        ui.Player2Btn.disconnect()
        self.timer1.singleShot(1000, self.animateStart) #Calls the animateStart1 method at 1000 milliseconds with a single shot approach
        self.timer2.timeout.connect(self.animateEnd1) #Calls the animateEnd1 method at timeout intervalls of 1400 milliseconds
        self.timer2.start(1400)
    def throwball2(self): #Will be called if user throws to Player 2 on the right to begin the came
        ui.Player1Btn.disconnect() #These lines disconnect the Player1 and Player2 buttons so that the user cannot throw to them again
        ui.Player2Btn.disconnect()
        self.timer1.singleShot(1000, self.animateStart2) #Calls the animateStart2 method at 1000 milliseconds with a single shot approach
        self.timer2.timeout.connect(self.animateEnd2) #Calls the animateEnd2 method at timeout intervalls of 1400 milliseconds
        self.timer2.start(1400)
    #There are two functions below for diagonal movement because the coordinates are slightly different to make the animation look more fluid
    #They also call for a different sequence of exlusive throwing between players 1 and 2 (who starts)
    def throwDiagonalLeft(self): #Sets up the animation for the ball to move from "Me" player to Player 1 on the left of screen
        if ui.ballLabel.y()>135:#If the ball label has not reached its destination height
            currentY=ui.ballLabel.y() #These lines get the ball label's current coordinates
            currentX=ui.ballLabel.x()
            ui.ballLabel.setGeometry(currentX-12, currentY-10, 61,61) #Incrementally move the label each time the method is called
        else:
            self.myTime.stop() #If the label has reached its designated height, stop the "me" Timer so that this method won't be called again
            self.throwball1() #Call the throwball method to begin the exclusive ball-throwing between players 1 and 2
    def throwDiagonalRight(self): #Sets up the animation for the ball to move from "Me" player to Player 2 on the right of screen
        if ui.ballLabel.y() >140: #If the ball label has not reached its destination height
            currentX = ui.ballLabel.x() #These lines get the ball label's current coordinates
            currentY=ui.ballLabel.y()
            ui.ballLabel.setGeometry(currentX + 16, currentY-10, 50, 50) #Incrementally move the label each time the method is called
        else:
            self.myTime.stop() #If the label has reached its designated height, stop the "me" Timer so that this method won't be called again
            self.throwball2() #Call the throwball method to begin the exclusive ball-throwing between players 1 and 2
    #There are two methods for animateStart and animateEnd because they require different labels to show/hide and timers
    #So creating two methods was more space-efficient than creating a number of conditionals within one method
    def animateStart(self): #This method starts a pattern of exclusive throwing between Players 1 and 2 if Player 2 throws the ball first
        ui.thrownleft.hide() #hides the labels with post-throw pictures initially
        ui.player1start.hide()
        ui.player2finish.hide()
        ui.myHand.show() #shows the labels with pre-throw pictures
        ui.player1finish.show()
        ui.player2start.show()
        self.timer.timeout.connect(self.moveBalltoRight) #Connects to a method that moves the ball to the right
        self.timer.start(50)
    def animateEnd1(self): #Hides and shows appropriate labels at the end of the throw
        ui.player1finish.hide()
        ui.player1start.show()
    def animateStart2(self): #This method starts a pattern of exclusive throwing between Players 1 and 2 if Player 1 throws the ball first
        ui.thrownright.hide()#hides the labels with post-throw pictures initially
        ui.player2start.hide()
        ui.player1finish.hide()
        ui.myHand.show()#Shows the labels with pre-throw pictures
        ui.player2finish.show()
        ui.player1start.show()
        self.timer.timeout.connect(self.moveBalltoLeft) #Connects to a method that moves the ball to the right
        self.timer.start(50)
    def animateEnd2(self): #Hides and shows appropriate labels at the end of the throw
        ui.player2finish.hide()
        ui.player2start.show()
    #There are two separate methods for moving the balls to the right and left because they have different coordinates
    def moveBalltoRight(self): #If the ball has reached its destination on the right (x), start Player 2's ball throw
        if ui.ballLabel.x()<890:
            currentX = ui.ballLabel.x()
            ui.ballLabel.setGeometry(currentX+10,110, 50, 50)
        else:
            self.animateStart2()
    def moveBalltoLeft(self): #If the ball has reached its destination on the left (x), start Player 1's ball throw
        if ui.ballLabel.x()>60:
            currentX = ui.ballLabel.x()
            ui.ballLabel.setGeometry(currentX - 10, 110, 61, 61)
        else:
            self.animateStart()

#These lines set up the media player to be used in the "dance" condition. The function using it is in the "Functions" module
mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface) #Creates a QMediaPlayer object
videoWidget = QVideoWidget(ui.ManipulationInstrctnPage)   #Adds it to the manipulation page
mediaPlayer.setVideoOutput(videoWidget) #Sets what will play in the media player
videoWidget.setGeometry(50,10,900,600)#Sets the geometry of the video shown
file = path.abspath('dancePractice.mov') #Converts relative to absolute path for use on a Mac
mediaPlayer.setMedia(QMediaContent( QUrl.fromLocalFile(file))) #Sets the media file to be played
videoWidget.hide() #Hides the vide wideget until it is called later on in program

