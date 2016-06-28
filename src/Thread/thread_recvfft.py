# -*- coding: utf-8 -*-
import threading
import wx
from src.Package.package import *

import time
import Queue
import struct
import sys
import math
from numpy import linspace
import usb
from src.Spectrum import Spectrum_1
from src.CommonUse.staticFileUpMode import staticFileUp
from src.CommonUse.press_hand import press_hand
from src.CommonUse.staticVar import staticVar


###########接受硬件上传FFT数据和异常频点并放入队列############ 
  

class ReceiveFFTThread(threading.Thread):
    def __init__(self,mainframe):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
      
        self.recvHardObj=mainframe.byte_to_package
        self.SweepRange=[]
        self.SweepRangeAb=[]
        self.SweepRangeBack=[]
        
        self.DrawIntv=20
        self.DrawBackIntv=2  ###背景功率谱间隔
        self.SweepTotalNum=0
        self.SweepCount=0
        self.SweepBackCount=0
        
         
        ###主窗口引用 从而间接引用子窗口#######
        self.mainframe=mainframe
        
        ###队列引用#####################
        self.queueFFTUpload=self.mainframe.queueFFTUpload
        self.queueAbUpload=self.mainframe.queueAbUpload
        
        self.queueFFTLocalSave=self.mainframe.queueFFTLocalSave
        self.queueAbLocalSave=self.mainframe.queueAbLocalSave
        
        
    def stop(self):
        self.event.clear()
        
    def Init(self):  ##初始化，只收一帧功率谱帧和异常频点
        while(1):
            self.event.wait()
            try:
                recvFFT=self.recvHardObj.ReceiveFFT()
                if(not recvFFT==0):
                    if(recvFFT.CurSectionInTotal==1):
                        FuncPara=recvFFT.CommonHeader.FunctionPara
                        self.SweepTotalNum=recvFFT.SweepSectionTotalNum
                        startSectionNo=recvFFT.CurSectionNo
                        if( isinstance(self.mainframe.SpecFrame,Spectrum_1.Spec )):
                            if(self.mainframe.FreqMax==5995):
                                self.SetTicksLable(FuncPara,startSectionNo)
    
                        if(FuncPara==0x56 or FuncPara==0x51):
                            self.SweepRange.append(recvFFT)
                            
                            recvAb=self.recvHardObj.ReceiveAb()
                            if(not recvAb==0):   
                                self.SweepRangeAb.append(recvAb)
                        else:
                            self.SweepRangeBack.append(recvFFT)
                        break
            except usb.core.USBError:
                print 'time out0'
                   
            
                

    def run(self):
        self.Init() 
        while(1):
            
            try:
                
                recvFFT=self.recvHardObj.ReceiveFFT()   ##收一个功率谱帧,一个异常频点
                if(not recvFFT==0):
                    # print '0000xxxxxxx0000000'
                    funcPara=recvFFT.CommonHeader.FunctionPara
                    self.SweepTotalNum=recvFFT.SweepSectionTotalNum

                    if(funcPara==0x51 or funcPara==0x56):
                        self.SweepRange.append(recvFFT)
                        
                        recvAb=self.recvHardObj.ReceiveAb()    
                        if(not recvAb==0):
                            self.SweepRangeAb.append(recvAb)
                        
                    else:
                        self.SweepRangeBack.append(recvFFT)

                    
                    if(recvFFT.CurSectionInTotal==self.SweepTotalNum):   ##如果当前总数到达总数.看列表里是不是总数
                        if(funcPara==0x51 or funcPara==0x56):
                            if(len(self.SweepRange)==self.SweepTotalNum):
                                ##仅仅是在点了上传或者下载后加入队列，不做其他操作########
                                self.FileToQueue()
                                if( isinstance(self.mainframe.SpecFrame,Spectrum_1.Spec )):
                                    self.DrawAndShowAb(funcPara)         
                            self.SweepRange=[]
                            self.SweepRangeAb=[]
                        
                        else:
                            
                            if(len(self.SweepRangeBack)==self.SweepTotalNum):
                                if( isinstance(self.mainframe.SpecFrame,Spectrum_1.Spec )):
                                    self.DrawBack(funcPara)
                            self.SweepRangeBack=[]                        
            except usb.core.USBError:
                print 'time out1'
            
            
                     
    def DrawAndShowAb(self,funcPara):
        self.SweepCount+=1
        if(self.SweepCount>=self.DrawIntv):
            self.SweepCount=0
            yData=self.ExtractPoint(self.SweepRange)
            self.DrawSpec(funcPara,yData)
            self.DrawWater(yData)
            for recvAb in self.SweepRangeAb:
                if(not recvAb.AbFreqNum==0):
                    self.ShowAb(recvAb)
                    if(press_hand.press_hand==1):
                        staticVar.outPoint.write(press_hand.press_set)
                        staticVar.outPoint.write(press_hand.press_freq)
        
        
    def DrawBack(self,funcPara):
        self.SweepBackCount+=1
        if(self.SweepBackCount>=self.DrawBackIntv):
            self.SweepBackCount=0
            
            yData=self.ExtractPoint(self.SweepRangeBack)
            self.DrawSpec(funcPara,yData)
            time.sleep(0.01)
    def FileToQueue(self):  
        if( isinstance(self.mainframe.SpecFrame,Spectrum_1.Spec )):
            if(self.queueFFTUpload.qsize()<=10):
                if(self.mainframe.SpecFrame.panelFigure.getstartUploadOnce() and (staticFileUp.getUploadMode()==0)):
                 
                    self.queueFFTUpload.put(self.SweepRange)
                    self.queueAbUpload.put(self.SweepRangeAb)
                    
                    self.mainframe.SpecFrame.panelFigure.restore2unstart()
                    
                elif(staticFileUp.getUploadMode()):
                    print 'auto_'
                    self.queueFFTUpload.put(self.SweepRange)
                    self.queueAbUpload.put(self.SweepRangeAb)
                
                else:
                    pass 

       
                    
            if(self.queueFFTLocalSave.qsize()<=10):
                if(self.mainframe.SpecFrame.panelFigure.getisDownLoad()):
                    self.queueFFTLocalSave.put(self.SweepRange)
                    self.queueAbLocalSave.put(self.SweepRangeAb)
                    
            if((not self.mainframe.thread_route_map==0) and self.mainframe.queueRouteMap.qsize()<=100):
                if(self.mainframe.thread_route_map.event.isSet()):
                    recvFFT=self.SweepRange[0]
                    
                    ###### 解析 经纬高 ##############
                    LonLatClass=recvFFT.LonLatAlti
                    fen=(LonLatClass.HighLonFraction >> 2) +float(((LonLatClass.HighLonFraction&0x03)<<8)+ LonLatClass.LowLonFraction)/1000
                    Lon=LonLatClass.LonInteger+float(fen)/60
            
                    fen = (LonLatClass.HighLatFraction >> 2) + float(((LonLatClass.HighLatFraction & 0x03)<<8) + LonLatClass.LowLatFraction) / 1000
                    Lat = LonLatClass.LatInteger + float(fen) / 60
               
                    self.mainframe.queueRouteMap.put([Lon,Lat])
                
                
                   
# 这里是用来自动判别的，每次关了软件再上传
    def SetTicksLable(self,FuncPara,startSectionNo):
        if(FuncPara==0x51 or FuncPara==0x52):
            endSectionNo=startSectionNo+self.SweepTotalNum-1
            begin=70+(startSectionNo-1)*25
            end=70+endSectionNo*25
            
        elif(FuncPara==0x56 or FuncPara==0x57):
            endSectionNo=startSectionNo+32*self.SweepTotalNum
            begin=70+(startSectionNo-1)*25
            end=70+(endSectionNo-1)*25

            print end

            
        ###设置线条的xdata################
        xx=linspace(begin , end,1024)
        self.mainframe.SpecFrame.panelFigure.lineSpec.set_xdata(xx)
        self.mainframe.SpecFrame.panelFigure.lineSpecBack.set_xdata(xx)            
        
        ##设置显示范围（包括文本框和Label）####################
        self.mainframe.FreqMin=begin
        self.mainframe.FreqMax=end 
        self.mainframe.SpecFrame.panelFigure.Min_X.SetLabel(str(begin))
        self.mainframe.SpecFrame.panelFigure.Max_X.SetLabel(str(end))

        self.mainframe.SpecFrame.panelFigure.setSpLabel(begin,end)

                
    def DrawSpec(self,funcPara,yData):
        try:
            self.mainframe.SpecFrame.panelFigure.PowerSpectrum(funcPara,yData)
        except wx.PyDeadObjectError:
            pass 
    

    def DrawWater(self,yData):
        try:
            if(not self.mainframe.WaterFrame==None):
                self.mainframe.WaterFrame.WaterFall(yData)
            
        except wx.PyDeadObjectError:
            self.mainframe.WaterFrame=None
            pass 

    
    def ParseFFTList(self,SweepRange):
        # parseResult=[]
        FFTList=[]
        for recvFFT in SweepRange:
            #print 'No',recvFFT.CurSectionNo
            # FFTList=[]
            AllFreq=recvFFT.AllFreq
            ii=0
            for FFTData in AllFreq:
                HighFreq1=FFTData.HighFreq1dB
                LowFreq1=FFTData.LowFreq1dB
                HighFreq2=FFTData.HighFreq2dB
                LowFreq2=FFTData.LowFreq2dB
                if(HighFreq1>=8):
                    FFTFreq1=-(2**12-(HighFreq1<<8)-LowFreq1)/8.0
                else:
                    FFTFreq1=((HighFreq1<<8)+LowFreq1)/8.0
                if(HighFreq2>=8):
                    FFTFreq2=-(2**12-(HighFreq2<<8)-LowFreq2)/8.0
                else:
                    FFTFreq2=((HighFreq2<<8)+LowFreq2)/8.0
                if(recvFFT.CommonHeader.FunctionPara==0x51):
                    pass
                    # print ii*2,FFTFreq1
                    # print ii*2+1,FFTFreq2

                ii=ii+1
                FFTList.append(FFTFreq1)
                FFTList.append(FFTFreq2)
            # parseResult.append(FFTList)
        return FFTList
                
    def ExtractPoint(self,SweepRange):
        allFreq=self.ParseFFTList(SweepRange)
        #if(SweepRange[0].CommonHeader.FunctionPara==0x57):
            #for i in allFreq[0]:
              #  print i
           # print0
           # print 
                    
                
        yData=[]
        ExtractM = len(allFreq)/1024
        Section=1024


        for i in xrange(Section):
            Sum=0
            for j in xrange(ExtractM):
                Sum+=math.pow(10,(allFreq[j+i*ExtractM])/10.0)
            Sum=(math.log10(Sum*(10**10))-10)*10
            yData.append(round(Sum,2))


        return yData[0:1024]

    def ShowAb(self,recvAbList):        
        AllAbFreq=recvAbList.AllAbFreq
        CurSectionNo=recvAbList.CurSectionNo
        funcPara=recvAbList.CommonHeader.FunctionPara
        i=0
        for AbFreq in AllAbFreq:
            HighFreqNo=AbFreq.HighFreqNo
            LowFreqNo=AbFreq.LowFreqNo
            HighdB=AbFreq.HighdB
            LowdB=AbFreq.LowdB
    
            FreqNo=(HighFreqNo<<8)+LowFreqNo
            if(funcPara==0x53):
                Freq=70+(CurSectionNo-1)*25+ float(FreqNo*25)/1024
            else:
                Freq=70+(CurSectionNo-1)*25+ float(FreqNo*800)/1024    
            
            if(HighdB>=8):
                dB=-(2**12-(HighdB<<8)-LowdB)/8.0
            else:
                dB=((HighdB<<8)+LowdB)/8.0

            if(dB<0):
                self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,1,str('%0.2f'%Freq))
                self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,2,str(dB))
                i=i+1

