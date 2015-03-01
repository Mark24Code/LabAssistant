# Author : Md Adil Ansar
# Date   : 12 Aug 2013
# A basic Calculator Application


from Tkinter import Tk,W,E,BOTH
from Tkinter import StringVar
from ttk import Frame,Button,Label,Style
from ttk import Entry


def calci(string):
    if string == "":
        return ""
    try:
        ans = eval(string)
        a = "%.2f" % ans
        return a
        #if you do not want to restric the code to 2 decimal places use this
        #return ans 
    except:
        ans = 'Error!!'
        return ans
    

class Calculator(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()
        self.string = ""

    def initUI(self):
        self.parent.title("Calculator")
        Style().configure("TButton",padding = (0,5,0,5),font = 'serif 10')
        self.data = StringVar()
        self.columnconfigure(0,pad = 3)
        self.columnconfigure(1,pad = 3)
        self.columnconfigure(2,pad = 3)
        self.columnconfigure(3,pad = 3)

        self.rowconfigure(0,pad = 3)
        self.rowconfigure(1,pad = 3)
        self.rowconfigure(2,pad = 3)
        self.rowconfigure(3,pad = 3)
        self.rowconfigure(4,pad = 3)

        self.entry = Entry(self,textvariable = self.data)
        self.entry.grid(row = 0,columnspan = 4,sticky = W+E)
        self.entry.focus_set()
        
        cls = Button(self,text = 'CLS',command = lambda: self.reset())
        cls.grid(row = 1,column = 0)
        bck = Button(self,text = 'Backspace',command = lambda: self.decrement())
        bck.grid(row = 1,column = 1, columnspan = 2,sticky = W+E)
        clo = Button(self,text = 'Close', command = lambda: self.close())
        clo.grid(row = 1,column = 3)
        
        sev = Button(self,text = '7',command = lambda: self.concat('7'))
        sev.grid(row = 2,column = 0)
        eig = Button(self,text = '8',command = lambda: self.concat('8'))
        eig.grid(row = 2,column = 1)
        nin = Button(self,text = '9',command = lambda: self.concat('9'))
        nin.grid(row = 2,column = 2)
        div = Button(self,text = '/',command = lambda: self.addop('/'))
        div.grid(row = 2,column = 3)
        
        fou = Button(self,text = '4',command = lambda: self.concat('4'))
        fou.grid(row = 3,column = 0)
        fiv = Button(self,text = '5',command = lambda: self.concat('5'))
        fiv.grid(row = 3,column = 1)
        six = Button(self,text = '6',command = lambda: self.concat('6'))
        six.grid(row = 3,column = 2)
        mul = Button(self,text = '*',command = lambda: self.addop('*'))
        mul.grid(row = 3,column = 3)
        
        one = Button(self,text = '1',command = lambda: self.concat('1'))
        one.grid(row = 4,column = 0)
        two = Button(self,text = '2',command = lambda: self.concat('2'))
        two.grid(row = 4,column = 1)
        thr = Button(self,text = '3',command = lambda: self.concat('3'))
        thr.grid(row = 4,column = 2)
        mns = Button(self,text = '-',command = lambda: self.addop('-'))
        mns.grid(row = 4,column = 3)
        
        zer = Button(self,text = '0',command = lambda: self.concat('0'))
        zer.grid(row = 5,column = 0)
        dot = Button(self,text = '.',command = lambda: self.concat('.'))
        dot.grid(row = 5,column = 1)
        equ = Button(self,text = '=',command = lambda: self.calculate())
        equ.grid(row = 5,column = 2)
        plu = Button(self,text = '+',command = lambda: self.addop('+'))
        plu.grid(row = 5,column = 3)
        self.pack()

    def addop(self, op):
        if '.' not in str(self.string):
            self.string = str(self.string)+str('.0')+str(op)
        else:
            self.string = str(self.string)+str(op)
        self.data.set(self.string)
        
    def calculate(self):
        self.string = self.data.get()
        self.string = calci(self.string)
        self.data.set(self.string)

    def concat(self,this):
        self.string = str(self.string)+str(this)
        self.data.set(self.string)

    def reset(self):
        self.string = ""
        self.data.set(self.string)

    def decrement(self):
        self.string = str(self.string)[0:len(str(self.string))-1]
        self.data.set(self.string)

    def close(self):
        self.parent.destroy()


def main():
    root = Tk()
    app = Calculator(root)
    root.mainloop()


if __name__ ==  '__main__':
    main()
