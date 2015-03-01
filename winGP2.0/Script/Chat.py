#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
程序说明：

  建立一个基于TCP/IP socket的可靠传输的,多线程，多人聊天,并且可以多人传输文件的程序。
特点，单个程序既可以作为客户端又可以作为服务器；去中心化。
灵活的提供解决方案。
  可以用来在课堂上或者任意局域网环境中，交流，提交作业。
跨平台特点，可以在各种机器系统之间提供文件和文字传输。

作者 张阳
联系 mark.zhangyoung@gmail.com
时间 2014年5月9日
'''
import socket
import threading
import webbrowser
import time
import os
import os.path
import Tkinter
import tkSimpleDialog
import tkFileDialog
import tkMessageBox
from functools import partial

WORKPATH=os.getcwd()

try:
    import winsound
    ring = lambda: winsound.PlaySound('%s/Ring/ring.wav'%WORKPATH, winsound.SND_NODEFAULT | winsound.SND_ASYNC)
except ImportError:
    import subprocess
    ring = lambda: subprocess.call(['aplay', '%s/Ring/ring.wav'%WORKPATH])

try:
    import cPickle as pickle
except ImportError:
    import Pickle as pickle

#为了获取自身IP做准备
#python中 os.name是系统平台的名称 windows对应nt；Linux/Unix对应 posix
if os.name != 'nt':
    import fcntl
    import struct

HOST = ''
BUFSIZE = 4096
PORT = 65500
VERS = '微聊 V0.3'
IP = None
nick_name = ''


class Window(Tkinter.Tk):
    def __init__(self, sock):
        Tkinter.Tk.__init__(self)
        self.sock = sock
        self.width=500
        self.height=500
        self.wm_minsize(width=self.width, height=self.height)
        self.wm_maxsize(width=self.width+30, height=self.height+30)
        self.title(VERS)
        #Button的偏函数和Text的偏函数
        self.Button = partial(Tkinter.Button, height=1, width=5,relief=Tkinter.GROOVE, )
        self.Text = partial(MyText, font=('Helvetica', 11),highlightthickness=0, padx=1, pady=1, )

        #菜单功能
        self.menu = Tkinter.Menu(self)
        #选项子菜单
        option_menu = Tkinter.Menu(self.menu,tearoff=0)
        option_menu.add_command(label='发送信息',command= self.send_chat)
        option_menu.add_command(label='发送文件',command=self.send_file)
        option_menu.add_command(label='退出',command=self.ask_exit)
        #帮助菜单
        help_menu = Tkinter.Menu(self.menu,tearoff=0)
        help_menu.add_command(label='使用说明',command=self.helper)
        help_menu.add_command(label='关于',command=self.about)
        #添加选项、帮助进入主菜单
        self.menu.add_cascade(label='选项',menu=option_menu)
        self.menu.add_cascade(label='帮助',menu=help_menu)
        #设置窗口默认的菜单栏为menu
        self['menu']=self.menu
        #右击菜单
        self.the_menu=Tkinter.Menu(self,tearoff=0)
        self.the_menu.add_command(label='剪切',accelerator='Ctrl+X',command=lambda: self.focus_get().event_generate('<<Cut>>'))
        self.the_menu.add_command(label='复制',accelerator='Ctrl+C',command=lambda: self.focus_get().event_generate('<<Copy>>'))
        self.the_menu.add_command(label='粘贴',accelerator='Ctrl+V',command=lambda: self.focus_get().event_generate('<<Paste>>'))
        self.bind('<Button-3>',self.popup)

        self.my_ip = self.get_ip()

        #个人信息栏
        #显示昵称
        self.mynamefrm = Tkinter.LabelFrame(self,text='昵称')
        self.myname_entry = Tkinter.Entry(self.mynamefrm,
                                                            highlightthickness=0,
                                                            relief=Tkinter.FLAT,
                                                            width=24,
                                                            bg='#f5f5f5')
        self.myname_entry.insert(0,nick_name)
        self.myname_entry.bind('<FocusIn>',self.no_input)
        self.myname_entry.pack(side=Tkinter.LEFT)
        self.mynamefrm.grid(row=0,column=0)
        #显示IP
        self.myinfofrm = Tkinter.LabelFrame(self,text='本机IP')
        self.myinfo_entry = Tkinter.Entry(self.myinfofrm,
                                                            highlightthickness=0,
                                                            relief=Tkinter.FLAT,
                                                            width=24,
                                                            bg='#f5f5f5')
        self.myinfo_entry.insert(0,self.my_ip)
        self.myinfo_entry.bind('<FocusIn>',self.no_input)
        self.myinfo_entry.pack(side=Tkinter.LEFT)
        self.myinfofrm.grid(row=1,column=0)

        #传输进度框
        self.label_frame = Tkinter.LabelFrame(self, text='传输进度:')
        self.progress_entry = Tkinter.Entry(self.label_frame,
                                            highlightthickness=0,
                                            relief=Tkinter.FLAT,
                                            width=46,
                                            fg='red',
                                            bg='#f5f5f5')

        self.progress_entry.bind('<FocusIn>', self.no_input)
        self.progress_entry.pack()
        self.label_frame.grid(row=0, column=1)

        #文件传输按钮
        self.trspt_frm = Tkinter.Frame(self)
        self.Button(self.trspt_frm,
                            text='发文件',
                            command=self.send_file
                            ).pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
        self.Button(self.trspt_frm,
                            text='收文件',
                            command=self.recv_file
                            ).pack(side=Tkinter.RIGHT, fill=Tkinter.BOTH)
        self.trspt_frm.grid(row=1, column=1, ipadx=2)


        #输出窗口
        self.outfrm = Tkinter.LabelFrame(self,text='聊天框')
        self.outtex = self.Text(self.outfrm, height=10, width=56)
        self.outtex.tag_config('warning', foreground='red', font=('Helvetica', 9, 'bold'))
        self.outtex.tag_config('remote', foreground='blue')
        self.outscl = Tkinter.Scrollbar(self.outfrm)
        self.outtex['yscrollcommand'] = self.outscl.set
        self.outscl['command'] = self.outtex.yview
        self.outtex.bind('<FocusIn>', self.no_input)
        self.outtex.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
        self.outscl.pack(sid=Tkinter.RIGHT, fill=Tkinter.BOTH)
        self.outfrm.grid(row=2, column=0,columnspan=2)


        #输入窗口
        self.infrm = Tkinter.LabelFrame(self,text='输入框')
        self.intex = self.Text(self.infrm, height=5, width=56)
        self.inscl = Tkinter.Scrollbar(self.infrm)
        self.intex['yscrollcommand'] = self.inscl.set
        self.inscl['command'] = self.intex.yview
        self.intex.bind('<Return>', self.send_chat)
        self.intex.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
        self.inscl.pack(side=Tkinter.RIGHT, fill=Tkinter.BOTH)
        self.infrm.grid(row=4, column=0,columnspan=2)
    
        #功能按键的Frame
        self.but2frm = Tkinter.Frame(self)
        self.Button(self.but2frm, 
                text='退出', 
                fg='red', 
                command=self.ask_exit,
                ).pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
        self.Button(self.but2frm,
                text='发送', 
                command=self.send_chat, 
                ).pack(side=Tkinter.RIGHT, fill=Tkinter.BOTH)
        self.but2frm.grid(row=5, column=0, ipadx=40, pady=5,columnspan=2)

    def popup(self,event):
        self.the_menu.post(event.x_root,event.y_root)

    def ask_exit(self):
        if tkMessageBox.askyesno(VERS, '    确认退出？'):
            self.destroy()
    
    def about(self):
        show_about = About()
    def helper(self):
        show_helper=Helper()

    #防止用户上屏输入的方法
    def no_input(self, event):
        self.intex.focus_set()

    #创建一个可以获得当前工作IP的函数
    def get_ip(self):
        return get_my_ip()
    
    #创建一个接收文件的线程 
    def recv_file(self):
        transport_thread = MyThread(file_in,(self,))
    
    #创建一个发送文件的线程
    def send_file(self):
        file_path = tkFileDialog.askopenfilename(title='选择要发送的文件',filetypes=[('All files', '*')])
        if not file_path:
            return
        file_name = os.path.split(file_path)[1].encode('utf8')
        file_size = os.stat(file_path).st_size
        file_dscrp = open(file_path, 'rb')
        sock.client_sock.send(pickle.dumps('对方要发送文件，若接收请点[接收文件]。', 2))
        self.outtex.my_insert('end', '等待对方同意...\n', 'warning')
        transport_thread = MyThread(file_out,(self, file_dscrp, (file_name, file_size)))
    
    def send_chat(self, event):
        global nick_name
        '''发送信息
        '''
        data = self.intex.get(1.0, 'end').strip().encode('utf8')
        if not data:
            self.intex.delete(1.0, 'end')
            return 'break'
        data = nick_name+': '+'%s'%time.strftime('%H:%M:%S',time.localtime(time.time()))+'\n'+data
        pickle_data = pickle.dumps(data, 2)
        self.sock.client_sock.send(pickle_data)
        self.outtex.my_insert('end',data+'\n')
        self.intex.delete(1.0, 'end')
        return 'break'

class Helper(object):
    def __init__(self):
        top = Tkinter.Toplevel()
        top.title('微聊帮助')
        top.geometry('400x420+300+200')
        self.helper_text=Tkinter.Text(top,cursor='hand2')
        self.helper_text.pack(fill='both',expand=1)
        self.textname='微聊帮助'
        self.texthead='\n  微聊'
        self.text=\
            '是一个简单的基于socket的聊天工具，图形界面使用Tkinter。提供双向的，双工聊天和文件传输功能。\n' \
            '\n[使用说明]:\n   刚开始进入的时候，输入昵称。然后将会是提示输入IP，这里准备了两个模式，当你选择Cancel，则认为是进入等待' \
            '连接的状态，你的角色是服务器，等待对方连接。当你选择输入IP，提示：IP就是对方聊天端的地址，可以简单理解为电话号码。这样子可以找到对方。' \
            '接收的文件将会被放到本程序的同一目录下。\n' \
            '\n更新日志：\n' \
            'V0.3增添了聊天框的复制、剪切、粘贴功能；追加了昵称显示和聊天文字显示格式；追加了多线程接受信息；完善了帮助。\n' \
            'V0.2修改了界面，增加了本地IP的显示,追加了聊天时间\n' \
            'V0.1完成了基本功能。\n'
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
        top.title('关于微聊')
        top.geometry('240x250+300+300')
        self.about_text = Tkinter.Text(top, cursor='hand2')
        self.about_text.pack(fill='both', expand=1)
        self.info_list = ['\n%s\n\n'%VERS,
                    '跨平台的P2P双工文件传输,聊天软件\n',
                    '作者: 张 阳\n',
                    'http://www.weibo.com/wb2young\n',
                    '(c) 2014\n', 
                    '< mark.zhangyoung@gmail.com >',
                    ]
        self.about_text.tag_config('name', justify='center', font=('Helvetica', 16, 'bold'))
        self.about_text.tag_config('info', justify='center', font=('Helvetica', 9))
        self.about_text.tag_config('url', justify='center', font=('Helvetica', 10),foreground='blue', underline=1)
        self.about_text.tag_bind('url', '<Button>', self.browser)
        
        self.about_text.insert('end', self.info_list[0], 'name')
        self.about_text.insert('end', self.info_list[1], 'info')
        self.about_text.insert('end', self.info_list[2], 'info')
        self.about_text.insert('end', self.info_list[3], 'url')
        self.about_text.insert('end', self.info_list[4], 'info')
        self.about_text.insert('end', self.info_list[5], 'info')
        self.about_text['state'] = 'disabled'

    def browser(self, event):
        webbrowser.open(self.info_list[3])

class MyText(Tkinter.Text):
    def my_insert(self, index, chars, *args):
        self.insert(index, chars, *args)
        self.yview('end')

class MyThread(threading.Thread):
    def __init__(self, func, argv, dae=True):
        threading.Thread.__init__(self)
        self.func = func
        self.argv = argv
        self.setDaemon(dae)
        self.start()

    def run(self):
        self.func(*self.argv)

class TranChat(socket.socket):
    def serverthread(self,bufsize,window):
        while True:
            dat = self.client_sock.recv(bufsize)
            dat = pickle.loads(dat)
            flag = self.recv_chat(dat,window)
            if not flag:
                self.client_sock.close()
                window.outtex.insert('end', '正在重新等待连接\n', 'warning')
                break
            else:
                continue

    def server(self, locaddr, window):
        global IP
        flag=1
        window.outtex.insert('end','正在等待连接，请稍后…\n','warning')
        while True:
            self.client_sock,remaddr=self.accept()
            IP = remaddr[0]
            window.outtex.insert('end', '已接受：%s的连接\n'%IP,'warning')
            thread_server=MyThread(self.serverthread,(1024,window))

    def client(self, remaddr, window):
        window.outtex.insert('end', '正在连接，请稍后..\n', 'warning')
        if connect_check(self, remaddr) == 0:
            window.outtex.insert('end', '连接超时！\n', 'warning')
            return
        window.outtex.insert('end', '已连接到：%s\n'%remaddr[0], 'warning')
        flag = 1
        while flag:
            dat = self.recv(1024)
            dat = pickle.loads(dat)
            flag = self.recv_chat(dat, window)
    #为client和server提供聊天信息接收功能
    def recv_chat(self,dat, window):
        if dat == 'SOCKET CLOSE':
            window.outtex.my_insert('end', '对方已断开连接！\n', 'warning')
            return 0
        dat = dat.decode('utf8')
        if not window.intex.focus_get():
            ring()
        window.outtex.my_insert('end', dat+'\n', 'remote')
        return 1

#文件接收
def file_in(window):
    window.outtex.my_insert('end', '准备接收...\n', 'warning')
    transpt_in_sock = link_process()
    if transpt_in_sock == 0:
        window.outtex.my_insert('end', '连接超时！\n', 'warning')
        return
    window.outtex.my_insert('end', '等待对方发送，请稍后..\n', 'warning')
    file_info = transpt_in_sock.recv(BUFSIZE)
    file_name, file_size = pickle.loads(file_info)
    file_name = file_name.decode('utf8')
    file_recv = open(file_name, 'wb')
    init_len = len('接收进度：%s/'%file_size)-9
    window.progress_entry.insert(0, '接收进度：%s/ '%file_size)
    current_size = 0
    window.outtex.my_insert('end', '开始接收...\n', 'warning')
    try:
        while 1:
            peer = transpt_in_sock.recv(BUFSIZE)
            file_recv.write(peer)
            current_size += len(peer)
            window.progress_entry.delete(init_len, 'end')
            window.progress_entry.insert(init_len, str(current_size))
            if file_size == current_size:
                transpt_in_sock.send('EOF')
                break
    finally:
        file_recv.close()
        transpt_in_sock.close()
    window.outtex.my_insert('end', '文件接收完毕！保存在当前目录下。\n', 'warning')

#文件发送
def file_out(window, file_dscrp, file_info):
    transpt_out_sock = link_process()
    if transpt_out_sock == 0:
        window.outtex.my_insert('end', '连接超时！\n', 'warning')
        return
    file_size = file_info[1]
    window.outtex.my_insert('end', '开始发送文件...\n', 'warning')
    info = pickle.dumps(file_info, 2)
    transpt_out_sock.sendall(info)
    init_len = len('发送进度：%s/'%file_size)-9
    window.progress_entry.insert(0, '发送进度：%s/ '%file_size)
    while 1:
        window.progress_entry.delete(init_len, 'end')
        window.progress_entry.insert(init_len, str(file_size))
        peer = file_dscrp.read(BUFSIZE)
        if not peer:
            break
        elif not file_size <= BUFSIZE:
            file_size -= BUFSIZE
        else:
            file_size -= len(peer)
        transpt_out_sock.send(peer)
    file_dscrp.close()
    while 1:
        flag = transpt_out_sock.recv(1024)
        if flag == 'EOF':
            break
    transpt_out_sock.close()
    window.outtex.my_insert('end', '文件发送完毕！\n', 'warning')

#获得工作IP
def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',ifname[:15]))[20:24])

def get_my_ip():
    '''
    只获得一次本机的IP
    '''
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

def connect_check(sock, addr):
    i = 0
    while True:
        if sock.connect_ex(addr) == 0:
            return sock
        elif i >= 14: #尝试15次
            return 0 #这里代表连接失败
        i += 1
        time.sleep(0.7)

def server_trans():
    temp_sock = socket.socket()
    temp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    temp_sock.bind((HOST, PORT+2))
    temp_sock.listen(5)
    remote_sock = temp_sock.accept()[0]
    temp_sock.close()
    return remote_sock

def client_trans():
    temp_sock = socket.socket()
    temp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    local_sock  = connect_check(temp_sock, (IP, PORT+2))
    return local_sock


'''
    def WinSetting(self,width,height):
        #get screen width and height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        #calculate position x,y
        x = (ws/2.0)-(width/2.0)
        y = (hs/2.0)-(height/2.0)
        self.withdraw()#隐藏一下窗口，避免窗口震颤被看到
        self .geometry('%dx%d+%d+%d'%(width,height,x,y))
        self.deiconify()#重新显示

'''

def main(sock):
    global IP
    global nick_name
    global link_process #这个代表server_trans 和client_trans 其中一个，文件传输要用到这个函数
    window = Window(sock)

    ws=window.winfo_screenwidth()
    hs=window.winfo_screenheight()
    x=(ws/2.0)-(window.width/2.0)
    y=(hs/2.0)-(window.height/2.0)
    window.withdraw()
    window.geometry('+%d+%d'%(x,y))
    window.deiconify()

    window.protocol('WM_DELETE_WINDOW', window.ask_exit)
    window.update()
    nick_name = tkSimpleDialog.askstring(title=VERS,prompt='请输入您的昵称(仅限英文)')
    window.myname_entry.insert(0,nick_name)
    while True:
        IP = tkSimpleDialog.askstring(title=VERS,prompt='通信的双方各选一个,但是不可以相同。\n[1]输入对方IP,点Yes发起连接\n[2]点Cancel选择等待连接\n')
        if IP:
            window.myinfo_entry.insert(0,'客户端 IP: ')
            link_process = client_trans#传递函数名，加上（）才起作用，用MyThread承担所有函数启动任务
            thread_chat = MyThread(sock.client, ((IP, PORT), window))
        else:
            window.myinfo_entry.insert(0,'服务端 IP: ')
            link_process = server_trans
            sock.bind((HOST,PORT))
            sock.listen(5)
            threadchat = MyThread(sock.server, ((HOST, PORT), window))
        window.mainloop()
        
        try:
            sock.client_sock.sendall(pickle.dumps('SOCKET CLOSE', 2))
        except IOError:
            pass

    sock.close()



if __name__ == '__main__':
    os.system('python  %s/CoverScript/Cover_Chat.py'%WORKPATH)
    sock = TranChat()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.client_sock = sock #只是为了传输文件的时候S/C端共用一个socket的命名
    try:
        main(sock)
    except KeyboardInterrupt:
        pass
