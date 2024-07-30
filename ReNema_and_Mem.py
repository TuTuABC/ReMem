# -*- coding:utf-8 -*-
import ctypes
import os
import socket
import sys
import threading
import maya.OpenMaya as om
import time
import maya.mel as mel
import maya.cmds as cmds
import PySide2
from PySide2.QtCore import Qt, QSize, QRect
from PySide2.QtGui import QCursor, QPixmap, QPainter, QBrush, QColor, QFont, QPen, QIcon, QImage, QFontDatabase
from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QPushButton, QGridLayout

dll_path = os.path.dirname(__file__).replace('\\', '/') + '\FistScannn.dll'  # 请替换为DLL的实际路径


class TopUI2(QLabel):

    def __init__(self, colR, colG, colB, WIDTH, HEIGHT, map_path):
        super(TopUI2, self).__init__()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.colR = colR
        self.colG = colG
        self.colB = colB

        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self.image = QImage(r'%s' % map_path)
        # self.setStyleSheet('''QWidget{border-radius:18px;background-color:#ff9d00;}''')
        self.pixmap = QPixmap.fromImage(
            self.image.scaled(self.WIDTH, self.HEIGHT, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.setPixmap(self.pixmap)


# 定义分割缝，输入R，G，B，长，宽，显示文本
class TopUI(QWidget):

    def __init__(self, colR, colG, colB, WIDTH, HEIGHT, text):
        super(TopUI, self).__init__()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.colR = colR
        self.colG = colG
        self.colB = colB

        self.text = text

        self.setFixedSize(self.WIDTH, self.HEIGHT)

    #   把N去掉
    def paintEventN(self, event, topcol=None, topcolG=None, topcolB=None):
        topcolR = self.colR
        topcolG = self.colG
        topcolB = self.colB
        p = QPainter()
        p.begin(self)

        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QBrush(QColor(topcolR, topcolG, topcolB))))
        p.drawRect(self.rect())

        font = QFont()
        font.setPixelSize(16)
        font.setFamily('BankGothic Md BT')
        p.setFont(font)
        pen = QPen(QColor(255, 255, 255))
        p.setPen(pen)
        p.drawText(self.rect(), Qt.AlignVCenter | Qt.AlignLeft, self.text)

        p.end()


# 定义按钮，输入图片路径，图片长，图片宽，提示
class cubutton(QPushButton):
    def __init__(self, map_path, icon_WIDTH, icon_HEIGHT, tips):
        super(cubutton, self).__init__()

        pixmap = QPixmap(r'%s' % map_path).scaled(icon_WIDTH, icon_HEIGHT)
        self.btn = QPushButton(parent=None)
        # self.btn.setFixedSize(42, 40)
        _A, _B, _C = os.path.dirname(__file__).replace('\\', '/') + "/icon/close.png", os.path.dirname(
            __file__).replace('\\', '/') + "/icon/close2.png", os.path.dirname(__file__).replace('\\',
                                                                                                 '/') + "/icon/close3.png"
        print(_A, _B, _C)
        self.btn.setStyleSheet("QPushButton{color: black}"
                               f"QPushButton{{border-image: url({_A})}}"
                               f"QPushButton:hover{{border-image: url({_B})}}"
                               f"QPushButton:pressed{{border-image: url({_C})}}"
                               "QPushButton{border-radius:20px;}")

        # self.btn.setStyleSheet("border: 0px solid red;"'background:brack')

        # self.btn.setIconSize(QSize(icon_WIDTH, icon_HEIGHT))
        # self.btn.setIcon(QIcon(pixmap))
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.btn.setToolTip(tips)


class Child(QWidget):
    def __init__(self):
        font_path = os.path.dirname(__file__).replace('\\', '/')+"/方正胖头鱼简体.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.SocketFlag = True
        super(Child, self).__init__()
        self.setWindowTitle('______')
        self.resize(800, 599)
        script_dir = os.path.dirname(__file__)

        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        main_layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        self.setLayout(main_layout)
        self.lab1el2 = TopUI(255, 0, 0, 700, 86, "NO")
        self.closebutton = cubutton(script_dir + "\icon\close.png", 100, 86, "关闭")
        self.closebutton.btn.setFixedSize(100, 86)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout2.setSpacing(0)
        layout2.setContentsMargins(0, 0, 0, 0)
        layout1.addWidget(self.lab1el2)
        layout1.addWidget(self.closebutton.btn)
        self.lab1el3 = TopUI(255, 255, 0, 40, 236, "NO")
        self.lab1elA = TopUI2(255, 200, 0, 180, 236, os.path.dirname(__file__).replace('\\', '/') + "/icon/A.png")
        self.lab1elB = TopUI2(255, 150, 0, 180, 236, os.path.dirname(__file__).replace('\\', '/') + "/icon/B.png")
        self.lab1elC = TopUI2(255, 100, 0, 180, 236, os.path.dirname(__file__).replace('\\', '/') + "/icon/C.png")
        self.lab1elD = TopUI2(255, 50, 0, 180, 236, os.path.dirname(__file__).replace('\\', '/') + "/icon/D.png")
        self.lab1el4 = TopUI(255, 255, 50, 40, 236, "NO")

        self.lab1el5 = TopUI(255, 0, 0, 800, 158, "NO")
        self.lab1el6 = QLabel()
        self.lab1el6.resize(800, 50)
        self.lab1el6.setFixedSize(800, 40)
        self.lab1el6.setText("准备开始扫描")
        self.lab1el6.setAlignment(Qt.AlignCenter)
        self.lab1el6.setStyleSheet(
            f"border: 0px solid red;color: #f7f7f7;font-size:36px;font-family:{font_family}")  # 去边框
        self.lab1elA.setStyleSheet('''QWidget{border: 0px;border-radius:18px;background-color:#ff9d00;}''')

        layout2.addWidget(self.lab1el3)
        layout2.addWidget(self.lab1elA)
        layout2.addWidget(self.lab1elB)
        layout2.addWidget(self.lab1elC)
        layout2.addWidget(self.lab1elD)
        layout2.addWidget(self.lab1el4)
        layout2.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Fixed))

        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addWidget(self.lab1el5)
        main_layout.addWidget(self.lab1el6)
        main_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.show()
        self.closebutton.btn.clicked.connect(self.closeChild)
        self.socketinit()
        print("准备开始扫描")
        # self.receive_socket_info()

        self.rename_layer_manager_child('layerManager', 'defaultLayer')
        mel.eval("layerEditorDisplayLayerChange;")
        self.lab1elA.setStyleSheet('''QWidget{border: 0px;border-radius:18px;background-color:None;}''')
        self.lab1elB.setStyleSheet('''QWidget{border-radius:18px;background-color:#ff9d00;}''')
        try:
            cmds.setAttr("layerManager.displayLayerId[0]", 24827)
        except:
            cmds.setAttr("layerManager.displayLayerId[0]", 24127)
            cmds.setAttr("layerManager.displayLayerId[0]", 24827)
        t = threading.Thread(target=self.fun, args=())
        t.daemon = True
        t.start()
        t2 = threading.Thread(target=self.fun2, args=())
        t2.daemon = True
        t2.start()

    def closeChild(self):
        self.SocketFlag = False
        self.socket_server.close()
        self.close()

    def rename_layer_manager_child(self, layer_manager_name, new_name):
        # 获取 layerManager 节点的 MObject
        selection_list = om.MSelectionList()
        selection_list.add(layer_manager_name)
        layer_manager_mobject = om.MObject()
        selection_list.getDependNode(0, layer_manager_mobject)
        # 获取 layerManager 节点的 MFnDependencyNode
        layer_manager_fn = om.MFnDependencyNode(layer_manager_mobject)
        # 获取 displayLayerId 属性
        display_layer_id_attr = layer_manager_fn.attribute('displayLayerId[0]')
        # 创建 displayLayerId 属性的 MPlug
        display_layer_id_plug = om.MPlug(layer_manager_mobject, display_layer_id_attr)
        # 获取连接到 displayLayerId 属性的节点
        connected_plugs = om.MPlugArray()
        display_layer_id_plug.connectedTo(connected_plugs, False, True)
        # 遍历连接并重命名子节点
        connected_node = connected_plugs[0].node()
        connected_fn = om.MFnDependencyNode(connected_node)
        # 设置新名称
        connected_fn.setName(new_name)

    def MTData(self, start_address):
        # 打开进程并获取进程句柄
        PROCESS_ALL_ACCESS = 0x1F0FFF
        process = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, os.getpid())
        if not process:
            raise Exception("无法打开进程")
        # 定义缓冲区大小为2字节
        buffer_size = 2
        # 要读取的内存地址（64位）
        # 修改数值，加上100
        modified_value = 0
        # 将修改后的值转换为字节序列，准备写入目标进程
        new_buffer = (ctypes.c_byte * buffer_size)(*modified_value.to_bytes(buffer_size, byteorder='little'))
        # 执行内存写入
        bytes_written = ctypes.c_ulonglong(0)
        result_write = ctypes.windll.kernel32.WriteProcessMemory(process, ctypes.c_void_p(int(start_address, 16)),
                                                                 new_buffer,
                                                                 buffer_size, ctypes.byref(bytes_written))

        if not result_write:
            raise Exception("写入内存失败")

        print(f"成功写入 {bytes_written.value} 字节")
        ctypes.windll.kernel32.CloseHandle(process)

    def rename_layer_manager_child(self,layer_manager_name, new_name):
        selection_list = om.MSelectionList()
        selection_list.add(layer_manager_name)
        layer_manager_mobject = om.MObject()
        selection_list.getDependNode(0, layer_manager_mobject)
        layer_manager_fn = om.MFnDependencyNode(layer_manager_mobject)
        display_layer_id_attr = layer_manager_fn.attribute('displayLayerId')
        display_layer_id_plug = om.MPlug(layer_manager_mobject, display_layer_id_attr)
        element_plug = display_layer_id_plug.elementByPhysicalIndex(0)
        connected_plugs = om.MPlugArray()
        element_plug.connectedTo(connected_plugs, False, True)
        connected_node = connected_plugs[0].node()
        connected_fn = om.MFnDependencyNode(connected_node)
        connected_fn.setName(new_name)

    def fun(self):
        self.receive_socket_info()

    def fun2(self):
        ce_lib = ctypes.WinDLL(dll_path)
        ce_lib.MM(ctypes.c_ulong(os.getpid()), ctypes.c_ulong(8888))

    def socketinit(self):

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket_server.bind(("localhost", 8888))
        except:
            self.socket_server.close()

            self.socket_server.bind(("localhost", 8888))
        self.socket_server.listen(1)

    def receive_socket_info(self):
        while self.SocketFlag:
            try:
                conn, address = self.socket_server.accept()
                self.socket_data = conn.recv(18)
                if str(self.socket_data)[2:7] == "start":
                    self.lab1elB.setStyleSheet('''QWidget{border-radius:18px;background-color:None;}''')
                    self.lab1elC.setStyleSheet('''QWidget{border-radius:18px;background-color:#ff9d00;}''')
                    msg = 24836
                    cmds.setAttr("layerManager.displayLayerId[0]", msg)
                    conn.send(str(msg).encode("UTF-8"))
                    self.socket_server.settimeout(3)
                    while self.SocketFlag:
                        try:
                            conn, address = self.socket_server.accept()
                        except:
                            self.lab1elC.setStyleSheet('''QWidget{border-radius:18px;background-color:None;}''')
                            self.lab1elD.setStyleSheet('''QWidget{border-radius:18px;background-color:#ff9d00;}''')
                            self.SocketFlag = False
                            mel.eval("layerEditorDisplayLayerChange;")
                            break
                        self.socket_data = conn.recv(18)
                        print(str(self.socket_data)[2:20])
                        self.MTData(str(self.socket_data)[2:20])
                    break



                else:
                    print(self.socket_data)
                    self.lab1el6.setText(str(self.socket_data)[2:20])


            except:
                print("退出")

    def paintEvent(self, event):  # set background_img

        painter = QPainter(self)

        # painter.drawRect(self.rect())

        pixmap = QPixmap(os.path.dirname(__file__).replace('\\', '/') + "/icon/background.png")  # 换成自己的图片的相对路径
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.drawPixmap(self.rect(), pixmap)

    # 鼠标事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            xy = self.pos()
            self.w, self.h = xy.x(), xy.y()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myPet = Child()

    sys.exit(app.exec_())
