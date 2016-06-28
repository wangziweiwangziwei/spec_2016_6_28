# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

###########################################################################
## Class MyDialog2
###########################################################################

from src.SweepDialog.sweepfreq import dialog_freqblock
import wx
import wx.xrc
import time 
from numpy import linspace
from src.Package.package import *
from src.CommonUse.staticVar import staticVar
from src.Spectrum import Spectrum_1
from src.Water.WaterFall import Water

from src.CommonUse.staticFileUpMode import staticFileUp


class dialog_sweep ( wx.Dialog ):

    def __init__( self,parent):
        ####   一些参数值    ######################
        
        self.freq_s=70
        self.freq_e=5995
        self.upload_mode=0
        self.extract_m=1
        self.changethres=10
        self.id=staticVar.getid()
        self.lowid=self.id&0x00FF
        self.highid=self.id>>8
        self.tail=FrameTail(0,0,0xAA)
        self.outPoint=staticVar.outPoint
        
       
        self.parent=parent
        
        print self.id 
        
        
        #### show #########
        self.show_recv_set=self.parent.show_recv_set
        self.byte_to_package=self.parent.byte_to_package
        ###  编码表   ###
        self.dictThres={3:0x00,10:0x01,20:0x02,25:0x03,30:0x04,40:0x05}
        
        ##########################################
    
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 404,365 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer2 = wx.GridSizer( 1, 1, 0, 0 )
        
        self.m_notebook3 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_sweep_set = wx.Panel( self.m_notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer3 = wx.GridSizer( 6, 2, 0, 0 )
        
        
        gSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText6 = wx.StaticText( self.p_sweep_set, wx.ID_ANY, u"扫频接收模式", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        gSizer3.Add( self.m_staticText6, 0, wx.ALL, 5 )
        
        m_sweep_modeChoices = [ u"全频段", u"指定频段" ]
        self.m_sweep_mode = wx.ComboBox( self.p_sweep_set, wx.ID_ANY, u"全频段", wx.DefaultPosition, wx.DefaultSize, m_sweep_modeChoices, 0 )
        self.m_sweep_mode.SetSelection( 0 )
        gSizer3.Add( self.m_sweep_mode, 0, wx.ALL, 5 )
        
        self.m_staticText9 = wx.StaticText( self.p_sweep_set, wx.ID_ANY, u"文件上传模式", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        gSizer3.Add( self.m_staticText9, 0, wx.ALL, 5 )
        
        m_upload_modeChoices = [ u"手动上传", u"不定时自动上传", u"抽取定时自动上传" ]
        self.m_upload_mode = wx.ComboBox( self.p_sweep_set, wx.ID_ANY, u"手动上传", wx.DefaultPosition, wx.DefaultSize, m_upload_modeChoices, 0 )
        self.m_upload_mode.SetSelection( 0 )
        gSizer3.Add( self.m_upload_mode, 0, wx.ALL, 5 )
        
        self.m_staticText11 = wx.StaticText( self.p_sweep_set, wx.ID_ANY, u"文件上传抽取倍率（1-63）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        gSizer3.Add( self.m_staticText11, 0, wx.ALL, 5 )
        
        self.m_extract_M = wx.TextCtrl( self.p_sweep_set, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.m_extract_M, 0, wx.ALL, 5 )
        
        self.m_staticText10 = wx.StaticText( self.p_sweep_set, wx.ID_ANY, u"数据变化判定门限", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        gSizer3.Add( self.m_staticText10, 0, wx.ALL, 5 )
        
        m_change_thredChoices = [ u"10", u"20" ]
        self.m_change_thred = wx.ComboBox( self.p_sweep_set, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, m_change_thredChoices, 0 )
        self.m_change_thred.SetSelection( 0 )
        gSizer3.Add( self.m_change_thred, 0, wx.ALL, 5 )
        
        self.btn_set = wx.Button( self.p_sweep_set, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.btn_set, 0, wx.ALL, 5 )
        
        self.btn_cancel = wx.Button( self.p_sweep_set, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.btn_cancel, 0, wx.ALL, 5 )
        
        
        self.p_sweep_set.SetSizer( gSizer3 )
        self.p_sweep_set.Layout()
        gSizer3.Fit( self.p_sweep_set )
        self.m_notebook3.AddPage( self.p_sweep_set, u"扫频设置", False )
        self.p_sweep_param = wx.Panel( self.m_notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer4 = wx.GridSizer( 6, 2, 0, 0 )
        
        self.m_check_recvgain = wx.CheckBox( self.p_sweep_param, wx.ID_ANY, u"  接收增益（dB）", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_check_recvgain, 0, wx.ALL, 5 )
        
        self.m_slider_recvgain = wx.Slider( self.p_sweep_param, wx.ID_ANY, 7, -1, 73, wx.DefaultPosition, wx.Size( 150,-1 ), wx.SL_HORIZONTAL|wx.SL_LABELS|wx.SL_SELRANGE )
        gSizer4.Add( self.m_slider_recvgain, 0, wx.ALL, 5 )
        
        self.m_check_adapt = wx.CheckBox( self.p_sweep_param, wx.ID_ANY, u"  自适应门限（dB）", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_check_adapt, 0, wx.ALL, 5 )
        
        m_combo_adaptChoices = [ u"3 ", u"10", u"20", u"25", u"30", u"40" ]
        self.m_combo_adapt = wx.ComboBox( self.p_sweep_param, wx.ID_ANY, u"20", wx.DefaultPosition, wx.Size( 110,-1 ), m_combo_adaptChoices, 0 )
        self.m_combo_adapt.SetSelection( 2 )
        gSizer4.Add( self.m_combo_adapt, 0, wx.ALL, 5 )
        
        self.m_check_fix = wx.CheckBox( self.p_sweep_param, wx.ID_ANY, u"  固定门限（dB）", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_check_fix, 0, wx.ALL, 5 )
        
        self.m_text_fix = wx.TextCtrl( self.p_sweep_param, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_text_fix, 0, wx.ALL, 5 )
        
        self.m_check_channelgain = wx.CheckBox( self.p_sweep_param, wx.ID_ANY, u"  通道接收增益表", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_check_channelgain, 0, wx.ALL, 5 )
        
        m_combo_channelgainChoices = ['SRF201','SRF301']
        self.m_combo_channelgain = wx.ComboBox( self.p_sweep_param, wx.ID_ANY, 'SRF201', wx.DefaultPosition, wx.DefaultSize, m_combo_channelgainChoices, 0 )
        gSizer4.Add( self.m_combo_channelgain, 0, wx.ALL, 5 )
        
        self.m_check_antgain = wx.CheckBox( self.p_sweep_param, wx.ID_ANY, u"天线接收增益表", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_check_antgain, 0, wx.ALL, 5 )
        
        m_combo_antgainChoices =[u"超短套筒天线",u"超短螺旋天线",u"单鞭螺旋天线",u"平面双锥天线",u"AH-8000",u"AH-7000", \
                      u"TQJ-1000",u"国人对数",u"汇讯通对数",u"BTA-BicoLog",u"LX-520",u"LX-840",u"LX-1080"]
        self.m_combo_antgain = wx.ComboBox( self.p_sweep_param, wx.ID_ANY, u"超短套筒天线", wx.DefaultPosition, wx.DefaultSize, m_combo_antgainChoices, 0 )
        gSizer4.Add( self.m_combo_antgain, 0, wx.ALL, 5 )
        
        self.m_button_paramSet = wx.Button( self.p_sweep_param, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_button_paramSet, 0, wx.ALL, 5 )
        
        self.m_button_cancel = wx.Button( self.p_sweep_param, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_button_cancel, 0, wx.ALL, 5 )
        
        
        self.p_sweep_param.SetSizer( gSizer4 )
        self.p_sweep_param.Layout()
        gSizer4.Fit( self.p_sweep_param )
        self.m_notebook3.AddPage( self.p_sweep_param, u"参数设置", True )
        self.p_sweep_display = wx.Panel( self.m_notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer41 = wx.GridSizer( 6, 1, 0, 0 )
        
        
        gSizer41.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.check_spec = wx.CheckBox( self.p_sweep_display, wx.ID_ANY, u"   功率谱图", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer41.Add( self.check_spec, 0, wx.ALL, 5 )
        
        self.check_water = wx.CheckBox( self.p_sweep_display, wx.ID_ANY, u"   瀑布图", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer41.Add( self.check_water, 0, wx.ALL, 5 )
        
        self.btn_display = wx.Button( self.p_sweep_display, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer41.Add( self.btn_display, 0, wx.ALL, 5 )
        
        
        self.p_sweep_display.SetSizer( gSizer41 )
        self.p_sweep_display.Layout()
        gSizer41.Fit( self.p_sweep_display )
        self.m_notebook3.AddPage( self.p_sweep_display, u"显示窗口", False )
        self.p_seep_query = wx.Panel( self.m_notebook3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
#         self.p_seep_query.SetFont( wx.Font( 12, 74, 90, 90, False, "微软雅黑" ) )
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        m_radio_queryChoices = [ u"扫频范围", u"接收增益", u"工作状态",u"检测门限",u"接收通道增益修正表", u"天线增益修正表" ]
        self.m_radio_query = wx.RadioBox( self.p_seep_query, wx.ID_ANY, u"查询项", wx.DefaultPosition, wx.DefaultSize, m_radio_queryChoices, 1, wx.RA_SPECIFY_COLS )
        self.m_radio_query.SetSelection( 0 )
        bSizer2.Add( self.m_radio_query, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.btn_query = wx.Button( self.p_seep_query, wx.ID_ANY, u"查询", wx.DefaultPosition, wx.DefaultSize, 0 )
#         self.btn_query.SetFont( wx.Font( 9, 74, 90, 90, False, "微软雅黑" ) )
        
        bSizer2.Add( self.btn_query, 0, wx.ALL, 5 )
        
        
        self.p_seep_query.SetSizer( bSizer2 )
        self.p_seep_query.Layout()
        bSizer2.Fit( self.p_seep_query )
        self.m_notebook3.AddPage( self.p_seep_query, u"查询", False )
        
        gSizer2.Add( self.m_notebook3, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( gSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.m_sweep_mode.Bind( wx.EVT_COMBOBOX, self.m_sweep_modeOnCombobox )
        self.m_upload_mode.Bind( wx.EVT_COMBOBOX, self.m_upload_modeOnCombobox )
        self.btn_set.Bind( wx.EVT_BUTTON, self.btn_setOnButtonClick )
        self.btn_cancel.Bind( wx.EVT_BUTTON, self.btn_cancelOnButtonClick )
        self.m_button_paramSet.Bind( wx.EVT_BUTTON, self.m_button_paramSetOnButtonClick )
        self.m_button_cancel.Bind( wx.EVT_BUTTON, self.m_button_cancelOnButtonClick )
        self.btn_display.Bind( wx.EVT_BUTTON, self.btn_displayOnButtonClick )
        self.m_radio_query.Bind( wx.EVT_RADIOBOX, self.m_radioBox1OnRadioBox )
        self.btn_query.Bind( wx.EVT_BUTTON, self.btn_queryOnButtonClick )
    
    def __del__( self ):
        pass
    
 
    # Virtual event handlers, overide them in your derived class
    def m_sweep_modeOnCombobox( self, event ):
        if self.m_sweep_mode.GetSelection()==1:
            dlg=dialog_freqblock(None)
            dlg.ShowModal()
          
            if(dlg.isValid):
                self.freq_s=int(dlg.text_freq_start.GetValue())
                self.freq_e=int(dlg.text_freq_end.GetValue())
                print self.freq_s
                print self.freq_e
        
        else:
            self.freq_s=70
            self.freq_e=5995
                   
        event.Skip()
    
    def m_upload_modeOnCombobox( self, event ):
        index=self.m_upload_mode.GetSelection()
        if(index==0):
            self.m_change_thred.Enable(False)
            self.m_extract_M.Enable(False)
        elif(index==1):
            self.m_change_thred.Enable(True)
            self.m_extract_M.Enable(False)
            
            self.upload_mode=1
        else:
            self.m_change_thred.Enable(False)
            self.m_extract_M.Enable(True)
            
            self.upload_mode=2
          
        event.Skip()
        
    def btn_setOnButtonClick( self, event ):
        
         
        ###################
              
        if(self.upload_mode==1):
            self.changethres=int(self.m_change_thred.GetValue())
        
        elif(self.upload_mode==2):
            self.extract_m=int(self.m_extract_M.GetValue())

        #######  设置staticFileUpMode 结构体  ###########
        
        staticFileUp.setUploadMode(self.upload_mode)
        staticFileUp.setExtractM(self.extract_m)
        staticFileUp.setChangeThres(self.changethres)
        
        ########扫频设置下发#############
        sweepRangeSet=SweepRangeSet()
        sweepRangeSet.CommonHeader=FrameHeader(0x55,0x01,self.lowid,self.highid)
        sweepRangeSet.CommonTail=self.tail
        sweepRangeSet.SweepSectionNo=1
        sweepRangeSet.SweepSectionTotalNum=1
        sweepRangeSet.FileUploadMode=self.upload_mode
        sweepRangeSet.ExtractM=self.extract_m
        sweepRangeSet.ChangeThres=self.changethres
        
        
        if(self.m_sweep_mode.GetSelection()==0):    
            sweepRangeSet.SweepRecvMode=1
            sweepRangeSet.StartSectionNo=1 
            sweepRangeSet.EndSectionNo=237 
            sweepRangeSet.HighEndFreq=3
            sweepRangeSet.LowEndFreq=255
            
        else:
            sweepRangeSet.SweepRecvMode=2    
            array=self.SweepSection(self.freq_s, self.freq_e)
            sweepRangeSet=self.FillSweepRange(sweepRangeSet, array)
            
            ######### set tick ########
            self.setTickLable(array)
       
        self.outPoint.write(bytearray(sweepRangeSet))
        
        ######## show ##################
        self.show_recv_set.ShowSweepRange(sweepRangeSet)
        
      
            
        
    def setTickLable(self,array):       
        begin=(array[0]-1)*25+70
        end = array[1]*25+70




        self.parent.SpecFrame.panelFigure.setSpLabel(begin_X=self.freq_s, end_X=self.freq_e)
        
        self.parent.FreqMin=self.freq_s
        self.parent.FreqMax=self.freq_e
        self.parent.SpecFrame.panelFigure.FFT_Min_X=self.freq_s
        
        self.parent.SpecFrame.panelFigure.FFT_Max_X=self.freq_e
        self.parent.SpecFrame.panelFigure.Min_X.SetValue(str(self.freq_s))
        self.parent.SpecFrame.panelFigure.Max_X.SetValue(str(self.freq_e))

        totalNum=array[1]-array[0]+1

        if(totalNum>=40):
            if(totalNum%32==0):
                totalNum=totalNum/32
            else:
                totalNum=totalNum/32+1
            end=70+(array[0]+32*totalNum-1)*25

            print '-----------------', end

        # print totalNum
        xx = linspace(begin, end, 1024)
        self.parent.SpecFrame.panelFigure.lineSpec.set_xdata(xx)
        self.parent.SpecFrame.panelFigure.lineSpecBack.set_xdata(xx)
         
        if(isinstance(self.parent.WaterFrame,Water)):
            self.parent.WaterFrame.setWfLabel(begin,end)

            
        
    def FillSweepRange(self,sweepRangeSet,array):
        sweepRangeSet.StartSectionNo=array[0]
        sweepRangeSet.EndSectionNo=array[1]
        sweepRangeSet.HighStartFreq=array[2]
        sweepRangeSet.LowStartFreq=array[3]
        sweepRangeSet.HighEndFreq=array[4]
        sweepRangeSet.LowEndFreq=array[5]
        return sweepRangeSet
    def SweepSection(self,freqStart,freqEnd):
        startK=(freqStart-70)/25
        endK=(freqEnd-70)/25
        startNum=int(float(freqStart-(startK*25+70))*1024/25)
        endNum=int(float(freqEnd-(endK*25+70))*1024/25)
        startKth=startK+1
        endKth=endK+1 
        if ((freqEnd-70)%25==0):
            endKth=endK 
            endNum=1023
        startf_h=startNum>>8
        startf_l=startNum&0x0FF
        endf_h=endNum>>8
        endf_l=endNum&0x0FF
        return (startKth,endKth,startf_h,startf_l,endf_h,endf_l)
        
   
    def btn_cancelOnButtonClick( self, event ):
        event.Skip()
    
    def m_button_paramSetOnButtonClick( self, event ):
        if(self.m_check_recvgain.GetValue()):
            Gain=int(self.m_slider_recvgain.GetValue())
            header=FrameHeader(0x55,0x04,self.lowid,self.highid)
            gainSet=RecvGainSet()
            gainSet.CommonHeader=header
            gainSet.RecvGain=Gain+3
            gainSet.CommonTail=self.tail
            self.outPoint.write(bytearray(gainSet))
            
        if(self.m_check_adapt.GetValue()):
        
            thresSet=ThresSet()
            thresSet.AdaptThres=self.dictThres[int(self.m_combo_adapt.GetValue())]
            thresSet.CommonHeader=FrameHeader(0x55,0x06,self.lowid,self.highid)
            thresSet.ThresMode=0            
            thresSet.CommonTail=self.tail
            self.outPoint.write(bytearray(thresSet))
            
        
        if(self.m_check_fix.GetValue()):
            thresSet=ThresSet()
            thresSet.CommonHeader=FrameHeader(0x55,0x06,self.lowid,self.highid)
            thresSet.ThresMode=1         
            thresSet.CommonTail=self.tail
            
            thres=int(self.m_text_fix.GetValue())
            thresSet.HighFixedThres=thres>>8
            thresSet.LowFixedThres=thres& 0x00FF    
            self.outPoint.write(bytearray(thresSet))
            
        if(self.m_check_channelgain.GetValue()):
            self.SetCorrGain(0xC1)
        
        if(self.m_check_antgain.GetValue()):
            self.SetCorrGain(0xC2)
        
        event.Skip()
    
    def SetCorrGain(self,func):
        if(staticVar.getSock()==0):
            wx.MessageBox('Please Connect to Server!!', 
                   'Alert', wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        else:
            
            head=FrameHeader(0x55,func,self.lowid,self.highid)
            tail=self.tail
            encode=self.m_combo_channelgain.GetSelection()+1
            gainTable=ReqGainTable(head,encode>>8,encode&0x00FF,tail)
        
            staticVar.getSock().send(gainTable)
                
    def m_button_cancelOnButtonClick( self, event ):
        event.Skip()
    
    def btn_displayOnButtonClick( self, event ):
        ###child MDI Frame 只能继承parent MDIframe####
        if(self.check_spec.GetValue()):
            if(self.parent.SpecFrame==None):
                self.parent.SpecFrame=Spectrum_1.Spec(self.parent)
                self.parent.SpecFrame.Activate()
             
                
        if(self.check_water.GetValue()):
            if(self.parent.WaterFrame==None):
                self.parent.WaterFrame=Water(self.parent)
                self.parent.WaterFrame.Activate()
                self.parent.WaterFrame.setWfLabel(self.parent.FreqMin,self.parent.FreqMax)
                
        
        self.Destroy()
        event.Skip()
    def m_radioBox1OnRadioBox( self, event ):
        event.Skip()
    
    def btn_queryOnButtonClick( self, event ):
        index=self.m_radio_query.GetSelection()
        
        if(index==0):
            self.QuerySend(0x11)
            
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToSweepRange(li)
            self.show_recv_set.ShowSweepRange(obj)
            
        elif(index==1):
            self.QuerySend(0x14)
            
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToRecvGain(li)
            self.show_recv_set.ShowRecvGain(obj)
        
        elif(index==2):  ##终端是否在网
            self.QuerySend(0x1C)
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToWorkMode(li)
            self.show_recv_set.ShowIsConnect(obj)            

        elif(index==3):
            self.QuerySend(0x16)
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToThres(li)
            self.show_recv_set.ShowTestGate(obj) 


        elif(index==4):
            self.QuerySend(0x1D)
            
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToCorrGain(li)
            self.show_recv_set.ShowCorrGain(obj)
            
        else:
            self.QuerySend(0x1E)
            
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToAntGain(li)
            self.show_recv_set.ShowAntGain(obj)
            
            
        event.Skip()
    
    def QuerySend(self,funcPara):
        query=Query()
        query.CommonHeader=FrameHeader(0x55,funcPara,self.lowid,self.highid)
        query.CommonTail=self.tail
        self.outPoint.write(bytearray(query))   
        
        
        

# app=wx.App()
# dialog_sweep(None).Show()
# app.MainLoop()
 	

