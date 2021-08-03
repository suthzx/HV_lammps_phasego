#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time
            
"""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
           #######################输入文件准备部分#######################
"""
def sbatch():  
    """
    提交所有任务
    以sbatch方式
    """
    import os, sys,time
    ela = []
    sblist = []
    for root,dirs,files in os.walk(r"./"):
        for dir in dirs:
            ela.append(os.path.join(root,dir))
    mine = os.getcwd()
    cmd = mine +"/lammps.slurm"   ##这里写提交脚本的名字     
    for i in ela:    
        os.chdir(mine)
        #print(i)
        os.chdir(i)
        p = os.popen('pwd')
        print(p.read())
        p.close()
        try:
            os.system("sbatch "+ cmd)
            print("sbatch it ",i)
            time.sleep(30)
        except:
            sblist.append(i)
        os.chdir(mine)
    os.chdir(mine)
    print(sblist)
    return sblist
def net_mkdir(Vlist,Tlist=[10,100,500,750,1000,1500,2000]):
    """
    网格式路径创建
    有时会遇到权限问题，单独列出该函数
    """
    for v in Vlist:
        for t in Tlist:
            try:
                os.makedirs("./"+str(v)+"V/"+str(t)+"K")
            except:
                print("already done")              
#str_new 是拷贝文件的目的目录，str_log_open是拷贝文件的源目录
#该函数将以当前时间命名的log文件拷贝到制定目录
def native_cp(str_log_open,str_new):
    import os
    import shutil
    str_log_open = str_log_open ###文件名写死！！！防止出错
    shutil.copyfile(str_log_open, str_new)

def change(a,b):
    with open('in.BCC.FeNi-NVT','r',encoding='utf-8') as f:   ###文件名写死！！！防止出错
        lines=[] # 创建了一个空列表，里面没有元素
        for line in f.readlines():
            if line!='\n':
                lines.append(line)
    f.close()
    with open('in.BCC.FeNi-NVT','w',encoding='utf-8') as f:
        for line in lines:
            if a in line:
                line = b 
                f.write('%s\n' %line)
            else:
                f.write('%s' %line) 
                
def net_file(Vlist,Tlist=[10,100,500,750,1000,1500,2000]):
    """
    网格式初始文件拷入与修改
    """
    mine = os.getcwd()
    os.chdir(mine)
    #path = []
    for v in Vlist:
        for t in Tlist:
            os.chdir(mine)
        #print(i)
            native_cp("./in.BCC.FeNi-NVT",mine+"/"+str(v)+"V/"+str(t)+"K/"+"in.BCC.FeNi-NVT")
            native_cp("./Fe-Ni.eam.alloy",mine+"/"+str(v)+"V/"+str(t)+"K/"+"Fe-Ni.eam.alloy")
            os.chdir(mine+"/"+str(v)+"V/"+str(t)+"K")   ##进入底层提交层目录
            change("variable ntemp equal","variable ntemp equal "+str(t))   ###改T
            change("variable a equal","variable a equal "+str(v))   ###改V
            os.chdir(mine)
            
"""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
           #######################数据后处理部分#######################
"""
def get_ve(V,T):
    """
    处理得到合法的ve-V-T文件
    """
    import os
    import pandas as pd
    df = pd.read_csv("./VE.txt",header = None,delim_whitespace = True)
    df = df.iloc[2:,1:3]
    df.to_csv('ve'+str(V)+str(T), sep='\t',index=False)
    lines = (i for i in open('ve'+str(V)+str(T), 'r') if '1	2' not in i )
    f = open('test_new.txt', 'w', encoding="utf-8")
    f.writelines(lines)
    f.close()
    os.rename('ve'+str(V)+str(T), 'test.bak')
    os.rename('test_new.txt', 've')
    os.remove('test.bak')
    return print("ve...ok")
def find_pdos(v_all, Nc, dt, omega):    #Calculate the vacf from velocity data
    """
    计算PDOS函数，参数冻结

    """

# v_all: all the velocity data in some format
# Nc: number of correlation steps
# dt: time interval between two frames, in units of ps
# omega: phonon angular frequency points you want to consider
    Nf = v_all.shape[0]                 # number of frames
    M  = Nf - Nc                        # number of time origins for time average
    vacf = np.zeros(Nc)                 # the velocity autocorrelation function (VACF)
    for nc in range(Nc):                # loop over the correlation steps
        ratio = (nc+1)/Nc * 100    
        print("Calculate PDOS Progress %s%%" %ratio)
        for m in range(M+1):            # loop over the time origins
            delta = np.sum(v_all[m + 0]*v_all[m + nc])
            # print(delta)
            vacf[nc] = vacf[nc] + delta

    
    vacf = vacf / vacf[0]                                       # normalize the VACF
    vacf_output = vacf                                          # copy the VACF before modifying it
    vacf = vacf*(np.cos(np.pi*np.arange(Nc)/Nc)+1)*0.5          # window function
    vacf = vacf*np.append(np.ones(1), 2*np.ones(Nc-1))/np.pi    # C(t) = C(-t)
    pdos = np.zeros(len(omega))                                 # the phonon density of states (PDOS)
    for n in range(len(omega)):                                 # Discrete cosine transform
        pdos[n] = dt * sum(vacf * np.cos(omega[n] * np.arange(Nc) * dt))
    return(vacf_output, pdos)
def get_pdos(V,T,Nc=1000):
    """
    后处理PDOS数据
    得ph.dos-V-T文件
    
    """
    
    V = V            ### 体积参数————需要读取
    T = T              ### 体系温度
    ### set up some parameters related to the MD simulation
    N = 3456                            # 原子数目
    Nc = Nc                         # 步长的十分之一
    dt = 0.001                         # time interval in units of ps (its inverse is roughly the maximum frequency attainable)
    omega = np.arange(1, 380.5, 0.5)    # angular frequency in units of THz
    nu = omega / 2 / np.pi;             # omega = 2 * pi * nu, while nu is the frequency range
    Nf = Nc*10                          # The calculation numbers
    num_frame = Nf                      # Frame numbers equals to calculation numbers
    fileName = "./v_output.lammpstrj"
    ### Read the atomic velocity data from the lammps dump file
    # Noted that the atomic ID should be sorted, set "dump_modify dump_id sort id" in lammps input file
    v_all = np.zeros((num_frame, N, 3))             # Initialize the velocity data
    fin = open(fileName, "r")
    for i in range(num_frame):
        ratio = (i+1)/num_frame * 100 
        print("Read Data Progress %s%%" %ratio)
        initial = i * (9 + N)
        for j in range(9):                          # The first 9 lines should be excluded
            fin.readline()
        for k in range(N):
            line = fin.readline().split()[2:]
            line = [float(l) for l in line]
            v_all[i, k] = line
    vacf, pdos = find_pdos(v_all, Nc, dt, omega)    # Call the function and calculate the vacf and pdos
    t = np.arange(Nc)*dt   
    df = pd.DataFrame()
    df["pdos"] = pdos
    df["nu"]=nu
    df = df[["nu","pdos"]]
    df.to_csv('./ph.dos-'+str(V)+"-"+str(T), header=None, index=False, sep=" ")

########################---------以上为处理ve文件和pdos文件------------########################    
def net_deal(Vlist,Tlist=[10,100,500,750,1000,1500,2000]):
    """
    网格式后处理与数据提取(ve数据提取dataframe)
    """
    mine = os.getcwd()
    os.chdir(mine)
    #path = []
    for v in Vlist:
        for t in Tlist:
            os.chdir(mine)
        #print(i)
            #native_cp("./in.BCC.FeNi-NVT",mine+"/"+str(v)+"V/"+str(t)+"K/"+"in.BCC.FeNi-NVT")
            os.chdir(mine+"/"+str(v)+"V/"+str(t)+"K")   ##进入底层提交层目录
            #change("variable ntemp equal 800","variable ntemp equal "+str(t))   ###改T
            #change("variable a equal 2.855","variable a equal "+str(v))   ###改T
            get_pdos(V=v,T=t)
            get_ve(V=v,T=t)
            os.chdir(mine)


# In[31]:


Vlist = [2.991892027173679,
 3.007600789715576,
 3.023147125824695,
 3.0385351700285743,
 3.053768890995359,
 3.068852100547055,
 3.0837884620584854,
 3.0985814982920545,
 3.113234598713697,
 3.1277510263311314,
 3.1421339240917945,
 3.156386320874386,
 3.170511137104981,
 3.1845111900258707,
 3.198389198642882]
net_mkdir(Vlist=Vlist)   ###创建所有文件夹
net_file(Vlist=Vlist)    ###注意函数内名字，每个文件夹的输入文件准备
sbatch()                 ###并行式任务完全提交


# In[ ]:




