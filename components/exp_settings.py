# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 16:13:27 2020

@author: Marcin Koculak
"""
from os.path import join  # change it to Path module
import numpy as np

# Turn the main parts of the experiments on/off
performTraining = False
performStaircase = True
performSession = True

EEG = True

# Set the procedure to attenion version
attention = True

# Participant details queried with a prompt at the begging of the experiment
expInfo = {
    'ID': '',
    }

# Response device used (either 'buttonBox' or 'keyboard')
responseDevice = 'buttonBox'

# Where to store the results
resultsFolder = 'data'

# Choose the shape of fixation - cross or dot
fixation_shape = 'cross'

# Timings of displayed elements in miliseconds
cue_dur = 100
cue_ISI = 400
fixation_dur = 1500
gabor_dur = 33
post_fixation_dur = 1200


# Code details of location response block, mapping keys to locations.
# Change dist variable to adjust gabor placement (8 deg -> 306px).
dist = 77 # 2 deg
locationResponse = {
    'image': join('materials', 'locations.png'),
    'keys': [2, 3, 4, 5],
    'correct': None,
    'responseCode': {
        f"({dist}, {dist})": [5],
        f"({dist}, {-dist})": [4],
        f"({-dist}, {dist})": [2],
        f"({-dist}, {-dist})": [3]
        }
    }

# Code details of orientation response block, mapping keys to orientations.
orientationResponse = {
    'image': join('materials', 'orientations.png'),
    'keys': [0, 1, 6, 7],
    'correct': None,
    'responseCode': {
        "0": [0],
        "-45": [1],
        "90": [6],
        "45": [7]
        }
    }

# Code details of PAS response block, mapping keys to scale points.
pasResponse = {
    'image': join('materials', 'pas.png'),
    'keys': [0, 1, 6, 7],
    'correct': None,
    'responseCode': {
        "0": [1],
        "1": [2],
        "6": [3],
        "7": [4]
        }
    }

# Defines staircase properties, including the stepping function.
staircase = {
    'nTrials': 70,
    'nReversals': 10,
    'startVal': 0.1,
    'stepType': 'log',
    'stepSizes': np.log(10/8)/np.log(10),       # Next step is 20% lower/higher
    # 'stepSizes': [0.05,0.05,0.02,0.02,0.001],
    'minVal': 0,
    'maxVal': 1,
    'nUp': 1,
    'nDown': 2,
    'applyInitalRule': False
    }

# How many samples from the end of staircase will be included in calculation of
# the final opacity level.
stairSamples = 40

# How many trials in the test session (only increments of 64)
trial_num = 384

# After how many trials there should be a break
block_length = 16
