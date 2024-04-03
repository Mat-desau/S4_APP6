# Libraries requises
from matplotlib import pyplot as plt, rcParams as mpl_rcParams
import numpy as np
from scipy import signal
def calcul_des_filtres(n: int, fc: float, fe: float):
    """
    Réponses impulsionnelles et fonctions de transfert des filtres FIR et IIR
    """
    # Sinusoïde à 200 Hz, rallongée à longueur 2N par "zero‐padding"
    f_sig: float = 200
    x200: np.ndarray = np.sin(2 * np.pi * np.arange(n) * f_sig / fe)
    x200_zero_pad: np.ndarray = np.append(x200, np.zeros(len(x200)))
    plt.figure()
    plt.plot(np.arange(len(x200_zero_pad)) / fe, x200_zero_pad)
    plt.plot(np.arange(len(x200)) / fe, x200)
    plt.title(f"Signal sinusoïdal à {f_sig} Hz doublé en longueur par zero‐padding")
    plt.xlabel("Temps (s)")
    plt.ylabel("Amplitude normalisée")
    # Filtre FIR: réponse impulsionnelle d'ordre N‐1 à fréquence de coupure fc
    fir_h: np.ndarray = signal.firwin(
        numtaps=n, cutoff=fc, pass_zero="lowpass", window="hamming", fs=fe
    )
    # Filtre FIR: fonctions de transfert harmoniques ("h_dft_*") calculées
    # par freqz() et explicitement par TF pour comparer. Dans l'appel de freqz()
    # pour un FIR, notez les bi qui sont les coefficients de la réponse
    # impulsionnelle et qu’il n’y a qu’un seul coefficient aj (a0 = 1),
    # ainsi que l'usage du paramètre worN pour augmenter la résolution du spectre.
    fir_freq_fz, fir_h_dft_fz = signal.freqz(b=fir_h, a=1, worN=10000, fs=fe)
    fir_h_dft_tf: np.ndarray = np.fft.fft(fir_h)
    # Filtre IIR d’ordre 4: coefficients a & b de l'équation aux différences
    # et calcul de sa réponse impulsionnelle tronquée (N premiers échantillons)
    [b, a] = signal.butter(N=4, Wn=fc, btype="low", fs=fe, output="ba")
    imp: np.ndarray = signal.unit_impulse(n)
    iir_h: np.ndarray = signal.lfilter(b=b, a=a, x=imp)
    # Filtre IIR: fonctions de transfert harmoniques ("h_dft_*") du filtre IIR
    # par freqz() et explicitement par TF (h tronqué) pour comparer
    freq_iir_fz, h_dft_iir_fz = signal.freqz(b=b, a=a, worN=10000, fs=fe)
    h_dft_iir_tf: np.ndarray = np.fft.fft(iir_h)
    # Graphiques des réponses impulsionnelles des filtres. Rremarquez que
    # le filtre FIR est causal versus le filtre IIR qui est non‐causal et déphasé
    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(fir_h, label="FIR")
    plt.plot(iir_h, label="IIR")
    plt.title("Réponses impulsionnelles des filtres")
    plt.xlabel("n")
    plt.ylabel("Amplitude normalisée")
    plt.legend()

    # Graphiques des fonctions de transfert harmoniques du filtre FIR (freqz & TF).
    # Dans le cas de la TF, afin d'extraire les valeurs du spectre aux fréquences
    # non‐négatives seulement, remarquez l'usage de la division avec
    # troncature "//" pour générer un nombre entier tel que requis pour des
    # indices de tableaux (une simple division avec "/" aurait causé une erreur).
    # Notez aussi la résolution accrue avec freqz() grace au paramètre worN.
    f_nn: np.ndarray = np.arange(0, fe / 2, fe / n)
    plt.subplot(3, 1, 2)
    plt.semilogx(fir_freq_fz, 20 * np.log10(np.abs(fir_h_dft_fz)), label="freqz()")
    plt.semilogx(f_nn, 20 * np.log10(np.abs(fir_h_dft_tf[0: n // 2])), label="TF")
    plt.ylim(top=10, bottom=-200)
    plt.title("Fonctions de transfert harmoniques du filtre FIR")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.legend()
    # Graphiques des fonctions de transfert harmoniques du filtre IIR (freqz & TF)
    # aux fréquences non‐négatives seulement.
    plt.subplot(3, 1, 3)
    plt.semilogx(freq_iir_fz, 20 * np.log10(np.abs(h_dft_iir_fz)), label="freqz()")
    plt.semilogx(f_nn, 20 * np.log10(np.abs(h_dft_iir_tf[0: n // 2])), label="TF")
    plt.ylim(top=10, bottom=-200)
    plt.title("Fonctions de transfert harmoniques du filtre IIR")
    plt.xlabel("Fréquence [Hz]")
    plt.ylabel("Gain [dB]")
    plt.legend()
    plt.show()

def code_exemple_guide_etudiant():
    """
    Fonction principale appelant les fonctions secondaires (e.g. main() en C++)
    """
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
    # Appel des fonctions spécifiques
    n: int = 1024
    fc: float = 100
    fe: float = 22100
    calcul_des_filtres(n, fc, fe)

    # Breakpoint pour mettre l'interpréteur en pause afin d’afficher les figures
    print("Done!")


if __name__ == "__main__":
    code_exemple_guide_etudiant()