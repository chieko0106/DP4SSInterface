# -*- coding: UTF-8 -*-
class File:
    Control = {}
    Data = {}
    def __init__(self,path,file):
        self.__path = path
        self.__file = file
    def Read(self):
        f = open(self.__path+self.__file)
        File.Control = {}
        File.Data = {'Strain':[],
                     'Stress':[],
                     'Tube_Water':[],
                     'Chamber_Volume':[],
                     'Seepage_Volume':[]}
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
    def New(self, If_Strain_Pointed = False, Pointed_Strain = []):
        __f = File(path, file)
        __f.Read()
        if If_Strain_Pointed:  # if Strain is pointed, then Strain is Pointed Strain.
            FlowRate = {'TimeLabel': [], 'Strain': Pointed_Strain, 'FlowRate': []}
            # Linear Interpolation
            j = 0
            __Stress = []
            __Tube = []
            __Chamber = []
            __Seepage = []
            for i in range(len(Pointed_Strain)):
                S = Pointed_Strain[i]
                while j < len(__f.Data['Strain']) - 1:
                    S0 = __f.Data['Strain'][j]
                    S1 = __f.Data['Strain'][j + 1]
                    if S <= S1 and S >= S0:
                        SS0 = __f.Data['Stress'][j]
                        SS1 = __f.Data['Stress'][j + 1]
                        __Stress.append(SS0 + (SS1 - SS0) * (S - S0) / (S1 - S0))
                        SS0 = __f.Data['Tube_Water'][j]
                        SS1 = __f.Data['Tube_Water'][j + 1]
                        __Tube.append(SS0 + (SS1 - SS0) * (S - S0) / (S1 - S0))
                        SS0 = __f.Data['Chamber_Volume'][j]
                        SS1 = __f.Data['Chamber_Volume'][j + 1]
                        __Chamber.append(SS0 + (SS1 - SS0) * (S - S0) / (S1 - S0))
                        SS0 = __f.Data['Seepage_Volume'][j]
                        SS1 = __f.Data['Seepage_Volume'][j + 1]
                        __Seepage.append(SS0 + (SS1 - SS0) * (S - S0) / (S1 - S0))
                        break
                    j += 1
                    if j == len(__f.Data['Strain']) - 1 and S > S1:
                        # if the pointed value exceeds the maximum, Outerpolation
                        SS0 = __f.Data['Stress'][j - 1]
                        SS1 = __f.Data['Stress'][j]
                        __Stress.append(SS1 + (SS1 - SS0) * (S - S1) / (S1 - S0))
                        SS0 = __f.Data['Tube_Water'][j - 1]
                        SS1 = __f.Data['Tube_Water'][j]
                        __Tube.append(SS1 + (SS1 - SS0) * (S - S1) / (S1 - S0))
                        SS0 = __f.Data['Chamber_Volume'][j - 1]
                        SS1 = __f.Data['Chamber_Volume'][j]
                        __Chamber.append(SS1 + (SS1 - SS0) * (S - S1) / (S1 - S0))
                        SS0 = __f.Data['Seepage_Volume'][j - 1]
                        SS1 = __f.Data['Seepage_Volume'][j]
                        __Seepage.append(SS1 + (SS1 - SS0) * (S - S1) / (S1 - S0))
                        print('Waring : Outerpolation warning. Check data at STRAIN IN FILE: '
                              , S0, 'and', S1,
                              'STRAIN POINTED :', S)
                        break
            __f.Data['Strain'] = Pointed_Strain
            __f.Data['Stress'] = __Stress
            __f.Data['Tube_Water'] = __Tube
            __f.Data['Chamber_Volume'] = __Chamber
            __f.Data['Seepage_Volume'] = __Seepage
    def Calculate_FlowRate(self, If_Strain_Pointed = False, Pointed_Strain = []):
        __f = File(path, file)
        __f.New(If_Strain_Pointed, Pointed_Strain)
        FlowRate = {'TimeLabel': [], 'Strain': [i/100 for i in __f.Data['Strain']], 'FlowRate': []}
        speed = float(__f.Control['Shear_Speed'][0])# unit of speed is mm/min
        for i in range(len(FlowRate['Strain'])-1):
            __dStrain = FlowRate['Strain'][i+1]-FlowRate['Strain'][i]
            __time = __dStrain/speed
            FlowRate['TimeLabel'].append(__time) # unit of time is minute
            __Ice_Out = __dStrain/10*4.5*2 # unit of ice out is cm^3 (mL)
            __Seepage_In = __f.Data['Seepage_Volume'][i + 1] - __f.Data['Seepage_Volume'][i]
            __Chamber_In = __f.Data['Chamber_Volume'][i + 1] - __f.Data['Chamber_Volume'][i]\
                         + __dStrain*(3.1415926 - 4.5*2) # Lever_In
            __All_Out = __f.Data['Tube_Water'][i] - __f.Data['Tube_Water'][i + 1]
            Flow = __All_Out-__Ice_Out
            # print(__All_Out)
            FlowRate['FlowRate'].append(Flow/__time)
        return(FlowRate)




import matplotlib.pyplot as plt

path = "H:\\data\\Shear_Seepage\\dataprocess\\Data\\"
file = "test.txt"
mod = [100,200,300,400,500,600,700,800,900,1000,1500,2000,2500,3000
    ,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]
# mod = [100,200,300,400,500,600,700,800,900,1000,2000,3000,4000,5000,6000,7000,8000]
fig, ax = plt.subplots()

file = "JC2_100.txt"
In1 = File(path,file)
a1 = In1.Calculate_FlowRate(True,mod)
line1, = ax.plot(a1['Strain'][1:], a1['FlowRate'], '--', linewidth=2,label=file)

file = "JC2_200.txt"
In2 = File(path,file)
a2 = In2.Calculate_FlowRate(True,mod)
line2, = ax.plot(a2['Strain'][1:], a2['FlowRate'], '--', linewidth=2,label=file)

file = "JC2_500.txt"
In3 = File(path,file)
a3 = In3.Calculate_FlowRate(True,mod)
line3, = ax.plot(a3['Strain'][1:], a3['FlowRate'], '--', linewidth=2,label=file)

file = "JC2_900.txt"
In4 = File(path,file)
a4 = In4.Calculate_FlowRate(True,mod)
line4, = ax.plot(a4['Strain'][1:], a4['FlowRate'], '--', linewidth=2,label=file)

ax.scatter(a1['Strain'][1:], a1['FlowRate'], marker='o')
ax.scatter(a2['Strain'][1:], a2['FlowRate'], marker='o')
ax.scatter(a3['Strain'][1:], a3['FlowRate'], marker='o')
ax.scatter(a4['Strain'][1:], a4['FlowRate'], marker='o')

ax.semilogx()
ax.legend(loc='upper right')
plt.show()
print('finished')

