import os
import sys
import copy
import queue as Q
#from sets import Set
import datetime
import math

# To print the puzzle in 2d matrix
def print_state(state):
    for i in range(len(state)):
        print(state[i])
        if i == len(state) - 1:
            print("")

# To print the items(state and cost of the node) in queue or pq for debugging purpose
def print_queue(q):
    print("Current queue:")
    for item in q.queue:
        print(str(item.state) + "  cost: " + str(item.cost))
    print("")


'''
Node in the search space.
@param parent: parent of the current node
@param action: action to be taken from parent state to child state
@param state: 2d matrix, a state representation of the n-puzzle
@param zero0: x-coordinate of the "0" in the puzzle
@param zero1: y-coordinate of the "0" in the puzzle
@param action_list: list of possible actions from the current state
@param cost:
@param heuristic: expected cost from current state to goal
@param f: evaluation function, passing through this node, the expected cost from init to goal
'''
class Node(object):
    def __init__(self, parent, action):
        self.parent = parent
        self.action = action
        self.action_list = ["UP", "RIGHT", "DOWN", "LEFT"]
        self.heuristic = 0      # to be computed
        self.f = 0              # to be computed
        if (parent == None):
            self.generate_init_node()
        else:
            self.generate_child_node()
            # self.debug_child_node()

    def debug_child_node(self):
        # print(self.parent.state)
        print(self.action)
        print(str(self.state) + "  cost: " + str(self.cost))
        # print(self.action_list)
        

    # comparator for priority queue
    def __lt__(self, other):
        return self.f < other.f

    def find_zero(self):
        for i in range(n):
            for j in range(n):
                if (init_state[i][j] == 0):
                    self.zero0 = i
                    self.zero1 = j

    def generate_init_node(self):
        self.state = copy.deepcopy(init_state)
        self.find_zero()
        self.generate_action() 
        self.cost = 0
        self.compute_f()
        # self.g = 0
        # self.h = self.compute_heuristic()
        # self.cost = self.g + self.h

    def generate_child_node(self):
        self.state = copy.deepcopy(self.parent.state)
        self.generate_child_state(self.parent.zero0, self.parent.zero1)
        self.generate_action()
        self.cost = self.parent.cost + 1
        self.compute_f()
        # self.g = self.parent.cost + 1
        # self.h = self.compute_heuristic()
        # self.cost = self.g + self.h
             
    # transition model/function
    # to generate child state based on parent state and input action
    def generate_child_state(self, zero0, zero1):
        if self.action == "LEFT":
            self.state[zero0][zero1] = self.state[zero0][zero1 + 1]
            self.state[zero0][zero1 + 1] = 0
            self.zero1 = zero1 + 1
            self.zero0 = zero0
            
        elif self.action == "RIGHT": 
            self.state[zero0][zero1] = self.state[zero0][zero1 - 1]
            self.state[zero0][zero1 - 1] = 0 
            self.zero1 = zero1 - 1
            self.zero0 = zero0

        elif self.action == "UP": 
            self.state[zero0][zero1] = self.state[zero0 + 1][zero1]
            self.state[zero0 + 1][zero1] = 0 
            self.zero0 = zero0 + 1
            self.zero1 = zero1
            
        elif self.action == "DOWN":    
            self.state[zero0][zero1] = self.state[zero0 - 1][zero1]
            self.state[zero0 - 1][zero1] = 0
            self.zero0 = zero0 - 1
            self.zero1 = zero1

        else:
            return

    # to generate list of possible actions from the current state
    def generate_action(self):
        if self.zero0 == 0:
            self.action_list.remove("DOWN")
        if self.zero0 == n - 1:
            self.action_list.remove("UP")
        if self.zero1 == 0:
            self.action_list.remove("RIGHT")
        if self.zero1 == n - 1:
            self.action_list.remove("LEFT")

    # to generate heuristic value
    def compute_heuristic(self):
        width = len(self.state[0])
        hue = 0
        for row_num, row in enumerate(self.state):
            for col_num, col in enumerate(row):
                (goal_row, goal_col) = divmod(col, width)
                goal_col -= 1
                hue += abs(goal_row - row_num)
                hue += abs(goal_col - col_num)
        self.heuristic = hue

    # using evaluation function to compute expected total cost
    def compute_f(self):
        self.compute_heuristic()
        self.f = self.cost + self.heuristic
        #print(self.f)
'''
    def __cmp__(self, other):
        if self.f < other.f:
            return -1
        elif self.f == other.f:
            return 0
        else:
            return 1
            '''

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        ## you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        # self.actions = ["UP", "RIGHT", "DOWN", "LEFT"]
                    
    def solve(self):
        ##TODO
        ##implement your search algorithm here
        
        success = False
        start = datetime.datetime.now()

        ## To implement graph-search
        visited = set()
        
        ## To implement BFS, FIFO Queue
        #q = Q.Queue()
        ## To implement DFS, LIFO Queue, may not terminate, due to infinite depth on tree search
        # q = Q.LifoQueue() 
        ## To implement UCS
        # q = Q.PriorityQueue()
        ## To implement A*
        pq = Q.PriorityQueue()

        # generate initial node, add it into the frontier
        node = Node(None, "NONE")
        pq.put(node)
        
        while(not pq.empty()):
            ## for debugging purpose 
            # print_queue(q) 

            node = pq.get()

            ## To implement graph-search
            visited.add(str(node.state))
            
            # print("Pop and expand:")
            print(node.state)
            print(node.cost)
            # print("")
            
            # print("Explored set:")
            # print(visited)
            # print("")

            ## goal test
            if (node.state == self.goal_state):
                print("Success: Goal found!")
                success = True
                end = datetime.datetime.now()
                break

            ## Expand the node, add all its successors/child_nodes into frontier  
            # print("Generating child_node:")
            for i in range(len(node.action_list)):
                child_node = Node(node, node.action_list[i])
                # q.put(child_node)
                ## implementing graph-search, not adding visited node 
                if not str(child_node.state) in visited:
                    pq.put(child_node)
                #pq.put(child_node)
                # else:
                #     print("visited, not added to frontier")
                # print("")

        solution_path = []
        if success:
            print("Depth of goal: " + str(node.cost))
            ## backtracking from goal node to init node, to find the solution path        
            while(node.parent != None):
                solution_path.append(node.action)
                node = node.parent
            solution_path.reverse()
        else:
            print("Max Depth: " + str(node.cost))
            end = datetime.datetime.now()
            print("UNSOLVABLE")
            solution_path = ["UNSOLVABLE"]

        print("Number of visited nodes: " + str(len(visited)))
        print("Start time: " + start.strftime("%Y-%m-%d %H:%M:%S"))
        print("End time  : " + end.strftime("%Y-%m-%d %H:%M:%S"))
        print("Time taken: " + str(end - start))    

        return solution_path


if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = 2 to the power of n - 1 Typo 
    max_num = n**2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    
    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0


    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    # 'a' means append, 'w' means 'overwrite' 
    # change 'a' to 'w', if u want to overwrite the content in the output file 
    with open(sys.argv[2], 'w') as f:
        for answer in ans:
            f.write(answer+'\n')
