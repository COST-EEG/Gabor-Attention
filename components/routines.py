# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:48:00 2020

@author: Marcin Koculak
"""
import numpy as np
from psychopy import visual, core, event, monitors, data, gui

from random import choice


def get_frames(exp, ms):
    return round((ms * exp['frameRate'])/1000, 0)


def display_instruction_screen(exp, image=None, trigger=100):

    instr_send = True

    # Set all the elements
    buttonBox = exp['buttonBox']
    data = exp['data']

    instruction = exp['instructionScreen']
    instruction.setImage(image)

    # Run the instruction screen
    continueRoutine = True
    frames = 0

    pressKey = []
    pressRT = []
    releaseKey = []
    releaseRT = []
    imageFlipTime = []

    start = exp['globalClock'].getTime()
    buttonBox.clock.reset()
    t0 = exp['win'].flip()

    while continueRoutine:
        if exp['keyBoard'].getKeys(keyList=["escape"]):
            print('\n')
            exp['win'].close()
            core.quit()

        instruction.draw()
        t = exp['win'].flip()

        if instr_send:
            print('Instruction -', image, end='\t\t')
            exp['set_data'](trigger)
            print('')
            instr_send = False

        imageFlipTime.append(t)

        # check for key presses
        buttonBox.poll_for_response()
        while len(buttonBox.response_queue):
            evt = buttonBox.get_next_response()

            if evt['pressed']:
                pressKey.append(evt['key'])
                pressRT.append(buttonBox.clock.getTime())
            else:
                releaseKey.append(evt['key'])
                releaseRT.append(buttonBox.clock.getTime())

            buttonBox.poll_for_response()
        buttonBox.clear_response_queue()  # don't process again
        if (len(pressKey) > 0) and (len(releaseKey) > 0):  # at least one key was pressed and released
            continueRoutine = False

        frames += 1

    end = exp['globalClock'].getTime()
    t1 = exp['win'].flip()

    # Save all the data
    data.addData('image_name', image)
    data.addData('global_start_time', start)
    data.addData('global_end_time', end)
    data.addData('pressKey', pressKey[0])
    data.addData('pressRT', pressRT[0])
    #data.addData('releaseKey', releaseKey[0])
    data.addData('releaseRT', releaseRT[0])
    data.addData('image_started', imageFlipTime[0]-t0)
    data.addData('image_ended', t1-t0)
    data.nextEntry()


def display_stimulus(exp, loop, trial):

    fix_send = True
    stim_send = True

    if exp['fixationShape'] == 'cross':
        fix = exp['fixationCross']
    elif exp['fixationShape'] == 'dot':
        fix = exp['dot']

    fixationJitter = np.random.choice(np.arange(100, 1001, 100))
    fixationDuration = get_frames(exp, exp['fixationDur'] + fixationJitter)
    postFixationDuration = get_frames(exp, exp['postFixationDur'])

    arrow = exp['arrow']
    arrow.ori = trial['orientation']

    gabor = exp['gabor']
    gaborDuration = exp['gaborDur']
    ori = trial['orientation']
    pos = (trial['x'], trial['y'])

    gabor.ori = ori
    gabor.pos = pos


    cuecentral = exp['cuecentral']
    nocue = exp['nocue']
    cuelocation = exp['cuelocation']
    cueupperleft = exp['cueupperleft']
    cueupperright = exp['cueupperright']
    cuelowerleft = exp['cuelowerleft']
    cuelowerright = exp['cuelowerright']
    cueDuration = exp['cueDur']
    cueISI = exp['cueISI']

    cuepos = (trial['x'], trial['y'])
    cuelocation.pos = cuepos

    conditionlist = (trial['condition'])



    try:
        gabor.opacity = exp['trialOpacity'][exp['trialIter']]
        exp['trialIter'] += 1
    except KeyError:
        pass
    try:
        gabor.opacity = trial['opacity']
    except KeyError:
        print("No experimentally set opacity")

    cueDuration = get_frames(exp, cueDuration)
    cueISI = get_frames(exp, cueISI)
    stimulusDuration = get_frames(exp, gaborDuration)

    if gabor.opacity == 0.4:
        stim_trigger = exp['locationResponse']['responseCode'][str(pos)][0]*10 + exp['orientationResponse']['responseCode'][str(ori)][0] + 140
    else:
        stim_trigger = exp['locationResponse']['responseCode'][str(pos)][0]*10 + exp['orientationResponse']['responseCode'][str(ori)][0] + 100

    continueRoutine = True
    frames = 0

    print(trial['condition'])

    while continueRoutine:

        ### CUE CONDITIONS ###
        if frames > fixationDuration + cueDuration:
            fix.draw()
        elif frames > fixationDuration:
            if trial['condition'] == 'nocue':
                fix.draw()
                trigger = 600
            elif trial['condition'] == 'centralcue':
                cuecentral.draw()
                trigger = 700
            elif trial['condition'] == 'locationcue':
                cuelocation.draw()
                trigger = 800
                fix.draw()
            elif trial['condition'] == 'allcue':
                cueupperleft.draw()
                cueupperright.draw()
                cuelowerleft.draw()
                cuelowerright.draw()
                fix.draw()
                trigger = 900
        else:
            fix.draw()

        if exp['EEG'] and fix_send:
            print('Fixation', end='')
            exp['set_data'](10)
            fix_send = False

        if frames > fixationDuration + stimulusDuration + cueDuration + cueISI:
            pass
        elif frames > fixationDuration + cueDuration + cueISI:
            gabor.draw()
            if exp['EEG'] and stim_send:
                print('Stim', end=' ')
                exp['set_data'](stim_trigger)
                print('\t', end='')
                stim_send = False

        exp['win'].flip()

        if frames > fixationDuration + stimulusDuration + postFixationDuration + cueDuration + cueISI:
            continueRoutine = False

        frames += 1

        if exp['keyBoard'].getKeys(keyList=["escape"]):
            print('\n')
            exp['win'].close()
            exp['core'].quit()

    if type(loop).__name__ == 'TrialHandler':
        loop.addData('fixation_dur', fixationDuration)
        loop.addData('cue_dur', cueDuration)
        loop.addData('stimulation_dur', stimulusDuration)
        loop.addData('post_fixation', postFixationDuration)
        loop.addData('opacity', gabor.opacity)
    elif type(loop).__name__ == 'StairHandler':
        loop.addOtherData('fixation_dur', fixationDuration)
        loop.addData('cue_dur', cueDuration)
        loop.addOtherData('stimulation_dur', stimulusDuration)
        loop.addOtherData('post_fixation', postFixationDuration)
        loop.addOtherData('opacity', gabor.opacity)


def create_stair_trial(variable):
    trial = {}
    trial['opacity'] = variable
    trial['orientation'] = choice([-45, 0, 45, 90])
    trial['x'] = choice([-77, 77])
    trial['y'] = choice([-77, 77])
    trial['condition'] = choice(['nocue', 'centralcue'])
    return trial


def get_response(exp, loop, trial, respType=None):

    responseScreen = exp['responseScreen']
    responseScreen.setImage(exp[respType]['image'])

    buttonBox = exp['buttonBox']
    buttonBox.clock.reset()

    # Clear any responses recorded before this screen
    buttonBox.poll_for_response()
    while len(buttonBox.response_queue):
        buttonBox.clear_response_queue()
        buttonBox.poll_for_response()

    pressKey = []
    pressRT = []
    releaseKey = []
    releaseRT = []

    continueRoutine = True

    while continueRoutine:

        resp_send = True

        responseScreen.draw()
        exp['win'].flip()

        # check for key presses
        if exp['keyBoard'].getKeys(keyList=["escape"]):
            print('\n')
            exp['win'].close()
            exp['core'].quit()

        buttonBox.poll_for_response()
        while len(buttonBox.response_queue):
            print(buttonBox.response_queue)
            evt = buttonBox.get_next_response()
            if evt['key'] not in exp[respType]['keys']:
                continue
            if evt['pressed']:
                pressKey.append(evt['key'])
                pressRT.append(buttonBox.clock.getTime())

                if respType == 'locationResponse':
                    value = (trial['x'], trial['y'])
                    resp_trigger = int(evt['key']) * 10
                elif respType == 'orientationResponse':
                    value = trial['orientation']
                    resp_trigger = int(evt['key']) + 100
                elif respType == 'pasResponse':
                    value = exp[respType]['responseCode'][str(evt['key'])][0]
                    resp_trigger = int(value)
                else:
                    resp_trigger = 99

                if exp['EEG'] and resp_send:
                    print(respType[:3], end=' ')
                    exp['set_data'](resp_trigger)

                    resp_send = False
            else:
                releaseKey.append(evt['key'])
                releaseRT.append(buttonBox.clock.getTime())
            buttonBox.poll_for_response()
        buttonBox.clear_response_queue()  # don't process again
        if (len(pressKey) > 0) and (len(releaseKey) > 0):  # at least one key was pressed and released
            continueRoutine = False

    if type(loop).__name__ == 'TrialHandler':
        loop.addData(f'{respType}_pressKey', pressKey[0])
        loop.addData(f'{respType}_pressRT', pressRT[0])
        #loop.addData(f'{respType}_releaseKey', releaseKey[0])
        loop.addData(f'{respType}_releaseRT', releaseRT[0])

    elif type(loop).__name__ == 'StairHandler':
        loop.addOtherData(f'{respType}_pressKey', pressKey[0])
        loop.addOtherData(f'{respType}_pressRT', pressRT[0])
        #loop.addOtherData(f'{respType}_releaseKey', releaseKey[0])
        loop.addOtherData(f'{respType}_releaseRT', releaseRT[0])

    if respType == 'pasResponse':
        return value
    elif pressKey[0] in exp[respType]['responseCode'][str(value)]:
        print(1, end='\t')
        return 1
    else:
        print(0, end='\t')
        return 0


def display_blank(exp, loop, trial, t=500, jitter=True, name='blank'):

    if jitter:
        t += np.random.choice(np.arange(-200, 201, 50))
    duration = get_frames(exp, t)
    continueRoutine = True
    frames = 0

    while continueRoutine:

        exp['win'].flip()

        if frames > duration:
            continueRoutine = False

        frames += 1
    if type(loop).__name__ == 'TrialHandler':
        loop.addData(name, duration)
    elif type(loop).__name__ == 'StairHandler':
        loop.addOtherData(name, duration)
