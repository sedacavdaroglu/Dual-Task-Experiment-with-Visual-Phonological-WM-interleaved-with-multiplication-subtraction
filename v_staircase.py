# -*- coding: ISO-8859-1 -*-
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui #import some libraries from PsychoPy
from psychopy import *
from psychopy.constants import *  # things like STARTED, FINISHED
import random #import some libraries from python
from random import choice
import array
import numpy
import os  # handy system and path functions
import pylab

    
mywin = visual.Window([800,800],units='pix',fullscr = True)
mywin.setMouseVisible(False) #set the mouse invisible

key_resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp.status = NOT_STARTED

#variables for color  duration etc...

blue = (0,0,1)
black = (-1,-1,-1)
letDur = 0.4 #the duration of each letter
testLetDur = 5 #the duration of the test letter
blockDur = 300 #the duration of each block
fixDur = 1.7 #the duration of the fixation cross
scale =188/2#the scale of the window area to be used for the experiment-->arranged according to visual field calculation
delayVisual = 2.0 #the delay period between visuospatial working memory stimulus and answer
testLetter = 'O' #the test letter for visuospatial working memory answer phase
stepDir = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,3,4,1,2,3,4,1,2,3,4]#,1,2,3,4] #the four directions for the probe letter
allLocs = [0,1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24]
random.shuffle(stepDir)
#xCoor = [-5*scale/6,-scale/2,-scale/6,5*scale/6,scale/2,scale/6,-5*scale/6,-scale/2,-scale/6,5*scale/6,scale/2,scale/6,-5*scale/6,-scale/2,-scale/6,5*scale/6,scale/2,scale/6,5*scale/6,-scale/2,-scale/6,5*scale/6,scale/2,scale/6,5*scale/6,-scale/2,-scale/6,5*scale/6,scale/2,scale/6,5*scale/6,-scale/2,-scale/6,5*scale/6,scale/2,scale/6]
#yCoor = [5*scale/6,5*scale/6,5*scale/6,5*scale/6,5*scale/6,5*scale/6,scale/2,scale/2,scale/2,scale/2,scale/2,scale/2,scale/6,scale/6,scale/6,scale/6,scale/6,scale/6,-5*scale/6,-5*scale/6,-5*scale/6,-5*scale/6,-5*scale/6,-5*scale/6,-scale/2,-scale/2,-scale/2,-scale/2,-scale/2,-scale/2,-scale/6,-scale/6,-scale/6,-scale/6,-scale/6,-scale/6]
xCoor = [-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5]
yCoor = [4*scale/5,4*scale/5,4*scale/5,4*scale/5,4*scale/5,2*scale/5,2*scale/5,2*scale/5,2*scale/5,2*scale/5,0,0,0,0,0,-2*scale/5,-2*scale/5,-2*scale/5,-2*scale/5,-2*scale/5,-4*scale/5,-4*scale/5,-4*scale/5,-4*scale/5,-4*scale/5]

fixCircle = visual.Circle(mywin,pos=(0,0),radius=10, edges=32, lineColor = blue, fillColor = blue)

key_resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp.status = NOT_STARTED


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

smallCircle = visual.Circle(mywin,pos=(0,0),radius=1, edges=32, lineColor = black, fillColor = black)
##############################################################################################
#-------------------base functions to be used during the experiment---------------------------
##############################################################################################
def my_shuffle(array):
        random.shuffle(array)
        return array    
##############################################################################################   
def draw_grid(x,y):
    for i in range(0,x+1):
        #lines for the grid
        shapeStim1 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale+i*2*scale/x,scale),(-scale+i*2*scale/x,-scale)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
        shapeStim1.setAutoDraw(True)
    for i in range(0,y+1):
        #lines for the grid
        shapeStim2 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale,scale-i*2*scale/y),(scale,scale-i*2*scale/y)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
        shapeStim2.setAutoDraw(True)
    mywin.flip()
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
def drawLocs(locs,span):   
    print 'locs',locs
    global msg    
    fixCircle = visual.Circle(mywin,radius=10, pos=(0,0),edges=32, lineColor = blue, fillColor = blue)
    smallCircle = visual.Circle(mywin,pos=(0,0), radius=1, edges=32, lineColor = black, fillColor = black)
    fixCircle.setAutoDraw(True)
    smallCircle.setAutoDraw(True)
    for i in range(0,span):
        msg = visual.TextStim(win=mywin, text='O', font='', pos=(xCoor[int(locs[i])],yCoor[int(locs[i])]),
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
    fixCircle.setAutoDraw(False)
    smallCircle.setAutoDraw(False)
    msg.setAutoDraw(False)
    mywin.update()
##############################################################################################
#determine the location for letters to be used during the current WM trial --> input parameters:
#number of letters to be tested, number of possible locations
def visualLocs(span):
    global xCoor,yCoor,allLocs
    locsUsed = numpy.zeros(span) #grid number of locations to be used
    locsX = numpy.zeros(span) #x coordinate of locations to be used
    locsY = numpy.zeros(span) #y coordinate of locations to be used
    #choose the locations to be used during the current working memory trial
    for i in range(0,span):
        curLoc = choice(allLocs)
        #check if the chosen location has already been used or not
        j = 0
        while 0<=j<i:
            #print 'BURA3'
            if curLoc == locsUsed[j]:
                curLoc = choice(allLocs)
                j = -1
            j += 1          
        locsUsed[i] = curLoc
    #print 'locs', locsUsed
    return locsUsed
##############################################################################################
#find the prob location
def findProb(locsUsed,dir,span):
    global xCoor,yCoor,allLocs
    curLoc= choice(locsUsed)
    indx = curLoc
    tmp = 0
    #print 'curLoc',curLoc
    while curLoc in locsUsed and tmp < 20:
        tmp = tmp+1
        #print 'BURA4'
        #print 'indx',indx,'span',span,'locsUsed',locsUsed
        curLoc=choice(locsUsed)
        indx = curLoc
        if dir == 1 and curLoc >4 and curLoc != 17:
            curLoc = curLoc - 5
        elif dir  == 2 and curLoc < 20 and curLoc != 7:
            curLoc = curLoc + 5
        elif dir  == 3 and curLoc%5 != 4 and curLoc != 11:
            curLoc  = curLoc +1
        elif dir == 4 and curLoc%5 != 0 and curLoc != 13:
            curLoc = curLoc -1
        if tmp == 20 and dir == 4:
            tmp = 0
            dir = dir-1
        elif tmp == 20 and dir == 1:
            tmp = 0 
            dir = dir +1
        elif tmp == 20:
            tmp = 0 
            dir = dir -1
    return indx,curLoc,dir
##############################################################################################
#draw the prob locations on the screen 
def drawTestLocs(locs,probeIndx,probeLoc,span):   
    global msg,fixCircle,smallCircle
    fixCircle = visual.Circle(mywin,pos=(0,0), radius=10, edges=32, lineColor = blue, fillColor = blue)
    smallCircle = visual.Circle(mywin,pos=(0,0), radius=1, edges=32, lineColor = black, fillColor = black)
    fixCircle.setAutoDraw(True)
    smallCircle.setAutoDraw(True)
    for i in range(0,span):
        if locs[i] == int(probeIndx):
            #print 'probLoc',probeLoc
            msg = visual.TextStim(win=mywin, text='O', font='', pos=(xCoor[int(probeLoc)],yCoor[int(probeLoc)]),
                                  depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb',
                                  opacity=1.0, ori=0.0, height=20, antialias=True,
                                  bold=False, italic=False, alignHoriz='center', alignVert='center',
                                  fontFiles=[], wrapWidth=None, name='', autoLog=False)
            msg.draw()
        else:
            msg = visual.TextStim(win=mywin, text='O', font='', pos=(xCoor[int(locs[i])],yCoor[int(locs[i])]),
                                  depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb',
                                  opacity=1.0, ori=0.0, height=20, antialias=True,
                                  bold=False, italic=False, alignHoriz='center', alignVert='center',
                                  fontFiles=[], wrapWidth=None, name='', autoLog=False)

            msg.draw()
    mywin.update()
##############################################################################################
#draw the prob locations on the screen 
def drawTestLocsSame(locs,span):
    global msg,fixCircle,smallCircle
    fixCircle = visual.Circle(mywin,pos=(0,0), radius=10, edges=32, lineColor = blue, fillColor = blue)
    smallCircle = visual.Circle(mywin,pos=(0,0), radius=1, edges=32, lineColor = black, fillColor = black)
    fixCircle.setAutoDraw(True)
    smallCircle.setAutoDraw(True)
    for i in range(0,span):
        msg = visual.TextStim(win=mywin, text='O', font='', pos=(xCoor[int(locs[i])],yCoor[int(locs[i])]),
                              depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb',
                              opacity=1.0, ori=0.0, height=20, antialias=True,
                              bold=False, italic=False, alignHoriz='center', alignVert='center',
                              fontFiles=[], wrapWidth=None, name='', autoLog=False)

        msg.draw()
    mywin.update()
##############################################################################################
############################# RUN THE EXPERIMENT #############################################
def run_v_staircase(participant):
    corrAnsSide = participant%2 #left if participant no is odd, right if even
    global stepDir
    if not os.path.isdir('v_staircase'):
        os.makedirs('v_staircase')  # if this fails (e.g. permissions) we will get error
    fileName = 'v_staircase' + os.path.sep + 'subject_'+str(participant)
    logFile = logging.LogFile(fileName+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    #make a text file to save data
    ##fileName = expInfo['participant'] + expInfo['date']
    dataFile = open(fileName+'.csv', 'w')#a simple text file with 'comma-separated-values'
    dataFile.write('targetSide,oriIncrement,correct\n')


    #create the staircase handler
    staircase = data.StairHandler(startVal = 3,
                              stepType = 'lin', stepSizes=[-1],
                              nTrials=25, nUp=3, nDown=3,  #will home in on the 80% threshold
                              minVal = 1, maxVal =7)

    
    #display instructions and wait
    message1 = visual.TextStim(mywin, pos=[0,+130],text='POSITIONEN')
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
    firstTrial = 1
    draw_grid(5,5)
    for thisIncrement in staircase: #will step through the staircase
        if firstTrial != 1:
            fixCircle.setAutoDraw(False)
            smallCircle.setAutoDraw(False)
            mywin.flip()
        firstTrial = 0
        core.wait(0.3)
        #determine the location and the letters
        lets = ['O']
        x = int(thisIncrement)
        if x < 1:
            x = 1
            thisIncrement = 1
        elif x > 7:
            x = 7
            thisIncrement = 7
        intensities.append(int(thisIncrement))
        for i in range (0,x):
            lets.append('O')
        locs = visualLocs(x)

        #draw all stimuli
        draw_circle(blue,fixDur)
        drawLocs(locs,x)
        draw_circle(blue,7.2)
        if stepDir[j%25] != 0:
            indx,probLoc,dir = findProb(locs,stepDir[j%25],x)
            drawTestLocs(locs,indx,probLoc,x)
        else:
            drawTestLocsSame(locs,x)

        
        t = 0
        trialClock.reset()  # clock
        if stepDir[j] == 0: targetSide = corrAnsSide
        else: targetSide = 1-corrAnsSide
        thisResp=None
        key_resp.status = NOT_STARTED
           
        while t < testLetDur:
            # get current time
            t = trialClock.getTime()
            # *key_resp* updates
            if key_resp.status == NOT_STARTED:
                key_resp.status = STARTED
                # keyboard checking is just starting
                key_resp.clock.reset()  # now
                t=0
                event.clearEvents()
                
            if key_resp.status == STARTED:  # only update if being drawn
                theseKeys = event.getKeys()
                if len(theseKeys) > 0:  # at least one key was pressed
                    t = testLetDur
                    key_resp.keys = theseKeys[-1]  # just the last key pressed
                    # was this 'correct'?
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


        key_resp.status = STOPPED
        #stop drawing the test letter
        #fixCircle.setAutoDraw(False)
        msg.setAutoDraw(False)
        mywin.update()
        
       # check responses
        if len(key_resp.keys) == 0:  # No response was made
            thisResp = 0    # failed to respond (incorrectly)

        #add the data to the staircase so it can calculate the next level    
        if thisResp == None: thisResp = 0
        staircase.addData(thisResp)
        staircase.calculateNextIntensity()
        responses.append(thisResp)
        dataFile.write('%i,%i,%i\n' %(targetSide, thisIncrement, thisResp))
        j += 1

    #staircase has ended
    dataFile.close()
    staircase.saveAsPickle(fileName) #special python binary file to save all the info
    mywin.close()