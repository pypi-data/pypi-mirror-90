"""
Digital Communications Function Module

Copyright (c) March 2017, Mark Wickert
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.
"""

from matplotlib import pylab
from matplotlib import mlab
import numpy as np
from numpy import fft
import matplotlib.pyplot as plt
from scipy import signal
from scipy.special import erfc
from sys import exit
from .sigsys import upsample
from .sigsys import downsample
from .sigsys import NRZ_bits
from .sigsys import NRZ_bits2
from .sigsys import PN_gen
from .sigsys import m_seq
from .sigsys import cpx_AWGN
from .sigsys import CIC

from logging import getLogger
log = getLogger(__name__)
import warnings


def farrow_resample(x, fs_old, fs_new):
    """
    Parameters
    ----------
    x : Input list representing a signal vector needing resampling.
    fs_old : Starting/old sampling frequency.
    fs_new : New sampling frequency.

    Returns
    -------
    y : List representing the signal vector resampled at the new frequency.

    Notes
    -----

    A cubic interpolator using a Farrow structure is used resample the
    input data at a new sampling rate that may be an irrational multiple of
    the input sampling rate.

    Time alignment can be found for a integer value M, found with the following:

    .. math:: f_{s,out} = f_{s,in} (M - 1) / M
    
    The filter coefficients used here and a more comprehensive listing can be
    found in H. Meyr, M. Moeneclaey, & S. Fechtel, "Digital Communication 
    Receivers," Wiley, 1998, Chapter 9, pp. 521-523.
    
    Another good paper on variable interpolators is: L. Erup, F. Gardner, &
    R. Harris, "Interpolation in Digital Modems--Part II: Implementation
    and Performance," IEEE Comm. Trans., June 1993, pp. 998-1008.
    
    A founding paper on the subject of interpolators is: C. W. Farrow, "A
    Continuously variable Digital Delay Element," Proceedings of the IEEE
    Intern. Symp. on Circuits Syst., pp. 2641-2645, June 1988.
    
    Mark Wickert April 2003, recoded to Python November 2013

    Examples
    --------

    The following example uses a QPSK signal with rc pulse shaping, and time alignment at M = 15.

    >>> import matplotlib.pyplot as plt
    >>> from numpy import arange
    >>> from sk_dsp_comm import digitalcom as dc
    >>> Ns = 8
    >>> Rs = 1.
    >>> fsin = Ns*Rs
    >>> Tsin = 1 / fsin
    >>> N = 200
    >>> ts = 1
    >>> x, b, data = dc.MPSK_bb(N+12, Ns, 4, 'rc')
    >>> x = x[12*Ns:]
    >>> xxI = x.real
    >>> M = 15
    >>> fsout = fsin * (M-1) / M
    >>> Tsout = 1. / fsout
    >>> xI = dc.farrow_resample(xxI, fsin, fsin)
    >>> tx = arange(0, len(xI)) / fsin
    >>> yI = dc.farrow_resample(xxI, fsin, fsout)
    >>> ty = arange(0, len(yI)) / fsout
    >>> plt.plot(tx - Tsin, xI)
    >>> plt.plot(tx[ts::Ns] - Tsin, xI[ts::Ns], 'r.')
    >>> plt.plot(ty[ts::Ns] - Tsout, yI[ts::Ns], 'g.')
    >>> plt.title(r'Impact of Asynchronous Sampling')
    >>> plt.ylabel(r'Real Signal Amplitude')
    >>> plt.xlabel(r'Symbol Rate Normalized Time')
    >>> plt.xlim([0, 20])
    >>> plt.grid()
    >>> plt.show()
    """
    
    #Cubic interpolator over 4 samples.
    #The base point receives a two sample delay.
    v3 = signal.lfilter([1/6., -1/2., 1/2., -1/6.],[1],x)
    v2 = signal.lfilter([0, 1/2., -1, 1/2.],[1],x)
    v1 = signal.lfilter([-1/6., 1, -1/2., -1/3.],[1],x)
    v0 = signal.lfilter([0, 0, 1],[1],x)
    
    Ts_old = 1/float(fs_old)
    Ts_new = 1/float(fs_new)
    
    T_end = Ts_old*(len(x)-3)
    t_new = np.arange(0,T_end+Ts_old,Ts_new)
    if x.dtype == np.dtype('complex128') or x.dtype == np.dtype('complex64'):
        y = np.zeros(len(t_new)) + 1j*np.zeros(len(t_new))
    else:
        y = np.zeros(len(t_new))

    for n in range(len(t_new)):
        n_old = int(np.floor(n*Ts_new/Ts_old))
        mu = (n*Ts_new - n_old*Ts_old)/Ts_old
        # Combine outputs
        y[n] = ((v3[n_old+1]*mu + v2[n_old+1])*mu
                + v1[n_old+1])*mu + v0[n_old+1]
    return y


def eye_plot(x,L,S=0):
    """
    Eye pattern plot of a baseband digital communications waveform.

    The signal must be real, but can be multivalued in terms of the underlying
    modulation scheme. Used for BPSK eye plots in the Case Study article.

    Parameters
    ----------
    x : ndarray of the real input data vector/array
    L : display length in samples (usually two symbols)
    S : start index

    Returns
    -------
    None : A plot window opens containing the eye plot
    
    Notes
    -----
    Increase S to eliminate filter transients.
    
    Examples
    --------
    1000 bits at 10 samples per bit with 'rc' shaping.

    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import digitalcom as dc
    >>> x,b, data = dc.NRZ_bits(1000,10,'rc')
    >>> dc.eye_plot(x,20,60)
    >>> plt.show()
    """
    plt.figure(figsize=(6,4))
    idx = np.arange(0,L+1)
    plt.plot(idx,x[S:S+L+1],'b')
    k_max = int((len(x) - S)/L)-1
    for k in range(1,k_max):
         plt.plot(idx,x[S+k*L:S+L+1+k*L],'b')
    plt.grid()
    plt.xlabel('Time Index - n')
    plt.ylabel('Amplitude')
    plt.title('Eye Plot')
    return 0


def scatter(x,Ns,start):
    """
    Sample a baseband digital communications waveform at the symbol spacing.

    Parameters
    ----------
    x : ndarray of the input digital comm signal
    Ns : number of samples per symbol (bit)
    start : the array index to start the sampling

    Returns
    -------
    xI : ndarray of the real part of x following sampling
    xQ : ndarray of the imaginary part of x following sampling

    Notes
    -----
    Normally the signal is complex, so the scatter plot contains 
    clusters at point  in the complex plane. For a binary signal 
    such as BPSK, the point centers are nominally +/-1 on the real
    axis. Start is used to eliminate transients from the FIR
    pulse shaping filters from appearing in the scatter plot.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import digitalcom as dc
    >>> x,b, data = dc.NRZ_bits(1000,10,'rc')

    Add some noise so points are now scattered about +/-1.

    >>> y = dc.cpx_AWGN(x,20,10)
    >>> yI,yQ = dc.scatter(y,10,60)
    >>> plt.plot(yI,yQ,'.')
    >>> plt.grid()
    >>> plt.xlabel('In-Phase')
    >>> plt.ylabel('Quadrature')
    >>> plt.axis('equal')
    >>> plt.show()
    """
    xI = np.real(x[start::Ns])
    xQ = np.imag(x[start::Ns])
    return xI, xQ


def strips(x,Nx,fig_size=(6,4)):
    """
    Plots the contents of real ndarray x as a vertical stacking of
    strips, each of length Nx. The default figure size is (6,4) inches.
    The yaxis tick labels are the starting index of each strip. The red
    dashed lines correspond to zero amplitude in each strip.

    strips(x,Nx,my_figsize=(6,4))

    Mark Wickert April 2014
    """
    plt.figure(figsize=fig_size)
    #ax = fig.add_subplot(111)
    N = len(x)
    Mx = int(np.ceil(N/float(Nx)))
    x_max = np.max(np.abs(x))
    for kk in range(Mx):
        plt.plot(np.array([0,Nx]),-kk*Nx*np.array([1,1]),'r-.')
        plt.plot(x[kk*Nx:(kk+1)*Nx]/x_max*0.4*Nx-kk*Nx,'b')
    plt.axis([0,Nx,-Nx*(Mx-0.5),Nx*0.5])
    plt.yticks(np.arange(0,-Nx*Mx,-Nx),np.arange(0,Nx*Mx,Nx))
    plt.xlabel('Index')
    plt.ylabel('Strip Amplitude and Starting Index')
    return 0


def bit_errors(tx_data,rx_data,Ncorr = 1024,Ntransient = 0):
    """
    Count bit errors between a transmitted and received BPSK signal.
    Time delay between streams is detected as well as ambiquity resolution
    due to carrier phase lock offsets of :math:`k*\\pi`, k=0,1.
    The ndarray tx_data is Tx 0/1 bits as real numbers I.
    The ndarray rx_data is Rx 0/1 bits as real numbers I.
    Note: Ncorr needs to be even
    """
    
    # Remove Ntransient symbols and level shift to {-1,+1}
    tx_data = 2*tx_data[Ntransient:]-1
    rx_data = 2*rx_data[Ntransient:]-1
    # Correlate the first Ncorr symbols at four possible phase rotations
    R0 = np.fft.ifft(np.fft.fft(rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R1 = np.fft.ifft(np.fft.fft(-1*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    #Place the zero lag value in the center of the array
    R0 = np.fft.fftshift(R0)
    R1 = np.fft.fftshift(R1)
    R0max = np.max(R0.real)
    R1max = np.max(R1.real)
    R = np.array([R0max,R1max])
    Rmax = np.max(R)
    kphase_max = np.where(R == Rmax)[0]
    kmax = kphase_max[0]
    # Correlation lag value is zero at the center of the array
    if kmax == 0:
        lagmax = np.where(R0.real == Rmax)[0] - Ncorr/2
    elif kmax == 1:
        lagmax = np.where(R1.real == Rmax)[0] - Ncorr/2
    taumax = lagmax[0]
    log.info('kmax =  %d, taumax = %d' % (kmax, taumax))

    # Count bit and symbol errors over the entire input ndarrays
    # Begin by making tx and rx length equal and apply phase rotation to rx
    if taumax < 0:
        tx_data = tx_data[int(-taumax):]
        tx_data = tx_data[:min(len(tx_data),len(rx_data))]
        rx_data = (-1)**kmax*rx_data[:len(tx_data)]
    else:
        rx_data = (-1)**kmax * rx_data[int(taumax):]
        rx_data = rx_data[:min(len(tx_data),len(rx_data))]
        tx_data = tx_data[:len(rx_data)]
    # Convert to 0's and 1's
    Bit_count = len(tx_data)
    tx_I = np.int16((tx_data.real + 1)/2)
    rx_I = np.int16((rx_data.real + 1)/2)
    Bit_errors = tx_I ^ rx_I
    return Bit_count,np.sum(Bit_errors)


def QAM_bb(N_symb,Ns,mod_type='16qam',pulse='rect',alpha=0.35):
    """
    QAM_BB_TX: A complex baseband transmitter 
    x,b,tx_data = QAM_bb(K,Ns,M)

    //////////// Inputs //////////////////////////////////////////////////
      N_symb = the number of symbols to process
          Ns = number of samples per symbol
    mod_type = modulation type: qpsk, 16qam, 64qam, or 256qam
       alpha = squareroot raised codine pulse shape bandwidth factor.
               For DOCSIS alpha = 0.12 to 0.18. In general alpha can 
               range over 0 < alpha < 1.
         SRC = pulse shape: 0-> rect, 1-> SRC
    //////////// Outputs /////////////////////////////////////////////////
           x = complex baseband digital modulation
           b = transmitter shaping filter, rectangle or SRC
     tx_data = xI+1j*xQ = inphase symbol sequence + 
               1j*quadrature symbol sequence

    Mark Wickert November 2014
    """
    # Filter the impulse train waveform with a square root raised
    # cosine pulse shape designed as follows:

    # Design the filter to be of duration 12 symbols and
    # fix the excess bandwidth factor at alpha = 0.35
    # If SRC = 0 use a simple rectangle pulse shape
    if pulse.lower() == 'src':
        b = sqrt_rc_imp(Ns,alpha,6)
    elif pulse.lower() == 'rc':
        b = rc_imp(Ns,alpha,6)    
    elif pulse.lower() == 'rect':
        b = np.ones(int(Ns)) #alt. rect. pulse shape
    else:
        raise ValueError('pulse shape must be src, rc, or rect')
        
    if mod_type.lower() == 'qpsk':
        M = 2 # bits per symbol
    elif mod_type.lower() == '16qam':
        M = 4
    elif mod_type.lower() == '64qam':
        M = 8
    elif mod_type.lower() == '256qam':
        M = 16
    else:
        raise ValueError('Unknown mod_type')

    # Create random symbols for the I & Q channels
    xI = np.random.randint(0,M,N_symb)
    xI = 2*xI - (M-1)
    xQ = np.random.randint(0,M,N_symb)
    xQ = 2*xQ - (M-1)
    # Employ differential encoding to counter phase ambiquities
    # Create a zero padded (interpolated by Ns) symbol sequence.
    # This prepares the symbol sequence for arbitrary pulse shaping.
    symbI = np.hstack((xI.reshape(N_symb,1),np.zeros((N_symb,int(Ns)-1))))
    symbI = symbI.flatten()
    symbQ = np.hstack((xQ.reshape(N_symb,1),np.zeros((N_symb,int(Ns)-1))))
    symbQ = symbQ.flatten()
    symb = symbI + 1j*symbQ
    if M > 2:
        symb /= (M-1)
    
    # The impulse train waveform contains one pulse per Ns (or Ts) samples
    # imp_train = [ones(K,1) zeros(K,Ns-1)]';
    # imp_train = reshape(imp_train,Ns*K,1);

    # Filter the impulse train signal
    x = signal.lfilter(b,1,symb)
    x = x.flatten() # out is a 1D vector
    # Scale shaping filter to have unity DC gain
    b = b/sum(b)
    return x, b, xI+1j*xQ


def QAM_SEP(tx_data,rx_data,mod_type,Ncorr = 1024,Ntransient = 0,SEP_disp=True):
    """
    Nsymb, Nerr, SEP_hat =
    QAM_symb_errors(tx_data,rx_data,mod_type,Ncorr = 1024,Ntransient = 0)
    
    Count symbol errors between a transmitted and received QAM signal.
    The received symbols are assumed to be soft values on a unit square.
    Time delay between streams is detected.
    The ndarray tx_data is Tx complex symbols.
    The ndarray rx_data is Rx complex symbols.
    Note: Ncorr needs to be even
    """
    #Remove Ntransient symbols and makes lengths equal
    tx_data = tx_data[Ntransient:]
    rx_data = rx_data[Ntransient:]
    Nmin = min([len(tx_data),len(rx_data)])
    tx_data = tx_data[:Nmin]
    rx_data = rx_data[:Nmin]
    
    # Perform level translation and quantize the soft symbol values
    if mod_type.lower() == 'qpsk':
        M = 2 # bits per symbol
    elif mod_type.lower() == '16qam':
        M = 4
    elif mod_type.lower() == '64qam':
        M = 8
    elif mod_type.lower() == '256qam':
        M = 16
    else:
        raise ValueError('Unknown mod_type')
    rx_data = np.rint((M-1)*(rx_data + (1+1j))/2.)
    # Fix-up edge points real part
    s1r = np.nonzero(np.ravel(rx_data.real > M - 1))[0]
    s2r = np.nonzero(np.ravel(rx_data.real < 0))[0]
    rx_data.real[s1r] = (M - 1)*np.ones(len(s1r))
    rx_data.real[s2r] = np.zeros(len(s2r))
    # Fix-up edge points imag part
    s1i = np.nonzero(np.ravel(rx_data.imag > M - 1))[0]
    s2i = np.nonzero(np.ravel(rx_data.imag < 0))[0]
    rx_data.imag[s1i] = (M - 1)*np.ones(len(s1i))
    rx_data.imag[s2i] = np.zeros(len(s2i))
    rx_data = 2*rx_data - (M - 1)*(1 + 1j)
    #Correlate the first Ncorr symbols at four possible phase rotations
    R0,lags = xcorr(rx_data,tx_data,Ncorr)
    R1,lags = xcorr(rx_data*(1j)**1,tx_data,Ncorr) 
    R2,lags = xcorr(rx_data*(1j)**2,tx_data,Ncorr) 
    R3,lags = xcorr(rx_data*(1j)**3,tx_data,Ncorr) 
    #Place the zero lag value in the center of the array
    R0max = np.max(R0.real)
    R1max = np.max(R1.real)
    R2max = np.max(R2.real)
    R3max = np.max(R3.real)
    R = np.array([R0max,R1max,R2max,R3max])
    Rmax = np.max(R)
    kphase_max = np.where(R == Rmax)[0]
    kmax = kphase_max[0]
    #Find correlation lag value is zero at the center of the array
    if kmax == 0:
        lagmax = lags[np.where(R0.real == Rmax)[0]]
    elif kmax == 1:
        lagmax = lags[np.where(R1.real == Rmax)[0]]
    elif kmax == 2:
        lagmax = lags[np.where(R2.real == Rmax)[0]]
    elif kmax == 3:
        lagmax = lags[np.where(R3.real == Rmax)[0]]
    taumax = lagmax[0]
    if SEP_disp:
        log.info('Phase ambiquity = (1j)**%d, taumax = %d' % (kmax, taumax))
    #Count symbol errors over the entire input ndarrays
    #Begin by making tx and rx length equal and apply 
    #phase rotation to rx_data
    if taumax < 0:
        tx_data = tx_data[-taumax:]
        tx_data = tx_data[:min(len(tx_data),len(rx_data))]
        rx_data = (1j)**kmax*rx_data[:len(tx_data)]
    else:
        rx_data = (1j)**kmax*rx_data[taumax:]
        rx_data = rx_data[:min(len(tx_data),len(rx_data))]
        tx_data = tx_data[:len(rx_data)]
    #Convert QAM symbol difference to symbol errors
    errors = np.int16(abs(rx_data-tx_data))
    # Detect symbols errors
    # Could decode bit errors from symbol index difference
    idx = np.nonzero(np.ravel(errors != 0))[0]
    if SEP_disp:
        log.info('Symbols = %d, Errors %d, SEP = %1.2e' \
               % (len(errors), len(idx), len(idx)/float(len(errors))))
    return  len(errors), len(idx), len(idx)/float(len(errors))


def GMSK_bb(N_bits, Ns, MSK = 0,BT = 0.35):
    """
    MSK/GMSK Complex Baseband Modulation
    x,data = gmsk(N_bits, Ns, BT = 0.35, MSK = 0)

    Parameters
    ----------
    N_bits : number of symbols processed
    Ns : the number of samples per bit
    MSK : 0 for no shaping which is standard MSK, MSK <> 0 --> GMSK is generated.
    BT : premodulation Bb*T product which sets the bandwidth of the Gaussian lowpass filter

    Mark Wickert Python version November 2014
    """
    x, b, data = NRZ_bits(N_bits,Ns)
    # pulse length 2*M*Ns
    M = 4
    n = np.arange(-M*Ns,M*Ns+1)
    p = np.exp(-2*np.pi**2*BT**2/np.log(2)*(n/float(Ns))**2);
    p = p/np.sum(p);

    # Gaussian pulse shape if MSK not zero
    if MSK != 0:
        x = signal.lfilter(p,1,x)
    y = np.exp(1j*np.pi/2*np.cumsum(x)/Ns)
    return y, data


def MPSK_bb(N_symb,Ns,M,pulse='rect',alpha = 0.25,MM=6):
    """
    Generate a complex baseband MPSK signal with pulse shaping.

    Parameters
    ----------
    N_symb : number of MPSK symbols to produce
    Ns : the number of samples per bit,
    M : MPSK modulation order, e.g., 4, 8, 16, ...
    pulse_type : 'rect' , 'rc', 'src' (default 'rect')
    alpha : excess bandwidth factor(default 0.25)
    MM : single sided pulse duration (default = 6) 

    Returns
    -------
    x : ndarray of the MPSK signal values
    b : ndarray of the pulse shape
    data : ndarray of the underlying data bits

    Notes
    -----
    Pulse shapes include 'rect' (rectangular), 'rc' (raised cosine), 
    'src' (root raised cosine). The actual pulse length is 2*M+1 samples.
    This function is used by BPSK_tx in the Case Study article.

    Examples
    --------
    >>> from sk_dsp_comm import digitalcom as dc
    >>> import scipy.signal as signal
    >>> import matplotlib.pyplot as plt
    >>> x,b,data = dc.MPSK_bb(500,10,8,'src',0.35)
    >>> # Matched filter received signal x
    >>> y = signal.lfilter(b,1,x)
    >>> plt.plot(y.real[12*10:],y.imag[12*10:])
    >>> plt.xlabel('In-Phase')
    >>> plt.ylabel('Quadrature')
    >>> plt.axis('equal')
    >>> # Sample once per symbol
    >>> plt.plot(y.real[12*10::10],y.imag[12*10::10],'r.')
    >>> plt.show()
    """
    data = np.random.randint(0,M,N_symb) 
    xs = np.exp(1j*2*np.pi/M*data)
    x = np.hstack((xs.reshape(N_symb,1),np.zeros((N_symb,int(Ns)-1))))
    x =x.flatten()
    if pulse.lower() == 'rect':
        b = np.ones(int(Ns))
    elif pulse.lower() == 'rc':
        b = rc_imp(Ns,alpha,MM)
    elif pulse.lower() == 'src':
        b = sqrt_rc_imp(Ns,alpha,MM)
    else:
        raise ValueError('pulse type must be rec, rc, or src')
    x = signal.lfilter(b,1,x)
    if M == 4:
        x = x*np.exp(1j*np.pi/4); # For QPSK points in quadrants
    return x,b/float(Ns),data


def QPSK_rx(fc,N_symb,Rs,EsN0=100,fs=125,lfsr_len=10,phase=0,pulse='src'):
    """
    This function generates
    """
    Ns = int(np.round(fs/Rs))
    log.info('Ns = ', Ns)
    log.info('Rs = ', fs/float(Ns))
    log.info('EsN0 = ', EsN0, 'dB')
    log.info('phase = ', phase, 'degrees')
    log.info('pulse = ', pulse)
    x, b, data = QPSK_bb(N_symb,Ns,lfsr_len,pulse)
    # Add AWGN to x
    x = cpx_AWGN(x,EsN0,Ns)
    n = np.arange(len(x))
    xc = x*np.exp(1j*2*np.pi*fc/float(fs)*n) * np.exp(1j*phase)
    return xc, b, data


def QPSK_tx(fc,N_symb,Rs,fs=125,lfsr_len=10,pulse='src'):
    """

    """
    Ns = int(np.round(fs/Rs))
    log.info('Ns = ', Ns)
    log.info('Rs = ', fs/float(Ns))
    log.info('pulse = ', pulse)
    x, b, data = QPSK_bb(N_symb,Ns,lfsr_len,pulse)
    n = np.arange(len(x))
    xc = x*np.exp(1j*2*np.pi*fc/float(fs)*n)
    return xc, b, data 


def QPSK_bb(N_symb,Ns,lfsr_len=5,pulse='src',alpha=0.25,M=6):
    """
    
    """
    if lfsr_len > 0:  # LFSR data
        data = PN_gen(2*N_symb,lfsr_len)
        dataI = data[0::2]
        dataQ = data[1::2]
        xI, b = NRZ_bits2(dataI,Ns,pulse,alpha,M)
        xQ, b = NRZ_bits2(dataQ,Ns,pulse,alpha,M)
    else:             # Random data
        data = np.zeros(2*N_symb)
        xI, b, data[0::2] = NRZ_bits(N_symb,Ns,pulse,alpha,M)
        xQ, b, data[1::2] = NRZ_bits(N_symb,Ns,pulse,alpha,M)        
    #print('P_I: ',np.var(xI), 'P_Q: ',np.var(xQ))
    x = (xI + 1j*xQ)/np.sqrt(2.)
    return x, b, data


def QPSK_BEP(tx_data,rx_data,Ncorr = 1024,Ntransient = 0):
    """
    Count bit errors between a transmitted and received QPSK signal.
    Time delay between streams is detected as well as ambiquity resolution
    due to carrier phase lock offsets of :math:`k*\\frac{\\pi}{4}`, k=0,1,2,3.
    The ndarray sdata is Tx +/-1 symbols as complex numbers I + j*Q.
    The ndarray data is Rx +/-1 symbols as complex numbers I + j*Q.
    Note: Ncorr needs to be even
    """
    
    #Remove Ntransient symbols
    tx_data = tx_data[Ntransient:]
    rx_data = rx_data[Ntransient:]
    #Correlate the first Ncorr symbols at four possible phase rotations
    R0 = np.fft.ifft(np.fft.fft(rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R1 = np.fft.ifft(np.fft.fft(1j*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R2 = np.fft.ifft(np.fft.fft(-1*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R3 = np.fft.ifft(np.fft.fft(-1j*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    #Place the zero lag value in the center of the array
    R0 = np.fft.fftshift(R0)
    R1 = np.fft.fftshift(R1)
    R2 = np.fft.fftshift(R2)
    R3 = np.fft.fftshift(R3)
    R0max = np.max(R0.real)
    R1max = np.max(R1.real)
    R2max = np.max(R2.real)
    R3max = np.max(R3.real)
    R = np.array([R0max,R1max,R2max,R3max])
    Rmax = np.max(R)
    kphase_max = np.where(R == Rmax)[0]
    kmax = kphase_max[0]
    #Correlation lag value is zero at the center of the array
    if kmax == 0:
        lagmax = np.where(R0.real == Rmax)[0] - Ncorr/2
    elif kmax == 1:
        lagmax = np.where(R1.real == Rmax)[0] - Ncorr/2
    elif kmax == 2: 
        lagmax = np.where(R2.real == Rmax)[0] - Ncorr/2
    elif kmax == 3:
        lagmax = np.where(R3.real == Rmax)[0] - Ncorr/2
    taumax = lagmax[0]
    log.info('kmax =  %d, taumax = %d' % (kmax, taumax))
    # Count bit and symbol errors over the entire input ndarrays
    # Begin by making tx and rx length equal and apply phase rotation to rx
    if taumax < 0:
        tx_data = tx_data[-taumax:]
        tx_data = tx_data[:min(len(tx_data),len(rx_data))]
        rx_data = 1j**kmax*rx_data[:len(tx_data)]
    else:
        rx_data = 1j**kmax*rx_data[taumax:]
        rx_data = rx_data[:min(len(tx_data),len(rx_data))]
        tx_data = tx_data[:len(rx_data)]
    #Convert to 0's and 1's
    S_count = len(tx_data)
    tx_I = np.int16((tx_data.real + 1)/2)
    tx_Q = np.int16((tx_data.imag + 1)/2)
    rx_I = np.int16((rx_data.real + 1)/2)
    rx_Q = np.int16((rx_data.imag + 1)/2)
    I_errors = tx_I ^ rx_I
    Q_errors = tx_Q ^ rx_Q
    #A symbol errors occurs when I or Q or both are in error
    S_errors = I_errors | Q_errors
    #return 0
    return S_count,np.sum(I_errors),np.sum(Q_errors),np.sum(S_errors)


def BPSK_BEP(tx_data,rx_data,Ncorr = 1024,Ntransient = 0):
    """
    Count bit errors between a transmitted and received BPSK signal.
    Time delay between streams is detected as well as ambiquity resolution
    due to carrier phase lock offsets of :math:`k*\\pi`, k=0,1.
    The ndarray tx_data is Tx +/-1 symbols as real numbers I.
    The ndarray rx_data is Rx +/-1 symbols as real numbers I.
    Note: Ncorr needs to be even
    """
    
    #Remove Ntransient symbols
    tx_data = tx_data[Ntransient:]
    rx_data = rx_data[Ntransient:]
    #Correlate the first Ncorr symbols at four possible phase rotations
    R0 = np.fft.ifft(np.fft.fft(rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    R1 = np.fft.ifft(np.fft.fft(-1*rx_data,Ncorr)*
                     np.conj(np.fft.fft(tx_data,Ncorr)))
    #Place the zero lag value in the center of the array
    R0 = np.fft.fftshift(R0)
    R1 = np.fft.fftshift(R1)
    R0max = np.max(R0.real)
    R1max = np.max(R1.real)
    R = np.array([R0max,R1max])
    Rmax = np.max(R)
    kphase_max = np.where(R == Rmax)[0]
    kmax = kphase_max[0]
    #Correlation lag value is zero at the center of the array
    if kmax == 0:
        lagmax = np.where(R0.real == Rmax)[0] - Ncorr/2
    elif kmax == 1:
        lagmax = np.where(R1.real == Rmax)[0] - Ncorr/2
    taumax = int(lagmax[0])
    log.info('kmax =  %d, taumax = %d' % (kmax, taumax))
    #return R0,R1,R2,R3
    #Count bit and symbol errors over the entire input ndarrays
    #Begin by making tx and rx length equal and apply phase rotation to rx
    if taumax < 0:
        tx_data = tx_data[-taumax:]
        tx_data = tx_data[:min(len(tx_data),len(rx_data))]
        rx_data = (-1)**kmax*rx_data[:len(tx_data)]
    else:
        rx_data = (-1)**kmax*rx_data[taumax:]
        rx_data = rx_data[:min(len(tx_data),len(rx_data))]
        tx_data = tx_data[:len(rx_data)]
    #Convert to 0's and 1's
    S_count = len(tx_data)
    tx_I = np.int16((tx_data.real + 1)/2)
    rx_I = np.int16((rx_data.real + 1)/2)
    I_errors = tx_I ^ rx_I
    #Symbol errors and bit errors are equivalent
    S_errors = I_errors
    #return tx_data, rx_data
    return S_count,np.sum(S_errors)


def BPSK_tx(N_bits,Ns,ach_fc=2.0,ach_lvl_dB=-100,pulse='rect',alpha = 0.25,M=6):
    """
    Generates biphase shift keyed (BPSK) transmitter with adjacent channel interference.

    Generates three BPSK signals with rectangular or square root raised cosine (SRC) 
    pulse shaping of duration N_bits and Ns samples per bit. The desired signal is
    centered on f = 0, which the adjacent channel signals to the left and right
    are also generated at dB level relative to the desired signal. Used in the 
    digital communications Case Study supplement.

    Parameters
    ----------
    N_bits : the number of bits to simulate
    Ns : the number of samples per bit
    ach_fc : the frequency offset of the adjacent channel signals (default 2.0)
    ach_lvl_dB : the level of the adjacent channel signals in dB (default -100)
    pulse : the pulse shape 'rect' or 'src'
    alpha : square root raised cosine pulse shape factor (default = 0.25)
    M : square root raised cosine pulse truncation factor (default = 6)

    Returns
    -------
    x : ndarray of the composite signal x0 + ach_lvl*(x1p + x1m)
    b : the transmit pulse shape 
    data0 : the data bits used to form the desired signal; used for error checking

    Notes
    -----

    Examples
    --------
    >>> x,b,data0 = BPSK_tx(1000,10,'src')
    """
    x0,b,data0 = NRZ_bits(N_bits,Ns,pulse,alpha,M)
    x1p,b,data1p = NRZ_bits(N_bits,Ns,pulse,alpha,M)
    x1m,b,data1m = NRZ_bits(N_bits,Ns,pulse,alpha,M)
    n = np.arange(len(x0))
    x1p = x1p*np.exp(1j*2*np.pi*ach_fc/float(Ns)*n)
    x1m = x1m*np.exp(-1j*2*np.pi*ach_fc/float(Ns)*n)
    ach_lvl = 10**(ach_lvl_dB/20.)
    return x0 + ach_lvl*(x1p + x1m), b, data0


def rc_imp(Ns,alpha,M=6):
    """
    A truncated raised cosine pulse used in digital communications.

    The pulse shaping factor :math:`0 < \\alpha < 1` is required as well as the
    truncation factor M which sets the pulse duration to be :math:`2*M*T_{symbol}`.

    Parameters
    ----------
    Ns : number of samples per symbol
    alpha : excess bandwidth factor on (0, 1), e.g., 0.35
    M : equals RC one-sided symbol truncation factor

    Returns
    -------
    b : ndarray containing the pulse shape

    See Also
    --------
    sqrt_rc_imp

    Notes
    -----
    The pulse shape b is typically used as the FIR filter coefficients
    when forming a pulse shaped digital communications waveform.

    Examples
    --------
    Ten samples per symbol and :math:`\\alpha = 0.35`.

    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm.digitalcom import rc_imp
    >>> from numpy import arange
    >>> b = rc_imp(10,0.35)
    >>> n = arange(-10*6,10*6+1)
    >>> plt.stem(n,b)
    >>> plt.show()
    """
    # Design the filter
    n = np.arange(-M*Ns,M*Ns+1)
    b = np.zeros(len(n))
    a = alpha
    Ns *= 1.0
    for i in range(len(n)):
        if (1 - 4*(a*n[i]/Ns)**2) == 0:
            b[i] = np.pi/4*np.sinc(1/(2.*a))
        else:
            b[i] = np.sinc(n[i]/Ns)*np.cos(np.pi*a*n[i]/Ns)/(1 - 4*(a*n[i]/Ns)**2)
    return b


def sqrt_rc_imp(Ns,alpha,M=6):
    """
    A truncated square root raised cosine pulse used in digital communications.

    The pulse shaping factor :math:`0 < \\alpha < 1` is required as well as the
    truncation factor M which sets the pulse duration to be :math:`2*M*T_{symbol}`.
     

    Parameters
    ----------
    Ns : number of samples per symbol
    alpha : excess bandwidth factor on (0, 1), e.g., 0.35
    M : equals RC one-sided symbol truncation factor

    Returns
    -------
    b : ndarray containing the pulse shape

    Notes
    -----
    The pulse shape b is typically used as the FIR filter coefficients
    when forming a pulse shaped digital communications waveform. When 
    square root raised cosine (SRC) pulse is used to generate Tx signals and
    at the receiver used as a matched filter (receiver FIR filter), the 
    received signal is now raised cosine shaped, thus having zero
    intersymbol interference and the optimum removal of additive white 
    noise if present at the receiver input.

    Examples
    --------
    Ten samples per symbol and :math:`\\alpha = 0.35`.

    >>> import matplotlib.pyplot as plt
    >>> from numpy import arange
    >>> from sk_dsp_comm.digitalcom import sqrt_rc_imp
    >>> b = sqrt_rc_imp(10,0.35)
    >>> n = arange(-10*6,10*6+1)
    >>> plt.stem(n,b)
    >>> plt.show()
    """
    # Design the filter
    n = np.arange(-M*Ns,M*Ns+1)
    b = np.zeros(len(n))
    Ns *= 1.0
    a = alpha
    for i in range(len(n)):
       if abs(1 - 16*a**2*(n[i]/Ns)**2) <= np.finfo(np.float).eps/2:
           b[i] = 1/2.*((1+a)*np.sin((1+a)*np.pi/(4.*a))-(1-a)*np.cos((1-a)*np.pi/(4.*a))+(4*a)/np.pi*np.sin((1-a)*np.pi/(4.*a)))
       else:
           b[i] = 4*a/(np.pi*(1 - 16*a**2*(n[i]/Ns)**2))
           b[i] = b[i]*(np.cos((1+a)*np.pi*n[i]/Ns) + np.sinc((1-a)*n[i]/Ns)*(1-a)*np.pi/(4.*a))
    return b    


def RZ_bits(N_bits,Ns,pulse='rect',alpha = 0.25,M=6):
    """
    Generate return-to-zero (RZ) data bits with pulse shaping.

    A baseband digital data signal using +/-1 amplitude signal values
    and including pulse shaping.

    Parameters
    ----------
    N_bits : number of RZ {0,1} data bits to produce
    Ns : the number of samples per bit,
    pulse_type : 'rect' , 'rc', 'src' (default 'rect')
    alpha : excess bandwidth factor(default 0.25)
    M : single sided pulse duration (default = 6) 

    Returns
    -------
    x : ndarray of the RZ signal values
    b : ndarray of the pulse shape
    data : ndarray of the underlying data bits

    Notes
    -----
    Pulse shapes include 'rect' (rectangular), 'rc' (raised cosine), 
    'src' (root raised cosine). The actual pulse length is 2*M+1 samples.
    This function is used by BPSK_tx in the Case Study article.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from numpy import arange
    >>> from sk_dsp_comm.digitalcom import RZ_bits
    >>> x,b,data = RZ_bits(100,10)
    >>> t = arange(len(x))
    >>> plt.plot(t,x)
    >>> plt.ylim([-0.01, 1.01])
    >>> plt.show()
    """
    data = np.random.randint(0,2,N_bits) 
    x = np.hstack((data.reshape(N_bits,1),np.zeros((N_bits,int(Ns)-1))))
    x =x.flatten()
    if pulse.lower() == 'rect':
        b = np.ones(int(Ns))
    elif pulse.lower() == 'rc':
        b = rc_imp(Ns,alpha,M)
    elif pulse.lower() == 'src':
        b = sqrt_rc_imp(Ns,alpha,M)
    else:
        warnings.warn('pulse type must be rec, rc, or src')
    x = signal.lfilter(b,1,x)
    return x,b/float(Ns),data


def my_psd(x,NFFT=2**10,Fs=1):
    """
    A local version of NumPy's PSD function that returns the plot arrays.

    A mlab.psd wrapper function that returns two ndarrays;
    makes no attempt to auto plot anything.

    Parameters
    ----------
    x : ndarray input signal
    NFFT : a power of two, e.g., 2**10 = 1024
    Fs : the sampling rate in Hz

    Returns
    -------
    Px : ndarray of the power spectrum estimate
    f : ndarray of frequency values
    
    Notes
    -----
    This function makes it easier to overlay spectrum plots because
    you have better control over the axis scaling than when using psd()
    in the autoscale mode.
    
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import digitalcom as dc
    >>> from numpy import log10
    >>> x,b, data = dc.NRZ_bits(10000,10)
    >>> Px,f = dc.my_psd(x,2**10,10)
    >>> plt.plot(f, 10*log10(Px))
    >>> plt.show()
    """
    Px,f = pylab.mlab.psd(x,NFFT,Fs)
    return Px.flatten(), f


def time_delay(x,D,N=4):
    """
    A time varying time delay which takes advantage of the Farrow structure
    for cubic interpolation:

    y = time_delay(x,D,N = 3)

    Note that D is an array of the same length as the input signal x. This
    allows you to make the delay a function of time. If you want a constant 
    delay just use D*zeros(len(x)). The minimum delay allowable is one sample
    or D = 1.0. This is due to the causal system nature of the Farrow 
    structure.

    A founding paper on the subject of interpolators is: C. W. Farrow, "A
    Continuously variable Digital Delay Element," Proceedings of the IEEE
    Intern. Symp. on Circuits Syst., pp. 2641-2645, June 1988.

    Mark Wickert, February 2014
    """

    if type(D) == float or type(D) == int:
        #Make sure D stays with in the tapped delay line bounds
        if int(np.fix(D)) < 1:
            log.info('D has integer part less than one')
            exit(1)
        if int(np.fix(D)) > N-2:
            log.info('D has integer part greater than N - 2')
            exit(1)
        # Filter 4-tap input with four Farrow FIR filters
        # Since the time delay is a constant, the LTI filter
        # function from scipy.signal is convenient.
        D_frac = D - np.fix(D)
        Nd = int(np.fix(D))
        b = np.zeros(Nd + 4)
        # Load Lagrange coefficients into the last four FIR taps
        b[Nd] = -(D_frac-1)*(D_frac-2)*(D_frac-3)/6.
        b[Nd + 1] = D_frac*(D_frac-2)*(D_frac-3)/2.
        b[Nd + 2] = -D_frac*(D_frac-1)*(D_frac-3)/2.
        b[Nd + 3] = D_frac*(D_frac-1)*(D_frac-2)/6.
        # Do all of the filtering in one step for this special case
        # of a fixed delay.
        y = signal.lfilter(b,[1],x)
    else:
        # Make sure D stays with in the tapped delay line bounds
        if np.fix(np.min(D)) < 1:
            log.info('D has integer part less than one')
            exit(1)
        if np.fix(np.max(D)) > N-2:
            log.info('D has integer part greater than N - 2')
            exit(1)
        y = np.zeros(len(x))
        X = np.zeros(N+1)
        # Farrow filter tap weights
        W3 = np.array([[1./6, -1./2, 1./2, -1./6]])
        W2 = np.array([[0, 1./2, -1., 1./2]])
        W1 = np.array([[-1./6, 1., -1./2, -1./3]])
        W0 = np.array([[0, 0, 1., 0]])
        for k in range(len(x)):
            Nd = int(np.fix(D[k]))
            mu = 1 - (D[k]-np.fix(D[k]))
            # Form a row vector of signal samples, present and past values
            X = np.hstack((np.array(x[k]), X[:-1]))
            # Filter 4-tap input with four Farrow FIR filters
            # Here numpy dot(A,B) performs the matrix multiply
            # since the filter has time-varying coefficients
            v3 = np.dot(W3,np.array(X[Nd-1:Nd+3]).T)
            v2 = np.dot(W2,np.array(X[Nd-1:Nd+3]).T)
            v1 = np.dot(W1,np.array(X[Nd-1:Nd+3]).T)
            v0 = np.dot(W0,np.array(X[Nd-1:Nd+3]).T)
            #Combine sub-filter outputs using mu = 1 - d
            y[k] = ((v3[0]*mu + v2[0])*mu + v1[0])*mu + v0[0]
    return y


def xcorr(x1,x2,Nlags):
    """
    r12, k = xcorr(x1,x2,Nlags), r12 and k are ndarray's
    Compute the energy normalized cross correlation between the sequences
    x1 and x2. If x1 = x2 the cross correlation is the autocorrelation.
    The number of lags sets how many lags to return centered about zero
    """
    K = 2*(int(np.floor(len(x1)/2)))
    X1 = fft.fft(x1[:K])
    X2 = fft.fft(x2[:K])
    E1 = sum(abs(x1[:K])**2)
    E2 = sum(abs(x2[:K])**2)
    r12 = np.fft.ifft(X1*np.conj(X2))/np.sqrt(E1*E2)
    k = np.arange(K) - int(np.floor(K/2))
    r12 = np.fft.fftshift(r12)
    idx = np.nonzero(np.ravel(abs(k) <= Nlags))
    return r12[idx], k[idx]


def Q_fctn(x):
    """
    Gaussian Q-function
    """
    return 1./2*erfc(x/np.sqrt(2.))


def PCM_encode(x,N_bits):
    """
    Parameters
    ----------
    x : signal samples to be PCM encoded
    N_bits ; bit precision of PCM samples

    Returns
    -------
    x_bits = encoded serial bit stream of 0/1 values. MSB first.

    Mark Wickert, Mark 2015
    """
    xq = np.int16(np.rint(x*2**(N_bits-1)))
    x_bits = np.zeros((N_bits,len(xq)))
    for k, xk in enumerate(xq):
        x_bits[:,k] = to_bin(xk,N_bits)
    # Reshape into a serial bit stream
    x_bits = np.reshape(x_bits,(1,len(x)*N_bits),'F')
    return np.int16(x_bits.flatten())


# A helper function for PCM_encode and elsewhere
def to_bin(data, width):
    """
    Convert an unsigned integer to a numpy binary array with the first
    element the MSB and the last element the LSB.
    """
    data_str = bin(data & (2**width-1))[2:].zfill(width)
    return [int(x) for x in tuple(data_str)]


def from_bin(bin_array):
    """
    Convert binary array back a nonnegative integer. The array length is 
    the bit width. The first input index holds the MSB and the last holds the LSB.
    """
    width = len(bin_array)
    bin_wgts = 2**np.arange(width-1,-1,-1)
    return int(np.dot(bin_array,bin_wgts))


def PCM_decode(x_bits,N_bits):
    """
    Parameters
    ----------
    x_bits : serial bit stream of 0/1 values. The length of
             x_bits must be a multiple of N_bits
    N_bits : bit precision of PCM samples

    Returns
    -------
      xhat : decoded PCM signal samples

    Mark Wickert, March 2015
    """
    N_samples = len(x_bits)//N_bits
    # Convert serial bit stream into parallel words with each 
    # column holdingthe N_bits binary sample value
    xrs_bits = x_bits.copy()
    xrs_bits = np.reshape(xrs_bits,(N_bits,N_samples),'F')
    # Convert N_bits binary words into signed integer values
    xq = np.zeros(N_samples)
    w = 2**np.arange(N_bits-1,-1,-1) # binary weights for bin 
                                     # to dec conversion
    for k in range(N_samples):
       xq[k] = np.dot(xrs_bits[:,k],w) - xrs_bits[0,k]*2**N_bits
    return xq/2**(N_bits-1)


def AWGN_chan(x_bits,EBN0_dB):
    """

    Parameters
    ----------
    x_bits : serial bit stream of 0/1 values.
    EBN0_dB : Energy per bit to noise power density ratio in dB of the serial bit stream sent through the AWGN channel. Frequently we equate EBN0 to SNR in link budget calculations.

    Returns
    -------
    y_bits : Received serial bit stream following hard decisions. This bit will have bit errors. To check the estimated bit error probability use :func:`BPSK_BEP` or simply:
    >>> Pe_est = sum(xor(x_bits,y_bits))/length(x_bits);

    Mark Wickert, March 2015
    """
    x_bits = 2*x_bits - 1 # convert from 0/1 to -1/1 signal values
    var_noise = 10**(-EBN0_dB/10)/2
    y_bits = x_bits + np.sqrt(var_noise)*np.random.randn(np.size(x_bits))

    # Make hard decisions
    y_bits = np.sign(y_bits) # -1/+1 signal values
    y_bits = (y_bits+1)/2 # convert back to 0/1 binary values
    return y_bits


def mux_pilot_blocks(IQ_data, Np):
    """
    Parameters
    ----------
    IQ_data : a 2D array of input QAM symbols with the columns
               representing the NF carrier frequencies and each
               row the QAM symbols used to form an OFDM symbol
    Np : the period of the pilot blocks; e.g., a pilot block is
               inserted every Np OFDM symbols (Np-1 OFDM data symbols
               of width Nf are inserted in between the pilot blocks.

    Returns
    -------
    IQ_datap : IQ_data with pilot blocks inserted

    See Also
    --------
    OFDM_tx

    Notes
    -----
    A helper function called by :func:`OFDM_tx` that inserts pilot block for use
    in channel estimation when a delay spread channel is present.
    """
    N_OFDM = IQ_data.shape[0]
    Npb = N_OFDM // (Np - 1)
    N_OFDM_rem = N_OFDM - Npb * (Np - 1)
    Nf = IQ_data.shape[1]
    IQ_datap = np.zeros((N_OFDM + Npb + 1, Nf), dtype=np.complex128)
    pilots = np.ones(Nf)  # The pilot symbol is simply 1 + j0
    for k in range(Npb):
        IQ_datap[Np * k:Np * (k + 1), :] = np.vstack((pilots,
                                                      IQ_data[(Np - 1) * k:(Np - 1) * (k + 1), :]))
    IQ_datap[Np * Npb:Np * (Npb + N_OFDM_rem), :] = np.vstack((pilots,
                                                               IQ_data[(Np - 1) * Npb:, :]))
    return IQ_datap


def OFDM_tx(IQ_data, Nf, N, Np=0, cp=False, Ncp=0):
    """
    Parameters
    ----------
    IQ_data : +/-1, +/-3, etc complex QAM symbol sample inputs
    Nf : number of filled carriers, must be even and Nf < N
    N : total number of carriers; generally a power 2, e.g., 64, 1024, etc
    Np : Period of pilot code blocks; 0 <=> no pilots
    cp : False/True <=> bypass cp insertion entirely if False
    Ncp : the length of the cyclic prefix

    Returns
    -------
    x_out : complex baseband OFDM waveform output after P/S and CP insertion

    See Also
    --------
    OFDM_rx

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import digitalcom as dc
    >>> x1,b1,IQ_data1 = dc.QAM_bb(50000,1,'16qam')
    >>> x_out = dc.OFDM_tx(IQ_data1,32,64)
    >>> plt.psd(x_out,2**10,1);
    >>> plt.xlabel(r'Normalized Frequency ($\omega/(2\pi)=f/f_s$)')
    >>> plt.ylim([-40,0])
    >>> plt.xlim([-.5,.5])
    >>> plt.show()

    """
    N_symb = len(IQ_data)
    N_OFDM = N_symb // Nf
    IQ_data = IQ_data[:N_OFDM * Nf]
    IQ_s2p = np.reshape(IQ_data, (N_OFDM, Nf))  # carrier symbols by column
    log.info(IQ_s2p.shape)
    if Np > 0:
        IQ_s2p = mux_pilot_blocks(IQ_s2p, Np)
        N_OFDM = IQ_s2p.shape[0]
        log.info(IQ_s2p.shape)
    if cp:
        x_out = np.zeros(N_OFDM * (N + Ncp), dtype=np.complex128)
    else:
        x_out = np.zeros(N_OFDM * N, dtype=np.complex128)
    for k in range(N_OFDM):
        buff = np.zeros(N, dtype=np.complex128)
        for n in range(-Nf // 2, Nf // 2 + 1):
            if n == 0:  # Modulate carrier f = 0
                buff[0] = 0  # This can be a pilot carrier
            elif n > 0:  # Modulate carriers f = 1:Nf/2
                buff[n] = IQ_s2p[k, n - 1]
            else:  # Modulate carriers f = -Nf/2:-1
                buff[N + n] = IQ_s2p[k, Nf + n]
        if cp:
            # With cyclic prefix
            x_out_buff = fft.ifft(buff)
            x_out[k * (N + Ncp):(k + 1) * (N + Ncp)] = np.concatenate((x_out_buff[N - Ncp:],
                                                                       x_out_buff))
        else:
            # No cyclic prefix included
            x_out[k * N:(k + 1) * N] = fft.ifft(buff)
    return x_out


def chan_est_equalize(z, Np, alpha, Ht=None):
    """

    This is a helper function for :func:`OFDM_rx` to unpack pilot blocks from
    from the entire set of received OFDM symbols (the Nf of N filled
    carriers only); then estimate the channel array H recursively,
    and finally apply H_hat to Y, i.e., X_hat = Y/H_hat
    carrier-by-carrier. Note if Np = -1, then H_hat = H, the true
    channel.

    Parameters
    ----------
    z : Input N_OFDM x Nf 2D array containing pilot blocks and OFDM data symbols.
    Np : The pilot block period; if -1 use the known channel impulse response input to ht.
    alpha : The forgetting factor used to recursively estimate H_hat
    Ht : The theoretical channel frquency response to allow ideal equalization provided Ncp is adequate.

    Returns
    -------
    zz_out : The input z with the pilot blocks removed and one-tap equalization applied to each of the Nf carriers.
    H : The channel estimate in the frequency domain; an array of length Nf; will return Ht if provided as an input.

    Examples
    --------
    >>> from sk_dsp_comm.digitalcom import chan_est_equalize
    >>> zz_out,H = chan_est_eq(z,Nf,Np,alpha,Ht=None)
    """
    N_OFDM = z.shape[0]
    Nf = z.shape[1]
    Npb = N_OFDM // Np
    N_part = N_OFDM - Npb * Np - 1
    zz_out = np.zeros_like(z)
    Hmatrix = np.zeros((N_OFDM, Nf), dtype=np.complex128)
    k_fill = 0
    k_pilot = 0
    for k in range(N_OFDM):
        if np.mod(k, Np) == 0:  # Process pilot blocks
            if k == 0:
                H = z[k, :]
            else:
                H = alpha * H + (1 - alpha) * z[k, :]
            Hmatrix[k_pilot, :] = H
            k_pilot += 1
        else:  # process data blocks
            if isinstance(type(None), type(Ht)):
                zz_out[k_fill, :] = z[k, :] / H  # apply equalizer
            else:
                zz_out[k_fill, :] = z[k, :] / Ht  # apply ideal equalizer
            k_fill += 1
    zz_out = zz_out[:k_fill, :]  # Trim to # of OFDM data symbols
    Hmatrix = Hmatrix[:k_pilot, :]  # Trim to # of OFDM pilot symbols
    if k_pilot > 0:  # Plot a few magnitude and phase channel estimates
        chan_idx = np.arange(0, Nf // 2, 4)
        plt.subplot(211)
        for i in chan_idx:
            plt.plot(np.abs(Hmatrix[:, i]))
        plt.title('Channel Estimates H[k] Over Selected Carrier Indices')
        plt.xlabel('Channel Estimate Update Index')
        plt.ylabel('|H[k]|')
        plt.grid();
        plt.subplot(212)
        for i in chan_idx:
            plt.plot(np.angle(Hmatrix[:, i]))
        plt.xlabel('Channel Estimate Update Index')
        plt.ylabel('angle[H[k] (rad)')
        plt.grid();
        plt.tight_layout()
    return zz_out, H


def OFDM_rx(x, Nf, N, Np=0, cp=False, Ncp=0, alpha=0.95, ht=None):
    """
    Parameters
    ----------
    x : Received complex baseband OFDM signal
    Nf : Number of filled carriers, must be even and Nf < N
    N : Total number of carriers; generally a power 2, e.g., 64, 1024, etc
    Np : Period of pilot code blocks; 0 <=> no pilots; -1 <=> use the ht impulse response input to equalize the OFDM symbols; note equalization still requires Ncp > 0 to work on a delay spread channel.
    cp : False/True <=> if False assume no CP is present
    Ncp : The length of the cyclic prefix
    alpha : The filter forgetting factor in the channel estimator. Typically alpha is 0.9 to 0.99.
    nt : Input the known theoretical channel impulse response

    Returns
    -------
    z_out : Recovered complex baseband QAM symbols as a serial stream; as appropriate channel estimation has been applied.
    H : channel estimate (in the frequency domain at each subcarrier)

    See Also
    --------
    OFDM_tx

    Examples
    --------

    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import digitalcom as dc
    >>> from scipy import signal
    >>> from numpy import array
    >>> hc = array([1.0, 0.1, -0.05, 0.15, 0.2, 0.05]) # impulse response spanning five symbols
    >>> # Quick example using the above channel with no cyclic prefix
    >>> x1,b1,IQ_data1 = dc.QAM_bb(50000,1,'16qam')
    >>> x_out = dc.OFDM_tx(IQ_data1,32,64,0,True,0)
    >>> c_out = signal.lfilter(hc,1,x_out) # Apply channel distortion
    >>> r_out = dc.cpx_AWGN(c_out,100,64/32) # Es/N0 = 100 dB
    >>> z_out,H = dc.OFDM_rx(r_out,32,64,-1,True,0,alpha=0.95,ht=hc)
    >>> plt.plot(z_out[200:].real,z_out[200:].imag,'.')
    >>> plt.xlabel('In-Phase')
    >>> plt.ylabel('Quadrature')
    >>> plt.axis('equal')
    >>> plt.grid()
    >>> plt.show()

    Another example with noise using a 10 symbol cyclic prefix and channel estimation:

    >>> x_out = dc.OFDM_tx(IQ_data1,32,64,100,True,10)
    >>> c_out = signal.lfilter(hc,1,x_out) # Apply channel distortion
    >>> r_out = dc.cpx_AWGN(c_out,25,64/32) # Es/N0 = 25 dB
    >>> z_out,H = dc.OFDM_rx(r_out,32,64,100,True,10,alpha=0.95,ht=hc);
    >>> plt.figure() # if channel estimation is turned on need this
    >>> plt.plot(z_out[-2000:].real,z_out[-2000:].imag,'.') # allow settling time
    >>> plt.xlabel('In-Phase')
    >>> plt.ylabel('Quadrature')
    >>> plt.axis('equal')
    >>> plt.grid()
    >>> plt.show()

    """
    N_symb = len(x) // (N + Ncp)
    y_out = np.zeros(N_symb * N, dtype=np.complex128)
    for k in range(N_symb):
        if cp:
            # Remove the cyclic prefix
            buff = x[k * (N + Ncp) + Ncp:(k + 1) * (N + Ncp)]
        else:
            buff = x[k * N:(k + 1) * N]
        y_out[k * N:(k + 1) * N] = fft.fft(buff)
    # Demultiplex into Nf parallel streams from N total, including
    # the pilot blocks which contain channel information
    z_out = np.reshape(y_out, (N_symb, N))
    z_out = np.hstack((z_out[:, 1:Nf // 2 + 1], z_out[:, N - Nf // 2:N]))
    if Np > 0:
        if isinstance(type(None), type(ht)):
            z_out, H = chan_est_equalize(z_out, Np, alpha)
        else:
            Ht = fft.fft(ht, N)
            Hht = np.hstack((Ht[1:Nf // 2 + 1], Ht[N - Nf // 2:]))
            z_out, H = chan_est_equalize(z_out, Np, alpha, Hht)
    elif Np == -1:  # Ideal equalization using hc
        Ht = fft.fft(ht, N)
        H = np.hstack((Ht[1:Nf // 2 + 1], Ht[N - Nf // 2:]))
        for k in range(N_symb):
            z_out[k, :] /= H
    else:
        H = np.ones(Nf)
    # Multiplex into original serial symbol stream
    return z_out.flatten(), H


def bin2gray(d_word,b_width):
    """
    Convert integer bit words to gray encoded binary words via
    Gray coding starting from the MSB to the LSB
    
    Mark Wickert November 2018
    """
    bits_in = to_bin(d_word,b_width)
    bits_out = np.zeros(b_width,dtype=np.int)
    for k, bit_k in enumerate(bits_in):
        if k > 0:
            bits_out[k] = bit_k^bits_in[k-1]
        else:
            bits_out[k] = bit_k
    return from_bin(bits_out)


def gray2bin(d_word,b_width):
    """
    Convert gray encoded binary words to integer bit words via
    Gray decoding starting from the MSB to the LSB
    
    Mark Wickert November 2018
    """
    bits_in = to_bin(d_word,b_width)
    bits_out = np.zeros(b_width,dtype=np.int)
    for k, bit_k in enumerate(bits_in):
        if k > 0:
            bits_out[k] = bit_k^bits_out[k-1]
        else:
            bits_out[k] = bit_k
    return from_bin(bits_out)


def QAM_gray_encode_bb(N_symb,Ns,M=4,pulse='rect',alpha=0.35,M_span=6,ext_data=None):
    """
    QAM_gray_bb: A gray code mapped QAM complex baseband transmitter 
    x,b,tx_data = QAM_gray_bb(K,Ns,M)
    
    Parameters
    ----------
    N_symb : The number of symbols to process
    Ns : Number of samples per symbol
    M : Modulation order: 2, 4, 16, 64, 256 QAM. Note 2 <=> BPSK, 4 <=> QPSK
    alpha : Square root raised cosine excess bandwidth factor.
            For DOCSIS alpha = 0.12 to 0.18. In general alpha can range over 0 < alpha < 1.
    pulse : 'rect', 'src', or 'rc'

    Returns
    -------
    x : Complex baseband digital modulation
    b : Transmitter shaping filter, rectangle or SRC
    tx_data : xI+1j*xQ = inphase symbol sequence + 1j*quadrature symbol sequence

    See Also
    --------
    QAM_gray_decode

    Examples
    --------
    
    
    
    """ 
    # Create a random bit stream then encode using gray code mapping
    # Gray code LUTs for 4, 16, 64, and 256 QAM
    # which employs M = 2, 4, 6, and 8 bits per symbol  
    bin2gray1 = [0,1]
    bin2gray2 = [0,1,3,2]
    bin2gray3 = [0,1,3,2,7,6,4,5] # arange(8) 
    bin2gray4 = [0,1,3,2,7,6,4,5,15,14,12,13,8,9,11,10]
    x_m = np.sqrt(M)-1
    # Create the serial bit stream [Ibits,Qbits,Ibits,Qbits,...], msb to lsb
    # except for the case M = 2
    if N_symb == None:
        # Truncate so an integer number of symbols is formed
        N_symb = int(np.floor(len(ext_data)/np.log2(M)))
        data = ext_data[:N_symb*int(np.log2(M))]
    else:
        data = np.random.randint(0,2,size=int(np.log2(M))*N_symb)
    x_IQ = np.zeros(N_symb,dtype=np.complex128)
    N_word = int(np.log2(M)/2)
    # binary weights for converting binary to decimal using dot()
    w = 2**np.arange(N_word-1,-1,-1)
    if M == 2: # Special case of BPSK for convenience
        x_IQ = 2*data - 1
        x_m = 1
    elif M == 4: # total constellation points
        for k in range(N_symb):
            wordI = data[2*k*N_word:(2*k+1)*N_word]
            wordQ = data[2*k*N_word+N_word:(2*k+1)*N_word+N_word]
            x_IQ[k] = (2*bin2gray1[np.dot(wordI,w)] - x_m) + \
                   1j*(2*bin2gray1[np.dot(wordQ,w)] - x_m)
    elif M == 16:
        for k in range(N_symb):
            wordI = data[2*k*N_word:(2*k+1)*N_word]
            wordQ = data[2*k*N_word+N_word:(2*k+1)*N_word+N_word]
            x_IQ[k] = (2*bin2gray2[np.dot(wordI,w)] - x_m) + \
                   1j*(2*bin2gray2[np.dot(wordQ,w)] - x_m)
    elif M == 64:
        for k in range(N_symb):
            wordI = data[2*k*N_word:(2*k+1)*N_word]
            wordQ = data[2*k*N_word+N_word:(2*k+1)*N_word+N_word]
            x_IQ[k] = (2*bin2gray3[np.dot(wordI,w)] - x_m) + \
                   1j*(2*bin2gray3[np.dot(wordQ,w)] - x_m)
    elif M == 256:
        for k in range(N_symb):
            wordI = data[2*k*N_word:(2*k+1)*N_word]
            wordQ = data[2*k*N_word+N_word:(2*k+1)*N_word+N_word]
            x_IQ[k] = (2*bin2gray4[np.dot(wordI,w)] - x_m) + \
                   1j*(2*bin2gray4[np.dot(wordQ,w)] - x_m)
    else:
        raise ValueError('M must be 2, 4, 16, 64, 256')        
    
    if Ns > 1:
        # Design the pulse shaping filter to be of duration 12 
        # symbols and fix the excess bandwidth factor at alpha = 0.35
        if pulse.lower() == 'src':
            b = sqrt_rc_imp(Ns,alpha,M_span)
        elif pulse.lower() == 'rc':
            b = rc_imp(Ns,alpha,M_span)    
        elif pulse.lower() == 'rect':
            b = np.ones(int(Ns)) #alt. rect. pulse shape
        else:
            raise ValueError('pulse shape must be src, rc, or rect')
        # Filter the impulse train signal
        x = signal.lfilter(b,1,upsample(x_IQ,Ns))
        # Scale shaping filter to have unity DC gain
        b = b/sum(b)
        return x/x_m, b, data
    else:
        return x_IQ/x_m, 1, data


def QAM_gray_decode(x_hat,M = 4):
    """
    Decode MQAM IQ symbols to a serial bit stream using
    gray2bin decoding
    
    x_hat = symbol spaced samples of the QAM waveform taken at the maximum
            eye opening. Normally this is following the matched filter
    
    Mark Wickert April 2018
    """
    # Inverse Gray code LUTs for 4, 16, 64, and 256 QAM
    # which employs M = 2, 4, 6, and 8 bits per symbol
    gray2bin1 = [0,1]
    gray2bin2 = [0,1,3,2]
    gray2bin3 = [0,1,3,2,6,7,5,4] # arange(8) 
    gray2bin4 = [0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8]
    x_m = np.sqrt(M)-1
    if M == 2: x_m = 1
    N_symb = len(x_hat)
    N_word = int(np.log2(M)/2)
    
    # Scale input up by x_m
    #x_hat = x_hat*x_m
    # Scale adaptively assuming var(x_hat) is proportional to 
    # signal power using a known relationship for QAM.
    x_hat = x_hat/(np.std(x_hat) * np.sqrt(3/(2*(M-1))))
    
    k_hat_gray = (x_hat + x_m*(1+1j))/2
    # Soft IQ symbol values are converted to hard symbol decisions
    k_hat_grayI = np.int16(np.clip(np.rint(k_hat_gray.real),0,x_m))
    k_hat_grayQ = np.int16(np.clip(np.rint(k_hat_gray.imag),0,x_m))
    data_hat = np.zeros(2*N_word*N_symb,dtype=int)
    # Create the serial bit stream [Ibits,Qbits,Ibits,Qbits,...], msb to lsb
    for k in range(N_symb):
        if M == 2: # special case for BPSK
            data_hat = k_hat_grayI
        elif M == 4: # total points of the square constellation
            data_hat[2*k*N_word:2*(k+1)*N_word] \
              = np.hstack((to_bin(gray2bin1[k_hat_grayI[k]],N_word),
                        to_bin(gray2bin1[k_hat_grayQ[k]],N_word)))
        elif M == 16:
            data_hat[2*k*N_word:2*(k+1)*N_word] \
              = np.hstack((to_bin(gray2bin2[k_hat_grayI[k]],N_word),
                        to_bin(gray2bin2[k_hat_grayQ[k]],N_word)))            
        elif M == 64:
            data_hat[2*k*N_word:2*(k+1)*N_word] \
              = np.hstack((to_bin(gray2bin3[k_hat_grayI[k]],N_word),
                        to_bin(gray2bin3[k_hat_grayQ[k]],N_word)))            
        elif M == 256:
            data_hat[2*k*N_word:2*(k+1)*N_word] \
              = np.hstack((to_bin(gray2bin4[k_hat_grayI[k]],N_word),
                        to_bin(gray2bin4[k_hat_grayQ[k]],N_word)))
        else:
            raise ValueError('M must be 2, 4, 16, 64, 256')  
            
    return data_hat


def MPSK_gray_encode_bb(N_symb,Ns,M=4,pulse='rect',alpha=0.35,M_span=6,ext_data=None):
    """
    MPSK_gray_bb: A gray code mapped MPSK complex baseband transmitter 
    x,b,tx_data = MPSK_gray_bb(K,Ns,M)

    //////////// Inputs //////////////////////////////////////////////////
      N_symb = the number of symbols to process
          Ns = number of samples per symbol
           M = modulation order: 2, 4, 8, 16 MPSK
       alpha = squareroot raised cosine excess bandwidth factor.
               Can range over 0 < alpha < 1.
       pulse = 'rect', 'src', or 'rc'
    //////////// Outputs /////////////////////////////////////////////////
           x = complex baseband digital modulation
           b = transmitter shaping filter, rectangle or SRC
     tx_data = xI+1j*xQ = inphase symbol sequence + 
               1j*quadrature symbol sequence

    Mark Wickert November 2018
    """ 
    # Create a random bit stream then encode using gray code mapping
    # Gray code LUTs for 2, 4, 8, 16, and 32 MPSK
    # which employs M = 1, 2, 3, 4, and 5  bits per symbol  
    bin2gray1 = [0,1]
    bin2gray2 = [0,1,3,2]
    bin2gray3 = [0,1,3,2,7,6,4,5] 
    bin2gray4 = [0,1,3,2,7,6,4,5,15,14,12,13,8,9,11,10]
    bin2gray5 = [0,1,3,2,7,6,4,5,15,14,12,13,8,9,11,10,31,30,
                 28,29,24,25,27,26,16,17,19,18,23,22,20,21]
    # Create the serial bit stream msb to lsb
    # except for the case M = 2
    N_word = int(np.log2(M))
    if N_symb == None:
        # Truncate so an integer number of symbols is formed
        N_symb = int(np.floor(len(ext_data)/N_word))
        data = ext_data[:N_symb*N_word]
    else:
        data = np.random.randint(0,2,size=int(np.log2(M))*N_symb)
    x_IQ = np.zeros(N_symb,dtype=np.complex128)
    # binary weights for converting binary to decimal using dot()
    bin_wgts = 2**np.arange(N_word-1,-1,-1)
    if M == 2: # Special case of BPSK for convenience
        x_IQ = 2*data - 1
    elif M == 4: # total constellation points
        for k in range(N_symb):
            word_phase = data[k*N_word:(k+1)*N_word]
            x_phase = 2*np.pi*bin2gray2[np.dot(word_phase,bin_wgts)]/M + np.pi/M
            x_IQ[k] = np.exp(1j*x_phase)
    elif M == 8:
        for k in range(N_symb):
            word_phase = data[k*N_word:(k+1)*N_word]
            x_phase = 2*np.pi*bin2gray3[np.dot(word_phase,bin_wgts)]/M
            x_IQ[k] = np.exp(1j*x_phase)
    elif M == 16:
        for k in range(N_symb):
            word_phase = data[k*N_word:(k+1)*N_word]
            x_phase = 2*np.pi*bin2gray4[np.dot(word_phase,bin_wgts)]/M
            x_IQ[k] = np.exp(1j*x_phase)
    elif M == 32:
        for k in range(N_symb):
            word_phase = data[k*N_word:(k+1)*N_word]
            x_phase = 2*np.pi*bin2gray5[np.dot(word_phase,bin_wgts)]/M
            x_IQ[k] = np.exp(1j*x_phase)
    else:
        raise ValueError('M must be 2, 4, 8, 16, or 32')        
    
    if Ns > 1:
        # Design the pulse shaping filter to be of duration 12 
        # symbols and fix the excess bandwidth factor at alpha = 0.35
        if pulse.lower() == 'src':
            b = sqrt_rc_imp(Ns,alpha,M_span)
        elif pulse.lower() == 'rc':
            b = rc_imp(Ns,alpha,M_span)    
        elif pulse.lower() == 'rect':
            b = np.ones(int(Ns)) #alt. rect. pulse shape
        else:
            raise ValueError('pulse shape must be src, rc, or rect')
        # Filter the impulse train signal
        x = signal.lfilter(b,1,upsample(x_IQ,Ns))
        # Scale shaping filter to have unity DC gain
        b = b/sum(b)
        return x, b, data
    else:
        return x_IQ, 1, data


def MPSK_gray_decode(x_hat,M = 4):
    """
    Decode MPSK IQ symbols to a serial bit stream using
    gray2bin decoding
    
    x_hat = symbol spaced samples of the MPSK waveform taken at the maximum
            eye opening. Normally this is following the matched filter
    
    Mark Wickert November 2018
    """
    # Inverse Gray code LUTs for 2, 4, 8, 16, and 32 MPSK
    # which employs M = 1, 2, 3, 4, and 5  bits per symbol
    gray2bin1 = [0,1]
    gray2bin2 = [0,1,3,2]
    gray2bin3 = [0,1,3,2,6,7,5,4] 
    gray2bin4 = [0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8]
    gray2bin5 = [0,1,3,2,6,7,5,4,12,13,15,14,10,11,9,8,24,25,
                 27,26,30,31,29,28,20,21,23,22,18,19,17,16]
    N_symb = len(x_hat)
    N_word = int(np.log2(M))
    
   
    # Soft IQ symbol angle values are converted to hard symbol decisions as 
    # decimal angles over the range [0, M-1]
    if M == 4:
        # For QPSK (M=4) rotate constellation angles to start at zero
        k_hat_gray_theta = np.mod(np.int64(np.rint(np.angle(x_hat *\
                           np.exp(-1j*np.pi/4))*M/2/np.pi)),M)
    else:
        #k_hat_gray_theta = np.mod(np.int64(np.rint(np.angle(x_hat)*M/2/np.pi)),M)
        k_hat_gray_theta = np.mod((np.rint(np.angle(x_hat)*M/2/np.pi)).astype(np.int),M)

    data_hat = np.zeros(N_symb*N_word,dtype=int)
    # Create the serial bit stream using Gray decoding, msb to lsb
    for k in range(N_symb):
        if M == 2: # special case for BPSK
            data_hat[k] = k_hat_gray_theta[k]
        elif M == 4: # total points of the square constellation
            data_hat[k*N_word:(k+1)*N_word] \
              = to_bin(gray2bin2[k_hat_gray_theta[k]],N_word)
        elif M == 8:
            data_hat[k*N_word:(k+1)*N_word] \
              = to_bin(gray2bin3[k_hat_gray_theta[k]],N_word)            
        elif M == 16:
            data_hat[k*N_word:(k+1)*N_word] \
              = to_bin(gray2bin4[k_hat_gray_theta[k]],N_word)            
        elif M == 32:
            data_hat[k*N_word:(k+1)*N_word] \
              = to_bin(gray2bin5[k_hat_gray_theta[k]],N_word)
        else:
            raise ValueError('M must be 2, 4, 8, 16, or 32')  
    return data_hat


def MPSK_BEP_thy(SNR_dB, M, EbN0_Mode = True):
    """
    Approximate the bit error probability of MPSK assuming Gray encoding
    
    Mark Wickert November 2018
    """
    if EbN0_Mode:
        EsN0_dB = SNR_dB + 10*np.log10(np.log2(M))
    else:
        EsN0_dB = SNR_dB
    Symb2Bits = np.log2(M)
    if M == 2:
        BEP = Q_fctn(np.sqrt(2*10**(EsN0_dB/10)))
    else:
        SEP = 2*Q_fctn(np.sqrt(2*10**(EsN0_dB/10))*np.sin(np.pi/M))
        BEP = SEP/Symb2Bits
    return BEP 


def QAM_BEP_thy(SNR_dB,M,EbN0_Mode = True):
    """
    Approximate the bit error probability of QAM assuming Gray encoding
    
    Mark Wickert November 2018
    """
    if EbN0_Mode:
        EsN0_dB = SNR_dB + 10*np.log10(np.log2(M))
    else:
        EsN0_dB = SNR_dB
    if M == 2:
        BEP = Q_fctn(np.sqrt(2*10**(EsN0_dB/10)))
    elif M > 2:
        SEP = 4*(1 - 1/np.sqrt(M))*Q_fctn(np.sqrt(3/(M-1)*10**(EsN0_dB/10)))
        BEP = SEP/np.log2(M)
    return BEP


