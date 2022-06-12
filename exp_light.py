# encoding=utf-8

"""
@version: 00
@author: haoming.zheng
@contact: zhmig@foxmail.com
@site: 
@software: PyCharm
@file: exp_light.py
@time: 2020/9/4 9:36
"""

import os, sys
# import pymel.core as pm
import maya.cmds as cmds

# import maya.mel as mel

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


class expLMainWin(QMainWindow):
    def __init__(self, parent=None):
        super(expLMainWin, self).__init__(parent)

        self.mainwindow()

    def mainwindow(self):
        self.setWindowTitle(u"导出主灯")
        self.setObjectName("expLWin")
        self.resize(400, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.expLwidget = QWidget(self)

        self.main_QVLay = QVBoxLayout()
        self.main_QVLay.setObjectName("main_QVLay")
        self.expLwidget.setLayout(self.main_QVLay)

        self.get_lightgrp()
        self.cam_combox()
        self.env_combox()
        self.atm_combox()
        self.exp_btn()
        self.cwd = os.getcwd()

        self.setCentralWidget(self.expLwidget)

    # def clear_layout(self, layout):
    #     for i in reversed(range(layout.count())):
    #         layout.itemAt(i).widget().setParent(None)

    def get_lightgrp(self):
        self.hor_Lay = QHBoxLayout()
        self.main_QVLay.addLayout(self.hor_Lay)

        self.expL_Label = QLabel(u"主灯组：")
        self.expL_Label.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.expL_Tx = QLineEdit()
        self.expL_Tx.setEnabled(False)
        self.getLigGrp_Btn = QPushButton(u"拾取")
        self.getLigGrp_Btn.clicked.connect(self.get_keylight)
        self.hor_Lay.addWidget(self.expL_Label)
        self.hor_Lay.addWidget(self.expL_Tx)
        self.hor_Lay.addWidget(self.getLigGrp_Btn)

        self.v_Spacer1 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.main_QVLay.addItem(self.v_Spacer1)

        if cmds.objExists("KeyLight"):
            self.expL_Tx.setText("KeyLight")
            print (u"获取到KeyLight组\n"),

    def cam_combox(self):

        self.cam_grpBox = QGroupBox(u"相机节点")
        self.cam_grpBox.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.cam_Hlay = QVBoxLayout(self.cam_grpBox)
        self.main_QVLay.addWidget(self.cam_grpBox)

        self.cam_ComBox = QComboBox()
        self.cam_Hlay.addWidget(self.cam_ComBox)
        self.v_Spacer2 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.main_QVLay.addItem(self.v_Spacer2)

    def env_combox(self):
        self.env_grpBox = QGroupBox(u"环境节点")
        self.env_grpBox.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.env_Hlay = QVBoxLayout(self.env_grpBox)
        self.main_QVLay.addWidget(self.env_grpBox)

        self.env_ComBox = QComboBox()
        self.env_Hlay.addWidget(self.env_ComBox)
        self.v_Spacer3 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.main_QVLay.addItem(self.v_Spacer3)

    def atm_combox(self):
        self.atm_grpBox = QGroupBox(u"大气节点")
        self.atm_grpBox.setStyleSheet("font: 10pt \"Adobe 黑体 Std R\";")
        self.atm_Hlay = QVBoxLayout(self.atm_grpBox)
        self.main_QVLay.addWidget(self.atm_grpBox)

        self.atm_ComBox = QComboBox()
        self.atm_Hlay.addWidget(self.atm_ComBox)
        self.v_Spacer4 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.main_QVLay.addItem(self.v_Spacer4)

    def exp_btn(self):
        self.exportBtn = QPushButton(u"导出灯光文件")
        self.exportBtn.setStyleSheet("font: 15pt \"Adobe 黑体 Std R\";")
        self.exportBtn.clicked.connect(self.exportLight)

        self.main_QVLay.addWidget(self.exportBtn)

    def add_camComBox(self, get_cam):
        if self.cam_ComBox.count() is not None:
            self.cam_ComBox.clear()
        self.cam_ComBox.addItems(get_cam)
        return get_cam

    def add_envComBox(self, get_env):
        if self.env_ComBox.count() is not None:
            self.env_ComBox.clear()
        self.env_ComBox.addItems(get_env)
        return get_env

    def add_atmComBox(self,get_atm):
        if self.atm_ComBox.count() is not None:
            self.atm_ComBox.clear()
        self.atm_ComBox.addItems(get_atm)
        return get_atm

    def get_keylight(self):
        sel_grp = cmds.ls(sl=True)
        if cmds.listRelatives(sel_grp[0], shapes=True):
            print (u"选中的不是组"),
        else:
            self.expL_Tx.setText(str(sel_grp[0]))

    def exportLight(self):
        node = []
        if self.cam_ComBox.count() > 0:
            node.append(self.cam_ComBox.currentText())
            # print node,
        if self.env_ComBox.count() > 0:
            node.append(self.env_ComBox.currentText())
            # print node,
        if self.atm_ComBox.count() > 0:
            node.append(self.atm_ComBox.currentText())
            # print node,
        if self.expL_Tx.text() == "":
            print u"没有获取主灯组",
        else:
            node.append(self.expL_Tx.text())
            print node,
            fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                    "文件保存",
                                                                    self.cwd,  # 起始路径
                                                                    "mayaAscii(*.ma);;mayaBinary(*.mb);;All Files (*.*)")

            if fileName_choose == "":
                print(u"\n取消选择")
                return
            cmds.select(node, r=True)
            cmds.file(fileName_choose,f=True,op="v=0",typ=filetype[:-6],pr=True,es=True)
            print(u"\n你选择要保存的文件为:")
            print(fileName_choose)
            self.close()
            print(u"文件筛选器类型: ", filetype)




if __name__ == '__main__':
    # test = QApplication(sys.argv)
    ex = expLMainWin()
    ex.show()
    # sys.exit(test.exec_())