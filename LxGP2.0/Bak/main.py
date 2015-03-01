#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import os
import sys,time
import Tkinter
import webbrowser
from tkintertable.Tables import TableCanvas
from tkintertable.Tables import TableModel
sys.modules['tkinter']=Tkinter
VERS = '高中物理实验辅助程序 V0.4'

WORKPATH = os.getcwd()

class Window(Tkinter.Tk):
    def __init__(self):
        Tkinter.Tk.__init__(self)
        #菜单部分
        self.title('高中物理实验辅助程序')
        self.wm_geo()
        self.main_menu=Tkinter.Menu(self)
        #菜单1：文件：打开，退出
        self.a_menu = Tkinter.Menu(self.main_menu,tearoff = 0)
        self.a_menu.add_command(label = '打开')
        self.a_menu.add_command(label = '退出',command = self.quitwin)
        #菜单2：设置：文字大小，偏好设置
        self.b_menu = Tkinter.Menu(self.main_menu,tearoff = 0)
        self.b_menu.add_command(label = '文字大小')
        self.b_menu.add_separator()#分割符号

        #v 是单选按钮的组变量，同时设置一下默认选项
        #self.b_menu.add_radiobutton(label = '多窗口模式')
        #菜单3：帮助：使用说明
        self.b_menu = Tkinter.Menu(self.main_menu,tearoff = 0)
        self.b_menu.add_command(label = '使用说明',command=self.helper)
        self.b_menu.add_command(label='关于',command=self.about)

        #把分菜单，加入主菜单栏
        self.main_menu.add_cascade(label = '文件',menu = self.a_menu)
        self.main_menu.add_cascade(label = '帮助',menu = self.b_menu)
        #把设置好的菜单，和根目录链接起来
        self['menu'] = self.main_menu

    def quitwin(self):
        self.destroy()
    def wm_geo(self,width=500,height=360):
        ws=self.winfo_screenwidth()
        hs=self.winfo_screenheight()
        self.x=(ws/2.0)-(width/2.0)
        self.y=(hs/2.0)-(height/2.0)
        self.withdraw()
        self.geometry("%dx%d+%d+%d"%(width,height,self.x,self.y))
        self.deiconify()

    def helper(self):
        Helper()
    def about(self):
        About()

class Helper(object):
    def __init__(self):
        top = Tkinter.Toplevel()
        top.title('物理辅助程序帮助')
        top.geometry('400x420+300+200')
        self.helper_text=Tkinter.Text(top,cursor='hand2')
        self.helper_text.pack(fill='both',expand=1)
        self.textname='物理辅助程序帮助'
        self.texthead='\n   物理实验辅助程序'
        self.text=\
            '是一个简单的基于Python的，图形界面使用Tkinter。提供高中物理实验辅助的程序。\n' \
            '\n[使用说明]:\n   主界面有两个区，一个是核心基本实验区，一个是核心的工具区。实验区提供了实验列表，进入相关的实验中，' \
            '实验提供了实验需要的实验工具，一般都是从实验工具列表中组合得到，还有实验的相关说明。' \
            '\n实验工具中提供的工具可以单独的使用。\n' \
            '程序还提供模拟实验的装置，可以用于战士一些模拟实验动画。' \
            '\n更新日志：\n' \
            'V0.3. 添加的模拟物理实验的动画\n' \
            'V0.2  完成了实验内容的增添\n' \
            'V0.1  完成了基本框架以及图表的内容，\n'
        self.helper_text.tag_config('name', justify='center', font=('Helvetica', 16, 'bold'))
        self.helper_text.tag_config('head', justify='center', font=('Helvetica', 12, 'bold'))
        self.helper_text.tag_config( 'text',justify='left', font=('Helvetica', 11))
        self.helper_text.insert('end',self.textname,'name')
        self.helper_text.insert('end',self.texthead,'head')
        self.helper_text.insert('end',self.text,'text')

        self.helper_text['state']='disable'


class About(object):
    def __init__(self):
        top = Tkinter.Toplevel()
        top.title('关于实验辅助程序')
        top.geometry('240x250+300+300')
        self.about_text = Tkinter.Text(top, cursor='hand2')
        self.about_text.pack(fill='both', expand=1)
        self.info_list = ['\n%s\n\n'%VERS,
                    '可以辅助高中实验的教学程序demo\n',
                    '作者: 谈 玲\n',
                    '\n',
                    '(c) 2014\n',
                    '< linda.tanling@gmail.com >',
                    ]
        self.about_text.tag_config('name', justify='center', font=('Helvetica', 16, 'bold'))
        self.about_text.tag_config('info', justify='center', font=('Helvetica', 9))
        self.about_text.tag_config('url', justify='center', font=('Helvetica', 10),foreground='blue', underline=1)
        #self.about_text.tag_bind('url', '<Button>', self.browser)

        self.about_text.insert('end', self.info_list[0], 'name')
        self.about_text.insert('end', self.info_list[1], 'info')
        self.about_text.insert('end', self.info_list[2], 'info')
        self.about_text.insert('end', self.info_list[3], 'url')
        self.about_text.insert('end', self.info_list[4], 'info')
        self.about_text.insert('end', self.info_list[5], 'info')
        self.about_text['state'] = 'disabled'

    def browser(self, event):
        webbrowser.open(self.info_list[3])

class Mainwm(Window):
    def __init__(self):
        Window.__init__(self)
        self.mlogo=Tkinter.PhotoImage(file='%s/Pic/Logo.gif'%WORKPATH)
        #实验界面
        self.exp_frm=Tkinter.LabelFrame(self,text='列表')
        self.exbt1=Tkinter.Button(self.exp_frm,
                                            text='实验1.匀速直线运动',
                                            height=2,
                                            width=30,
                                            command=Exp1).pack(side=Tkinter.TOP,expand=1)
        self.exbt2=Tkinter.Button(self.exp_frm,
                                            text='实验2.验证平抛运动',
                                            height=2,
                                            width=30,
                                           command=Exp2 ).pack(side=Tkinter.TOP,expand=1)
        self.exbt3=Tkinter.Button(self.exp_frm,
                                            text='实验1.绘制小电珠的伏安特性曲线',
                                            height=2,
                                            width=30,
                                            command=Exp3).pack(side=Tkinter.TOP,expand=1)
        self.exbt4=Tkinter.Button(self.exp_frm,
                                            text='实验4.demo未开发',
                                            height=2,
                                            width=30,
                                           command=Exp2 ).pack(side=Tkinter.TOP,expand=1)
        self.exbt5=Tkinter.Button(self.exp_frm,
                                            text='实验5.demo未开发',
                                            height=2,
                                            width=30,
                                            command=Exp3).pack(side=Tkinter.TOP,expand=1)

        self.exp_frm.grid(row=0,column=0,ipadx=5,ipady=5)
        #工具集合
        self.tools_frm=Tkinter.LabelFrame(self,text='工具集合')
        self.tbt1=Tkinter.Button(self.tools_frm,
                                            text='数据绘图',
                                            height=2,
                                            width=30,
                                            command=self.pop_tool1).pack(side=Tkinter.TOP,expand=1)
        self.tbt2=Tkinter.Button(self.tools_frm,
                                            text='计算器',
                                            height=2,
                                            width=30,
                                            command=self.pop_tool2).pack(side=Tkinter.TOP,expand=1)
        self.tbt3=Tkinter.Button(self.tools_frm,
                                            text='物理模型',
                                            height=2,
                                            width=30,
                                            command=self.pop_tool3).pack(side=Tkinter.TOP,expand=1)
        self.tbt4= Tkinter.Button(self.tools_frm,
                                            text='计时器',
                                            height=2,
                                            width=30,
                                            command=self.pop_tool4).pack(side=Tkinter.TOP,expand=1)
        self.tbt5= Tkinter.Button(self.tools_frm,
                                            text='聊天功能',
                                            height=2,
                                            width=30,
                                            command=self.pop_tool5).pack(side=Tkinter.TOP,expand=1)

        self.tools_frm.grid(row=0,column=1,ipadx=5,ipady=5)

        #显示logo和权利声明
        self.Logo()

    def Logo(self):
        self.llb = Tkinter.Label(self,
                   text='CopyRight©2014->Inf.Zero Group. All Rights Reserved.',
                   compound = 'left',
                   image=self.mlogo).grid(row=1,column=0,columnspan=2,ipadx=5,ipady=5)

    #实验部分，函数接口
    def pop_exp1(self):
        Exp1()
    def pop_exp2(self):
         Exp2()
    def pop_exp3(self):
         Exp3()
    #工具部分，函数接口
    def pop_tool1(self):
        Table()
    def pop_tool2(self):
        Calc()
    def pop_tool3(self):
        Model()
    def pop_tool4(self):
        Timer()
    def pop_tool5(self):
        Chat()

#封面功能的设计
def Exp1():
    exp1wm=Tkinter.Toplevel()
    exp1wm.title('实验1.匀速直线运动')
    #表格
    tablefrm=Tkinter.LabelFrame(exp1wm,text='表格')
    table=TableCanvas(tablefrm)
    table.createTableFrame()
    tablefrm.grid(row=0,column=0)
    #实验说明
    textfrm=Tkinter.LabelFrame(exp1wm,
                                            text='实验说明')
    exp1text=Tkinter.Text(textfrm,height=20)
    exptxt='1．2  匀速直线运动的实验研究\n【教学目标】\n' \
           '1、理解匀速直线运动，会判定匀速直线运动。\n' \
           '2、会运用公式S=vt解有关问题。\n' \
           '【教学重点、难点】\n' \
           '匀速直线运动的规律的灵活运用。\n【教学方法】\n' \
           '实验与练习法。\n' \
           '【教学过程】\n回顾初中的定义——物体作匀速直线运动的速度大小等于路程与通过这段路程所需时间的比。怎样判断和测定匀速直线运动的速度？\n' \
           '实验1.2\n[目的]:\n1．判定匀速直线运动。\n2．测定匀速直线运动的速度。\n' \
           '[器材]  500mL的量筒、蓖麻油、钢珠、刻度尺、节拍器。\n' \
           '节拍器是一种计时工具。它所发出的每两个相邻节拍声之间的时间是一定的，时间的长短可以通过改变摆锤在摆杆上的位置来调节。摆杆上刻有40～208的标度，如把摆锤移动到120的标度上，摆每分钟就摆动120次，每两个相邻节拍声之间的时间为0．5s。\n' \
           '[步骤]\n调节节拍器摆锤的位置，使它发出每分钟60次的节拍声。\n' \
           '2．把钢珠由静止开始下落到盛满蓖麻油的量筒。待钢珠进入油面后，每次听到节拍声时，把钢珠的位置记录下来。\n' \
           '3．用刻度尺测量相邻节拍声之间钢珠通过的路程。\n' \
           '4．确定钢珠开始作匀速直线运动的位置。\n5．计算钢珠作匀速直线运动的速度。\n6．重复实验两次。\n'
    exp1text.insert('end',exptxt)
    exp1text.pack()
    textfrm.grid(row=0,column=1)

def Exp2():
    exp1wm=Tkinter.Toplevel()
    exp1wm.title('实验2.验证平抛运动')
    #表格
    tablefrm=Tkinter.LabelFrame(exp1wm,text='表格')
    table=TableCanvas(tablefrm)
    table.createTableFrame()
    tablefrm.grid(row=0,column=0)
    #实验说明
    textfrm=Tkinter.LabelFrame(exp1wm,
                                            text='实验说明')
    exptxt='一、研究平抛物体的运动\n【重要知识提示】\n1．实验目的、原理\n(1)实验目的：\n' \
           '(a)用描迹法描出平抛物体的运动轨迹；\n' \
           '(b)求出平抛物体的初速度；\n' \
           '(2)实验原理：\n(a)平抛运动可以看作是由两个分运动合成，一个是在水平方向上的匀速直线运动，其速度等于平抛物体运动的初速度，另一个是在竖直方向上的自由落体运动．\n' \
           '(b)在水平分运动中，运用x=v•t；在竖直分运动中，运用y=1/2gt2或△y=gT2．\n' \
           '  2．实验器材\n斜槽(附挡球板和铅锤线)、水准仪、小钢球、木板、竖直固定支架、刻度尺、三角板、白纸、图钉、定点用的有孔卡片、重垂、铅笔等 \n' \
           '说明  定点用的有孔卡片的制作要求如图5—1所示，在方形硬纸上沿中间实线挖出一个孔，孔宽(A)应稍大于钢球直径，孔长(B)一般大于钢球直径．\n' \
           '实验步骤及安装调整\n(1)描述平抛物体运动的轨迹:\n' \
           '(a)将斜槽放在桌面上，让其末端伸出桌面边缘外．借助水准仪调节末端，使槽末端切线水平，随之将其固定，如图5—2所示．\n' \
           '说明  如果没有水准仪，则可将钢球放于槽的末端．调节斜槽后，轻轻拨动钢球，若钢球能在任何位置平衡，说明达到要求；\n' \
           '(b)用图钉将白纸钉在木板上，让木板左上方靠近槽口处桌面边缘，用支架将木板竖直固定，使小球滚下飞出槽口后的轨迹平面跟板面平行；\n' \
           '(c)将小球飞离斜槽末端时的球心位置水平投影到白纸上描点O，并过。沿重垂线用直尺描出竖直方向；\n' \
           '(d)选择钢球从槽上滚下的合适初位置Q，在Q点放上挡球板；\n' \
           '(e)将小球从斜槽上释放，用中心有孔的卡片靠在纸面上并沿纸面移动，当飞行的小球顺利地穿过卡片上小孔时，在小孔靠近纸面所在处做上记号；重复该步骤，描下至少5个不同位置的对应点；\n' \
           '(f)把白纸从木板上取下来，将前面描述的一系列点用平滑的曲线连接起来，即为小球平抛运动的轨迹．\n' \
           '(2)求小球平抛的初速度：\n' \
           '(a)以。为坐标原点，用三角板在白纸上建立z0夕坐标系\n' \
           '(b)在轨迹线上选取点M，并测出它的坐标值(z，y)，代人公式计算水平初速度；\n' \
           '(c)再在曲线上选取不同点，重复步骤2(b)，测量、计算水平初速度，最后求出其平均值，即为小球平抛初速度的测量值．\n' \
           '4．注意事项\n' \
           '(1)在调整安装时，应保证斜槽末端切线水平，确保钢球飞出后作平抛运动；应使木板(包括白纸)靠近槽口、竖直且与小球运动轨迹所在平面平行，确保运动小球靠近木板，但不接触木板.\n' \
           '(2)在实验中应使用斜槽挡球板，保证小球每次均从同一位置无初速释放．\n' \
           '说明：斜槽挡球板的位置应恰当，以便使小球的运动轨迹由木板左上角到右下角.\n(3)在取下白纸前，应在白纸上记下小球飞离槽口时球心位置0(钢球球心在图板上的水平投影点，而不是斜槽末端点的投影)，如图5—3所示．确定坐标轴原点，并用重垂线过0  作竖直线，以准确确定坐标系的y轴．\n' \
           '(4)在轨迹曲线上选点时，应选离坐标原点稍远的点用以测量计算，这样可减小误差.'

    exp1text=Tkinter.Text(textfrm,height=20)
    exp1text.insert('end',exptxt)
    exp1text.pack()
    textfrm.grid(row=0,column=1)

def Exp3():
    exp1wm=Tkinter.Toplevel()
    #exp1wm.wm_geo(width=1050,height=380)
    exp1wm.title('实验3.描绘小电珠的伏安特性曲线')
    #表格
    tablefrm=Tkinter.LabelFrame(exp1wm,text='表格')
    table=TableCanvas(tablefrm)
    table.createTableFrame()
    tablefrm.grid(row=0,column=0)
    #实验说明
    textfrm=Tkinter.LabelFrame(exp1wm,
                                            text='实验说明')
    exptxt='知识点：实验七：描绘小灯泡的伏安特性曲线\n知识点总结\n' \
           '描绘小灯泡的伏安特性曲线；并分析曲线的变化规律。\n' \
           '一、实验目的\n1.描绘小灯泡的伏安特性曲线。\n' \
           '2.分析曲线变化规律。\n二、实验原理\n用电流表测流过小灯泡的电流，用电压表测出加在小灯泡两端的电压，测出多组对应的U、I值，在直角坐标系中描出各对应点，用一条平滑的曲线将这些点连接起来。\n' \
           '三、实验器材\n小灯泡、4V~6V学生电源、滑动变阻器、电压表、电流表、开关、导线若干\n四、实验步骤\n1．连接电路：将小灯泡、电流表、电压表、滑动变阻器、开关用导线按照电路图连接起来。\n' \
           '2. 测出小灯泡在不同电压下的电流。移动滑动变阻器触头位置，测出12组左右不同的电压值U和电流值I，并将测量数据填入已经画好的表格中。\n' \
           '3．画出伏安特性曲线。\n⑴在坐标纸上以U为横轴，以I为纵轴，建立坐标系。\n⑵在坐标纸上描出各做数据对应的点。注意横纵坐标的比例标度选取要适中，以使所描图线占据整个坐标纸为宜。\n' \
           '⑶将描出的点用平滑的曲线连接起来，就得到小灯泡的伏安特性曲线\n4.拆除电路，整理仪器。\n五、注意事项\n' \
           '1．电路的连接方式\n⑴电流表应采用外接法：因为小灯泡的电阻很小，与0~0.6A的电流表串联式，电流表的分压影响很大。\n' \
           '⑵滑动变阻器应采用分压式连接：目的是使小灯泡两端的电压能从0开始变化。\n2．闭合电键S之前，一定要使滑动变阻器的滑片处于恰当的位置（应该使小灯泡被短路）。\n' \
           '3．保持小灯泡电压接近额定值是要缓慢增加，到额定值，记录I后马上断开开关。\n' \
           '4．误差较大的点药舍去，U-I图像应是平滑曲线而非折线。\n常见考法\n' \
           '近几年，涉及小灯泡的伏安特性曲线的题目成为高考的热点，因为该实验考题灵活，即可以考查仪器的选择又可以考查实验电路图的连接，还可以考查数据和图像。本考点有三大考点：⑴电路的选择⑵仪器的选择和连接⑶数据和图像，对于小灯泡的电阻随着温度的升高而改变的情形可以画出U-I图像或者I-U图像是一条曲线来研究小灯泡的规律。\n' \
           '误区提醒\n1.由于电压表不是理想电表,内阻并非无穷大,对电路的影响会带来误差.\n2.在坐标纸上描点、作图带来误差.\n' \
           '3.由于小灯泡在电压较低时没有发光,灯丝温度较低,其电阻变化不明显,所以在伏安特性曲线的开始一段接近直线.但随着电压的不断增大,灯泡开始发光,温度变化很大,因此对应电阻值也变化很大,伏安特性曲线为曲线.'
    exp1text=Tkinter.Text(textfrm,height=20)
    exp1text.insert('end',exptxt)
    exp1text.pack()
    textfrm.grid(row=0,column=1)

def Table():
    tbwm=Tkinter.Toplevel()
    tbwm.title('计算表格')
    tfrm=Tkinter.Frame(tbwm)
    tfrm.pack()
    #表格
    table=TableCanvas(tfrm)
    table.createTableFrame()

def Calc():
    os.system('python Script/Calculator.py')

def Model():
    modelwm=Window()
    modelwm.wm_geo(width=380,height=380)
    modelwm.title('模拟实验')
    #实验动画
    mbfrm=Tkinter.LabelFrame(modelwm,text='模拟实验动画列表')
    mbt1=Tkinter.Button(mbfrm,
                       text='万有引力,星体运动',
                       width=40,
                       height=2,
                       command=StarModel).pack(side=Tkinter.TOP,expand=1)
    mbt2=Tkinter.Button(mbfrm,
                        text='小球弹性碰撞',
                        width=40,
                        height=2,
                        command=CrashBall).pack(side=Tkinter.TOP,expand=1)
    mbfrm.pack()


#线程

class MyThread(threading.Thread):
    def __init__(self, func, argv, dae=True):
        threading.Thread.__init__(self)
        self.func = func
        self.argv = argv
        self.setDaemon(dae)
        self.start()

    def run(self):
        self.func(*self.argv)

#模拟实验部分
def StarModel():
    os.system('python %s/Script/StarModel.py'%WORKPATH)
def CrashBall():
    os.system('python %s/Script/MultiBall.py'%WORKPATH)
def Timer():
    os.system('python %s/Script/Timer.py'%WORKPATH)
def Chat():
    os.system('python %s/Script/Chat.py'%WORKPATH)
#封面


if __name__ == '__main__':
    os.system('python  %s/CoverScript/Cover_Expmain.py'%WORKPATH)
    main = Mainwm()
    main.mainloop()