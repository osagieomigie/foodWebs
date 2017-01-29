# Osa Omigie
# 30008204
# This program analyzes the food web

import sys
from formatList import formatList

# This creates the animal dictionary
# Parameters: 
#      inf: Input file for reading 
# return:
#      animal dictionary 
def animalDict(inf):
    line = inf.readline()
    animals = {}
    while line != "":
      line = line.rstrip()
      line = line.split(' eats ')
      pred = line[0]
      prey = line[1]
    
      if pred in animals.keys():
        if prey not in animals[pred]:
          animals[pred].append(prey)
      else:
        animals[pred] = [] 
        animals[pred].append(prey) #add extra values to key
    
      #read next line
      line = inf.readline() 
    inf.close()
    return animals

# This outputs preds and preys in a file 
# Parameters: 
#      animals : Takes the animal dictionary
# return:
#     None
def predPrey(animals):
    print('Predators and Prey: ')
    for pred in animals.keys():
      print ('',pred, 'eats', formatList(animals[pred]))

#part 2   
# This outputs the Apex predators in a file 
# Parameters: 
#      animals: Animal dictionary
# return:
#      None
def apexPred(animals):     
    print('Apex Predators: ', end = '')
    apex = []
    for pred in animals.keys():
        isApex = True
        #searches for each pred in list of preys 
        for preys in animals.values():
           if pred in preys:
               # pred is not a apex pred
               isApex = False
               
               break; # ends iteration 
               
        if (isApex) :
             apex.append(pred)  # pred is a apex 
    print(formatList(apex))

#part 3
# This outputs the producers of the file 
# Parameters: 
#      animal: Animal dictionary 
# return:
#      producers 
def getProducers(animals):
    producers = [] #list of producers 
    preds = animals.keys() #predators
    
    for preys in animals.values():
        for prey in preys: #each animal in preys
            if prey not in preds and prey not in producers: #prey not a predator and avoids duplicates 
                producers.append(prey)
        
    return producers

#part 4
# This outputs the flexible animals of the file 
# Parameters: 
#      animal: Animal dictionary 
# return:
#      None
def Flexible(animals):
   #The on with the most list
    flex_pred = []
    max_preys = 0
    
    for pred in animals.keys():
      number_of_preys = len(animals[pred]) #stores length of the list 
      if number_of_preys == max_preys:
        flex_pred.append(pred)
      elif number_of_preys > max_preys :
        max_preys = number_of_preys 
        flex_pred = [pred] # New max pred is stored in flex_pred, the old list is deleted 
    
    print('Most Flexible Eaters:', formatList(flex_pred))

#part 5
# This outputs the tastiest animals of the file 
# Parameters: 
#      animal: Animal dictionary 
# return:
#      None
def Tastiest(animals):
    countTable = getPreyCount(animals)
    tastiest = []
    maxCount = 0
    for prey in countTable.keys():
      currentCount = countTable[prey]
      if currentCount == maxCount:
        tastiest.append(prey)
      elif currentCount > maxCount:
        maxCount = currentCount
        tastiest = [prey]
        
    print('Tastiest:',formatList(tastiest))

# This creates a dictionary for preys and the count of the times it was eaten  
# Parameters: 
#      animal: Animal dictionary 
# return:
#      (countTable) prey:count
def getPreyCount(animals) :
    countTable = {}
    
    for preys in animals.values():
      for prey in preys:
        if prey in countTable.keys():
          countTable[prey] = countTable[prey] + 1 
        else:
          countTable[prey] = 1
    return countTable

#part 6 
# This creates a dictionary for preds and the count of the animals it eats  
# Parameters: 
#      animal: Takes the animal dictionary 
# return:
#      (countTable) pred:count
def getPredCount(animals) :
    countTable = {}
    for pred in animals.keys():
        countTable[pred] = len(animals[pred])
    return countTable

# This gathers data from getPreyCount and getPredCount and merges it   
# along with their corresponding keys and values  
# Parameters: 
#      getPreyCount: Takes the prey count dictionary
#      getPredCount: Takes the pred count dictionary
# return:
#      involvementCount
def mergeDict(dictOne,dictTwo):
    involveCount = {}
    for x in dictOne:
        if x in dictTwo :
            involveCount[x] = dictTwo[x] + dictOne[x]
        else:
            involveCount[x] = dictOne[x]
            
    # ones in pred that are not in prey
    for x in dictTwo:
        if x not in dictOne:
            involveCount[x] = dictTwo[x]
    return involveCount 

# This outputs the most involved animal   
# along with their corresponding keys and values  
# Parameters: 
#      getPreyCount: Takes the prey count dictionary 
#      getPredCount: Takes the pred count dictionary
#      animals: Takes the animal dictionary 
# return:
#      None
def Most_involved(getPreyCount,getPredCount,animals):
    involveCount = mergeDict(getPreyCount(animals),getPredCount(animals))
    mostInvolved = []
    highestCount = 0
    for x in involveCount:
        xValue = involveCount[x] #get value of animal 
        if xValue > highestCount: 
            highestCount = xValue 
            mostInvolved = [x] # assigns animal to most involved
        elif xValue == highestCount:
            mostInvolved.append(x) #add animal to most involved 
            
    print('Most Involved Organism:',formatList(mostInvolved))


# part 7 
# Finds all the predators of the given prey 
# Parameters: 
#      animal: Takes the animal dictionary
#      prey: Takes a prey
# return:
#      predators 
def predatorsOf(prey, animals) :
  predators = []
  for pred in animals.keys():
    if prey in animals[pred] and pred not in predators:
      predators.append(pred)
  return predators


# This outputs the longest path from an organism to a producer  
# Parameters: 
#      animal: Takes the animal dictionary
# return:
#      None 
def printHeight(animals) :
  heights = {}

  heights = mergeDict(getPreyCount(animals),getPredCount(animals))
  producers = getProducers(animals)

  # Initializations
  for pred in heights:
    if pred in producers :
       heights[pred] = 0
    else : 
       heights[pred] = None
       
  # Producers already have a height of 0
  lastVisited = [x for x in getProducers(animals)] # add producers to list of visited organisms
  visited = [x for x in getProducers(animals)]

  traverse(lastVisited, visited, heights, animals)

  print('Heights:')
  for organism in heights :
    print(' ',organism,':\t',heights[organism])

# Recursively finds the height of all the organisms in the lastvisited list and updates the heights dictionary  
# Parameters: 
#      animal: Takes the animal dictionary
#      lastVisited: List of organisms that their heights were previously calculated
#      visited: List of organisms in the heights dictionary that their heights have already been #    
#       calculated/determined
#      heights: Dictionary containing the heights of every organism  
# return:
#      None  
def traverse(lastVisited, visited, heights, animals):
  if len(lastVisited) < 1 :
    return

  newLastVisited = []
  for prey in lastVisited: # goes through organisms that their heights were last calculated 
    for pred in predatorsOf(prey,animals) : # goes through predators of last visited (i.e who eats the lastvisited organism)

      if pred not in newLastVisited:
        newLastVisited.append(pred) #add to new last visited list
        heights[pred] = heights[prey] + 1
  visited.extend(newLastVisited) # adding content of 'newLastVisited' list to 'visited' list
  if len(newLastVisited) :
    traverse(newLastVisited,visited, heights, animals)
      
# Runs the whole file  
# Parameters: 
#      None
# return:
#      None
def main():
  try:
   # print("sys.argv[0]" , sys.argv[0]) #/path/to/Aquatic
   if len(sys.argv) == 2:
     filename = sys.argv[1]

   elif len(sys.argv) > 2:
     print('Program accepts only one commmand line')
     quit()

   else:
     filename = input('Enter file name: ')

  except:
    print("input",sys.argv[0],"along with correct file name, or just input file name")
    quit()


  try:
    inf = open(filename, "r")
    animals = animalDict(inf)
    #part1
    predPrey(animals)
    print()
    #part2
    apexPred(animals)
    #part3
    prod = getProducers(animals)
    print('Producers:',formatList(prod))
    #part4
    Flexible(animals)
    #part5
    Tastiest(animals)
    #part6
    Most_involved(getPreyCount,getPredCount, animals)
    print()
    #part7
    printHeight(animals)

  except:
    print('Invalid entry')
    quit()



main()


