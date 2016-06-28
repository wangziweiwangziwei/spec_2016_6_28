
# -*- coding: utf-8 -*-
import threading
import wx
from src.Package.package import *
import struct
import time
import Queue
import usb 
import os
from src.Wave.IQWave import WaveIQ
from src.CommonUse.staticVar import staticVar

class ReceiveIQThread(threading.Thread):
    def __init__(self,mainframe):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        
        ###########################
        self.byte_to_package=mainframe.byte_to_package
        self.mainframe=mainframe
       
        
        self.SweepRangeIQ=[]
        
        ##########################
        if(not os.path.exists("./LocalData//IQ//")):
            os.makedirs('./LocalData//IQ//')
            
    
    def run(self):
        while(1):
            try:
                recvIQ=self.byte_to_package.ReceiveIQ()
                if(not recvIQ==0):
                    self.SweepRangeIQ.append(recvIQ)
                    while(len(self.SweepRangeIQ)<self.SweepRangeIQ[0].Param.UploadNum):
                        recvIQ=self.byte_to_package.ReceiveIQ()
                        if(not recvIQ==0):
                            self.SweepRangeIQ.append(recvIQ)
                    break
            except usb.core.USBError,e:
                print e
        
        if(self.mainframe.WaveFrame==None):   #有IQ数据来时自动弹出WaveFrame
            self.mainframe.WaveFrame=WaveIQ(self.mainframe,u"定频波形图                ")  
            self.mainframe.WaveFrame.Activate()



        self.SendAndSaveIQ()


        ### 循环画五次 ####
        for i in range(5):
            for recvIQ in self.SweepRangeIQ:
                if(isinstance(self.mainframe.WaveFrame,WaveIQ)):
                    self.DrawIQ(recvIQ)

        self.mainframe.WaveFrame.Destroy()
        self.mainframe.WaveFrame=None
        del self.SweepRangeIQ

                 
                  
                    
                                        
    def DrawIQ(self,recvIQ):
        try:
            #chData=[]
            IDataSet=[]
            DataRate=recvIQ.Param.DataRate
            
            if(DataRate==0x01):self.Fs=5e6
            elif(DataRate==0x02): self.Fs=2.5e6
            elif(DataRate==0x03):self.Fs=1e6
            elif(DataRate==0x04):self.Fs=0.5e6
            elif(DataRate==0x05): self.Fs=0.1e6
            else:
                pass
            print "IQ Wave BandWidth -->",self.Fs
            DataArray=[]
            DataArray=recvIQ.IQDataAmp
            print len(DataArray),'len(DataArray)'
            for i in range(len(DataArray)):
                HighIPath=DataArray[i].HighIPath
                HighQPath=DataArray[i].HighQPath
                LowIPath=DataArray[i].LowIPath
                LowQPath=DataArray[i].LowQPath
                if(HighIPath>=8):
                    IData=-(2**12-(HighIPath<<8)-LowIPath)
                else:
                    IData=((HighIPath<<8)+LowIPath)
                if(HighQPath>=8):
                    QData=-(2**12-(HighQPath<<8)-LowQPath)
                else:
                    QData=((HighQPath<<8)+LowQPath)

                #chData.append(complex(IData,QData))
                IDataSet.append(IData)
            self.mainframe.WaveFrame.Wave(self.Fs,IDataSet)
        except:
            self.mainframe.WaveFrame=None
            pass

    def SendAndSaveIQ(self):
        self.IQList=[]
        recvIQList = self.SweepRangeIQ
        for recvIQ in recvIQList:
            block = IQBlock(recvIQ.CurBlockNo, recvIQ.IQDataAmp)
            self.IQList.append(block)

        head = IQUploadHeader(0x00, recvIQ.LonLatAlti, recvIQ.Param)

        #####组合IQ文件################
        curTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        Year = int(curTime[0:4])
        Month = int(curTime[4:6])
        Day = int(curTime[6:8])
        Hour = int(curTime[8:10])
        Minute = int(curTime[10:12])
        Second = int(curTime[12:14])
        ID = staticVar.getid()

        fileName = str(Year) + "-" + str(Month) + "-" + str(Day) + \
                   "-" + str(Hour) + "-" + str(Minute) + "-" + str(Second) + '-' + str(ID) + '.iq'

        fileNameLen = len(fileName)
        fileContentLen = sizeof(head) + sizeof(block) * len(self.IQList) + 1

        print fileName
        print fileNameLen
        print fileContentLen

        ###########SendToServer###################(H :2字节  Q:8 字节)
        if (not staticVar.getSockFile()==0):
            if(not self.mainframe.start_local_iq):   ##如果没有启动本地定频才是中心站发起的
                sockFile=staticVar.getSockFile()
                str1 = struct.pack("!2BHQ", 0x00, 0xFF, fileNameLen, fileContentLen)
                sockFile.send(str1 + fileName)
        
                sockFile.send(bytearray(head))
                for block in self.IQList:
                    sockFile.send(bytearray(block))
                sockFile.send(struct.pack("!B", 0x00))
            else:
                self.mainframe.start_local_iq=0


        ###########SaveToLocal####################
        fid=open(".\LocalData\\IQ\\"+ fileName,'wb+')
        # fid = open(self.dir_iq + fileName, 'wb+')
        fid.write(bytearray(head))
        for block in self.IQList:
            fid.write(bytearray(block))
        fid.write(struct.pack("!B", 0x00))
        fid.close()
        #########################################
        del self.IQList





