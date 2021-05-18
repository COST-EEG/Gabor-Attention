import numpy as np

from psychopy import core, gui
(
from components.structure import create_structure, setup_EEG, save_json
from components.routines import (display_instruction_screen, display_stimulus,
                                 create_stair_trial, get_response,
                                 display_blank)

exp = create_structure()
exp['core'] = core

setup_EEG(exp)

display_instruction_screen(exp, image=exp['welcome'], trigger=200)
display_instruction_screen(exp, image=exp['training_instruction'], trigger=201)
display_instruction_screen(exp, image=exp['location_instruction'], trigger=202)
display_instruction_screen(exp, image=exp['orientation_instruction'], trigger=203)
display_instruction_screen(exp, image=exp['pas_instruction'], trigger=204)


###################
###  STAIRCASE  ###
###################

if exp['performStaircase']:

    display_instruction_screen(exp, image=exp['staircase_start'], trigger=205)

    staircaseLoop = exp['staircaseTrials']
    print('\n', 'Staircase started:')

    posCorr = []
    oriCorr = []

    for variable in staircaseLoop:
        trial = create_stair_trial(variable)
        staircaseLoop.addOtherData('name', 'staircase')
        staircaseLoop.addOtherData('globalTime', exp['globalClock'].getTime())

        display_stimulus(exp, staircaseLoop, trial)
        #display_blank(exp, staircaseLoop, trial, name='postStim')

        orientationCorrect = get_response(exp, staircaseLoop, trial, respType='orientationResponse')

        staircaseLoop.addResponse(orientationCorrect)
        oriCorr.append(orientationCorrect)

        exp['data'].nextEntry()

    print('\n\n', f'Staircase ended with value: {staircaseLoop.intensities[-1]}')

    samples = exp["stairSamples"]
    print(f'Accuracy of position response for the last {samples} trials: {np.mean(posCorr[-samples:])}')
    print(f'Accuracy of orientation response for the last {samples} trials: {np.mean(oriCorr[-samples:])}')

##################
###  TRAINING  ###
##################

if exp['performTraining']:

    loop = exp['trainingTrials']
    for trial in loop:
        loop.addData('name', 'session')
        loop.addData('globalTime', exp['globalClock'].getTime())

        print('')
        print(f'Block {loop.thisRepN}:\t', end='')
        print(f'Trial {loop.thisTrialN}:\t', end='')

        exp['trainingClock'].reset()

        display_stimulus(exp, loop, trial)

        #display_blank(exp, loop, trial, name='postStim')

        get_response(exp, loop, trial, respType='locationResponse')

        get_response(exp, loop, trial, respType='orientationResponse')

        get_response(exp, loop, trial, respType='pasResponse')
        exp['data'].nextEntry()

        print(f'T-trial {round(exp["trainingClock"].getTime(),2)}s', end='\t')


######################
###  TEST SESSION  ###
######################

if exp['performSession']:

    display_instruction_screen(exp, image=exp['session_start'], trigger=206)

    try:
        opacity = np.mean(staircaseLoop.intensities[-samples:])
        try:
            exp['data'].addData('finalOpacity', opacity)
            exp['data'].nextEntry()
        except:
            pass
        print('\n', f'Setting the opacity based on mean value from last {samples} trials to {opacity}', sep='')
    except:
        opacity = 0.02
        print('\n', f'Setting the opacity based on preset value to {opacity}', sep='')

    exp['finalOpacity'] = opacity
    exp['trialOpacity'] = [opacity]*384
    np.random.shuffle(exp['trialOpacity'])
    exp['trialIter'] = 0

    timer = core.Clock()

    loop = exp['experimentTrials']
    for trial in loop:
        loop.addData('name', 'session')
        loop.addData('globalTime', exp['globalClock'].getTime())

        print('')
        print(f'Block {loop.thisRepN}:\t', end='')
        print(f'Trial {loop.thisTrialN}:\t', end='')

        exp['trialClock'].reset()

        display_stimulus(exp, loop, trial)
        #display_blank(exp, loop, trial, 1000, name='postStim')

        get_response(exp, loop, trial, respType='locationResponse')
        display_blank(exp, loop, trial, 1000, name='postLoc')

        get_response(exp, loop, trial, respType='orientationResponse')
        display_blank(exp, loop, trial, 1000, name='postOri')

        get_response(exp, loop, trial, respType='pasResponse')
        exp['data'].nextEntry()

        print(f'T-trial {round(exp["trialClock"].getTime(),2)}s', end='\t')
        print(f'T-total {round(timer.getTime(),2)}s', end='')

        # if timer.getTime() > 3600:
        #    break

        if ((loop.thisN + 1) % exp['blockLength']) == 0:
            display_instruction_screen(exp, image=exp['break'], trigger=230)


#######################
###  SAVE & FINISH  ###
#######################

display_instruction_screen(exp, image=exp['end'], trigger=207)

save_json(exp)

exp['win'].close()
core.quit()
