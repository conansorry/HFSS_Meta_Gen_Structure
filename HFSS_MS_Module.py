import HFSS_Script



def gen_A_cross(H = HFSS_Script.HFSS, l1 = float, l2= float, w = float, theta= float, t=0.2):
    H.create_box(str(-l1 / 2.0) + 'mm', str(-w / 2.0) + 'mm', '0mm',
                    str(l1) + "mm", str(w) + "mm", str(t) + 'mm',
                    "L1", 'pec')
    H.create_box(str(-w / 2.0) + 'mm', str(-l2 / 2.0) + 'mm', '0mm',
                    str(w) + "mm", str(l2) + "mm", str(t) + 'mm',
                    "L2", 'pec')

    H.unite("L1", "L2")
    if (theta != 0):   H.rotation("L1", theta)

def gen_B_Square_with_Cap(H = HFSS_Script.HFSS, l1 = float, l2= float, w = float, theta= float, t=0.2):
    H.create_box(str(-l1 / 2.0) + 'mm', str(-l1 / 2.0) + 'mm', '0mm',
                    str(l1) + "mm", str(l1) + "mm", str(t) + 'mm',
                    "L1_o", 'pec')

    H.create_box(str(-l1 / 2.0 + 0.5 * w) + 'mm', str(-l1 / 2.0 + 0.5 * w) + 'mm', '0mm',
                    str(l1 - w) + "mm", str(l1 - w) + "mm", str(t) + 'mm',
                    "L1_i", 'pec')

    H.subtract("L1_o", "L1_i")

    H.create_box(str(-l1 / 2.0) + 'mm', str(-0.5 * w) + 'mm', '0mm',
                    str(l1 / 2.0 - 0.5 * l2) + "mm", str(w) + "mm", str(t) + 'mm',
                    "L2_x", 'pec')

    H.create_box(str(-l1 / 2.0 - w) + 'mm', str(-0.75) + 'mm', '0mm',
                    str(w) + "mm", str(1.5) + "mm", str(t) + 'mm',
                    "L2_y", 'pec')

    H.unite("L2_x", "L2_y")

    H.duplicate_mirror("L2_x", 'yz')

    H.unite("L1_o", "L2_x")
    H.unite("L1_o", "L2_x_1")
    if (theta != 0):   H.rotation("L1_o", theta)



def gen_C_Cir_Arm(H = HFSS_Script.HFSS, l1 = float, l2= float, w = float, theta= float, t=0.2):
    H.create_cylinder('0.0mm',  '0.0mm', '0.0mm',
                 str(0.5*l1) + "mm", str(t) + 'mm',
                 "L1_o", 'pec')

    H.create_cylinder('0.0mm', '0.0mm', '0.0mm',
                      str(0.5*l1 - w) + "mm", str(t) + 'mm',
                      "L1_o", 'pec')

    H.subtract("L1_o", "L1_i")

    H.create_box(str(-l1 / 2.0) + 'mm', str(-0.5 * l2) + 'mm', '0mm',
                 str(l1) + "mm", str(l2) + "mm", str(t) + 'mm',
                 "L2_x", 'pec')
    H.subtract("L1_o", "L2_x")

    H.create_box(str(-0.5*w) + 'mm', str(-l1 / 2.0 + 0.5* w ) + 'mm', '0mm',
                 str(w) + "mm", str(l1 - w ) + "mm", str(t) + 'mm',
                 "arm", 'pec')

    H.unite("L1_o", "arm")
    if (theta != 0):   H.rotation("L1_o", theta)

def gen_D_Cir_No_Cross(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2):

    H.create_cylinder('0.0mm', '0.0mm', '0.0mm',
                      str(4.0) + "mm", str(t) + 'mm',
                      "Cir", 'pec')

    H.create_box(str(-l1 / 2.0) + 'mm', str(-w / 2.0) + 'mm', '0mm',
                 str(l1) + "mm", str(w) + "mm", str(t) + 'mm',
                 "L1", 'pec')
    H.create_box(str(-w / 2.0) + 'mm', str(-l2 / 2.0) + 'mm', '0mm',
                 str(w) + "mm", str(l2) + "mm", str(t) + 'mm',
                 "L2", 'pec')

    H.subtract("Cir", "L1")
    H.subtract("Cir", "L2")
    if (theta != 0):   H.rotation("Cir", theta)


def gen_E_Cir_No_Arm(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2):

    H.create_cylinder('0.0mm', '0.0mm', '0.0mm',
                      str(l1*0.5) + "mm", str(t) + 'mm',
                      "Cir", 'pec')

    H.create_box(str(-l1 *0.5) + 'mm', str(-l2 / 2.0) + 'mm', '0mm',
                 str(l1) + "mm", str(l2) + "mm", str(t) + 'mm',
                 "L1L2", 'pec')

    H.subtract("Cir", "L1L2")
    if (theta != 0):   H.rotation("Cir", theta)

def gen_F_H_Shape(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2):


    H.create_box(str(-l2 *0.5) + 'mm', str(-l1 *0.5) + 'mm', '0mm',
                 str(w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 "L1_1", 'pec')

    H.create_box(str(l2 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(-w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 "L1_2", 'pec')

    H.create_box(str(-l2 * 0.5) + 'mm', str(-w * 0.5) + 'mm', '0mm',
                 str(l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 "L2", 'pec')

    H.unite("L2", "L1_1")
    H.unite("L2", "L1_2")
    if (theta != 0):   H.rotation("L2", theta)

def gen_G_H_Shape(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2):


    H.create_box(str(-l1 *0.5) + 'mm', str(-l1 *0.5) + 'mm', '0mm',
                 str(w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 "L1_1", 'pec')

    H.create_box(str(l1 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(-w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 "L1_2", 'pec')

    H.create_box(str(-l2 * 0.5) + 'mm', str(-w * 0.5) + 'mm', '0mm',
                 str(l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 "L2", 'pec')

    H.unite("L1", "L1_1")
    H.unite("L1", "L1_2")

    H.create_box(str(-l2 / 2.0) + 'mm', str(-w*0.5) + 'mm', '0mm',
                 str(-l2 / 2.0 - 0.5 * 0.5) + "mm", str(w) + "mm", str(t) + 'mm',
                 "L2_x", 'pec')

    H.create_box(str(- 0.5 * 0.5) + 'mm', str(-0.75) + 'mm', '0mm',
                 str(-w) + "mm", str(1.5) + "mm", str(t) + 'mm',
                 "L2_y", 'pec')

    H.unite("L1", "L2_z")
    H.unite("L1", "L2_y")

    H.duplicate_mirror("L1", 'xz')
    H.unite("L1", "L1_1")
    if (theta != 0):   H.rotation("L1", theta)

def gen_H_Half_H(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2):
    H.create_box(str(-l2 *0.5) + 'mm', str(-l1 *0.5) + 'mm', '0mm',
                 str(w) + "mm", str(l1) + "mm", str(t) + 'mm',
                 "L1", 'pec')

    H.create_box(str(-l2 * 0.5) + 'mm', str(-l1 * 0.5) + 'mm', '0mm',
                 str(l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 "L1_1", 'pec')

    H.create_box(str(l2 * 0.5) + 'mm', str(-0.25) + 'mm', '0mm',
                 str(-w) + "mm", str(-0.5*l2+0.25) + "mm", str(t) + 'mm',
                 "L1_2", 'pec')

    H.unite("L", "L1_1")
    H.unite("L", "L1_2")
    H.duplicate_mirror("L", 'xz')
    H.unite("L", "L_1")
    if( theta != 0 ):   H.rotation("L", theta)


def gen_I_Two_Arm(H=HFSS_Script.HFSS, l1=float, l2=float, w=float, theta=float, t=0.2):
    H.create_box(str(-w*0.5) + 'mm', str(-w / 2.0) + 'mm', '0mm',
                 str(l1) + "mm", str(w) + "mm", str(t) + 'mm',
                 "L1", 'pec')
    H.create_box(str(-w*0.5) + 'mm', str(-w / 2.0) + 'mm', '0mm',
                 str(l2) + "mm", str(w) + "mm", str(t) + 'mm',
                 "L2", 'pec')

    H.rotation("L2", theta)
    H.unite("L1", "L2")














