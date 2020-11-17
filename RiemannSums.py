from tkinter import *
import math as m
from sympy import *
from PIL import ImageTk,Image 
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
class optionsOfSums(enum.Enum):
    Left = 0
    Right = 1


def RectCaluclator(giv):
    global equation
    res = parse_expr(equation).subs(x,giv)
    return res

def findVerticalAsymptotes(): #finds the vertical asymptotes that are limits to the interval
    global equation
    
    onDisvior = False
    parathesesCounter = 0
    interval = [0,0]
    problems = []
    nonallowed = []
    counter = 0
    intervalcounter = 0
    for i in equation+" ":
        
        if onDisvior:
            if i == "(":
                parathesesCounter+=1
                if equation[intervalcounter-1] not in ["/","*","+","-"]:
                    equation = ''.join((equation[:intervalcounter],"*",equation[intervalcounter:]))
                    intervalcounter+=1
                    counter+=1
            elif i == ")":
                parathesesCounter-=1
            elif parathesesCounter == 0:
                if i in ["*","/","x"] or i.isdigit():
                    pass
                else:
                    onDisvior = False
                    interval[1] = counter
                    problems.append(equation[interval[0]+1:interval[1]])
                    inverval = [0,0]
        elif i == "/":
            onDisvior = True
            interval[0] = counter
        counter += 1
        intervalcounter +=1
    x = Symbol('x')
    for p in problems:
        for s in solve(p):
            nonallowed.append(s)
    return nonallowed
def callback(P):
    if str.isdigit(P[1:]) or P[1:] =="" :
        if P == "" or str.isdigit(P[0]) or P[0] in ["-"]:
            return True
        return False
    else:
        return False

def Riemmanstuff():
    global equation
    #try:
    equation = str(equationFunctionInput.get())
    numberOfRect = int(amountOfRectangles.get())
    interval[0]   = int(leftIntervalInput.get())
    interval[1]   = int(rightIntervalInput.get())
    GraphInterval = [interval[0]-0.05*abs(interval[0]),interval[1]+0.05*abs(interval[1])]
    GraphEquation = equation

    mainGraph.clf()
    GraphSubPlot = mainGraph.add_subplot(111)
    GraphSubPlot.set(title='Le Graph')
    GraphSubPlot.grid()


    x = np.array(np.arange(GraphInterval[0],GraphInterval[1],0.01))
    y = eval(GraphEquation)
    GraphSubPlot.plot(x,y)

    canvas.draw()
    currentAxis = mainGraph.gca()

    


    intervalLimits = findVerticalAsymptotes()
    if numberOfRect > m.pow(10,6):
        resultShower['text'] ='You have inputed a super large number, which will crash the program!'
        return
    estimatedArea = 0
    print(intervalLimits)
    for i in intervalLimits:
        if i >= interval[0] and i <= interval[1]:
            resultShower['text'] ='The interval is at a vertical asymptote! The program has detected x = ' + str(intervalLimits)
            return
    totalBase = abs(interval[1]-interval[0])
    for t in range(0, numberOfRect) :
        leftcurrent = (t)* totalBase/numberOfRect+interval[0]
        yValue = RectCaluclator(leftcurrent)
        currentAxis.add_patch(Rectangle((leftcurrent, 0), totalBase/numberOfRect,yValue, facecolor="grey"))
        area = totalBase/numberOfRect * yValue
        
        estimatedArea += area
    canvas.draw()
    resultShower['text'] = 'Estimated: '+ str(estimatedArea)

#except:
    resultShower['text'] ='An error occured, check if values are correctly inputed'


#GUI STUFF
#Button stuff

#main stuff
root = Tk()
canvas = FigureCanvasTkAgg(mainGraph, master=root)
vcmd = (root.register(callback)) #gets inputs
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