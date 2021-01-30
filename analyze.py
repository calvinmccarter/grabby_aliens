import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import argparse
import subprocess
import math

parser = argparse.ArgumentParser(description='Run Grabby Aliens model')
parser.add_argument('--n', type=str, help='The power in the origin-time power-law. You may pass a comma-separated list of values')
parser.add_argument('--N', type=str, help='Number of potential civilizations')
parser.add_argument('--sc', type=str, help='The ratio s/c - how fast civs expand relative to the speed of light. You may pass a comma-separated list of values.')
parser.add_argument('--s', type=float, default=1.0, help='The speed of civilization expansion (default 1.0)')
parser.add_argument('--m', type=float, default=2.0/3.0, help='The power in the universe expansion scale factor (default 2/3; see section "8 Cosmology")')
parser.add_argument('--D', type=int, default=3, help='Number of spatial dimensions. Should be 1,2 or 3 (default 3)')
parser.add_argument('--L', type=float, default=1.0, help='The size of the universe (default 1.0)')
parser.add_argument('--seed', type=float, default=0, help='A random seed (default 0)')
parser.add_argument('--empty_samples', type=int, default=0, help='How precisely to estimate how full the universe is (default 0, meaning no estimate at all)')

args = parser.parse_args()
D,ns,N,s,m,sc,L,seed,empty_samples = args.D,args.n,int(float(args.N)),float(args.s),args.m,args.sc,args.L,args.seed,args.empty_samples

cs = [s/float(sc_ratio) for sc_ratio in sc.split(',')]
ns = [float(n) for n in ns.split(',')]

DATA = {}
for c in cs:
    for n in ns:
        proper_n = (n+1)/3
        fname = os.path.join('data', f'D={D}_n={n}_N={N:.2e}_s={s}_c={c}_L={L}_seed={seed}_empty={empty_samples}_m={m}')
        if os.path.exists(f'{fname}_civs.csv') and os.path.exists(f'{fname}_years.csv'):
            print(f'Reusing {fname}_civs.csv and {fname}_years.csv')
        else:
            subprocess.check_output(f'g++ -std=c++17 -O3 -Wall -Werror -Wextra -Wshadow -Wno-sign-compare simulate.cc && ./a.out {D} {n} {N} {s} {c} {L} {fname} {seed} {empty_samples} {m}', shell=True)
            print(f'Generated {fname}_civs.csv and {fname}_years.csv')

        # Read CIV data
        with open(f'{fname}_civs.csv') as csvfile:
            CIVS = list(csv.DictReader(csvfile))

        # Read years data
        with open(f'{fname}_years.csv') as yearfile:
            YEARS = list(csv.DictReader(yearfile))

        DATA[(c,proper_n)] = (CIVS, YEARS)


C = ','.join([str(len(CIVS)) for (CIVS,YEARS) in DATA.values()])
n_str = ','.join([str(n) for c,n in DATA.keys()])
c_str = ','.join([str(c) for c,n in DATA.keys()])

def getLabels():
    return ['Origin', 'MinArrival', 'MinSee',
            'Origin (Gyr)', 'MinTillMeet (Gyr)', 'MinTillSee (Gyr)',
            'MaxAngle', '% Empty']

def getData(CIVS, YEARS, label):
    civs_x = [float(i)/len(CIVS) for i in range(len(CIVS))]
    years_x = [float(i)/len(YEARS) for i in range(len(YEARS))]
    # Rescale model times so median(Origin)=1.0
    T50 = np.median([float(row['OriginTime']) for row in CIVS])
    if label == 'Origin':
        x = civs_x
        y = [float(row['OriginTime'])/T50 for row in CIVS]
    elif label == 'Origin (Gyr)':
        x = years_x
        y = sorted([float(row['OriginTime']) for row in YEARS])
    elif label == 'MinArrival':
        x = civs_x
        y = sorted([float(row['MinArrival'])/T50 for row in CIVS])
    elif label == 'MinTillMeet (Gyr)':
        x = years_x
        y = sorted([float(row['MinWait']) for row in YEARS])
    elif label == 'MinSee':
        x = civs_x
        y = sorted([float(row['MinSee'])/T50 for row in CIVS])
    elif label == 'MinTillSee (Gyr)':
        x = years_x
        y = sorted([float(row['MinSETI']) for row in YEARS])
    elif label == 'MaxAngle':
        x = civs_x
        y = sorted([float(row['MaxAngle']) for row in CIVS])
    elif label == '% Empty':
        x = civs_x
        y = list(reversed(sorted([float(row['PctEmpty']) for row in CIVS])))
    else:
        assert False, f'Unknown label={label}'
    return (x,y)


# Table 1
# k1 = (2.0, 6.0)
# k2 = (4.0/3.0, 12.0)
# print('Name,p1,p25,p75,p1,p25,p75')
# for label in getLabels():
#    C1,Y1 = DATA[k1]
#    C2,Y2 = DATA[k2]
#    x1,y1 = getData(C1, Y1, label)
#    x2,y2 = getData(C2, Y2, label)
#    print(f'{label},{np.percentile(y1, 1)},{np.percentile(y1, 25)},{np.percentile(y1, 75)},{np.percentile(y2, 1)},{np.percentile(y2, 25)},{np.percentile(y2, 75)}')

def plot(ax, label, target_c, log):
    ax.minorticks_on()
    ax.grid(b=True, which='major', axis='both')
    ax.tick_params(axis='both', which='both', bottom=True, left=True)
    ax.set_xlabel('Percentile')
    for (c,n),(CIVS,YEARS) in DATA.items():
        if c != target_c:
            continue
        x,y = getData(CIVS, YEARS, label)
        ax.plot(x, y, label=f'n={n}')

    ax.set_ylabel(label)
    if log:
        ax.set_yscale('log')

# How many galaxies per civ for various powers of N?
#Also, there are now 2E6 galaxies/GLyr^3
#(Conselice et al. 2019). Thus model box has G = 2E6*(13.8/τ) 3 galaxies. If s&lt;c, then G is (c/s) 3
#times larger.
#for (c,n),(CIVS,YEARS) in DATA.items():
#    T50 = np.median([float(row['OriginTime']) for row in CIVS])
#    G = 2e6*pow(13.8/T50, 3)*pow(c/s, 3) / len(CIVS)
#    print(n,G)

# Make graphs
fig, p = plt.subplots(4,len(cs)+1,constrained_layout=True,figsize=(18,12))

plot(p[0,0], 'Origin', cs[0], log=False)
plot(p[1,0], 'MinArrival', cs[0], log=False)
if empty_samples:
    plot(p[2,0], '% Empty', cs[0], log=False)
else:
    fig.delaxes(p[2,0])
fig.delaxes(p[3,0])

for i,c in enumerate(cs):
    p[0,i+1].annotate(f's/c={1.0/c}', xy=(0.5, 1), xytext=(0, 5),
            xycoords='axes fraction', textcoords='offset points',
                            size='large', ha='center', va='baseline')
    plot(p[0,i+1], 'Origin (Gyr)', c, log=True)
    plot(p[1,i+1], 'MinTillMeet (Gyr)', c, log=True)
    # Omitted for space
    #plot(p[2,i+1], 'MinSee', c, log=False)
    plot(p[2,i+1], 'MinTillSee (Gyr)', c, log=True)
    plot(p[3,i+1], 'MaxAngle', c, log=False)

plt.savefig(f'{fname}.png')
# Open PNG in windows
# Switch which line is commented for Linux
subprocess.check_output(f'cmd.exe /C start {fname}.png', shell=True)
#subprocess.check_output(f'display {fname}.png', shell=True)
