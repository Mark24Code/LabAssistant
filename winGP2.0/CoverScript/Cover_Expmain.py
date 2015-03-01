#!/usr/bin/env/python
# -*- coding: utf-8 -*-
__author__ = 'matrix24'


#!/usr/bin/env/python
# -*- coding: utf-8 -*-
__author__ = 'matrix24'
import Tkinter
import os

WORKPATH = os.getcwd()

class Cover(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.withdraw()
        self.width = 694
        self.height = 555

        self.cfrm = Tkinter.Toplevel(self)
        self.cimage = Tkinter.PhotoImage(file='%s/Pic/Cover_Exp.gif'%WORKPATH)
        self.cfrm.overrideredirect(1)
        prograssbar = '请点击\n'
        clb = Tkinter.Label(self.cfrm,
                                    text=prograssbar,
                                    compound ='top',
                                    image=self.cimage).pack(fill=Tkinter.BOTH,expand=1)
        ws=self.cfrm.winfo_screenwidth()
        hs=self.cfrm.winfo_screenheight()
        x=(ws/2.0)-(self.width/2.0)
        y=(hs/2.0)-(self.height/2.0)
        self.cfrm.withdraw()
        self.cfrm.geometry("%dx%d+%d+%d"%(self.width,self.height,x,y))
        self.cfrm.deiconify()
        self.lower(self.cfrm)
        self.cfrm.bind('<Button-1>',self.delself)
    def delself(self,event):
        self.destroy()

if __name__=='__main__':
    cover=Cover()
    cover.mainloop()
