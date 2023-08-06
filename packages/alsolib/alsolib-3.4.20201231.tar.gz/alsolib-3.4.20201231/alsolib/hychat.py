import tkinter
import tkinter.font as tkFont
import pygame
import socket,select,threading;
from urllib.request import *
try:
    import huoyanlib, alsolib
except:
    print("请先安装huoyanlib xingyunlib库以体验更好功能！")
def playsound(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
class ClientUI():


    def __init__(self):
        self.zhanghao = input("请输入您的hychat码:")
        self.password = input("请输入hyChat码 "+self.zhanghao+" 的密码:")
        try:
            urlretrieve("http://user.hychat.asunc.cn/" + self.zhanghao + '-' + self.password + '.txt', 'i.txt')
            f = open('i.txt', 'r')
            self.text = f.read()
            self.text = self.text.split('-', 3)
            self.name=self.text[1]
            print('欢迎你,亲爱的用户', self.text[1])
        except:
            print("密码或账号错误")
            exit()
        self.root=tkinter.Tk()
        self.root.title("Web hyChat聊天室(用户昵称:"+self.text[1]+")")
        self.root.iconbitmap('hychaticon.ico')
        #窗口面板，用四个面板布局
        self.frame=[tkinter.Frame(),tkinter.Frame(),tkinter.Frame(),tkinter.Frame()]

        #以下为界面设计与服务器端相同
        # 显示消息Text右边的滚动条
        self.chatTextScrollBar = tkinter.Scrollbar(self.frame[0])
        self.chatTextScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # 显示消息Text，并绑定上面的滚动条
        ft = tkFont.Font(family='Fixdsys', size=11)
        self.chatText = tkinter.Listbox(self.frame[0], width=100, height=20, font=ft)
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set
        self.chatText.pack(expand=1, fill=tkinter.BOTH)
        self.chatTextScrollBar['command'] = self.chatText.yview()
        self.frame[0].pack(expand=1, fill=tkinter.BOTH)
        # 标签，分开消息显示Text和消息输入Text
        label = tkinter.Label(self.frame[1], height=2)
        label.pack(fill=tkinter.BOTH)
        self.frame[1].pack(expand=1, fill=tkinter.BOTH)
        # 输入消息Text的滚动条
        self.inputTextScrollBar = tkinter.Scrollbar(self.frame[2])
        self.inputTextScrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # 输入消息Text，并于滚动条绑定
        ft = tkFont.Font(family='Fixdsys', size=11)
        self.inputText = tkinter.Text(self.frame[2], width=70, height=8, font=ft)
        self.inputText['yscrollcommand'] = self.inputTextScrollBar.set
        self.inputText.pack(expand=1, fill=tkinter.BOTH)
        self.inputTextScrollBar['command'] = self.chatText.yview()
        self.frame[2].pack(expand=1, fill=tkinter.BOTH)
        # 发送消息按钮
        self.sendButton = tkinter.Button(self.frame[3], text="发送", width=10, command=self.sendMessage)
        self.sendButton.pack(expand=1, side=tkinter.BOTTOM and tkinter.RIGHT, padx=15, pady=8)
        # 关闭按钮
        self.closeButton = tkinter.Button(self.frame[3], text='官网', width=10, command=self.close)
        self.closeButton.pack(expand=1, side=tkinter.RIGHT, padx=15, pady=8)
        self.frame[3].pack(expand=1, fill=tkinter.BOTH)
    #接收消息
    def receiveMessage(self):
        try:
            #建立socket连接
            self.clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientSock.connect(('connect.hychat.asunc.cn',52360))
            self.flag=True
            self.clientSock.send(self.zhanghao.encode("gbk"))
        except:
            self.flag=False
            self.chatText.insert(tkinter.END,'你还没有与服务器建立连接，请检查服务器端是否开启')
            return
        self.buffer=1024

        while True:
            try:
                if self.flag==True:# 建立连接，接收服务器端消息
                    my = [self.clientSock]
                    while True:
                        r, w, e = select.select(my, [], [])

                        if self.clientSock in r:
                            try:
                                try:
                                    a = self.clientSock.recv(1024)
                                    a = a.decode("gbk")
                                    chatstr = ""
                                    if a != "烫" and a != "烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫烫":
                                        for i in range(len(a)):
                                            if a[i] != "烫":
                                                chatstr+=a[i]
                                        chatstr+="\n"
                                        self.chatText.insert(tkinter.END, chatstr)
                                        self.chatText.insert(tkinter.END, " ")
                                except:
                                    pass

                            except socket.error:
                                print('socket is error')
                                exit()


                else:
                    break
            except EOFError as msg:
                raise msg
                self.clientSock.close()
                break

    def sendMessage(self):
        #  得到用户在Text中输入的消息
        message=self.inputText.get('1.0',tkinter.END)
        info = '<web端>' + '<聊天号:' + self.zhanghao + ' 昵称:' + self.name + '>\n   ' + message + '\0'
        self.chatText.insert(tkinter.END, info)
        #格式化当前的时间
        if self.flag==True:
            self.clientSock.send(info.encode('gbk'))
            self.inputText.delete(0.0, message.__len__() - 1.0)
            import time
            time.sleep(0.5)
        else:
            #socket连接没有建立，提示用户
            self.chatText.insert(tkinter.END,'你还未与服务器端建立连接，服务器端无法收到你发送的消息\n')
            #清空用户在Text中输入的消息
            self.inputText.delete(0.0,message.__len__()-1.0)

    def close(self):
        import webbrowser
        webbrowser.open("http://hychat.asunc.cn/")

    #启动线程接收服务器端的消息
    def startNewThread(self):
        #   启动一个新线程来接收服务器的消息
        #args是传递给线程函数的参数，receiveMessage函数不需要参数，就传一个空元组
        thread=threading.Thread(target=self.receiveMessage,args=())
        thread.setDaemon(True)
        thread.start()
def main():
    client=ClientUI()
    client.startNewThread()
    client.root.mainloop()
if __name__=='__main__':
    main()
