# -*- coding: utf-8 -*-
import socket 
class ServerCommunication():
    def __init__(self):
        self.sock=0
        self.sockFile=0
    def ConnectToServer(self,port):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('27.17.8.142',port))
        #sock.connect(('115.156.209.42',9123))
        
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,4096)
        
        if(port==9000):    #####监控服务器#############
            self.sock=sock 
        elif(port==9988):  ######文件服务器############
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1048576)
            self.sockFile=sock 
        else:
            pass 

    def SendQueryData(self,structrueObj):
        if(not self.sock==0):
            self.sock.send(bytearray(structrueObj))

    def DisconnectToServer(self):
        self.sock.close()
    def RecvConnectFlag(self):
        data =self.sock.recv(1024)
        return data
