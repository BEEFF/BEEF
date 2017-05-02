# QES Maps by Thomas O'Keeffe #
# Version 3: FINAL Adapted Console Based Program to Work with User Interface #

''' Import Modules '''
import pickle

class Node:                                             # Start Node Class #
    def __init__(self, NodeName,x,y):               
        self.ID = NodeName                              # ID of node is set to User Inputted NodeName
        self.Connections = {}                           # Create a dictionary for all the connected nodes
        self.x = x                                      
        self.y = y                                      # Create co-ordinate varibles for each node

    def GetXandY(self):
        return self.x,self.y                            # Method for returning x and y nodes

    def AddConnection(self, Neighbour, Weight):         # Add a connection to the node to it's neighbour
        self.Connections[Neighbour] = Weight            # Add the weight of the connection as the dictionary value

    def DeleteConnection(self, NodeToDelete):           # Method for deleting a connection between two nodes
        NewConnections = {}
        for EachConnection in self.Connections:         # Loop through each nodes connection until the neighbouring node is found
            if EachConnection.GetID() == NodeToDelete:
                del EachConnection                      # Delete the connection
                print "Deleted connection"
            else:
                NewConnections[EachConnection] = self.Connections[EachConnection]
        self.Connections = NewConnections

    def RenameConnection(self, OldNode, NodeToRename):                              # Method for renaming a connected node
        NewConnections = {}
        for EachConnection in self.Connections:
            if EachConnection.GetID() == OldNode:                                   # Loop through connections of node until desired node is found
                NewConnections[EachConnection] = self.Connections[EachConnection]   # Change the name of the connected node
                print "Renamed Node"
        self.Connections = NewConnections
        
    def ViewConnections(self):  #Returns the Connections dictionary of the node
        return self.Connections

    def DoesConnectionExist(self, OtherNode):           # Returns true or false depending on whether node is connected to specified node
        ConnectionExists = False
        for EachConnection in self.Connections:         # Iterates through each connected node until specified node is found
            if EachConnection == OtherNode:             # If the node is found, true is returned
                ConnectionExists = True                 # If no node is found, no connection exists and hence false is returned
        return ConnectionExists

    def GetID(self):                        #Method for returning ID  of a certain node
        return self.ID

    def GetWeight(self, Neighbour):         #Method that returns the weight of a connection to a specified node
        return self.Connections[Neighbour]

    def __iter__(self):
        return iter(self.Connections.values())      #Iterates through each connection value until the desired value is found


''' Start Graph Class '''

class Graph:
    def __init__(self):                     # Graph class contains a series of instances of the Node class as well as methods and attributes
        self.NodeList = {}                  # Private Attributes defined
        self.NoOfNodes = 0

    def AddNode(self, NodeName, x,y):       # Method for adding a node to the graph
        self.NoOfNodes += 1                 # Number of nodes incremented by 1
        NewNode = Node(NodeName,x,y)        # Create an instance of the node class with shown parameters and set this to NewNode
        self.NodeList[NodeName] = NewNode   # Add this to the NodeList dictionary
        print "Succesfully added node. "
        return NewNode

    def GetNode(self,Node):                 # Get Node method returns a node if it exists in node list
        if Node in self.NodeList:
            return self.NodeList[Node]
        else:
            print "Node doesn't exist! "    # Error message printed if node doesn't exist
            return None


    def AddEdge(self,NodeA,NodeB, Weight):      # Add edge creates a connection between two nodes
        if NodeA not in self.NodeList:      
            self.AddNode(NodeA)
        if NodeB not in self.NodeList:          # Add quick facility to add new node if node doesn't already exist
            self.AddNode(NodeB)
        
        self.NodeList[NodeA].AddConnection(self.NodeList[NodeB], Weight)
        self.NodeList[NodeB].AddConnection(self.NodeList[NodeA], Weight)

    def RemoveNode(self, NodeName):      #method that deletes the inputted node, if it exists
        Valid = False
        if NodeName == "":
            NodeName = raw_input("Enter the ID you wish to delete from the graph. ")    # Get the name of the specified node to delete

        while not Valid:
            if NodeName == "":
                print "Node Name cannot be empty. Try again. "      # Simple validation to trap errors
            try:           
                for EachNode in self.GetNodes():
                    print EachNode
                    self.NodeList[EachNode].DeleteConnection(NodeName)  # Call Delete Connection method in Node class
                del self.NodeList[NodeName]
                print "Node deleted"
                Valid = True
            except KeyError:
                print "That node doesn't exist. Try again. "
                NodeName = raw_input("Enter the ID you wish to delete from the graph. ")    # Loop until valid Node Name is inputted
        
    def GetNodes(self):                  
        return self.NodeList.keys()      # method that returns the keys / ID all nodes in the loaded graph.

    def Dijkstra(self, Source, Dest):
        Distances = {} #define dictionary for neighbouring distances
        Previous = {} #define dictionary for the predecessors
        
        for EachNode in self.GetNodes(): #get the dictionary key from each node in the graph.
            Distances[EachNode] = -1 #set the distances to -1 (inacessible) so only connected paths are reached.
            Previous[EachNode] = "" #set the predecessors to an empty string.
            
        Distances[Source] = 0 #set the current distance of the source to 0 as source --> source = 0
        UnseenNodes = self.GetNodes() #create a list of keys from all the nodes in the graph
        
        while len(UnseenNodes) > 0: #only loop while the list is not empty 
            ShortestDistance = None
            Node = ""
            for TempNode in UnseenNodes:
                if Distances[TempNode] == -1: continue #if nodes are not connected, return to the while loop condition
                if ShortestDistance == None:
                    ShortestDistance = Distances[TempNode] #set new shortest distance. 
                    Node = TempNode
                elif Distances[TempNode] < ShortestDistance:
                    ShortestDistance = Distances[TempNode] #if a smaller shortest distance found, set shortest distance to this new value
                    Node = TempNode

            if ShortestDistance is None:
                break 
            UnseenNodes.remove(Node)
            #if all connected nodes / neighbours have been analysed, remove the node from unseen list

            for Neighbour, NeighbourValue in self.NodeList[Node].Connections.items(): #get neighbour node and weight from the nodelist
                NeighbourID = Neighbour.GetID() #get ID of node to refer to
                if Distances[NeighbourID] == -1 or Distances[NeighbourID] > Distances[Node] + NeighbourValue:
                    # do below if Distance hasn't been set or previous distance is bigger than new neighbouring distance
                    Distances[NeighbourID] = Distances[Node] + NeighbourValue #SET new distance 
                    Previous[NeighbourID] = Node #SET current predecessor

        
        Path = []
        Node = Dest
        while not (Node == Source):
            if Path.count(Node) == 0:       #work through predecessors dictionary and append to the new Path list backwards                              
                Path.insert(0,Node)         #using the previous predecessor to GET the value of the next
                if Previous[Node] != "":
                    Node = Previous[Node]   
            else:
                break
        Path.insert(0,Source)               # Insert the source node to the front of the path
        
        print "\n\nHere is the shortest path from the graph:\n "
        print Path
        print ""
        print "And the total distance between the points is: " + str(Distances[Dest])
        print ""
        return Path, Distances[Dest]     #returns the Shortest Path list and the total distance

    def Save(self,Nodes, Filename):         # Method for Saving the Graph to File
        self.Nodes = Nodes
        if Filename == "":
            Valid = False                   # Simple Validation to Trap Input Errors
            while not Valid:
                Filename = raw_input("Enter filename you want to save graph as: ")
                if Filename == "":
                    print "The filename cannot be empty. Try again. "
                elif len(Filename) > 30:
                    print "File name cannot exceed 30 characters. Try again. "
                else:
                    Valid = True
        
        PickleString = pickle.dumps(self)   # Creating a pickle string of each object
        File = open(Filename, 'w')          # Open a connection to the file
        File.write(PickleString)            # Write the pickle string to file
        File.close()                        # Close the connection
        print "Graph saved successfully. "



''' Start User Functions and Procedures for GUI Link '''

def UserDoesConnectionExist(MyGraph,Node1,Node2):                   # Function that tells you if two nodes are connected
    if MyGraph.NodeList[Node1].DoesConnectionExist(Node2) == True:
        return True
    else:
        return False

def SaveMap(Graph,Nodes):                       # Saves the Map to the default file
    Graph.Save(Nodes,'OfficialGraph.txt')       # Calls the Save procedure
        
def LoadMap():                                  #Loads back the default graph
    Map = LoadGraph('OfficialGraph.txt')        # Map is the actual graph
    Points = ReturnAllPoints(Map)               # Points is a list of all co-ordinates
    Nodes = Map.GetNodes()                      # Nodes is a list of all the node names
    return Map, Points, Nodes                   # Returns all of these to the GUI

def LoadGraph(Filename):                        # Load graph but for the console verison 
    Valid = False
    # Filename validation
    if Filename == "":        
        Filename = raw_input("Enter the filename of the graph: ")
    
    while not Valid:
        try:
            Graph = pickle.load(open(Filename, 'r'))    # Pickle Loads the Graph if Validation is correct
            print ""
            Valid = True    
        except IOError: # Traps Incorrect Filenames
            Filename = raw_input("Filename Incorrect, please try again. ")      # Ensures proper filename is inputted 
    return Graph

    
def GetWeightOfConnection(MyGraph, Node, ConnectedNode):
    Weight = MyGraph.NodeList[Node.GetID()].GetWeight(MyGraph.NodeList[ConnectedNode.GetID()])  
    return Weight       # Returns the weight of a connection between two nodes

def ReturnAllPoints(MyGraph):
    Points = []
    for EachNode in MyGraph.NodeList.values():  # Iterates through the list of nodes returning each node 
        Points.append(EachNode.GetXandY())      # Use the GetXandY function to return the co-ordinates and append them to the Points list
    return Points

def ReturnAllConnectionPoints(MyGraph):
    Points = []
    for EachNode in MyGraph.NodeList.values():                          # Iterates through each node and its connected node   
        ConnectedPoints = []
        for EachConnectedNode in EachNode.Connections:              
            if EachConnectedNode != EachNode:
                ConnectedPoints.append(EachConnectedNode.GetXandY())    # Returns the X and Y co-ordinates of each connected node to that node
        Points.append(ConnectedPoints)                                  # Appends each co-ordinate to the Points list
    return Points                                                       # Return Points List

def ReturnXY(MyGraph,Node):                                             # User can return the X and Y of a specific node in the graph
    return MyGraph.NodeList[Node].GetXandY()

def CompareXY(MyGraph,Node,x,y):                                        # Parameters are the name of node and the X and Y
    if (x,y) == MyGraph.NodeList[Node].GetXandY():                      # Function to determine whether a node is located at two specific points 
        print "print node detected at click point"
        return True
    else:
        return False

def ViewTextVersion(MyGraph):                                           # View text version iterates through each node and it's subsequent connections
    print ""                                                            # Outputting each connection in a text based format in the console
    print "Text Mode: (Node A / Node B) and Weight: \n "
    for EachNode in MyGraph.NodeList.values():                          # Loop through each node
        print "Node with ID =  " + EachNode.GetID()
        print " ---> Located at cordinates: " + str(EachNode.GetXandY())
        print ""
        for ConnectedNode in EachNode.ViewConnections():                # Loop through each connected node
            print " ---> Is connected to node with ID = " + ConnectedNode.GetID()
            print " ---> With a Weight of: " + str(GetWeightOfConnection(MyGraph,EachNode, ConnectedNode))
            print ""
    print ""

def UserAddNode(MyGraph, NodeName,x,y):                                 # User Add Node allows the user to add a node to the graph
    Valid = False
    if NodeName == 'console':
        while not Valid:                                                    # The name of the node is first validated
            NodeName = raw_input("Enter name of the node")
            if len(NodeName) == 0:
                print "Name of Node cannot be empty. Try again: "
            elif len(NodeName) > 30:
                print "Node name cannot exceed 30 characters. Try again: "
            else:
                Valid = True
    MyGraph.AddNode(NodeName,x,y)                                       # So the node is added first
    MyGraph.AddEdge(NodeName,NodeName,0)                                # and a connection is made to itself

def UserRemoveNode(MyGraph,NodeName):
    MyGraph.RemoveNode(NodeName)

def UserAddEdge(MyGraph,NodeName1,NodeName2,Weight):        # Allows user to add an edge between two nodes

    if __name__ == "__main__":                              # Validates if the edge has been inputted via the console
        Valid = False
        while Valid == False:
            try:
                NodeName1 = str(raw_input("Enter Node A : "))
                NodeName2 = str(raw_input("Enter Node B : "))
                Weight = int(raw_input("Enter Weight / distance between nodes: "))
                if Weight <0:
                    print "Weight of connection cannot be negative. "
                else:
                    Valid = True
            except:
                print "INVALID INPUT: "
                print "Only letters and numbers allowed, with length 1-25 characters. "
    
    MyGraph.AddEdge(NodeName1, NodeName2, Weight)           # Calls the graph method Add edge with verified parameters


def ViewNodeNames(MyGraph):     # Prints the list of nodes on the console
    print MyGraph.GetNodes()

def ShortestPath(MyGraph,Source,Dest):
    if __name__ == "__main__":          #Validates if it has been called via the console
        Valid = False
        while not Valid:
            Source = raw_input("Enter the source node: ")
            Dest = raw_input("Enter the destination node")
            try:
                Path, TotalDistance = MyGraph.Dijkstra(Source, Dest)
                Valid = True
            except KeyError:
                print ("Dijkstra's algorithm failed. Please enter the nodes again,\n"
                       "making sure they are correct. ")
    
    Path, TotalDistance = MyGraph.Dijkstra(str(Source), str(Dest))  # Calls Dijkstras Algorithm and gets back the Path and Total Distance
    return Path, TotalDistance                                      # Returns this to where it has been called from


def Menu():                                             # Console menu is printed if this function is called. 
    Valid = False
    #start menu#
    print ""
    print "Welcome to QES Maps Console "
    print "Select an option to continue: \n"
    print "1. View Graph Representation (Text) "
    print "2. Add Node "
    print "3. Add / Modify Edge "
    print "4. Calculate Shortest Path "
    print "5. View Node ID's "
    print "6. Remove Node "
    print "7. Save graph "
    print "8. Load Test Graph 1 "
    print "9. Load Other Graph "
    print "10. Rename Node "
    print "11. Return All Points"
    print "99. Quit "
    print ""
    while not Valid:
        try:
            MenuChoice = int(raw_input("Enter menu choice: " )) # The valid menu input is assigned here
            Valid = True
        except ValueError:
            print "Enter a valid option from the list. "
    return MenuChoice

def MenuControl():           # This procedure determines which other function / procedure is called depending on the menu choice
    MenuChoice = Menu()
    MyGraph = Graph()
    while MenuChoice != 99:
        if MenuChoice == 1:
            ViewTextVersion(MyGraph)
        elif MenuChoice == 2:
            UserAddNode(MyGraph, "console",'0','0')
        elif MenuChoice == 3:
            UserAddEdge(MyGraph)
        elif MenuChoice == 4:
            ShortestPath(MyGraph,"","")
        elif MenuChoice == 5:
            ViewNodeNames(MyGraph)
        elif MenuChoice == 6:
            MyGraph.RemoveNode("")
        elif MenuChoice == 7:
            MyGraph.Save()
        elif MenuChoice == 8:
            MyGraph = LoadGraph("testgraph.txt")
        elif MenuChoice == 9:
            MyGraph = LoadGraph("")
        elif MenuChoice == 10:
            MyGraph.RenameNode()
        elif MenuChoice == 11:
            ReturnAllPoints(MyGraph)
        else:
            print "Invalid Menu Choice, Try again: "
        MenuChoice = Menu()

if __name__ == "__main__":          # If console based program is being run, it starts here
    MenuControl()
    Map, Points, Nodes = LoadMap()
    ReturnAllConnectionPoints(Map)

