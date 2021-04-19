# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 16:09:12 2020

@author: Marcin Koculak
"""
import numpy as np
import json
from collections import OrderedDict

from psychopy import core, visual, data, logging, gui
from psychopy.hardware import keyboard

from os.path import join  # change it to Path module

from .exp_settings import (staircase, expInfo, responseDevice, resultsFolder,
                           fixation_shape, fixation_dur, gabor_dur, cue_dur, cue_ISI,
                           post_fixation_dur, trial_num, block_length, attention,
                           locationResponse, orientationResponse, pasResponse,
                           EEG, stairSamples, performTraining, performStaircase,
                           performSession)

def create_structure():
    '''
    This function creates the core structure of the experiment, which is
    a dictionary containing all important components of the experiment.

    It is used to store all the settings, experimental components like stimuli
    or response screens, and participant responses.

    On top of results datafiles and logs, this structure is saved into a json
    file after each session, allowing to retrieve many additional information
    about the experiments execution.
    '''
    structure = {}

    gui.DlgFromDict(expInfo)

    structure['expInfo'] = expInfo

    structure['performTraining'] = performTraining
    structure['performStaircase'] = performStaircase
    structure['performSession'] = performSession

    structure['EEG'] = EEG

    structure['attention'] = attention

    # Create clocks for the experiment
    structure['globalClock'] = core.Clock()
    structure['trainingClock'] = core.Clock()
    structure['trialClock'] = core.Clock()

    # Create a chosen response device
    structure['responseDevice'] = responseDevice
    structure['keyBoard'] = keyboard.Keyboard()
    structure['buttonBox'] = None

    structure['stairSamples'] = stairSamples

    if responseDevice == 'buttonBox':
        try:  # to use the Cedrus response box
            import pyxid2 as pyxid
        except ImportError:
            import pyxid

        for n in range(10):  # doesn't always work first time!
            try:
                devices = pyxid.get_xid_devices()
                core.wait(0.1)
                structure['buttonBox'] = devices[0]
                structure['buttonBox'].clock = core.Clock()
                break  # found the device so can break the loop
            except Exception:
                pass
        if not structure['buttonBox']:
            logging.error('could not find a Cedrus device.')
            core.quit()

    # Create a filename for the results
    date = data.getDateStr()
    structure['expFileName'] = join(resultsFolder, expInfo['ID']+'_'+date)

    # Create an experimental window
    structure['win'] = visual.Window(
        size=[1920, 1080],
        screen=1,
        fullscr=True,
        checkTiming=True,
        color='grey',
        monitor='testMonitor',
        colorSpace='rgb'
        )

    structure['frameRate'] = round(structure['win'].getActualFrameRate(),0)
    structure['expInfo']['frameRate'] = structure['frameRate']

    structure['data'] = data.ExperimentHandler(
        name='test',
        extraInfo=expInfo,
        dataFileName=structure['expFileName']
        )

    structure['instructionScreen'] = visual.ImageStim(
        win=structure['win'],
        image=None,
        interpolate=True,
        depth=-1.0
        )

    crossVert = [(6, 1),
                 (6, -1),
                 (1, -1),
                 (1, -6),
                 (-1, -6),
                 (-1, -1),
                 (-6, -1),
                 (-6, 1),
                 (-1, 1),
                 (-1, 6),
                 (1, 6),
                 (1, 1)
                 ]

    structure['fixationCross'] = visual.ShapeStim(
        win=structure['win'],
        vertices=crossVert,
        units='pix',
        lineWidth=0,
        fillColor='white'
        )

    structure['dot'] = visual.Circle(
        win=structure['win'],
        units='pix',
        size=8,
        fillColor='white',
        lineWidth=0
        )

    structure['cuelocation'] = visual.ShapeStim(
        win=structure['win'], name='polygon', vertices='star7',
        size=(10, 10), units='pix',
        ori=0, pos=(0, 0),
        lineWidth=0.01, lineColor='black', lineColorSpace='rgb',
        fillColor='black', fillColorSpace='rgb',
        opacity=1, depth=0.0, interpolate=True)

    structure['cuecentral'] = visual.ShapeStim(
        win=structure['win'], name='polygon', vertices='star7',
        size=(10, 10), units='pix',
        ori=0, pos=(0, 0),
        lineWidth=0.01, lineColor='black', lineColorSpace='rgb',
        fillColor='black', fillColorSpace='rgb',
        opacity=1, depth=0.0, interpolate=True)

    structure['cueupperleft'] = visual.ShapeStim(
        win=structure['win'], name='polygon', vertices='star7',
        size=(10, 10), units='pix',
        ori=0, pos=(-77, 77),
        lineWidth=0.01, lineColor='black', lineColorSpace='rgb',
        fillColor='black', fillColorSpace='rgb',
        opacity=1, depth=0.0, interpolate=True)

    structure['cueupperright'] = visual.ShapeStim(
        win=structure['win'], name='polygon', vertices='star7',
        size=(10, 10), units='pix',
        ori=0, pos=(77, 77),
        lineWidth=0.01, lineColor='black', lineColorSpace='rgb',
        fillColor='black', fillColorSpace='rgb',
        opacity=1, depth=0.0, interpolate=True)

    structure['cuelowerleft'] = visual.ShapeStim(
        win=structure['win'], name='polygon', vertices='star7',
        size=(10, 10), units='pix',
        ori=0, pos=(-77, -77),
        lineWidth=0.01, lineColor='black', lineColorSpace='rgb',
        fillColor='black', fillColorSpace='rgb',
        opacity=1, depth=0.0, interpolate=True)

    structure['cuelowerright'] = visual.ShapeStim(
        win=structure['win'], name='polygon', vertices='star7',
        size=(10, 10), units='pix',
        ori=0, pos=(77, -77),
        lineWidth=0.01, lineColor='black', lineColorSpace='rgb',
        fillColor='black', fillColorSpace='rgb',
        opacity=1, depth=0.0, interpolate=True)

    structure['nocue'] = visual.ShapeStim(
        win=structure['win'],
        vertices=crossVert,
        units='pix',
        lineWidth=0,
        fillColor='white'
        )

    arrowVert = [(-15, 3),
                 (-15, -3),
                 (0, -3),
                 (0, -9),
                 (15, 0),
                 (0, 9),
                 (0, 3)]

    structure['arrow'] = visual.ShapeStim(
        win=structure['win'],
        units='pix',
        vertices=arrowVert,
        fillColor='black',
        lineWidth=0
        )

    structure['gabor'] = visual.GratingStim(
        win=structure['win'],
        name='gaborUpLeft',
        units='pix',
        tex='sin',
        mask='gauss',
        ori=45,
        pos=(0, 0),
        size=(128, 128),
        sf=1.5 / 40.0,
        phase=1.0,
        color=1.0,
        colorSpace='rgb',
        opacity=0.2,
        texRes=512,
        interpolate=True,
        depth=-2.0
        )

    structure['responseScreen'] = visual.ImageStim(
        win=structure['win'],
        image=None,
        interpolate=True,
        depth=-1.0
        )

    structure['fixationShape'] = fixation_shape
    structure['fixationDur'] = fixation_dur
    structure['postFixationDur'] = post_fixation_dur
    structure['cueDur'] = cue_dur
    structure['cueISI'] = cue_ISI
    structure['gaborDur'] = gabor_dur
    
    structure['blockLength'] = block_length

    # Create instruction screens
    structure['welcome'] = join('materials/instructions', '1_welcome.png')
    structure['training_instruction'] = join('materials/instructions', '2_instruction.png')
    structure['location_instruction'] = join('materials/instructions', '3_location_demo.png')
    structure['orientation_instruction'] = join('materials/instructions', '4_orientation_demo.png')
    structure['pas_instruction'] = join('materials/instructions', '5_pas_demo.png')
    structure['training_start'] = join('materials/instructions', '6_training_start.png')
    structure['training_end'] = join('materials/instructions', '7_training_end.png')
    structure['correct_screen'] = join('materials/instructions', '8_correct.png')
    structure['incorrect_screen'] = join('materials/instructions', '9_incorrect.png')
    structure['staircase_start'] = join('materials/instructions', '10_staircase_start.png')
    structure['session_start'] = join('materials/instructions', '11_session_start.png')
    structure['break'] = join('materials/instructions', '12_break.png')
    structure['end'] = join('materials/instructions', '13_end.png')


    structure['training_trials_file'] =  join('materials', 'training_trials.csv')
    # structure['trainingConditions'] = data.importConditions(structure['training_trials_file'])
    structure['trainingConditions'] = data.importConditions(structure['training_trials_file'], selection='0:5')
    structure['trainingTrials'] = data.TrialHandler(structure['trainingConditions'], nReps=1)
    structure['data'].addLoop(structure['trainingTrials'])

    #structure['trials_file'] =  join('materials', 'experiment_trials.csv')
    #structure['experimentConditions'] = data.importConditions(structure['trials_file'])
    #structure['experimentTrials'] = data.TrialHandler(structure['experimentConditions'], nReps=trial_num/16)
    #structure['data'].addLoop(structure['experimentTrials'])
    
    structure['trials_file'] =  join('materials', 'experiment_trials_cue.csv')
    structure['experimentConditions'] = data.importConditions(structure['trials_file'])
    structure['experimentTrials'] = data.TrialHandler(structure['experimentConditions'], nReps=trial_num/64)
    structure['data'].addLoop(structure['experimentTrials'])
    

    structure['locationResponse'] = locationResponse
    structure['orientationResponse'] = orientationResponse
    structure['pasResponse'] = pasResponse

    structure['staircaseTrials'] = data.StairHandler(**staircase)
    structure['data'].addLoop(structure['staircaseTrials'])
    return structure


def setup_EEG(exp):
    # Check if labjack library is present
    if exp['EEG']:
        try:
            import u3
            print('Labjack library imported.')
        except:
            print('No Labjack library found.')

        # Check if labjack is conneScted and recognized by the library.
        # This might require installing drivers to work.
        try:
            trigger = u3.U3()
            exp['EEG'] = True
        except:
            print('No Labjack device connected. Switching to test mode.')
            exp['EEG'] = False

    # Create a helper function to send triggers to the EEG via Labjack
    # or create a dummy function just to print the triggers for the test mode.
    if exp['EEG']:
        port = 6701

        trigger.writeRegister(6750, 65535)  # set as out port
        trigger.writeRegister(6751, 65535)  # set as out port
        trigger.writeRegister(port+1, 65280)  # start low
        trigger.writeRegister(port, 65280)  # start low

        def set_data(number, port=port, wait=0.001):
            trigger.writeRegister(port, 65280+number)
            core.wait(wait)
            print('TR {}'.format(number), end='\t')
            trigger.writeRegister(port, 65280)

        exp['set_data'] = set_data

        exp['set_data'](244)
        print('')

    else:
        def set_data(number, wait=0.001):
            print('TR {}.'.format(number), end='\t')

        exp['set_data'] = set_data

        exp['set_data'](244)
        print('')


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


def save_json(exp):
    exp['data'].saveAsWideText(exp['expFileName'], delim=',')

    expsave = {}
    for key, value in exp.items():
        if type(value) in [str, dict, OrderedDict, list]:
            expsave[str(key)] = value
        elif value in [data.TrialHandler]:
            expsave[str(key)] = repr(value)
        else:
            expsave[str(key)] = str(value)
    with open(exp['expFileName']+'.json', 'w') as file:
        json.dump(expsave, file, default=np_encoder)
