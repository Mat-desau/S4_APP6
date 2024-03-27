#
# Filemane:         S4GE-APP6-Plot-Complex-CSV.py
#
# Last modified:    23/07/2021
#
# Author:           Paul Charette
#
# Purpose:          Plot the norm of a complex array in a .csv file exported from MPLAB
#                   (right-click on a variable in the MPLAB "Variables" window, then
#                   Export Data -> CSV File -> Hexadecimal Format)
#
# Output:           None
#
# Notes             1) The data must be in hexadecimal format
#                   2) The data are in column 2 of the .csv file, with real
#                      and imaginary parts interleaved line-by-line
#                   3) A scale factor can be supplied, for example to remove
#                      the 2**Y scaling in the QXY encoding of H
#                   3) The script can be run from the command line with
#                      "python.exe S4GE-APP6-Plot-Complex-CSV.py <filename> <sampling frequency> <scale factor>"
#                      or in PyCharm with hard-coded parameters
#
import matplotlib.pyplot as plt
import numpy as np
import sys


def plot_complex_csv_data(file_name: str, scale_factor: float = 1, fe: float = 20000):
    """
    Plot the norm in dB of a complex array loaded from a .csv file

    :param file_name: name of .csv file containing complex array in second column,
                      with interleaved real/imaginary hexadecimal components
    :param scale_factor: scale factor, optional (default = 1, i.e. no scaling)
                         ex: scale_factor = 2**Y, to remove scaling in QXY encoding of H
    :param fe: sampling frequency in Hz, optional (default = 20 kHz)
    :return: None
    """

    # Load re/im interleaved hex data from .csv file as unsigned 64 bit integer array
    # NB: int(s, 0) converts a string containing a hexadecimal number with leading "0x"
    #     to an unsigned integer, but np.int64() is required as a wrapper otherwise
    #     genfromtxt() tries to load result into a 32 bit integer and overflow may occur
    data: np.ndarray = np.genfromtxt(
        file_name,
        delimiter=",",
        usecols=[1],
        converters={1: lambda s: np.int64(int(s, 0))},
    )
    data[data >= 0x80000000] -= 0x100000000  # Convert to signed 64 bit integers
    x: np.ndarray = data[0::2] + 1j * data[1::2]  # Convert to complex array of floats

    # Build frequency array for plotting
    f: np.ndarray = np.arange(0, fe, fe / len(x))

    # Calculate vector norm, replace any null values with array minimum (non-zero)
    # so log10() function doesn't complain about null values, convert to dB
    x_norm: np.ndarray = np.abs(x) / scale_factor
    x_norm[x_norm == 0] = np.amin(x_norm[x_norm > 0])
    x_norm_db: np.ndarray = 20 * np.log10(x_norm)

    # Plot norm in dB as a function of frequency, on linear (like DMCI) & log scales
    fig, axs = plt.subplots(3)
    fig.suptitle(f"{file_name} (fe = {fe} Hz, scale factor = {scale_factor})")
    axs[0].plot(f, x_norm_db)
    axs[0].set_xlabel("Fréquence sur échelle linéaire [0, fe] (Hz)")
    axs[0].set_ylabel("Amplitude [dB]")
    axs[0].grid(which="both")
    axs[1].plot(
        np.concatenate((f[len(x) // 2 :] - fe, f[: len(x) // 2])),
        np.concatenate((x_norm_db[len(x) // 2 :], x_norm_db[: len(x) // 2])),
    )
    axs[1].set_xlabel("Fréquence sur échelle linéaire [-fe/2, fe/2] (Hz)")
    axs[1].set_ylabel("Amplitude [dB]")
    axs[1].grid(which="both")
    axs[2].semilogx(f[: len(x) // 2], x_norm_db[: len(x) // 2])
    axs[2].set_xlabel("Fréquence sur échelle logarithmique [0, fe/2] (Hz)")
    axs[2].set_ylabel("Amplitude [dB]")
    axs[2].grid(which="both")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # matplotlib interactive mode
    plt.ion()

    # If running outside PyCharm, read parameters from command line (* == unpack)
    if sys.gettrace() is None:
        plot_complex_csv_data(sys.argv[1], *np.array(sys.argv[2:]).astype(np.float64))
        input("Press any key to exit...\n")
    # else running in PyCharm, specify parameters explicitly
    else:
        plot_complex_csv_data("Htot.csv", 2 ** 13)
        # plot_complex_csv_data("outFFT.csv")
        print("Breakpoint here in PyCharm!")
