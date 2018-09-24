import maya.cmds as mc
import maya.mel as mel

class CarRig(object):
    def __init__(self):
        self.RR = []
        self.RL = []
        self.FR = []
        self.FL = []
        self.centroid = [0, 0, 0]
        self.car_name = 'hoge'

    def adjustCentroid(self, *args):
        self.RR = [mc.getAttr('tire_rearR.translateX'), mc.getAttr('tire_rearR.translateY'), mc.getAttr('tire_rearR.translateZ')]
        self.RL = [mc.getAttr('tire_rearL.translateX'), mc.getAttr('tire_rearL.translateY'), mc.getAttr('tire_rearL.translateZ')]
        self.FR = [mc.getAttr('tire_frontR.translateX'), mc.getAttr('tire_frontR.translateY'), mc.getAttr('tire_frontR.translateZ')]
        self.FL = [mc.getAttr('tire_frontL.translateX'), mc.getAttr('tire_frontL.translateY'), mc.getAttr('tire_frontL.translateZ')]

        self.centroid[1] = (self.RR[1] + self.RL[1] + self.FR[1]+ self.FL[1]) / 4
        self.centroid[2] = (self.RR[2] + self.RL[2] + self.FR[2]+ self.FL[2]) / 4

        mc.setAttr('centroid.translateX', self.centroid[0])
        mc.setAttr('centroid.translateY', self.centroid[1])
        mc.setAttr('centroid.translateZ', self.centroid[2])

    def adjustBody(self, *args):
        mc.setAttr('body_ctrl_null.translateY', mc.getAttr('height.translateY'))
        mc.setAttr('body_ctrl_null.translateZ', self.centroid[2])

        mc.setAttr('bodyGP_null.translateY', self.centroid[1])
        mc.setAttr('bodyGP_null.translateZ', self.centroid[2])

    def addAllCtrl(self, *args):
        mc.setAttr('typeMesh1.rotateX', -90)
        mc.select('typeMesh1')
        mel.eval("convertTypeCapsToCurves;")
        curve_list = mc.listRelatives(type='transform')
        for i in range(len(curve_list)):
            curve_list[i] = curve_list[i].replace('Curve', 'CurveShape')
            mc.setAttr('%s.overrideEnabled' %(curve_list[i]), 1)
            mc.setAttr('%s.overrideColor' %(curve_list[i]), 17)

        mc.createNode('transform', n='all_ctrl')
        mc.select(curve_list)
        mc.select('all_ctrl', add=True)
        mc.parent(r=True, s=True)

    def hierarchicalOrganization(self, *args):
        mc.parent('all_ctrl', 'local')
        mc.setAttr('all_ctrl.translateX', 0)
        mc.setAttr('all_ctrl.translateY', 0)
        mc.setAttr('all_ctrl.translateZ', 0)
        mc.parent('bodyGP_null', 'tire_rearL', 'tire_rearR', 'tire_frontL', 'tire_frontR', 'body_ctrl_null', 'all_ctrl')

    def tireRotate(self, *args):
        mc.addAttr('all_ctrl', at='float', ln='rot', k=True)
        mc.connectAttr('all_ctrl.rot', 'tire_rearL_ctrl.rotateX')
        mc.connectAttr('all_ctrl.rot', 'tire_rearR_ctrl.rotateX')
        mc.connectAttr('all_ctrl.rot', 'tire_frontL_ctrl.rotateX')
        mc.connectAttr('all_ctrl.rot', 'tire_frontR_ctrl.rotateX')

    def deleteObject(self, *args):
        mc.delete('typeMesh1', 'height', 'centroid', 'typeMesh1Curves1')

    def execution(self, *args):
        self.adjustCentroid()
        self.adjustBody()
        self.addAllCtrl()
        self.hierarchicalOrganization()
        self.tireRotate()
        self.deleteObject()


a = CarRig()
a.execution()
