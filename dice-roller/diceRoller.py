# - - - - - - - - - - - #
# This program allows   #
# you to roll different #
# kinds of dice         #
# - - - - - - - - - - - #

import random
import re

def dice(args):
    #converts all the arguments the user passes into a list
    argsList = args.split()
    if len(argsList) == 0:
        print("Please enter dice to roll")
        return
    
    for i in argsList:
        matched = re.match("^[0-9]+d[0-9]+$", i) #regex checks dice formatting
        is_match = bool(matched)
        if is_match == False:
            #if the input doesn't match, lets the user know and returns
            print("Please enter a valid die") 
            return
    sum = 0
    rolls = []
    for i in range(len(argsList)):
        #splits the index of argsList into two numbers, splicing at 'd'
        entry = argsList[i].split('d') 
        #repeats the dice roll for a number of times equal to the first index of the split
        for i in range(int(entry[0])): 
            #rolls a dice with the number of sides equal to the second index of the split
            roll = random.randint(1,int(entry[1])) 
            rolls.append(roll)
            sum += roll
    #sends a message containing the rolls and the sum of all the rolls
    print("Rolls: "+', '.join(map(str,rolls))+"\nSum: "+str(sum)) 

while True:
    inp = input(str("Dice: "))
    if inp == "":
        break
    else:
        dice(inp)

