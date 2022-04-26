import sys
import os
from cmath import phase,pi,log10
import numpy as np
from scipy.fftpack import fft
from Ui_demo1 import Ui_bodeplot_by_ZR
from PyQt5 import QtWidgets,QtGui
import matplotlib.pyplot as plt
import csv
# GUI打包代码 生成 exe 文件pyinstaller -F -w -i 1.ico run_ui.py
# GUI打包带图标 https://blog.csdn.net/momo3507/article/details/122639340

class Demo(QtWidgets.QWidget, Ui_bodeplot_by_ZR):
    def __init__(self):
        super(Demo, self).__init__()
        self.setupUi(self)
        self.inputbrowser.clicked.connect(self.inputread)
        self.outputbrowser.clicked.connect(self.outputread)
        self.calcul_begin.clicked.connect(self.calcul) 
        self.plot_time.clicked.connect(self.plottime)
        ICON=self.resource_path(os.path.join('ico','9.png'))
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.fileName_input=""
        self.fileName_output=""
    
        self.len_row=0
    ## 读入输入文件路径
    def inputread(self):
        fileName1,_=QtWidgets.QFileDialog.getOpenFileName(self,'Open input file',"./","表格(*.csv)")
        if fileName1:
            self.inputdir.setText(fileName1)
            self.outputdir.setText(fileName1)
            self.len_row= len(open(fileName1,errors='ignore').readlines())
            with open(fileName1,errors='ignore') as f:
                f_csv=csv.reader(f)
                csv_line=list(f_csv)
                if csv_line[7]==[]:
                    
                    self.len_row=self.len_row-9

            text=str(self.len_row)
            self.input_num.setText("输入数据总数："+text)
            self.output_num.setText("输出数据总数："+text)
            self.fileName_input=fileName1
            self.fileName_output=fileName1


        

    def outputread(self):
        fileName1,_=QtWidgets.QFileDialog.getOpenFileName(self,'Open output file',"./","表格(*.csv)")
        if fileName1:
            self.outputdir.setText(fileName1)
            self.len_row= len(open(fileName1,errors='ignore').readlines())
            with open(fileName1,errors='ignore') as f:
                f_csv=csv.reader(f)
                csv_line=list(f_csv)
                if csv_line[7]==[]:
                    self.list_pianzhi=9
                    self.len_row=self.len_row-9

            text=str(self.len_row)
            self.output_num.setText("输出数据总数："+text)
            self.fileName_output=fileName1

    def calcul(self):
        #读入需要的数据
        self.input_data=[];
        self.output_data=[];
        inputlie_pianzhi=int(self.inputlie.value())
        inputhang_pianzhi=int(self.inputhang.value())
        outputlie_pianzhi=int(self.outputlie.value())
        outputhang_pianzhi=int(self.outputhang.value())
        dianshu=int(self.point_num.value())
        groupshu=int(self.group_num.value())
        Fs=self.sample_frequ.value()
        
        frequ=np.linspace(0,Fs/2,int(dianshu/2))
        
        # 设置窗函数
        wind=self.comboBox.currentText()
        wind_data=np.ones(dianshu);
        if wind == "kaiser":
            parm=int(self.kaiser_parm.value())
            wind_data=np.kaiser(dianshu,int(self.kaiser_parm.value()))
            wind=wind+" with "+str(self.kaiser_parm.value())
        if wind == "hanning":
            wind_data=np.hanning(dianshu)
        if wind == "blackman":
            wind_data=np.blackman(dianshu)
        if self.checkBox.isChecked():
            wind_plot=wind_data
            wind_plot[0]=0
            wind_plot[-1]=0
            plt.figure("窗函数"+self.fileName_input)
            plt.plot(wind_plot)
        
        if self.fileName_input and self.fileName_output:
            with open(self.fileName_input,errors='ignore') as f:
                f_csv=csv.reader(f)
                csv_line=list(f_csv)
                for i in range(9,self.len_row):
                    data=csv_line[i][0].split('\t')
                    # print(data)
                    if len(data)>1:
                        self.input_data.append(float(data[inputlie_pianzhi-1]))
            # print(input_data)

            with open(self.fileName_output,errors='ignore') as f:
                f_csv=csv.reader(f)
                csv_line=list(f_csv)
                for i in range(9,self.len_row):
                    data=csv_line[i][0].split('\t')
                    # print(data)
                    if len(data)>1:
                        self.output_data.append(float(data[outputlie_pianzhi-1]))
            # print(output_data)
            #数据分组
            input_fftdata=np.ones([groupshu,dianshu],dtype=float)
            output_fftdata=np.ones([groupshu,dianshu],dtype=float)
            input_fft=np.ones([groupshu,dianshu],dtype=complex)
            output_fft=np.ones([groupshu,dianshu],dtype=complex)
            input_fft_avrage=np.ones(dianshu,dtype=complex)
            output_fft_avrage=np.ones(dianshu,dtype=complex)
            TF_=np.ones([int(dianshu/2)],dtype=complex)
            TF_pha=np.ones([int(dianshu/2)],dtype=float)
            TF_mag=np.ones([int(dianshu/2)],dtype=complex)
            for i in range(0,groupshu):
                for j in range(0,dianshu):
                    input_fftdata[i][j]=self.input_data[inputhang_pianzhi+j+dianshu*i];
                    output_fftdata[i][j]=self.output_data[outputhang_pianzhi+j+dianshu*i];

            for i in range(0,groupshu):
                input_fft[i]=fft(np.multiply(input_fftdata[i],wind_data))
                output_fft[i]=fft(np.multiply(output_fftdata[i],wind_data))
            for i in range(0,groupshu):
                for j in range(0,dianshu):
                    input_fft_avrage[j]=input_fft[i][j]/groupshu
                    output_fft_avrage[j]=output_fft[i][j]/groupshu

            for j in range (0,int(dianshu/2)):
                TF_[j]=output_fft_avrage[j]/input_fft_avrage[j]
                TF_pha[j]=phase(TF_[j])/pi*180
                TF_mag[j]=20*(log10(abs(TF_[j])).real)
            # print(TF_mag)
            # TF_pha=np.unwrap(TF_pha,pi)/pi*180
            plt.figure("传递函数"+" using "+wind+" wind "+self.fileName_input)
            plt.subplot(211)
            plt.xscale('log')
            plt.axhline(y=0,c='r',ls="--",lw=1)
            plt.axvline(x=frequ[-1],c='black',ls="-",lw=0.5)
            # plt.yscale('log')
            plt.grid()
            plt.plot(frequ,TF_mag,lw=0.8)
            plt.subplot(212)
            plt.xscale('log')
            plt.axhline(y=180,c='r',ls="--",lw=1)
            plt.axhline(y=-180,c='r',ls="--",lw=1)
            plt.axvline(x=frequ[-1],c='black',ls="-",lw=0.5)
            plt.grid()
            plt.ylim(-270,270)
            plt.plot(frequ,TF_pha,lw=0.8)
        
        plt.show()
        
    


    def plottime(self):
        #读入需要的数据
        self.input_data=[];
        self.output_data=[];
        inputlie_pianzhi=self.inputlie.value()
        inputhang_pianzhi=self.inputhang.value()
        outputlie_pianzhi=self.outputlie.value()
        outputhang_pianzhi=self.outputhang.value()
        dianshu=self.point_num.value()
        groupshu=self.group_num.value()
        if self.fileName_input and self.fileName_output:
            with open(self.fileName_input,errors='ignore') as f:
                f_csv=csv.reader(f)
                csv_line=list(f_csv)
                for i in range(9,self.len_row):
                    data=csv_line[i][0].split('\t')
                    
                    if len(data)>1:
                        self.input_data.append(float(data[inputlie_pianzhi-1]))

            with open(self.fileName_output,errors='ignore') as f:
                f_csv=csv.reader(f)
                csv_line=list(f_csv)
                for i in range(9,self.len_row):
                    data=csv_line[i][0].split('\t')
                    
                    if len(data)>1:
                        self.output_data.append(float(data[outputlie_pianzhi-1]))
                        # print(float(data[outputlie_pianzhi-1]))
            
            plt.figure("input data")
            plt.plot(range(dianshu*groupshu),self.input_data[inputhang_pianzhi:inputhang_pianzhi+dianshu*groupshu])
            plt.figure("output data")
            plt.plot(range(dianshu*groupshu),self.output_data[outputhang_pianzhi:outputhang_pianzhi+dianshu*groupshu])
            plt.show()

    def resource_path(self, relative_path):
    #"""将相对路径转为exe运行时资源文件的绝对路径"""
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS		# 只有通过exe运行时才会进入这个分支，它返回的是exe运行时的临时目录路径
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
   

if __name__ == '__main__':
   
    app = QtWidgets.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())