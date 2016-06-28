# -*- coding: utf-8 -*-
import threading 
import time 
import wx 
from src.Package.package import *
from src.Spectrum import Spectrum_1
import struct 
from src.CommonUse.staticVar import staticVar
from src.CommonUse.staticFileUpMode import staticFileUp
import socket 


class SendFileThread(threading.Thread): 
    def __init__(self,SpecFrame,
                 queueFFTUpload,queueAbUpload):
        threading.Thread.__init__(self)
        self.event = threading.Event()  
        self.event.set()
        
        self.queueFFTUpload=queueFFTUpload
        self.queueAbUpload=queueAbUpload

        self.SpecFrame=SpecFrame
        
        self.sockFile=staticVar.getSockFile()
        
        self.SpecList=[]

        
        self.Second=0
        self.countFFT=0

        self.count=1  ##用来计数一秒钟发了多少个功率谱文件
        
        self.fileUploadMode=2
        self.extractM=1
        self.changeThres=10
        
        
        self.startTrans=0
    def stop(self):
        self.event.clear()
    def run(self):
        while(1):
            self.event.wait()
            
            self.SendSpec()
 

            
                
            time.sleep(0.5)
            
        
    def SendSpec(self):
        ### 每次都要获取 ，会变的 ####

        ### 在队列加到一定的时候,如果改变了传输方式要马上改过来
        flag_for_extract=0
        flag_for_auto=0
        self.fileUploadMode=staticFileUp.getUploadMode()
        
        if(self.fileUploadMode):    
            self.extractM=staticFileUp.getExtractM()
            self.changeThres=staticFileUp.getChangeThres()
            
        
        while((not self.queueAbUpload.empty()) and (not self.queueFFTUpload.empty())):
            if(self.fileUploadMode==0):
                ListSpec=self.queueFFTUpload.get()
                ListAb=self.queueAbUpload.get()
                self.FFTParse(ListSpec, ListAb)
                
            elif(self.fileUploadMode==2): ##抽取自动
                count=0
                while((not self.queueAbUpload.empty()) and (not self.queueFFTUpload.empty())):
                    if(staticFileUp.getUploadMode()==2):
                        ListSpec=self.queueFFTUpload.get()
                        ListAb=self.queueAbUpload.get()
                    else:
                        flag_for_extract=1
                        break 
                    count+=1
                    if(count==self.extractM):
                        print 'start to transfer----------------'
                        count=0
                        self.FFTParse(ListSpec,ListAb)
                if(flag_for_extract):
                    break
                        
            elif(self.fileUploadMode==1):  ##功率谱是否变化
                while((not self.queueAbUpload.empty()) and (not self.queueFFTUpload.empty())):
                    if(staticFileUp.getUploadMode()==1):
                        ListSpec=self.queueFFTUpload.get()
                        ListAb=self.queueAbUpload.get()
                    else:
                        flag_for_auto=1
                        break
                    flag=0
                    for recvFFT in ListSpec:
                        changeFlag=recvFFT.SpecChangeFlag
                        if(changeFlag==14 or changeFlag==15):
                            flag=1
                            break
                    if(flag==1):
                        print 'start to auto >>>>>>>>>>>>>>>  '
                        self.FFTParse(ListSpec,ListAb)
                
                if(flag_for_auto):
                    break
#         wx.MessageBox(u'传功率谱文件完毕', 
#                        'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
#                        
            
    
    def FFTParse(self,ListSpec,ListAb):    
        for i in range(len(ListSpec)):   
            recvFFT=ListSpec[i]
            recvAbList=ListAb[i]
           
            TotalNum=recvFFT.SweepSectionTotalNum         
            blockFFT=FFTBlock(recvFFT.CurSectionNo,recvFFT.AllFreq)
            blockAb=AbListBlock(recvAbList.CurSectionNo,recvAbList.AbFreqNum,recvAbList.AllAbFreq)
            self.SpecList.append(blockFFT)
            self.SpecList.append(blockAb)
        
        head=SpecUploadHeader(0x00,recvFFT.LonLatAlti,recvFFT.SweepRecvMode, \
        recvFFT.FileUploadMode,self.changeThres,self.extractM,TotalNum)
            

        ###组合功率谱文件####
        '''
        Time=recvFFT.Time_
        CommonHeader=recvFFT.CommonHeader
        ID=(CommonHeader.HighDeviceID<<8)+CommonHeader.LowDeviceID
        Year=(Time.HighYear<<4)+Time.LowYear
        Month=Time.Month
        Day=Time.Day
        Hour=(Time.HighHour<<2)+Time.LowHour
        Minute=Time.Minute
        Second=Time.Second
        '''

        curTime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        Year=int(curTime[0:4])
        Month=int(curTime[4:6])
        Day=int(curTime[6:8])
        Hour=int(curTime[8:10])
        Minute=int(curTime[10:12])
        Second=int(curTime[12:14])
        
        
        
        ID=staticVar.getid()
        
        if(self.startTrans==0):
            self.Second=Second 
            self.startTrans=1  
        if((self.startTrans==1) and (self.Second!=Second)):
            self.count=1
            self.Second=Second
        fileName=str(Year)+"-"+str(Month)+"-"+str(Day)+  \
                 "-"+str(Hour)+"-"+str(Minute)+"-"+str(Second)+"-"+str(self.count)+'-'+str(ID)
                 
        if(recvFFT.CommonHeader.FunctionPara==0x51):
            fileName+='-fine.pwr'
        else:
            fileName+='-coarse.pwr'
            
        

        fileNameLen=len(fileName)
        fileContentLen=sizeof(head)+(sizeof(blockFFT)+sizeof(blockAb))*TotalNum+2

        print fileName
        print fileNameLen
        print fileContentLen
        
        ############SendToServer###################
        if(self.sockFile):
            try:
                str1=struct.pack("!2BHQ",0x00,0xFF,fileNameLen,fileContentLen)
                self.sockFile.send(str1+fileName)
        
                self.sockFile.send(bytearray(head))
                for i in xrange(len(self.SpecList)/2):
                    self.sockFile.send(bytearray(self.SpecList[2*i]))
                self.sockFile.send(struct.pack("!B",0xFF))
                for i in xrange(len(self.SpecList)/2):
                    self.sockFile.send(bytearray(self.SpecList[2*i+1])) 
                self.sockFile.send(struct.pack("!B",0x00))
            except socket.error,e:
                print 'socket_error',e 
                staticVar.sockFile=0
                self.sockFile=0
                
                

        #########################################
        self.SpecList=[]
        
        self.count+=1
        self.countFFT+=1
        print 'self.countFFT',self.countFFT
            

            
        
        
                
        
        
        




            



            
