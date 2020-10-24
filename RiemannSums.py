from tkinter import *
import math as m
import tkinter.font as tkFont
import re


def Riemmanstuff():
    numberOfRect = int(amountOfRectangles.get())
    estimatedArea = 0
    totalBase = interval[1]-interval[0]
    for t in range(0, numberOfRect) :
        leftcurrent = (t)* totalBase/numberOfRect+interval[0]
        area = totalBase/numberOfRect * Equation(leftcurrent)
        estimatedArea += area
    print(estimatedArea)

def Equation(fltnumb):
    return 1/fltnumb

def callback(P):
    if str.isdigit(P) or P == "":
        return True
    else:
        return False

#GUI STUFF
#Button stuff

#main stuff
root = Tk()
vcmd = (root.register(callback))
root.geometry("1200x800")
root.title("Riemann sum calculator")
#Widgets
SubTitle = Label(root, text="Riemann sum calculator", font=("Courier", 10))
typeTitle = Label(root, text="Type/Starting point")
numOfRectTitle = Label(root, text="How many rectangles to calculate?")

calculateButton = Button(root, text="Calculate!", padx=150, command=Riemmanstuff)


amountOfRectangles = Entry(root, validate = 'all', validatecommand=(vcmd, '%P')) #validatecommand and validate limit input to digits


equationFunction = Entry(root)

typeOfSum = (Listbox(root, height=2))
typeOfSum.insert(1,"Left")
typeOfSum.insert(2,"Right")

#Display stuff
SubTitle.pack(anchor='nw')
typeTitle.pack(anchor='nw')
typeOfSum.pack(anchor='nw')
numOfRectTitle.pack(anchor="nw")
amountOfRectangles.pack(anchor='nw')


calculateButton.pack(anchor='nw')

root.mainloop() # runs main loop

numberOfRect = 0 # int(input("type in an integer to calculate:  "))
interval     =(1,m.e)

#def Pageinnit():
