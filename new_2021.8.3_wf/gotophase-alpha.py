import os
filePath =r"./"



def native_cp(str_log_open,str_new):
    import os
    import shutil
    str_log_open = str_log_open ###文件名写死！！！防止出错
    shutil.copyfile(str_log_open, str_new)


def jsknb():
    import os
    try:
        os.makedirs('./gophase')
    except:
        print("alreay done")


    t=[]
    v=[]
    filename1=os.listdir(filePath)
    filename=[]
    #print(filename)
    #m=0
    for i in filename1:
        #print(i)
        if i[0:2]=="ve":
            filename.append(i)
    #print(filename)
    filesunxu=[filename[0]]
    for i in filename:
        k=0
        for j in filesunxu:
            if float(i.split('-')[2])>float(j.split('-')[2]) or (float(i.split('-')[2])==float(j.split('-')[2]) and float(i.split('-')[1])!=float(j.split('-')[1])) :
                filesunxu.insert(k,i)
                break
            else:
                if float(i.split('-')[2])==float(j.split('-')[2]) and float(i.split('-')[1])==float(j.split('-')[1]) :
                    break
                else:
                    if k>=len(filesunxu)-1:
                       filesunxu.append(i)
            k=k+1
    #print(filesunxu)
    flag=1
    while flag==1:
        m = 0
        flag=0
        for i in filesunxu:
            if m > 0:
                if filesunxu[m].split('-')[2] == filesunxu[m - 1].split('-')[2]:
                    if float(filesunxu[m].split('-')[1]) > float(filesunxu[m - 1].split('-')[1]):
                        flag=1
                        filesunxu[m], filesunxu[m - 1] = filesunxu[m - 1], filesunxu[m]
                        break
            m = m + 1

    #print(filesunxu)
    record=[]
    #print("shunxu",filesunxu)
    for i in filesunxu:
        path=filePath+i
        #print(path)
        # print(path)
        f=open(path,'r+')
        line=f.readlines()
        record.append(line[-1])
        f.close()
    #print("record",record)
    print("shunxu",filesunxu)
    m=0
    namelist=[filesunxu[0].split('-')[2]]
    file=filesunxu[0].split('-')[2]
    filenew = open(file, "w")
    
    import os
    for i in filesunxu:
        if file != i.split('-')[2]:
            filenew.close()
            file=i.split('-')[2]
            filenew=open(file,"w")
            namelist.append(i.split('-')[2])
        filenew.write(record[m])
        
        m=m+1
        
    filenew.close()
    
    return namelist
def cpdos(Vlist,Tlist = [100,500,750,1000,1500,2000]):
    Vlist = Vlist
    Tlist = Tlist
    
    for v in Vlist:
        for t in Tlist:
            native_cp("./ph.dos-"+str(v)+"-"+str(t),"./gophase/"+"ph.dos-"+str(v)+"-"+str(t))
    return print("done")
    


def trans_pdos(alist,vlist,Tlist=[100,500,750,1000,1500,2000]):
    import os
    os.chdir("./gophase")
    alist = alist
    vlist = vlist
    Tlist=Tlist
    import pandas as pd
    df = pd.DataFrame()
    df["v1"] = alist
    df["v2"] = vlist
    dict1 = dict(zip(df['v1'],df['v2']))
    dict1
    import os
    for a in alist:
        for t in Tlist:
            os.rename("ph.dos-"+str(a)+"-"+str(t),"ph.dos-"+str(dict1[a])+"000-"+str(t))












#namelist = jsknb()
#for i in namelist:
nmlist = []
for i  in jsknb(): native_cp("./"+str(i),"./gophase/ve-"+str(i))

for i  in jsknb(): nmlist.append(str(i))
    #print(i,"done")
#print(nmlist)
import pandas as pd
df = pd.read_csv("./"+nmlist[-1],header = None,delim_whitespace = True)
vlist = []
for i in df.iloc[:,0]: vlist.append(i)

print(vlist)

cpdos(Vlist=[2.6,2.7,2.8])    ###这里传入alist,也就是w1和w2的vlist,最开始的参数搜索

trans_pdos(alist =[2.6,2.7,2.8],
           vlist = vlist )