from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np 
import pandas as pd
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  
import sys 
import time

from psychopy.hardware import keyboard


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'cartoon'  # from the Builder filename that created this script
expInfo = {'participant': '', '': ''}

dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1.000,-1.000,-1.000], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')
win.monitor.setSizePix([2560, 1600])
win.monitor.setWidth(33.3)

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "Consent"
ConsentClock = core.Clock()
ConsentPage = visual.ImageStim(
    win=win,
    name='ConsentPage', 
    image=_thisDir + '/images/Consent.jpeg', mask=None,
    ori=0, pos=(0, 0), size=(10.2, 10.0),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,  units="cm",
    texRes=128, interpolate=True, depth=0.0)
ConsentResp = keyboard.Keyboard()

# Initialize components for Routine "Break"
BreakClock = core.Clock()
blankscreen = visual.TextStim(win=win, name='blankscreen',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR', units="cm",
    depth=0.0);

# Initialize components for Routine "Instructions1"
Instructions1Clock = core.Clock()
textInstructions = visual.TextStim(win=win, name='textInstructions',
    text='Task Instructions\n\nIn this experiment, you will switch back and forth between 2 games.\n\n In the first game, press X for letters c & o and N for letters i & l.\n\nIn the second game, press X for letters d & p and N for letters q & b.\n\nYou will switch between both games 4 times.\n\nYou will be reminded of the instructions each time you switch!\n\n The task takes less than 20 minutes! \n\n Press SPACEBAR for more instructions!',
    font='Arial',
    pos=(0, 0), height=0.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR', units="cm",
    depth=0.0);
textInstructionsResp = keyboard.Keyboard()

# Initialize components for Routine "Break"
BreakClock = core.Clock()
blankscreen = visual.TextStim(win=win, name='blankscreen',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR', units="cm",
    depth=0.0);

# Initialize components for Routine "Instructions2"
Instructions2Clock = core.Clock()
imgInstructions = visual.ImageStim(
    win=win,
    name='imgInstructions', 
    image=_thisDir + '/images/Instructions.jpeg', mask=None,
    ori=0, pos=(0, 0), size=(11.0, 11.0),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,  units="cm",
    texRes=128, interpolate=True, depth=0.0)
imgInstructionsResp = keyboard.Keyboard()

# Initialize components for Routine "Break"
BreakClock = core.Clock()
blankscreen = visual.TextStim(win=win, name='blankscreen',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',  units="cm",
    depth=0.0);

# Initialize components for Routine "PracticeWarning"
PracticeWarningClock = core.Clock()
PracticeText = visual.TextStim(win=win, name='PracticeText',
    text='PRESS SPACEBAR TO BEGIN PRACTICE!\n\n Remember: \n\n Game 1: Press X for c & o and N for i & l\n\n Game 2: Press X for d & p and N for q & b',
    font='Arial',
    pos=(0, 0), height=0.5, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',  units="cm",
    depth=0.0);
PracticeTextResp = keyboard.Keyboard()

PracticeClock = core.Clock()

# Initialize components for Routine "ReminderLow"
ReminderLowClock = core.Clock()
imageReminderLow = visual.ImageStim(
    win=win,
    name='imageReminderLow', 
    image=_thisDir + '/images/LowReminder.jpeg', mask=None,
    ori=0, pos=(0, 0), size=(6.0, 4.0),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,  units="cm",
    texRes=128, interpolate=True, depth=0.0)
ReminderLow_Resp = keyboard.Keyboard()

# Initialize components for Routine "ReminderHigh"
ReminderHighClock = core.Clock()
imageReminderHigh = visual.ImageStim(
    win=win,
    name='imageReminderHigh', 
    image=_thisDir + '/images/HighReminder.jpeg', mask=None,
    ori=0, pos=(0, 0), size=(6.0, 4.0),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,  units="cm",
    texRes=128, interpolate=True, depth=0.0)
ReminderHigh_Resp = keyboard.Keyboard()
# Initialize components for Routine "LowLoad1"
def item_generator(name, pos, win):
    if name == "circle_situator":
        h=1.5
    else:
        h=0.5
    item = visual.TextStim(
        win=win, name=name,
        text='default text',
        font='Arial',
        pos=pos, height=h, wrapWidth=None, ori=0, 
        color='white', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',  units="cm",
        depth=0.0)
    
    return item

LowLoad1Clock = core.Clock()
item1 = item_generator("item1", (0, 4.1), win)
item1_resp = keyboard.Keyboard()

item2 = item_generator("item2", (1.905, 3.5), win)
item3 = item_generator("item3", (3.5, 2.2), win)
item4 = item_generator("item4", (4.2, 0), win)
item5 = item_generator("item5", (3.5, -2.2), win)
item6 = item_generator("item6", (1.905, -3.5), win)
item7 = item_generator("item7", (0, -4.1), win)
item8 = item_generator("item8", (-1.905, -3.5), win)
item9 = item_generator("item9", (-3.5, -2.2), win)
item10 = item_generator("item10", (-4.2, 0), win)
item11 = item_generator("item11", (-3.5, 2.2), win)
item12 = item_generator("item12", (-1.905, 3.5), win)
item13 = item_generator("circle_situator", (0, 4.1), win)


# Initialize components for Routine "Break"
BreakClock = core.Clock()
blankscreen = visual.TextStim(win=win, name='blankscreen',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',  units="cm",
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()            # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "Consent"-------
continueRoutine = True
# update component parameters for each repeat
ConsentResp.keys = []
ConsentResp.rt = []
_ConsentResp_allKeys = []
# keep track of which components have finished
ConsentComponents = [ConsentPage, ConsentResp]
for thisComponent in ConsentComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
ConsentClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Consent"-------
while continueRoutine:
    # get current time
    t = ConsentClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=ConsentClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *ConsentPage* updates
    if ConsentPage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ConsentPage.frameNStart = frameN  # exact frame index
        ConsentPage.tStart = t  # local t and not account for scr refresh
        ConsentPage.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ConsentPage, 'tStartRefresh')  # time at next scr refresh
        ConsentPage.setAutoDraw(True)
    
    # *ConsentResp* updates
    waitOnFlip = False
    if ConsentResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ConsentResp.frameNStart = frameN  # exact frame index
        ConsentResp.tStart = t  # local t and not account for scr refresh
        ConsentResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ConsentResp, 'tStartRefresh')  # time at next scr refresh
        ConsentResp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(ConsentResp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(ConsentResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if ConsentResp.status == STARTED and not waitOnFlip:
        theseKeys = ConsentResp.getKeys(keyList=['space'], waitRelease=False)
        _ConsentResp_allKeys.extend(theseKeys)
        if len(_ConsentResp_allKeys):
            ConsentResp.keys = _ConsentResp_allKeys[-1].name  # just the last key pressed
            ConsentResp.rt = _ConsentResp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ConsentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Consent"-------
for thisComponent in ConsentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if ConsentResp.keys in ['', [], None]:  # No response was made
    ConsentResp.keys = None

# the Routine "Consent" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Break"-------
continueRoutine = True
routineTimer.add(0.500000)
# update component parameters for each repeat
# keep track of which components have finished
BreakComponents = [blankscreen]
for thisComponent in BreakComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
BreakClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Break"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = BreakClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=BreakClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *blankscreen* updates
    if blankscreen.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        blankscreen.frameNStart = frameN  # exact frame index
        blankscreen.tStart = t  # local t and not account for scr refresh
        blankscreen.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(blankscreen, 'tStartRefresh')  # time at next scr refresh
        blankscreen.setAutoDraw(True)
    if blankscreen.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > blankscreen.tStartRefresh + 0.5-frameTolerance:
            # keep track of stop time/frame for later
            blankscreen.tStop = t  # not accounting for scr refresh
            blankscreen.frameNStop = frameN  # exact frame index
            win.timeOnFlip(blankscreen, 'tStopRefresh')  # time at next scr refresh
            blankscreen.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in BreakComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Break"-------
for thisComponent in BreakComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# ------Prepare to start Routine "Instructions1"-------
continueRoutine = True
# update component parameters for each repeat
textInstructionsResp.keys = []
textInstructionsResp.rt = []
_textInstructionsResp_allKeys = []
# keep track of which components have finished
Instructions1Components = [textInstructions, textInstructionsResp]
for thisComponent in Instructions1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Instructions1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Instructions1"-------
while continueRoutine:
    # get current time
    t = Instructions1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Instructions1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *textInstructions* updates
    if textInstructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        textInstructions.frameNStart = frameN  # exact frame index
        textInstructions.tStart = t  # local t and not account for scr refresh
        textInstructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(textInstructions, 'tStartRefresh')  # time at next scr refresh
        textInstructions.setAutoDraw(True)
    
    # *textInstructionsResp* updates
    waitOnFlip = False
    if textInstructionsResp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        textInstructionsResp.frameNStart = frameN  # exact frame index
        textInstructionsResp.tStart = t  # local t and not account for scr refresh
        textInstructionsResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(textInstructionsResp, 'tStartRefresh')  # time at next scr refresh
        textInstructionsResp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(textInstructionsResp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(textInstructionsResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if textInstructionsResp.status == STARTED and not waitOnFlip:
        theseKeys = textInstructionsResp.getKeys(keyList=['space'], waitRelease=False)
        _textInstructionsResp_allKeys.extend(theseKeys)
        if len(_textInstructionsResp_allKeys):
            textInstructionsResp.keys = _textInstructionsResp_allKeys[-1].name  # just the last key pressed
            textInstructionsResp.rt = _textInstructionsResp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Instructions1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Instructions1"-------
for thisComponent in Instructions1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
        
# the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Break"-------
continueRoutine = True
routineTimer.add(0.500000)
# update component parameters for each repeat
# keep track of which components have finished
BreakComponents = [blankscreen]
for thisComponent in BreakComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
BreakClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Break"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = BreakClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=BreakClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *blankscreen* updates
    if blankscreen.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        blankscreen.frameNStart = frameN  # exact frame index
        blankscreen.tStart = t  # local t and not account for scr refresh
        blankscreen.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(blankscreen, 'tStartRefresh')  # time at next scr refresh
        blankscreen.setAutoDraw(True)
    if blankscreen.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > blankscreen.tStartRefresh + 0.5-frameTolerance:
            # keep track of stop time/frame for later
            blankscreen.tStop = t  # not accounting for scr refresh
            blankscreen.frameNStop = frameN  # exact frame index
            win.timeOnFlip(blankscreen, 'tStopRefresh')  # time at next scr refresh
            blankscreen.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in BreakComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Break"-------
for thisComponent in BreakComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# ------Prepare to start Routine "Instructions2"-------
continueRoutine = True
# update component parameters for each repeat
imgInstructionsResp.keys = []
imgInstructionsResp.rt = []
_imgInstructionsResp_allKeys = []
# keep track of which components have finished
Instructions2Components = [imgInstructions, imgInstructionsResp]
for thisComponent in Instructions2Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Instructions2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Instructions2"-------
while continueRoutine:
    # get current time
    t = Instructions2Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Instructions2Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *imgInstructions* updates
    if imgInstructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        imgInstructions.frameNStart = frameN  # exact frame index
        imgInstructions.tStart = t  # local t and not account for scr refresh
        imgInstructions.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(imgInstructions, 'tStartRefresh')  # time at next scr refresh
        imgInstructions.setAutoDraw(True)
    
    # *imgInstructionsResp* updates
    waitOnFlip = False
    if imgInstructionsResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        imgInstructionsResp.frameNStart = frameN  # exact frame index
        imgInstructionsResp.tStart = t  # local t and not account for scr refresh
        imgInstructionsResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(imgInstructionsResp, 'tStartRefresh')  # time at next scr refresh
        imgInstructionsResp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(imgInstructionsResp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(imgInstructionsResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if imgInstructionsResp.status == STARTED and not waitOnFlip:
        theseKeys = imgInstructionsResp.getKeys(keyList=['space'], waitRelease=False)
        _imgInstructionsResp_allKeys.extend(theseKeys)
        if len(_imgInstructionsResp_allKeys):
            imgInstructionsResp.keys = _imgInstructionsResp_allKeys[-1].name  # just the last key pressed
            imgInstructionsResp.rt = _imgInstructionsResp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Instructions2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Instructions2"-------
for thisComponent in Instructions2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if imgInstructionsResp.keys in ['', [], None]:  # No response was made
    imgInstructionsResp.keys = None

# the Routine "imgInstructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "PracticeWarning"-------
continueRoutine = True
# update component parameters for each repeat
PracticeTextResp.keys = []
PracticeTextResp.rt = []
_PracticeTextResp_allKeys = []
# keep track of which components have finished
PracticeWarningComponents = [PracticeText, PracticeTextResp]
for thisComponent in PracticeWarningComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
PracticeWarningClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Practice Warning"-------
while continueRoutine:
    # get current time
    t = PracticeWarningClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=PracticeWarningClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *PracticeText* updates
    if PracticeText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        PracticeText.frameNStart = frameN  # exact frame index
        PracticeText.tStart = t  # local t and not account for scr refresh
        PracticeText.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(PracticeText, 'tStartRefresh')  # time at next scr refresh
        PracticeText.setAutoDraw(True)
    
    # *PracticeTextResp* updates
    waitOnFlip = False
    if PracticeTextResp.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
        # keep track of start time/frame for later
        PracticeTextResp.frameNStart = frameN  # exact frame index
        PracticeTextResp.tStart = t  # local t and not account for scr refresh
        PracticeTextResp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(PracticeTextResp, 'tStartRefresh')  # time at next scr refresh
        PracticeTextResp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(PracticeTextResp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(PracticeTextResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if PracticeTextResp.status == STARTED and not waitOnFlip:
        theseKeys = PracticeTextResp.getKeys(keyList=['space'], waitRelease=False)
        _PracticeTextResp_allKeys.extend(theseKeys)
        if len(_PracticeTextResp_allKeys):
            PracticeTextResp.keys = _PracticeTextResp_allKeys[-1].name  # just the last key pressed
            PracticeTextResp.rt = _PracticeTextResp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in PracticeWarningComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Practice Warning"-------
for thisComponent in PracticeWarningComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#----------------------------PRACTICE TRIALS----------------------------
#Parameters
npractrials = 2
npracblocks = 2
#Lists
pracresponses_list = []
pracreaction_list = []
praccorrect_list = []

for i in range(npracblocks):
    
    if i % 2 == 0:
        letters = ["c", "o", "i", "l"]
    else:
        letters = ["p", "d", "q", "b"]
        
    for tr in range(npractrials):
        
        low_letters = np.random.choice(letters, size=12)
        
        #-----Prepare to start Routine "PRACTICE"-----
        continueRoutine = True
        #update component parameters for each repeat
        item1.setText(low_letters[0])
        item1_resp.keys = []
        item1_resp.rt = []
        _item1_resp_allKeys = []
        
        item2.setText(low_letters[1])
        item3.setText(low_letters[2])
        item4.setText(low_letters[3])
        item5.setText(low_letters[4])
        item6.setText(low_letters[5])
        item7.setText(low_letters[6])
        item8.setText(low_letters[7])
        item9.setText(low_letters[8])
        item10.setText(low_letters[9])
        item11.setText(low_letters[10])
        item12.setText(low_letters[11])
        item13.setText("O")
        
        #keep track of which components have finished
        PracticeComponents = [
            item1, item1_resp
        ]
        for thisComponent in PracticeComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        #reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        PracticeClock.reset(-_timeToFirstFrame) #t0 is time of first possible flip
        frameN = -1
        
        #--------Run Routine "Practice"--------
        while continueRoutine:
            #get current time
            t = PracticeClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=PracticeClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1 #number of completed frames (so 0 is the first frame)
            #updaate/draw components on each frame
            
            #--------item1--------
            #*item1* updates
            if item1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                #keep track of start time/frame for later
                item1.frameNStart = frameN             #exact frame index
                item1.tStart = t                       #local t and not account for scr refresh
                item1.tStartRefresh = tThisFlipGlobal  #on global time
                win.timeOnFlip(item1, 'tStartRefresh') #time at next scr refresh
                item1.setAutoDraw(True)
                
            #*item1_resp* updates
            waitOnFlip = False
            if item1_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                #keep track of start time/frame for later
                item1_resp.frameNStart = frameN              #exact frame index
                item1_resp.tStart = t                        #local t and not account for scr refresh
                item1_resp.tStartRefresh = tThisFlipGlobal   #on global time
                win.timeOnFlip(item1_resp, 'tStartRefresh')  #time at next scr refresh
                item1_resp.status = STARTED
                #keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(item1_resp.clock.reset)       # t=0 on next screen flip 
            if item1_resp.status == STARTED and not waitOnFlip:
                theseKeys = item1_resp.getKeys(keyList=['x', 'n'], waitRelease=False)
                _item1_resp_allKeys.extend(theseKeys)
                if len(_item1_resp_allKeys):
                    item1_resp.keys = [key.name for key in _item1_resp_allKeys] #storing all keys
                    item1_resp.rt = [key.rt for key in _item1_resp_allKeys]
                    
            #--------item 2 through 12--------
            item2.setAutoDraw(True)
            item3.setAutoDraw(True)
            item4.setAutoDraw(True)
            item5.setAutoDraw(True)
            item6.setAutoDraw(True)
            item7.setAutoDraw(True)
            item8.setAutoDraw(True)
            item9.setAutoDraw(True)
            item10.setAutoDraw(True)
            item11.setAutoDraw(True)
            item12.setAutoDraw(True)
            item13.setAutoDraw(True)
            
            #--------------------------------------------------------------------
            if len(item1_resp.keys) == 12:
                item1.setAutoDraw(False)
                item2.setAutoDraw(False)
                item3.setAutoDraw(False)
                item4.setAutoDraw(False)
                item5.setAutoDraw(False)
                item6.setAutoDraw(False)
                item7.setAutoDraw(False)
                item8.setAutoDraw(False)
                item9.setAutoDraw(False)
                item10.setAutoDraw(False)
                item11.setAutoDraw(False)
                item12.setAutoDraw(False)
                item13.setAutoDraw(False)
                win.flip()
                continueRoutine = False
            else:
                continueRoutine = True
                
            #refresh the screen
            if continueRoutine:   #don't flip if this routine is over or we'll get blank screen
                win.flip()
                
        if i % 2 == 0:
            correct_response = [
                "x" if r == "c" or r == "o" else "n"
                for r in low_letters
            ]
        else:
            correct_response = [
                "x" if r == "d" or r == "b" else "n"
                for r in low_letters
            ]
            
        correct = np.array(correct_response) == np.array(item1_resp.keys)
        
        pracresponses_list.append(item1_resp.keys)
        pracreaction_list.append(item1_resp.rt)
        praccorrect_list.append(correct)

        time.sleep(1)

pracreaction_list = np.diff(pracreaction_list).tolist()

pracresults = pd.DataFrame(
    data = {
        "block": [n+1 for n in range(npracblocks) for n1 in range (npractrials)],
        "trials": [n%npractrials + 1 for n in range (npracblocks*npractrials)],
        "Responses": pracresponses_list,
        "Accuracy": praccorrect_list,
        "Reaction Times": pracreaction_list
    }
)

pracresults.to_csv(os.getcwd() + f"/pracresults_{expInfo['participant']}.csv")

item1.setAutoDraw(False)
item2.setAutoDraw(False)
item3.setAutoDraw(False)
item4.setAutoDraw(False)
item5.setAutoDraw(False)
item6.setAutoDraw(False)
item7.setAutoDraw(False)
item8.setAutoDraw(False)
item9.setAutoDraw(False)
item10.setAutoDraw(False)
item11.setAutoDraw(False)
item12.setAutoDraw(False)
item13.setAutoDraw(False)

#------------------------------------------------------------------------------------------

# ------Prepare to start Routine "ReminderLow"-------
continueRoutine = True
# update component parameters for each repeat
ReminderLow_Resp.keys = []
ReminderLow_Resp.rt = []
_ReminderLow_Resp_allKeys = []
# keep track of which components have finished
ReminderLowComponents = [imageReminderLow, ReminderLow_Resp]
for thisComponent in ReminderLowComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
ReminderLowClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "ReminderLow"-------
while continueRoutine:
    # get current time
    t = ReminderLowClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=ReminderLowClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *imageReminderLow* updates
    if imageReminderLow.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        imageReminderLow.frameNStart = frameN  # exact frame index
        imageReminderLow.tStart = t  # local t and not account for scr refresh
        imageReminderLow.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(imageReminderLow, 'tStartRefresh')  # time at next scr refresh
        imageReminderLow.setAutoDraw(True)
    
    # *ReminderLow_Resp* updates
    waitOnFlip = False
    if ReminderLow_Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        ReminderLow_Resp.frameNStart = frameN  # exact frame index
        ReminderLow_Resp.tStart = t  # local t and not account for scr refresh
        ReminderLow_Resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(ReminderLow_Resp, 'tStartRefresh')  # time at next scr refresh
        ReminderLow_Resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(ReminderLow_Resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(ReminderLow_Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if ReminderLow_Resp.status == STARTED and not waitOnFlip:
        theseKeys = ReminderLow_Resp.getKeys(keyList=['space'], waitRelease=False)
        _ReminderLow_Resp_allKeys.extend(theseKeys)
        if len(_ReminderLow_Resp_allKeys):
            ReminderLow_Resp.keys = _ReminderLow_Resp_allKeys[-1].name  # just the last key pressed
            ReminderLow_Resp.rt = _ReminderLow_Resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ReminderLowComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "ReminderLow"-------
for thisComponent in ReminderLowComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
routineTimer.reset()

# ----------------------------------RUN EXPERIMENT TRIALS---------------------------------

######################## EXPERIMENT PARAMETERS ########################
ntrials = 2
nblocks = 2
#######################################################################
responses_list = []
reaction_list = [] 
correct_list = []
distractor_pos_list = []

def longest_rep(seq):
    streak = 1
    longest_streak = streak
    for s in range(1, seq.shape[0]):
        if seq[s] == seq[s-1]:
            streak += 1
        else:
            streak = 1
        longest_streak = max(longest_streak, streak)
            
    return longest_streak

for i in range(nblocks):

    if i % 2 == 0:
        letters = ["c", "o", "i", "l"]
    else:
        letters = ["p", "d", "q", "b"]

    distractor_trials = np.random.choice(
        np.arange(2, 21, 1), size=6, replace=False
    )

    distractor_images = os.listdir(_thisDir + "/distractors")
    np.random.shuffle(distractor_images)
    d = 0

    for tr in range(ntrials):
        
        low_letters = None
        gen = True
        while gen:
            low_letters = np.random.choice(letters, size=12)
            if longest_rep(low_letters) < 4:
                gen = False

        image = distractor_images[d]
        distractor_image = visual.ImageStim(
            win=win,
            name='distractor', 
            image=_thisDir + f'/distractors/{image}', mask=None,
            ori=0, pos=(0, 0), size=(2.0, 2.0),
            color=[1,1,1], colorSpace='rgb', opacity=1,
            flipHoriz=False, flipVert=False, units="cm",
            texRes=128, interpolate=True, depth=0.0
        )
        distractor_step = np.random.choice(np.arange(3, 9, 1), size=1)

        # ------Prepare to start Routine "LowLoad1"-------
        continueRoutine = True
        # update component parameters for each repeat
        item1.setText(low_letters[0])
        item1_resp.keys = []
        item1_resp.rt = []
        _item1_resp_allKeys = []

        item2.setText(low_letters[1])
        item3.setText(low_letters[2])
        item4.setText(low_letters[3])
        item5.setText(low_letters[4])
        item6.setText(low_letters[5])
        item7.setText(low_letters[6])
        item8.setText(low_letters[7])
        item9.setText(low_letters[8])
        item10.setText(low_letters[9])
        item11.setText(low_letters[10])
        item12.setText(low_letters[11])
        item13.setText("O")
        
        # keep track of which components have finished
        LowLoad1Components = [
            item1, item1_resp
        ]
        for thisComponent in LowLoad1Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        LowLoad1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "LowLoad1"-------
        while continueRoutine:
            # get current time
            t = LowLoad1Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=LowLoad1Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # --------------item1--------------
            # *item1* updates
            if item1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                item1.frameNStart = frameN  # exact frame index
                item1.tStart = t  # local t and not account for scr refresh
                item1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(item1, 'tStartRefresh')  # time at next scr refresh
                item1.setAutoDraw(True)
            
            # *item1_resp* updates
            waitOnFlip = False
            if item1_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                item1_resp.frameNStart = frameN  # exact frame index
                item1_resp.tStart = t  # local t and not account for scr refresh
                item1_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(item1_resp, 'tStartRefresh')  # time at next scr refresh
                item1_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(item1_resp.clock.reset)  # t=0 on next screen flip
            if item1_resp.status == STARTED and not waitOnFlip:
                theseKeys = item1_resp.getKeys(keyList=['x', 'n'], waitRelease=False)
                _item1_resp_allKeys.extend(theseKeys)
                if len(_item1_resp_allKeys):
                    item1_resp.keys = [key.name for key in _item1_resp_allKeys]  # storing all keys
                    item1_resp.rt = [key.rt for key in _item1_resp_allKeys]

            # --------------item2--------------
            item2.setAutoDraw(True)
            item3.setAutoDraw(True)
            item4.setAutoDraw(True)
            item5.setAutoDraw(True)
            item6.setAutoDraw(True)
            item7.setAutoDraw(True)
            item8.setAutoDraw(True)
            item9.setAutoDraw(True)
            item10.setAutoDraw(True)
            item11.setAutoDraw(True)
            item12.setAutoDraw(True)
            item13.setAutoDraw(True)
            
            if tr+1 in distractor_trials and (len(item1_resp.keys) == distractor_step):
                distractor_image.setAutoDraw(True)
            
            # --------------------------------------------------------------------- 
            
            if len(item1_resp.keys) == 12:
                item1.setAutoDraw(False)
                item2.setAutoDraw(False)
                item3.setAutoDraw(False)
                item4.setAutoDraw(False)
                item5.setAutoDraw(False)
                item6.setAutoDraw(False)
                item7.setAutoDraw(False)
                item8.setAutoDraw(False)
                item9.setAutoDraw(False)
                item10.setAutoDraw(False)
                item11.setAutoDraw(False)
                item12.setAutoDraw(False)
                item13.setAutoDraw(False)
                distractor_image.setAutoDraw(False)
                win.flip()
                continueRoutine=False
            else:
                continueRoutine=True

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        if tr+1 in distractor_trials:
            distractor_pos_list.append(distractor_step[0])
        else:
            distractor_pos_list.append("None")

        if i % 2 == 0:
            correct_response = [
                "x" if r == "c" or r == "o" else "n"
                for r in low_letters
            ]
        else:
            correct_response = [
                "x" if r == "d" or r == "b" else "n"
                for r in low_letters
            ]
        
        correct = np.array(correct_response) == np.array(item1_resp.keys)

        responses_list.append(item1_resp.keys)
        reaction_list.append(item1_resp.rt)
        correct_list.append(correct)

        if tr+1 in distractor_trials and d<5:
            d+=1

        distractor_image.setAutoDraw(False)

        time.sleep(1)

    item1.setAutoDraw(False)
    item2.setAutoDraw(False)
    item3.setAutoDraw(False)
    item4.setAutoDraw(False)
    item5.setAutoDraw(False)
    item6.setAutoDraw(False)
    item7.setAutoDraw(False)
    item8.setAutoDraw(False)
    item9.setAutoDraw(False)
    item10.setAutoDraw(False)
    item11.setAutoDraw(False)
    item12.setAutoDraw(False)
    item13.setAutoDraw(False)

    #------------------------------------------------------------------------------------------
    if i+1 != nblocks:

        if i % 2 == 1:

            # ------Prepare to start Routine "ReminderLow"-------
            continueRoutine = True
            # update component parameters for each repeat
            ReminderLow_Resp.keys = []
            ReminderLow_Resp.rt = []
            _ReminderLow_Resp_allKeys = []
            # keep track of which components have finished
            ReminderLowComponents = [imageReminderLow, ReminderLow_Resp]
            for thisComponent in ReminderLowComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            ReminderLowClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1

            # -------Run Routine "ReminderLow"-------
            while continueRoutine:
                # get current time
                t = ReminderLowClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=ReminderLowClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *imageReminderLow* updates
                if imageReminderLow.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    imageReminderLow.frameNStart = frameN  # exact frame index
                    imageReminderLow.tStart = t  # local t and not account for scr refresh
                    imageReminderLow.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(imageReminderLow, 'tStartRefresh')  # time at next scr refresh
                    imageReminderLow.setAutoDraw(True)
                
                # *ReminderLow_Resp* updates
                waitOnFlip = False
                if ReminderLow_Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    ReminderLow_Resp.frameNStart = frameN  # exact frame index
                    ReminderLow_Resp.tStart = t  # local t and not account for scr refresh
                    ReminderLow_Resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ReminderLow_Resp, 'tStartRefresh')  # time at next scr refresh
                    ReminderLow_Resp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(ReminderLow_Resp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(ReminderLow_Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if ReminderLow_Resp.status == STARTED and not waitOnFlip:
                    theseKeys = ReminderLow_Resp.getKeys(keyList=['space'], waitRelease=False)
                    _ReminderLow_Resp_allKeys.extend(theseKeys)
                    if len(_ReminderLow_Resp_allKeys):
                        ReminderLow_Resp.keys = _ReminderLow_Resp_allKeys[-1].name  # just the last key pressed
                        ReminderLow_Resp.rt = _ReminderLow_Resp_allKeys[-1].rt
                        # a response ends the routine
                        continueRoutine = False
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ReminderLowComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "ReminderLow"-------
            for thisComponent in ReminderLowComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            routineTimer.reset()
        
        else:

            # ------Prepare to start Routine "ReminderHigh"-------
            continueRoutine = True
            # update component parameters for each repeat
            ReminderHigh_Resp.keys = []
            ReminderHigh_Resp.rt = []
            _ReminderHigh_Resp_allKeys = []
            # keep track of which components have finished
            ReminderHighComponents = [imageReminderHigh, ReminderHigh_Resp]
            for thisComponent in ReminderHighComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            ReminderHighClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1

            # -------Run Routine "ReminderHigh"-------
            while continueRoutine:
                # get current time
                t = ReminderHighClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=ReminderHighClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *imageReminderHigh* updates
                if imageReminderHigh.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    imageReminderHigh.frameNStart = frameN  # exact frame index
                    imageReminderHigh.tStart = t  # local t and not account for scr refresh
                    imageReminderHigh.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(imageReminderHigh, 'tStartRefresh')  # time at next scr refresh
                    imageReminderHigh.setAutoDraw(True)
                
                # *ReminderHigh_Resp* updates
                waitOnFlip = False
                if ReminderHigh_Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    ReminderHigh_Resp.frameNStart = frameN  # exact frame index
                    ReminderHigh_Resp.tStart = t  # local t and not account for scr refresh
                    ReminderHigh_Resp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ReminderHigh_Resp, 'tStartRefresh')  # time at next scr refresh
                    ReminderHigh_Resp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(ReminderHigh_Resp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(ReminderHigh_Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if ReminderHigh_Resp.status == STARTED and not waitOnFlip:
                    theseKeys = ReminderHigh_Resp.getKeys(keyList=['space'], waitRelease=False)
                    _ReminderHigh_Resp_allKeys.extend(theseKeys)
                    if len(_ReminderHigh_Resp_allKeys):
                        ReminderHigh_Resp.keys = _ReminderHigh_Resp_allKeys[-1].name  # just the last key pressed
                        ReminderHigh_Resp.rt = _ReminderHigh_Resp_allKeys[-1].rt
                        # a response ends the routine
                        continueRoutine = False
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in ReminderHighComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "ReminderHigh"-------
            for thisComponent in ReminderHighComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            routineTimer.reset()
            

reaction_list = np.diff(reaction_list).tolist()

results = pd.DataFrame(
    data = {
        "block" : [n+1 for n in range(nblocks) for n1 in range(ntrials)],
        "trial" : [n%ntrials + 1 for n in range(nblocks*ntrials)],
        "Responses" : responses_list, 
        "Accuracy" : correct_list,
        "Reaction Times" : reaction_list,
        "Distractor Position" : distractor_pos_list   #Not working - need column of True and Falses for distraactor presence for each trial
    }
)

results.to_csv(os.getcwd() + f"/results_{expInfo['participant']}.csv")

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# make sure everything is closed down
win.close()
core.quit()