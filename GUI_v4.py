# QES MAPS BY THOMAS O'KEEFFE #
# Version 4 of Complete User Interface # # commented and beta tested #


''' Import Modules '''

from Tkinter import *
import Image, ImageTk
import QESMAPS_v3
import math
import datetime
import time

''' Administrative Interface Class'''

class Admin(Frame):
    def __init__(self, Parent):                 # Define Adminisrative Private Attiributes:
        Frame.__init__(self, Parent)            # Create Parent Window #
        self.Parent = Parent                    
        self.MyGraph = QESMAPS_v3.Graph()       # Get QES Map data structure 
        self.UserLoaded = False                 # Define other private attributes for program control
        self.Points = []
        self.Nodes = []
        self.SelectedNodes = ['','']
        self.CreateCanvas()                     # Call create canvas sub-routine
        self.initUI()                           # Call interface sub-routine
        
    def Exit(self):                                       
        self.Parent.destroy()                   # Close all windows and return to console only
        self.quit()

    def CreateCanvas(self):                     # Define a Tkinter canvas to draw on
        self.CanvasFrame = Frame(self.Parent)
        self.MapCanvas = Canvas(self.CanvasFrame, height=630,width=900, bg='sea green',borderwidth=3, relief=RIDGE)     
        self.CanvasFrame.pack(side=LEFT, fill=BOTH)
        self.MapCanvas.grid(row=0,column=0,sticky=N)
                                                       
        File = "map.jpg"                        # Adding the Background Image
        self.MapCanvas.img = ImageTk.PhotoImage(Image.open(File))
        self.MapCanvas.create_image(0,0,image=self.MapCanvas.img,anchor="nw")

        #Bindings
        #Adding Nodes (Doubleclick)
        #Detecting Nodes (Right, Left Clicks)
        self.MapCanvas.bind('<Button-1>',self.DetectNode)
        self.MapCanvas.bind('<Button-3>',self.DetectNode2)

    def ImportDrawings(self):                                                               #import all node drawings in from graph nodes
        for EachPoint in self.Points:
            X,Y = EachPoint[0],EachPoint[1]
            self.MapCanvas.create_rectangle(X,Y,X+5,Y+5, fill="red", tags="Nodes")

        Points = QESMAPS_v3.ReturnAllConnectionPoints(self.MyGraph)                         #import all line drawings from graph connections
        Counter = 0
        for EachNode in self.MyGraph.NodeList:
            Point1 = QESMAPS_v3.ReturnXY(self.MyGraph, EachNode)
            for EachConnectedPoint in range(len(Points[Counter])):
                Point2 = Points[Counter][EachConnectedPoint]
                self.MapCanvas.create_line(Point1,Point2,width=1.2,fill='red',tags="Lines")
            Counter += 1

    def Clear(self):                                            #Clear any canvas drawings by deleting drawings that are tagged
        self.MapCanvas.delete("Nodes","Lines", "lines")

    def PopUp(self):                                            # Initiate Pop Up Window
        self.Entry = AddNodeWindow(self.Parent)
        self.Parent.wait_window(self.Entry.Top)

    def EntryValue(self):                                       # Return the entry value from the input in the pop up window
        return self.Entry.value

    def AddNode(self,event):                                    # Add a node to the graph using the administrative funtions
        if self.UserLoaded == False:
            self.PopUp()
            NodeName = self.EntryValue()                                                                                # Get the name of the node using the pop up window
            
            self.MapCanvas.create_rectangle(event.x,event.y,event.x+5,event.y+5, fill="red", tags="Nodes")              # Add the node as a rectangle vector drawing on the canvas
            
            QESMAPS_v3.UserAddNode(self.MyGraph, NodeName,event.x,event.y)                                              # Use QESMAPS module to add the node to the graph data structure
            self.Nodes.append(NodeName)                                                                                 # Append the added node to the list of nodes on the canvas

    def DetectNode(self,event):                             # Detect node, used to select a node from the canvas so it can be referenced using the actual graph data structure
        NoNodesFound = True
        for X in range((event.x-15),(event.x+15)):          #Search 15 x 15 square radius around the click point
            for Y in range((event.y-15),(event.y+15)):
                for EachNode in self.Nodes: 
                    if QESMAPS_v3.CompareXY(self.MyGraph,EachNode,X,Y) == True:     # First node to be detected in the radius is assigned to variable self.Node
                        self.Node = EachNode
                        NoNodesFound = False
                        break

        if NoNodesFound == True:
            print "No nodes found at click point. "                              #display error message on canvas if no node is found in that radius
        else:
            print "Node Detected: " + str(self.Node)

            self.SelectedNodes[0] = self.Node

            if self.UserLoaded == True:                                         #draw a vector circle around the selected node on canvas
                self.Start.delete(0,END)
                self.Start.insert(END,self.Node)
                X1Y1 = QESMAPS_v3.ReturnXY(self.MyGraph,self.SelectedNodes[0])
                X1,Y1 = X1Y1[0],X1Y1[1]
                self.MapCanvas.delete("oval1")
                self.MapCanvas.create_oval(X1-8,Y1-8,X1+8,Y1+8, tags="oval1", outline="sea green")
            else:
                self.Node1.configure(text=str(self.Node))                   # configure the text on the interface to show the selected node

    def DetectNode2(self,event):                                                        #detect node 2 is a repeat of detect node 1
        NoNodesFound = True
        for X in range((event.x-15),(event.x+15)):
            for Y in range((event.y-15),(event.y+15)):
                for EachNode in self.Nodes:
                    if QESMAPS_v3.CompareXY(self.MyGraph,EachNode,X,Y) == True:
                        self.Node = EachNode
                        NoNodesFound = False

        if NoNodesFound == True:
            print "No nodes found at click point. "                         # show error message if no node found
        else:
            print "Node Detected: " + str(self.Node)
            self.SelectedNodes[1] = self.Node                                   # assign the detected node to the second item in the slected node list

            if self.UserLoaded == True:
                self.End.delete(0,END)
                self.End.insert(END,self.Node)
                X1Y1 = QESMAPS_v3.ReturnXY(self.MyGraph,self.SelectedNodes[1])      # creating a differnt coloured circle vector around the selected node 
                X1,Y1 = X1Y1[0],X1Y1[1]
                self.MapCanvas.delete("oval2")
                self.MapCanvas.create_oval(X1-8,Y1-8,X1+8,Y1+8, tags="oval2")
            else:
                self.Node2.configure(text=str(self.Node))                       # configure the node 2 text 

    def GetCurrentPoints(self):                                                 
        #Get Points of First Node                                               # Returns the co-ordinates of a selected node
        X1Y1 = QESMAPS_v3.ReturnXY(self.MyGraph,self.SelectedNodes[0])          # Uses QESMAPS module to do this
        X1,Y1 = X1Y1[0],X1Y1[1]
        #GetPoints of Other Node
        X2Y2 = QESMAPS_v3.ReturnXY(self.MyGraph,self.SelectedNodes[1])
        X2,Y2 = X1Y1[0],X1Y1[1]
        X1 = X1Y1[0]
        Y1 = X1Y1[1]
        X2 = X2Y2[0]
        Y2 = X2Y2[1]
        return X1,Y1,X2,Y2

    def GetDistance(self):                                      #Using Pythagoras's Theorem to get distance between points.
        X1,Y1,X2,Y2 = self.GetCurrentPoints()                   #This is applicable as the map has been drawn to scale.
        print "Getting the distance between nodes: "
        Distance = math.sqrt(((X2-X1)**2)+((Y2-Y1)**2))     
        return int(Distance)                                    #Return the distance as an interger as that is the data type that the canvas works with. 

    def AssignConnection(self):
        print "Making a connection between nodes: "
        Distance = self.GetDistance()                                                                     #Get the distance between the two points on the canvas
        QESMAPS_v3.UserAddEdge(self.MyGraph,self.SelectedNodes[0],self.SelectedNodes[1],Distance)         #Add an edge to the graph
        self.MapCanvas.create_line(self.GetCurrentPoints(),width=2, fill='red', tags="lines")             #Create a visual connection on the canvas

    def Save(self):                                         # Save the graph structure
        QESMAPS_v3.SaveMap(self.MyGraph,self.Nodes)

    def Load(self):                                                         
        self.MyGraph, self.Points, self.Nodes = QESMAPS_v3.LoadMap()    # load the graph data and assign it to the admin class private attributes

    def ViewText(self):
        QESMAPS_v3.ViewTextVersion(self.MyGraph)        # view the console verison of the graph data for debugging purposes

    def DrawPath(self,Path):                                                                # draw the shortest path on the canvas
        for EachPoint in range(len(Path)-1):                                                # iterate through each point in the path returned by shortest path algorithm
            Point1 = QESMAPS_v3.ReturnXY(self.MyGraph,Path[EachPoint])                      # return the co-ordinates of each path node
            Point2 = QESMAPS_v3.ReturnXY(self.MyGraph,Path[EachPoint+1])                
            PathLine = self.MapCanvas.create_line(Point1,Point2,width=2.5,fill='green')     # connect the each of the points one by one witha green line
            self.MapCanvas.itemconfig(PathLine, tags=("Path","Lines"))                      # tag the lines, so they can be deleted later on

    def CalculateTime(self,Distance):
        Seconds = int(float(Distance) / 1.4 / 3.4)              #Calculating the time it takes from A-B.
        Time = str(datetime.timedelta(seconds=Seconds))         #Using averge walking speed of 1.4m/s, (Wikipedia)
        self.TotalTime.configure(text="Jouney Time: " + Time)   #Time = Distance / Speed

    def ShortestPath(self):                                                                     # start the shortest path 
        if (self.SelectedNodes[0]  == 'default0') or (self.SelectedNodes[1] == "default1"):     # ensure two nodes have been selected first
            print "Select two nodes first!"
            self.TotalDistance.configure(text="Select two points first! ")
        else:
            print "Shortest Path: "
            Path, Distance = QESMAPS_v3.ShortestPath(self.MyGraph,self.SelectedNodes[0],self.SelectedNodes[1])  #path and total distance got from graph module
            if Distance == -1:
                self.ShortestPath.configure(text="No Available Route!")         # print error message if no route is available, this shouldn't ever happen
            else:
                TextToDisplay = " \n "
                for EachPlace in Path:
                    if not self.UserLoaded:                                                 #display the shortest path either on the canvas or path list depending 
                        self.PathList.insert(END,str(EachPlace))
                self.TotalDistance.configure(text="Total Distance: " + str(Distance) +"m")
                self.CalculateTime(Distance)                                                 # calculate time taken 
                self.DrawPath(Path)

    def Reset(self):                                                        # Reset the fields and canvas to default
        #resets the path text box to default
        self.MapCanvas.delete("Path","oval1","oval2")                       # Clear the canvas
        if self.UserLoaded == True:
            try:
                self.Start.delete(0,END)
                self.Start.insert(END,"Select a node to begin.")
                self.End.delete(0,END)
                self.End.insert(END,"Select a node to begin.")
                self.MapCanvas.delete(self.CanvasWindow)
            except: AttributeError
        else:
            self.PathList.delete(0,END)
            self.TotalDistance.configure(text="..............")             # Reset the canvas text
            self.TotalTime.configure(text="..............")
            
        
    def Delete(self):                                                       # Delete a node from the graph structure
        X1Y1 = QESMAPS_v3.ReturnXY(self.MyGraph,self.SelectedNodes[0])      # return the co-ordinates from the selected point given by a  mouse click
        X1 = X1Y1[0]    
        Y1 = X1Y1[1]
                                                                            # Delete Node from Structures
        QESMAPS_v3.UserRemoveNode(self.MyGraph,self.SelectedNodes[0])       # remove the selcted node from the graph 
        self.Nodes.remove(self.SelectedNodes[0])                            # remove the nodes 
        self.MapCanvas.addtag_closest("delete",X1,Y1)                       # Delete Rectangle from Canvas
        self.MapCanvas.delete("delete")
        self.Node1.configure(text="..............")

    def AddAccount(self):                                                   # Add an account using the console
        Valid = False
        Users = open("Usernames.txt", 'a')                                  # Open a connection to the file and use the variable users as a reference
        while not Valid:
            NewUsername = raw_input("Enter new username: ")                 # Get the input from the user
            NewPassword = raw_input("Enter new password: ")
            if "," in NewUsername:
                print "Please enter valid characters only. [ 0-9 Aa-Zz ] "
            else:
                print "Valid.. " 
                Valid = True
                Users.write(NewUsername + "," + NewPassword + "\n")         # Combine the username and password and write into a CSV file 
        Users.close()                                                       # Close the connection to the file to prevent file errors

    def ReturnToUserMode(self):                 # Return to the user option window           
        self.Clear()                            # Clear the administrative options
        self.OptionsFrame.destroy()
        self.UI()                               # Load the user options
        self.UserLoaded = True                  # Set the private attribute user loaded to true so the rest of the program knows the admin is not active
        self.MapCanvas.unbind("<Button-1>")

    def initUI(self):                               # Administrative GUI 
        #admin window config
        self.Parent.title("Admin Interface")        # Title of the window
        self.Parent.geometry("1050x660")            # Define the window size accordingly
        self.MapCanvas.bind('<Double-Button-1>',self.AddNode)

        ''' Start Widgets '''
         
        #Admin Menubar
        menubar = Menu(self.Parent)
        self.Parent.config(menu=menubar)
        #File
        fileMenu = Menu(menubar)
        menubar.add_cascade(label="Console Settings", menu=fileMenu)
        fileMenu.add_command(label="Return to Console", command=self.Exit)
        fileMenu.add_command(label="Add Account", command=self.AddAccount)
        #Help
        helpMenu = Menu(menubar)
        menubar.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="Show help window", command=self.Help)

        #Admin Frame
        self.OptionsFrame = Frame(self.Parent,borderwidth=3,relief=SUNKEN)
        self.OptionsFrame.configure(bg="sea green")
        self.OptionsFrame.pack(padx=8,pady=10)
        
        #Display Selected Node
        #Label
        self.TextLabel = Label(self.OptionsFrame, text="Node Selected: ",width=25)
        self.TextLabel.pack()
        #Node 1 Text Display
        self.Node1 = Label(self.OptionsFrame, text="..............",width=25)
        self.Node1.pack()
        #Node 2 Text Display
        self.Node2 = Label(self.OptionsFrame, text="..............",width=25)
        self.Node2.pack()
        
        #Options
        self.AssignConnection = Button(self.OptionsFrame,text="Assign Connection",width=25, command=self.AssignConnection)     
        self.AssignConnection.pack()
        #Save Button
        self.SaveButton = Button(self.OptionsFrame,text="Save Map",command=self.Save,width=25)
        self.SaveButton.pack()
        #Load Button
        self.LoadButton = Button(self.OptionsFrame,text="Load Map",command=self.Load,width=25)
        self.LoadButton.pack()
        #Show Graph Button
        self.ShowGraph = Button(self.OptionsFrame, text="Show Graph", command=self.ImportDrawings,width=25)
        self.ShowGraph.pack()
        #Clear Graph Button
        self.ClearGraph = Button(self.OptionsFrame, text="Clear Graph",command=self.Clear,width=25)
        self.ClearGraph.pack()
        #View Text Version
        self.ViewTextButton = Button(self.OptionsFrame, text="View Console Graph", command=self.ViewText,width=25)
        self.ViewTextButton.pack()
        
        #Test Shortest Path
        #Button
        self.TestShortestPath = Button(self.OptionsFrame,text="Test Shortest Path",command=self.ShortestPath,width=25)
        self.TestShortestPath.pack()
        #Path textbox
        self.PathBox = Frame(self.OptionsFrame)
        self.PathBox.pack()
        self.Scroll = Scrollbar(self.PathBox)       # Create scrollbar 
        self.Scroll.pack(side=RIGHT,fill=Y)         # Place scrollbare to the right of the listbox
        self.PathList = Listbox(self.PathBox)
        self.PathList.pack(side=LEFT)
        self.PathList.config(yscrollcommand=self.Scroll.set)
        self.Scroll.config(command=self.PathList.yview)  
        #Distance Field
        self.TotalDistance = Label(self.OptionsFrame, text="..............",width = 25)
        self.TotalDistance.pack()
        #Total Time Field
        self.TotalTime = Label(self.OptionsFrame, text="..............", width = 25)
        self.TotalTime.pack()
        
        #Reset
        self.ResetButton = Button(self.OptionsFrame,text="Reset", width=25,command=self.Reset)
        self.ResetButton.pack()
        
        #Delete Node
        self.DeleteButton = Button(self.OptionsFrame,text="Delete Point", width=25,command=self.Delete)
        self.DeleteButton.pack()
        
        #Exit Button
        self.ExitButton = Button(self.OptionsFrame, text="Return to User Mode",width=25,command=self.ReturnToUserMode)
        self.ExitButton.pack()

        ''' End Widgets '''

''' User class '''

class User(Frame,Admin):                                # Inherit  public attributes and public methods from Admin Class
    def __init__(self, Parent):
        Frame.__init__(self, Parent)                    #__init__ configuration 
        self.Parent = Parent
        self.UserLoaded = True                          # User class private attributes
        self.Differ = 0
        self.SelectedNodes = ['default0','default1']
        self.CreateCanvas()                             # Create Canvas
        self.Load()                                     # Load Graph onto Canvas
        self.UI()                                       # Load User Options

    def Help(self):                                     # Method for opening help window
        print "Loading help file... "
        self.Window = HelpWindow(self.Parent)           # Open help window as a pop up window
        self.Parent.wait_window(self.Window.Top)

    def LoginValue(self):                               # Return the Boolean value determined by the log in pop up
        return self.Window.Verified

    def Login(self):                                    # method for opening the log in window
        print "loggin in... "
        self.Window = LoginWindow(self.Parent)
        self.Parent.wait_window(self.Window.Top)
        if self.LoginValue() == True:                   # if correct log in details destroy user interface
            self.User.destroy()
            self.initUI()                               # and load the administrative interface instead
            self.UserLoaded = False

    def LoadNodeList(self):                             # Method that's used to retrieve each node name from the canvas
        for EachNode in self.Nodes:
            self.NodeListBox.insert(END, EachNode)      # And inserts it into the list of nodes on the user interface

    def ListBoxSelect(self, event):                             # Method to select a node from the node list in the user interface
        widget = event.widget
        Selection = widget.curselection()
        self.SelectedValue = widget.get(Selection[0])           # Get the node selected at click point 
        self.SelectedNodes[self.Differ] = self.SelectedValue

        if self.Differ == 0:                                    # The first node that is clicked is assinged to the START (Source) node. 
            self.Start.delete(0,END)
            self.Start.insert(END,self.SelectedValue)
            self.Differ = 1
        else:                                                   # The second node that is clicked is assigned to the END (Dest) node. 
            self.End.delete(0,END)
            self.End.insert(END,self.SelectedValue)
            self.Differ = 0

        
    def UserPath(self):                                                                     # This is the window displayed on the canvas when a path is created
        self.Reset()                                                                        # Reset the current information / path
        self.Info = Frame(self.MapCanvas)
        self.InfoHeader = Label(self.Info,text="Your journey: ",bg="sea green", fg="white")
        self.InfoHeader.pack(fill=X)
        self.TotalDistance = Label(self.Info ,bg="medium sea green")
        self.TotalDistance.pack(fill=X)
        self.TotalTime = Label(self.Info, bg="medium sea green")
        self.TotalTime.pack(fill=X)
        self.CanvasWindow = self.MapCanvas.create_window(775,310,window=self.Info)          # Create the window at a fixed point on the map
        self.ShortestPath()                                                                 # Draw the shortest path on the canvas
        
    ''' Start User Interface ''' 
    
    def UI(self):
        self.Parent.title("QES MAPS")       # configure the window title
        self.Parent.geometry("1120x660")    # configure the fixed window size
        self.MapCanvas.unbind("<Double-Button-1>")

        ''' User widgets ''' 
        
        #User Menubar
        menubar = Menu(self.Parent)
        self.Parent.config(menu=menubar)
        #File
        AdminMenu = Menu(menubar)
        menubar.add_cascade(label="Admin", menu=AdminMenu)
        AdminMenu.add_command(label="Log in", command=self.Login)
        #Help
        HelpMenu = Menu(menubar)
        menubar.add_cascade(label="Help", menu=HelpMenu)
        HelpMenu.add_command(label="Show Help", command=self.Help)

        #User Panel
        self.User = Frame(self.Parent,bg="sea green",borderwidth=3, relief=RIDGE)
        self.User.grid(row=0,column=1)
        self.User.pack()

        #'Start'
        self.StartLabel = Label(self.User, text="START: ",anchor='nw',bg="sea green", width=30,fg='white')
        self.StartLabel.config(font=("Comic Sans MS", 18))
        self.StartLabel.pack(padx=5)

        self.Start = Entry(self.User,bg="dark green", width=36,fg='white')
        self.Start.insert(END, "Click a point on the map to begin. ")
        self.Start.pack(padx=5,pady=(0,10))

        #'End'
        self.EndLabel = Label(self.User, text="END: ", anchor='nw',bg="sea green", width=30,fg='white')
        self.EndLabel.config(font=("Comic Sans MS", 18))
        self.EndLabel.pack(padx=5)

        self.End = Entry(self.User,bg="dark green", width=36,fg='white')
        self.End.insert(END, "Click a point on the map to begin. ")
        self.End.pack(padx=5,pady=(0,10))

        #Reset and GO Buttons
        self.Buttons = Frame(self.User, bg="sea green")
        self.Buttons.pack()

        self.ResetButton = Button(self.Buttons, command=self.Reset, width=8, height=1, text="Reset", bg="medium sea green")
        self.ResetButton.config(font=("Comic Sans MS", 12))
        self.ResetButton.pack(side=LEFT,padx=(0,5))

        self.GoButton = Button(self.Buttons, command=self.UserPath, width=8, height=1, text="GO!", bg="medium sea green", fg='white')
        self.GoButton.config(font=("Comic Sans MS", 12))
        self.GoButton.pack(side=RIGHT, pady=10)

        #Listbox of all Nodes/Rooms called 'Nodebox'
        self.NodeBox = Frame(self.User)
        self.NodeBox.pack(padx=5,pady=(5,27))
        self.Scroll = Scrollbar(self.NodeBox)                               # Create scrollbar
        self.Scroll.pack(side=RIGHT,fill=Y)                                 # Place this to the right of the listbox to scroll through each node
        self.NodeListBox = Listbox(self.NodeBox,width=30,height=25)
        self.LoadNodeList()
        self.NodeListBox.pack(side=LEFT)
        self.NodeListBox.config(yscrollcommand=self.Scroll.set)
        self.Scroll.config(command=self.NodeListBox.yview)
        self.NodeListBox.bind('<Double-Button-1>', self.ListBoxSelect)      # Bind the double click to the method list box select

    ''' End of User Interface and User Class ''' 

''' Help Window Class '''

class HelpWindow(Frame):                
    def __init__(self,Parent):
        Top = self.Top = Toplevel(Parent)           # Help Window Configuration: 
        self.Top.title("Help")                      # Title
        self.Top.geometry("220x300")                # Window Size
        self.HelpContent()                          # Window Content

    def HelpContent(self):
        self.Interface = Frame(self.Top, bg = "sea green")
        self.Interface.pack()
        
        # Header #
        self.Header = Frame(self.Interface, bg = "sea green", width = 160)
        self.TitleText = Label(self.Header,text="Welcome to QES MAPS" , bg="dark sea green", width=160)
        self.TitleText.pack(fill=X)
        self.Header.pack(pady=10, fill=X)
        
        # Content #
        self.Content = Frame(self.Interface, width = 160)
        self.Content.pack()
        TextToDisplay = ("To get started, use the left and right mouse buttons to select your journey route. \n\n "
                         "Once you have done that, hit the 'GO' button and the quickest route will be displayed"
                         "on screen. \n\n If you cant find your room on the map, scroll down the list of rooms until"
                         "you find the one your looking for. Then double click each room to select it. \n\n"
                         "Your journey details will then be displayed on the map. Have fun!")
        self.HelpText = Label(self.Content, wraplength = 200, text=TextToDisplay, bg="dark sea green")
        self.HelpText.pack()

        # Footer #
        self.Footer = Frame(self.Interface,bg="sea green")
        self.Footer.pack(pady=20)
        
'''End Help Window Class ''' 


''' Log In Window Class ''' 

class LoginWindow(Frame):
    def __init__(self,Parent):                  # Log In Window Configuration
        Top = self.Top = Toplevel(Parent)       # Make Window over the top of other windows
        self.Top.title("Log In")                # Title
        self.Top.geometry("210x160")            # Fixed Window Size
        self.Verified = False                   # Variable that denotes if successfull login has occured
        self.LoginInterface()                   # Load Interface 
        self.Top.bind('<Return>',self.Login)    # Bind the enter button to the log in function

    def LoginScript(self):                      # Log In Script
        Username = self.UsernameInput.get()     # Get Username from username field
        Password = self.PasswordInput.get()     # Get Password from password field
        ReadingUsername = ""
        ReadingPassword = ""
        UsernameRead = False
        Users = open("Usernames.txt", 'r')      #Open a connection to the file with reference variable Users
        Usernames = Users.readlines()           #Read each account in the file and check this with inputted username and password
        for EachUser in range(len(Usernames)):
            Combination = Usernames[EachUser]
            for char in range(len(Combination)):
                if Combination[char] == ",":
                    UsernameRead = True
                elif UsernameRead == False:
                    ReadingUsername += Combination[char]
                elif Combination[char] in "\n":
                    ""
                else:
                    ReadingPassword += Combination[char]
            UsernameRead = False
            ActualUsername,ActualPassword = ReadingUsername,ReadingPassword
            ReadingUsername, ReadingPassword = "",""
             
            if Username == ActualUsername and Password == ActualPassword: # if credentials are stored in file they are a verfied administrator
                self.Verified = True
            else:
                ActualUsername, ActualPassword = "",""
        Users.close()                                                   # Close the connection to the file

    def Login(self,event):                                                      # Method called when return button hit
        self.LoginScript()
        if not self.Verified:
            self.TitleText.configure(text="Incorrect Details: Try again. ")     # Error message displayed if username or password is incorrect
        else:
            self.Top.destroy()                                                  # Destroy the log in window if credentials are correct

    def LoginButton(self):                                                      # Method called when the log in button is pressed
        self.LoginScript()
        if not self.Verified:
            self.TitleText.configure(text="Incorrect Details: Try again. ")     # Same message displayed if credentials are incorrect
        else:
            self.Top.destroy()                                                  # Window destroyed if log in is correct

    def LoginInterface(self):
        ''' Login Interface Widgets ''' 
        self.Interface = Frame(self.Top, bg = "sea green")
        self.Interface.pack()
        
        # Header #
        self.Header = Frame(self.Interface)
        self.TitleText = Label(self.Header,text="LOG IN TO QES MAPS:" , bg="dark sea green")
        self.TitleText.pack(fill=X)
        self.Header.pack(pady=10)
        
        # Username Input #
        self.Username = Frame(self.Header)
        self.Username.pack(pady=10)
        self.UsernameLabel = Label(self.Username, text="Username: ", width=10)
        self.UsernameLabel.pack(side=LEFT)
        self.UsernameInput = Entry(self.Username)
        self.UsernameInput.pack(fill=X,padx=5,pady=2)
        self.UsernameInput.focus_set()
        
        # Password Input #
        self.Password = Frame(self.Header)
        self.Password.pack(pady=10)
        self.PasswordLabel = Label(self.Password, text="Password: ", width=10)
        self.PasswordLabel.pack(side=LEFT)
        self.PasswordInput = Entry(self.Password, show="*")
        self.PasswordInput.pack(fill=X,padx=5,pady=2)
        
        # Submit Button
        self.Buttons = Frame(self.Header)
        self.Buttons.pack(fill = BOTH, expand = True)
        self.LoginButton = Button(self.Buttons, text = "Log in", command=self.LoginButton)
        self.LoginButton.pack(side=RIGHT, padx=3, pady=3)
        '''End Login Interface Widgets '''
    


class AddNodeWindow(Frame):                                     #### Add node pop up window ####
    def __init__(self,Parent):
        Top = self.Top = Toplevel(Parent)                       # Configure private attributes, window is displayed over any others (TopLevel) 
        self.Text = Label(Top,text="Enter Node Name:")          # Get Node name from user input 
        self.Text.pack()
        self.TextEntry = Entry(Top)
        self.TextEntry.focus_set()                              # Focus Method automatically makes keyboard input go into the text entry
        self.TextEntry.pack()
        self.TextEntry.bind('<Return>',self.Destroy)            #Bind enter key to cleanup command

    def Destroy(self,Other):
        self.value = self.TextEntry.get()                       # Return text field string value
        self.Top.destroy()                                      # Destroy the window

def main():                                     # main procedure that controls the startup of the program
    root = Tk()                                 # create a root window
    app = User(root)                            # create a user class called app
    root.resizable(width=False, height=False)   # Lock the size of the main window
    root.iconbitmap('icon.ico')                 # Change the default icon in the title
    root.mainloop()                             # Loop the interface window

if __name__ == '__main__':
    main()                                      # Start the program if the program is not being uses as a module
