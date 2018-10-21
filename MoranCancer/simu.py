# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 22:04:55 2018

@author: Océane
"""

import random as rd
import matplotlib.pyplot as plt
import numpy as np

class Cell():
    def __init__(self, cancerous=False, f=1.2, mu=0.5):
        self.cancerous = cancerous
        if not cancerous:
            self.fitness = 1
            self.mu = 0.001
        else:
            self.fitness = f
            self.mu = mu

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)
            
class simu():
    def __init__(self, N, w, c0, f=1.2, mu=0.2):
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

        
    def step(self):
        
        self.cancerous_types_counts = [self.pop[k] for k in list(self.pop.keys()) if k!=0]
        self.nbCanc = sum(self.cancerous_types_counts)
        self.cancerous_types = [k for k in list(self.pop.keys()) if k!=0]
        
        breaks = []
        r = rd.random()
        for cell_type in list(self.pop.keys()):
            breaks.append(self.fitnesses[cell_type]*self.pop[cell_type])
        nbTot = sum(breaks)
        breaks = np.cumsum(breaks)/nbTot
        chosen = 0
        print(breaks)
        for i, b in enumerate(breaks):
            if r<b:
                chosen = i
                break                
        #nbTot = self.f*self.nbCanc + (self.N-self.nbCanc)        
        #pCanc = self.f*self.nbCanc/nbTot*1.0
        
        if chosen > 0:
            #a cancerous cell was chosen
            if rd.random() <= self.mu:
                #a new cancerous clone is born
                print("cancerous cell mutation!")
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
                print("normal cell mutation!")
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
                print("killing ", killed)
                break
        self.pop[killed] -= 1
        print(self.pop)
        self.history.append(dict(self.pop))
        
    def cancer_detection(self):
        self.cancerous_types = [self.pop[k] for k in list(self.pop.keys()) if k!=0]
        self.nbCanc = sum(self.cancerous_types)
        if self.nbCanc/self.N*1.0 >= self.w:
            return True 
        return False
    
    def run(self, T):
        for t in range(T):
            self.step()
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
                #print(n, tmp)
                if n > tmp:
                    cell += 1
                    tmp += self.history[t][cell]
                #print(cmap(cell)[0:3], cmap(cell)[0:3])
                if cell == 1:
                    color = "blue"
                else:
                    color = "red"
                plt.plot(t, n*0.1, 'x', color = cmap(cell), markersize = 2)
    def plot_pop(self):
        cells = []
        evol = [self.history[i][0] for i in range(len(self.history))]
        plt.plot(evol)

            
s = simu(50, 0.2, 10, f = 4, mu = 0.5)
s.run(30)
s.plot_history()
