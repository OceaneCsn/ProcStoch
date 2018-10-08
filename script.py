# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import random as rd
#sys.path.append('/home/ocassan/ProcStoch')

############################# Simple functions ##########################

def poisson_process(lam, T):
    #donne les inter events times
    return np.random.exponential(scale = 1/lam, size=T)
    
p = poisson_process(2,200)

def counting(poisson, t):
    return sum(poisson[0:t])

counting(p, 10)

def lam_estimate(poisson):
    return 1.0/np.mean(poisson)


############################# Neuron pikes ##########################

#pathToFiles = "D:/ProcStoch"
pathToFiles = "/home/ocassan/ProcStoch/"
sham4_art = pd.read_csv(os.path.join(pathToFiles, 'SHAM4_artefact_timing.txt'), header = None, sep = '\t')
sham5_art = pd.read_csv(os.path.join(pathToFiles, 'SHAM5_artefact_timing.txt'), header = None, sep = '\t')
sham4_spikes = pd.read_csv(os.path.join(pathToFiles, 'SHAM4_spike_timing.txt'), header = None, sep = '\t')
sham5_spikes = pd.read_csv(os.path.join(pathToFiles, 'SHAM5_spike_timing.txt'), header = None, sep = '\t')

def split(elec, spikes):
    res = []
    j = 0
    for i, stim in enumerate(elec[1]):

        res.append([stim])
        print('********************* ', i, str(stim))
        if i+1<len(elec[1]):
            while spikes[0][j]< elec[1][i+1]:
                print(spikes[0][j])
                res[i].append(spikes[0][j])
                j += 1
        else:
            while j<len(spikes[0]):
                print(spikes[0][j])
                res[i].append(spikes[0][j])
                j += 1
    return res

def set_to_zero(splits):
    return [[spikes- values[0] for spikes in values] for values in splits]
        

s = split(sham4_art, sham4_spikes)
data = set_to_zero(s)


data = [np.asarray(d) for d in data]
data = [d[d<0.1] for d in data]
data = [d[d>0] for d in data]
for i,d in enumerate(data): 
    plt.plot(d, np.repeat(i,len(d)), 'o')

concat = []
for values in data:
    for v in values:
        concat.append(v)
#lambda estimate : 1/mean des intervalles de temps du process de Poisson
print(1/np.mean(concat))

#checking the fit on the plot
histogram_results = plt.hist(concat, bins = 100)
x = np.linspace(0,0.10, num = 100)
plt.plot(x, [1.0/0.0337*math.exp(-xs/0.0337) for xs in x], 'r-')

#wrong!!! lambda depends on t and must be estimated for every interval... 
#on fait la moyenne des counts divisée par le temps sur chaque bin de l'histogramme pour avoir les lambda de t
#Sergio's code (on peut aussi le faire avec une régression de random forest) :
counts = pd.DataFrame()
nb_experiments = 50
mean_count = histogram_results[0]/nb_experiments
t = histogram_results[1][1:] - histogram_results[1][:-1]
counts["lambda"] = mean_count/(t)
window_size = 5
#smoothing
z = counts.rolling(window_size, center=True, win_type="triang",min_periods=int(window_size*1/4))
Lambda_t = z.mean()
plt.plot(Lambda_t ,"o")
plt.xlabel("$Time$ $t$ $(\cdot 10^{-3} s)$",fontsize=20)
plt.ylabel("$\lambda(t)$",fontsize=20)



#regression model 
from sklearn.ensemble import RadomForestRegressor
rf=RandomForestRegressor(n_estimators=50, criterion='mse', max_depth=5)

################ Simultaing a non homogenous Poisson Process
#my idea : for a given number of T experiments for 1000 replicates, pick a value in a poisson law
#with the value of lambda depending on time.

poiss = []
for r in range(100):
    poiss.append([])
    for t in range(10):
        l = Lambda_t['lambda'][t]
        if Lambda_t['lambda'][t] == 0:
            l = 1
        poiss[r].append(np.random.exponential(scale = 1.0/l, size=1)[0])
poiss
Lambda_t

poiss = [np.asarray(d) for d in poiss]
poiss = [d[d<0.1] for d in poiss]
poiss = [d[d>0] for d in poiss]
for i,d in enumerate(poiss): 
    plt.plot(d, np.repeat(i,len(d)), 'o')


##premiere methode
values = [0]    
for t in range(0:100):
    values.append(0)
    
#deuxieme methode : separation. Pour chaque evenement, on le mets dans un des 2 processus de poisson (on garde le spike ou pas)
#suivant une loi de Bernouilli. On tire dans une loi uniforme entre 0 et 0.1. On le garde suivant une proba qui dépend de la valeur piochée

spikes =  []
for i in range(0,10000):
    spike = rd.random()*100
    prob = Lambda_t['lambda'][int(spike)]/max(Lambda_t['lambda'])
    if rd.random()<prob:
        spikes.append(spike)

histogram_results = plt.hist(spikes, bins = 100)

Lambda_t['lambda']
    