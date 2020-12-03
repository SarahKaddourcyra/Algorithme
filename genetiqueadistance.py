"""
Created on Thu Oct 29 15:26:04 2020

@author: sarah
"""
# -*- coding: utf-8 -*-
'''
	Algorithme de Génétique appliquée au problème du voyageur de commerce
	Genetic algorithm for Traveling Salesman Problem
'''


import numpy as np
import math
import random
#import copy
import time
from plot import plot

    

class GènètiqueAlgorithmeTSP:
    def __init__(self, générations=10, taille_population=20, tournamenttaille=20, probmutation=0.1, probelitism=0.1,villes=42):
        self.générations = générations
        self.taille_population = taille_population
        self.tournamenttaille = tournamenttaille
        self.probmutation = probmutation
        self.probelitism = probelitism
        self.villes=villes
    def __A(self,c):
        s=0
        x = []
        y = []
        points=[]
        with open('./data/att16.txt') as f:
           for line in f.readlines():
             #print(line)
             city = line.split(' ')
             #print(city)
             x.append(int(city[1]))
             y.append(int(city[2]))
             points.append((int(city[1]), int(city[2])))
        for i in range(len(c)-1):
            #print('kkjdbkdbd',c[i],c[i+1])
            s=s+math.sqrt((x[c[i]]-x[c[i+1]])**2+(y[c[i]]-y[c[i+1]])**2)
          
        s=s+math.sqrt((x[c[0]]-x[c[-1]])**2+(y[c[0]]-y[c[-1]])**2)
        return(s)
    
    def donnecoutparcour(self,parcour):# la longeur(le cout) de parcour 
        #print(parcour, len(parcour))
        S=self.__A(parcour)
        #print('A',parcour)
        coutparcour = S
        return coutparcour
    
    
    def optimise(self):
        population = self.__prodPopulation(prodpopulation=[])
        #for v in range(len(population)):
            #population[v]=population[v]+(population[v][0])
        elitismOffset = math.ceil(self.taille_population*self.probelitism)

        if (elitismOffset > self.taille_population):
            raise ValueError('Elitism Rate must be in [0,1].')
        
        #print ('Optimisation De Parcours Du PVC(TSP) Pour Le Graphe:\n{0}'.format(graphe))

        for génération in range(self.générations):
            #if(génération!=19):
               #print ('\nGènèration: {0}'.format(génération + 1))
            #if (génération== self.générations-1):
               #for v in range(len(population)):
                  #population[v]=population[v]+(population[v][0])
               #print ('\nGènèration: {0}'.format(génération + 1))
               #print ('Population: {0}'.format(population))
            
            novelPopulation = []            
            fitness = self.__calculeFitness(population)
            #if (génération== self.générations-1):
               # print ('La Fonction Fitness: {0}'.format(fitness))
            fittest = np.argmin(fitness)

            #print ('Le Meilleur Parcours  : {0} ({1})'.format(population[fittest], fitness[fittest]))
            
            if elitismOffset:
                elites = np.array(fitness).argsort()[:elitismOffset]
                [novelPopulation.append(population[i]) for i in elites]
               # for v in range(len(population)):
                   #population[v]=population[v]+(population[v][0])
            for gen in range(elitismOffset, self.taille_population):
                parent1 = self.__tournamentSelection(population)
                parent2 = self.__tournamentSelection(population)
                #parent2[0]='a'
                arretspring = self.__croissement(parent1, parent2)
                #arretsprin=self.__recherche_local(arretspring ,v=[],c=[],enfant_1=[],F=[])
                novelPopulation.append(arretspring)
                #print ('\nParent 1: {0}'.format(parent1))
                #print ('Parent 2: {0}'.format(parent2))
                #print ('arretspring: {0}\n'.format(arretspring))
            for gen in range(elitismOffset, self.taille_population):
                novelPopulation[gen] = self.__mutate(novelPopulation[gen])
            
            population = novelPopulation
           
            #if (self.générations==20):
                #for v in range(len(population)):
                   #population[v]=population[v]+(population[v][0])
               
            
        return (population[fittest], fitness[fittest])


    def __prodPopulation(self,prodpopulation=[]):
       #print(A)
       for i in range(self.taille_population):
           a=[]
           while len(a)!=self.villes:
               c=random.randint(0,self.villes-1)  
               if c not in a:
                 a.append(c)
           #print('aaaaaaa',a)   
           prodpopulation.append(a)
       #print('prodpopulation',prodpopulation)
       return (prodpopulation)
       
        
    
    def __calculeFitness(self,population):
        #print([self.donnecoutparcour(parcour) for parcour in population])
        return [self.donnecoutparcour(parcour) for parcour in population]

    def __tournamentSelection(self, population):
        tournament_contestants=[]
        tournament_contestants_fitness=[]
        for i in range(self.tournamenttaille):
           a=random.randint(0,len(population)-1)
           tournament_contestants.append(population[a])
           tournament_contestants_fitness.append(self.__calculeFitness(tournament_contestants))
        #print(tournament_contestants[np.argmin(tournament_contestants_fitness)])
        return tournament_contestants[np.argmin(tournament_contestants_fitness)]

    def __croissement(self, parent1, parent2):
       # print('parent1, parent2',parent1, parent2)
        arretspring = ['' for allele in range(len(parent1))]
        indice_un, indice_deux = self.__calculeundeuxIndices(parent1)
        
        arretspring[indice_un:indice_deux+1] = list(parent1)[indice_un:indice_deux+1]
        #j=0
        arretspring_available_indice = list(range(0, indice_un)) + list(range(indice_deux+1, len(parent1)))        
        for allele in parent2:
            if '' not in arretspring:
                break
            if allele not in arretspring:
                arretspring[arretspring_available_indice.pop(0)] = allele
        return (arretspring) 


    def __mutate(self, genome):
        if np.random.random() < self.probmutation:
            indice_un, indice_deux = self.__calculeundeuxIndices(genome)
            return self.__swap(indice_un, indice_deux, genome)
        else:
            return genome


    def __calculeundeuxIndices(self, int):
        indice_un = np.random.randint(1, len(int)-2)
        indice_deux = np.random.randint(indice_un+1, len(int))
        while indice_deux - indice_un > math.ceil(len(int)//2):
            try:
                indice_un = np.random.randint(1, len(int)-2)
                indice_deux = np.random.randint(indice_un+1, len(int)-1)
            except ValueError:
                pass
        return (indice_un, indice_deux)


    def __swap(self, indice_un, indice_deux, int):
        int = list(int)
        int[indice_un], int[indice_deux] = int[indice_deux], int[indice_un]
        return (int)
    #def __converged(self, population):
        #return all(genome == population[0] for genome in population)
if __name__ == '__main__':
    debut=time.time()
   
    for i in range(1):
        print('iteration',i+1)
        ga_tsp = GènètiqueAlgorithmeTSP(générations=200, taille_population=100, tournamenttaille=10, probmutation=0.2, probelitism=0.1,villes=16)
        #d = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23, 'x':24, 'y':25, 'z':26, 'A':27, 'B':28, 'C':29, 'D':30, 'E':31, 'F':32, 'G':33, 'H':34, 'I':35, 'J':36, 'K':37, 'L':38, 'M':39, 'N':40, 'O':41, 'P':42}
        parcour_optimal, cout_parcour = ga_tsp.optimise()
        #if(parcour_optimal[0]!=parcour_optimal[-1]):
           #a=parcour_optimal[0]
           #parcour_optimal=parcour_optimal+a
        
        parcouroptimal=[]       
        for i in range(len(parcour_optimal)):
            a=parcour_optimal[i]+1
            parcouroptimal.append(a)
        parcouroptimal.append(parcouroptimal[0])
        print('La mellieur solution trouver est:')
        print ('Solution finale par l algorithme Génétique: %s | le coût: %d\n' % (' -> '.join(str(i) for i in parcouroptimal),cout_parcour))
    fin=time.time()
    print('terminer le temps d execution=',fin-debut)
    x=[]
    y=[]
    points=[]
    with open('./data/att16.txt') as f:
           for line in f.readlines():
             #print(line)
             city = line.split(' ')
             #print(city)
             x.append(int(city[1]))
             y.append(int(city[2]))
             points.append((int(city[1]), int(city[2])))
    plot(points, parcour_optimal)
