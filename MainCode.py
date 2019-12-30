#######################################Run program by running this module#############################################
##This module connects GUI buttons to functions defined elsewhere and uses objects of classes defined in other modules##
#Apart from this file, these files must be in the directory to run the program:
        #AssessmentThreeUI.ui, CyberballandCustomWidgets.py,AssessmentThreePython.py, GUI.py, Functions.py
        #Media files:antiBrexitVoice.wav,neutralAudio.wav, proBrexitVoice.wav, dancePractice.mov
        #Image files: IOS-scale.png, uclLogo.jpg, avatar1.png, avatar2.png, ballresized.png, methrow.png,
                      #Player2Done.png, Player2Start.png, speechbubble.png, thrown.png
#Running this module will open the experiment window for participants to use

from Functions import *

#These lines create an object of class "Experiment", which is defined in the "Functions" module
#They then call methods of the class to assign the participant an ID number, condition, and set up the experiment's manipulation page (audio or video and prompts)
thisExperiment=Experiment()
thisExperiment.assignPartcptID()
thisExperiment.assignCondition()
thisExperiment.setManipulation()

exclusivegame=throwBallExclusive() #Creates an object of class throwBallExclusive, which is the Cyberball game

#These lines make a "no consent message" label that blinks using class "Coloured Label" in CyberballandCustomWidgets module
#This label appears on the first page of the experiment's stacked widget
ui.noConsentMsg=ColouredLabel(ui.ConsentPage)
ui.noConsentMsg.setAlignment(QtCore.Qt.AlignCenter)
ui.noConsentMsg.setText("You have not consented. Please exit this program and speak with a research assistant.")
ui.noConsentMsg.setGeometry(370,410, 355,65)
ui.noConsentMsg.setWordWrap(True)
ui.noConsentMsg.blink("white", "orange")
ui.noConsentMsg.hide()


#The functions below remain in this module because they use the object "thisExperiment" created in this module.

def checkResponse(): #Checks if the participant has entered a response after listening to the audio selection.
    if thisExperiment.condition=="dance" or thisExperiment.condition=="combo": #These conditions don't have response section initally
        videoWidget.hide()
        ui.groupDanceInstrctnLbl.show()
        ui.exptProceedBtn.hide()
        ui.endDanceSessionBtn.show()
        stopVideo()
    elif ui.audioResponseLineEdit.text()=="":
        ui.summaryErrorLbl.show() #If there is no response, participants cannot proceed and see an error message
    else:
        nextPage()
    thisExperiment.PANASTestScore()

def addIntermediary(): #Creates a list of strings that are then added as a line to the CSV using a method of the "Experiment" class
    listToAdd=[str(thisExperiment.participantIDNumber), str(thisExperiment.condition), str(ui.ageSpinBox.value()), recordGender(), str(ui.EduComboBx.currentIndex()), str(ui.BrexitComboBox.currentIndex()), ui.audioResponseLineEdit.text(), str(thisExperiment.analgesiaMeasure1-thisExperiment.analgesiaMeasure2), str(thisExperiment.analgesiaMeasure1), str(thisExperiment.analgesiaMeasure2), str(thisExperiment.PANASPositivePreScore), str(thisExperiment.PANASNegativePreScore), str(thisExperiment.PANASPositivePostScore), str(thisExperiment.PANASNegativePostScore), str(thisExperiment.PANASPositivePostScore-thisExperiment.PANASPositivePreScore), str(thisExperiment.PANASNegativePostScore-thisExperiment.PANASNegativePreScore), str(thisExperiment.selfInOtherScore)]
    for item in listToAdd:
        thisExperiment.addToLine(item)
    thisExperiment.addToCSV(thisExperiment.lineInCSV)
    nextPage()

def playSound():# Plays an audio clip for the "perspective-taking", "control", and "combo" conditions
    # Each of the audio options are different lengths, so the audioTimer can be set to the appropriate time
    # This function can include more or different audio options, just insert the ".wav" file name after QSound.play and its length in milliseconds after singleShot
    audioTimer = QTimer()
    ui.PLAYBtn.disconnect()
    # audioTimer.singleShot(1000,thisExperiment.audioResponseRecord) #This line is helpful for testing audio to avoid listening full clips
    #To use this shortened audio line (above) to test, comment out the rest of the function
    if ui.BrexitComboBox.currentIndex() == 2: # Brexit supporters receive an anti-Brexit clip and vice-versa
        QSound.play("proBrexitVoice.wav")
        audioTimer.singleShot(84000, thisExperiment.audioResponseRecord)
    elif ui.BrexitComboBox.currentIndex() == 1:
        QSound.play("antiBrexitVoice.wav")
        audioTimer.singleShot(122000, thisExperiment.audioResponseRecord)
    else: # If the participant is indifferent on Brexit, they will receive the neutral audio
        QSound.play("neutralAudio.wav")
        audioTimer.singleShot(60000, thisExperiment.audioResponseRecord)

def comboManipulation(): #Checks the audio response box for the combo condition
    if ui.audioResponseLineEdit.text()=="":
        ui.summaryErrorLbl.show()
    else:
        nextPage()
    thisExperiment.PANASTestScore()

def checkCombo(): #Sets up audio part of the combo condition or proceeds to next page for dance condition
    if thisExperiment.condition=="combo":
        ui.groupDanceInstrctnLbl.hide()
        ui.PLAYBtn.show()
        ui.dancePartyBtn.hide()
        ui.endDanceSessionBtn.hide()
    elif thisExperiment.condition=="dance":
        nextPage()

def prepareGame(): #Hides the pictures for the "thrown" figures so that the animation will appear properly
    #Also hides the instructions label and buttons for finishing the game and turns the page
    ui.player1finish.hide()
    ui.player2finish.hide()
    ui.thrownleft.hide()
    ui.thrownright.hide()
    ui.thxforplayingLbl.hide()
    ui.EndGameNextBtn.hide()
    ui.ballLabel.show()
    nextPage()
    thisExperiment.resetPANAS()

def passToCheckPANAS4(): #Intermediary function that checks in PANAS 4 is filled and checks the post-test score
    panasPart4.checkIfFilled(listOfItems4, ui.PANASErrorLbl4)
    thisExperiment.PANASTestScore()

#This is a dictionary of all the widgets that need to be connected to other functions when clicked
dictionaryOfWidgets={ui.consentSubmitPushBtn: checkConsent, ui.demogSubmitPushBtn: checkDemographics,
                    ui.dancePartyBtn:playVideo, ui.Timer1StartButton:thisExperiment.analgesiaTimerStart,
                    ui.Timer1StopButton: thisExperiment.analgesiaTimerStop, ui.NextBtnPANAS1:passToCheckPANAS1, ui.NxtBtnPANAS2: passToCheckPANAS2, ui.NxtBtnPANAS3:passToCheckPANAS3,
                    ui.PLAYBtn:playSound, ui.exptProceedBtn:checkResponse, ui.endDanceSessionBtn: checkCombo, ui.Timer2StartButton:thisExperiment.analgesiaTimerStart,
                    ui.Timer2StopButton:thisExperiment.analgesiaTimerStop, ui.comboProceedBtn:comboManipulation,  ui.NxtBtnPANAS3:passToCheckPANAS3, ui.NxtBtnPANAS4:passToCheckPANAS4,
                    ui.selfInOtherNextBtn:thisExperiment.checkSelfInOther, ui.submitBtn:addIntermediary,
                    ui.FinishBtn:thisExperiment.endTrial, ui.cyberballStartBtn:prepareGame, ui.EndGameNextBtn:nextPage,
                    ui.Player1Btn:exclusivegame.buttonCounter, ui.Player2Btn:exclusivegame.buttonCounter, ui.callForBallBtn:passToMe}
for widget in dictionaryOfWidgets:
    widget.clicked.connect(dictionaryOfWidgets[widget])

sys.exit (app.exec_())