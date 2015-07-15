### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### January 30th, 2012

# ************************************
# *    DESIGN OF THE EXPERIMENT 2    *
# *'Trial Tracks for each RUN-STAGE' *
# ************************************



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
from __future__ import division
import copy
import numpy as np
import random as rd
import scipy as sp
import time


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL VARIABLES
# @@@@@ Initialization of Cue-Driven System @@@@@
BUFSIZ = 1024
triggers = {'left':'7*', 'right':'8*', 'idle':'9*'}
# @@@@@ Brain States @@@@@
L = '2*cue_left'
R = '3*cue_right'
I = '4*cue_idle'
# @@@@@ Default Tracks @@@@@
default_tracks = {21:[R,R,L,R,R,R,L,L,L,R,L,R,R,L,L,R,L,R,R,L,L,L,R,L,R,L,R,R,L,L,L,R,R,R,L,R,R,L,L,L],\
                  22:[R,L,R,L,L,L,L,R,R,R,R,R,L,R,R,L,R,R,R,L,R,L,L,R,R,L,R,L,R,R,L,L,L,L,R,L,R,L,L,L],\
                  23:[R,R,R,R,L,R,R,R,L,L,L,L,R,R,L,R,L,L,R,L,R,R,R,L,R,R,R,L,L,L,L,L,R,R,L,L,R,L,L,L],\
                  24:[R,R,L,R,R,R,R,R,R,R,L,R,R,R,L,L,L,R,L,L,L,R,R,L,L,L,L,R,R,L,L,R,L,L,L,R,L,R,L,L],\
                  31:[R,L,R,R,L,R,R,R,L,R,L,R,L,R,L,R,R,R,L,R,L,L,L,R,L,R,L,R,R,L,L,L,L,R,L,R,L,L,R,L],\
                  32:[R,L,R,R,R,R,L,R,L,L,R,L,R,L,L,R,L,L,L,R,L,R,L,R,R,L,L,L,R,L,R,L,R,R,L,L,R,R,L,R],\
                  33:[R,R,L,R,L,L,L,R,R,L,R,L,L,R,R,R,L,R,L,R,L,L,L,R,L,R,L,R,L,L,L,R,R,L,L,R,R,L,R,R],\
                  34:[R,L,R,L,R,R,L,R,L,R,L,R,L,L,L,R,L,R,L,R,R,L,L,R,L,L,L,R,R,R,L,L,R,R,L,L,R,L,R,R],\
                  41:[L,R,L,L,R,L,L,L,R,L,R,L,R,L,R,L,R,R,L,R,R,R,L,R,R,L,R,L,L,R,R,L,R,L,R,R,L,L,R,L],\
                  42:[R,R,R,L,L,L,R,L,R,R,L,R,L,L,R,R,L,L,L,R,L,R,R,R,L,R,L,L,R,L,R,R,R,L,R,L,L,L,R,L],\
                  43:[L,L,R,L,L,R,L,L,R,L,L,R,R,L,L,R,L,R,R,R,L,L,R,L,R,L,R,R,R,R,R,L,L,R,L,R,L,R,L,R],\
                  44:[R,L,R,R,R,L,R,R,L,R,R,L,R,L,R,L,R,L,R,R,L,L,R,L,R,L,L,L,R,R,L,R,R,L,L,L,L,R,L,L],\
                  51:[L,R,L,L,L,R,L,R,L,L,R,L,R,L,R,L,R,R,L,R,L,R,L,L,R,L,R,L,R,R,R,R,L,L,R,R,L,R,L,R],\
                  52:[R,R,L,R,L,L,L,R,R,L,L,R,L,R,L,L,R,R,R,L,R,R,L,R,L,R,L,L,L,R,L,R,L,R,L,R,R,L,R,L],\
                  53:[R,L,R,R,L,R,R,R,L,R,R,L,R,L,R,L,L,R,R,L,L,L,R,R,L,L,R,R,R,L,R,L,L,L,R,L,L,R,L,L],\
                  54:[R,R,R,L,L,L,R,R,R,L,L,L,R,L,R,R,L,R,L,R,L,R,L,R,L,L,R,R,L,R,L,R,R,L,R,L,R,L,L,L]}
# @@@@@ Cue-Driven Systems & Target-Driven Systems @@@@@
Cues_Targets = {'cue-driven':   [([L,R,R,R,R,R,L],[6]), ([R,R,R,L,R,L,R,R,L],[None]), ([R,R,L,R,R,R,L,R,L,L],[6,7]),\
                                 ([R,L],[0]), ([R,L],[3]),([R,L,R,L,R,R,R,R,R,R,R,L],[None]), ([R,L,R,L,R,L],[2]),\
                                 ([R,L],[0]), ([R,R,R,R,R,L],[0]), ([R,L,R,R,L,R,R,R,R,R,R,L,L,L],[0,2,3])],\
                'target-driven':[('*target1-Doorbell.mp3'    , '230'), ('*target2-Hello.wav'        , '307'),\
                                 ('*target3-WaterPouring.mp3', '064'), ('*target4-HandWashing.mp3'  , '017'),\
                                 ('*target5-BaconFrying.mp3' , '066'), ('*target6-GoodBye.mp3'      , '307'),\
                                 ('*target7-Farting.mp3'     , '030'), ('*target8-BrushingTeeth.mp3', '010'),\
                                 ('*target9-Yawning.wav'     , '075')]}



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATIONS


# ---------- F1. Training Stages of the Session 1 ----------
def Session1_Tracks(stage, run, Idle_ON, numtr_run):
    'Run-Tracks for each Stage of Session 1'
    
    # (a) Variable Declaration
    cue_labels = [L, R]    
    stage += 1
    # (b) Cue-Labelling Process
    # --- STAGE: Motor Imagery Training
    if stage == 1:
        cue_labels = cue_labels * numtr_run[0]        
        if Idle_ON: cue_labels.extend([I] * numtr_run[-1])
        rd.shuffle(cue_labels)
    # --- STAGES: Command Training & GUI Training
    else:
        cue_labels = default_tracks[(stage*10) + run]
        if Idle_ON: cue_labels = Idle_Labelling(cue_labels, [I] * numtr_run[-1])    
    return cue_labels


# --------- F2. Training Stages of the Session 2/3 ---------
def Session23_Tracks(session, stage, run, Idle_ON, numtr_run):
    'Run-Tracks for Training-Stages of Sessions 2 & 3'
    
    # (a) Variable Declaration
    cue_labels = [L, R]    
    # (b) Cue-Labelling Process
    # --- STAGE: GUI Training
    if stage == 'training':
        cue_labels = default_tracks[(session+2)*10 + run]
        if Idle_ON: cue_labels = Idle_Labelling(cue_labels, [I] * numtr_run[-1])
    # --- STAGE: GUI Testing
    elif stage == 'testing':
        cue_labels = cue_labels * numtr_run[0]
        if Idle_ON: cue_labels.extend([I] * numtr_run[-1])
        rd.shuffle(cue_labels)
    return cue_labels


# ---------- F3. Cues & Targets for System Control ---------
def Session23_CueTarget(SysType):
    'Cues & Targets to Control the BCI-System'
    
    return Cues_Targets[SysType]
    

# -------------- F4. Labelling the Idle State --------------
def Idle_Labelling(cue_labels, idle_label):
    'Idle Brain State Labels'
    
    while idle_label != []:
        item = idle_label.pop()
        index= rd.randint(0, len(cue_labels))
        cue_labels.insert(index, item)
    return cue_labels


# --------- F5. Removal of the Achieved Targets ------------
def Achieved_Targets(TCPmsg, prev_target, targets, codes):
    'Removal of the Achieved Targets from the Current List'
    
    # (a) Check-up of conditions
    conditions = [item == L for item in targets]
    conditions.append(prev_target == R)
    conditions.append(codes[0] != None)
    #(b) Decision of removing or leaving the current target
    if all(conditions):
        ans, position, length = TCPmsg.split('_')
        current_pos = int(position) 
        new_targets = []
        for index in range(len(targets)):
            target_pos = codes[index]
            num_idle = target_pos - current_pos
            if current_pos > target_pos: num_idle += int(length)
            new_targets.extend([I] * num_idle)
            new_targets.append(item)
            # -- finishing the current target,the cursor will be moved 
            #    automatically to next position
            current_pos = target_pos + 1
    else:
        new_targets = targets
    return new_targets



# ------ F6. Starting Point of the Cue-Driven System -------
def Initialization_CueDriven(tcpCliSock):
    'Starting Point of the Cue-Driven System'
    
    # (a) Default track to follow
    targets = [R,L,R,R,R,L,R,L,R,R,R]
    # (b) Drawing the default track
    for target in targets:
        # -- warning
        tcpCliSock.send('1*warning')
        tcpCliSock.recv(BUFSIZ)
        time.sleep(1.5)
        # -- cue delivery
        tcpCliSock.send(target)
        tcpCliSock.recv(BUFSIZ)
        time.sleep(1.5)
        # -- action exection
        t   = target.split('_')[-1]
        cmd = ''.join([triggers[t], t, '_', t])
        tcpCliSock.send(cmd)
        tcpCliSock.recv(BUFSIZ)
        time.sleep(1.5)
    
    

