from matplotlib import pyplot as plt
import numpy as np
from scipy import signal

pi = np.pi

#Valid
Filtres_Tout_Les_H = True
Filtre_IIR_Test_Sans_int8 = True
Reponse_Frequence_IIR = True

#Autres
FFT_FIR_Different_Q = False
Graphique_Test_H4 = False
Reponse_Frequentiel_sans_signal = False
FFT_B0_B1 = False
Graph_Fenetrage = False

def MiseLog(Valeur):
    return 20*np.log10(np.abs(Valeur))

def MiseQ15(Valeur):
    Valeur *= 2**15
    Valeur = np.round(Valeur)
    return Valeur.astype(int)

def Q2_28_to_Q15(Valeur):
    Temp = Valeur * (2 ** (-13))
    Temp = Temp.astype(np.int16)
    return Temp

def Q2_20_to_Q15(Valeur):
    Temp = Valeur * (2 ** (-5))
    Temp = Temp.astype(np.int16)
    return Temp

def Calcul(Sinus, sos, Q_2_13):
    OUT1 = np.zeros_like(Sinus)
    IIRv1 = np.zeros(4)
    IIRu1 = np.zeros(4)
    count = 0

    for i in range(len(Sinus)):
        X1 = Sinus[i]
        for nSOS in range(0, 4):
            Y1 = (sos[nSOS][0] * X1) + IIRv1[nSOS]

            if(Q_2_13):
                Y1 = Q2_28_to_Q15(Y1)
            if (Q_2_13 == False):
                Y1 = Q2_20_to_Q15(Y1)

            IIRv1[nSOS] = (sos[nSOS][1] * X1) - (sos[nSOS][4] * Y1) + IIRu1[nSOS]

            IIRu1[nSOS] = (sos[nSOS][2] * X1) - (sos[nSOS][5] * Y1)

            X1 = Y1

        OUT1[count] = Y1
        count += 1

    return OUT1

def Cree_Sin(f_sig, fe, n, fois):
    Temp = fois * np.sin(2 * np.pi * np.arange(n) * f_sig / fe)
    return MiseQ15(Temp)

def calcul_des_filtres(n: int, fc: float, fe: float, Label_Graph, type, fois):
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
    if (Reponse_Frequentiel_sans_signal):
        plt.subplot(3, 1, 1)
        plt.plot(fir_h, label=Label_Graph)
        plt.title("Réponses impulsionnelles des filtres")
        plt.xlabel("n")
        plt.ylabel("Amplitude normalisée")
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.semilogx(fir_freq_fz, 20 * np.log10(np.abs(fir_h_dft_fz)), label=Label_Graph)
        if(n == 256):
            plt.semilogx(f_nn, 20 * np.log10(np.abs(fir_h_dft_tf[0: n // 2])), label="TF")
        plt.ylim(top=10, bottom=-45)
        plt.xlim(left=10, right=10000)
        plt.title("Freqz")
        plt.xlabel("Fréquence [Hz]")
        plt.ylabel("Gain [dB]")
        plt.legend()

        plt.subplot(1, 1, 1)
        plt.semilogx(f_nn, 20 * np.log10(np.abs(fir_h_dft_tf[0: NombreEchantillons // 2])), label=Label_Graph)
        plt.ylim(top=10, bottom=-20)
        plt.xlim(left=10, right=10000)
        plt.title("FFT (TF)")
        plt.xlabel("Fréquence [Hz]")
        plt.ylabel("Gain [dB]")
        plt.legend()

    fir_h_dft_tf *= 2**fois
    fir_h_dft_fz *= 2**fois

    fir_h_dft_fz = np.round(fir_h_dft_fz)
    fir_h_dft_tf = np.round(fir_h_dft_tf)

    return fir_h_dft_tf.astype(np.int32)

def Fenetrage():
    fe = 20000
    nombre_n = 768
    divise = fe / 1024
    han = np.hanning(nombre_n)

    # Sinusoïde à 200 Hz, rallongée à longueur 2N par "zero‐padding"
    f_sig = 2000

    x2000 = np.sin(2 * np.pi * np.arange(nombre_n) * f_sig / fe)

    fnn = np.arange(0, fe, fe/1024)

    x2000_han = x2000 * han

    FFT = np.fft.fft(x2000, n=1024)
    FFT_han = np.fft.fft(x2000_han, n=1024)

    if(Graph_Fenetrage):
        Figure, [SUB1, SUB2, SUB3] = plt.subplots(3, 1)
        Figure.suptitle('Graphiques A2 & A3')
        SUB1.plot(np.arange(len(x2000)) / fe, x2000)
        SUB1.set_title(f"Signal sinusoïdal à {f_sig} Hz")
        SUB1.set_xlabel("Temps (s)")
        SUB1.set_ylabel("Amplitude normalisée")

        SUB2.plot(fnn/divise, MiseLog(FFT), label='Fenêtre Rectangulaire')
        SUB2.plot(fnn/divise, MiseLog(FFT_han), label='Fenêtre Hanning')
        SUB2.set_title(f"Spectre de la sinus de {f_sig} Hz")
        SUB2.set_xlabel("Nombre d'échantillons (N)")
        SUB2.set_ylabel("Amplitude normalisée")
        SUB2.legend()

        SUB3.semilogx(fnn, MiseLog(FFT), label='Fenêtre Rectangulaire')
        SUB3.semilogx(fnn, MiseLog(FFT_han), label='Fenêtre Hanning')
        SUB3.set_title(f"Spectre de la sinus de {f_sig} Hz")
        SUB3.set_xlabel("Fréquence [k] (log)")
        SUB3.set_ylabel("Amplitude normalisée (dB)")
        SUB3.legend()

def FIR():
    if(Reponse_Frequentiel_sans_signal):
        plt.figure()

    n: int = 256  # Ordre
    fc: float = 500  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H7 = calcul_des_filtres(n, fc, fe, 'H7: lowpass (fc = 500Hz)', "lowpass", 13)
    H7_5 = calcul_des_filtres(n, fc, fe, 'H7_5: lowpass (fc = 500Hz)', "lowpass", 5)

    n: int = 256  # Ordre
    fc: float = [500, 1500]  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H6 = calcul_des_filtres(n, fc, fe, 'H6: bandpass (fc = 1000Hz)', "bandpass", 13)
    H6_5 = calcul_des_filtres(n, fc, fe, 'H6_5: bandpass (fc = 1000Hz)', "bandpass", 5)

    n: int = 256  # Ordre
    fc: float = [1500, 2500]  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H5 = calcul_des_filtres(n, fc, fe, 'H5: bandpass (fc = 2000Hz)', "bandpass", 13)
    H5_5 = calcul_des_filtres(n, fc, fe, 'H5_5: bandpass (fc = 2000Hz)', "bandpass", 5)

    n: int = 256  # Ordre
    fc: float = [2500, 4500]  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H4 = calcul_des_filtres(n, fc, fe, 'H4: bandpass (fc = 3500Hz)', "bandpass", 13)
    H4_5 = calcul_des_filtres(n, fc, fe, 'H4: bandpass (fc = 3500Hz)', "bandpass", 5)

    n: int = 255  # Ordre
    fc: float = 4490  # Frequence coupure
    fe: float = 20000  # frequence echantillon
    H3 = calcul_des_filtres(n, fc, fe, 'H3: highpass (fc = 4490Hz)', "highpass", 13)
    H3_5 = calcul_des_filtres(n, fc, fe, 'H3: highpass (fc = 4490Hz)', "highpass", 5)

    Htot = H7 + H6 + H5 + H4 + H3
    Htot_5 = H7_5 + H6_5 + H5_5 + H4_5 + H3_5

    x2000 = Cree_Sin(2000, 20000, 1024, 0.02)
    x1500 = Cree_Sin(1500, 20000, 1024, 0.05)
    x3500 = Cree_Sin(3500, 20000, 1024, 0.05)
    x5500 = Cree_Sin(5500, 20000, 1024, 0.05)
    fnn = np.arange(0, fe, fe / 1024)

    FFT = np.fft.fft(x2000, n=1024)
    FFT_1500 = np.fft.fft(x1500, n=1024)
    FFT_3500 = np.fft.fft(x3500, n=1024)
    FFT_5500 = np.fft.fft(x5500, n=1024)

    FFT_H7 = Q2_28_to_Q15(FFT * H7)
    FFT_H6 = Q2_28_to_Q15(FFT * H6)
    FFT_H5 = Q2_28_to_Q15(FFT * H5)
    FFT_H4 = Q2_28_to_Q15(FFT * H4)
    FFT_H3 = Q2_28_to_Q15(FFT * H3)

    FFT_H4_OVER = Q2_28_to_Q15(FFT_5500 * H4)
    FFT_H4_UNDER = Q2_28_to_Q15(FFT_1500 * H4)
    FFT_H4_COUPURE = Q2_28_to_Q15(FFT_3500 * H4)

    FFT_Filtrer_Q2_28 = FFT * Htot                                                            #En Q2.28
    FFT_Filtrer_Q2_20 = FFT * Htot_5

    FFT_Filtrer_Q15 = Q2_28_to_Q15(FFT_Filtrer_Q2_28)

    iFFT_Q2_28 = np.fft.ifft(FFT_Filtrer_Q2_28)
    iFFT_Q2_20 = np.fft.ifft(FFT_Filtrer_Q2_20)
    iFFT_Q15 = np.fft.ifft(FFT_Filtrer_Q15)

    if(Graphique_Test_H4):
        Figure, [SUB1, SUB2] = plt.subplots(2, 1)
        Figure.suptitle('Graphiques Test H4')
        SUB1.plot(MiseLog(FFT_H4_OVER), label='f > fc')
        SUB1.plot(MiseLog(FFT_H4_UNDER), label='f < fc')
        SUB1.plot(MiseLog(FFT_H4_COUPURE), label='f = fc')
        SUB1.set_title('FFT')
        SUB1.set_ylabel('Amplitude (dB)')
        SUB1.set_xlabel('Nombre d\'échantillons [k]')
        SUB1.legend()

        SUB2.semilogx(fnn, MiseLog(FFT_H4_OVER), label='f > fc')
        SUB2.semilogx(fnn, MiseLog(FFT_H4_UNDER), label='f < fc')
        SUB2.semilogx(fnn, MiseLog(FFT_H4_COUPURE), label='f = fc')
        SUB2.set_title('FFT')
        SUB2.set_ylabel('Amplitude (dB)')
        SUB2.set_xlabel('Fréquence (Hz)')
        SUB2.legend()

    if(FFT_B0_B1):
        Figure, [SUB1, SUB2] = plt.subplots(2, 1)
        Figure.suptitle('Graphiques B0 & B1')
        SUB1.plot(MiseLog(FFT))
        SUB1.set_title('FFT')
        SUB1.set_ylabel('Amplitude (dB)')
        SUB1.set_xlabel('Nombre d\'échantillons [k]')

        SUB2.semilogx(fnn, MiseLog(FFT))
        SUB2.set_title('FFT')
        SUB2.set_ylabel('Amplitude (dB)')
        SUB2.set_xlabel('Fréquence (Hz)')

    if(FFT_FIR_Different_Q):
        Figure, [SUB1, SUB2, SUB3] = plt.subplots(3, 1)
        Figure.suptitle('Graphiques B2 avec Q différents')
        SUB1.plot(MiseLog(FFT))
        SUB1.set_title('FFT')
        SUB1.set_ylabel('Amplitude (dB)')
        SUB1.set_xlabel('Nombre d\'échantillons [k]')

        SUB2.plot(MiseLog(FFT_Filtrer_Q2_28), label='Q2.28', color='red')
        SUB2.plot(MiseLog(FFT_Filtrer_Q2_20), label='Q2.20', color='blue')
        SUB2.set_title('FFT avec les filtres')
        SUB2.set_ylabel('Amplitude (dB)')
        SUB2.set_xlabel('Nombre d\'échantillons [k]')
        SUB2.legend()

        SUB3.semilogx(fnn, MiseLog(FFT_Filtrer_Q2_28), label='Q2.28', color='red')
        SUB3.semilogx(fnn, MiseLog(FFT_Filtrer_Q2_20), label='Q2.20', color='blue')
        SUB3.set_title('FFT avec les filtres')
        SUB3.set_ylabel('Amplitude')
        SUB3.set_xlabel('Fréquence (Hz)')
        SUB3.legend()

    if(Filtres_Tout_Les_H):
        Figure2, SUB = plt.subplots(3, 2)
        Figure2.suptitle('Graphique B2 avec tout les Filtres + Addition à 2000 Hz')
        SUB[0][0].plot(MiseLog(FFT_H3))
        SUB[0][0].set_title('H3')
        SUB[0][0].set_ylabel('Amplitude (dB)')
        SUB[0][0].set_xlabel('Nombre d\'échantillons [k]')

        SUB[0][1].plot(MiseLog(FFT_H4))
        SUB[0][1].set_title('H4')
        SUB[0][1].set_ylabel('Amplitude (dB)')
        SUB[0][1].set_xlabel('Nombre d\'échantillons [k]')

        SUB[1][0].plot(MiseLog(FFT_H5))
        SUB[1][0].set_title('H5')
        SUB[1][0].set_ylabel('Amplitude (dB)')
        SUB[1][0].set_xlabel('Nombre d\'échantillons [k]')

        SUB[1][1].plot(MiseLog(FFT_H6))
        SUB[1][1].set_title('H6')
        SUB[1][1].set_ylabel('Amplitude (dB)')
        SUB[1][1].set_xlabel('Nombre d\'échantillons [k]')

        SUB[2][0].plot(MiseLog(FFT_H7))
        SUB[2][0].set_title('H7')
        SUB[2][0].set_ylabel('Amplitude (dB)')
        SUB[2][0].set_xlabel('Nombre d\'échantillons [k]')

        SUB[2][1].plot(MiseLog(FFT_Filtrer_Q15))
        SUB[2][1].set_title('H3+H4+H5+H6+H7')
        SUB[2][1].set_ylabel('Amplitude (dB)')
        SUB[2][1].set_xlabel('Nombre d\'échantillons [k]')

def IIR():
    fe: float = 20000
    fc_low: float = 950
    fc_high: float = 1050
    filter_order: int = 4
    pass_band_ripple_db: float = 1
    stop_band_attn_db: float = 70
    WorN = 1024

    sos = signal.ellip(N=filter_order, rp=pass_band_ripple_db, rs=stop_band_attn_db, Wn=[fc_low, fc_high], fs=fe,
                       btype="bandstop", output="sos")

    sos_Q2_13 = sos * (2**13)
    #sos_Q2_13 = sos_Q2_13.astype(np.int16)
    sos_Q2_5 = sos * (2**5)
    sos_Q2_5 = sos_Q2_5.astype(np.int8)

    b1_13 = sos_Q2_13[0][0:3]
    a1_13 = sos_Q2_13[0][3:6]

    b2_13 = sos_Q2_13[1][0:3]
    a2_13 = sos_Q2_13[1][3:6]

    b3_13 = sos_Q2_13[2][0:3]
    a3_13 = sos_Q2_13[2][3:6]

    b4_13 = sos_Q2_13[3][0:3]
    a4_13 = sos_Q2_13[3][3:6]

    b1_5 = sos_Q2_5[0][0:3]
    a1_5 = sos_Q2_5[0][3:6]

    b2_5 = sos_Q2_5[1][0:3]
    a2_5 = sos_Q2_5[1][3:6]

    b3_5 = sos_Q2_5[2][0:3]
    a3_5 = sos_Q2_5[2][3:6]

    b4_5 = sos_Q2_5[3][0:3]
    a4_5 = sos_Q2_5[3][3:6]

    w1_Q2_13, h1_Q2_13 = signal.freqz(b1_13, a1_13, worN=WorN, fs=fe)
    w2_Q2_13, h2_Q2_13 = signal.freqz(b2_13, a2_13, worN=WorN, fs=fe)
    w3_Q2_13, h3_Q2_13 = signal.freqz(b3_13, a3_13, worN=WorN, fs=fe)
    w4_Q2_13, h4_Q2_13 = signal.freqz(b4_13, a4_13, worN=WorN, fs=fe)
    w1_Q2_5, h1_Q2_5 = signal.freqz(b1_5, a1_5, worN=WorN, fs=fe)
    w2_Q2_5, h2_Q2_5 = signal.freqz(b2_5, a2_5, worN=WorN, fs=fe)
    w3_Q2_5, h3_Q2_5 = signal.freqz(b3_5, a3_5, worN=WorN, fs=fe)
    w4_Q2_5, h4_Q2_5 = signal.freqz(b4_5, a4_5, worN=WorN, fs=fe)

    if (Reponse_Frequence_IIR):
        Figure, [SUB1, SUB2] = plt.subplots(2, 1)
        Figure.suptitle('Réponses en fréquence du filtre IIR')
        SUB1.semilogx(w1_Q2_13, 20 * np.log10(np.abs(h1_Q2_13)), label='1')
        SUB1.semilogx(w2_Q2_13, 20 * np.log10(np.abs(h2_Q2_13)), label='2')
        SUB1.semilogx(w3_Q2_13, 20 * np.log10(np.abs(h3_Q2_13)), label='3')
        SUB1.semilogx(w4_Q2_13, 20 * np.log10(np.abs(h4_Q2_13)), label='4')
        SUB1.set_title('Q2.13')
        SUB1.set_xlabel('Fréquence [Hz]')
        SUB1.set_ylim(top=15, bottom=-50)
        SUB1.set_xlim(left=100, right=10000)
        SUB1.set_ylabel('Gain [dB]')

        SUB2.semilogx(w1_Q2_5, 20 * np.log10(np.abs(h1_Q2_5)), label='1')
        SUB2.semilogx(w2_Q2_5, 20 * np.log10(np.abs(h2_Q2_5)), label='2')
        SUB2.semilogx(w3_Q2_5, 20 * np.log10(np.abs(h3_Q2_5)), label='3')
        SUB2.semilogx(w4_Q2_5, 20 * np.log10(np.abs(h4_Q2_5)), label='4')
        SUB2.set_title('Q2.5')
        SUB2.set_xlabel('Fréquence [Hz]')
        SUB2.set_ylim(top=20, bottom=-60)
        SUB2.set_xlim(left=100, right=10000)
        SUB2.set_ylabel('Gain [dB]')

    [wsos, h_dftsos] = signal.sosfreqz(sos, worN=WorN, fs=fe)

    #Réponse impulsionelle
    #if(Reponse_Frequence_IIR):
        #plt.figure()
        #plt.semilogx(wsos, 20 * np.log10(np.abs(h_dftsos)), color='blue')
        #plt.title('Réponses en fréquence du filtre IIR')
        #plt.xlabel('Fréquence [Hz]')
        #plt.ylim(top=5, bottom=-100)
        #plt.xlim(left=100, right=10000)
        #plt.ylabel('Gain [dB]')

    x900 = Cree_Sin(900, 20000, 768, 0.1)

    x1000 = Cree_Sin(1000, 20000, 768, 0.1)

    x1100 = Cree_Sin(1100, 20000, 768, 0.1)

    OUT1 = Calcul(x900, sos_Q2_13, True)
    OUT2 = Calcul(x1000, sos_Q2_13, True)
    OUT3 = Calcul(x1100, sos_Q2_13, True)

    OUT1_Q2_5 = Calcul(x900, sos_Q2_5, False)
    OUT2_Q2_5 = Calcul(x1000, sos_Q2_5, False)
    OUT3_Q2_5 = Calcul(x1100, sos_Q2_5, False)

    if(Filtre_IIR_Test_Sans_int8):
        Figure, [SUB1, SUB2, SUB3] = plt.subplots(3, 1)
        Figure.suptitle('Graphiques C1')
        SUB1.plot(OUT1, color='blue', label='Sortie Q2.13')
        #SUB1.plot(OUT1_Q2_5, color='red', label='Sortie Q2.5')
        SUB1.plot(x900, color='grey', label='Entree')
        SUB1.set_title('900 Hz')
        SUB1.set_xlabel('Nombre d\'échantillons [k]')
        SUB1.legend()

        SUB2.plot(OUT2, color='blue', label='Sortie Q2.13')
        #SUB2.plot(OUT2_Q2_5, color='red', label='Sortie Q2.5')
        SUB2.plot(x1000, color='grey', label='Entree')
        SUB2.set_title('1000 Hz')
        SUB2.set_xlabel('Nombre d\'échantillons [k]')
        SUB2.legend()

        SUB3.plot(OUT3, color='blue', label='Sortie Q2.13')
        #SUB3.plot(OUT3_Q2_5, color='red', label='Sortie Q2.5')
        SUB3.plot(x1100, color='grey', label='Entree')
        SUB3.set_title('1100 Hz')
        SUB3.set_xlabel('Nombre d\'échantillons [k]')
        SUB3.legend()


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

    Fenetrage()
    FIR()
    IIR()

    print('BreakPoint')

if __name__ == "__main__":
    main()