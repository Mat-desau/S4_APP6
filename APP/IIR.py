import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def CalculFiltre(fe: float):
    """
    Problème 1: Filtre IIR elliptique
    """

    # Filter specifications
    fc_low: float = 950
    fc_high: float = 1050
    filter_order: int = 4
    pass_band_ripple_db: float = 1
    stop_band_attn_db: float = 70
    WorN = 1024

    sos = signal.ellip(N=filter_order, rp=pass_band_ripple_db, rs=stop_band_attn_db, Wn=[fc_low, fc_high], fs=fe, btype="bandstop", output="sos")

    [wsos, h_dftsos] = signal.sosfreqz(sos, worN=WorN, fs=fe)

    plt.semilogx(wsos, 20 * np.log10(np.abs(h_dftsos)), label='Normal', color='red')

    sos_Q = np.round(sos*(2**13))

    sos_Q *= 2**(-13)

    [wsos_Q, h_dftsos_Q] = signal.sosfreqz(sos_Q, worN=WorN, fs=fe)

    plt.semilogx(wsos_Q, 20 * np.log10(np.abs(h_dftsos_Q)), label='SOS Q2.13', color='blue')

    #plt.legend()
    plt.title('Réponses en fréquence de filtre elliptique')
    plt.xlabel('Fréquence [Hz]')
    plt.ylim(top=5, bottom=-100)
    plt.xlim(left=100, right=10000)
    plt.ylabel('Gain [dB]')
    plt.legend()

    #Question B
    #Numero 1
    N = 512
    N = N-1
    fir_low_h = signal.firwin(numtaps=N, cutoff=1000, fs=fe, pass_zero="lowpass", window="hamming")
    fir_high_h = signal.firwin(numtaps=N, cutoff=950, fs=fe, pass_zero="highpass", window="hamming")

    #plt.figure()
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


    #plt.figure()
    Figure, (SUB1, SUB2) = plt.subplots(2, 1)
    SUB1.semilogx(fft_freq_low, fft_low)
    SUB2.semilogx(fft_freq_high, fft_high)
    SUB1.set_title('Réponses en fréquence des filtres FIR passe-bas et passe-haut')
    SUB1.set_xlabel('Frequence [Hz]')
    SUB1.set_ylabel('Gain [dB]')
    SUB2.set_title('Total des réponses en fréquence des deux filtres')
    SUB2.set_xlabel('Frequence [Hz]')
    SUB2.set_ylabel('Gain [dB]')

    print('yo')

    sos *= (2**13)
    return sos

def main():
    plt.rcParams.update(
        {
            "backend": "TkAgg",
            "axes.grid": True,
            "axes.grid.which": "both",
            "figure.autolayout": True,
            "interactive": True,
        }
    )

    fe: float = 20000
    OUT = CalculFiltre(fe)

    Print_Texte = True
    if (Print_Texte):
        # print out in fichier
        with open("filterIIRcoeffs.h", "w") as fd:
            fd.write(f"// IIRCoeffs : coefficients (b0, b1, b2, a0, a1, a2) for N_SOS_SECTIONS cascaded SOS sections\n#define IIR_QXY_RES_NBITS 13 // Q2.13\n#define N_SOS_SECTIONS 4\nint32_t IIRCoeffs[N_SOS_SECTIONS][6] = {{\n")
            for a in range(0, 4):
                fd.write("{")
                for b in range(0, 6):
                    fd.write(f"{int(np.round(OUT[a][b]))}")
                    if(b < 5):
                        fd.write(",")
                fd.write("},\n")
            fd.write("};\n")
            fd.write("int32_t IIRu[N_SOS_SECTIONS] = {0}, IIRv[N_SOS_SECTIONS] = {0};\n")

    print('We made it here')


if __name__ == "__main__":
    main()
