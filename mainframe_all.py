# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui 
import matplotlib
import Queue
import os
import time
import sys
import struct
import threading
from src.PressDialog.press import dialog_press
from src.PressDialog.pressmode import dialog_pressmode
from src.SweepDialog.sweep import dialog_sweep
from src.IQDialog.IQ import dialog_IQ
from src.MapDialog.map import dialog_map

from src.RomteControlDialog.remote_control import dialog_remoteCtrl
from src.HistoryDisplayDialog.history_display import dialog_historydis
from src.FreqPlanDialog.freqplan import QueryFreqPlanDialog
from src.Spectrum import Spectrum_1
from src.CommonUse.staticVar import staticVar
from src.CommonUse.show_recv_and_set import ShowRecvAndSet
from src.CommonUse.byte_2_package import ByteToPackage
from src.CommonUse.connect import ServerCommunication
from src.CommonUse import configfpga
from src.CommonUse.timer import Timer

from src.DataBase import CreateAllTable

from src.Package.package import TransferSet,FrameHeader,FrameTail,ConnectServer,LonLatAltitude, Query

from threading import Thread
from src.Thread.thread_upload import SendFileThread
from src.Thread.thread_station import ReceiveServerData
from src.Thread.thread_recvfft import ReceiveFFTThread

###########################################################################
## Class MyFrame1
###########################################################################

class MainFrame ( wx.aui.AuiMDIParentFrame ):
    
    def __init__( self, parent ):
        wx.aui.AuiMDIParentFrame.__init__ ( self, parent, -1, title = wx.EmptyString,  \
        pos = wx.DefaultPosition, size = wx.Size( 887,545 ), \
        style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        
        #######################################
        matplotlib.rcParams["figure.facecolor"] = '#F2F5FA'
        matplotlib.rcParams["axes.facecolor"] = '0'
        matplotlib.rcParams["ytick.color"] = '0'
        matplotlib.rcParams["xtick.color"] = '0'
        matplotlib.rcParams["grid.color"] = 'w'
        matplotlib.rcParams["text.color"] = 'w'
        matplotlib.rcParams["figure.edgecolor"]="0"
        matplotlib.rcParams["xtick.labelsize"]=12
        matplotlib.rcParams["ytick.labelsize"]=12
        matplotlib.rcParams["axes.labelsize"]=14
        matplotlib.rcParams["grid.linestyle"]="-"
        matplotlib.rcParams["grid.linewidth"]=0.5
        matplotlib.rcParams["grid.color"]='#707070'
        
        #######################################
        # os.chdir("./apache-tomcat-7.0.68//bin//")
#         os.chdir("../apache-tomcat-7.0.68//bin//")
        
        os.system("startup.bat")
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        os.chdir(dirname)
        ########### 初始化变量  #################
        self.start_local_iq=0

        ########### 心跳相关 ##########
        self.timer=0
        self.count_heart = 0
        


        self.frame_count=0    #打开的窗口数量#
        
        self.FreqMin=70
        self.FreqMax=5995
        
        self.tail=FrameTail(0,0,0xAA)
        #### 窗口################
        self.SpecFrame=Spectrum_1.Spec(self)
        self.SpecFrame.Activate()
      
        self.WaterFrame=None
        self.WaveFrame=None
        
        self.MapFrame=None 
        
        #################################

        staticVar.setid(11) #初始化id
        
        print staticVar.getid()
      
#         staticVar.initPort()  #初始化硬件 端口
        self.serverCom=ServerCommunication() #实例化服务器连接对象
        
        ########## 用于显示的  ############
        
        self.show_recv_set=ShowRecvAndSet(self)
        self.byte_to_package=ByteToPackage()

        self.GPS_list=[]  ##记录GPS 查询信息，发送给服务器
        ####上传的队列############
        self.queueFFTUpload=Queue.Queue()
        self.queueAbUpload=Queue.Queue()

        
        ###本地存储的队列#############
        self.queueFFTLocalSave=Queue.Queue()
        self.queueAbLocalSave=Queue.Queue()

        ### 画地图所使用的队列 （FFT的经纬度打包放进去）#########
        
        self.queueRouteMap=Queue.Queue()
        
        
        
        
        ###### 创建数据表 #############
        if(not os.path.isfile( "C:\\DataBase\\PortSRF.db" )):
            os.mkdir(r'C:/DataBase/')
        CreateAllTable.create_all_table()
        
        
        ##### thread 管理 #########
        self.thread_recvfft=0
        self.thread_upload=0
        self.thread_station=0
        self.thread_route_map=0
        ''' 

        if (configfpga.get_fx3_status()[0] == 0x04):
            pass
        else:
            configfpga.load_fpga('c:/top_sao.bit')

            wx.MessageBox('Config  OK!',
                          'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
                          '''

        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL|wx.TB_TEXT, wx.ID_ANY ) 
        self.m_start_hw = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"硬件上传", wx.Bitmap( ".//icons//green_2.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        self.m_toolBar1.AddSeparator()
        
        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()
        
        self.m_connect = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"服务器连接", wx.Bitmap( ".//icons//link_start.jpg", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.AddSeparator()
        
        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()
        
        self.m_tool_sweep = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"扫频接收 ", wx.Bitmap( ".//icons//open_1.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.AddSeparator()
        
        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()
        
        self.m_tool_iq = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"定频接收  ", wx.Bitmap( ".//icons//link_a.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.AddSeparator()
        
        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()
        
        self.m_tool_press = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"压制发射", wx.Bitmap( ".//icons//red_1.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.AddSeparator()
        
        self.m_toolBar1.AddSeparator()
        
        self.m_tool_map = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"地图服务", wx.Bitmap( ".//icons//Play_1.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.AddSeparator()
        
        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()
        
        self.m_tool_freqplan = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"频率规划", wx.Bitmap( ".//icons//Pause_1.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.AddSeparator()
        
        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()
        
        self.m_tool_remoteCtrl = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"远程控制", wx.Bitmap( ".//icons//laba_1.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.AddSeparator()
        
        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()
        
        self.m_tool_replay = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"历史回放", wx.Bitmap( ".//icons//local_read_a.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
        
        self.m_toolBar1.Realize() 
        
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.Bind(wx.EVT_CLOSE,self.OnDoClose)
        self.Bind( wx.EVT_TOOL, self.m_start_hwOnToolClicked, id = self.m_start_hw.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_connectOnToolClicked, id = self.m_connect.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_sweepOnToolClicked, id = self.m_tool_sweep.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_iqOnToolClicked, id = self.m_tool_iq.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_pressOnToolClicked, id = self.m_tool_press.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_mapOnToolClicked, id = self.m_tool_map.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_freqplanOnToolClicked, id = self.m_tool_freqplan.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_remoteCtrlOnToolClicked, id = self.m_tool_remoteCtrl.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_replayOnToolClicked, id = self.m_tool_replay.GetId() )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class

    def hello(self):

        print '----------------------------------------------------------------------'
        staticVar.getSock().sendall(struct.pack("!B", 0x55))
        staticVar.getSock().sendall(struct.pack("!B", 0x66))
        if(self.count_heart<=staticVar.count_heat_beat):
            self.count_heart=staticVar.count_heat_beat
        else:
            print 're--------connect---------------'
            staticVar.sock=0
            staticVar.sockFile=0
            
            self.thread_station.input1=[]
            
            while (1):
                try:
                    self.serverCom.ConnectToServer(9000)
                    staticVar.sock = self.serverCom.sock
                    self.thread_station.input1.append(staticVar.sock)
                except Exception:
                    wx.MessageBox('Connect To Monitor Server Failure!',
                                  'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)


                try:
                    self.serverCom.ConnectToServer(9988)
                    staticVar.sockFile = self.serverCom.sockFile
                    self.thread_station.input1.append(staticVar.sockFile)
                    break
                except Exception:
                    wx.MessageBox('Connect To File Server Failure!',
                                  'Alert', wx.ICON_INFORMATION | wx.STAY_ON_TOP)
                time.sleep(5)
                
                

        self.timer = threading.Timer(15, self.hello, [])
        self.timer.start()


    def ConnectCore(self):
        flag_sock=0
        flag_sockFile=0

        while(1):
            if(staticVar.sock==0 and flag_sock==0):
                try:
                    self.serverCom.ConnectToServer(9000)
                    staticVar.sock=self.serverCom.sock
                    flag_sock=1
                except Exception:
                    (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
                    wx.MessageBox('Connect To Monitor Server Failure!\n'+
                                   str(ErrorValue[0])+' '+str(ErrorValue[1]), 
                               'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
                    
                    
             
    
                    
            if(staticVar.sockFile==0 and flag_sockFile==0):
                try:
                    self.serverCom.ConnectToServer(9988)
                    staticVar.sockFile=self.serverCom.sockFile
                    flag_sockFile=1
                except Exception:
                    (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
                    wx.MessageBox('Connect To File Server Failure!\n'+
                                  str(ErrorValue[0])+' '+str(ErrorValue[1]),  
                               'Alert', wx.ICON_INFORMATION | wx.STAY_ON_TOP)

            if(flag_sock and flag_sockFile):
                break
            time.sleep(5)
             
        
        
        
        connect=ConnectServer()
        
        connect.CommonHeader=FrameHeader(0x55,0xA1,staticVar.getid()&0x00FF,staticVar.getid()>>8)
        connect.CommonTail=self.tail
        
        if(self.GPS_list==[]):
            #临时加的测试 
            self.GPS_list=[0]*9
            #############################
            
            Lon=114.4202
            Lat=30.5100
            Alti=35
            Lon_fen=0.4202*60
            Lat_fen=0.51*60
            Lon_fen_I=int(Lon_fen)
            Lon_fen_f=int((Lon_fen-int(Lon_fen))*1000)
            Lat_fen_I=int(Lat_fen)
            Lat_fen_f=int((Lat_fen-int(Lat_fen))*1000)
            
        
            self.GPS_list[1]=114
            self.GPS_list[2]=(Lon_fen_I<<2)+(Lon_fen_f>>8)
            self.GPS_list[3]=Lon_fen_f&0x00FF
            self.GPS_list[4]=30
            self.GPS_list[5]=(Lat_fen_I<<2)+(Lat_fen_f>>8)
            self.GPS_list[6]=Lat_fen_f&0x00FF
            self.GPS_list[8]=35
            
        list =self.GPS_list
        
        connect.LonLatAlti=LonLatAltitude(list[0],list[1],list[2],list[3],list[4]>>7,list[4]&0x7F,
                                          list[5],list[6],list[7]>>7,list[7]&0x7F,list[8])
        self.serverCom.SendQueryData(connect)
        
      
        self.thread_station=ReceiveServerData(self)
        self.thread_station.setDaemon(True)
        self.thread_station.start()
        

        self.thread_upload = SendFileThread(self.SpecFrame, self.queueFFTUpload,
                              self.queueAbUpload)
        self.thread_upload.setDaemon(True)
        self.thread_upload.start()

        self.timer = threading.Timer(15, self.hello, [])
        self.timer.start()
       
        '''
        thread_timer=Timer(self.thread_upload,self.thread_station)
        thread_timer.setDaemon(True)
        thread_timer.start()   
        '''

        self.m_connect.Enable(False)


    def QuerySend(self,funcPara):
        query=Query()
        query.CommonHeader=FrameHeader(0x55,funcPara,staticVar.getid()&0x00FF,staticVar.getid()>>8)
        query.CommonTail=self.tail
        staticVar.outPoint.write(bytearray(query))


    def m_start_hwOnToolClicked( self, event ):

        self.QuerySend(0x0A)
        ''' send query '''
        self.QuerySend(0x1C)
        self.GPS_list = self.byte_to_package.ReceiveRecv()

        obj = self.byte_to_package.ByteToWorkMode(self.GPS_list)
        self.show_recv_set.ShowIsConnect(obj)


        self.thread_recvfft=ReceiveFFTThread(self) 
        self.thread_recvfft.setDaemon(True)
        self.thread_recvfft.start()        
    
    def m_connectOnToolClicked( self, event ):
        Thread(target=self.ConnectCore,args=()).start()
        event.Skip()
        
        
    
    def m_tool_sweepOnToolClicked( self, event ):
        dlg=dialog_sweep(self)
        dlg.ShowModal()
        event.Skip()
    
    def m_tool_iqOnToolClicked( self, event ):
        dlg=dialog_IQ(self)
        dlg.ShowModal()
        event.Skip()
    
    def m_tool_pressOnToolClicked( self, event ):
        dlg=dialog_press(self)
        dlg.ShowModal()
        
        event.Skip()
    
    def m_tool_mapOnToolClicked( self, event ):
        dlg=dialog_map(self)
        dlg.ShowModal()
        event.Skip()
    
    def m_tool_freqplanOnToolClicked( self, event ):
        dlg=QueryFreqPlanDialog()
        dlg.ShowModal()
        event.Skip()
    
    def m_tool_remoteCtrlOnToolClicked( self, event ):
        dlg=dialog_remoteCtrl(self)
        dlg.ShowModal()
        event.Skip()
    
    def m_tool_replayOnToolClicked( self, event ):
        dlg=dialog_historydis(self)
        dlg.ShowModal()
        event.Skip()
    
#     def OnNewChild(self, evt):
#         self.count += 1
#         child = ChildFrame(self, self.count)
#         child.Activate()
# 
    def OnDoClose(self, evt):
        # Close all ChildFrames first else Python crashes
        print 'Close all window '
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        os.chdir(dirname)
        # os.chdir("./apache-tomcat-7.0.68//bin//")
#         os.chdir("../apache-tomcat-7.0.68//bin//")
        
        os.system("shutdown.bat")
        if(not self.thread_route_map==0):
            if(self.thread_route_map.event.isSet()):
                self.thread_route_map.stop()
                
        if(not self.thread_route_map==0):
            self.thread_route_map.conn.close()
        
        '''
        flag1=0
        flag2=0
        flag3=0

        while(1):
            if(not self.thread_recvfft==0):
                self.thread_recvfft.stop()
            else:
                flag1=1
            if(not self.thread_upload==0):
                self.thread_upload.stop()
            else:
                flag2=1
            if(not self.thread_station==0):
                self.thread_station.stop()
            else:
                flag3=1

            time.sleep(0.5)
            if(not flag1):
                if(not self.thread_recvfft.isAlive()):
                    flag1=1
            if(not flag2):
                if(not self.thread_upload.isAlive()):
                    flag2=1
            if(not flag3):
                if(not self.thread_station.isAlive()):
                    flag3=1
            if(flag1 and flag2 and flag3):
                break
                '''


        for m in self.GetChildren():
            if isinstance(m, wx.aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    k.Close()
        
        sys.exit(0)
        


app=wx.App()
app.locale=wx.Locale(wx.LANGUAGE_ENGLISH)
MainFrame(None).Show()
app.MainLoop()

