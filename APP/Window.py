# Libraries requises
from matplotlib import pyplot as plt, rcParams as mpl_rcParams
import numpy as np
from scipy import signal
pi = np.pi
def printtofile(file):
    # Breakpoint pour mettre l'interpréteur en pause afin d’afficher les figures
    text_file = open("window.h", "w")

    text_file.write("// rectangle window // Q2.13\n")
    text_file.write("const int32_t window[SIG_LEN] = {")

    for i in file:
        text_file.write(f"{i},\n")

    text_file.write("};")

    text_file.close()

def main():
    han = np.hanning(768)
    han = han * (2**13)
    han_Q2_13 = han.astype(np.int16)

    printtofile(han_Q2_13)
    print('hi')

if __name__ == "__main__":
    main()

