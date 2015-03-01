#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'Davinci'

from Tkinter import *
from math import pi,sin,cos
import threading
import time

x_list=[]
y_list=[]

def frange(start,stop,step=1.0):
    n=int((stop-start)/step)
    step_list=[]
    temp=start
    step_list.append(start)

    for i in range(n):
        temp += step
        step_list.append(temp)
    return step_list
step_range=frange(0,2*pi,0.01*pi)


class Planet():
    def __init__(self,master,n,x0=100,y0=100,R=10,color='White'):
        self.n=n
        self.master=master
        self.R=R
        self.x0=x0
        self.y0=y0
        self.color=color

    def DrawPlanet(self):
        self.planet=self.master.create_oval(
            self.x0-self.R,
            self.y0-self.R,
            self.x0+self.R,
            self.y0+self.R,
            fill=self.color,
            outline='')

    def DeletePlanet(self):
        self.master.delete(self.planet)

def Orbit(planet,satellite,speed=100,A=100,B=100):
    global canvas
    sleep_time = 1.0/speed
    while True:
        for t in step_range:
            #把坐标同步到全局的坐标列表
            px=x_list[planet.n]
            py=y_list[planet.n]

            sx=A*cos(t)+px
            sy=B*sin(t)+py

            satellite=Planet(canvas,
                             n=satellite.n,
                             x0=sx,
                             y0=sy,
                             R=satellite.R,
                             color=satellite.color)
            #把坐标同步到全局的坐标列表
            x_list[satellite.n]=sx
            y_list[satellite.n]=sy

            satellite.DrawPlanet()
            canvas.update()
            time.sleep(sleep_time)
            satellite.DeletePlanet()



def main():
    global root,canvas,cwidth,cheight
    #创造星型
    sun = Planet(canvas,n=0,x0=cwidth/2.0,y0=cheight/2.0,R=30,color='red')
    earth = Planet(canvas,n=1,x0=150,y0=150,R=15,color='blue')
    moon = Planet(canvas,n=2,x0=31,y0=90,R=5,color='yellow')
    mars = Planet(canvas,n=3,x0=32,y0=130,R=15,color='orange')
    aplit = Planet(canvas,n=4,x0=33,y0=80,R=14,color='gray')
    hadis = Planet(canvas,n=5,x0=35,y0=69,R=5,color='green')
    #编辑行行列表
    PlanetList=[sun,earth,moon,mars,aplit,hadis]
    #加入同步的坐标列表
    for item in PlanetList:
        x_list.append(item.x0)
        y_list.append(item.y0)
    
    #创建线程，每个运动的行星就是一个线程
    #创建的方式，由里向外的方式创建，要关注的是围绕关系
    #orbit(center,satellite,L,speed)
    #轨道（中心球体，卫星球体，围绕速度（int），围绕的半径）
    threading.Thread(target=Orbit,args=(sun,sun,1,0,0)).start()
    threading.Thread(target=Orbit,args=(sun,earth,50,100,200)).start()
    threading.Thread(target=Orbit,args=(earth,moon,100,30,30)).start()
    threading.Thread(target=Orbit,args=(sun,aplit,100,120,120)).start()
    threading.Thread(target=Orbit,args=(sun,hadis,190,260,260)).start()
    
    root.mainloop()

root = Tk()
root.title('行星运动')
cwidth=800
cheight=600

root.geometry('%dx%d'%(cwidth,cheight))
canvas = Canvas(root,width=cwidth, height=cwidth, bg='black')
#bt=Button(root,text='退出',command=root.destroy).pack(side=TOP)
canvas.pack(side=TOP)


if __name__=='__main__':
    main()