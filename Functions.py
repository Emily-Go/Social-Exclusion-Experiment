#This module contains code for many functions used in this program
#It also holds the Experiment class used in each trial and the QuestionnaireItem class used to set up the PANAS scale during the experiment

from random import choice, randint, choices
from CyberballandCustomWidgets import *
from operator import itemgetter #These lines import parts of other modules necessary to create an ordered dictionary
from collections import OrderedDict

#This is a list of labels that need to be hidden at the start of each trial, which is done in the lines following the list
listOfLabels=[ui.demogErrorFieldLbl, ui.demogErrorLbl, ui.PANASErrorLbl1, ui.PANASErrorLbl2, ui.callForBallBtn,
              ui.PANASErrorLbl3, ui.PANASErrorLbl4, ui.SelfInOtherErrorLbl, ui.dancePartyInstructionLbl, ui.groupDanceInstrctnLbl, ui.exptProceedBtn,
              ui.ptakingInstrctnLbl, ui.comboProceedBtn, ui.endDanceSessionBtn, ui.PLAYBtn, ui.audioResponseInstrctnLbl, ui.audioResponseLineEdit, ui.summaryErrorLbl]
for label in listOfLabels:
    label.hide()

def checkConsent(): #Checks that consent has been given
    if ui.consentBtn.isChecked()==True and ui.noConsentBtn.isChecked()==False:
        nextPage()
    else:
        ui.noConsentMsg.show()

def nextPage (): #Turns the page
    currentPage = ui.exprmtStackedWdgt.currentIndex()
    ui.exprmtStackedWdgt.setCurrentIndex(currentPage+1)

def showErrorMessage(errorLabel, errorFieldLabel, text): #Displays the correct error labels for the demographics page
    errorFieldLabel.setText("Please indicate your "+ text + " before submitting")
    errorFieldLabel.show()
    errorLabel.show()

def checkDemographics(): #Checks that all fields in the demographics page are filled out properly
    if ui.ageSpinBox.value() == 0:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "age")
    elif ui.ageSpinBox.value() <18:
        ui.demogErrorFieldLbl.setText ("Sorry, you must be over 18 years of age to participate.")
        ui.demogErrorFieldLbl.show()
    elif ui.maleWidg.isChecked() == False and ui.femaleWidg.isChecked() == False and ui.nonBinaryWidg.isChecked() == False:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "gender")
    elif ui.EduComboBx.currentIndex()==0:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "education")
    elif ui.BrexitComboBox.currentIndex()==0:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "political view")
    elif ui.yesPregnant.isChecked()==False and ui.noPregnant.isChecked()==False:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "health status")
    elif ui.yesPregnant.isChecked()==True and ui.noPregnant.isChecked()==False:
        ui.demogErrorFieldLbl.setText("Sorry, your health status makes you ineligible for this study. Please call the research assistant over.")
        ui.demogErrorFieldLbl.show()
    elif ui.yesAlcohol.isChecked()==False and ui.noAlcohol.isChecked()==False:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "substance consumption")
    elif ui.yesAlcohol.isChecked()==True and ui.noAlcohol.isChecked()==False:
        ui.demogErrorFieldLbl.setText("Sorry, you are not eligible to participate. Please call the research assistant over.")
        ui.demogErrorFieldLbl.show()
    else:
        nextPage()

def recordGender (): #Records gender so that it can be written into the csv
    if ui.maleWidg.isChecked()==True:
        gender="male"
        return gender
    if ui.femaleWidg.isChecked()==True:
        gender="female"
        return gender
    if ui.nonBinaryWidg.isChecked()==True:
        gender="nonbinary"
        return gender

def playVideo(): #Plays a video for the "dance" and "combo" conditions using the videoWidget created in "CyberballandCustomWidgets" module
    ui.dancePartyBtn.hide()
    ui.dancePartyInstructionLbl.hide()
    videoWidget.show()
    mediaPlayer.play()
    ui.exptProceedBtn.show() #If the Proceed Button should not show immediately, the experimenter can add a timer here so that it appears later
def stopVideo(): #Stops video
    mediaPlayer.stop()

#The experiment class sets up each trial of the experiment
#Each object of class Experiment counts the participants in each condition in the conditionsDictinary
#If new conditions are added to the experiment, it should be added to the conditionsDictionary with a value of 0
#The class definition checks for an "Output" csv and, if one doesn't exist, creates it
#The Experiment class also creates a list of items in the current directory (self.directory), and the headers for the experiments' csv
#The class also times each analgesia task and the class definitioon holds the two analgesia measurements as integers
#The self.timesCalled counter keeps track of how many times the PANAS score has been calculated in order to differentiate between the PANAS pre-test and post-test scores
#An object of class Experiment is created in the "MainCode" module
class Experiment:
    def __init__(self):
        self.conditionsDictionary={"dance":0, "perspective-taking":0, "combo":0, "control":0}
        self.conditionPossibilities=["dance", "perspective-taking", "combo", "control"]
        self.directory=listdir()
        self.headers="ID, Condition, Age, Gender, Education, Political_View, Audio_Response, PainThreshold_DIFFERENCE_START_END, PainThreshold_Start, PainThreshold_End, Positive_Affect_Pre, Negative_Affect_Pre, Positive_Affect_Post, Negative_Affect_Post, Positive_Affect_Difference, Negative_Affect_Difference, Self_In_Others "
        self.analgesiaTimer = QTimer()
        window.counter = 0
        self.timesCalled=0
        self.lineInCSV=""
        self.comboCounter=0
        if "Output.csv" not in self.directory:
            file = open("Output.csv", "w")
            file.write(self.headers)
            file.close()
    def assignPartcptID(self): #Assigns each participant an ID that will show on their form
        file = open("Output.csv", "r")
        self.linesofCSV = file.readlines()
        self.participantIDNumber = 0
        for line in self.linesofCSV:
            self.participantIDNumber += 1
        file.close()
        ui.prtcptntIDAssignmtLbl.setText(str(self.participantIDNumber))
    def assignCondition(self): #Assigns each participant a condition
        for line in self.linesofCSV: #The next lines calculate the number of former participants in each condition and add this to the conditionsDictionary
            line = line.strip("\n").split(",")
            if line[1] == "dance":
                self.conditionsDictionary["dance"] += 1
            elif line[1] == "perspective-taking":
                self.conditionsDictionary["perspective-taking"] += 1
            elif line[1] == "combo":
                self.conditionsDictionary["combo"] += 1
            elif line[1] == "control":
                self.conditionsDictionary["control"] += 1
        if (self.participantIDNumber-1) % 4==0: #This line assumes that participants are run in batches of 4. If this changes, change the number in this line
            if self.conditionsDictionary["dance"] == self.conditionsDictionary["perspective-taking"] ==self.conditionsDictionary["combo"] == self.conditionsDictionary["control"]:
                self.condition = choice(self.conditionPossibilities) #
            else: #Uses OrderedDict from the collections library to sort the dictionary into an order dictated by the keys' values
                sortedCondDict=sorted(self.conditionsDictionary.items(), key=itemgetter(1))
                item2 = sortedCondDict[1][0] #Results are then called using sortedCondDict[item in list[0 for key or 1 for value]]
                item1 = sortedCondDict[0][0]
                item3 = sortedCondDict[2][0]
                item4 = sortedCondDict[3][0]
                if sortedCondDict[0][0] == sortedCondDict[1][0]==sortedCondDict[2][0]: #If three conditions are equal and less than the fourth
                    self.condition = choice([sortedCondDict[0][0], sortedCondDict[1][0], sortedCondDict[2][0]])
                elif sortedCondDict[0][0] == sortedCondDict[1][0]: #If two conditions are equal and less than the other two
                    self.condition=choice([sortedCondDict[0][0], sortedCondDict[1][0]])
                else: #If one condition has fewer past participants than the others
                    self.condition = sortedCondDict[0][0]
        elif len(self.linesofCSV)==1: #If there is nothing in the csv besides the headers, randomly choose a condition
            self.condition = choice(self.conditionPossibilities)
        else: #If there were not four people in this batch of the condition yet, assign the condition of the previous participant
            lengthOfCSV = len(self.linesofCSV)-1
            self.linesofCSV[lengthOfCSV]=self.linesofCSV[lengthOfCSV].strip("\n").split(",")
            lastLine=self.linesofCSV[lengthOfCSV]
            self.condition=(lastLine[1])
    def addToCSV (self,contents, file="Output.csv"):
        CSVOpened=open (file, "a")
        CSVOpened.write("\n"+contents)
        CSVOpened.close()
    def addToLine(self,addition):
        self.lineInCSV += addition + ","
        return (self.lineInCSV)
    def endTrial (self): #Ends each trial
        window.close()
    def PANASTestScore(self):
        dictionaryOfResults = self.getPANASResultsDictionary() #Calls a function defined in coming lines
        positiveScore = dictionaryOfResults["Interested"] + dictionaryOfResults["Excited"] + dictionaryOfResults[
                "Strong"] + dictionaryOfResults["Enthusiastic"] + dictionaryOfResults["Proud"] + dictionaryOfResults[
                                "Alert"] + dictionaryOfResults["Inspired"] + dictionaryOfResults["Determined"] + \
                            dictionaryOfResults["Attentive"] + dictionaryOfResults["Active"]
        negativeScore = dictionaryOfResults["Distressed"] + dictionaryOfResults["Upset"] + dictionaryOfResults[
                "Guilty"] + dictionaryOfResults["Scared"] + dictionaryOfResults["Hostile"] + dictionaryOfResults[
                                "Irritable"] + dictionaryOfResults["Ashamed"] + dictionaryOfResults["Nervous"] + \
                            dictionaryOfResults["Jittery"] + dictionaryOfResults["Afraid"]
        self.timesCalled+=1 #Lines below create the PANAS test scores as dictated by PANAS procedures
        if self.timesCalled==1: #This will be called for the PANAS pre-test
            self.PANASPositivePreScore=positiveScore
            self.PANASNegativePreScore=negativeScore
        else: #This will be called for the PANAS post-test
            self.PANASPositivePostScore=positiveScore
            self.PANASNegativePostScore=negativeScore
    def getPANASResultsDictionary(self):#Creates a dictionary with the name and score for each PANAS item with a checked button
        self.dictionaryOfResults = {}
        for item in listofAll:
            for button in item.buttons: #The buttons property is defined below in the QuestionnaireItem class
                if button.isChecked() == True:
                    myPlaceInList = item.buttons.index(button)
                    item.score = item.buttonValues[myPlaceInList]
                    self.dictionaryOfResults[item.objectName()] = item.score
        return (self.dictionaryOfResults)
    def resetPANAS(self): #Resets all items in the PANAS dictionaryOfResults to 0 so that the questionnaire can be done and its results recorded twice
        for item in self.dictionaryOfResults:
            self.dictionaryOfResults[item]=0
        listofAll=[] #Holds all of the PANAS labels and buttons created by objects of the QuestionnaireItem class
    def analgesiaTimerStart(self): #Starts the analgesia timer
        # If the timer is better off invisible, add "ui.Timer1Seconds and ui.Timer2Seconds" to the hide label function at the top of this module
        if window.sender()==ui.Timer1StartButton: #If the function was called by the first analgesia measure, updates Timer1 label
            ui.Timer1StartButton.disconnect() #Prevents multiple presses of the button
            self.whichLabel=ui.Timer1Seconds
        elif window.sender()==ui.Timer2StartButton: #If it was called by the second analgesia measure, updates Timer2 label
            ui.Timer2StartButton.disconnect() #Prevents multiple presses of the button
            self.whichLabel=ui.Timer2Seconds
        window.counter = 0 #This resets the clock counter on the timer window to 0 each time the timer is called
        self.analgesiaTimer.timeout.connect(self.timerEvent)
        self.analgesiaTimer.start(1000)
    def timerEvent(self):
        window.counter += 1
        self.analgesiaTimer.setInterval(1000) #Timer "ticks" every 1 second
        self.whichLabel.setText(str(window.counter))
    def analgesiaTimerStop(self): #Stops the timer and stores result as self.analgesiaMeasure1 or 2
        self.analgesiaTimer.disconnect()
        nextPage()
        if self.whichLabel == ui.Timer1Seconds:
            self.analgesiaMeasure1=int((self.whichLabel.text())) #It also records the first and second analgesia measures
        else:
            self.analgesiaMeasure2=int((self.whichLabel.text()))
    def checkSelfInOther(self): #Checks and records the selfInOther score and shows an error label if it's not recorded
        if ui.selfInOtherSpinbox.value()!=0:
            self.selfInOtherScore=ui.selfInOtherSpinbox.value()
            nextPage() #It also turns the page if the score is recorded
        else:
            ui.SelfInOtherErrorLbl.show()
    def setManipulation(self): #Displays the appropriate instructions based on participant condition
        if self.condition == "dance" or self.condition=="combo":
            ui.dancePartyInstructionLbl.show()
            ui.exptProceedBtn.hide()
        else:
            ui.PLAYBtn.show()
            ui.exptProceedBtn.hide()
            ui.dancePartyBtn.hide()
    def audioResponseRecord(self): # Shows the audio response task after the audio is played (except "dance" condition)
        if self.condition=="combo":
            self.comboCounter+=1
        ui.audioResponseInstrctnLbl.show()
        ui.audioResponseLineEdit.show()
        if self.comboCounter == 0:
            ui.exptProceedBtn.show()
        else:
            ui.comboProceedBtn.show()

#This class creates containers for each PANAS item and creates radiobuttons that correspond to the PANAS Likert scale
class QuestionnaireItem(QWidget):
    def __init__(self, container, list):
        super().__init__(container)
        self.score=0 #The score, as an integer, of any one PANAS item
        self.buttonTitles=["Not at all", "Slightly", "A Little", "Moderately","Quite A Bit", "Extremely"]
        self.buttonValues=[1,2,3,4,5] #Each button title above corresponds to the integer held in its index in this list
        self.buttons=[] #An empty list of buttons for each item
        y=50*(list.index(item))+50 #This sets the vertical spacing for each button
        aLabel=QLabel(self) #These few lines create a label for the PANAS item name, name the labels, and set their colors, font, and placement
        aLabel.setGeometry(0,10,80,16)
        aLabel.setText(item)
        aLabel.setObjectName(item+"Lbl")
        aLabel.setAutoFillBackground(True)
        labelColors=aLabel.palette()
        labelColors.setColor (QPalette.Window, QColor ("orange"))
        labelColors.setColor (QPalette.WindowText, QColor ("white"))
        aLabel.setPalette(labelColors)
        aLabel.setAlignment(Qt.AlignCenter)
        aLabel.setFont(QtGui.QFont("Times", 15, weight=QtGui.QFont.Bold))
        for i in range(5): #These lines set up the five radio buttons for each item's Likert scale
            btn = QRadioButton(self)
            btn.setGeometry(100 + i * 145, 10, 211, 20)
            btn.setText(self.buttonTitles[i]) #These lines iterate through the button text held in buttonTitles to set button text and name them
            btn.setObjectName(self.buttonTitles[i])
            self.buttons.append(btn) #Each button is added to the buttons list
    def checkIfFilled (self, listOfObjects, label): #This method checks that at least one button per PANAS item is checked
        totalItemsEmpty=0 #This counts if, overall per page, any PANAS items were left with an unchecked button
        for item in listOfObjects:
            listOfButtonsPerItem = [] #Creates a list of buttons per item
            for i in range (1,6):
                thisButton=item.children()[i] #Indicates each individual button
                listOfButtonsPerItem.append(thisButton) #Adds each individual button to the list
                checkedButtonsPerItem=0 #Sets the number of checked buttons per item to zero
            for button in listOfButtonsPerItem:#Goes through each item's buttons to see if any are checked
                if button.isChecked()==True:
                    checkedButtonsPerItem+=1
            if checkedButtonsPerItem==0: #If no buttons are checked for an item, an error label will show
                label.show()
                totalItemsEmpty+=1
        if totalItemsEmpty==0: #If all items have a checked button, will proceed to the next page
            nextPage()
    def getValue(self, listOfItems): #This method records the integer number of each item's selected button and adds it to a dictionary called dictionaryOfResults
        dictionaryOfResults={}
        for item in listOfItems:
            for button in item.buttons:
                if button.isChecked()==True:
                    myPlaceInList=item.buttons.index(button)
                    self.score=self.buttonValues[myPlaceInList]
                    dictionaryOfResults[item.objectName()]=self.score

#This code writes the PANAS items on their respective pages by creating a list of the objects that go on each page and a listOfAll containing objects from all pages
dictionaryOfPANAS={}
listOfItems1=[]
listOfItems2=[]
listOfItems3=[]
listOfItems4=[]
listofAll=[]
PANASitems1=["Interested", "Distressed", "Excited", "Upset", "Strong", "Guilty", "Scared", "Hostile", "Enthusiastic", "Proud"]
for item in PANASitems1:
    panasPart1 = QuestionnaireItem(ui.PANAS1Page, PANASitems1)
    panasPart1.setGeometry(10, 50+50*PANASitems1.index(item), 771, 41)
    panasPart1.setObjectName(item)
    dictionaryOfPANAS[panasPart1.objectName()]=0
    listOfItems1.append(panasPart1)
    listofAll.append(panasPart1)
    panasPart3 = QuestionnaireItem(ui.PANAS3Page, PANASitems1)
    panasPart3.setGeometry(10, 50+50*PANASitems1.index(item), 771, 41)
    panasPart3.setObjectName(item)
    dictionaryOfPANAS[panasPart3.objectName()]=0
    listOfItems3.append(panasPart3)
    listofAll.append(panasPart3)

PANASitems2=["Irritable", "Alert", "Ashamed", "Inspired", "Nervous", "Determined", "Attentive", "Jittery", "Active", "Afraid"]
for item in PANASitems2:
    panasPart2=QuestionnaireItem(ui.PANAS2Page, PANASitems2)
    panasPart2.setGeometry(10,50+50*PANASitems2.index(item), 771, 41)
    panasPart2.setObjectName(item)
    dictionaryOfPANAS[panasPart2.objectName()]=0
    listOfItems2.append(panasPart2)
    listofAll.append(panasPart2)
    panasPart4=QuestionnaireItem(ui.PANAS4Page, PANASitems2)
    panasPart4.setGeometry(10,50+50*PANASitems2.index(item), 771, 41)
    panasPart4.setObjectName(item)
    dictionaryOfPANAS[panasPart4.objectName()]=0
    listOfItems4.append(panasPart4)
    listofAll.append(panasPart4)

# These are intermediary functions that pass the correct PANAS page to a function that checks if all items have been filled out
# Intermediary functions are needed because the signal emitted from the button being clicked cannot carry an argument indicating which page to check
def passToCheckPANAS1():
    panasPart1.checkIfFilled(listOfItems1, ui.PANASErrorLbl1)
def passToCheckPANAS2():
    panasPart2.checkIfFilled(listOfItems2, ui.PANASErrorLbl2)
def passToCheckPANAS3():
    panasPart3.checkIfFilled(listOfItems3, ui.PANASErrorLbl3)

def hideDialogue(): #Hides the speech bubble and dialogue for the "me" player in Cyberball
    ui.passBallLbl.hide()
    ui.speechbubbleLbl.hide()

def startGame(): #Sets the ball position upon starting Cyberball
    ui.ballLabel.setGeometry(470,450,61,61)

def passToMe(): #Activates the "me" player dialogue bubble in Cyberball and hides it after 2 seconds
    ui.passBallLbl.show()
    ui.speechbubbleLbl.show()
    dialogueTimer=QTimer()
    dialogueTimer.singleShot(2000,hideDialogue)

hideDialogue() #Calls the fucntion that hides the "me" player dialogue
startGame() #Sets up the Cyberball ball's initial geometry

window.show() #shows the window for the whole GUI
