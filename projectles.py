#"""
#Created on Mon Nov 23 07:58:02 2020
#
#@author: mahir kaya
#Projectile Motion Simulation
#"""
#
#
###########IMPORTED MODULES############
import math
from tkinter import *
import tkinter 
import pylab
import PIL
import numpy as np 
from PIL import ImageTk,Image  

from matplotlib import pyplot as plt
##########################################
########GRAPH CLASSES###############
class Pos(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def __str__(self):
        return str(self.x)+','+str(self.y)
    
class projectile(object):
    
    def __init__(self, vi, initPos,angle=0 , g=-9.8,  finalPos=0):
        self.vi=vi
        self.angle=angle
        self.g=g
        self.initPos=initPos
        self.finalPos=finalPos
        self.accelerationx=0
        self.deltaxy=self.initPos.getY()-finalPos
        self.angleRadian=(math.pi/180)*(self.angle)
        self.Viy=((self.vi)*math.sin(self.angleRadian))
        self.Time=0
        self.OrigT=0
        self.origFP=0
        self.Vix=round(math.cos(self.angleRadian),2)*self.vi
        
    def calculateTimeToFall(self):        
        delta=((4*self.Viy**2)+(8*-self.g*self.initPos.getY()))**.5
        time=((2*self.Viy)+delta)/(-2*self.g)
        return time
    def getRange(self):
         Range=self.vi**2*2*math.sin(self.angleRadian)*math.cos(self.angleRadian)/-self.g
         Range=self.Vix*self.calculateTimeToFall()
         return round(Range,2)
     
    def update1s(self,time):
        self.Time+=time
        self.VY=self.Viy+self.g*self.Time
        xComponent=self.Vix*self.Time+(1/2*self.accelerationx*self.Time**2)
        yComponent=(self.Viy*self.Time+(1/2*self.g*self.Time**2))
        newPos=Pos(round(self.initPos.getX()+xComponent,2),round(self.initPos.getY()+yComponent,2))
        return(newPos)
        
    def graphDxT(self):
        x_values=[]
        y_values=[]
        y2_values=[]
        x_graph=[]
        p=0
        while True:
            updated=self.update1s(.1)    
            x_values.append(updated.getX())
            
            y_values.append(updated.getY())    
            if updated.getY()>self.finalPos:
                x_graph.append(updated.getX())
                y2_values.append(updated.getY())
                
            if updated.getY()<self.origFP:
                break
        with plt.style.context('dark_background'):
                plt.figure()
                plt.plot(x_values, y_values, 'b-o',label='projectile of ball with range '+ str(self.getRange())+' m')
                plt.plot(x_graph,y2_values,'y-o',label='Wanted path')
                StTime=str(round(self.calculateTimeToFall(),2))
                plt.xlabel("X Position",size=14)
                plt.ylabel("Y position",size=14)
                plt.scatter(self.initPos.getX(),self.initPos.getY(),color='r',label='starting point')
                plt.legend()
                plt.annotate('starting point',xy=(self.initPos.getX()-15,self.initPos.getY()-25),color='m')
                txt='Plot of a projectile fired with initial velocity of '+ str(self.vi)+ ' m/s at '+str(self.angle)+' degrees'
                txt2='Predicted flight time: '+str(round(self.calculateTimeToFall(),2))+ ' seconds'
                txt3='Predicted range for flight: '+ str(round(self.getRange(),2))+ ' meters'
                plt.figtext(0.5, -.1, txt, wrap=True, horizontalalignment='center', fontsize=1)
                plt.figtext(0.5, -.2, txt2, wrap=True, horizontalalignment='center', fontsize=14)
                plt.figtext(0.5, -.3, txt3, wrap=True, horizontalalignment='center', fontsize=14)
                plt.title("Position graph of the ball thrown at "+ str(self.angle)+' degrees with initial speed \n of '+str(self.vi)+' m/s  from position ' +str(self.initPos)+ ' that took '+str(StTime+' seconds'),fontsize=12)
                plt.savefig('DvT.png')
                plt.show()
                plt.close()
                self.Time=self.OrigT
            

    def graphSxT(self):
        x_values=[]
        y_values=[]
        k=0
        pos1=self.initPos
        while True:
            pos2=self.update1s(.1)
            d=pos2.getY()-pos1.getY()
            k+=0.1 
            Vy=(self.Viy**2+ 2*self.g*d)
            if Vy<0:
                Vy=abs(Vy)
            Vy=Vy**.5
            resultant=(Vy**2+self.Vix**2)**.5
            x_values.append(round(resultant,3))
            y_values.append(self.Time)
            if pos2.getY()<self.finalPos:
                break       
        with plt.style.context('dark_background'):
            plt.ylim([0,10])
            plt.figure()
            plt.plot(y_values,x_values, 'r--',label='speed')
            plt.xlabel("Time",size=14)
            plt.ylabel("Speed",size=14)
            txt="Speed graph over time"
            plt.title("Graph of the speed of the ball thrown at "+ str(self.angle)+' degrees \n with initial speed of '+str(self.vi)+' from position ' +str(self.initPos))
            plt.legend()
            plt.figtext(0.5, -.1, txt, wrap=True, horizontalalignment='center', fontsize=14)
            plt.savefig('VvT.png')
            self.Time=self.OrigT
            plt.close()
        
    def graphAvT(self):
        x_values=[]
        y_values=[]
        k=0
        while True:
            pos2=self.update1s(.1)
            aY=self.g 
            aX=self.accelerationx
            Vya=(aX**2+aY**2)**.5
            y_values.append(k)
            k+=.1
            x_values.append(round(Vya,3))
            if pos2.getY()<self.finalPos:
                break      
            
        with plt.style.context('dark_background'):
            plt.figure()
            plt.ylim(self.calculateTimeToFall())
            plt.plot( x_values,y_values, 'b--',label='acceleration')
            plt.ylabel("Time",size=14)
            plt.xlabel("Magnitude of Acceleration",size=14)
            plt.title("Graph of the acceleration of the ball thrown at "+ str(self.angle)+' degrees \n with initial speed of '+str(self.vi)+' from position ' +str(self.initPos))
            plt.legend(loc='best')
            txt="Magnitude of Acceleration graph over time"
            plt.figtext(0.5, -.1, txt, wrap=True, horizontalalignment='center', fontsize=14)

            plt.savefig('AvT.png')
            self.Time=self.OrigT
            plt.close()
    def graphAll(self):
        print('Starting')
        self.graphDxT()
        print(1)
        self.graphAvT()
        print(2)
        self.graphSxT()
        print(3)
a=projectile(10, Pos(0,100), angle=80)
a.graphAll()
print('Step 1 is completed')
##############SETTINGS FOR GEOMETYRY###############
master=Tk()
master.geometry('1400x570')
master.config(bg = "black")
master.title('Projectile Motion Simulation')
x=6
label=Label(master,text='Θ:',bg='black',fg='white').grid(row=1,column=1)
teta_entry=Entry(master,width=x)
angle_symbol=Label(master, text='°',bg='black',fg='white').grid(row=1,column=3)
teta_entry.insert(END,'0')

label2=Label(master,text='Initial Speed:',bg='black',fg='white').grid(row=2,column=1)
speed_entry=Entry(master,width=x)
speed_symbol=Label(master,text='m/s',fg='white', bg='black').grid(row=2,column=3)
speed_entry.insert(END, '10')

label3=Label(master,text='g:',bg='black',fg='white').grid(row=3,column=1)
g_entry=Entry(master,width=x)
g_symbol=Label(master,text='m/s/s',fg='white', bg='black').grid(row=3,column=3)
g_entry.insert(END,'-9.8')

label4=Label(master,text='Final Y pos:',bg='black',fg='white').grid(row=4,column=1)
FinalY=Entry(master,width=x)
Finaly_symbol=Label(master,text='m',fg='white', bg='black').grid(row=4,column=3)
FinalY.insert(END,'0')

label5=Label(master,text='Initial Coordinates:',bg='black',fg='white').grid(row=5,column=1)
Coordinates=Entry(master,width=x)
Coordinates_symbol=Label(master,text='x,y',fg='white', bg='black').grid(row=5,column=3)
Coordinates.insert(END,'0,100')
######Global Images#############
teta=float(teta_entry.get())
speed=float(speed_entry.get())
g=float(g_entry.get())
Yend=float(FinalY.get())    
coordinates=(Coordinates.get()).split(',')
Position=Pos(int(coordinates[0]),int(coordinates[1]))


img=PhotoImage(file='DvT.png')       
img2=PhotoImage(file='VvT.png') 
img3=PhotoImage(file='AvT.png')
###########BUTTONS##########
     
print('Step 2 is completed')
def XYgrapher():
    global img
    teta=float(teta_entry.get())
    speed=float(speed_entry.get())
    g=float(g_entry.get())
    Yend=float(FinalY.get())    
    coordinates=(Coordinates.get()).split(',')
    Position=Pos(int(coordinates[0]),int(coordinates[1]))
    projected=projectile(speed, Position, teta, g, Yend)
    projected.graphAll()
    img=PhotoImage(file='DvT.png')
    Label(master,image=img).grid(row=11,column=1,columnspan=10) 
    
def SvTgrapher():
    global img2
    teta=float(teta_entry.get())
    speed=float(speed_entry.get())
    g=float(g_entry.get())
    Yend=float(FinalY.get())    
    coordinates=(Coordinates.get()).split(',')
    Position=Pos(int(coordinates[0]),int(coordinates[1]))
    projected=projectile(speed, Position, teta, g, Yend)
    projected.graphAll()
    img2=PhotoImage(file='VvT.png')  
    Label(master,image=img2).grid(row=10,column=1,columnspan=10)   
    
def AvTgrapher():
    global img3
    teta=float(teta_entry.get())
    speed=float(speed_entry.get())
    g=float(g_entry.get())
    Yend=float(FinalY.get())    
    coordinates=(Coordinates.get()).split(',')
    Position=Pos(int(coordinates[0]),int(coordinates[1]))
    projected=projectile(speed, Position, teta, g, Yend)
    projected.graphAll()
    img3=PhotoImage(file='AvT.png')
    Label(master,image=img3).grid(row=10,column=9,columnspan=10)
img4=PhotoImage(file='logo.png')
Label(master,image=img4).grid(row=11,column=9,columnspan=10) 

Button(master,command=SvTgrapher,text='graph speed versus time',fg='white',bg='black').grid(row=1,column=6)
Button(master,command=XYgrapher,text='graph X versus Y',fg='white',bg='black').grid(row=1,column=5)
Button(master,command=AvTgrapher,text='graph acceleration versus time',fg='white',bg='black').grid(row=1,column=7)
####FINAL#####
print('Step 3 is completed')
teta_entry.grid(row=1,column=2)
speed_entry.grid(row=2,column=2)
g_entry.grid(row=3,column=2)
FinalY.grid(row=4,column=2)
Coordinates.grid(row=5,column=2)
mainloop()
