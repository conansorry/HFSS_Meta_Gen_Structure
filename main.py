import HFSS_Script as HF
import Meta_Generator as Gnr
import multiprocessing
import os.path
import shutil
import sys

my_path = "D:\Dropbox\Current_Research\\3 Metasurface GAN\Data2\\"
# if __name__ == '__main__':
#
def auto_generator(count):
    fs =5.0
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
def close_ANSYS():
    try:
        os.system("taskkill /F /IM ansysedt.exe")
    except:
        print("stop ansys not finished:", sys.exc_info()[0])

    try:
        delete_path("D:\Jiangy\JY_HFSS\Ansoft")
    except:
        print("not delete:", sys.exc_info()[0])
        # h.save_prj()

def delete_path( rootdir ):
    filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
    for f in filelist:
        filepath = os.path.join(rootdir, f)  # 将文件名映射成绝对路劲
        if os.path.isfile(filepath):  # 判断该文件是否为文件或者文件夹
            os.remove(filepath)  # 若为文件，则直接删除
            print("file:  " + str(filepath) + " removed!")
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件
            print("dic:  " + str(filepath) + " removed!")



def auto_restart(count):

    ct = 0
    while ct < 10:
        try:
            ct = ct + 1
            auto_generator(count)
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

    start_ind = [500, 1000]
    jobs = []
    for i in range(2):
        # t =
        p = multiprocessing.Process(target=auto_restart, args=(start_ind[i],))
        jobs.append(p)
        p.start()