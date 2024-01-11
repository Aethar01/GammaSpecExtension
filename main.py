import matplotlib.pyplot as plt
import scipy.optimize as opt
import numpy as np

e = 2.7182818284590452353602874713527


def get_log_fit(bins, data, data_err):
    def log_func(x, a, b, c):
        return a * e**(-b * x) + c

    p0 = (1000, 1, 0)
    popt, pcov = opt.curve_fit(log_func, bins, data, sigma=data_err, p0=p0)
    binsnew = []
    for x in range(int(max(bins))+1):
        binsnew.append(x)
    return (binsnew, [log_func(binsnew[x], *popt) for x in range(len(binsnew))]), popt


def import_data(filename):
    with open(filename) as file:
        lines = [int(line.rstrip()) for line in file]
        return lines


def calibrate(data):
    temp = []
    for x in range(len(data)):
        temp.append(float(x)*0.82 + 7.60 + 14.68)
    return temp


def writedata(data):
    with open(f'./peaks_for_{data["NAME"]}.txt', 'w') as f:
        for key in data:
            if key != 'NAME':
                f.write(f"{key}: {str(max(data[key][500:700]))} \n")


def graph(bins, data, log=False):
    plt.xlabel("Energy [keV]")
    plt.ylabel("Counts")
    for key in data:
        if key != 'NAME':
            plt.plot(bins[500:700], data[key][500:700], label=key)
    plt.legend(title=f"{data['NAME']} depth [mm]", fontsize=5)
    if log:
        plt.yscale('log')
        plt.title(f"{data['NAME']} Attenuation with varying material depth (log)")
    else:
        plt.yscale('linear')
        plt.title(f"{data['NAME']} Attenuation with varying material depth (linear)")
    plt.ylim(ymin=0)
    if log:
        plt.savefig(f"./{data['NAME']}_log.png")
    else:
        plt.savefig(f"./{data['NAME']}_linear.png")
    plt.clf()


def graph_peak_counts_vs_depth(data, log=False):
    with open(f'./peaks_for_{data["NAME"]}.txt', 'r') as f:
        lines = f.readlines()
        depth = []
        peaks = []
        for line in lines:
            depth.append(float(line.split(':')[0]))
            peaks.append(float(line.split(':')[1]))
        peaks_err = [x**0.5 for x in peaks]
        fit_data, popt = get_log_fit(depth, peaks, peaks_err)
        plt.xlabel("Depth [mm]")
        plt.ylabel("Counts")
        plt.plot(depth, peaks)
        plt.plot(*fit_data, label=f"Fit: {round(popt[0], 6)}exp[-{round(popt[1], 6)}*x] + {round(popt[2], 6)}")
        plt.errorbar(depth, peaks, yerr=peaks_err)
        if log:
            plt.yscale('log')
            plt.title(f"{data['NAME']} Peak Count vs Depth (log)")
        else:
            plt.yscale('linear')
            plt.title(f"{data['NAME']} Peak Count vs Depth (linear)")
        plt.ylim(ymin=0)
        plt.legend(fontsize=10)
        if log:
            plt.savefig(f"./{data['NAME']}_attenuation_log.png")
        else:
            plt.savefig(f"./{data['NAME']}_attenuation_linear.png")
        plt.clf()
        return popt[1]


def plot_and_peaks(data, log=False):
    bins = calibrate(data["0"])

    writedata(data)

    graph(bins, data, log=log)


def plot_attenuation(attenfits):
    plt.xlabel("Depth [mm]")
    plt.ylabel("Proportion of Original Counts (log)")
    for key in attenfits:
        def expression(x):
            return e ** (-attenfits[key]*x)
        x_range = np.linspace(0, 1000, 10000)
        plt.plot(x_range, [expression(x) for x in x_range], label=f"{key}: -{round(attenfits[key], 6)}")
    # plt.ylim(ymin=0,)
    # plt.xlim(xmin=-50, xmax=50)
    plt.yscale('log')
    plt.legend(title="Material Attenuation Coefficient", fontsize=5)
    plt.title("Proportion of Original Counts vs Material Depth (log)")
    plt.savefig("./Attenuation_Coefficient.png")
    plt.clf()


if __name__ == "__main__":

    attenfits = {
            "Pb": None,
            "Al": None,
            "Steel": None,
            "W": None,
            }

    Pb = {
        "NAME": "Pb",
        "0": import_data("./ExtensionData/22Na.dat"),
        "2.25": import_data("./ExtensionData/pb1mm.dat"),
        "3.37": import_data("./ExtensionData/pb2mm.dat"),
        "4.49": import_data("./ExtensionData/pb3mm.dat"),
        "5.61": import_data("./ExtensionData/pb4mm.dat"),
        "6.7": import_data("./ExtensionData/pb5mm.dat"),
        "7.82": import_data("./ExtensionData/pb6mm.dat"),
        "8.89": import_data("./ExtensionData/pb7mm.dat"),
        "10.01": import_data("./ExtensionData/pb8mm.dat"),
    }

    plot_and_peaks(Pb, log=True)
    plot_and_peaks(Pb, log=False)
    _ = graph_peak_counts_vs_depth(Pb, log=True)
    attenfits["Pb"] = graph_peak_counts_vs_depth(Pb, log=False)

    Al = {
        "NAME": "Al",
        "0": import_data("./ExtensionData/22Na_today.dat"),
        "6": import_data("./ExtensionData/Al1.dat"),
        "12": import_data("./ExtensionData/Al2.dat"),
        "18": import_data("./ExtensionData/Al3.dat"),
        "24": import_data("./ExtensionData/Al4.dat"),
        "30": import_data("./ExtensionData/Al5.dat"),
        "36": import_data("./ExtensionData/Al6.dat"),
        "42": import_data("./ExtensionData/Al7.dat"),
        "48": import_data("./ExtensionData/Al8.dat"),
        "54": import_data("./ExtensionData/Al9.dat"),
        "60": import_data("./ExtensionData/Al10.dat"),
        "66": import_data("./ExtensionData/Al11.dat"),
        "72": import_data("./ExtensionData/Al12.dat"),
        "78": import_data("./ExtensionData/Al13.dat"),
        "84": import_data("./ExtensionData/Al14.dat"),
        "90": import_data("./ExtensionData/Al15.dat"),
    }

    plot_and_peaks(Al, log=True)
    plot_and_peaks(Al, log=False)
    _ = graph_peak_counts_vs_depth(Al, log=True)
    attenfits["Al"] = graph_peak_counts_vs_depth(Al, log=False)

    Steel = {
        "NAME": "Steel",
        "0": import_data("./ExtensionData/22Na_today.dat"),
        "5.75": import_data("./ExtensionData/Steel1.dat"),
        "11.5": import_data("./ExtensionData/Steel2.dat"),
        "17.25": import_data("./ExtensionData/Steel3.dat"),
        "23": import_data("./ExtensionData/Steel4.dat"),
        "28.75": import_data("./ExtensionData/Steel5.dat"),
        "34.5": import_data("./ExtensionData/Steel6.dat"),
        "40.25": import_data("./ExtensionData/Steel7.dat"),
        "46": import_data("./ExtensionData/Steel8.dat"),
        "51.75": import_data("./ExtensionData/Steel9.dat"),
        "57.5": import_data("./ExtensionData/Steel10.dat"),
        "63.25": import_data("./ExtensionData/Steel11.dat"),
        "69": import_data("./ExtensionData/Steel12.dat"),
    }

    plot_and_peaks(Steel, log=True)
    plot_and_peaks(Steel, log=False)
    _ = graph_peak_counts_vs_depth(Steel, log=True)
    attenfits["Steel"] = graph_peak_counts_vs_depth(Steel, log=False)

    W = {
        "NAME": "W",
        "0": import_data("./ExtensionData/22Na_gluecap.dat"),
        "0.55": import_data("./ExtensionData/W1.dat"),
        "1.12": import_data("./ExtensionData/W2.dat"),
        "1.68": import_data("./ExtensionData/W3.dat"),
        "2.25": import_data("./ExtensionData/W4.dat"),
        "2.83": import_data("./ExtensionData/W5.dat"),
        "3.38": import_data("./ExtensionData/W6.dat"),
        "3.96": import_data("./ExtensionData/W7.dat"),
        "4.45": import_data("./ExtensionData/W8.dat"),
        "4.93": import_data("./ExtensionData/W9.dat"),
        "5.4": import_data("./ExtensionData/W10.dat"),
        "5.89": import_data("./ExtensionData/W11.dat"),
        "6.35": import_data("./ExtensionData/W12.dat"),
    }

    plot_and_peaks(W, log=True)
    plot_and_peaks(W, log=False)
    _ = graph_peak_counts_vs_depth(W, log=True)
    attenfits["W"] = graph_peak_counts_vs_depth(W, log=False)

    plot_attenuation(attenfits)
