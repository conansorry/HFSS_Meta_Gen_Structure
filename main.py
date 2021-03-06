import HFSS_Script as HF
import Meta_Generator as Gnr
import multiprocessing
import os.path
import shutil
import sys
import numpy as np
import HFSS_MS_Module as HS

my_path = "D:\Jiangy\GAN_Training_Data\Patterned"
# if __name__ == '__main__':
#

def gen_space( ):

    X = []
    count = 0


    theta_list = [0, 30, 45, 60, 90]
    thickness = 0.01
    w = 0.5

    # A
    l11_list = np.arange(3.0, 7.5, 0.5)
    l21_list = np.arange(3.0, 7.5, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 1.0, l1, l2, w, theta, thickness])
                count = count + 1

    # B
    l11_list = np.arange(3.0, 7.5, 0.5)
    l21_list = np.arange(0.0, 1.0, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 2.0, l1, l2, w, theta, thickness])
                count = count + 1

    # C
    l11_list = np.arange(3.0, 7.5, 0.5)
    l21_list = np.arange(0.5, 1.0, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 3.0, l1, l2, w, theta, thickness])
                count = count + 1

    # D
    l11_list = np.arange(3.0, 6.0, 0.5)
    l21_list = np.arange(3.0, 6.0, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 4.0, l1, l2, w, theta, thickness])
                count = count + 1
    # E
    l11_list = np.arange(3.0, 7.5, 0.5)
    l21_list = np.arange(0.5, 1.0, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 5.0, l1, l2, w, theta, thickness])
                count = count + 1

    # F
    l11_list = np.arange(3.0, 7.0, 0.5)
    l21_list = np.arange(3.0, 7.0, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 6.0, l1, l2, w, theta, thickness])
                count = count + 1

    # G
    l11_list = np.arange(3.0, 7.0, 0.5)
    l21_list = np.arange(3.0, 7.0, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 7.0, l1, l2, w, theta, thickness])
                count = count + 1

    # H
    l11_list = np.arange(3.0, 7.5, 0.5)
    l21_list = np.arange(3.0, 7.5, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 8.0, l1, l2, w, theta, thickness])
                count = count + 1

    # # I
    # l11_list = np.arange(3.0, 7.0, 0.5)
    # l21_list = np.arange(3.0, 7.0, 0.5)
    # for l1 in l11_list:
    #     for l2 in l21_list:
    #         for theta in theta_list:
    #             X.append([count, 9.0, l1, l2, w, theta, thickness])
    #             count = count + 1


    # J
    l11_list = np.arange(3.0, 7.5, 0.5)
    l21_list = np.arange(3.0, 7.5, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 10.0, l1, l2, w, theta, thickness])
                count = count + 1

    # k
    l11_list = np.arange(3.0, 7.5, 0.5)
    l21_list = np.arange(3.0, 7.5, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 11.0, l1, l2, w, theta, thickness])
                count = count + 1


    # L
    l11_list = np.arange(3.0, 7.5, 0.5)
    l21_list = np.arange(3.0, 7.5, 0.5)
    for l1 in l11_list:
        for l2 in l21_list:
            for theta in theta_list:
                X.append([count, 12.0, l1, l2, w, theta, thickness])
                count = count + 1

    np.savetxt(my_path + "/Property.txt", X, fmt='%.4f')
    return X




def evalue_Pattern(x, h , shift_z = 0):
    l1 = x[2]
    l2 = x[3]
    w = x[4]
    theta = x[5]
    thickness = x[6]
    func_dict = {1: HS.gen_A_cross,
                 2: HS.gen_B_Square_with_Cap,
                 3: HS.gen_C_Cir_Arm,
                 4: HS.gen_D_Cir_No_Cross,
                 5: HS.gen_E_Cir_No_Arm,
                 6: HS.gen_F_H_Shape,
                 7: HS.gen_G_H_Shape,
                 8: HS.gen_H_Half_H,
                 9: HS.gen_I_Two_Arm,
                 10: HS.gen_J_Ellips,
                 11: HS.gen_K_Squre,
                 12: HS.gen_L_Empty_Squre
                 }
    def func_None():
        print( "cannot find func")

    return func_dict.get(x[1], func_None)(h, l1, l2, w, theta, thickness, shift_z )



def auto_gen_structure(_st):
    fs = 5.0
    fe = 25.0
    f_sol = 20.0
    nfp = 101
    dim_a = 10


    if os.path.isfile(my_path + "/Property.txt"):
        X = np.loadtxt(my_path + "/Property.txt")
    else:
        X = gen_space()
    # X = gen_space()

    count = _st

    if (os.path.isdir(my_path + "/Res") == False): os.makedirs(my_path + "/Res")
    if (os.path.isdir(my_path + "/Mat") == False): os.makedirs(my_path + "/Mat")
    if (os.path.isdir(my_path + "/Fig") == False): os.makedirs(my_path + "/Fig")

    h = HF.HFSS()



    while(count<X.shape[0]):
        if (os.path.isfile(my_path + "/Res/design" + str(count) + ".txt")):
            # print("exist:",  count)
            a=1
        else:
            print("evluating:" , count)
            design_name = "design" + str(count)
            h.new_design(design_name)

            evalue_Pattern( X[count, :], h)
            h.create_box(str(-dim_a / 2.0) + "mm", str(-dim_a / 2.0) + "mm", str(-30.0 ) + "mm",
                         str(dim_a) + "mm", str(dim_a) + "mm", str(2 * 30.0) + "mm", 'Boundary')

            h.assign_mater_slave_boundary_condition('Boundary')
            h.assign_floque_port('Boundary', f_sol)

            solution_name = 's' + str(count)

            h.insert_analysis_setup_old(solution_name, f_sol, 0.02, 8)
            h.insert_frequency_swap(solution_name, fs, fe, nfp)
            h.run(solution_name)
            h.create_reports_tr_ri(solution_name, my_path +"/Res" , design_name)
            h.delete_design(design_name)

        count = count + 1


    np.savetxt(my_path + "/Property.txt", X)

def close_ANSYS():
    try:
        os.system("taskkill /F /IM ansysedt.exe")
    except:
        print("stop ansys not finished:", sys.exc_info()[0])

    try:
        # delete_path("D:\Jiangy\JY_HFSS\Ansoft")
        delete_path("D:\Jiangy\JY_HFSS\Ansoft")
    except:
        print("not delete:", sys.exc_info()[0])
        # h.save_prj()

def delete_path( rootdir ):
    filelist = os.listdir(rootdir)  # ????????????????????????????????????
    for f in filelist:
        filepath = os.path.join(rootdir, f)  # ?????????????????????????????????
        if os.path.isfile(filepath):  # ?????????????????????????????????????????????
            os.remove(filepath)  # ??????????????????????????????
            print("file:  " + str(filepath) + " removed!")
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)  # ??????????????????????????????????????????????????????????????????
            print("dic:  " + str(filepath) + " removed!")



def auto_restart(count):

    ct = 0
    while ct < 10:
        try:
            ct = ct + 1
            # auto_generator(count)
            auto_gen_structure(count)
        except RuntimeError as err:
            print(ct,"RuntimeError error: {0}".format(err))
        except OSError as err:
            print(ct,"OS error: {0}".format(err))
        except:
            print(ct,"Unexpected error:", sys.exc_info()[0])
        finally:
            print( 'finished')


if __name__ == '__main__':
    close_ANSYS()
    # x =gen_space()
    count = 0
    # auto_restart(count)
    # auto_gen_structure(count)

    start_ind = [1600, 1601]
    jobs = []
    auto_restart(0)
    # for i in range(2):
    #     # t =
    #     p = multiprocessing.Process(target=auto_restart, args=(start_ind[i],))
    #     jobs.append(p)
    #     p.start()



def auto_generator(_st):
    fs =25.0
    fe =35.0
    f_sol = 30.0
    nfp = 101
    dim_a = 10
    n = 128
    thickness = 0.01
    pix_l = dim_a/(2*n)

    count = _st


    if( os.path.isdir(my_path+"/Res") ==False ): os.makedirs(my_path+"/Res")
    if (os.path.isdir(my_path+"/Mat") == False): os.makedirs(my_path+"/Mat")
    if (os.path.isdir(my_path+"/Fig") == False): os.makedirs(my_path+"/Fig")


    h = HF.HFSS()

    surf = Gnr.Meta_Surf(n, dim_a, thickness)

    num_test = 1000
    for ii in range(num_test):

        while (os.path.isfile("./Res/design" + str(count) + ".txt")):
            count = count + 1
        print(count)

        design_name = "design"+ str(count)

        # surf.rand_normal()
        # surf.rand_modi(0.3)
        surf.rand_xy(0.4)

        surf.continu()
        surf.remove_single()


        h.new_design(design_name)
        h.gen_meta_with_surf_025( surf )


        h.create_box( str(-dim_a/2.0)+"mm", str(-dim_a/2.0)+"mm", str(-300.0/fs) + "mm",
                      str(dim_a) + "mm", str(dim_a) + "mm", str(2*300.0 / fs) + "mm", 'Boundary')

        h.assign_mater_slave_boundary_condition('Boundary')
        h.assign_floque_port('Boundary', f_sol)

        solution_name = 's'+str(count)


        h.insert_analysis_setup_old(solution_name, f_sol, 0.02, 8)
        h.insert_frequency_swap(solution_name, fs, fe, nfp)
        h.run(solution_name)

        # h.create_reports_tr(solution_name, "db")
        # h.create_reports_tr(solution_name, "phase")
        h.create_reports_tr_ri(solution_name, design_name)
        surf.save(design_name)
        h.delete_design(design_name)
    # h.delete_design(_ps_n)
