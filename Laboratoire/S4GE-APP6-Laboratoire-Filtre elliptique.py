import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from zplane import zplane


def probleme_1(fe: float):
    """
    Problème 1: Filtre IIR elliptique
    """

    # Filter specifications
    fc_low: float = 900
    fc_high: float = 1100
    filter_order: int = 2
    pass_band_ripple_db: float = 1
    stop_band_attn_db: float = 40

    # Filter coefficients
    [b, a] = signal.ellip(
        N=filter_order,
        rp=pass_band_ripple_db,
        rs=stop_band_attn_db,
        Wn=[fc_low, fc_high],
        fs=fe,
        btype="bandpass",
        output="ba",
    )

    # Frequency response
    [w, h_dft] = signal.freqz(b, a, worN=10000, fs=fe)
    plt.figure()
    plt.semilogx(w, 20 * np.log10(np.abs(h_dft)))
    plt.title(f"Réponse en fréquence du filtre elliptique (ordre {filter_order})")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.grid(which="both", axis="both")
    plt.tight_layout()

    #Numero 2
    plt.figure()
    zplane(b, a)

    # Numero 3
    Impulse = signal.unit_impulse(1000)
    Z = signal.lfilter(b, a, Impulse)
    plt.figure()
    plt.plot(Z)
    plt.grid(color='grey')
    plt.title('Réponse impulsionnelle du filtre elliptique')
    plt.xlabel('n')
    plt.ylabel('Amplitude')

    #Numero 4
    sos = signal.ellip(N=2, rp=pass_band_ripple_db, rs=stop_band_attn_db, Wn=[fc_low, fc_high], fs=fe, btype="bandpass", output="sos")
    [wsos, h_dftsos] = signal.sosfreqz(sos, worN=10000, fs=fe)
    plt.figure()
    plt.semilogx(wsos, 20 * np.log10(np.abs(h_dftsos)), label='Normal', color='red')

    #Numero 5
    a_Q = np.round(a*2**13)
    b_Q = np.round(b*2**13)
    sos_Q = np.round(sos*2**13)

    a_Q = a_Q * 2**(-13)
    b_Q = b_Q * 2 ** (-13)
    sos_Q = sos_Q * 2 ** (-13)

    [wsos_Q, h_dftsos_Q] = signal.sosfreqz(sos_Q, worN=100000, fs=fe)
    plt.semilogx(wsos_Q, 20 * np.log10(np.abs(h_dftsos_Q)), label='SOS Q2.13', color='blue')

    [w_Q, h_dft_Q] = signal.freqz(b_Q, a_Q, worN=10000, fs=fe)
    plt.semilogx(w_Q, 20 * np.log10(np.abs(h_dft_Q)), label='a&b Q2.13', color='green')

    plt.legend()
    plt.title('Réponses en fréquence de filtre elliptique')
    plt.xlabel('Fréquence [Hz]')
    plt.ylabel('Gain [dB]')
    plt.grid()

    #Question B
    #Numero 1
    N = 512
    N = N-1
    fir_low_h = signal.firwin(numtaps=N, cutoff=1000, fs=fe, pass_zero="lowpass", window="hamming")
    fir_high_h = signal.firwin(numtaps=N, cutoff=950, fs=fe, pass_zero="highpass", window="hamming")

    plt.figure()
    Figure, (SUB1, SUB2) = plt.subplots(2, 1)
    SUB1.plot(fir_low_h)
    SUB1.set_title('Filtre passe-bas - Réponse impulsionelle')
    SUB1.set_xlabel('n')
    SUB1.set_ylabel('Amplitude')
    SUB2.plot(fir_high_h)
    SUB2.set_title('Filtre passe-haut - Réponse impulsionelle')
    SUB2.set_xlabel('n')
    SUB2.set_ylabel('Amplitude')
    #Numero 2
    while(len(fir_low_h) < 4*N):
        fir_low_h = np.append(fir_low_h, 0)
        fir_high_h = np.append(fir_high_h, 0)

    fft_low = np.fft.fft(fir_low_h)
    fft_high = np.fft.fft(fir_high_h)

    fft_low = fft_low[int(len(fft_low) / 2):]
    fft_high = fft_high[int(len(fft_high) / 2):]
    fft_freq_high = np.fft.fftfreq(len(fft_high)) * fe
    fft_freq_low = np.fft.fftfreq(len(fft_low)) * fe

    fft_low = 20*np.log10(np.abs(fft_low))
    fft_high = 20 * np.log10(np.abs(fft_high))


    plt.figure()
    Figure, (SUB1, SUB2) = plt.subplots(2, 1)
    SUB1.semilogx(fft_freq_low, fft_low)
    SUB1.semilogx(fft_freq_high, fft_high)
    SUB1.set_title('Réponses en fréquence des filtres FIR passe-bas et passe-haut')
    SUB1.set_xlabel('Frequence [Hz]')
    SUB1.set_ylabel('Gain [dB]')
    SUB2.set_title('Total des réponses en fréquence des deux filtres')
    SUB2.set_xlabel('Frequence [Hz]')
    SUB2.set_ylabel('Gain [dB]')

    print('yo')

def laboratoire():
    plt.ion()  # Comment out if using scientific mode!

    fe = 20000
    probleme_1(fe)
    print("Done!")


if __name__ == "__main__":
    laboratoire()
