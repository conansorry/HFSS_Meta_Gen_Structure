import HFSS_Script
import math
import numpy as np

def gen_A_cross(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre ="" ):
    H.create_box(str(-l1 / 2.0) + 'mm', str(-w / 2.0) + 'mm', '0mm',
                 str(l1) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre+"aL1", _mat='pec')
    H.create_box(str(-w / 2.0) + 'mm', str(-l2 / 2.0) + 'mm', '0mm',
                 str(w) + "mm", str(l2) + "mm", str(t) + 'mm',
                 _pre+"aL2", _mat='pec')

    H.unite(_pre+"aL1", _pre+"aL2")
    if (theta != 0):   H.rotation(_pre+"aL1", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"aL1", 0,0, str(shift_z)+"mm")


def gen_B_Square_with_Cap(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_box(str(-l1 / 2.0) + 'mm', str(-l1 / 2.0) + 'mm', '0mm',
                 str(l1) + "mm", str(l1) + "mm", str(t) + 'mm',
                 _pre+"bL1_o", _mat='pec')

    H.create_box(str(-l1 / 2.0 +  w) + 'mm', str(-l1 / 2.0 +  w) + 'mm', '0mm',
                 str(l1 - 2*w) + "mm", str(l1 - 2*w) + "mm", str(t) + 'mm',
                 _pre+"bL1_i", _mat='pec')

    H.subtract(_pre+"bL1_o", _pre+"bL1_i")

    H.create_box(str(-l1 * 0.5) + 'mm', str(-0.5 * w) + 'mm', '0mm',
                 str(l1 / 2.0 - 0.5 * l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre+"bL2_x", _mat='pec')

    H.create_box(str(-l2 / 2.0 ) + 'mm', str(-0.75) + 'mm', '0mm',
                 str(-w) + "mm", str(1.5) + "mm", str(t) + 'mm',
                 _pre+"bL2_y", _mat='pec')

    H.unite(_pre+"bL2_x", _pre+"bL2_y")

    H.duplicate_mirror(_pre+"bL2_x", 'yz')

    H.unite(_pre+"bL1_o", _pre+"bL2_x")
    H.unite(_pre+"bL1_o", _pre+"bL2_x_1")
    if (theta != 0):   H.rotation(_pre+"bL1_o", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"bL1_o", 0, 0, str(shift_z) + "mm")

def gen_C_Cir_Arm(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_cylinder('0.0mm', '0.0mm', '0.0mm',
                      str(0.5 * l1) + "mm", str(t) + 'mm',
                      _pre+"cL1_o", _mat='pec')

    H.create_cylinder('0.0mm', '0.0mm', '0.0mm',
                      str(0.5 * l1 - w) + "mm", str(t) + 'mm',
                      _pre+"cL1_i", _mat='pec')

    H.subtract(_pre+"cL1_o", _pre+"cL1_i")

    H.create_box(str(-l1 / 2.0) + 'mm', str(-0.5 * l2) + 'mm', '0mm',
                 str(l1) + "mm", str(l2) + "mm", str(t) + 'mm',
                 _pre+"cL2_x", _mat='pec')
    H.subtract(_pre+"cL1_o", _pre+"cL2_x")

    H.create_box(str(-0.5 * w) + 'mm', str(-l1 / 2.0 + 0.5 * w) + 'mm', '0mm',
                 str(w) + "mm", str(l1 - w) + "mm", str(t) + 'mm',
                 _pre+"carm", _mat='pec')

    H.unite(_pre+"cL1_o", _pre+"carm")
    if (theta != 0):   H.rotation(_pre+"cL1_o", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"cL1_o", 0, 0, str(shift_z) + "mm")

def gen_D_Cir_No_Cross(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_cylinder('0.0mm', '0.0mm', '0.0mm',
                      str(4.0) + "mm", str(t) + 'mm',
                      _pre+"dCir", _mat='pec')

    H.create_box(str(-l1 / 2.0) + 'mm', str(-w / 2.0) + 'mm', '0mm',
                 str(l1) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre+"dL1", _mat='pec')
    H.create_box(str(-w / 2.0) + 'mm', str(-l2 / 2.0) + 'mm', '0mm',
                 str(w) + "mm", str(l2) + "mm", str(t) + 'mm',
                 _pre+"dL2", _mat='pec')

    H.subtract(_pre+"dCir", _pre+"dL1")
    H.subtract(_pre+"dCir", _pre+"dL2")
    if (theta != 0):   H.rotation(_pre+"dCir", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"dCir", 0, 0, str(shift_z) + "mm")


def gen_E_Cir_No_Arm(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_cylinder('0.0mm', '0.0mm', '0.0mm',
                      str(l1 * 0.5) + "mm", str(t) + 'mm',
                      _pre+"eCir", _mat='pec')

    H.create_box(str(-l1 * 0.5) + 'mm', str(-l2 / 2.0) + 'mm', '0mm',
                 str(l1) + "mm", str(l2) + "mm", str(t) + 'mm',
                 _pre+"eL1L2", _mat='pec')

    H.subtract(_pre+"eCir", _pre+"eL1L2")
    if (theta != 0):   H.rotation(_pre+"eCir", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"eCir", 0, 0, str(shift_z) + "mm")


def gen_F_H_Shape(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_box(str(-l2 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 _pre+"fL1_1", _mat='pec')

    H.create_box(str(l2 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(-w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 _pre+"fL1_2", _mat='pec')

    H.create_box(str(-l2 * 0.5) + 'mm', str(-w * 0.5) + 'mm', '0mm',
                 str(l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre+"fL2", _mat='pec')

    H.unite(_pre+"fL2", _pre+"fL1_1")
    H.unite(_pre+"fL2", _pre+"fL1_2")
    if (theta != 0):   H.rotation(_pre+"fL2", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"fL2", 0, 0, str(shift_z) + "mm")


def gen_G_H_Shape(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_box(str(-l2 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 _pre+"gL1_1", _mat='pec')

    H.create_box(str(l2 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(-w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 _pre+"gL1_2", _mat='pec')

    H.create_box(str(-l2 * 0.5) + 'mm', str(-w * 0.5) + 'mm', '0mm',
                 str(l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre+"gL1", _mat='pec')

    H.unite(_pre+"gL1", _pre+"gL1_1")
    H.unite(_pre+"gL1", _pre+"gL1_2")

    H.create_box(str(-l2 / 2.0) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(l2 / 2.0 - 0.5 * 0.5) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre+"gL2_x", _mat='pec')

    H.create_box(str(- 0.5 * 0.5) + 'mm', str(-l1 * 0.5-0.5) + 'mm', '0mm',
                 str(-w) + "mm", str(1.5) + "mm", str(t) + 'mm',
                 _pre+"gL2_y", _mat='pec')

    H.unite(_pre+"gL2_x", _pre+"gL2_y")


    H.duplicate_mirror(_pre+"gL2_x", 'yz')
    H.unite(_pre+"gL1", _pre+"gL2_x")
    H.unite(_pre+"gL1",_pre+ "gL2_x_1")
    H.duplicate_mirror(_pre+"gL1", 'xz')
    H.unite(_pre+"gL1", _pre+"gL1_3")
    if (theta != 0):   H.rotation(_pre+"gL1", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"gL1", 0, 0, str(shift_z) + "mm")


def gen_H_Half_H(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_box(str(-l2 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 _pre+"hL", _mat='pec')

    H.create_box(str(-l2 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre + "hL1_1", _mat='pec')

    H.create_box(str(l2 * 0.5) + 'mm', str(-0.25) + 'mm', '0mm',
                 str(-w) + "mm", str(-0.5 * l1 + 0.25) + "mm", str(t) + 'mm',
                 _pre+"hL1_2", _mat='pec')

    H.create_box(str(l2 * 0.5-w) + 'mm', str(-0.25) + 'mm', '0mm',
                 str(-1.0) + "mm", str(-0.5) + "mm", str(t) + 'mm',
                 _pre+"hL1_3", _mat='pec')

    H.unite(_pre+"hL", _pre+"hL1_1")
    H.unite(_pre+"hL", _pre+"hL1_2")
    H.unite(_pre+"hL", _pre+"hL1_3")
    H.duplicate_mirror(_pre+"hL", _pre+'hxz')
    H.unite(_pre+"hL", _pre+"hL_1")
    if (theta != 0):   H.rotation(_pre+"hL", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"hL", 0, 0, str(shift_z) + "mm")


def gen_I_Two_Arm(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_box(str(-w * 0.5) + 'mm', str(-w / 2.0) + 'mm', '0mm',
                 str(l1) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre+"iL1", 'pec')
    H.create_box(str(-w * 0.5) + 'mm', str(-w / 2.0) + 'mm', '0mm',
                 str(l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 _pre + "iL2", _mat='pec')

    if (theta != 0): H.rotation(_pre+"iL2", theta)
    H.unite(_pre+"iL1", _pre+"iL2")
    if (abs(shift_z) > 0.0):    H.move(_pre+"iL1", 0, 0, str(shift_z) + "mm")

    # shift_y = -l1 * math.sin(theta*np.pi/180.0)*0.5
    # H.move("L1", str(-l1 * 0.5)+"mm", str(shift_y)+"mm", "0.0mm")


def gen_J_Ellips(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_Ellips(str(0.5*l1) + "mm", str(min(l2/l1, l1/l2)), t, _pre+"jEllip", _mat='pec')
    if (theta != 0): H.rotation(_pre+"jEllip", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"jEllip", 0, 0, str(shift_z) + "mm")


def gen_K_Squre(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_box(str(-l1 * 0.5) + 'mm', str(-l2 * 0.5) + 'mm', '0mm',
                 str(l1) + "mm", str(l2) + "mm", str(t) + 'mm',
                 _pre+"kL1", _mat='pec')

    if (theta != 0): H.rotation(_pre+"kL1", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"kL1", 0, 0, str(shift_z) + "mm")


def gen_L_Empty_Squre(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2, shift_z = 0.0 , _pre =""):
    H.create_box(str(-l1 * 0.5) + 'mm', str(-l2 * 0.5) + 'mm', '0mm',
                 str(l1) + "mm", str(l2) + "mm", str(t) + 'mm',
                 _pre+"lL1", _mat='pec')

    H.create_box(str(-l1 * 0.5 + w) + 'mm', str(-l2 * 0.5 +  w) + 'mm', '0mm',
                 str(l1 - 2*w) + "mm", str(l2 - 2*w) + "mm", str(t) + 'mm',
                 _pre+"lL2", _mat='pec')
    H.subtract(_pre+"lL1", _pre+"lL2")
    if (theta != 0): H.rotation(_pre+"lL1", theta)
    if (abs(shift_z) > 0.0):    H.move(_pre+"lL1", 0, 0, str(shift_z) + "mm")
