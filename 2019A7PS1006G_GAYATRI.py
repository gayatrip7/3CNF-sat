from CNF_Creator import *
import time
import random
import math

def fitness(curr,sentence,fit,maxfitness):
    sat = 0  #number of satisfied clauses
    for j in sentence:
        num = 0   #number of true values
        for k in range(3):
            if (j[k]<0):
                if curr[-j[k]-1] == False:
                    num+= 1
            else:
                if curr[j[k]-1] == True:
                    num+= 1
        if num > 0:
            sat+= 1
    best = []   #best state found
    if (sat > maxfitness):
        for it in range(50):
            if (curr[it]):
                best.append(it+1)
            else:
                best.append(-it-1)
        maxfitness = sat
    fit.append(sat)
    return fit,maxfitness,best

def genetic_algorithm(population):
    cnf = CNF_Creator(n=50)
    sentence = cnf.ReadCNFfromCSVfile()
    subjects = []
    for i in range(population):
        subjects.append(random.choices([True,False], k=population))
    seconds = time.time()
    maxfitness = 0
    while ((time.time()-seconds < 44.5) and not (maxfitness == len(sentence))):
        new_population = []
        fit = []
        combined = []
        for i in subjects:
            fit,temp_maxfitness,temp_best = fitness(i,sentence,fit,maxfitness)
            if (temp_maxfitness > maxfitness):
                maxfitness = temp_maxfitness
                best = []
                for j in range(len(temp_best)):
                    best.append(temp_best[j])
        for i in range(len(subjects)):
            combined.append([fit[i],subjects[i]])
        combined.sort()
        for i in range(len(subjects)-20,len(subjects)):
            new_population.append(combined[i][1])    #to take the most fit 20% of individuals directly to the next generation
        combined = combined[len(subjects)-20:]   #to take the less fit individuals for generating the next generation
        subjects = []
        fit = []
        for i in combined:
            fit.append(i[0])
            subjects.append(i[1])
        for i in range(len(subjects)):
            parent1 = random.choices(subjects,weights=fit)[0]
            parent2 = random.choices(subjects,weights=fit)[0]
            parent3 = random.choices(subjects,weights=fit)[0]
            parent4 = random.choices(subjects,weights=fit)[0]    #generating 4 parents and performing crossover on them
            c1 = random.randint(0,49)
            c2 = random.randint(c1,49)
            c3 = random.randint(c2,49)
            child = parent1[:c1]+parent2[c1:c2]+parent3[c2:c3]+parent4[c3:]
            for j in range(50):
                if (random.randint(1,100) == 1):    #for mutation
                    child[j] = not(child[j])
            sat = 0
            temp,temp_maxfitness,temp_best = fitness(child,sentence,[],maxfitness)  #to check fitness of child
            if (temp_maxfitness > maxfitness):
                maxfitness = temp_maxfitness
                best = []
                for j in range(len(temp_best)):
                    best.append(temp_best[j])
            new_population.append(child)
        subjects = new_population
    return maxfitness/len(sentence),best,len(sentence)


start = time.time()
stor = genetic_algorithm(50)
print("Roll No : 2019A7PS1006G")
print("Number of clauses in CSV file :",stor[2])
print("Best model :",stor[1])
print("Fitness value of best model :",stor[0]*100,"%")
print("Time taken :",time.time()-start,"seconds")
