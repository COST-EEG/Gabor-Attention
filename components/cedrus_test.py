# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 23:03:51 2020

@author: Praca
"""

from psychopy import core, visual
from psychopy.hardware import keyboard

import pyxid2 as pyxid

win = visual.Window(
    size=[1920, 1080], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0.725,0.725,0.725], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='pix')

text = visual.TextStim(win)

key = keyboard.Keyboard()

devices = pyxid.get_xid_devices()
core.wait(0.1)
cedrus = devices[0]

run = True

while run:
    text.draw()
    win.flip()
    
    cedrus.poll_for_response()
    if len(cedrus.response_queue):
        evt = cedrus.get_next_response()
        text.setText(evt['key'])
    
    char = key.getKeys()
    if char:
        if char[-1].name == 'escape':
            run = False
        else:
            text.setText(char[-1].name)

win.close()
core.quit()