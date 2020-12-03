# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:26:04 2020

@author: sarah
"""
'''
	Algorithme de Génétique appliquée au problème du voyageur de commerce
	Genetic algorithm for Traveling Salesman Problem
'''


import numpy as np
#import operator
#import Graph2
import math
import random
import copy
import time
from plot import plot
'''
	Algorithme de Génétique appliquée au problème du voyageur de commerce
	Genetic algorithm for Traveling Salesman Problem
'''


    

class GènètiqueAlgorithmeTSP:
    def __init__(self, générations=10, taille_population=20, tournamenttaille=20, probmutation=0.1, probelitism=0.1,villes=16):
        self.générations = générations
        self.taille_population = taille_population
        self.tournamenttaille = tournamenttaille
        self.probmutation = probmutation
        self.probelitism = probelitism
        self.villes=villes
    def __A(self,c):
        s=0
        for i in range(len(c)-1):
            #print('la somme',math.sqrt((x[c[i]]-x[c[i+1]])**2+(y[c[i]]-y[c[i+1]])**2))
            s=s+math.sqrt((x[c[i]]-x[c[i+1]])**2+(y[c[i]]-y[c[i+1]])**2)
            
        s=s+math.sqrt((x[c[0]]-x[c[-1]])**2+(y[c[0]]-y[c[-1]])**2)
        return(s)
   
    def __recherche_local(self,enfant,v=[],c=[],enfant_1=[],F=[]):
      enfant_1=enfant
      for i in range(len(enfant_1)-1):
       #a=[]
       #print('la sol i=',i, enfant)
         for j in range(i+1,len(enfant_1)):
           a=[]
           #print('la sol j=',j)
           k=i
           while(k<=j):
             #print('est cas',enfant[k])
             a.append(enfant_1[k])
             #print(a)
             k=k+1  
           a.reverse()
           #print('a=',a)
           l=0
           #print('i,j,enfant',i,j,enfant)
           c = copy.copy(enfant_1)
           for k in range(i,j+1):
              # print('a[k]',a[l])
               c[k]=a[l]
               l=l+1
           f=self.__A(c)
           F.append(f)
           #print('c=',c)
           v.append(c)
      F_k=(min(F))
      a=F.index(F_k)
      #print(v[a],F[a])        
      return(v[a])

    
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
            fittest = np.argmin(fitness)
            if elitismOffset:
                elites = np.array(fitness).argsort()[:elitismOffset]
                [novelPopulation.append(population[i]) for i in elites]
            for gen in range(elitismOffset, self.taille_population):
                parent1 = self.__tournamentSelection(population)
                parent2 = self.__tournamentSelection(population)
                arretspring = self.__croissement(parent1, parent2)
                arretsprin=self.__recherche_local(arretspring ,v=[],c=[],enfant_1=[],F=[])
                novelPopulation.append(arretsprin)
            for gen in range(elitismOffset, self.taille_population):
                novelPopulation[gen] = self.__mutate(novelPopulation[gen])
            population = novelPopulation
        return (population[fittest], fitness[fittest])

    def __prodPopulation(self,prodpopulation=[]):
       #print(A)
       for i in range(self.taille_population):
           a=[]
           while len(a)!=self.villes:
               c=random.randint(0,self.villes-1)  
               if c not in a:
                 a.append(c)
           prodpopulation.append(a)
       return (prodpopulation)
       
        
    
    def __calculeFitness(self,population):
        return [self.donnecoutparcour(parcour) for parcour in population]

    def __tournamentSelection(self, population):
        tournament_contestants=[]
        tournament_contestants_fitness=[]
        for i in range(self.tournamenttaille):
           a=random.randint(0,len(population)-1)
           tournament_contestants.append(population[a])
        tournament_contestants_fitness.append(self.__calculeFitness(tournament_contestants))
        return tournament_contestants[np.argmin(tournament_contestants_fitness)]

    def __croissement(self, parent1, parent2):
        arretspring = ['' for allele in range(len(parent1))]
        indice_un, indice_deux = self.__calculeundeuxIndices(parent1)
        
        arretspring[indice_un:indice_deux+1] = list(parent1)[indice_un:indice_deux+1]
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
    #B=[]
    
    debut=time.time()
    x = []
    y = []
    with open('./data/ulysses16.tsp') as f:
           for line in f.readlines():
             #print(line)
             city = line.split(' ')
             #print(city)
             x.append(float(city[1]))
             y.append(float(city[2]))
    for i in range(1):
        print('iteration',i+1)
        ga_tsp = GènètiqueAlgorithmeTSP(générations=100, taille_population=40, tournamenttaille=20, probmutation=0.2, probelitism=0.1,villes=16)
        #d = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23, 'x':24, 'y':25, 'z':26, 'A':27, 'B':28, 'C':29, 'D':30, 'E':31, 'F':32, 'G':33, 'H':34, 'I':35, 'J':36, 'K':37, 'L':38, 'M':39, 'N':40, 'O':41, 'P':42}
        parcour_optimal, cout_parcour = ga_tsp.optimise()
        print(cout_parcour)
        #if(parcour_optimal[0]!=parcour_optimal[-1]):
           #a=parcour_optimal[0]ulysses16.tsp
           #parcour_optimal=parcour_optimal+a
        #B.append(cout_parcour)
        parcouroptimal=[]
        for i in range(len(parcour_optimal)):
            a=parcour_optimal[i]+1
            parcouroptimal.append(a)
        parcouroptimal.append(parcouroptimal[0])
        print('La mellieur solution trouver est:')
        print ('Solution finale par l algorithme Mémitique: %s | le coût: %f\n' % (' -> '.join(str(i) for i in parcouroptimal),cout_parcour))
    parcour_optimal.append(parcour_optimal[0])
    fin=time.time()
    print('terminer le temps d execution=',fin-debut)
    x=[]
    y=[]
    points=[]
    with open('./data/ulysses16.tsp') as f:
           for line in f.readlines():
             #print(line)
             city = line.split(' ')
             #print(city)
             x.append(float(city[1]))
             y.append(float(city[2]))
             points.append((float(city[1]), float(city[2])))
    plot(points, parcour_optimal)

