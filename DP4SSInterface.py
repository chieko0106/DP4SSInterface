# -*- coding: UTF-8 -*-
class File:
    Control={}
    Data = {'Strain':[],
            'Stress':[],
            'Tube_Water':[],
            'Chamber_Volume':[],
            'Seepage_Volume':[]}
    def __init__(self,path,file):
        self.__path = path
        self.__file = file
    def Read(self):
        f = open(self.__path+self.__file)
        for line in f:
            if line[0].isalpha():
                line = line[0:-1]
                line = line.split('\t')
                File.Control[line[0]] = line[1:]
            else:
                line = line[0:-1]
                line = line.split('\t')
                File.Data['Strain'].append(float(line[0]))
                File.Data['Stress'].append(float(line[1]))
                File.Data['Tube_Water'].append(float(line[2]))
                File.Data['Chamber_Volume'].append(float(line[3]))
                File.Data['Seepage_Volume'].append(float(line[4]))
        f.close()
    def Calculate_FlowRate(self):
        __f = File(path, file)
        __f.Read()
        speed = float(__f.Control["Shear_Speed"][0])




path = "H:\\data\\Shear_Seepage\\dataprocess\\"
file = "test.txt"


In = File(path,file)
#In.Read()
In.Calculate_FlowRate()
print('finished')

