from matplotlib import pyplot as plt, rcParams as mpl_rcParams
import numpy as np
from scipy import signal

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
    f_nn: np.ndarray = np.arange(0, fe / 2, fe / n)
    fir_freq_fz, fir_h_dft_fz = signal.freqz(b=fir_h, a=1, worN=NombreEchantillons, fs=fe)

    plt.subplot(3, 1, 1)
    plt.plot(fir_h, label="FIR")
    plt.title("Réponses impulsionnelles des filtres")
    plt.xlabel("n")
    plt.ylabel("Amplitude normalisée")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.semilogx(fir_freq_fz, 20 * np.log10(np.abs(fir_h_dft_fz)), label=Label_Graph)
    if(n == 256):
        plt.semilogx(f_nn, 20 * np.log10(np.abs(fir_h_dft_tf[0: n // 2])), label="TF")
    plt.ylim(top=10, bottom=-45)
    plt.title("Fonctions de transfert harmoniques du filtre FIR")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.legend()

    fir_h_dft_tf *= 2**13

    return fir_h_dft_tf

def main():
    # Propriétés par défaut de matplotlib
    plt.rcParams.update(
        {
            "backend": "TkAgg",
            "axes.grid": True,
            "axes.grid.which": "both",
            "figure.autolayout": True,
            "interactive": True,
        }
    )
    plt.figure()

    n: int = 256        #Ordre
    fc: float = 500     #Frequence coupure
    fe: float = 20000   #frequence echantillon
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

    with open("OUT.h", "w") as fd:
        fd.write(f"#define H_and_W_QXY_RES_NBITS 13 // Q2.13\n// Lowpass filter (blackman window), fc = 500 Hz, fe = 20000 Hz\nconst int32c H7[FFT_LEN] = {{\n")
        for a in H7:
            fd.write(f"{{{int(np.round(a.real))},{int(np.round(a.imag))}}},\n")
        fd.write("};\n")
        fd.write(f"// Bandpass filter, fcLow = 500 Hz,fcHigh = 1500 Hz, fe = 20000 Hz\nconst int32c H6[FFT_LEN] = {{\n")
        for b in H6:
            fd.write(f"{{{int(np.round(b.real))},{int(np.round(b.imag))}}},\n")
        fd.write("};\n")
        fd.write(f"// Bandpass filter, fcLow = 1500 Hz,fcHigh = 2500 Hz, fe = 20000 Hz\nconst int32c H5[FFT_LEN] = {{\n")
        for c in H5:
            fd.write(f"{{{int(np.round(c.real))},{int(np.round(c.imag))}}},\n")
        fd.write("};\n")
        fd.write(f"// Bandpass filter, fcLow = 2500 Hz,fcHigh = 4500 Hz, fe = 20000 Hz\nconst int32c H4[FFT_LEN] = {{\n")
        for d in H4:
            fd.write(f"{{{int(np.round(d.real))},{int(np.round(d.imag))}}},\n")
        fd.write("};\n")
        fd.write(f"// Highpass filter, fc = 4490 Hz, fe = 20000 Hz\nconst int32c H3[FFT_LEN] = {{\n")
        for e in H3:
            fd.write(f"{{{int(np.round(e.real))},{int(np.round(e.imag))}}},\n")
        fd.write("};\n")

    #plt.show()

    print('Whats up Bro')

if __name__ == "__main__":
    main()