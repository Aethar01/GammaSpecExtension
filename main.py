import matplotlib.pyplot as plt


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
    with open('./peaks.txt', 'w') as f:
        for key in data:
            f.write(f"{key}: {str(max(data[key][500:700]))} \n")


if __name__ == "__main__":
    data = {
        "22Na with no Pb": import_data("./ExtensionData/22Na.dat"),
        "pb1": import_data("./ExtensionData/pb1mm.dat"),
        "pb2": import_data("./ExtensionData/pb2mm.dat"),
        "pb3": import_data("./ExtensionData/pb3mm.dat"),
        "pb4": import_data("./ExtensionData/pb4mm.dat"),
        "pb5": import_data("./ExtensionData/pb5mm.dat"),
        "pb6": import_data("./ExtensionData/pb6mm.dat"),
        "pb7": import_data("./ExtensionData/pb7mm.dat"),
        "pb8": import_data("./ExtensionData/pb8mm.dat"),
            }

    bins1 = calibrate(data["22Na with no Pb"])

    writedata(data)

    plt.xlabel("Energy [keV]")
    plt.ylabel("Counts")
    for key in data:
        plt.plot(bins1[500:700], data[key][500:700], label=key)
    plt.legend()
    plt.yscale('log')
    plt.savefig("./pbattenuation.png")
