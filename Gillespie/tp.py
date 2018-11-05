#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:26:24 2018

@author: ocassan
"""

import matplotlib.pyplot as plt
import numpy as np
import random as rd

#gillespie modélise des réactions
#différent des edo car discret et stochastique


def gillespie(x0, k, T, V):
    X = np.zeros((len(x0), T))
    x = x0
    xs = []
    ts = []
    for t in range(0, T):
        lam = [k[0], x[0]*k[1]]
        r_tot = sum(lam)
        delta = np.random.exponential(scale = 1/r_tot, size=1)[0]
        #choose which reaction is going to be done depending on lam
        lam_sum = sum(lam)
        breaks = np.cumsum(lam)/lam_sum
        reaction = 0
        r = rd.random()
        for i, b in enumerate(breaks):
            if r<b:
                reaction = i
                break
        x += V[reaction]        
        xs.append(x[0])
        t += delta
        ts.append(t)
    print(xs)
    plt.plot(xs)
    return X

#V1 = np.array([[1],[-1]])
#gillespie([100], [1, 0.05], 1000, V1)

def gillespie2(x0, k, T, V):
    X = np.zeros((len(x0), T))
    x = x0
    ts = []
    for t in range(0, T):
        lam = [x[0]*x[1]*k[0]]
        print(lam)
        if lam[0]!=0:
            r_tot = sum(lam)
            print("rtot", r_tot)
            delta = np.random.exponential(scale = 1/r_tot, size=1)[0]
            #choose which reaction is going to be done depending on lam
            lam_sum = sum(lam)
            breaks = np.cumsum(lam)/lam_sum
            reaction = 0
            r = rd.random()
            for i, b in enumerate(breaks):
                if r<b:
                    reaction = i
                    break
            x += V[reaction]        
            print(x)
            X[:,t]= x
            t += delta
            ts.append(ts)
        else:
            X[:,t]= x
    for react in range(len(x0)):
        plt.plot(X[react])
    return X

#V2 = np.array([[-1,-1,1]])
#gillespie2([50, 30, 2], [0.00005], 50, V2)

def gillespie3(x0, k, T, V):
    X = np.zeros((len(x0), T))
    x = x0
    ts = []
    for t in range(0, T):
        lam = [x[0]*k[0]]
        print(lam)
        if lam[0]!=0:
            r_tot = sum(lam)
            #print("rtot", r_tot)
            delta = np.random.exponential(scale = 1/r_tot, size=1)[0]
            #choose which reaction is going to be done depending on lam
            lam_sum = sum(lam)
            breaks = np.cumsum(lam)/lam_sum
            reaction = 0
            r = rd.random()
            for i, b in enumerate(breaks):
                if r<b:
                    reaction = i
                    break
            x += V[reaction]        
            print(t)
            X[:,t]= x
            t += delta
            ts.append(t)
        else:
            X[:,t]= x
    print(ts)
    for react in range(len(x0)):
        plt.plot(ts, X[react])
    return X

V3 = np.array([[0,1]])
gillespie3([20,10], [0.005], 100, V3)