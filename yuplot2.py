### tool: plot radar IQ output using SocioNext 60GHz radar
### date: Jan 12, 2024
### coder: YT

import sys
import matplotlib.pyplot as plt

## -- Get input filename from command line input,
input_file = sys.argv[-1]
## -- or directly enter filename below. But comment out above.
# input_file = "data1.txt"

# read in all lines
with open(input_file) as f:
    raw = f.readlines()

# nol: number of lines
nol = len(raw)

# get the positions, total number of chirps(noc) and tool fft points(NFFT)
pos = []
noc = 0
NFFT = 0
for i in range(nol):
    if raw[i][:3] == "fft":
        end_of_raw = i
    if raw[i][0] == "=":
        pos.append(i)
        noc += 1
        if noc == 2:
            NFFT = pos[1] - pos[0] - 1
        if noc > 2:
            nextNFFT = pos[-1] - pos[-2] - 1
            assert NFFT == nextNFFT, "NFFT points inconsistent!/n"
# in the case of single chirp
if noc == 1:
    NFFT = end_of_raw - pos[0] - 1

# arrange data
# in the structure of [([],[]),([],[]), .. ([],[])]
# It is a list of tuples.  There are noc tuples.  In each tuple, there are one list of I, and one list of Q.
data = []
for x in range(noc):
    tempI = []
    tempQ = []
    for y in range(NFFT):
        dot = raw[pos[x] + 1 + y][:-1].split(',')
        tempI.append(int(dot[0]))
        tempQ.append(int(dot[1]))
    data.append((tempI, tempQ))

# Joint the data.
data_I = []
data_Q = []
for i in range(len(data)):
    data_I += data[i][0]
    data_Q += data[i][1]




# plotting
plt.plot(data_I, 'r', label = 'I')
plt.plot(data_Q, 'b', label = 'Q')
plt.xlabel('NFFT Point')
plt.ylabel('I and Q reading')
plt.title('60GHz radar plot, Number of Chirps:' + str(noc))


plt.gcf().set_size_inches(10, 5)
plt.savefig(input_file[:-4] + '.png')
plt.show()