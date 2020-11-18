from tkinter import *
import math as m
from sympy import *
from PIL import ImageTk,Image 
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

#Graph Variables
GraphEquation = ''
GraphInterval = ''
x = Symbol('x')
mainGraph = Figure(figsize=(5,5), dpi=100)


#Arithmetic stuff
interval = [1,3]
nonallowed =[]
typeOfSum = 0
numberOfRect = 0
equation =""
#an enumerator
class optionsOfSums(enum.Enum):
    Left = 0
    Right = 1

#Calculates y-value of function
def RectCaluclator(giv):
    global equation                         #makes sure equation is actual equation
    res = parse_expr(equation).subs(x,giv)  #caluclates it
    return res                              #returns value

def findVerticalAsymptotes(): #finds the vertical asymptotes that are limits to the interval
    global equation
    
    #Values to make find divisors(vertical asymptotes occur when divisors = 0)
    onDisvior = False   
    parathesesCounter = 0
    interval = [0,0]
    problems = []
    nonallowed = []
    counter = 0
    intervalcounter = 0
    for i in equation+" ":  #loops through each char of equation
        
        if onDisvior:   #runs when inside a divisor
            if i == "(":
                parathesesCounter+=1
                if equation[intervalcounter-1] not in ["/","*","+","-"]:                            #Checks if something like 3a turns to 3*a
                    equation = ''.join((equation[:intervalcounter],"*",equation[intervalcounter:])) #adds a multiplication sign to make sure equation is readable
                    intervalcounter+=1  #makes sure offset is correct
                    counter+=1          #^^
            elif i == ")":  #goes down one nested parathesis
                parathesesCounter-=1
            elif parathesesCounter == 0:
                if i in ["*","/","x"] or i.isdigit():
                    pass    #makes sure to not end on multiplication, division, or x
                else:
                    onDisvior = False
                    interval[1] = counter
                    problems.append(equation[interval[0]+1:interval[1]])
                    inverval = [0,0]
        elif i == "/":              #If a divisor is detected, cant nest due to elif
            onDisvior = True        #if a / is found, then it is a divisor(tells program)
            interval[0] = counter   #sets  the start of divisor
        counter += 1                #adds to the offset to make sure code is referencing the correct character
        intervalcounter +=1         #increases the interval counter by 1
    x = Symbol('x')                 # makes sure that x is the symbol
    for p in problems:              #loops through every divisor(their equations)
        for s in solve(p):          #Finds all solutions in the given problem
            nonallowed.append(s)    # appends all solutions to the not allowed array(to prevent infinite areas)
    return nonallowed               #returns all non allowed domains
def callback(P):        #limits inputs of certain text inputs to numbers(neg and pos)
    if str.isdigit(P[1:]) or P[1:] =="" :
        if P == "" or str.isdigit(P[0]) or P[0] in ["-"]:
            return True
        return False
    else:
        return False    

def Riemmanstuff(): #Main calculations
    global equation #makes sure equation is the equation
    try:            #attempts to calculate, will fail(try here to prevent code from dying)
        equation        = str(equationFunctionInput.get())  #obtains equation from equation input box
        numberOfRect    = int(amountOfRectangles.get())     #obtains the amount of rectangles to draw
        interval[0]     = int(leftIntervalInput.get())      #obtains first part of interval
        interval[1]     = int(rightIntervalInput.get())     #obtains second part of interval
        GraphInterval   = [interval[0],interval[1]]         #creates the graph interval, also not needed
        GraphEquation   = equation                          #not really needed, but its cool

        #Graph graphical stuff
        mainGraph.clf()                                 #clears current graph from prevent instance
        GraphSubPlot = mainGraph.add_subplot(111)       #adds subplot to main graph figure
        GraphSubPlot.grid()                             #adds grid to graph

        #sets equation of the graph
        x = np.array(np.arange(GraphInterval[0],GraphInterval[1],0.01))
        y = eval(GraphEquation)
        GraphSubPlot.plot(x,y)  #plots it

        
        #updates graphical stuff
        toolbar.update()
        canvas.draw()
        currentAxis = mainGraph.gca()

        intervalLimits = findVerticalAsymptotes()   #limits domain to prevent nonpossible calculations
        if numberOfRect > m.pow(10,6):              #prevents computer death
            resultShower['text'] ='You have inputed a super large number, which will crash the program!'
            return                                  #gets out of function
        estimatedArea = 0           #intilize estimateed area from rectangles
        for i in intervalLimits:    #makes sure domain doesnt cross over limits
            if i >= interval[0] and i <= interval[1]:
                resultShower['text'] ='The interval is at a vertical asymptote! The program has detected x = ' + str(intervalLimits)
                return
        totalBase = abs(interval[1]-interval[0])    #calculates total base of the graph
        for t in range(0, numberOfRect) :           #calculates every rectangle
            leftcurrent = (t)* totalBase/numberOfRect+interval[0]
            yValue = RectCaluclator(leftcurrent)    #calculates y cordinate                 !!!!!!!!!!!!!!ADD ON HERE ABOUT PIVOT TYPE!!!!!!!!
            currentAxis.add_patch(Rectangle((leftcurrent, 0), totalBase/numberOfRect,yValue, facecolor="grey")) #adds rectangle to graph, HARDWARE INTENSIVE, can cause lag
            area = totalBase/numberOfRect * yValue  #calculates area of rectangle
            estimatedArea += area                   #adds to estimated area
        canvas.draw()                               #draws all rectangles, is also  HARDWARE INTENSIVE 
        resultShower['text'] = 'Estimated: '+ str(estimatedArea)    #shows total estimated area
    except: #when something fails, prevents total death(ie no input)
        resultShower['text'] ='An error occured, check if values are correctly inputed'


#GUI STUFF
#Button stuff

#root
root = Tk()
#canvas
canvas = FigureCanvasTkAgg(mainGraph, master=root)
toolbar = NavigationToolbar2Tk(canvas, root)

vcmd = (root.register(callback)) #gets inputs for certain text inputs(to limit)
root.geometry("1200x800")
root.title("Riemann sum calculator")

#Widgets
SubTitle = Label(root, text="Riemann sum calculator", font=("Courier", 10))
typeTitle = Label(root, text="Type/Starting point")
numOfRectTitle = Label(root, text="How many rectangles to calculate?")
resultShower = Label(root, text="Feed me information!", fg='red',bg='white', font=("Courier", 15)) #shows result

calculateButton = Button(root, text="Calculate!", padx=150, command=Riemmanstuff)

equationFunctionInput = Entry(root,fg="red")
equationFunctionInput.pack()
#intervalInputRange = Entry


intervalFrame = Frame(root)
leftIntervalInputLabel  = Label(intervalFrame, text ="From").pack(side=LEFT)
leftIntervalInput       = Entry(intervalFrame, width=5, validate = 'all', validatecommand=(vcmd, '%P'))
leftIntervalInput.pack(side=LEFT)
rightIntervalInputLabel = Label(intervalFrame, text ="To").pack(side=LEFT)
rightIntervalInput      = Entry(intervalFrame, width=5, validate = 'all', validatecommand=(vcmd, '%P'))
rightIntervalInput.pack(side=LEFT)


amountOfRectangles = Entry(root, validate = 'all', validatecommand=(vcmd, '%P')) #validatecommand and validate limit input to digits
calculateEquation = Entry(root, validate = 'all', validatecommand=(vcmd, '%P'))

#Radio buttons
typeToCalculate = Frame(root)
typeRadio0 = Radiobutton(typeToCalculate, text='Left', variable =typeOfSum, value=0, indicatoron=1).pack(side=LEFT)
typeRadio1 = Radiobutton(typeToCalculate, text='Right', variable =typeOfSum, value=1, indicatoron=1).pack(side=RIGHT)
#Interval stuff
invervalFrame = Frame(root)



#Display stuff
SubTitle.pack(anchor='n')
typeTitle.pack(anchor='n')


typeToCalculate.pack(anchor='n')

intervalFrame.pack(anchor='n')

numOfRectTitle.pack(anchor="n")
amountOfRectangles.pack(anchor='n')


calculateButton.pack(anchor='n')
resultShower.pack(anchor='s')
canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

root.mainloop() # runs main loop