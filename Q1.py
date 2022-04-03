import math #import math the help calculate heursitic 
from copy import deepcopy #import function used the make a copy of a state
import time #import time to help us calculate run time

class Node:
    def __init__(self, state, parent, gen , h, movement): #initialization requires this informantion
        self.state = state #current config of node
        self.parent = parent #points to parent node 
        self.h = h #cost to the end position (heuristic)
        self.mov = movement #direction from last move as a string
        self.gen = gen #generation of node 
     
    def f(self): #class function to calculate approximation cost 
        return self.gen + self.h # f= g + h     
    
    ##class function to generate legal move that the current node can take
    def Generate_Children(self):
        directions = {"Up": [-1,0], "Down": [1,0], "Left": [0,-1], "Right" : [ 0, 1]} #Dictionary on each legal move and how that would affect the 0 cooridnate
        empty = FindElement(self.state, 0) # find location of the space
        validchildren = [] #new possible children
        for x in directions.keys(): #for every direction try and move the space
            move = (empty[0] + directions[x][0], empty[1] + directions[x][1]) #move the space location depenant on the attempted move
            if 0 <=  move[0] < n: #if the new location of the space is still on the board 
                if 0 <= move[1] < n: #then the move if valid 
                    newState = deepcopy(self.state) #take a copy of the the current state
                    newState[empty[0]][empty[1]] = self.state[move[0]][move[1]] # swap the space and moved piece
                    newState[move[0]][move[1]] = 0 
                    validchildren += [Node(newState, self.state, int(self.gen) +1, Cost(newState,goal), x )] #create a node class with with all the correct information for all the new explored locations
        return validchildren #return the valid moves

def solution(closedlist): #this function is called when the goal state is found
        path = closedlist[str(goal)] #starting with the goal state 
        route = [] #set up an path
        notdone = True 
        while notdone == True : #loops until we backtrack to the initial state
            route = [path] + route #add the new node to the parent node to the front of the route
            if path.gen == 0: # we have reached the start note 
                notdone = False #leave the 
                break
            previous = closedlist[str(path.parent)]
            path = previous
        return route   

def Cost(current,goal): #function to help the program calculate heuristics
    cost = 0 #reset cost
    if select == 0: #if manhatten is chosen 
        cost = ManhattenCost(current,goal) #use manhattan to approximate
    elif select == 1: #if euclidean is chosen 
        cost = EuclideanCost(current,goal) #use Euclidean to approximate
    else:
        print("Error: Function not defined correctly") #error message if something has gone wrong
    return cost #return approximation 
#Hueristic function 1
def ManhattenCost(current,goal): #Manhattan Distance approximation
        cost = 0  #reset cost
        for i in range(len(current)): #for every row 
            for j in range(len(current[0])): #for every columm
                pos = FindElement(goal, current[i][j]) # find the location of the current element in the goal state 
                #manhattan distance for this tile
                cost += abs(i - pos[0]) + abs(j - pos[1])
        return cost #return the total manhattan distance
#Heuristic function 2
def EuclideanCost(current, goal): #euclidean distance approximation
        cost = 0  #reset cost 
        for i in range(len(current)): #for every row 
            for j in range(len(current[0])): #for every column in that row
                pos = FindElement(goal, current[i][j]) #find element in goal state
                #calculate euclidean distance
                cost += math.sqrt( (i - pos[0])**2 + (j - pos[1])**2)
        return cost #return total euclidean distance

def FindElement(state,elem):#functions finds an element in a given state
    for row in range(len(state)): #check every row
        if elem in state[row]: #if element is in that row
            return (row,state[row].index(elem)) #return co-ordinates

def getbestnode(openlist): #function to find the approxiate closest node to the solution
    firstIter = True # for first value
    for node in openlist.values(): #checks every value in the dictorary 
        # for first time and when the approximate is better 
        if firstIter or node.f() < bestF: # if next node is approximately closer or is first node
            firstIter = False #make sure that not every value is accpected
            bestNode = node #the new node is the best node to explore 
            bestF = bestNode.f() #reset the bar
    return bestNode #return best choice of node

def pprint(finalpath): #function to print the final path
    if finalpath == []: #if no solution was found then print
        print("No solution was found")
    while finalpath != []: #as long as the path in none empty
        next = finalpath[0] #take the next move 
        print("\n") #and print out the required information
        print("Step " + str(next.gen) + ": " + str(next.mov)) #nice formating 
        for x in range(n): #for every row 
            print("| " , end = '') #print border 
            for x2 in range(n): #for every columm 
                print( str(next.state[x][x2]) + " " , end = ' ' ) #print the element for that given location in that step
            print(" |") #print border
        del finalpath[0] #remove the print step for the list so we can print the next step

class puzzle: 
    def __init__(self,size):
        """ Initialize the puzzle size by the specified size"""
        self.n = size

        
    def accept(self):
        """ Accepts the puzzle from the user """
        puz = [] #empty puzzle value
        for i in range(n): #for every row  
            temp = [] #empty row value 
            for x in range(n): #for every columm
                temp.append(int(input("(" + str(i+1) + ", " + str(x+1)+ "): "))) # add entry in loaction i x 
            puz.append(temp) #add the row to puzzle
        return puz #return the whole completed puzzle
    
    
    def solve(self): #class function 
        global select #declering global variable goal state to be used in a few functions
        valid = False #acceptance critea 
        while valid == False: #Repeat untill we have a valid input 
            print("Please select mode: Manhattan (0) or Euclidean (1)") #print instructions\help
            select = int(input()) #takes the user input
            if select == 0 or select == 1 : #if the input has selected is valid 
                valid = True #accept answer 

        print("Enter the Start state matrix") #Printing instructions for user
        #Calling the class function accept which gets the user to input the start state
        start = self.accept() #a #a2 #This can be change depending on which grid option the user wants
        print("Enter the Goal state matrix") #Printing instructions for user 
        global goal #declering global goal state to be used in a few functions
        #Calling the class function accept which gets the user to input the goal state
        goal =  self.accept() #b #b2 #This can be change depending on which grid option the user wants
        tic = time.time() #timer 'start'
        closedlist = {} #list of looked upon nodes
        openlist = {str(start) : Node(start, None, 0, Cost(start,goal) , None) }
        #create the dictionary of unexplored  nodes starting with the initial state and its information
        finalpath= [] #empty final path
        while len(openlist) > 0: #while we have some unchecked nodes 
            testnode = getbestnode(openlist) # find the best approximation for closest to solution            
            closedlist[str(testnode.state)] = testnode #add the best node to the list of looked nodes
            if testnode.state == goal: # if the selected node is the same as the goal then we have found the solution 
                finalpath = solution(closedlist) #recreate the solution path using the fuction solution
                break #break the loop as solution is found
            newmoves =  Node.Generate_Children(testnode) #call the function to genereate new grids based on the current best           
            del openlist[str(testnode.state)]#delete the checked node from the unchecked list
            for node in newmoves: #check to see if newmove is good
                #if the node is already been generated by solution that route in not optimal 
                #so not worth investigating so skip to next possible move
                if str(node.state) in closedlist.keys() or str(node.state) in openlist.keys() and openlist[str(node.state)].f() < node.f():
                    continue
                openlist [str(node.state)] = node # add the new config to the Dictionary with all the infomation
        pprint(finalpath) #printing the solution in a suitable format 
        toc = time.time() #time 'stop' 
        timez = toc - tic #calculate difference in time between start and finish 
        print("The program took " + str(round(timez,3)) + " seconds") 
        print("Closed list length: " + str(len(closedlist))) #Printing results 
        print("Open list length: " + str(len(openlist)))


#Pre made Inital and Goal states for Q1.2.3
# later replace by inputed states 
a = [[7,2,4],[5,0,6],[8,3,1]]
b = [[0,1,2],[3,4,5],[6,7,8]]
#Testing of larger more complex grids
a2 = [[7,2,4,11],[5,0,6,12],[8,3,1,13],[9,10,14,15]]
b2 = [[0,1,2,11],[3,4,5,12],[6,7,8,13],[9,10,14,15]]
#start progam
print("Welcome to 8 Puzzle Solver") #welcome message 
n = int(input("Enter the puzzle size: ")) # select the puzzle size 
#create an instance of the class puzzle of size n given
test=puzzle(n)
test.solve() #call the class function to start the puzzle process