import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class fileDialogdemo(QWidget):
    def __init__(self,parent=None):
        super(fileDialogdemo, self).__init__(parent)

        #垂直布局
        layout=QVBoxLayout()

        #创建按钮，绑定自定义的槽函数，添加到布局中
        self.btn=QPushButton("加载图片")
        self.btn.clicked.connect(self.getimage)
        layout.addWidget(self.btn)

        #创建标签，添加到布局中
        self.le=QLabel('')
        layout.addWidget(self.le)

        #创建按钮，绑定自定义的槽函数，添加到布局
        self.btn1=QPushButton('加载文本文件')
        self.btn1.clicked.connect(self.getFiles)
        layout.addWidget(self.btn1)

        #实例化多行文本框，添加到布局
        self.contents=QTextEdit()
        layout.addWidget(self.contents)

        #设置主窗口的布局及标题
        self.setLayout(layout)
        self.setWindowTitle('File Dialog 例子')

    def getimage(self):
        #从C盘打开文件格式（*.jpg *.gif *.png *.jpeg）文件，返回路径
        image_file,_=QFileDialog.getOpenFileName(self,'Open file','C:\\','Image files (*.jpg *.gif *.png *.jpeg)')
        #设置标签的图片
        self.le.setPixmap(QPixmap(image_file))
    def getFiles(self):
        #实例化QFileDialog
        dig=QFileDialog()
        #设置可以打开任何文件
        dig.setFileMode(QFileDialog.AnyFile)
        #文件过滤
        dig.setFilter(QDir.Files)

        if dig.exec_():
            #接受选中文件的路径，默认为列表
            filenames=dig.selectedFiles()
            #列表中的第一个元素即是文件路径，以只读的方式打开文件
            f=open(filenames[0],'r')

            with f:
                #接受读取的内容，并显示到多行文本框中
                data=f.read()
                self.contents.setText(data)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=fileDialogdemo()
    ex.show()
    sys.exit(app.exec_())
123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263
