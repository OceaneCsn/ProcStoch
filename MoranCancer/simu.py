# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 22:04:55 2018

@author: Océane
"""

import random as rd
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import math

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)
            
class simu():
    def __init__(self, N, w, c0, alpha = 0.01, f=1.2, mu=0.2, treat = None):
        self.cells = []
        self.nbCanc = c0
        self.f = f
        self.mu = mu
        self.pop = dict()
        self.f_norm = 1
        self.mu_norm = 0.001
        self.N = N
        self.pop[0] = N-c0
        self.pop[1] = c0
        self.cancerous_cells = [1]
        self.w = w
        self.fitnesses = dict()
        self.fitnesses[1] = f
        self.fitnesses[0] = 1
        self.history = [self.pop]
        self.treat = treat
        self.alpha = alpha
        self.treatment = False
        self.cpt_treat = 0
        self.treat_times = []
        self.shannon = []
        
    def step(self, t):
        
        self.cancerous_types_counts = [self.pop[k] for k in list(self.pop.keys()) if k!=0]
        self.nbCanc = sum(self.cancerous_types_counts)
        self.cancerous_types = [k for k in list(self.pop.keys()) if k!=0]
        
        #print(self.fitnesses)
        if self.cancer_detection()[0] and not self.treatment:
            self.fitnesses[self.cancer_detection()[1]] *= self.alpha
            #print("******************** treatment ! ************************************")
            if not self.treatment:
                self.treat_times.append(t)
            self.treatment = True
            
        if self.treatment:
            self.cpt_treat +=1
            
        if self.cpt_treat == 50:
            self.cpt_treat = 0
            self.treatment = False
            self.fitnesses[self.cancer_detection()[1]] /= self.alpha
            
        breaks = []
        r = rd.random()
        for cell_type in sorted(list(self.pop.keys())):
            breaks.append(self.fitnesses[cell_type]*self.pop[cell_type])
        nbTot = sum(breaks)
        breaks = np.cumsum(breaks)/nbTot
        chosen = 0
        #print(breaks)
        for i, b in enumerate(breaks):
            if r<b:
                chosen = i
                break                

        #print("chosen", chosen)
        if chosen > 0:
            #a cancerous cell was chosen
            if rd.random() <= self.mu:
                #a new cancerous clone is born
                new_type = max(self.cancerous_types)+1
                self.cancerous_types.append(new_type)
                self.pop[new_type] = 1
                self.fitnesses[new_type] = self.f
            else:
                #the current cancerous clone just divides
                self.pop[chosen] += 1
        else:
            #a normal cell was chosen
            if rd.random() <= self.mu_norm:
                #a new cancerous clone is born
                new_type = max(self.cancerous_types)+1
                self.cancerous_types.append(new_type)
                self.pop[new_type] = 1
                self.fitnesses[new_type] = self.f
            else:
                #one more normal cell
                self.pop[chosen] += 1
        #now let's kill someone randomly
        indiv = np.random.randint(self.N, size=1)[0]
        tmp = 0
        killed = 0
        for typ in list(self.pop.keys()):
            tmp += self.pop[typ]
            if tmp >= indiv:
                killed = typ
                break
        self.pop[killed] -= 1
        #print(self.pop)
        self.history.append(dict(self.pop))
        self.set_shannon()
        
    def cancer_detection(self):
        #self.cancerous_cell_types = [self.pop[k] for k in list(self.pop.keys()) if k!=0]
        self.cancerous_types_counts = [self.pop[k] for k in sorted(list(self.pop.keys())) if k!=0]
        self.nbCanc = sum(self.cancerous_types_counts)
        
        if self.nbCanc/self.N*1.0 >= self.w:
            biggest_clone = np.argmax(self.cancerous_types_counts)+1
            return (True, biggest_clone)
        return (False, 0)
    
    def set_shannon(self):
        s = 0
        for k in list(self.pop.keys()):
            pi = self.pop[k]/self.N*1.0
            print(pi, math.log(pi))
            s += pi*math.log(pi)
        self.shannon.append(-s)
        #self.shannon.append(sum([*math.log(self.pop[k]/self.N*1.0) for k in list(self.pop.keys())]))
        
        
    def run(self, T):
        for t in range(T):
            self.step(t)
        plt.plot(self.shannon)
        #self.plot_history()
    
    def plot_history(self):
        cmap = get_cmap(len(list(self.pop.keys())))
        colors = [cmap(i) for i in range(len(list(self.pop.keys())))]
        rd.shuffle(colors)
        for t in range(len(self.history)):
            print("Time point ", t)
            cell = 0
            tmp = self.history[t][cell]
            for n in range(self.N):
                if n > tmp:
                    cell += 1
                    tmp += self.history[t][cell]
                plt.plot(t, n*0.1, 'x', color = cmap(cell), markersize = 2)
    def plot_pop(self):
        cells = []
        #for c in list(self.history.keys():
        evol0 = [self.history[i][0] for i in range(len(self.history))]
        evol1 = [self.N-self.history[i][0] for i in range(len(self.history))]
        plt.plot(evol0)
        plt.plot(evol1, color = "red")
        for t_t in self.treat_times:
            plt.axvline(x=t_t, color = "black")
        
s = simu(500, 0.2, 10, f = 4, mu = 0.00005)
s.run(3000)
#s.plot_history()
#s.plot_pop()

#N = 500, f=1.5, mu = 0.005, c0 = 50, w = 0.2, 0.01, n = 10000

