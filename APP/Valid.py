from matplotlib import pyplot as plt
import numpy as np
from scipy import signal

pi = np.pi
def MiseLog(Valeur):
    return 20*np.log10(Valeur)
def A2_A3():
    fe = 20000
    nombre_n = 768

    han = np.hanning(nombre_n)

    # Sinusoïde à 200 Hz, rallongée à longueur 2N par "zero‐padding"
    f_sig = 2000

    x2000 = np.sin(2 * np.pi * np.arange(nombre_n) * f_sig / fe)

    fnn = np.arange(0, fe, fe/nombre_n)

    x2000_han = x2000 * han
    FFT = np.fft.fft(x2000, n=nombre_n)
    FFT_han = np.fft.fft(x2000_han, n=nombre_n)

    Figure, [SUB1, SUB2, SUB3] = plt.subplots(3, 1)
    SUB1.plot(np.arange(len(x2000)) / fe, x2000)
    SUB1.set_title(f"Signal sinusoïdal à {f_sig} Hz")
    SUB1.set_xlabel("Temps (s)")
    SUB1.set_ylabel("Amplitude normalisée")

    SUB2.plot(fnn, MiseLog(FFT), label='Fenêtre Rectangulaire')
    SUB2.plot(fnn, MiseLog(FFT_han), label='Fenêtre Hanning')
    SUB2.set_title(f"Spectre de la sinus de {f_sig} Hz")
    SUB2.set_xlabel("Fréquence [k]")
    SUB2.set_ylabel("Amplitude normalisée")
    SUB2.legend()

    SUB3.semilogx(fnn, MiseLog(FFT), label='Fenêtre Rectangulaire')
    SUB3.semilogx(fnn, MiseLog(FFT_han), label='Fenêtre Hanning')
    SUB3.set_title(f"Spectre de la sinus de {f_sig} Hz")
    SUB3.set_xlabel("Fréquence [k]")
    SUB3.set_ylabel("Amplitude normalisée")
    SUB3.legend()

def H3_a_H7():
    plt.figure()

    n: int = 256  # Ordre
    fc: float = 500  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H7 = calcul_des_filtres(n, fc, fe, 'H7: lowpass (fc = 500Hz)', "lowpass")

    n: int = 256  # Ordre
    fc: float = [500, 1500]  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H6 = calcul_des_filtres(n, fc, fe, 'H6: bandpass (fc = 1000Hz)', "bandpass")

    n: int = 256  # Ordre
    fc: float = [1500, 2500]  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H5 = calcul_des_filtres(n, fc, fe, 'H5: bandpass (fc = 2000Hz)', "bandpass")

    n: int = 256  # Ordre
    fc: float = [2500, 4500]  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H4 = calcul_des_filtres(n, fc, fe, 'H4: bandpass (fc = 3500Hz)', "bandpass")

    n: int = 255  # Ordre
    fc: float = 4490  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H3 = calcul_des_filtres(n, fc, fe, 'H3: highpass (fc = 4490Hz)', "highpass")

def calcul_des_filtres(n: int, fc: float, fe: float, Label_Graph, type):
    NombreEchantillons: int = 1024  # Nombre echantillon

    # Filtre FIR: réponse impulsionnelle d'ordre N‐1 à fréquence de coupure fc
    fir_h: np.ndarray = signal.firwin(numtaps=n, cutoff=fc, pass_zero=type, window="blackman", fs=fe)
    fir_h_dft_tf: np.ndarray = np.fft.fft(fir_h, n=1024)

    # Filtre FIR: fonctions de transfert harmoniques ("h_dft_*") calculées
    # par freqz() et explicitement par TF pour comparer. Dans l'appel de freqz()
    # pour un FIR, notez les bi qui sont les coefficients de la réponse
    # impulsionnelle et qu’il n’y a qu’un seul coefficient aj (a0 = 1),
    # ainsi que l'usage du paramètre worN pour augmenter la résolution du spectre.
    f_nn: np.ndarray = np.arange(0, fe / 2, fe / NombreEchantillons)
    fir_freq_fz, fir_h_dft_fz = signal.freqz(b=fir_h, a=1, worN=NombreEchantillons, fs=fe)

    plt.subplot(3, 1, 1)
    plt.plot(fir_h, label=Label_Graph)
    plt.title("Réponses impulsionnelles des filtres")
    plt.xlabel("n")
    plt.ylabel("Amplitude normalisée")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.semilogx(fir_freq_fz, 20 * np.log10(np.abs(fir_h_dft_fz)), label=Label_Graph)
    #if(n == 256):
        #plt.semilogx(f_nn, 20 * np.log10(np.abs(fir_h_dft_tf[0: n // 2])), label="TF")
    plt.ylim(top=10, bottom=-45)
    plt.xlim(left=10, right=10000)
    plt.title("Freqz")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.semilogx(f_nn, 20 * np.log10(np.abs(fir_h_dft_tf[0: NombreEchantillons // 2])), label=Label_Graph)
    plt.ylim(top=10, bottom=-45)
    plt.xlim(left=10, right=10000)
    plt.title("FFT (TF)")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.legend()

    fir_h_dft_tf *= 2**13
    fir_h_dft_fz *= 2 ** 13

    return fir_h_dft_tf
def main():
    # Propriétés par défaut de matplotlib
    plt.rcParams.update(
        {   "backend": "TkAgg",
            "axes.grid": True,
            "axes.grid.which": "both",
            "figure.autolayout": True,
            "interactive": True,
        }
    )

    A2_A3()
    #H3_a_H7()

    print('BreakPoint')

if __name__ == "__main__":
    main()