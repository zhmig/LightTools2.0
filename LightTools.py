# coding=utf-8

"""
@version: 00(内测版)
@author: haoming.zheng
@contact: zhmig@foxmail.com
@site: 
@software: PyCharm
@file: LightTools.py
@time: 2020/4/6 16:47
"""

import os, re, sys
import maya.mel as mel
import pymel.core as pm
import maya.cmds as cmds
from functools import partial

sys.path.append(r"//10.2.1.250/Enlighten_Tools/python/light/lightTools2.0")
import exp_light
reload(exp_light)

class lightTool(object):
    def __init__(self):
        pass

    def createWin(self):
        self.lt_Dock = cmds.optionVar(q = "lightToolDock")
        if mel.eval("exists dockControl") == "1L":
            if not cmds.optionVar('lightToolDock', ex=True):
                self.lt_Dock = 1

        if (cmds.window('lighttools_win', q=True, ex=True)):
            cmds.deleteUI('lighttools_win')

        if cmds.dockControl('lighttools_win_dock',q=True , ex=True):
            cmds.deleteUI('lighttools_win_dock',ctl=True)
        self.window = cmds.window('lighttools_win', t=u'LightTools 2.0.1 内测版', wh=(400, 600), rtf=True)
        self.menuOptions()
        self.mainFormLay = cmds.formLayout('main_lay')
        self.rs_win_formLay()
        self.parameter_tablay()
        cmds.formLayout(self.mainFormLay, e=1, af=[['rs_win_formlay', 'top', 3],
                                                   ['rs_win_formlay', 'left', 2],
                                                   ['rs_win_formlay', 'right', 2],
                                                   ['mainparameter_tablay', 'left', 2],
                                                   ['mainparameter_tablay', 'right', 2],
                                                   ['mainparameter_tablay', 'bottom', 3]],
                        ac=[['mainparameter_tablay', 'top', 3, 'rs_win_formlay']])

        if pm.pluginInfo("redshift4maya", q=True,l=True) == 1:
            cmds.checkBox('rs_checkBox', e=True, v=1)

        if self.lt_Dock == 1:
            cmds.dockControl('lighttools_win_dock', l='Light Tool 2.0', con=self.window, a='left',
                             aa=['top', 'bottom', 'left', 'right'])
            cmds.evalDeferred('cmds.dockControl("lighttools_win_dock", e=True, r=True)')
        else:
            cmds.showWindow()

    def ltDockWin(self,dock,*args):
        self.lt_Dock = cmds.optionVar(q = "lightToolDock")
        cmds.optionVar(iv=("lightToolDock", dock))
        if cmds.dockControl('lighttools_win_dock',q=True , ex=True):
            cmds.deleteUI('lighttools_win_dock',ctl=True)
        self.createWin()

    def menuOptions(self,*args):

        self.menuLay = cmds.menuBarLayout(p=self.window)
        self.file_menu = cmds.menu(p=self.menuLay, l=u"File")
        self.edit_menu = cmds.menu(p=self.menuLay, l=u"Edit")
        self.help_menu = cmds.menu(p=self.menuLay, l=u"Help")

        self.exp_light = cmds.menuItem(p=self.file_menu,
                                       l=u"导出灯光",
                                       c=self.change_exp_lightfile)

    def change_exp_lightfile(self,*args):
        self.lightwin = exp_light.expLMainWin()

        if cmds.objExists('redshiftOptions') == 0:
            cmds.createNode("RedshiftOptions",n="redshiftOptions")
        get_cam = cmds.ls(type="RedshiftPostEffects")
        get_env = cmds.ls(type=["RedshiftEnvironment", "RedshiftPhysicalSky"])
        get_atm = cmds.ls(type="RedshiftVolumeScattering")

        self.lightwin.add_camComBox(get_cam)
        self.lightwin.add_envComBox(get_env)
        self.lightwin.add_atmComBox(get_atm)
        # if self.lightwin.isEnabled():
        #     self.lightwin.close()
        self.lightwin.show()

    def rs_win_formLay(self):
        self.rswin_formLay = cmds.formLayout('rs_win_formlay', p=self.mainFormLay)
        self.rsPlugin_CBox = cmds.checkBox('rs_checkBox', l=u'是否加载Redshift渲染器', cc=self.load_rs_plugin)
        self.dockBtn = cmds.button('dockBtn', l=u'挂靠窗口', c=partial(self.ltDockWin,1))
        self.undockBtn = cmds.button('undockBtn', l=u'悬浮窗口', c=partial(self.ltDockWin,0))
        cmds.formLayout(self.rswin_formLay, e=1, af=[[self.rsPlugin_CBox, 'top', 3],
                                                     [self.rsPlugin_CBox, 'left', 5],
                                                     [self.dockBtn, 'top', 3],
                                                     [self.dockBtn, 'right', 90],
                                                     [self.undockBtn, 'top', 3]],
                        ac=[[self.undockBtn, 'left', 5, self.dockBtn]])

    # 主要模块界面加载窗口
    def parameter_tablay(self):
        self.mainPar_tabLay = cmds.tabLayout('mainparameter_tablay', p=self.mainFormLay, tv=False, scr=True, cr=True)
        self.mainPar_formLay = cmds.formLayout('mainparameter_formlay', p=self.mainPar_tabLay)
        self.rsLightLayot()
        self.objAttriLayout()
        self.objID_lay()
        self.renderlayer_lay()
        self.im_light_lay()
        cmds.formLayout('mainparameter_formlay', e=1,
                        af=[['createlight_framelay', 'top', 3], ['createlight_framelay', 'left', 2],
                            ['createlight_framelay', 'right', 2], ['attri_framelay', 'left', 2],
                            ['attri_framelay', 'right', 2], ['objID_framelay', 'left', 2],
                            ['objID_framelay', 'right', 2], ['renderlayer_framelay', 'left', 2],
                            ['renderlayer_framelay', 'right', 2], ['importlight_framelay', 'left', 2],
                            ['importlight_framelay', 'right', 2]],
                        ac=[['attri_framelay', 'top', 3, 'createlight_framelay'],
                            ['objID_framelay', 'top', 3, 'attri_framelay'],
                            ['renderlayer_framelay', 'top', 3, 'objID_framelay'],
                            ['importlight_framelay', 'top', 3, 'renderlayer_framelay']])

    # 获取是否加载redshift 插件
    def load_rs_plugin(self,*args):
        if cmds.checkBox('rs_checkBox', q=True, v=True) == 0:
            pm.unloadPlugin("redshift4maya")
        else:
            pm.loadPlugin("redshift4maya")

    # 创建rs默认灯光界面模块
    def rsLightLayot(self):
        self.createLightFrameLay = cmds.frameLayout('createlight_framelay', ebg=True, cll=True, l=u'创建灯光',
                                                    fn='fixedWidthFont')
        self.rsdefaultlight_famelay = cmds.formLayout('rsdefaultlight_famelay')
        self.lightmethod = {u'平行灯': [u'rs_lightDirectional.svg','directional_iconTxBtn','directionalLight','RedshiftPhysicalLight'],
                            u'面光灯': [u'rs_lightArea.svg','area_iconTxBtn','areaLight','RedshiftPhysicalLight'],
                            u'点光灯': [u'rs_lightPoint.svg','point_iconTxBtn','pointLight','RedshiftPhysicalLight'],
                            u'聚光灯': [u'rs_lightSpot.svg','spot_iconTxBtn','spotLight','RedshiftPhysicalLight'],
                            u'窗口灯': [u'rs_lightPortal.svg','portal_iconTxBtn','PortalLight','RedshiftPortalLight'],
                            u'IES灯': [u'rs_lightIES.svg','ies_iconTxBtn','IESLight','RedshiftIESLight'],
                            u'太阳灯': [u'rs_lightSunSky.svg','sunsky_iconTxBtn','PhysicalSun','RedshiftPhysicalSun'],
                            u'天光': [u'rs_lightDome.svg','dome_iconTxBtn','DomeLight','RedshiftDomeLight']}
        for name, value in self.lightmethod.items():
            cmds.iconTextButton(('%s' % value[1]), i=value[0],
                                                    l=name,
                                                    st='iconAndTextVertical',
                                                    c=partial(self.createRslightType,value[2],value[3]))

        cmds.formLayout(self.rsdefaultlight_famelay, e=1,
                        af=[['directional_iconTxBtn', 'top', 5], ['area_iconTxBtn', 'top', 5],
                            ['point_iconTxBtn', 'top', 5], ['spot_iconTxBtn', 'top', 5],
                            ['portal_iconTxBtn', 'top', 5], ['ies_iconTxBtn', 'top', 5],
                            ['sunsky_iconTxBtn', 'top', 5], ['dome_iconTxBtn', 'top', 5]],
                        ap=[['directional_iconTxBtn', 'left', 0, 3], ['area_iconTxBtn', 'left', 2, 15],
                            ['point_iconTxBtn', 'left', 2, 28], ['spot_iconTxBtn', 'left', 2, 40],
                            ['portal_iconTxBtn', 'left', 2, 53], ['ies_iconTxBtn', 'left', 2, 65],
                            ['sunsky_iconTxBtn', 'left', 2, 77], ['dome_iconTxBtn', 'left', 2, 88]])

    # 创建灯光的命令
    def createRslightType(self,*args):
        self.light = cmds.shadingNode(args[1], al=True, n=("%sShape" % args[0]))
        print (u"创建Rs灯光: %s\n" % self.light),
        self.light_type = {'directionalLight':3,'areaLight':0,'pointLight':1,'spotLight':2}
        if self.light :
            if self.light in self.light_type.keys():
                cmds.setAttr(("%s.lightType" % self.light),self.light_type[self.light])
            cmds.setAttr(("%s.scaleX") % self.light, 2)
            cmds.setAttr(("%s.scaleY") % self.light, 2)
            cmds.setAttr(("%s.scaleZ") % self.light, 2)
            cmds.select(self.light, r=True)

    # 主要界面布局
    def objAttriLayout(self):
        self.attriFrame = cmds.frameLayout('attri_framelay', p='mainparameter_formlay', cll=True, l=u'属性修改', fn='fixedWidthFont')
        self.attriTab = cmds.tabLayout('attri_tablay', cr=True)
        self.commonAttriCol = cmds.columnLayout('commonAttri_col',adj=True)
        self.commonAttri_control()
        self.mayadefault_funcAtti_control()
        self.rscommon_funcattri_control()
        cmds.tabLayout('attri_tablay', e=1,
                       tli=[[1, u'\u5e38\u7528\u5c5e\u6027'], [2, u'MAYA \u81ea\u5e26\u5c5e\u6027'],
                            [3, u'Redshift \u5c5e\u6027']])

    # 常用参数布局
    def commonAttri_control(self):
        attri_opt_tx = {u"Proxy": [(u"Proxy遮罩", "on", "off"),
                                   (u"Proxy材质覆盖", "on", "off"),
                                   (u"Proxy自身投影", "on", "off"),
                                   (u"Proxy后台细分", "on", "off"),
                                   (u"Proxy高低模切换","High Mode","Low Mode"),
                                   (u"Proxy氛围模型切换",u"白天",u"晚上")],
                       u"物体": [(u"物体遮罩", "on", "off"),
                               (u"物体细分", "on", "off"),
                               (u"物体置换", "on", "off")],
                       u"灯光": [(u"灯光连接", "Make Link", "Break Link")]}
        for index, com_attri in enumerate(attri_opt_tx):
            self.opt_colLay = cmds.columnLayout(("optColLay_%s" % str(index)), p = 'commonAttri_col', adj = True)
            self.commomtext = cmds.text(("tx_%s" % index),
                                        p ="optColLay_%s" % index,
                                        l = ((u"----------* {} *----------").format(com_attri)),
                                        h = 18,
                                        al = 'center',
                                        fn = 'fixedWidthFont',
                                        bgc = [0.2,0.2,0.2])
            for opt_name in range(len(attri_opt_tx[com_attri])):
                if (len(attri_opt_tx[com_attri][opt_name])) >0:
                    self.optRowLay = cmds.rowLayout(("rowLay_%s" % str(index) + str(opt_name)),
                                                    p = ("optColLay_%s" % (index)),
                                                    bgc = [0.2,0.2,0.2],
                                                    nc = 3,
                                                    cw = [[2, 100], [3, 100]],adj=1)
                    self.func_tx = cmds.text(("func_tx_%s" % str(index) + str(opt_name)),
                                             p = ("rowLay_%s" % str(index) + str(opt_name)),
                                             l = attri_opt_tx[com_attri][opt_name][0],
                                             fn = 'fixedWidthFont',
                                             bgc = [0.3,0.3,0.3])
                    self.func_on_Btn = cmds.button(("func_on_Btn_%s" % str(index) + str(opt_name)),
                                                   p = ("rowLay_%s" % str(index) + str(opt_name)),
                                                   l = attri_opt_tx[com_attri][opt_name][1],
                                                   w = 70,
                                                   c = partial(self.commonfunc_attri,
                                                               com_attri,
                                                               attri_opt_tx[com_attri][opt_name][0],
                                                               attri_opt_tx[com_attri][opt_name][1]))
                    self.func_off_Btn = cmds.button(("func_off_Btn_%s" % str(index) + str(opt_name)),
                                                    p = ("rowLay_%s" % str(index) + str(opt_name)),
                                                    l = attri_opt_tx[com_attri][opt_name][2],
                                                    w = 70,
                                                    c = partial(self.commonfunc_attri,
                                                                com_attri,
                                                                attri_opt_tx[com_attri][opt_name][0],
                                                                attri_opt_tx[com_attri][opt_name][2]))

    # 常用参数调用
    def commonfunc_attri(self,functx,func_op_tx,commonfunc,*args):

        light_shape_type = ["RedshiftPhysicalLight", "RedshiftIESLight", "RedshiftPhysicalSun", "RedshiftDomeLight",
                            "ambientLight", "directionalLight", "pointLight", "spotLight", "areaLight", "volumeLight"]
        lights = []
        objects = []

        select_obj = pm.ls(sl=True)
        for obj in select_obj:
            shapes = obj.listRelatives(s=True)

            #redshift代理属性部分
            if functx == u"Proxy":
                if func_op_tx == u"Proxy遮罩":
                    for shape in shapes:
                        if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                            pm.editRenderLayerAdjustment("%s.rsMatteEnable" % shape)
                            pm.editRenderLayerAdjustment("%s.rsMatteAlpha" % shape)
                            pm.editRenderLayerAdjustment("%s.visibilityMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0])
                        if commonfunc == "on":
                            pm.setAttr(("%s.rsMatteEnable" % shape),1)
                            pm.setAttr(("%s.rsMatteAlpha" % shape), 0)
                            pm.setAttr(("%s.visibilityMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0]), 1)
                            print(u"{} Proxy物体遮罩已打开".format(obj)),
                        if commonfunc == "off":
                            pm.setAttr(("%s.rsMatteEnable" % shape),0)
                            pm.setAttr(("%s.rsMatteAlpha" % shape), 1)
                            pm.setAttr(("%s.visibilityMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0]), 0)
                            print(u"{} Proxy物体遮罩已关闭".format(obj)),

                if func_op_tx == u"Proxy材质覆盖":
                    for shape in shapes:
                        if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                            pm.editRenderLayerAdjustment("%s.materialMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0])
                        if commonfunc == "on":
                            pm.setAttr(("%s.materialMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0]), 1)
                            print(u"{} Proxy物体材质覆盖已打开".format(obj)),
                        if commonfunc == "off":
                            pm.setAttr(("%s.materialMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0]), 0)
                            print(u"{} Proxy物体材质覆盖已关闭".format(obj)),

                if func_op_tx == u"Proxy自身投影":
                    for shape in shapes:
                        if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                            pm.editRenderLayerAdjustment("%s.rsEnableVisibilityOverrides" % shape)
                            pm.editRenderLayerAdjustment("%s.rsShadowCaster" % shape)
                            pm.editRenderLayerAdjustment("%s.rsSelfShadows" % shape)
                            pm.editRenderLayerAdjustment(
                                "%s.visibilityMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0])
                        if commonfunc == "on":
                            pm.setAttr(("%s.visibilityMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0]),
                                       0)
                            pm.setAttr(("%s.rsEnableVisibilityOverrides" % shape), 0)
                            print(u"{} Proxy物体自身投影已打开".format(obj)),
                        if commonfunc == "off":
                            pm.setAttr(("%s.visibilityMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0]), 1)
                            pm.setAttr(("%s.rsEnableVisibilityOverrides" % shape), 1)
                            pm.setAttr(("%s.rsShadowCaster" % shape), 0)
                            pm.setAttr(("%s.rsSelfShadows" % shape), 0)
                            print(u"{} Proxy物体自身投影已关闭".format(obj)),

                if func_op_tx == u"Proxy后台细分":
                    for shape in shapes:
                        if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                            pm.editRenderLayerAdjustment("%s.rsEnableSubdivision" % shape)
                            pm.editRenderLayerAdjustment("%s.rsEnableDisplacement" % shape)
                            pm.editRenderLayerAdjustment(
                                "%s.tessellationMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0])
                        if commonfunc == "on":
                            pm.setAttr(("%s.rsEnableSubdivision" % shape), 1)
                            pm.setAttr(("%s.rsEnableDisplacement" % shape), 1)
                            pm.setAttr(
                                ("%s.tessellationMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0]), 1)
                            print(u"{} Proxy物体后台细分已打开".format(obj)),
                        if commonfunc == "off":
                            pm.setAttr(("%s.rsEnableSubdivision" % shape), 0)
                            pm.setAttr(("%s.rsEnableDisplacement" % shape), 0)
                            pm.setAttr(
                                ("%s.tessellationMode" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0]), 0)
                            print(u"{} Proxy物体后台细分已关闭".format(obj)),

                if func_op_tx == u"Proxy高低模切换":
                    for shape in shapes:
                        proxyfile = pm.getAttr("%s.fileName" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0])
                        if commonfunc == "High Mode":
                            new_proxyFile = ("%s.rs" %  (('.').join(proxyfile.split('.')[:-1]))[:-2])
                            print new_proxyFile,
                            if os.path.exists(new_proxyFile):
                                pm.setAttr("%s.fileName" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0],
                                           new_proxyFile)
                        if commonfunc == "Low Mode":
                            new_proxyFile = ("%s_D.rs" %  ('.').join(proxyfile.split('.')[:-1]))
                            print new_proxyFile,
                            if os.path.exists(new_proxyFile):
                                pm.setAttr("%s.fileName" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0],
                                           new_proxyFile)

                if func_op_tx == u"Proxy氛围模型切换":
                    for shape in shapes:
                        proxyfile = pm.getAttr("%s.fileName" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0])
                        if commonfunc == u"白天":
                            if re.compile("_night*.rs").findall(proxyfile) is not None:
                                new_proxyFile = re.sub("_night", "", proxyfile)
                                print new_proxyFile,
                                if os.path.exists(new_proxyFile):
                                    pm.setAttr("%s.fileName" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0],
                                               new_proxyFile)
                        if commonfunc == u"晚上":
                            if re.compile("_D.rs").findall(proxyfile):
                                new_proxyFile = re.sub("_D","_night_D",proxyfile)
                                print  u"转为低模晚上：",new_proxyFile,
                                if os.path.exists(new_proxyFile):
                                    pm.setAttr("%s.fileName" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0],
                                               new_proxyFile)
                            else:
                                new_proxyFile = ("%s_night.rs" %  ('.').join(proxyfile.split('.')[:-1]))
                                print u"转为高模晚上：",new_proxyFile,
                                if os.path.exists(new_proxyFile):
                                    pm.setAttr("%s.fileName" % shape.listConnections(s=True, t="RedshiftProxyMesh")[0],
                                               new_proxyFile)


            #常用物体属性部分
            if functx == u"物体":
                if func_op_tx == u"物体遮罩":
                    for shape in shapes:
                        if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                            pm.editRenderLayerAdjustment("%s.rsMatteEnable" % shape)
                            pm.editRenderLayerAdjustment("%s.rsMatteAlpha" % shape)
                        if commonfunc == "on":
                            pm.setAttr(("%s.rsMatteEnable" % shape),1)
                            pm.setAttr(("%s.rsMatteAlpha" % shape), 0)
                            print(u"{} 物体遮罩已打开".format(obj)),
                        if commonfunc == "off":
                            pm.setAttr(("%s.rsMatteEnable" % shape),0)
                            pm.setAttr(("%s.rsMatteAlpha" % shape), 1)
                            print(u"{} 物体遮罩已关闭".format(obj)),
                if func_op_tx == u"物体细分":
                    for shape in shapes:
                        if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                            pm.editRenderLayerAdjustment("%s.rsEnableSubdivision" % shape)
                        if commonfunc == "on":
                            pm.setAttr(("%s.rsEnableSubdivision" % shape),1)
                            print(u"{} 物体细分已打开".format(obj)),
                        if commonfunc == "off":
                            pm.setAttr(("%s.rsEnableSubdivision" % shape),0)
                            print(u"{} 物体细分已关闭".format(obj)),
                if func_op_tx == u"物体置换":
                    for shape in shapes:
                        if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                            pm.editRenderLayerAdjustment("%s.rsEnableDisplacement" % shape)
                        if commonfunc == "on":
                            pm.setAttr(("%s.rsEnableDisplacement" % shape),1)
                            print (u"{} 物体置换已打开".format(obj)),
                        if commonfunc == "off":
                            pm.setAttr(("%s.rsEnableDisplacement" % shape),0)
                            print (u"%s 物体置换已关闭" % obj),

            #灯光连接部分
            if functx == u"灯光":
                if func_op_tx == u"灯光连接":
                    if pm.nodeType(shapes[0]) in light_shape_type :
                        lights.append(obj)
                    else :
                        objects.append(obj)
                    if commonfunc == "Make Link" :
                        pm.lightlink(m=True, l=lights, o=objects)
                        print(u"{} 已创建连接".format(obj)),
                    if commonfunc == "Break Link" :
                        pm.lightlink(b=True, l=lights, o=objects)
                        print(u"{} 已断开连接".format(obj)),

    # maya自带属性布局
    def mayadefault_funcAtti_control(self):
        pattern = "[A-Z]"
        self.own_attri_ScroLay = cmds.scrollLayout('ownAttri_scrolay',p='attri_tablay',h=250,cr=True)

        renderstats = ["castsShadows", "receiveShadows", "holdOut", "motionBlur", "primaryVisibility", "smoothShading",
                       "visibleInReflections", "visibleInRefractions", "doubleSided", "opposite"]

        for i in renderstats:
            new_string = re.sub(pattern, lambda x: " " + x.group(0), i)
            new_string = "{}{}".format(new_string[0].upper(),new_string[1:])
            self.own_rowlay = cmds.rowLayout(("own_rowlay_%s" %(i)),
                                             p='ownAttri_scrolay',
                                             bgc=[0.2,0.2,0.2],
                                             nc=3,
                                             cw=[[2, 100], [3, 100]],
                                             adj=1)
            self.own_tx = cmds.text(("own_tx_%s" %(i)),
                                    p=("own_rowlay_%s" %(i)),
                                    l=new_string,
                                    fn='fixedWidthFont',
                                    bgc=[0.3,0.3,0.3])
            self.own_on_btn = cmds.button(("own_on_btn_%s" %(i)),
                                          p=("own_rowlay_%s" %(i)),
                                          l="on",
                                          w=70,
                                          c=partial(self.mayadefault_funcattri,i,"on"))#partial(mayadefault_funcattri,i,"on"))
            self.own_off_btn = cmds.button(("own_off_btn_%s" %(i)),
                                          p=("own_rowlay_%s" %(i)),
                                          l="off",
                                          w=70,
                                          c=partial(self.mayadefault_funcattri,i,"off"))#partial(mayadefault_funcattri,i,"off"))
        self.own_restore_formlay = cmds.formLayout("own_restore_formlay",
                                                 p="ownAttri_scrolay",
                                                 bgc=[0.2,0.2,0.2],
                                                 nd=100)
        self.own_restore_tx = cmds.text("own_restore_tx",
                                        p="own_restore_formlay",
                                        bgc=[0.3,0.3,0.3],
                                        l="Restore All Setting",
                                        fn='fixedWidthFont')
        self.own_restore_btn = cmds.button("own_restore_btn",
                                           p="own_restore_formlay",
                                           l="Reset All",
                                           bgc=[0.1,0.1,0.1],
                                           c=partial(self.mayadefault_funcattri,"Restore All Setting","All"))
        cmds.formLayout(self.own_restore_formlay, e=1, af=[[self.own_restore_tx, 'top', 6], [self.own_restore_btn, 'top', 2]],
                        ap=[[self.own_restore_tx, 'left', 0, 2], [self.own_restore_tx, 'right', 1, 49], [self.own_restore_btn, 'left', 1, 50],
                            [self.own_restore_btn, 'right', 0, 98]])

    # maya自带属性调用
    def mayadefault_funcattri(self,stats,own_on_off,*args):
        select_obj = pm.ls(sl=True,dag=True,fl=True,s=True)
        renderstats = ["castsShadows", "receiveShadows", "holdOut", "motionBlur", "primaryVisibility", "smoothShading",
                       "visibleInReflections", "visibleInRefractions", "doubleSided", "opposite"]
        restore_value = [1,1,0,1,1,1,1,1,1,1]
        for i in range(len(renderstats)):
            if stats == renderstats[i]:
                for obj in select_obj:
                    if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                        pm.editRenderLayerAdjustment("{}.{}".format(obj,renderstats[i]))
                    if own_on_off == "on":
                        pm.setAttr("{}.{}".format(obj,renderstats[i]), 1)
                        print (u"{}.{} 已开启".format(obj,renderstats[i])),
                    if own_on_off == "off":
                        pm.setAttr("{}.{}".format(obj, renderstats[i]), 0)
                        print(u"{}.{} 已关闭".format(obj, renderstats[i])),
        if stats == "Restore All Setting":
            if own_on_off == "All":
                for obj in select_obj:
                    for attri in range(len(renderstats)):
                        pm.setAttr("{}.{}".format(obj, renderstats[attri]), restore_value[attri])
                        print (u"{} 参数已重置完毕".format(obj)),

    # rs属性布局
    def rscommon_funcattri_control(self):
        self.rscommon_attri_ScroLay = cmds.scrollLayout('rscommon_scrolay',p='attri_tablay',h=250,cr=True)
        rs_opt_attri = ["Redshift Visibility Overrides=rsEnableVisibilityOverrides",
                        "Primary Ray Visible=rsPrimaryRayVisible",
                        "Secondary Ray Visible=rsSecondaryRayVisible",
                        "Casts Shadow=rsShadowCaster",
                        "Receives Shadow=rsShadowReceiver",
                        "Self-Shadows=rsSelfShadows",
                        "Caster AO=rsAOCaster",
                        "Reflection In Visible=rsReflectionVisible",
                        "Refraction In Visible=rsRefractionVisible",
                        "Casts Reflection=rsReflectionCaster",
                        "Casts Refraction=rsRefractionCaster",
                        "Visible to Non-Photon GI=rsFgVisible",
                        "Visible to GI Photons=rsGiVisible",
                        "Visible to Caustic Photons=rsCausticVisible",
                        "Receives GI=rsFgCaster",
                        "Force Brute-Force GI=rsForceBruteForceGI",
                        "Casts GI Photons=rsGiCaster",
                        "Casts Caustic Photons=rsCausticCaster",
                        "Receives GI Photons=rsGiReceiver",
                        "Receives Caustic Photons=rsCausticReceiver"]

        for i in range(len(rs_opt_attri)):
            name, value = rs_opt_attri[i].split("=")
            self.rs_rowlay = cmds.rowLayout(("rs_rowlay_%s" % (value)),
                                             p='rscommon_scrolay',
                                             bgc=[0.2, 0.2, 0.2],
                                             nc=3,
                                             cw=[[2, 100], [3, 100]],
                                             adj=1)
            self.rs_tx = cmds.text(("rs_tx_%s" % (value)),
                                    p=("rs_rowlay_%s" % (value)),
                                    l=name,
                                    fn='fixedWidthFont',
                                    bgc=[0.3, 0.3, 0.3])
            self.rs_on_btn = cmds.button(("rs_on_btn_%s" % (value)),
                                          p=("rs_rowlay_%s" % (value)),
                                          l="on",
                                          w=70,
                                          c=partial(self.rscommon_funcattri, name,"on"))
            self.rs_off_btn = cmds.button(("rs_off_btn_%s" % (value)),
                                           p=("rs_rowlay_%s" % (value)),
                                           l="off",
                                           w=70,
                                           c=partial(self.rscommon_funcattri, name,"off"))
        self.rs_restore_formlay = cmds.formLayout("rs_restore_formlay",
                                                 p="rscommon_scrolay",
                                                 bgc=[0.2,0.2,0.2],
                                                 nd=100)
        self.rs_restore_tx = cmds.text("rs_restore_tx",
                                        p="rs_restore_formlay",
                                        bgc=[0.3,0.3,0.3],
                                        l="Restore All Setting",
                                        fn='fixedWidthFont')
        self.rs_restore_btn = cmds.button("rs_restore_btn",
                                           p="rs_restore_formlay",
                                           l="Reset All",
                                           bgc=[0.1,0.1,0.1],
                                           c=partial(self.rscommon_funcattri,"Restore All Setting","All"))
        cmds.formLayout(self.rs_restore_formlay, e=1, af=[[self.rs_restore_tx, 'top', 6], [self.rs_restore_btn, 'top', 2]],
                        ap=[[self.rs_restore_tx, 'left', 0, 2], [self.rs_restore_tx, 'right', 1, 49], [self.rs_restore_btn, 'left', 1, 50],
                            [self.rs_restore_btn, 'right', 0, 98]])

    # rs属性参数调用
    def rscommon_funcattri(self,rsname,rs_on_off,*args):

        select_obj = pm.ls(sl=True, dag=True, fl=True, s=True)

        rs_opt_attri = ["Redshift Visibility Overrides=rsEnableVisibilityOverrides",
                        "Primary Ray Visible=rsPrimaryRayVisible",
                        "Secondary Ray Visible=rsSecondaryRayVisible",
                        "Casts Shadow=rsShadowCaster",
                        "Receives Shadow=rsShadowReceiver",
                        "Self-Shadows=rsSelfShadows",
                        "Caster AO=rsAOCaster",
                        "Reflection In Visible=rsReflectionVisible",
                        "Refraction In Visible=rsRefractionVisible",
                        "Casts Reflection=rsReflectionCaster",
                        "Casts Refraction=rsRefractionCaster",
                        "Visible to Non-Photon GI=rsFgVisible",
                        "Visible to GI Photons=rsGiVisible",
                        "Visible to Caustic Photons=rsCausticVisible",
                        "Receives GI=rsFgCaster",
                        "Force Brute-Force GI=rsForceBruteForceGI",
                        "Casts GI Photons=rsGiCaster",
                        "Casts Caustic Photons=rsCausticCaster",
                        "Receives GI Photons=rsGiReceiver",
                        "Receives Caustic Photons=rsCausticReceiver"]
        rs_default_v = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1]
        for i in range(len(rs_opt_attri)):
            name, value = rs_opt_attri[i].split("=")
            if rsname == name:
                for obj in select_obj:
                    if cmds.editRenderLayerGlobals(q=True, crl=True) != "defaultRenderLayer":
                        pm.editRenderLayerAdjustment("{}.{}".format(obj, value))
                    if rs_on_off == "on":
                        pm.setAttr("{}.{}".format(obj, value), 1)
                        print(u"{}.{} 已开启".format(obj, value)),
                    if rs_on_off == "off":
                        pm.setAttr("{}.{}".format(obj, value), 0)
                        print(u"{}.{} 已关闭".format(obj, value)),
        if rsname == "Restore All Setting":
            if rs_on_off == "All":
                for obj in select_obj:
                    for attri in range(len(rs_opt_attri)):
                        name, value = rs_opt_attri[attri].split("=")
                        pm.setAttr("{}.{}".format(obj, value), rs_default_v[attri])
                        print (u"{} redshift参数已重置完毕".format(obj)),

    def objID_lay(self):
        cmds.objID_Form = cmds.frameLayout('objID_framelay',p='mainparameter_formlay',cll=True,l=u'Object ID设置',fn='fixedWidthFont')
    def renderlayer_lay(self):
        self.renderlay_Form = cmds.frameLayout('renderlayer_framelay',p='mainparameter_formlay',cll=True,l=u'渲染层',fn='fixedWidthFont',mh=5)
    def im_light_lay(self):
        self.imLight_Form = cmds.frameLayout('importlight_framelay',p='mainparameter_formlay',cll=True,l=u'灯光导入',la='center',fn='fixedWidthFont',mh=5)
        cmds.textFieldButtonGrp('lig_filepath',adj=2,l='Light File Path',bl='<<<',cal=[1,"left"],cw=[1,80],bc=partial(self.create_lig_btn))
        cmds.scrollLayout('lig_colLay',p='importlight_framelay',h=500,cr=True)
        
    def get_light_file(self):
        dir_choose = cmds.fileDialog2(dialogStyle=1, fileMode=3)[0]
        if dir_choose:
            list_files = []    
            for root, dirs, files in os.walk(dir_choose):
                for f in files:
                    list_files.append(os.path.join(root, f).replace("\\","/"))
            
           
            list_files = list(filter(self.file_filter, list_files))
            
            if list_files:
                cmds.textFieldButtonGrp('lig_filepath',e=True,tx=dir_choose)
            else:
                cmds.confirmDialog( title=u'Warning', message='No Maya file in the path!!!', button=['Yes'], defaultButton='Yes' )

            list_files = self.file_array(list_files)
            print (list_files)
            
            return list_files 
        
    def file_array(self,m_args):
        for m_f in range(len(m_args)):
            m_args[m_f] = [os.path.basename(os.path.splitext(m_args[m_f])[0]),m_args[m_f]]
      
        return m_args
            
    def file_filter(self,file_name):
        mayaFilters = ['.ma','.mb','.MA','.MB']
        fbxFilters = ['.fbx','.FBX']
        if file_name[-3:] in mayaFilters or file_name[-4:] in fbxFilters :
            return True
        else:
            return False 
            
    def create_lig_btn(self):
        lightfile_args = self.get_light_file()
        for lig,ligpath in lightfile_args:
            ext = os.path.splitext(ligpath)[1]
            if ext == ".ma":
                ext_type = "mayaAscii"
            else:
                ext_type = "MayaBinary"
            openfilecommand = 'cmds.file(\"%s\",f=True,op=\"v=0;\",iv=True,typ=\"%s\",o=True)'% (ligpath,ext_type)
            importfileconnamn = 'cmds.file(\"%s\",f=True,op=\"v=0;\",iv=True,typ=\"%s\",ra=True,mnc=True,ns=\":\",pr=True,i=True)'% (ligpath,ext_type)
            referencefilecommand = 'cmds.file(\"%s\",f=True,op=\"v=0;\",iv=True,typ=\"%s\",r=True,gl=True,mnc=False,ns=\"%s\")'% (ligpath,ext_type,lig)
            cmds.button(("%s_btn" % lig),p='lig_colLay',l=str(lig),c=('mel.eval("print \\"The File Is %s \\\\n\\";")' % lig))
            cmds.popupMenu(p=("%s_btn" % lig),b=3)
            cmds.menuItem(l=('Open %s'% lig),c = openfilecommand,ann = openfilecommand)
            cmds.menuItem(l=('Import %s'% lig),c=importfileconnamn,ann=importfileconnamn)
            cmds.menuItem(l=('Reference %s'% lig),c = referencefilecommand,ann = referencefilecommand)
            cmds.separator(("%s_sep" % lig),p='lig_colLay',st="shelf")

if __name__ == '__main__':
    lightTool = lightTool()
    lightTool.createWin()