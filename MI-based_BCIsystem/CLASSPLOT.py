### VE PROJECT: Human-Computer Interface Design
### Luz Maria Alonso Valerdi
### Essex BCI Group
### January 26th, 2012

# ************************************
# *       BIOSIGNAL PROCESSING       *
# *      'Feature Classifiers'       *
# ************************************



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# MODULES IMPORTS
# ....................Python Libraries......................
from __future__ import division
import copy
import numpy as np
import scipy as sp
import mlpy 
import svmutil as libsvm
from IIR_Filters import filtfilt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter



# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# GLOBAL CONSTANT DECLARATION
layout_labels =  ['Fp1','AF7','AF3','F1' ,'F3' ,'F5' ,'F7' ,'FT7',
                  'FC5','FC3','FC1','C1' ,'C3' ,'C5' ,'T7' ,'TP7',
                  'CP5','CP3','CP1','P1' ,'P3' ,'P5' ,'P7' ,'P9' ,
                  'PO7','PO3','O1' ,'Iz' ,'Oz' ,'POz','Pz' ,'CPz',
                  'Fpz','Fp2','AF8','AF4','AFz','Fz' ,'F2' ,'F4' ,
                  'F6' ,'F8' ,'FT8','FC6','FC4','FC2','FCz','Cz' ,
                  'C2' ,'C4' ,'C6' ,'T8' ,'TP8','CP6','CP4','CP2',
                  'P2' ,'P4' ,'P6' ,'P8' ,'P10','PO8','PO4','O2'  ]
MIMov = ['Left MI', 'Rigth MI', 'Idle', 'Current BS']
colours_lines = ['b', 'g', 'r', 'k', 'm','c','y']
colours_marker = ['b-.', 'g-.', 'r', 'k', 'm--','c--','y']
Titles = ['LEFT Imaginary Movement','RIGHT Imaginary Movement','IDLE Brain State']
root = 'C:\\Documents and Settings\\lmalon\\Desktop\\'


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# FUNCTION DECLARATION
# ------------------- F1. Window Library -------------------
def WinLibrary(choice, segment):
    'Digital Window Selection'

    if   choice == 'Bartlett':
        WindoW = sp.signal.bartlett(segment)
    elif choice == 'Blackman':
        WindoW = sp.signal.blackman(segment)
    elif choice == 'Boxcar':
        WindoW = sp.signal.boxcar(segment)
    elif choice == 'FlatTop':
        WindoW = sp.signal.flattop(segment)
    elif choice == 'Gaussian':
        WindoW = sp.signal.gaussian(segment)
    elif choice == 'Hamming':
        WindoW = sp.signal.hamming(segment)
    elif choice == 'Triangular':
        WindoW = sp.signal.triang(segment)
    elif choice == 'Hanning':
        WindoW = sp.signal.hanning(segment)
    return WindoW
# ----------------------------------------------------------


# ------------------- F2. Color Converter ------------------
ColourConverter = lambda arg: colorConverter.to_rgba(arg, alpha = 0.6)
# ----------------------------------------------------------


# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# CLASS DECLARATION

class Class_Plot():
    'Methods to Train & Test a Selected Group of Classifiers'
    
    
    # -------------- METHOD 1: Initialization --------------
    def __init__(self, BCIparameters):
        'Variable Reassignment of "bci_output" from BCI_gui()'
        
        # (a) bci_output parameters
        self.BCI_type = BCIparameters[0][0]
        # --> offline system
        if BCIparameters[0][0] == 'offline':
            self.samples  = BCIparameters[0][4]
            self.Fs       = BCIparameters[0][7]
            self.SegLen   = BCIparameters[0][8]
        # --> online system
        elif BCIparameters[0][0] == 'online':
            self.samples  = range(BCIparameters[0][8])
            self.Fs       = BCIparameters[0][5]
            self.SegLen   = BCIparameters[0][6]       
        # --> offline & online systems    
        #   + SigCon    
        self.Fdown        = BCIparameters[1][0]
        self.ch_pos       = BCIparameters[1][2]
        TrialTrain        = BCIparameters[0][5]
        TrialTest         = BCIparameters[0][6]        
        #   + FeaSel        
        self.DBI          = BCIparameters[3][0]
        self.RFE          = BCIparameters[3][1][0]
        self.DBIfeatures  = BCIparameters[3][2][0]
        self.DBIrange     = BCIparameters[3][2][1]
        self.RFEfeatures  = BCIparameters[3][3][0]
        self.RFErange     = BCIparameters[3][3][1]
        #   + Classifier        
        self.Classifier   = BCIparameters[4][0]
        self.Class_Label  = BCIparameters[4][1] 
        self.StandardScore= BCIparameters[4][3]
        #    + Plots               
        self.mental_states= BCIparameters[5][7][0]
        self.labels_ch    = BCIparameters[5][7][1]
        self.win_len      = BCIparameters[5][7][4]
        self.window       = BCIparameters[5][7][5]
        self.overlapping  = BCIparameters[5][7][6]
        self.overlap_bs   = BCIparameters[5][7][7]
        self.overlap_ch   = BCIparameters[5][7][8]        
        # (b) Default Parameters
        Idle_ON = False  
        if self.Class_Label[-1] != 0: Idle_ON = True  
        self.Idle_ON = Idle_ON   
        # (c) Calculated Parameters
        Ntrials = min(len(TrialTrain), len(TrialTest))
        Nsets   = 10
        if Ntrials < Nsets: Nsets = Ntrials
        self.Nsets = Nsets 
        
    
    # ---------- METHOD 2: Labelling the Features ----------
    def Feature_Labels(self, Noverlap_Samples, active_bands, features, bsMAT_idxs):
        'Labels for channel, band and time (feature labelling process)'
        
        # (1) Local Variable Declaration
        ch_labels, band_labels, all_labels = [], [], []
        Bands = ['Theta','LowerTheta','UpperTheta','Alpha','LowerAlpha','UpperAlpha',\
                 'Beta','LowerBeta','UpperBeta','Gamma','Whole'] 
        # --- number of samples per MI        
        if self.BCI_type == 'online': 
            MI_samples   = self.samples
            segmentation = self.SegLen
        # --- channel labels
        for ch in self.ch_pos: ch_labels.append(layout_labels[ch])        
        # --- freq band labels
        for index in range(len(Bands)): 
            if active_bands[index][0] == 'on': band_labels.append(Bands[index])        
        # (2) Variable Calculation per available Brain State
        for idx in bsMAT_idxs:
            labels = []
            # --- number of samples per MI        
            if self.BCI_type == 'offline': 
                MI_samples   = self.samples[idx]
                segmentation = self.SegLen[idx]            
            # --- time point labels
            step = int((Noverlap_Samples/self.Fdown)*1000)
            MITime  = int((len(MI_samples)/self.Fs)*1000)
            SegTime = int(segmentation*1000)                   
            start, time_start, stop, time_stop = 0, [], SegTime, []
            while True:            
                time_start.append(str(start))
                start += step            
                time_stop.append(str(stop))
                stop += step
                if (start+SegTime) > MITime: break     
            # --- required parameters
            NumSeg    = len(time_start)
            NumSeg_Ch = len(time_start) * len(band_labels) 
            time_start= time_start * len(band_labels)
            time_stop = time_stop  * len(band_labels)  
            # (3) Labelling Process per available Brain State
            for feature in features:
                ch_idx   = int(feature//NumSeg_Ch)
                time_idx = int(feature-(NumSeg_Ch * ch_idx))
                band_idx = int(time_idx//NumSeg)
                time     = time_start[time_idx-1] + '~' + time_stop[time_idx-1] + 'ms'
                labels.append('_'.join([ch_labels[ch_idx],band_labels[band_idx],time]))
            # (4) Storing the feature_labels per brain-state
            all_labels.append(labels)
        return all_labels 
    
    
    # --- METHOD 3: Data Organization for Classification ---
    def Organization_Features(self, Selection_Out, numfea):
        'Feature Organization according to Number of Classes and Subsets'
        
        # (1) Local Variable Declaration
        # --- feature organization
        #     FEATURE_IDX = [[run1_classifier1_MIvsIDLE_features, run1_classifier2_LEFTvsRIGHT_features],\
        #                    [run2_classifier1_MIvsIDLE_features, run2_classifier2_LEFTvsRIGHT_features],\
        #                 ...[runM_classifier1_MIvsIDLE_features, runM_classifier2_LEFTvsRIGHT_features]]
        FEATURE_IDX, feature_indices, Range, step = [], [], [], 0
        # (2) Data Organization: Feature Selection and use of these selected features for Classification
        # 2.1 Use of "DBI" feature selection to classify the classes
        if all([self.DBI, self.DBIfeatures]):
            # --- whenever the differences among the ranges are equal, the system will create subsets based
            #     on the unique difference for the classification process
            DIFFs = np.unique(np.diff(self.DBIrange))
            if len(DIFFs) == 1: step = DIFFs[0]           
            # --- if users insert MIXED ranges (e.g., [1:100, 256, 301]), the system will not do 
            #     subsets and it only will take these as feature indexes for classifying the patterns.
            #     Then, the features will be classified in one run
            if step == 0:
                # a- from the feature_indices previously ordered by the DBI procedure 
                #    (i.e., selection_out['DBI']) taking only the features selected 
                #    by the user (i.e., DBIrange)
                indices = np.array(selection_out['DBI'][self.DBIrange], dtype = int).tolist()
                indices.sort()
                # b- insertion of the feature-indices for classifier LEFTvsRIGHT
                feature_indices.append(indices)
                # c- insertion of the feature-indices for classifier MIvsIDLE
                if self.Idle_ON: feature_indices.append(indices) 
                FEATURE_IDX.append(feature_indices)
            # --- if users insert ranges (i.e., [1:2:300] or [1:490]) features will be classified 
            #     per subsets. This means, it will classify according to the subsets created according
            #     to the step (i.e, step = 2 or step = 1 from the previous example) and after it will be
            #     creating new subsets obeying the peak classification accuracies. The system will do 
            #     stop/step (i.e., 1000/10) subsets to assess the classification process via stop/step runs.
            else:       
                # a- creation of the boundaries of each run
                self.DBIrange.append(self.DBIrange[-1]+step)
                start = self.DBIrange[0]
                # b- insertion of the feature-indices for each run
                for end in self.DBIrange[1:]:
                    indices = np.array(Selection_Out['DBI'][start:end], dtype = int).tolist()
                    indices.sort()
                    # insertion of the feature-indices for classifier LEFTvsRIGHT
                    feature_indices.append(indices)                
                    # insertion of the feature-indices for classifier MIvsIDLE
                    if self.Idle_ON: feature_indices.append(indices)
                    FEATURE_IDX.append(feature_indices)   
                    feature_indices = []    
            # --- number of features used for the classification
            Range = self.DBIrange     
        # 2.2 Use of "RFE" feature selection to classify the classes
        elif all([self.RFE, self.RFEfeatures]):
            DIFFs = np.unique(np.diff(self.RFErange[0]))
            if len(DIFFs) == 1: step = DIFFs[0] 
            # --- only one subset, only one overall run
            if step == 0:
                if self.Idle_ON: 
                    length = len(selection_out['RFE'])
                    # a- extracting the ranked_features to discriminate between MIs and idle states
                    selection_C1 = selection_out['RFE'][:length//2]
                    # b- extracting the ranked_features to discriminate between left and right movements
                    selection_C2 = selection_out['RFE'][length//2:]
                    # c- selecting the features via the user's insertion (i.e., RFErange[0] for MI versus idle)
                    indices = np.array(selection_C1[self.RFErange[0]], dtype = int).tolist()
                    indices.sort()
                    # d- insertion of the feature-indices for classifier MIvsIDLE
                    feature_indices.append(indices)
                    # e- selecting the features via the user's insertion (i.e., RFErange[1] for left vs right)
                    indices = np.array(selection_C2[self.RFErange[1]], dtype = int).tolist()
                    indices.sort()
                    # f- insertion of the feature-indices for classifier LEFTvsRIGHT
                    feature_indices.append(indices)
                else:
                    indices = np.array(selection_out['RFE'][self.RFErange[0]], dtype = int).tolist()
                    indices.sort()
                    # insertion of the feature-indices for classifier LEFTvsRIGHT
                    feature_indices.append(indices)
                FEATURE_IDX.append(feature_indices)
            # --- number of subsets = number of overall runs
            else:           
                if self.Idle_ON: 
                    # a- creation of the boundaries of each run for each classifier
                    self.RFErange[0].append(self.RFErange[0][-1]+step)
                    start_C1 = self.RFErange[0][0]
                    start_C2 = self.RFErange[1][0]
                    step_C2  = self.RFErange[1][1] - self.RFErange[1][0]
                    self.RFErange[1].append(self.RFErange[1][-1]+step_C2)    
                    # b- insertion of the feature-indices for each run for each classifier            
                    for index in range(len(self.RFErange[0][1:])):
                        end_C1 = self.RFErange[0][index+1]
                        end_C2 = self.RFErange[1][index+1]
                        length = len(Selection_Out['RFE'])
                        selection_C1 = Selection_Out['RFE'][:length//2]
                        selection_C2 = Selection_Out['RFE'][length//2:]
                        indices = np.array(selection_C1[start_C1:end_C1], dtype = int).tolist()
                        indices.sort()
                        # insertion of the feature-indices for classifier MIvsIDLE
                        feature_indices.append(indices)
                        indices = np.array(selection_C2[start_C2:end_C2], dtype = int).tolist()
                        indices.sort()
                        # insertion of the feature-indices for classifier LEFTvsRIGHT
                        feature_indices.append(indices)
                        FEATURE_IDX.append(feature_indices)
                        feature_indices = []
                else:                  
                    # a- creation of the boundaries of each run for only one classifier (LEFTvsRIGHT)
                    self.RFErange[0].append(self.RFErange[0][-1]+step)
                    start_C1 = self.RFErange[0][0]
                    # b- insertion of the feature-indices for each run for only one classifier (LEFTvsRIGHT)
                    for end_C1 in self.RFErange[0][1:]:
                        indices = np.array(Selection_Out['RFE'][start_C1:end_C1], dtype = int).tolist()
                        indices.sort()
                        feature_indices.append(indices)
                        FEATURE_IDX.append(feature_indices)   
                        feature_indices = []  
            # --- number of features to use for the classification       
            Range = self.RFErange[0]
        # (3) Data Organization: Use of the selected features by default
        #     *The user has selected some features for classification, but DBI/RFE have been left in turned off state
        # --- Arbitrary selection of features via DBI entry (it's only possible one run)
        elif self.DBIfeatures:
            # a- feature indexes
            feature_indices.append(self.DBIrange)
            if self.Idle_ON: feature_indices.append(self.DBIrange)
            FEATURE_IDX.append(feature_indices)
            # b- number of features to use for the classification       
            Range = self.DBIrange
        # --- Arbitrary selection of features via RFE entry (it's only possible one run)
        elif self.RFEfeatures:  
            # a- feature indexes  
            if self.Idle_ON: 
                feature_indices.append(self.RFErange[0])
                feature_indices.append(self.RFErange[1])
            else:
                feature_indices.append(self.RFErange[0])
            FEATURE_IDX.append(feature_indices)
            # b- number of features to use for the classification       
            Range = self.RFErange[0]
        # (4) Data Organization: Use of ALL the features for Classification (only one run)
        #     *The DBI and/or RFE are turned on, but the selected features are not required for classification
        #     *Either the DBI/RFE selection, or the DBI/RFE range have been selected
        else:
            # a- feature indexes
            feature_indices.append(range(numfea))
            if self.Idle_ON: feature_indices.append(range(numfea))
            FEATURE_IDX.append(feature_indices)
            # b- number of features to use for the classification
            Range = range(numfea)
        return FEATURE_IDX, Range, step


    # - METHOD 4: DataSet Construction for Classification Process -
    def Datasets(self, eeg_feaext, trialsTR, trialsTS):
        'Dataset Construction for Classification Process'         
        
        # (a) Variable Declaration          
        # --- total number of trials
        total_trs = 0
        for item in trialsTR: total_trs += len(item)
        # --- number of features
        dimY = np.size(eeg_feaext[0], axis = 1)
        # a.1 configuration for 3 brain-states
        if self.Idle_ON:
            if len(trialsTR[0]) == len(trialsTR[-1]):
                # --- indices to insert the current trials
                left_idxtr  = range(0, total_trs, 3)
                right_idxtr = range(1, total_trs, 3)
                idle_idxtr  = range(2, total_trs, 3)
                # --- label for the classes in training and testing stages
                classes_trainC1 = [1, 1, -1]
                classes_test = self.Class_Label
            else:
                # --- indices to insert the current trials
                left_idxtr  = range(0, total_trs, 4)
                right_idxtr = range(2, total_trs, 4)
                idle_idxtr  = range(1, total_trs, 2)
                # --- label for the classes in training and testing stages
                classes_trainC1 = [1, -1, 1, -1]
                classes_test = [self.Class_Label[0], self.Class_Label[-1], self.Class_Label[1], self.Class_Label[-1]] 
            # --- default feature-matrices
            features_trainC1 = np.zeros((total_trs, dimY))
            features_trainC2 = np.zeros((len(left_idxtr)+len(right_idxtr), dimY))
            features_testC1  = np.zeros((total_trs, dimY))   
            features_testC2  = np.zeros((len(left_idxtr)+len(right_idxtr), dimY))
            # --- label for the classes in training and testing stages
            classes_trainC2 = [1, -1]                         
        else:
        # a.2 configuration for 2 brain-states
            # --- indices to insert the current trials
            left_idxtr  = range(0, total_trs, 2)
            right_idxtr = range(1, total_trs, 2)
            # --- default feature-matrices
            features_trainC2 = np.zeros((total_trs, dimY))
            features_testC2  = np.zeros((total_trs, dimY))      
            # --- label for the classes in training and testing stages
            classes_trainC2 = [1, -1]
            classes_test = [self.Class_Label[0], self.Class_Label[1]]             
        # (b) === Left + Right + Idle ===            
        if self.Idle_ON:
            # (b.1) Training Dataset (trials x features)    
            # --- left~MI trials
            features_trainC1[left_idxtr, :] = eeg_feaext[ 0][trialsTR[ 0], :]
            # --- right~MI trials
            features_trainC1[right_idxtr,:] = eeg_feaext[ 1][trialsTR[ 1], :]
            # --- idle~MI trials
            features_trainC1[idle_idxtr, :] = eeg_feaext[-1][trialsTR[-1], :]
            # (b.2) Training Dataset (trials x features)   
            # --- left~MI trials
            features_trainC2[trialsTR[0], :]= eeg_feaext[0][trialsTR[0], :]
            # --- right~MI trials
            features_trainC2[trialsTS[0],:] = eeg_feaext[1][trialsTR[1], :]  
            # (b.3) Testing dataset (trials x features)    
            # --- left~MI trials          
            features_testC1[left_idxtr, :] = eeg_feaext[0 ][trialsTS[0], :]
            # --- right~MI trials
            features_testC1[right_idxtr,:] = eeg_feaext[1 ][trialsTS[1], :]
            # --- idle~MI trials
            features_testC1[idle_idxtr, :] = eeg_feaext[-1][trialsTS[-1],:] 
            # (b.4) Testing dataset (trials x features)    
            # --- left~MI trials          
            features_testC2[trialsTR[0],:] = eeg_feaext[0 ][trialsTS[0], :]
            # --- right~MI trials
            features_testC2[trialsTS[0],:] = eeg_feaext[1 ][trialsTS[1], :]            
        # (c) === Left + Right ===
        else:
            # (c.1) Training Dataset (trials x features)   
            # --- left~MI trials
            features_trainC2[left_idxtr, :] = eeg_feaext[0][trialsTR[0], :]
            # --- right~MI trials
            features_trainC2[right_idxtr,:] = eeg_feaext[1][trialsTR[1], :] 
            # (c.2) Testing dataset (trials x features)   
            # --- left~MI trials
            features_testC2[left_idxtr,  :] = eeg_feaext[0][trialsTS[0], :]
            # --- right~MI trials
            features_testC2[right_idxtr, :] = eeg_feaext[1][trialsTS[1], :]     
        # (d) Target labels for TRAINING dataset
        # --- targets for the Classifier 1 (MI versus idle)
        if self.Idle_ON: target_trainC1 = np.array(classes_trainC1 * len(trialsTR[0]))
        # --- targets for the Classifier 2 (left-MI versus right-MI)
        target_trainC2 = np.array(classes_trainC2 * len(trialsTR[0]))          
        # (e) Target labels for TESTING dataset
        Target_Test = np.array(classes_test * len(trialsTS[0]))
        # (f) Composing the datasets according to the necessary classifiers
        Training, Target_Train, Testing = [], [], []
        # --- two classifiers: C1 (MI versus idle) and C2 (left versus right)
        if self.Idle_ON:
            # training trials considering all the mental states
            Training.append(features_trainC1)
            # training trials considering only motor imagery trials
            Training.append(features_trainC2)
            # targets for training considering the discrimination between motor imagery and idle states
            Target_Train.append(target_trainC1)
            # targets for training considering the discrimination between left and right
            Target_Train.append(target_trainC2)
            # testing trials considering all the mental states
            Testing.append(features_testC1)
            # testing trials considering only MI trials
            Testing.append(features_testC2)            
        # --- only one classifier: C2 (left versus right)
        else:
            # training trials 
            Training.append(features_trainC2)
            # targets for training                
            Target_Train.append(target_trainC2)  
            # testing trials
            Testing.append(features_testC2)
        # (g) Assignment of Out-Variables
        self.Training     = Training
        self.Target_Train = Target_Train
        self.Testing      = Testing
        self.Target_Test  = Target_Test                         
    
    
    # ----------- METHOD 5: Classifier Creator -------------
    def Classifier_Creator(self, feature_indices):
        'Modelling & Testing of the Requested Classifier'
                                       
        # (a) Variable Declaration
        MODELS, GRID_SEARCH, ACCURACY, PREDICTIONS, TRAINING = [], [], [], [], []
        # ***** Classifier Modelling *****
        # (b) Selecting the features that are requested according to "Organization_Features"
        for index in range(len(self.Training)):            
            training = self.Training[index]
            TRAINING.append(training[:, feature_indices[index]])                    
        # (c) Parameter (C and/or kp) Search by 10-fold Cross-Validation
        #  A- Creating a model for each case: MIvsIDLE and/or LEFTvsRIGHT 
        #  B- Making only use of the training datasets
        #  C- Selection of the pre-selected classifier (FDA,linear-SVM,rbd_SVM)       
        # c.1 Fisher Discriminant Analysis (FDA)
        if self.Classifier == 'FDA':
            for index in range(len(TRAINING)):
                # --- model creating via cross-validation
                FisherDA, grid_search = self.TrainFDA_mlpy(TRAINING[index], self.Target_Train[index])   
                # --- storage of results                                                              
                MODELS.append(FisherDA)
                GRID_SEARCH.append(grid_search)
        # c.2 Linear Support Vector Machine (SVM)
        elif self.Classifier == 'Linear_SVM':
            for index in range(len(TRAINING)):
                # --- model creating via cross-validation
                SVM_linear, grid_search = self.Train_SVMlinear_LIBSVM(TRAINING[index], self.Target_Train[index])
                # --- storage of results                          
                MODELS.append(SVM_linear)
                GRID_SEARCH.append(grid_search)           
        # c.3 Radial Basis Function - Support Vector Machine
        elif self.Classifier == 'RBF_SVM':
            for index in range(len(TRAINING)):
                # --- model creating via cross-validation
                SVM_rbf, grid_search = self.Train_SVMrbf_LIBSVM(TRAINING[index], self.Target_Train[index])
                # --- storage of results         
                MODELS.append(SVM_rbf)
                GRID_SEARCH.append(grid_search)
        # ***** Classifier Assessment *****
        # ------------------------------------------------------------------
        # The assessment of the classifiers or classifier is done separately
        # ------------------------------------------------------------------
        # (d) Assessment of a Model only constructed via Classifier2 (LEFTvsRIGHT)
        for index in range(len(MODELS)):
            # d.1 Selecting the features that are requested according to "Organization_Features"
            scaled_testing = self.Testing[index][:, feature_indices[index]]
            # --- Classifier (MI vs idle or Left vs Rigth)
            Classifier  = MODELS[index]
            target_test = self.Target_Train[index]
            # d.2 Binary Classifier Testing
            # --- Fisher Discriminant Analysis (FDA)
            if self.Classifier == 'FDA':
                # Classifier Testing
                predictions = Classifier.predict(scaled_testing)
                # Accuracy calculation
                accuracy = mlpy.acc(target_test, predictions)       
            # --- Support Vector Machine (SVM)
            else:
                # Classifier Testing
                predictions,accuracy,dec_vals = libsvm.svm_predict(target_test.tolist(),scaled_testing.tolist(),Classifier);
            ACCURACY.append(accuracy)
            PREDICTIONS.append(predictions)       
        return MODELS, GRID_SEARCH, ACCURACY, PREDICTIONS


    # -- METHOD 6: Modelling of a FDA classifier via MLPY --
    def TrainFDA_mlpy(self, training, target_train):
        'FDA Modelling via mlpy-library'
        
        # (1) Finding the best Regularization Parameter
        prevACC, grid_search = 0, []
        for i in range(-1, 16):
            c = 2**i
            # --- initializing the FDA classifier
            FisherDA = mlpy.Fda(C = c)
            # --- sample indexes for computing cross-validation
            idx = mlpy.kfoldS(cl = target_train, sets = self.Nsets)
            pred_acc = 0.0
            for idxtr, idxts in idx:
                # build training data
                xtr, xts = training[idxtr], training[idxts]          
                # build test data   
                ytr, yts = target_train[idxtr], target_train[idxts]    
                # adapt the model 
                FisherDA.compute(xtr, ytr)                     
                # test the model on test data         
                pred = FisherDA.predict(xts)                           
                # compute the accuracy prediction
                pred_acc += mlpy.acc(yts, pred)                         
            # --- compute the average accuracy
            ACC = pred_acc/len(idx)                           
            # --- compare and/or save the parameter with the highest accuracy
            if ACC > prevACC:
                grid_search = []
                grid_search.append([c, ACC])
                prevACC = ACC
            elif ACC == prevACC:
                grid_search.append([c, ACC])                
        # (2) Model Implementation (use of the first best found parameters)
        c = grid_search[0][0]
        # --- initializing the FDA classifier
        FisherDA = mlpy.Fda(C = c)                
        # --- sample indexes for computing cross-validation
        idx = mlpy.kfoldS(cl = target_train, sets = self.Nsets)
        for idxtr, idxts in idx:
            xtr, xts = training[idxtr], training[idxts]             
            ytr, yts = target_train[idxtr], target_train[idxts]     
            FisherDA.compute(xtr, ytr)                              
            pred = FisherDA.predict(xts)    
        return FisherDA, grid_search
    
    
    # - METHOD 7: Modelling of a liner SVM classifier via MLPY -
    def Train_SVMlinear_mlpy(self, training, target_train):
        'Linear SVM Modelling via mlpy-library'
        
        # (1) Modelling the classifier (the best parameters are not searched
        #     because the library doesn't allow it)                    
        # --- initializing the FDA classifier
        SVM_linear = mlpy.Svm()
        # --- sample indexes for computing cross-validation
        idx = mlpy.kfoldS(cl = target_train, sets = self.Nsets)
        pred_acc = 0.0
        for idxtr, idxts in idx:
            # build training data
            xtr, xts = training[idxtr], training[idxts]             
            # build test data
            ytr, yts = target_train[idxtr], target_train[idxts]     
            # adapt the model
            SVM_linear.compute(xtr, ytr)                            
            # test the model on test data
            pred = SVM_linear.predict(xts)                          
            # compute the accuracy prediction
            pred_acc += mlpy.acc(yts, pred)                         
        # --- compute the average accuracy
        ACC = pred_acc/len(idx)                           
        grid_search = []
        grid_search.append([ACC])    
        return SVM_linear, grid_search
    
    
    # - METHOD 8: Modelling of a liner SVM classifier via LIBSVM -
    def Train_SVMlinear_LIBSVM(self, training, target_train):
        'Linear SVM Modelling via LIBSVM-library'
        
        # (1) LIBSVM format
        training, target_train = training.tolist(), target_train.tolist()
        # (2) Finding the best regularization C parameter
        problem = libsvm.svm_problem(target_train, training);
        prevACC = 0
        grid_search = []
        for j in range(-1, 16):
            # --- model creation via 10-fold cross-validation
            C = 2**j
            options = '-s 0 ' + '-t 0 ' + '-c ' + str(C) + ' -v 10'
            parameters = libsvm.svm_parameter(options);
            ACC = libsvm.svm_train(problem, parameters);
            # --- storage of the best parameter
            if ACC > prevACC:
                grid_search = []
                grid_search.append([C, ACC])
                prevACC = ACC
            elif ACC == prevACC:
                grid_search.append([C, ACC])
        # (3) Model Implementation (use of the first best found parameters)
        C = grid_search[0][1]
        options = '-s 0 ' + '-t 0 ' + '-c ' + str(C) 
        parameters = libsvm.svm_parameter(options);
        SVM_linear = libsvm.svm_train(problem, parameters); 
        return SVM_linear, grid_search
    
    
    # - METHOD 9: Modelling of a rbf SVM classifier via MLPY -
    def Train_SVMrbf_mlpy(self, training, target_train):
        'Radial Basis Function SVM Modelling via mlpy-library'
        
        # (1) Modelling the classifier (the best parameters are not searched
        #     because the library doesn't allow it)                    
        # --- initializing the SVM classifier
        SVM_rbf = mlpy.Svm(kernel = 'gaussian')
        # --- sample indexes for computing cross-validation
        idx = mlpy.kfoldS(cl = target_train, sets = self.Nsets)
        pred_acc = 0.0
        for idxtr, idxts in idx:
            # build training data
            xtr, xts = training[idxtr], training[idxts]             
            # build test data
            ytr, yts = target_train[idxtr], target_train[idxts]     
            # adapt the model
            SVM_rbf.compute(xtr, ytr)                               
            # test the model on test data
            pred = SVM_rbf.predict(xts)                             
            # compute the accuracy prediction
            pred_acc += mlpy.acc(yts, pred)                         
        # --- compute the average accuracy
        ACC = pred_acc/len(idx)                           
        grid_search = []
        grid_search.append([ACC])  
        return SVM_rbf, grid_search       
    
    
    # - METHOD 10: Modelling of a rbf SVM classifier via LIBSVM -
    def Train_SVMrbf_LIBSVM(self, training, target_train):
        'Radial Basis Function SVM Modelling via LIBSVM-library'    
        
        # (1) LIBSVM format
        training, target_train = training.tolist(), target_train.tolist()
        # (2) Finding the best regularization C parameter and gamma parameter
        problem = libsvm.svm_problem(target_train, training);
        prevACC = 0
        grid_search = []
        for i in range(-15, 5):
            gamma = 2**i
            for j in range(-1, 16):
                # --- model creation via 10-fold cross-validation
                C = 2**j
                options = '-s 0 ' + '-t 2 ' + '-g ' + str(gamma) + ' -c ' + str(C) + ' -v 10'
                parameters = libsvm.svm_parameter(options);
                ACC = libsvm.svm_train(problem, parameters);
                # --- storage of the best parameter
                if ACC > prevACC:
                    grid_search = []
                    grid_search.append([gamma, C, ACC])
                    prevACC = ACC
                elif ACC == prevACC:
                    grid_search.append([gamma, C, ACC])            
        # (3) Model Implementation (use of the first best found parameters)
        gamma = grid_search[0][0]
        C = grid_search[0][1]
        options = '-s 0 ' + '-t 2 ' + '-g '+ str(gamma) + ' -c ' + str(C) 
        parameters = libsvm.svm_parameter(options);
        SVM_rbf = libsvm.svm_train(problem, parameters);    
        return SVM_rbf, grid_search

    
    # ----- METHOD 11: Evaluation of a Tree Classifier -----
    def Tree_Evaluation(self, MODELS, feature_indices):
        'Evaluation of a Tree Classifier'   
        
        # =====  (a) Selecting the features that are requested according to "Organization_Features" =====
        predictions, NumTr = np.zeros(0), len(self.Target_Test)
        # ====== (b) Three Classes =====
        if self.Idle_ON:
            # b.1 datasets
            scaled_testing1 = self.Testing[0][:, feature_indices[0]]
            scaled_testing2 = self.Testing[0][:, feature_indices[-1]]
            # b.2 Classifier 1 (MI versus idle)
            Classifier1 = MODELS[0]
            # b.3 Classifier 2 (Left versus Rigth)
            Classifier2 = MODELS[-1]
            # b.4 Classifier Evaluation
            for tr in range(NumTr):
                # --- Fisher Discriminant Analysis (FDA)
                if self.Classifier == 'FDA':                    
                    pred = Classifier1.predict(scaled_testing1[tr, :])               
                    # idle detection
                    if pred == -1:
                        predictions = np.append(predictions, self.Class_Label[2])
                    # MI detection
                    else:
                        pred = Classifier2.predict(scaled_testing2[tr, :])
                        # Right detection
                        if pred == -1:
                            predictions = np.append(predictions, self.Class_Label[1])
                        # Left detection
                        else:
                            predictions = np.append(predictions, self.Class_Label[0])
                # --- Support Vector Machine (SVM)
                else:
                    pred, accuracy, dec_vals = libsvm.svm_predict([0], [scaled_testing1[tr, :].tolist()], Classifier1);
                    # idle detection
                    if int(pred[0]) == -1:
                        predictions = np.append(predictions, self.Class_Label[2])
                    # MI detection
                    else:
                        pred, accuracy, dec_vals = libsvm.svm_predict([0], [scaled_testing2[tr, :].tolist()], Classifier2);
                        # Right detection
                        if int(pred[0]) == -1:
                            predictions = np.append(predictions, self.Class_Label[1])
                        # Left detection
                        else:
                            predictions = np.append(predictions, self.Class_Label[0])
        # ====== (c) Two Classes =====
        else:
            # c.1 datasets
            scaled_testing1 = self.Testing[0][:, feature_indices[0]]
            # c.2 Classifier (Left versus Rigth)
            Classifier1 = MODELS[0]
            # c.3 Classifier Evaluation
            for tr in range(NumTr):
                # --- Fisher Discriminant Analysis (FDA)
                if self.Classifier == 'FDA':                    
                    pred = Classifier1.predict(scaled_testing1[tr, :])               
                    # right detection
                    if pred == -1:
                        predictions = np.append(predictions, self.Class_Label[1])
                    # left detection
                    else:
                        predictions = np.append(predictions, self.Class_Label[0])
                # --- Support Vector Machine (SVM)
                else:
                    pred, accuracy, dec_vals = libsvm.svm_predict([0], [scaled_testing1[tr, :].tolist()], Classifier1);
                    # right detection
                    if int(pred[0]) == -1:
                        predictions = np.append(predictions, self.Class_Label[1])
                    # left detection
                    else:
                        predictions = np.append(predictions, self.Class_Label[0])
        # ===== (d) Classification Accuracy =====               
        hits = (self.Target_Test - predictions).tolist()
        accuracy = (hits.count(0) * 100)/len(self.Target_Test)       
        return accuracy


    # ---------- METHOD 12: Spectrogram Plotting -----------
    def Spectrogram(self, eeg_dsp, channels, new_trials, new_samples):
        'OffLine Spectrogram'
        
        # (a) Variable Declaration
        plot = 1
        # --- figure 1 configuration    
        FIG1 = plt.figure(num = 1, figsize = (15,10), facecolor = '#A0AEC1', edgecolor = 'white')  
        # (b) Plot Creation
        for i in range(len(channels)):
            TITLE = layout_labels[self.labels_ch[i]]
            for j in self.mental_states: 
                SUBTITLE = MIMov[int(self.Class_Label[j]-1)]
                # --- trials reading
                trials_idxs = new_trials[j]
                # --- samples reading
                samples_idxs = new_samples[j]
                # --- signal extraction                                   
                signal = eeg_dsp[self.mental_states[j]][channels[i]]                    
                signal = np.take(signal, trials_idxs, axis = 0)
                signal = np.take(signal, samples_idxs, axis = 1)                    
                signal = np.average(signal, axis = 0)
                # --- required parameter calculation
                N = len(signal)
                total_time = N/self.Fdown
                segment = (self.win_len * N)//total_time
                overlap = segment * (self.overlapping/100)
                WindoW = WinLibrary(self.window, segment)
                ax = FIG1.add_subplot(len(channels), len(self.mental_states), plot)
                ax.specgram(signal, NFFT = int(segment), Fs = self.Fdown, window = WindoW, noverlap = overlap)
                ax.tick_params(labelsize = 9) 
                ax.set_xlabel('T i m e [s]', fontsize = 9, fontname = 'Byington')
                ax.set_ylabel('F r e q u e n c y [Hz]', fontsize = 9, fontname = 'Byington')
                ax.set_title(TITLE + ' ~ ' + SUBTITLE, color = 'black', fontsize = 11, fontname = 'Byington')
                plot += 1
        # (c) Adjustment of Subplot Dimensions
        FIG1.subplots_adjust(left = 0.075, right = 0.95, bottom = 0.05, top = 0.925, hspace = 0.3)
        # (d) Save Figure 1
        url = root + 'spectro.png'
        plt.savefig(url, facecolor = '#A0AEC1', edgecolor = 'white')
        return FIG1


    # -------------- METHOD 13: PSD Plotting ---------------
    def PSD(self, eeg_dsp, channels, new_trials, new_samples):
        'OffLine Power Spectral Density'

        # (a) Variable Declaration
        # --- initialization
        Legends, AXS, titles, plotb, plotc = [], [], [], 1, 1
        # --- overlap option for PSD
        if any([self.overlap_bs == 'psd', self.overlap_bs == 'both']): 
            overlap_psd = True
        else:
            overlap_psd = False
        # --- figure 2 configuration           
        FIG2 = plt.figure(num = 2, figsize = (15,10), facecolor = '#A0AEC1', edgecolor = 'white')
        # (b) Plot Process: Initialization
        for i in range(len(channels)):
            TITLE, plota = layout_labels[self.labels_ch[i]], 1   
            maximo, minimo = [], []             
            for j in self.mental_states: 
                SUBTITLE = MIMov[int(self.Class_Label[j]-1)]                    
                # --- trials reading
                trials_idxs = new_trials[j]
                # --- samples reading
                samples_idxs = new_samples[j]
                # --- signal extraction                                   
                signal = eeg_dsp[self.mental_states[j]][channels[i]]                    
                signal = np.take(signal, trials_idxs, axis = 0)
                signal = np.take(signal, samples_idxs, axis = 1)                     
                signal = np.average(signal, axis = 0)
                # --- max and min of signal
                maximo.append(np.max(signal))
                minimo.append(np.min(signal)) 
                # --- required parameter calculation
                N = len(signal)
                total_time = N/self.Fdown
                segment = int((self.win_len*N)/total_time)
                overlap = segment*(self.overlapping/100)
                WindoW = WinLibrary(self.window, segment)
                # (c) plotting and configuring each subplot
                if all([not(overlap_psd), (self.overlap_ch)]):
                    # --- overlap of channels
                    if plota == 1:
                        if plota == plotc:
                            ax = FIG2.add_subplot(len(self.mental_states), 1, plota)
                            ax.tick_params(labelsize = 9) 
                            ax.set_title(SUBTITLE, color = 'black', fontsize = 11, fontname = 'Byington')
                            ax.set_xlabel('T i m e [s]', fontsize = 9, fontname = 'Byington')
                            ax.set_ylabel('PowerSpectralDensity[db/Hz]', fontsize = 9, fontname = 'Byington')                                
                            AXS.append(ax)
                        AXS[0].psd(signal, NFFT = segment, Fs = self.Fdown, window = WindoW, noverlap = overlap, linewidth = 1.5, label = TITLE)
                        Legends.append(AXS[0].legend(fancybox = True, shadow = True))
                    elif plota == 2:
                        if plota == plotc:
                            ax = FIG2.add_subplot(len(self.mental_states), 1, plota)  
                            ax.tick_params(labelsize = 9)                               
                            ax.set_title(SUBTITLE, color = 'black', fontsize = 11, fontname = 'Byington')
                            ax.set_xlabel('T i m e [s]', fontsize = 9, fontname = 'Byington')
                            ax.set_ylabel('PowerSpectralDensity[db/Hz]', fontsize = 9, fontname = 'Byington')                                
                            AXS.append(ax)
                        AXS[1].psd(signal, NFFT = segment, Fs = self.Fdown, window = WindoW, noverlap = overlap, linewidth = 1.5, label = TITLE)
                        Legends.append(AXS[1].legend(fancybox = True, shadow = True))                        
                    elif plota == 3:
                        if plota == plotc:
                            ax = FIG2.add_subplot(len(self.mental_states), 1, plota)
                            ax.tick_params(labelsize = 9) 
                            ax.set_title(SUBTITLE, color = 'black', fontsize = 11, fontname = 'Byington')
                            ax.set_xlabel('T i m e [s]', fontsize = 9, fontname = 'Byington')
                            ax.set_ylabel('PowerSpectralDensity[db/Hz]', fontsize = 9, fontname='Byington')                                
                            AXS.append(ax)
                        AXS[2].psd(signal, NFFT = segment, Fs = self.Fdown, window = WindoW, noverlap = overlap, linewidth = 1.5, label = TITLE)
                        Legends.append(AXS[2].legend(fancybox = True, shadow = True))
                elif all([(overlap_psd), not(self.overlap_ch)]):
                    # --- overlap of mental states
                    if j == 0:
                        ax = FIG2.add_subplot(len(channels), 1, plotb)
                        ax.tick_params(labelsize = 9) 
                        ax.set_title(TITLE, color = 'black', fontsize = 11, fontname = 'Byington')
                        ax.set_xlabel('T i m e [s]', fontsize = 9, fontname = 'Byington')
                        ax.set_ylabel('PowerSpectralDensity[db/Hz]', fontsize = 9, fontname = 'Byington')                                
                        AXS.append(ax)
                    AXS[-1].psd(signal, NFFT = segment, Fs = self.Fdown, window = WindoW, noverlap = overlap, linewidth = 1.5, label = SUBTITLE)
                    Legends.append(AXS[-1].legend(fancybox = True, shadow = True))
                else:
                    # --- none
                    ax = FIG2.add_subplot(len(channels), len(self.mental_states), plotc)
                    ax.tick_params(labelsize = 9) 
                    ax.psd(signal, NFFT = segment, Fs = self.Fdown, window = WindoW, noverlap = overlap, linewidth = 1.5)
                    ax.set_xlabel('F r e q u e n c y [Hz]', fontsize = 9, fontname='Byington')
                    ax.set_ylabel('PowerSpectralDensity[db/Hz]', fontsize = 9, fontname='Byington')
                    ax.set_title(TITLE + ' ~ ' + SUBTITLE, color = 'black', fontsize = 11, fontname='Byington')
                    AXS.append(ax)
                plota += 1
                plotc += 1                    
            plotb += 1
        # (d) legend configuration
        if Legends != []:            
            for leg in Legends:
                frame = leg.get_frame()
                frame.set_facecolor('#E7E7E7')
                for t in leg.get_texts(): t.set_fontsize(9)
                for l in leg.get_lines(): l.set_linewidth(3.0)            
        # (e) adjustment of Subplot Dimensions
        FIG2.subplots_adjust(left = 0.075, right = 0.95, bottom = 0.05, top = 0.925, hspace = 0.3)           
        # (f) Save Figure 2
        url = root + 'psd.png'
        plt.savefig(url, facecolor = '#A0AEC1', edgecolor = 'white')
        return FIG2
    
    
    # ------------ METHOD 14: BoxPlot Plotting -------------
    def BoxPlot(self, eeg_feaext, feaext_labels):
        'OffLine BoxPlot'
        
        # (a) Variable Declaration
        maximo, minimo, AXS, plot = [], [], [], 1    
        # --- Figure 3 configuration
        FIG3 = plt.figure(num = 3, figsize = (15,10), facecolor = '#A0AEC1', edgecolor = 'white')
        # (b) Plotting Process            
        for i in range(len(eeg_feaext)): 
            TITLE = feaext_labels[i]
            # --- max and min of the signal
            maximo.append(np.max(np.max(eeg_feaext[i], axis = 0)))
            minimo.append(np.min(np.min(eeg_feaext[i], axis = 0)))                    
            # --- plotting the a boxplot
            ax = FIG3.add_subplot(len(eeg_feaext), 1, plot)
            ax.tick_params(labelsize = 9)             
            ax.boxplot(eeg_feaext[i])
            # --- plot configuration                              
            ax.set_xlabel('Number of Feature', fontsize = 9, fontname='Byington')           
            ax.set_ylabel('Feature Magnitude' , fontsize = 9, fontname='Byington')
            ax.set_title(TITLE, color = 'black', fontsize = 11, fontname='Byington')
            ax.grid(True)
            AXS.append(ax)
            plot += 1
        # (c) Scaling the Axis
        for ax in AXS: ax.set_ylim(min(minimo), max(maximo))  
        # (d) Subplot Adjustment
        FIG3.subplots_adjust(left = 0.075, right = 0.95, bottom = 0.05, top = 0.925, hspace = 0.3) 
        # (e) Save Figure 3
        url = root + 'bxplot.png'
        plt.savefig(url, facecolor = '#A0AEC1', edgecolor = 'white')  
        return FIG3
    
    
    # ----------- METHOD 15: Histogram Plotting ------------
    def Histogram(self, eeg_feaext, feaext_labels):
        'OffLine Histogram'
        
        # (a) Variable Creation
        AXS, plot, titles = [], 1, ''
        # --- Figure 4 configuration
        FIG4 = plt.figure(num = 4, figsize = (15,10), facecolor = '#A0AEC1', edgecolor = 'white')
        # ***** Plot Creation *****
        for i in range(len(eeg_feaext)): 
            TITLE = feaext_labels[i]     
            # (b) Overlapping Case
            if any([self.overlap_bs == 'histo', self.overlap_bs == 'both']):
                if i == 0:
                # --- axis creation and configuration
                    ax = FIG4.add_subplot(111)
                    ax.tick_params(labelsize = 9) 
                    ax.set_xlabel('Feature Magnitude', fontsize = 9, fontname = 'Byington')
                    ax.set_ylabel('Frequency of Occurrence', fontsize = 9, fontname = 'Byington')
                    ax.set_title('Feature Distribution', color = 'black', fontsize = 11, fontname = 'Byington')
                    ax.grid(True)
                    AXS.append(ax)
                # --- histogram creation
                ax.hist(eeg_feaext[i], fc = colours_lines[i], ec = colours_lines[i], linewidth = 3, label = TITLE, alpha = 0.5)
                ax.legend(fancybox = True, shadow = True)
                # --- legend configuration
                Legend = ax.get_legend()
                Ltext  = Legend.get_texts()
                Lframe = Legend.get_frame()
                Lframe.set_facecolor('#E7E7E7')
                plt.setp(Ltext, fontsize = 9)          
            # (c) No Overlapping Case
            else:
                # --- histogram creation
                ax = FIG4.add_subplot(len(eeg_feaext), 1, plot)
                ax.tick_params(labelsize = 9)     
                # --- axis configuration
                ax.set_xlabel('Feature Magnitude', fontsize = 9, fontname = 'Byington')
                ax.set_ylabel('Frequency of Occurrence', fontsize = 9, fontname = 'Byington')
                ax.set_title(TITLE, color = 'black', fontsize = 11, fontname = 'Byington')               
                ax.hist(eeg_feaext[i], fc = colours_lines[i], ec = colours_lines[i], linewidth = 3, label = TITLE, alpha = 0.5)
                ax.grid(True)
                AXS.append(ax)
                plot += 1        
        # (d) Subplot Adjustement (non overlapping)
        FIG4.subplots_adjust(left = 0.075, right = 0.95, bottom = 0.05, top = 0.925, hspace = 0.3)
        # (e) Save Figure 4
        url = root + 'histo.png'
        plt.savefig(url, facecolor = '#A0AEC1', edgecolor = 'white')  
        return FIG4 


    # ------------ METHOD 16: ERD/ERS Plotting -------------
    def ERDS2d(self, channels, Power_ERDS, Reference, current_bands, greek_bd):
        'OffLine Event-Related (De-)Synchronization Maps: 2D'
        
        # (a) Variable Declaration
        plot = 0
        # --- samples to smooth data
        seg_smooth = int(self.Fdown * self.win_len)
        # --- plot creation
        FIG5 = plt.figure(num = 5, figsize = (15,10), facecolor = '#A0AEC1', edgecolor = 'white')
        # (b) Percentage values calculation and plotting            
        for i in range(len(channels)):    
            AXS, maximo, minimo, lines = [], [], [], []             
            TITLE = layout_labels[self.labels_ch[i]]                          
            for j in self.mental_states:                  
                # --- subplot configuration
                SUBTITLE = MIMov[int(self.Class_Label[j]-1)] 
                plot += 1                  
                ax = FIG5.add_subplot(len(channels), len(self.mental_states), plot)
                ax.tick_params(labelsize = 9)                  
                # --- ERDS map for each band   
                lines, legend_labels = [], []               
                for k in range(len(current_bands)):
                    tempo = []
                    # 1- signal extraction                     
                    signal = (((Power_ERDS[j][i, k, :])-Reference[j][i, k])/Reference[j][i, k])*100
                    Yaxis = np.zeros(0)
                    for s in range(0,len(signal),seg_smooth): Yaxis = np.append(Yaxis, np.average(signal[s:(s+seg_smooth)]))
                    # 2- smoothing Yaxis
                    len_time = len(Power_ERDS[j][i, k, :])/self.Fdown
                    # 3- X axis calculation (i.e., time)
                    Xaxis = np.arange(0,len_time, self.win_len) 
                    # 4- saving min and max values of Y-axis                                                 
                    maximo.append(np.max(Yaxis))
                    minimo.append(np.min(Yaxis))                        
                    # 5- plot and legend line creation                       
                    tempo.append(ax.plot(Xaxis, Yaxis, colours_marker[k], linewidth = 1.5))
                    lines.append(tempo[0][0])
                    legend_labels.append(greek_bd[k].lower())                        
                # --- axis configuration
                ax.set_xlabel('TIME', fontsize = 9, fontname = 'Byington', rotation = 'horizontal')  
                ax.set_xlim(0, len_time) 
                ax.axhline(y = 0, xmin = 0, xmax = len_time, color = 'black', linewidth = 0.5)                                     
                ax.set_ylabel('RELATIVE POWER [%]',fontsize = 9,fontname='Byington', rotation = 'vertical')
                ax.set_title(TITLE + ' ~ ' + SUBTITLE, color = 'black', fontsize = 11, fontname = 'Byington')
                ax.grid(True) 
                AXS.append(ax)
        # (c) Generic Figure Legend            
        legend = plt.figlegend(lines,legend_labels,loc = 'lower center',shadow=True,ncol=len(legend_labels),fancybox=True,borderpad=0.1)            
        for t in legend.get_texts(): t.set_fontsize(14)
        for t in legend.get_texts(): t.set_fontname('Byington')
        for l in legend.get_lines(): l.set_linewidth(1.5)               
        FIG5.subplots_adjust(left = 0.075, right = 0.95, bottom = 0.1, top = 0.925, hspace = 0.3)
        # (d) Save figure 5
        url = root + 'erds2D.png'
        plt.savefig(url, facecolor = '#A0AEC1', edgecolor = 'white') 
        return FIG5


    # ------------ METHOD 17: ERD/ERS Plotting -------------
    def ERDS3d(self, channels, Power_ERDS, Reference, current_bands):
        'OffLine Event-Related (De-)Synchronization Maps: 3D'
        
        # (a) Variable Declaration
        plot = 0
        # --- samples to smooth data
        seg_smooth = int(self.Fdown * self.win_len)
        # --- plot pre-configuration
        FIG6 = plt.figure(num = 6, figsize = (15,10), facecolor = '#A0AEC1', edgecolor = 'white')        
        # (b) Percentage Values Calculation and Plotting            
        for i in range(len(channels)):    
            AXS, Maximo = [], []             
            TITLE = layout_labels[self.labels_ch[i]]                          
            for j in self.mental_states:    
                XY, FaceColours, maximo, minimo = [], [], [], []                                
                # --- subplot configuration
                SUBTITLE = MIMov[int(self.Class_Label[j]-1)] 
                plot += 1                  
                ax = FIG6.add_subplot(len(channels), len(self.mental_states), plot, projection='3d')
                ax.tick_params(labelsize = 9)                     
                # --- ERDS map for each band                  
                for k in range(len(current_bands)):
                    # 1- Y axis calculation                        
                    signal = (((Power_ERDS[j][i, k, :])-Reference[j][i, k])/Reference[j][i, k])*100
                    Yaxis = np.zeros(0)
                    for s in range(0,len(signal),seg_smooth): Yaxis = np.append(Yaxis, np.average(signal[s:(s+seg_smooth)]))
                    Yaxis[0], Yaxis[-1] = 0, 0
                    # 2- smoothing Yaxis
                    len_time = len(Power_ERDS[j][i, k, :])/self.Fdown
                    # 3- X axis calculation (i.e., time)
                    Xaxis = np.arange(0,len_time, self.win_len)
                    # 4- zipping X and Y values
                    XY.append(zip(Xaxis, Yaxis))
                    # 5- saving min and max values of Y-axis                                                 
                    maximo.append(np.max(Yaxis))
                    minimo.append(np.min(Yaxis))                                                 
                    # 6- face color for each current band
                    FaceColours.append(ColourConverter(colours_lines[k]))
                # (c) 3D-Graph Process
                poly = PolyCollection(XY, facecolors = FaceColours) 
                poly.set_alpha(0.7)
                ax.add_collection3d(poly, zs = range(1, len(current_bands)+1), zdir = 'y')  
                # (d) Axis Configuration
                ax.set_xlabel('TIME', fontsize = 9, fontname = 'Byington', rotation = 'horizontal', ha = 'right')  
                ax.set_xlim3d(0, len_time) 
                ax.set_ylabel('BAND', fontsize = 9, fontname = 'Byington', rotation = 'horizontal', ha = 'left')  
                ax.set_ylim3d(0, len(current_bands)+1)                    
                ax.set_zlabel('RELATIVE POWER [%]', fontsize = 9, fontname='Byington', rotation = 'vertical', ha = 'left')
                ax.set_zlim3d(min(minimo), max(maximo)) 
                ax.set_title(TITLE + ' ~ ' + SUBTITLE, color = 'black', fontsize = 11, fontname='Byington')
                ax.set_axis_bgcolor('#A0AEC1')                    
                ax.grid(True)
                AXS.append(ax)
                Maximo.append(max(maximo))     
            # (e) Line Configuration and Labelling Process                       
            for ax in AXS:  
                maxy = Maximo.pop(0)
                for index in range(len(current_bands)): 
                    if current_bands[index] == 'Theta':
                        ax.text(0, index+1, maxy, r'$\theta$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'LowerTheta':
                        ax.text(0, index+1, maxy, r'$\theta_L$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'UpperTheta':
                        ax.text(0, index+1, maxy, r'$\theta_U$', color=colours_lines[index],fontsize=16,fontweight='bold')             
                    elif current_bands[index] == 'Alpha':
                        ax.text(0, index+1, maxy, r'$\alpha$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'LowerAlpha':
                        ax.text(0, index+1, maxy, r'$\alpha_L$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'UpperAlpha':
                        ax.text(0, index+1, maxy, r'$\alpha_U$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'Beta':
                        ax.text(0, index+1, maxy, r'$\beta$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'LowerBeta':
                        ax.text(0, index+1, maxy, r'$\beta_L$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'UpperBeta':
                        ax.text(0, index+1, maxy, r'$\beta_U$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'Gamma':
                        ax.text(0, index+1, maxy, r'$\gamma$', color=colours_lines[index],fontsize=16,fontweight='bold')
                    elif current_bands[index] == 'Whole':
                        ax.text(0, index+1, maxy, 'Whole', color=colours_lines[index],fontsize=14,fontname='Byington')
        # (f) Figure 6 Last Adjustments
        FIG6.subplots_adjust(left = 0.075, right = 0.95, bottom = 0.05, top = 0.925, hspace = 0.3)
        # (g) Save Figure 6
        url = root + 'erds3D.png'
        plt.savefig(url, facecolor = '#A0AEC1', edgecolor = 'white')
        return FIG6

