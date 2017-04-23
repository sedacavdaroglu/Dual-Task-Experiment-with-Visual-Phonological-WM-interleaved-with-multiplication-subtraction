from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event,logging, gui #import some libraries from PsychoPy
from psychopy import *
from psychopy.constants import *  # things like STARTED, FINISHED
from random import choice
#from win32com.client import Dispatch #for writing stimuli onto excell file
import random #import some libraries from python
import array
import numpy
import os  # handy system and path functions
import pylab
import create_stimuli
try:
    import openpyxl
    from openpyxl.cell import get_column_letter
    from openpyxl.reader.excel import load_workbook
    haveOpenpyxl=True
except:
    haveOpenpyxl=False

# Store info about the experiment session
expName = 'Experiment'
expInfo = {'participant':'','session':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
participant = 'subject_' + expInfo['participant'] +''
subNo = int(expInfo['participant'])
groupNo = int((int(expInfo['participant'])%4)/2)+1
#groupNo = 1
participantNo = int(expInfo['participant'])
session = int(expInfo['session'])
##############################################################################################    
#randomly decide whether visuospatial or phonological span task will be conducted first
sessions1 = [1,1]
random.shuffle(sessions1)
if session == 0 and sessions1[0] == 1:
    import p_staircase
    p_staircase.run_p_staircase(participantNo)
#    import v_staircase
#    v_staircase.run_v_staircase(participantNo)
elif session == 0 and sessions1[0] == 2:
    import v_staircase
    v_staircase.run_v_staircase(participantNo)
    import p_staircase
    p_staircase.run_p_staircase(participantNo)
calcOrder = [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

#print groupNo
if  groupNo == 1:
    calcFile1 = 'multiplications'+str(calcOrder[subNo%6][0])+'.xlsx'
    calcFile2 = 'multiplications'+str(calcOrder[subNo%6][1])+'.xlsx'
    calcFile3 = 'multiplications'+str(calcOrder[subNo%6][2])+'.xlsx'

elif groupNo == 2:
    calcFile1 = 'subtractions'+str(calcOrder[subNo%6][0])+'.xlsx'
    calcFile2 = 'subtractions'+str(calcOrder[subNo%6][1])+'.xlsx'
    calcFile3 = 'subtractions'+str(calcOrder[subNo%6][2])+'.xlsx'


if groupNo == 1:
    create_stimuli.run_create_stimuli(participantNo,groupNo,'tmp.xlsx','p',20)
    create_stimuli.run_create_stimuli(participantNo,groupNo,calcFile1,'pm',28)
    create_stimuli.run_create_stimuli(participantNo,groupNo,'tmp.xlsx','v',20)
    create_stimuli.run_create_stimuli(participantNo,groupNo,calcFile2,'vm',28)
elif groupNo == 2:
    create_stimuli.run_create_stimuli(participantNo,groupNo,'tmp.xlsx','p',20)
    create_stimuli.run_create_stimuli(participantNo,groupNo,calcFile1,'ps',28)
#    create_stimuli.run_create_stimuli(participantNo,groupNo,'tmp.xlsx','v',20)
#    create_stimuli.run_create_stimuli(participantNo,groupNo,calcFile2,'vs',28)


# Store info about the experim1ent session
if not os.path.isdir('mydata'):
    os.makedirs('mydata')  # if this fails (e.g. permissions) we will get error
filename = 'mydata' + os.path.sep + participant #name of the results file

thisExp = data.ExperimentHandler(name='WorkingMemory', version='',
    extraInfo='', runtimeInfo=None,
    originPath=None,                                                     
    savePickle=True, saveWideText=True,
    dataFileName='')
stim = []
trials = data.TrialHandler(stim,1)
trials.data.addDataType('probAnsCorrOrNot')
trials.data.addDataType('probRT')
trials.data.addDataType('corrOrNot')
trials.data.addDataType('RT')
trials.data.addDataType('probAns')


trialsCalc = data.TrialHandler(stim,1)
trialsCalc.data.addDataType('probAnsCorrOrNot')
trialsCalc.data.addDataType('probRT')

#some handy variables for coloring etc
green = (0,1.0,0)
white = (1.0,1.0,1.0)
red = (1.0,0,0)
blue = (0,0,1)
black = (-1,-1,-1)
gray = (0,0,0)

#variables for working memory tasks
letDur = 0.4 #the duration of each letter
testLetDur = 4 #the duration of the test letter
fixDur = 2.0 #the duration of the fixation cross
delayVisual = 2.0 #the delay period between visuospatial working memory stimulus and answer
blockDur = 300 #5 mins of block, then the subject can take a break
testLetter = 'O' #the test letter for visuospatial working memory answer phase

calcDur = 3.0 #the display period of calculation
stepSize = 15
scale = 188/2 #the part of the screen that will be used, in pixelss
listOfConsonants =  ['B','C','D','F','G','H','J','K','L','M','N','P','R','S','T','Z'] #list of consonants to be used during the experi
testLetters = ['b','c','d','f','g','h','j','k','l','m','n','p','r','s','t','z'] 

#output variables
probAnsCorrOrNot = []
probRT = []
corrOrNot = []
RT = []
probAns = []
countProbAnsCorrOrNot= 0
countProbRT= 0
countCorrOrNot = 0
countRT= 0
countProbAns = 0
ansSides = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
random.shuffle(ansSides)
trialNo = 0
runOrder = [[6, 4, 5, 7, 3], [3, 7, 4, 5, 6], [4, 3, 5, 7, 6], [4, 3, 7, 6, 5], [5, 7, 4, 6, 3], [6, 4, 7, 5, 3], [4, 6, 3, 7, 5], [6, 7, 5, 3, 4], [7, 5, 6, 3, 4], [5, 6, 4, 3, 7], [7, 6, 5, 4, 3], [6, 4, 3, 5, 7], [6, 5, 4, 3, 7], [5, 6, 3, 4, 7], [3, 7, 4, 5, 6], [6, 4, 3, 7, 5], [7, 3, 4, 5, 6], [7, 6, 4, 5, 3], [5, 7, 4, 6, 3], [5, 4, 7, 3, 6], [3, 7, 4, 5, 6], [6, 7, 4, 3, 5], [7, 3, 6, 4, 5], [7, 3, 5, 4, 6]]
#runOrder = [3,3,3,3,3]
#create a window
#mywin = visual.Window([1920,1200],monitor="testMonitor", units="pix")
#mywin = visual.Window([1280,1024],monitor="testMonitor", units="pix",fullscr = True)
mywin = visual.Window([800,800],units = 'pix',color = gray,fullscr = True)
mywin.setMouseVisible(False) #set the mouse invisible
#mywin = visual.Window([800,800],units = 'pix',fullscr = True)



key_resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp.status = NOT_STARTED


cont_key = event.BuilderKeyResponse() # for handling the breaks in between blocks
cont_key.status = NOT_STARTED

# Initialize components for Routine "trial"
trialClock = core.Clock() 
letterClock = core.Clock()
experimentClock = core.Clock()
calcClock = core.Clock()
circleClock = core.Clock()
globalClock = core.Clock()
blockClock = core.Clock()

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

fixCircle = visual.Circle(mywin,radius=0.04, edges=32, lineColor = red, fillColor = red)
smallCircle = visual.Circle(mywin,radius=1, pos=(0,0),edges=32, lineColor = black, fillColor = black)

xCoor = [-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5,-4*scale/5,-2*scale/5,0,2*scale/5,4*scale/5]
yCoor = [4*scale/5,4*scale/5,4*scale/5,4*scale/5,4*scale/5,2*scale/5,2*scale/5,2*scale/5,2*scale/5,2*scale/5,0,0,0,0,0,-2*scale/5,-2*scale/5,-2*scale/5,-2*scale/5,-2*scale/5,-4*scale/5,-4*scale/5,-4*scale/5,-4*scale/5,-4*scale/5]


#probeLetter = visual.TextStim(mywin, name = 'probeLetter', text=testLetter, font='', pos=(0, 0), depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, units='', ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center', fontFiles=[], wrapWidth=None, autoLog=True)
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

multSign = visual.TextStim(mywin, text='   *   ', font='', pos=(0, 0), depth=0, rgb=None,
                      color=black, colorSpace='rgb', opacity=1.0, 
                      ori=0.0, height=20, antialias=True, bold=False, italic=False,
                      alignHoriz='center', alignVert='center', fontFiles=[],
                      wrapWidth=None, name='', autoLog=True)
                      
subSign = visual.TextStim(mywin, text='   -   ', font='', pos=(0, 0), depth=0, rgb=None,
                      color=black, colorSpace='rgb', opacity=1.0, 
                      ori=0.0, height=20, antialias=True, bold=False, italic=False,
                      alignHoriz='center', alignVert='center', fontFiles=[],
                  wrapWidth=None, name='', autoLog=True)
shapeStim1 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale,scale),(-scale,-scale)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim2 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale+2*scale/5,scale),(-scale+2*scale/5,-scale)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim3 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale+2*2*scale/5,scale),(-scale+2*2*scale/5,-scale)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim4 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale+3*2*scale/5,scale),(-scale+3*2*scale/5,-scale)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim5 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale+4*2*scale/5,scale),(-scale+4*2*scale/5,-scale)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim6 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale+5*2*scale/5,scale),(-scale+5*2*scale/5,-scale)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim7 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale,scale),(scale,scale)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim8 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale,scale-2*scale/5),(scale,scale-2*scale/5)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim9 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale,scale-2*2*scale/5),(scale,scale-2*2*scale/5)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim10 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale,scale-3*2*scale/5),(scale,scale-3*2*scale/5)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim11 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale,scale-4*2*scale/5),(scale,scale-4*2*scale/5)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
shapeStim12 = visual.ShapeStim(win=mywin, lineWidth=1.0, lineColor=(1.0, 1.0, 1.0), lineColorSpace='rgb',
                                         fillColor=(0.0,0.0,0.0), fillColorSpace='rgb',
                                         vertices=((-scale,scale-5*2*scale/5),(scale,scale-5*2*scale/5)), pos=(0, 0),
                                         size=1, ori=0.0, opacity=0.5, depth=0, interpolate=True,
                                         lineRGB=None, fillRGB=None, name='', autoLog=True)
##############################################################################################
#------------------------------base functions to be used during the experiment-----------------------------------------
##############################################################################################
#draw the fixation circle in between task and answer
def draw_circle(color,dur,mywin):
    t = globalClock.getTime()
    fixCircle = visual.Circle(mywin,radius=10, pos=(0,0),edges=32, lineColor = color, fillColor = color)
    smallCircle = visual.Circle(mywin,radius=1, pos=(0,0),edges=32, lineColor = black, fillColor = black)
    #draw the stimuli and update the window
    t1 = 0
    circleClock.reset()
    while t1 < dur:
        t1 = circleClock.getTime()
        #draw the stimuli and update the window
        fixCircle.setAutoDraw(True)
        smallCircle.setAutoDraw(True)
        mywin.flip()
        t = globalClock.getTime()
    
    fixCircle.setAutoDraw(False)    
    smallCircle.setAutoDraw(False)
    mywin.update()
##############################################################################################
def draw_grid(x,y):
    global shapeStim1,shapeStim2,shapeStim3,shapeStim4,shapeStim5,shapeStim6,shapeStim7,shapeStim8,shapeStim9,shapeStim10,shapeStim11,shapeStim12S
    shapeStim1.setAutoDraw(True)
    shapeStim2.setAutoDraw(True)
    shapeStim3.setAutoDraw(True)
    shapeStim4.setAutoDraw(True)
    shapeStim5.setAutoDraw(True)
    shapeStim6.setAutoDraw(True)
    shapeStim7.setAutoDraw(True)
    shapeStim8.setAutoDraw(True)
    shapeStim9.setAutoDraw(True)
    shapeStim10.setAutoDraw(True)
    shapeStim11.setAutoDraw(True)
    shapeStim12.setAutoDraw(True)
    mywin.flip()
##############################################################################################
#undraw the grid
def undraw_grid():
    global shapeStim1,shapeStim2,shapeStim3,shapeStim4,shapeStim5,shapeStim6,shapeStim7,shapeStim8,shapeStim9,shapeStim10
    #lines for the grid
    shapeStim1.setAutoDraw(False)
    shapeStim2.setAutoDraw(False)
    shapeStim3.setAutoDraw(False)
    shapeStim4.setAutoDraw(False)
    shapeStim5.setAutoDraw(False)
    shapeStim6.setAutoDraw(False)
    shapeStim7.setAutoDraw(False)
    shapeStim8.setAutoDraw(False)
    shapeStim9.setAutoDraw(False)
    shapeStim10.setAutoDraw(False)
    shapeStim11.setAutoDraw(False)
    shapeStim12.setAutoDraw(False)
    mywin.update()
##############################################################################################
#draw the letters on the screen 
def drawLocs(locs,span):   
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
def drawTestLocsSame(locs,probeIndx,probeLoc,span):
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
#draw the letters on the screen def drawLets(letters,locs,span):
#draw the letters on the screen 
def drawLets(letters,locs,span):
    global msg
    for i in range(0,span):
#        if int(locs[i]) == -20:
#            #print 'lets[i]',letters[i]
#            msg = visual.TextStim(win=mywin, text=letters[i], font='', pos=(-20,0),
#                              depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb',
#                              opacity=1.0, ori=0.0, height=20, antialias=True,
#                              bold=False, italic=False, alignHoriz='center', alignVert='center',
#                              fontFiles=[], wrapWidth=None, name='', autoLog=False)
#
#            msg.draw()
        msg = visual.TextStim(win=mywin, text=letters[i], font='', pos=(locs[i],0),
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
def drawTestLets(letters,locs,probeLet1,probeLet2,span,trueOrFalse):
    global msg,fixCircle,smallCircle
    fixCircle.setAutoDraw(False)
    smallCircle.setAutoDraw(False)
    mywin.update()
    if trueOrFalse == 0 and probeLet1 != '-1' and probeLet2 != '-1':
        #print 'testLetters',testLetters,'probeLetters',probeLet1
        l1 = probeLet1
        l2 = probeLet2
        tmp = letters[l1]
        letters[l1] = letters[l2]
        letters[l2] = tmp
    for i in range(0,span):
        msg = visual.TextStim(win=mywin, text=testLetters[listOfConsonants.index(letters[i])], font='', pos=(locs[i],0),
                              depth=0, rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb',
                              opacity=1.0, ori=0.0, height=20, antialias=True,
                              bold=False, italic=False, alignHoriz='center', alignVert='center',
                              fontFiles=[], wrapWidth=None, name='', autoLog=False)

        msg.draw()
    mywin.update()

 ##############################################################################################
#draw the calculation problem, ifparam == 1, draw multiplication, if param == 0, draw subtraction
def draw_calc(thisTrial,param,ans):
    global countProbAnsCorrOrNot,countProbRT,multSign
    fixCircle = visual.Circle(mywin,pos=(0,0), radius=10, edges=32, opacity = 0.3,lineColor = green, fillColor = green)
    fixCircle.setAutoDraw(True)
    if ans  == 1:
        posRes = -20
        posResAlt = 20
    elif ans  == 0:
        posRes = 20
        posResAlt = -20        
    fake = visual.TextStim(mywin, text='', font='', pos=(-20, 0), depth=0, rgb=None,
              color=black, colorSpace='rgb', opacity=1.0, 
              ori=0.0, height=20, antialias=True, bold=False, italic=False,
              alignHoriz='center', alignVert='center', fontFiles=[],
              wrapWidth=None, name='', autoLog=True)
    op1 = visual.TextStim(mywin, text=thisTrial.operand1, font='', pos=(-19, 0), depth=0, rgb=None,
                  color=black, colorSpace='rgb', opacity=1.0, 
                  ori=0.0, height=20, antialias=True, bold=False, italic=False,
                  alignHoriz='center', alignVert='center', fontFiles=[],
                  wrapWidth=None, name='', autoLog=True)
    op2 = visual.TextStim(mywin, text=thisTrial.operand2, font='', pos=(20, 0), depth=0, rgb=None,
                  color=black, colorSpace='rgb', opacity=1.0, 
                  ori=0.0, height=20, antialias=True, bold=False, italic=False,
                  alignHoriz='center', alignVert='center', fontFiles=[],
                  wrapWidth=None, name='', autoLog=True)
    res = visual.TextStim(mywin, text=thisTrial.probRes, font='', pos=(posRes, 0), depth=0, rgb=None,
                  color=black, colorSpace='rgb', opacity=1.0, 
                  ori=0.0, height=20, antialias=True, bold=False, italic=False,
                  alignHoriz='center', alignVert='center', fontFiles=[],
                  wrapWidth=None, name='', autoLog=True)
    resAlt = visual.TextStim(mywin, text=thisTrial.respAlt, font='', pos=(posResAlt, 0), depth=0, rgb=None,
                  color=black, colorSpace='rgb', opacity=1.0, 
                  ori=0.0, height=20, antialias=True, bold=False, italic=False,
                  alignHoriz='center', alignVert='center', fontFiles=[],
                  wrapWidth=None, name='', autoLog=True)

    #fake.setAutoDraw(True)
    if groupNo == 1:
        multSign.setAutoDraw(True)
    else:
        subSign.setAutoDraw(True)
    op1.setAutoDraw(True)
    op2.setAutoDraw(True)
    mywin.update()
    core.wait(2)
    op1.setAutoDraw(False)
    if groupNo == 1:
        multSign.setAutoDraw(False)
    else:
        subSign.setAutoDraw(False)
    op2.setAutoDraw(False)
    
    mywin.update()
    core.wait(0.2)

    key_resp.status = NOT_STARTED
    pressed = 0
    t2 = 0
    calcClock.reset()  # clock
    while t2 < calcDur:
        # get current time
        t2 = calcClock.getTime()
        t = globalClock.getTime()
        
        # *key_resp* updates
        if key_resp.status == NOT_STARTED:
            res.setAutoDraw(True)
            resAlt.setAutoDraw(True)
            # keep track of start time for later
            key_resp.tStart = t2  # underestimates by a little under one frame
            key_resp.status = STARTED
            # keyboard checking is just starting
            key_resp.clock.reset()  # now t=0
            event.clearEvents()

        if key_resp.status == STARTED:  # only update if being drawn
            theseKeys = event.getKeys(keyList=['lctrl', 'rctrl'])
            if len(theseKeys) > 0:  # at least one key was pressed
                pressed = 1
                if param == 1:
                    t2 = calcDur #exit the loop if the subject already responded
                key_resp.keys = theseKeys[-1]  # just the last key pressed
                key_resp.rt = key_resp.clock.getTime()
                # was this 'correct'?
                if (key_resp.keys == 'lctrl'):
                    key_resp.corr = 1
                elif (key_resp.keys == 'rctrl'): key_resp.corr=0
                else:
                    key_resp.corr = -1

        # check for quit (the [Esc] key)
        if event.getKeys(["escape"]):
            mywin.close()
            core.quit()
        
        # refresh the screen
        #draw_grid(mywin)
        mywin.update()
    if pressed == 0:
        key_resp.corr= -1
        key_resp.rt = 0
    probAns.append(key_resp.corr)
    if key_resp.corr == ans:
        probAnsCorrOrNot.append(1)
    elif key_resp.corr == -1:
        probAnsCorrOrNot.append(-1)
    else:
        probAnsCorrOrNot.append(0)
    #print 'probAnsCorrOrNot',probAnsCorrOrNot
    res.setAutoDraw(False)
    resAlt.setAutoDraw(False)
    fixCircle.setAutoDraw(False)
    mywin.update()
    #add the data to trial handler
    probRT.append(key_resp.rt)#rt of the subject-->time it takes the subject to press right or left arrow   
    countProbAnsCorrOrNot += 1
    countProbRT += 1
    trials.data.add('probAns',key_resp.corr)
##############################################################################################
#a function to write multiple variables to a line in the log file
def write_infos_to_logfile(listIN, logfile):
    #"""takes the elements from listIN and writes them to the logfile"""
    for i in range(0,len(listIN)):
        logfile.write(str(listIN[i]))
        logfile.write('\t')
    logfile.write('\n')

logFile = open('mydata' + os.path.sep +'log.txt','a+')
listN = ['groupNo','subject','type','calcFile','sessionNo','trialNo','span','spanLevel','operand1','operand2','probRes','respAlt','subDist','tableError','RT','corrOrNot','probRT','probAnsCorrOrNot','dir','carry']
#write_infos_to_logfile(listN, logFile)
##############################################################################################
#run the actual experiment
def run_experiment(participant,sessions,mywin):
    global fixCircle,smallCircle,trialNo
    for i in range(0,5):
        gridDrawn = 0
        undraw_grid()
        types = []
        if groupNo == 1:
            types = ['c','p','v','pm','vm']
        else:
            types = ['c','p','v','ps','vs']
        #print 'types',types,'sessions',sessions
        filename = 'mydata' + os.path.sep + participant + '_session_' + types[sessions[i]-3]+'.xlsx'
        #run the calculation experiment only if it is the first session
        if sessions[i] == 3:
            ansIndx = 0
            # set up handler to look after randomisation of conditions etc
            #if group == 1, do multiplication, if group == 2, do subtraction
            trials = data.TrialHandler(nReps=1, method='random', 
                extraInfo=expInfo, originPath=None,
                trialList=data.importConditions(calcFile3),
                seed=None, name='trials')
            thisExp.addLoop(trials)  # add the loop to the experiment
            thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial.keys():
                    exec(paramName + '= thisTrial.' + paramName)
            #display instructions and wait
            text1 = ['MULTIPLIKATIONEN','SUBTRAKTIONEN']
            text2 = [""]
            message1 = visual.TextStim(mywin, pos=[0,+35],text=text1[groupNo-1])
            message2 = visual.TextStim(mywin, pos=[0,-35], text=text2[groupNo-2])
            message3 = visual.TextStim(mywin, pos=[0,-105], text="Drucken Sie eine beliebige Taste, um zu beginnen")
            message1.draw()
            message2.draw()
            message3.draw()
            mywin.flip()#to show our newly drawn 'stimuli'
            #pause until there's a keypress
            event.waitKeys()

            globalClock.reset()
            t0 = 0 #general clock of the experiment
            experimentClock.reset()
            for thisTrial in trials:
                currentLoop = trials
                trialNo = trialNo + 1
                # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
                if thisTrial != None:
                    for paramName in thisTrial.keys():
                        exec(paramName + '= thisTrial.' + paramName)

                stimCalc = []
                        #-------Start "trial"-------
                #draw the fixation cross, then letters, and then the cross again
                draw_circle(green,fixDur,mywin) #indicating that the following task will be calculation
                ansSide = ansSides[ansIndx%28]
                draw_calc(thisTrial,1,ansSide)
                ansIndx = ansIndx + 1
                thisExp.nextEntry()  
                trials.data.add('probAnsCorrOrNot',probAnsCorrOrNot[countProbAnsCorrOrNot-1])
                trials.data.add('probRT',"{0:.4f}".format(1000*probRT[countProbRT-1]))
                listN = [groupNo,subNo,thisTrial.type,calcFile3,i+1,trialNo,'-1','-1',thisTrial.operand1,thisTrial.operand2,thisTrial.probRes,thisTrial.respAlt,thisTrial.subDist,thisTrial.tableError,'-1','-1',"{0:.4f}".format(1000*probRT[countProbRT-1]),probAnsCorrOrNot[countProbAnsCorrOrNot-1],'-1',thisTrial.carry]
                write_infos_to_logfile(listN,logFile)
                #logFile.write(thisTrial.type,"\t",'',"\t",'',"\t",'',"\t",str(probRT[countProbRT-1]),"\t",str(probAnsCorrOrNot[countProbAnsCorrOrNot-1]),"\t",str(thisTrial.subDist),"\t",str(thisTrial.tableError),"\n")
            

            trials.saveAsExcel(filename, sheetName='calculations',
                stimOut=[],
                dataOut=['probAnsCorrOrNot_raw','probRT_raw','probAns_raw'])

            #mywin.close()

        else:    
            global ans
            if sessions[i] == 4:
                #display instructions and wait
                message1 = visual.TextStim(mywin, pos=[0,+100],text='BUCHSTABEN')
                message2 = visual.TextStim(mywin, pos=[0,10], text='')
                message3 = visual.TextStim(mywin, pos=[0,-60],text='Drucken Sie eine beliebige Taste, um zu beginnen.')
                message1.draw()
                message2.draw()
                message3.draw()
                mywin.flip()#to show our newly drawn 'stimuli'
                #pause until there's a keypress
                event.waitKeys()
            elif sessions[i] == 5:
                #display instructions and wait
                message1 = visual.TextStim(mywin, pos=[0,+100],text='POSITIONEN')
                message2 = visual.TextStim(mywin, pos=[0,10], text='')
                message3 = visual.TextStim(mywin, pos=[0,-60],text='Drucken Sie eine beliebige Taste, um zu beginnen.')
                message1.draw()
                message2.draw()
                message3.draw()
                mywin.flip()#to show our newly drawn 'stimuli'
                #pause until there's a keypress
                event.waitKeys()
            elif sessions[i] == 6:
                #display instructions and wait
                message1 = visual.TextStim(mywin, pos=[0,+100],text='BUCHSTABEN UND RECHNENAUFGABEN')
                message2 = visual.TextStim(mywin, pos=[0,10], text='')
                message3 = visual.TextStim(mywin, pos=[0,-60],text='Drucken Sie eine beliebige Taste, um zu beginnen.')
                message1.draw()
                message2.draw()
                message3.draw()
                mywin.flip()#to show our newly drawn 'stimuli'
                #pause until there's a keypress
                event.waitKeys()
            elif sessions[i] == 7:
                #display instructions and wait
                message1 = visual.TextStim(mywin, pos=[0,+100],text='POSITIONEN UND RECHNENAUFGABEN')
                message2 = visual.TextStim(mywin, pos=[0,10], text='')
                message3 = visual.TextStim(mywin, pos=[0,-60],text= 'Drucken Sie eine beliebige Taste, um zu beginnen.')
                message1.draw()
                message2.draw()
                message3.draw()
                mywin.flip()#to show our newly drawn 'stimuli'
                #pause until there's a keypress
                event.waitKeys()
            # set up handler to look after randomisation of conditions etc
            trials = data.TrialHandler(nReps=1, method='random', 
                extraInfo=expInfo, originPath=None,
                trialList=data.importConditions('mydata\\'+participant+'_session_'+types[sessions[i]-3]+'.xlsx'),
                seed=None, name='trials')
            thisExp.addLoop(trials)  # add the loop to the experiment
            thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial.keys():
                    exec(paramName + '= thisTrial.' + paramName)

            ansIndx = 0
            firstTrial = 1
            t0 = 0 #general clock of the experiment
            experimentClock.reset()
            for thisTrial in trials:
                #blockClock.reset()
                #check if it has been more than 10 mins or not
                t = blockClock.getTime()
                if t>blockDur:
                    text1 ='PAUSE'
                    text2 = "Druecken Sie eine Taste, um fortzufahren"
                    message1 = visual.TextStim(mywin, pos=[0,+35],text=text1)
                    message2 = visual.TextStim(mywin, pos=[0,-35], text=text2)
                    message1.draw()
                    message2.draw()
                    mywin.flip()#to show our newly drawn 'stimuli'
                    #pause until there's a keypress
                    event.waitKeys()
                    blockClock.reset()

                currentLoop = trials
                trialNo += 1
                if firstTrial != 1:
                    fixCircle.setAutoDraw(False)
                    smallCircle.setAutoDraw(False)
                    mywin.update()
                firstTrial = 0
                core.wait(0.3)
                # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
                if thisTrial != None:
                    for paramName in thisTrial.keys():
                        exec(paramName + '= thisTrial.' + paramName)


                #-------Start "trial"-------
                #draw the fixation cross, then letters, and then the cross again
                if thisTrial.type == 'p' or thisTrial.type == 'pm' or thisTrial.type == 'ps':
                    lets = [thisTrial.letter1,thisTrial.letter2,thisTrial.letter3,thisTrial.letter4,thisTrial.letter5,thisTrial.letter6,thisTrial.letter7,
                            thisTrial.letter8,thisTrial.letter9]
                    locsX = [thisTrial.loc1x,thisTrial.loc2x,thisTrial.loc3x,thisTrial.loc4x,thisTrial.loc5x,thisTrial.loc6x,thisTrial.loc7x,
                         thisTrial.loc8x,thisTrial.loc9x]
                    locsY = [thisTrial.loc1y,thisTrial.loc2y,thisTrial.loc3y,thisTrial.loc4y,thisTrial.loc5y,thisTrial.loc6y,thisTrial.loc7y,
                            thisTrial.loc8y,thisTrial.loc9y]

                elif thisTrial.type == 'v' or thisTrial.type == 'vm' or thisTrial.type == 'vs':
                    lets = ['O','O','O','O','O','O','O','O','O','O','O','O','O','O','O']
                    locs = [thisTrial.loc1,thisTrial.loc2,thisTrial.loc3,thisTrial.loc4,thisTrial.loc5,thisTrial.loc6,thisTrial.loc7,
                         thisTrial.loc8,thisTrial.loc9]

                
                if thisTrial.type == 'p':
                    #draw all stimuli
                    draw_circle(red,fixDur,mywin)
                    drawLets(lets,locsX,thisTrial.span)
                    draw_circle(red,7.2,mywin)
                    fixCircle.setAutoDraw(False)
                    smallCircle.setAutoDraw(False)
                    mywin.update()
                    #draw the test sequence
                    drawTestLets(lets,locsX,thisTrial.probeLet1,thisTrial.probeLet2,thisTrial.span,(thisTrial.taskAns==subNo%2))
                elif thisTrial.type == 'v':
                    if gridDrawn == 0:
                        draw_grid(5,5)
                    gridDrawn = 1
                    draw_circle(blue,fixDur,mywin)
                    drawLocs(locs,thisTrial.span)
                    dur = fixDur+1.2+calcDur
                    draw_circle(blue,7.2,mywin)
                    if thisTrial.probeIndx != thisTrial.probeLoc:
                        drawTestLocs(locs,thisTrial.probeIndx,thisTrial.probeLoc,span)
                    else:
                        drawTestLocsSame(locs,thisTrial.probeIndx,thisTrial.probeLoc,span)
                elif thisTrial.type =='pm' or thisTrial.type == 'ps':
                    #draw all stimuli
                    draw_circle(red,fixDur,mywin)
                    drawLets(lets,locsX,thisTrial.span)
                    draw_circle(green,fixDur,mywin)
                    fixCircle.setAutoDraw(False)
                    smallCircle.setAutoDraw(False)
                    mywin.update()
                    ansSide = ansSides[ansIndx%28]
                    draw_calc(thisTrial,0,ansSide)    
                    #draw the test sequence
                    drawTestLets(lets,locsX,thisTrial.probeLet1,thisTrial.probeLet2,thisTrial.span,(thisTrial.taskAns==subNo%2))
                elif thisTrial.type =='vm' or thisTrial.type == 'vs':
                    if gridDrawn == 0:
                        draw_grid(5,5)
                    gridDrawn = 1
                    draw_circle(blue,fixDur,mywin)
                    drawLocs(locs,thisTrial.span)
                    #undraw_grid()
                    draw_circle(green,fixDur,mywin) #indicating that the following task will be calculation
                    ansSide = ansSides[ansIndx%28]
                    draw_calc(thisTrial,0,ansSide)
                    if thisTrial.probeIndx != thisTrial.probeLoc:
                        drawTestLocs(locs,thisTrial.probeIndx,thisTrial.probeLoc,span)
                    else:
                        drawTestLocsSame(locs,thisTrial.probeIndx,thisTrial.probeLoc,span)

                t = 0
                trialClock.reset()  # clock
                key_resp.status = NOT_STARTED

                probeTime = 0
                if thisTrial.type == 'v' or thisTrial.type == 'vm' or thisTrial.type == 'vs':
                    probeTime = 4
                else:
                    probeTime = testLetDur
                t1 = globalClock.getTime()
                key_resp.keys = []
                global pressed
                pressed = 0
                while t < probeTime:
                    # get current time
                    t = trialClock.getTime()
                    t1 = globalClock.getTime()

                    # *key_resp* updates
                    if key_resp.status == NOT_STARTED:
                        # keep track of start time for later
                        key_resp.tStart = t  # underestimates by a little under one frame
                        key_resp.status = STARTED
                        # keyboard checking is just starting
                        key_resp.clock.reset()  # now t=0
                        event.clearEvents()
                        
                    if key_resp.status == STARTED:  # only update if being drawn
                        theseKeys = event.getKeys()
                        if len(theseKeys) > 0:  # at least one key was pressed
                            pressed = 1
                            t = probeTime
                            key_resp.keys = theseKeys[-1]  # just the last key pressed
                            key_resp.rt = key_resp.clock.getTime()
                            # was this 'correct'?
                            if (key_resp.keys == 'lctrl'):
                                key_resp.corr = 1
                            elif (key_resp.keys == 'rctrl'): key_resp.corr=0
                            else: key_resp.corr = -1
                    # check for quit (the [Esc] key)
                    if event.getKeys(["escape"]):
                        mywin.close()
                        core.quit()
               
                if pressed == 0:
                    key_resp.corr = -1
                    corrOrNot.append(-1)
                    key_resp.rt = 0
                else:
                    if key_resp.corr == thisTrial.taskAns:
                        corrOrNot.append(1)
                    else:
                        corrOrNot.append(0)
                    
                t1 = globalClock.getTime()
                #add the data to trial handler
                RT.append(key_resp.rt)#rt of the subject-->time it takes the subject to press right or left arrow        
                probAns.append(key_resp.corr)


                #msg.setAutoDraw(True)
                key_resp.status = STOPPED
                #stop drawing the test letter
                fixCircle.setAutoDraw(False)
                smallCircle.setAutoDraw(False)
                msg.setAutoDraw(False)
                mywin.update()

                # check responses
                if len(key_resp.keys) == 0:  # No response was made
                    key_resp.corr = 0  # failed to respond (incorrectly)
                # store data for trials (TrialHandler)
                if key_resp.keys != None:  # we had a response
                    rt = key_resp.rt
                    ans = key_resp.corr

                global countCorrOrNot,countRT,countProbAns
                countCorrOrNot += 1
                countRT += 1
                countProbAns += 1
                ansIndx += 1

                if thisTrial.type == 'vs' or thisTrial.type == 'vm':
                    trials.data.add('probAnsCorrOrNot',probAnsCorrOrNot[countProbAnsCorrOrNot-1])
                    trials.data.add('probRT',"{0:.4f}".format(1000*probRT[countProbRT-1]))
                    trials.data.add('corrOrNot',corrOrNot[countCorrOrNot-1])
                    trials.data.add('RT',"{0:.4f}".format(1000*probRT[countProbRT-1]))
                    trials.data.add('probAns',probAns[countProbAns-1])
                    listN = [groupNo,subNo,thisTrial.type,calcFile2,i+1,trialNo,thisTrial.span,thisTrial.spanLevel,thisTrial.operand1,thisTrial.operand2,thisTrial.probRes,thisTrial.respAlt,thisTrial.subDist,thisTrial.tableError,"{0:.4f}".format(1000*RT[countRT-1]),corrOrNot[countCorrOrNot-1],"{0:.4f}".format(1000*probRT[countProbRT-1]),probAnsCorrOrNot[countProbAnsCorrOrNot-1],thisTrial.dir,thisTrial.carry]
                    write_infos_to_logfile(listN, logFile)
                
                elif thisTrial.type == 'ps' or thisTrial.type == 'pm':
                    trials.data.add('probAnsCorrOrNot',probAnsCorrOrNot[countProbAnsCorrOrNot-1])
                    trials.data.add('probRT',"{0:.4f}".format(1000*probRT[countProbRT-1]))
                    trials.data.add('corrOrNot',corrOrNot[countCorrOrNot-1])
                    trials.data.add('RT',"{0:.4f}".format(1000*probRT[countProbRT-1]))
                    trials.data.add('probAns',probAns[countProbAns-1])
                    listN = [groupNo,subNo,thisTrial.type,calcFile1,i+1,trialNo,thisTrial.span,thisTrial.spanLevel,thisTrial.operand1,thisTrial.operand2,thisTrial.probRes,thisTrial.respAlt,thisTrial.subDist,thisTrial.tableError,"{0:.4f}".format(1000*RT[countRT-1]),corrOrNot[countCorrOrNot-1],"{0:.4f}".format(1000*probRT[countProbRT-1]),probAnsCorrOrNot[countProbAnsCorrOrNot-1],'-1',thisTrial.carry]
                    write_infos_to_logfile(listN, logFile)

                elif thisTrial.type == 'v':
                    trials.data.add('corrOrNot',corrOrNot[countCorrOrNot-1])
                    trials.data.add('RT',"{0:.4f}".format(1000*RT[countRT-1]))
                    listN = [groupNo,subNo,thisTrial.type,'-1',i+1,trialNo,thisTrial.span,thisTrial.spanLevel,'-1','-1','-1','-1','-1','-1',"{0:.4f}".format(1000*RT[countRT-1]),corrOrNot[countCorrOrNot-1],'-1','-1',thisTrial.dir,'-1']
                    write_infos_to_logfile(listN, logFile)
                    
                elif thisTrial.type == 'p':
                    trials.data.add('corrOrNot',corrOrNot[countCorrOrNot-1])
                    trials.data.add('RT',"{0:.4f}".format(1000*RT[countRT-1]))
                    listN = [groupNo,subNo,thisTrial.type,'-1',i+1,trialNo,thisTrial.span,thisTrial.spanLevel,'-1','-1','-1','-1','-1','-1',"{0:.4f}".format(1000*RT[countRT-1]),corrOrNot[countCorrOrNot-1],'-1','-1','-1','-1']
                    write_infos_to_logfile(listN, logFile)
            trials.saveAsExcel(filename, sheetName='wm',
                stimOut=[],
                dataOut=['probAnsCorrOrNot_raw','probRT_raw','corrOrNot_raw','RT_raw','probAns_raw'])
####################################################################################################
#randomly decide the order of tasks 3= calc 4 = phonological, 5 = visuospatial, 6 = phonological + calc 7 = visuospatial + calc
#sessions2 = runOrder[subNo%24]
sessions2 = [4,6]
#sessions2 = runOrder

run_experiment(participant,sessions2,mywin)

#after the experiment save the data
print '\n'