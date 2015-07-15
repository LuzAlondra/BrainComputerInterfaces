# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:42:17 2015

@author: L03030440 - Luz María Alonso Valerdi

@title:  NEUROPHYSIOLOGICAL CHARACTERIZER & PREDICTOR

@description: 
- NC: A power density spectrum is calculated by using a Fast Fourier Transform 
      applied to 4-sec epochs of the 3-min recordings of each condition. 
      This yielded 44 epochs (epoch 45 was not used for computational reasons) 
      and a 0.25 Hz resolution in the power spectra. Because the occipital-parietal 
      alpha rhythm can best be detected at occipital leads (depressed by opening 
      of the eyes), O1 and O2 were chosen to calculate the power density spectra 
      and the individual alpha peak frequencies (IAF). The peak frequency in the 
      EC condition is determined as the highest peak in a window of 7 to 14 Hz 
      in the EC power spectrum.
- NP: To construct this SMR predictor, only a short two minute recording of 
      EEG under the condition ‘relax with eyes open’ using two Laplacian channels 
      (C3 and C4, calculated from nine original monopolar channels) is required. 
      From these data it is calculated the power spectral density (PSD) in the 
      Laplace-filtered channels C3, C4 and determined for each of those channels 
      the maximum difference between the PSD curve and a fit of the 1/f noise 
      spectrum. These two values were estimates of the strength of the SMR over 
      the hand areas. The SMR predictor was calculated as the average of those 
      two values.
"""
# -----------------------------------------------------------------------------
#                               PYTHON LIBRARIES
# -----------------------------------------------------------------------------
from __future__ import division
from DSP_Functions import spectral_filter
from lmfit.models import GaussianModel, ConstantModel, PowerLawModel
import datetime
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import io, signal

# -----------------------------------------------------------------------------
#                            FUNCTION DECLARATION
# -----------------------------------------------------------------------------
# F1. Final Results 
def InitialReport():

    print ' ___________________________________________________________________________'
    print '|                                                                           |'
    print '|Tecnológico de Monterrey, Campus Ciudad de México                          |'
    print '|Instituto de Neurociencias, Universidad de Guadalajara                     |'
    print '|PROJECT (Part I):                                                          |'
    print '|"Study of the Brain Oscillations modulated by Endogenous Control Tasks:    |'
    print '| Activities of Daily Living (ADLs)"                                        |'
    print '|AUTHOR:                                                                    |'
    print '|Luz Maria Alonso Valerdi                                                   |'
    print ' ___________________________________________________________________________'
    print '\n\n\n'
    print datetime.datetime.today()
    print '\n\n\n'
    print '.............................................................................'
    print '...................... NEUROPHYSIOLOGICAL PREDICTOR .........................'
    print '..................... AND INDIVIUDAL ALPHA FREQUENCY ........................'
    print '.............................................................................'
    print '\n\n\n'


# -----------------------------------------------------------------------------
#                             CLASS DECLARATION
# -----------------------------------------------------------------------------
class NeuroIndexes():
    'Class to obtain IAF and Neurophysiological Predictor based on PSD and C3/C4'

    #.............Method 1: Initialization Process.........
    def __init__(self):        
        'Reading mat-files'
        
        # ----- insertion of the required information -----        
        print 'Insert the complete filename-paths for the following brain states\n'        
        EO_t = raw_input('1) eyes open:  ')
        EC_t = raw_input('2) eyes closed:  ')
        print '\nInsert the sampling frecuency\n'  
        Fs = raw_input('3) sampling frecuency:  ')
        # ----- general filepath and sampling frecuency -----
        i = EO_t.rfind('\\')
        self.url = EO_t.replace(EO_t[i:], '\\')  
        self.Fs  = int(Fs)
        # ----- data reader -----
        if EO_t[-3:] == 'mat':
            m1 = sp.io.loadmat(EO_t)
            eo = m1['eo']
            m2 = sp.io.loadmat(EC_t)
            ec = m2['ec']
        else: 
            eo = np.loadtxt(EO_t)
            ec = np.loadtxt(EC_t)
        # ----- neuroindexes calculation -----
        iaf = self.AlphaPeak(eo, ec)  
        self.NeuroPredictor(eo, iaf)
        print '\nDone! PSD-plots have been saved'
             
       
    #.........Method 2: Individual Alpha Frequency.........
    def AlphaPeak(self, eo, ec):
        'Method to calculate the individual alpha frequency'
        
        # ----- Variable Declaration -----
        fL, fH, fs = 7, 14, 128
        down = int(self.Fs/fs)
        B, A = spectral_filter(fs, fL, fH, 7, 'bandpass')
        EOn = np.zeros((2, 3*60*fs))
        ECn = np.zeros((2, 3*60*fs))
        # ----- Digital Signal Processing -----
        o1, o2 = 8, 9
        # PSD for eyes-open: O1 and O2    
        EOn[0,:], EOn[1,:] = sp.signal.decimate(eo[o1,:], down), sp.signal.decimate(eo[o2,:], down)
        EOn[0,:], EOn[1,:] = sp.signal.filtfilt(B, A, EOn[0,:]), sp.signal.filtfilt(B, A, EOn[1,:])
        frec, Pxx = sp.signal.welch(EOn[0,:], fs, nfft = fs*4)
        frec_eo, Pxx_eo = np.zeros((2, len(frec))), np.zeros((2, len(Pxx)))
        frec_eo[0, :], Pxx_eo[0, :] = frec, Pxx        
        frec, Pxx = sp.signal.welch(EOn[1,:], fs, nfft = fs*4)
        frec_eo[1, :], Pxx_eo[1, :] = frec, Pxx
        # PSD for eyes-closed: O1 and O2       
        ECn[0,:], ECn[1,:] = sp.signal.decimate(ec[o1,:], down), sp.signal.decimate(ec[o2,:], down)
        ECn[0,:], ECn[1,:] = sp.signal.filtfilt(B, A, ECn[0,:]), sp.signal.filtfilt(B, A, ECn[1,:])        
        frec, Pxx = sp.signal.welch(ECn[0,:], fs, nfft = fs*4)
        frec_ec, Pxx_ec = np.zeros((2, len(frec))), np.zeros((2, len(Pxx)))
        frec_ec[0, :], Pxx_ec[0, :] = frec, Pxx        
        frec, Pxx = sp.signal.welch(ECn[1,:], fs, nfft = fs*4)
        frec_ec[1, :], Pxx_ec[1, :] = frec, Pxx
        # ----- Power Spectral Density: PLOT -----
        fig = plt.figure(num = 1, figsize = (20,15), facecolor = '#A0AEC1', edgecolor = 'white')
        fig.subplots_adjust(left = 0.05, right = 0.99, bottom = 0.075, top = 0.925, hspace = 0.3, wspace=0.1)
        # (a) eyes-closed (ec) condition
        ax_a, ax_b = fig.add_subplot(3, 2, 1), fig.add_subplot(3, 2, 2)
        ax_a.set_ylabel('PSD [mV**2/Hz]', fontsize = 'x-large')
        ax_a.set_title('O1: Eyes-closed', fontsize = 'x-large')
        ax_b.set_title('O2: Eyes-closed', fontsize = 'x-large')               
        frecs = self.PSDaxis(frec_ec, Pxx_ec, ax_a, ax_b, 'g.-')
        # (b) eyes-open (eo) condition
        ax_c, ax_d = fig.add_subplot(3, 2, 3), fig.add_subplot(3, 2, 4)
        ax_c.set_ylabel('PSD [mV**2/Hz]', fontsize = 'x-large')
        ax_c.set_title('O1: Eyes-open', fontsize = 'x-large')
        ax_d.set_title('O2: Eyes-open', fontsize = 'x-large')               
        frecs = self.PSDaxis(frec_eo, Pxx_eo, ax_c, ax_d, 'b.-')
        # (c) ec - eo condition
        ax_e, ax_f = fig.add_subplot(3, 2, 5), fig.add_subplot(3, 2, 6)
        ax_e.set_xlabel('Frequency [Hz]', fontsize = 'x-large')
        ax_e.set_ylabel('PSD [mV**2/Hz]', fontsize = 'x-large')
        ax_e.set_title('O1: EC-EO', fontsize = 'x-large')
        ax_f.set_xlabel('Frequency [Hz]', fontsize = 'x-large')
        ax_f.set_title('O2: EC-EO', fontsize = 'x-large')               
        frecs = self.PSDaxis(frec_eo, Pxx_ec-Pxx_eo, ax_e, ax_f, 'r.-')     
        iaf = np.around(np.mean(frecs), decimals=2)
        fig.suptitle('IAF = '+str(iaf)+' Hz', fontsize = 'xx-large', color = 'r', va = 'top')
        plt.savefig(self.url+'IAF.png', edgecolor = 'white')
        plt.close(fig)
        
        return iaf
             
       
    #.........Method 3: Axes for plotting PSD - IAF........
    def PSDaxis(self, frec, Pxx, ax1, ax2, style):
        'Method to plot PSD for each Occipital Channel'
        
        ## -- axis 1 configuration: O1
        ax1.plot(frec[0,:], Pxx[0,:], style, linewidth = 2, markersize = 10)
        ax1.set_xlim(xmax = 15)
        ax1.tick_params(axis = 'both', labelsize = 14)
        ax1.grid()
        peak1 = np.amax(np.abs(Pxx[0,:]))
        idx = np.where(np.abs(Pxx[0,:]) == peak1)[0]
        frec1 = np.around(frec[0,idx], decimals=2)[0]
        ax1.text(frec[0,idx], Pxx[0,idx], str(frec1)+ ' Hz ', color = style[0], fontsize = 'large', ha = 'right')        
        ## -- axis 2 configuration: O2
        ax2.plot(frec[1,:], Pxx[1,:], style, linewidth = 2, markersize = 10)
        ax2.set_xlim(xmax = 15)
        ax2.tick_params(axis = 'both', labelsize = 14)
        ax2.grid()
        peak2 = np.amax(np.abs(Pxx[1,:]))
        idx = np.where(np.abs(Pxx[1,:]) == peak2)[0]
        frec2 = np.around(frec[1,idx], decimals=2)[0]
        ax2.text(frec[1,idx], Pxx[1,idx], str(frec2)+' Hz ', color = style[0], fontsize = 'large', ha = 'right')
        
        return (frec1, frec2)       


    #...........Method 4: Neurological Predictor...........
    def NeuroPredictor(self, eo, iaf):
        'Method to determine a Neurophysiological Predictor based on a SMR-method\
         proposed by Blanketz et al.(2010)'
        
        # ----- Variable Declaration -----
        fL, fH, length = 2, 32, 2*60*self.Fs
        B, A = spectral_filter(self.Fs, fL, fH, 5, 'bandpass')
        # ----- Digital Signal Processing -----
        # PSD for channel C3
        c3 = eo[4,:length] - np.mean(eo[(2,6,12,17),:length], axis=0)
        c3 = sp.signal.filtfilt(B, A, c3)
        frec, Pxx = sp.signal.welch(c3, self.Fs, nfft=4*self.Fs)
        i = np.where(np.amax(Pxx) == Pxx)
        Pxx_c3 = Pxx[i[0]:]
        frec_c3= frec[i[0]:]
        # PSD for channel C4
        c4 = eo[5, :length] - np.mean(eo[(3,7,13,17), :length], axis=0)
        c4 = sp.signal.filtfilt(B, A, c4)
        frec, Pxx = sp.signal.welch(c4, self.Fs, nfft=4*self.Fs)
        i = np.where(np.amax(Pxx) == Pxx)
        Pxx_c4 = Pxx[i[0]:]
        frec_c4= frec[i[0]:]
        # ----- Curve fitting for the obtained PSD -----
        fig = plt.figure(num = 1, figsize = (20,15), facecolor = '#A0AEC1', edgecolor = 'white')
        fig.subplots_adjust(left=0.05, bottom=0.1, right=0.95, top=0.875, wspace=0.1)        
        ax1, ax2 = fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)
        ax1.set_ylabel('PSD [mV**2/Hz]', fontsize = 'x-large')
        ax1.set_title('C3', fontsize = 'xx-large')
        ax2.set_title('C4', fontsize = 'xx-large')        
        peak1a, peak1b = self.CurveFitting(frec_c3, Pxx_c3, iaf, ax1)
        peak2a, peak2b = self.CurveFitting(frec_c4, Pxx_c4, iaf, ax2)  
        peaka = np.around(np.mean([peak1a, peak2a]), decimals=2)
        peakb = np.around(np.mean([peak1b, peak2b]), decimals=2)
        t = 'PredictorA = ' + str(peaka) + '\nPredictorB = ' + str(peakb)
        fig.suptitle(t, fontsize = 'xx-large', color = 'r', va = 'top')
        plt.savefig(self.url+'NeuroPredictor.png', edgecolor = 'white')
        plt.close(fig)


    #............... Method 5: Curve Fitting ..............
    def CurveFitting(self, frec, Pxx, iaf, ax):
        'Non-Linear Least-Squares Minimization and Curve-Fitting for Python'
        
        # ----- adjusting a model to the obtained PSD -----               
        # model 1: constante
        g1 = ConstantModel(prefix = 'g1_')
        pars = g1.guess(Pxx, x = frec)    
        pars['g1_c'].set(0)
        # model 2: k2/f^-1
        g2 = PowerLawModel(prefix = 'g2_')
        pars += g2.guess(Pxx, x = frec)
        pars['g2_exponent'].set(-1)
        #model 3: probability density function
        g3 = GaussianModel(prefix = 'g3_')
        pars += g3.guess(Pxx, x = frec)
        pars['g3_center'].set(iaf, min = iaf-2, max = iaf+2)
        # model 4: probability density function
        g4 = GaussianModel(prefix = 'g4_')
        pars += g4.guess(Pxx, x = frec)
        pars['g4_center'].set(20, min = 16, max = 25)
        # final model
        g = g1 + g2 + g3 + g4
        out = g.fit(Pxx, pars, x = frec)        
        # ----- plotting the desire PSD -----   
        # original and fitted curves
        ax.plot(frec, Pxx, 'k', linewidth = 2)
        ax.plot(frec, out.best_fit, 'b.-', linewidth = 2, markersize = 9)
        ax.set_xlim(frec[0], 32)
        ax.set_ylim(ymin = 0)
        ax.tick_params(axis = 'both', labelsize = 16)
        ax.set_xlabel('Frequency [Hz]', fontsize = 'x-large')
        ax.grid()
        # components of the fitted curved
        comps = out.eval_components(x = frec)
        g12 = comps['g1_'] + comps['g2_']
        ax.plot(frec, g12, 'g--', linewidth = 2)       
        # final value on the subplot
        diffs = out.best_fit - g12
        peak1 = np.amax(diffs)
        idx = np.where(diffs == peak1)[0]
        ax.plot((frec[idx],frec[idx]), (g12[idx],out.best_fit[idx]), 'r-o', linewidth = 3, markersize = 9) 
        ax.text(frec[idx], g12[idx], str(np.around(peak1, decimals=2)), horizontalalignment='right', verticalalignment='top', color='r', fontsize='xx-large')
        # optional valued on the subplot
        idx1, idx2 = np.where(frec == (np.round(iaf)-2))[0], np.where(frec == (np.round(iaf)+2))[0]
        diffs = Pxx[idx1:idx2] - g12[idx1:idx2]
        peak2 = np.amax(diffs)        
        idx = np.where(peak2 == diffs)[0]
        idx+= len(Pxx[:idx1])
        ax.plot((frec[idx],frec[idx]), (g12[idx], Pxx[idx]), 'r-*', linewidth = 3, markersize = 11) 
        ax.text(frec[idx], Pxx[idx], str(np.around(peak2, decimals=2)), horizontalalignment='left', verticalalignment='top', color='r', fontsize='xx-large')
        
        return peak1, peak2

# -----------------------------------------------------------------------------
#                       MAIN BODY - Main Calling Process
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    InitialReport()
    NeuroIndexes()