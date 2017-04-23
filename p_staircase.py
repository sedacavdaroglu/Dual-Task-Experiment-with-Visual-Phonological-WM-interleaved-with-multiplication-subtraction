# -*- coding: cp1252 -*-
"""measure your JND in horizontal visuospatial working memory using a staircase method"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event,logging, gui #import some libraries from PsychoPy
from psychopy import *
from psychopy.constants import *  # things like STARTED, FINISHED
import random #import some libraries from python
from random import choice
import array
import numpy
import os  # handy system and path functions
import pylab

#create window and stimuli
#mywin = visual.Window([1366,768],allowGUI=True, monitor='testMonitor', units='pix')
#mywin = visual.Window([1920,1080],allowGUI=True, monitor='testMonitor', units='pix')
mywin = visual.Window([800,800],units='pix',fullscr = True)
mywin.setMouseVisible(False) #set the mouse invisible

key_resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp.status = NOT_STARTED

                
#variables for working memory tasks
red = (1.0,0,0)
black = (-1,-1,-1)
listOfConsonants =  ['B','C','D','F','G','H','J','K','L','M','N','P','R','S','T','Z'] #list of consonants to be used during the experi
testLetters = ['b','c','d','f','g','h','j','k','l','m','n','p','r','s','t','z'] 
#listOfConsonants = array.array('c','BCDFGHKLMNPRSTVWZ') #list of consonants to be used during phonological and visuospatial wm trials
listSize = len(listOfConsonants)
letDur = 0.4
testLetDur =5 #the duration of the test letter
blockDur = 300 #the duration of each block
fixDur = 1.7 #the duration of the fixation cross


delayVisual = 2.0 #the delay period between visuospatial working memory stimulus and answer
testLetter = '' #the test letter for visuospatial working memory answer phase


# Initialize components for Routine "trial"
trialClock = core.Clock()
letterClock = core.Clock()
experimentClock = core.Clock()
circleClock = core.Clock()
btwLetsClock = core.Clock()

prob = visual.TextStim(mywin, ori=0, name='prob',
    text='nonsense',
    font='Arial',
    pos=[0, 0], height=20, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

msg = visual.TextStim(mywin, text='', font='', pos=(0,0),
                      depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb',
                      opacity=1.0, units='norm', ori=0.0, height=20, antialias=True,
                      bold=False, italic=False, alignHoriz='center', alignVert='center',
                      fontFiles=[], wrapWidth=None, name='', autoLog=True)

probeLetter = visual.TextStim(mywin, ori=0, name='probeLetter',
    text=testLetter,
    font='Arial',
    pos=[0.0,0.0], height=20, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    )

pauseMsg = visual.TextStim(mywin, ori=0, name='pauseMsg',
    text='To continue the experiment, press any key',
    font='Arial',
    pos=[0.0,0.0], height=20, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    )

fixCircle = visual.Circle(mywin,pos=(0,0),radius=10, edges=32, lineColor = red, fillColor = red)
smallCircle = visual.Circle(mywin,pos=(0,0),radius=1, edges=32, lineColor = black, fillColor = black)
##############################################################################################
#-------------------base functions to be used during the experiment---------------------------
##############################################################################################
def my_shuffle(array):
        random.shuffle(array)
        return array
##############################################################################################   
#draw the fixation circle in between task and answer
def draw_circle(color,dur):
    fixCircle = visual.Circle(mywin,pos=(0,0),radius=10, edges=32, lineColor = color, fillColor = color)
    smallCircle = visual.Circle(mywin,pos=(0,0),radius=1, edges=32, lineColor = black, fillColor = black)
    t = 0
    circleClock.reset()
    #pause, so you get a chance to see it!
    while t < dur:       
        t = circleClock.getTime()
        #draw the stimuli and update the window
        fixCircle.setAutoDraw(True)
        smallCircle.setAutoDraw(True)
        mywin.flip()
    fixCircle.setAutoDraw(False)
    smallCircle.setAutoDraw(False)

##############################################################################################
#draw the letters on the screen 
def drawLets(letters,locs,span):
    global msg
    for i in range(0,span):
        msg = visual.TextStim(win=mywin, text=listOfConsonants[int(letters[i])], font='', pos=(locs[i],0),
                              depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb',
                              opacity=1.0, ori=0.0, height=20, antialias=True,
                              bold=False, italic=False, alignHoriz='center', alignVert='center',
                              fontFiles=[], wrapWidth=None, name='', autoLog=False)

        msg.draw()
    mywin.update()
    t = 0
    letterClock.reset() #start the letter clock
    while t < letDur*span:
        t = letterClock.getTime()
        # check for quit (the [Esc] key)
        if event.getKeys(["escape"]):
            mywin.close()
            core.quit()
    msg.setAutoDraw(False)
    mywin.update()
##############################################################################################
#draw the letters on the screen 
def drawTestLets(letters,locs,span,trueOrFalse):
    global msg
    if trueOrFalse == 0:
        tmp = numpy.zeros(span-1)
        for i in range(1,span):
            tmp[i-1] = i
        let1 = choice(tmp)
        let2 = choice(tmp)
        while let1== let2:
            let1 = choice(tmp)
        print 'let1',let1,'let2',let2
        l1 = letters[let1]
        l2 = letters[let2]
        letters[let1] = l2
        letters[let2] = l1
    for i in range(0,span):
        msg = visual.TextStim(win=mywin, text=testLetters[int(letters[i])], font='', pos=(locs[i],0),
                              depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb',
                              opacity=1.0, ori=0.0, height=20, antialias=True,
                              bold=False, italic=False, alignHoriz='center', alignVert='center',
                              fontFiles=[], wrapWidth=None, name='', autoLog=False)

        msg.draw()
    mywin.update()
##############################################################################################
#determine the letters to be used during the current WM trial --> input parameters: number of
#letters to be tested, length of the list of letters to be used, output--> location of letters to be used 
def wmLets(span):
    i = 0
    letsUsed = numpy.zeros(span)
    #choose the first letter to be used
    letsUsed[0] = random.randint(0,listSize-1) #pick the position from the array of consonants
    #choose the letters to be used during the current working memory trial
    for i in range(0,span):
        curLet = random.randint(0,listSize-1) #pick the position from the array of consonants
        #check if the chosen letter has already been used or not
        j = 0
        while j in range(0,i):
            if curLet == letsUsed[j]:
                j = -1
                curLet = random.randint(0,listSize-1) #pick a different letter from the list
            j += 1
        letsUsed[i] = curLet
        i += 1
    return letsUsed

##############################################################################################
#determine the location for letters to be used during the current WM trial --> input parameters:
#number of letters to be tested, number of possible locations
def wmLocs(span):
    #choose the first location to be used
    locs =numpy.zeros(span)
    #choose the locations to be used during the current working memory trial
    for i in range(1,int(span/2)+1):
        locs[i-1] = -i*20
    locs[int(span/2)] = 0
    for j in range(int(span/2)+1,span):
        locs[j] = (j-int(span/2))*20
    return locs
 ##############################################################################################
############################# RUN THE EXPERIMENT #############################################
def run_p_staircase(participant):
    corrAnsSide = participant%2 #left if participant no is odd, right if even
    # Setup files for saving
    if not os.path.isdir('p_staircase'):
        os.makedirs('p_staircase')  # if this fails (e.g. permissions) we will get error
    fileName = 'p_staircase' + os.path.sep + 'subject_'+'%s' %(participant)
    logFile = logging.LogFile(fileName+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
    
    trueOrFalse = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]#,0,1,0,1,0,1,0,1,0]#,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
    indxes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    #make a text file to save data
    #fileName = expInfo['participant'] + expInfo['date']
    dataFile = open(fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
    dataFile.write('targetSide,oriIncrement,correct\n')


    #create the staircase handler
    staircase = data.StairHandler(startVal = 3,
                              stepType = 'lin', stepSizes=[-1],
                              nTrials=25, nUp=3, nDown=3,  #will home in on the 80% threshold
                              minVal = 1, maxVal = 9)

    
    #display instructions and wait
    message1 = visual.TextStim(mywin, pos=[0,+130],text='BUCHSTABEN')
    message2 = visual.TextStim(mywin, pos=[0,30], text='')
    message3 = visual.TextStim(mywin, pos=[0,-70],text='Drucken Sie eine beliebige Taste, um zu beginnen.')
    message1.draw()
    message2.draw()
    message3.draw()
    mywin.update()#to show our newly drawn 'stimuli'
    #pause until there's a keypress
    event.waitKeys()
    intensities = []
    responses = []
    j = 0
    trueOrFalse = my_shuffle(trueOrFalse)
    firstTrial = 1
    for thisIncrement in staircase: #will step through the staircase        
        if firstTrial != 1:
            fixCircle.setAutoDraw(False)
            smallCircle.setAutoDraw(False)
            mywin.flip()
        firstTrial = 0
        core.wait(0.3)
        #determine the location and the letters
        x = int(thisIncrement)
        if x < 3:
            x = 3
            thisIncrement = 3
        elif x > 9:
            x = 9
            thisIncrement = 9
        lets = wmLets(x)
        intensities.append(int(thisIncrement))

        locsX = wmLocs(x)
        usedLets = []
        for col in range(0,x):
            usedLets.append(listOfConsonants[int(lets[col])])

        #draw all stimuli
        draw_circle(red,fixDur)
        drawLets(lets,locsX,x)
        draw_circle(red,7.2)
        fixCircle.setAutoDraw(False)
        smallCircle.setAutoDraw(False)
        mywin.update()
        #draw the test sequence
        drawTestLets(lets,locsX,x,trueOrFalse[j%20])

        if trueOrFalse[j]%2 == 1: targetSide = corrAnsSide
        else: targetSide = 1-corrAnsSide
        thisResp=None
        t = 0
        trialClock.reset()  # clock
        key_resp.status = NOT_STARTED
        while t < testLetDur:
            # get current time
            t = trialClock.getTime()

            # *key_resp* updates
            if key_resp.status == NOT_STARTED:
                key_resp.status = STARTED
                # keyboard checking is just starting
                key_resp.clock.reset()  # now t=0
                event.clearEvents()
                
            if key_resp.status == STARTED:  # only update if being drawn
                theseKeys = event.getKeys()
                if len(theseKeys) > 0:  # at least one key was pressed
                    t = testLetDur
                    key_resp.keys = theseKeys[-1]  # just the last key pressed
                    
                if key_resp.keys=='lctrl':
                    if targetSide== 1: thisResp = 1#correct
                    else: thisResp = 0             #incorrect
                elif key_resp.keys=='rctrl':
                    if targetSide== 0: thisResp = 1#correct
                    else: thisResp = 0

 
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                mywin.close()
                core.quit()
        msg.setAutoDraw(False)
        key_resp.status = STOPPED
        

        # check responses
        if len(key_resp.keys) == 0:  # No response was made
            thisResp = 0    # failed to respond (incorrectly)
        #add the data to the staircase so it can calculate the next level
        if thisResp == None:
            thisResp = 0
        staircase.addData(thisResp)
        staircase.calculateNextIntensity()
        responses.append(thisResp)
        dataFile.write('%i,%i,%i\n' %( trueOrFalse[j%25], thisIncrement, thisResp))
        j += 1


    #staircase has ended
    dataFile.close()
    staircase.saveAsPickle(fileName) #special python binary file to save all the info
    mywin.close()