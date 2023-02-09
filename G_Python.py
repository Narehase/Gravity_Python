#======================
import numpy as np
import cv2
import os
import math
#각 모듈 불러오기
#====================== 

def IntToAlpabet(Wa):
    if Wa > 25:
        Wa = 25
        
    al = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return str(al[Wa])
def IntToAlpabet_s(Wa):
    if Wa > 25:
        Wa = 25
        
    al = "abcdefghijklmnopqrstuvwxyz"
    return str(al[Wa])

class Gravity:
    def __init__(self, reZeroset = [500,500], D_acc = [0.,0.],pixel_size = 1,frame_time = 0.01, unit = 1.): # 함수 초기 설정 및 초기화
        # pixel_size 단위는 미터
        self.pixel = pixel_size
        self.num_ = 0
        self.dt= 1.0
        self.Set_List = []
        self.Gra = []
        self.rx = reZeroset[0]
        self.ry = reZeroset[1]
        self.Dacc = D_acc
        self.frame_t = frame_time
        self.unit = unit

    def set_fild(self, size = [1000,1000]): # 화면 표시영역 크기 설정
        self.fild = np.zeros([size[0],size[1],3])
        self.fild_size = size
        self.cov = self.fild.copy()

    def test(self):
        cv2.imshow("a",self.fild)
        cv2.waitKey()
    
    def sets(self, name:str, m, r, acc = [0.,0.], axis = [0,0], color = [0,255,100], Move = "Y"): # 각 객체 저장
        #acc = [0.,0.] || [가속도, 각도]
        ch = False
        for i in self.Set_List:
            if i[0] == name:
                for al in range(26):
                    plus_text = IntToAlpabet_s(al)
                    rename = name + "_{}".format(plus_text)
                    for i in self.Set_List:
                        if i[0] == rename:
                            ch = True
                            break
                    if(al == 25 and i[0] == rename):
                        print("같은 이름이 너무 많습니다! 객체별 이름을 다르게 설정해 주세요!")
                        raise
                    if ch:
                        ch = False
                        continue                    
                    if(i[0] != rename):
                        print("같은 이름의 객체가 존재합니다. 이에 {} 의 객체명을 {}로 변경 합니다.".format(name,rename))
                        name = rename
                        break
                
        self.Set_List.append([name, m, r, acc, axis, color, Move])
        self.Pick(axis,r,color)

    def Nuton(self):
        List_r = []
        for A in self.Set_List:
            L1 = []
            for B in self.Set_List:
                if A != B:
                    F, Seta = self.__A_to_B__(A,B)
                    Ac = F / A[1]
                    L1.append([Seta,Ac])
                
            x = 0.
            y = 0.
            
            #가속도 분해 합성
            x += A[3][1]*math.cos(math.radians(A[3][0]))
            y += A[3][1]*math.sin(math.radians(A[3][0]))
            
            for L2 in L1: # 벡터 합성
                x += L2[1]*math.cos(math.radians(L2[0])) 
                y += L2[1]*math.sin(math.radians(L2[0]))
            
            #가속도 분해 합성
            x += self.Dacc[1]*math.cos(math.radians(self.Dacc[0]))
            y += self.Dacc[1]*math.sin(math.radians(self.Dacc[0]))


            
            #각도 구하기
            Seta = math.atan2(y,x)*(180/math.pi)
            All_Acc = math.sqrt((x**2)+(y**2))
            re_Acc = All_Acc*(self.dt)

            Date = self._Draw_(A[4],Seta,re_Acc,30)

            if A[6] == "Y" or A[6] == "y":
                List_r.append([A[0],A[1],A[2],[Seta,All_Acc],Date,A[5],A[6]])
            elif A[6] == "N" or A[6] == "n":
                List_r.append([A[0],A[1],A[2],[Seta,All_Acc],A[4],A[5],A[6]])
            else:
                print("sets의 변수 Move 는 Y 또는 N이어야 합니다.")
                raise TypeError

        self.List_r = List_r

        cv2.imshow("G",self.fild)
        cv2.waitKey(32)

    def Pick(self, axis, r, color = [0,0,255]):
        for i in range(r):
            i += 1
            for ip in range(360):
                
                rad = math.radians(ip)

                x = int(i*math.cos(rad)) + self.rx
                y = int(i*math.sin(rad)) + self.ry
                
                y = int(axis[1])+y
                x = int(axis[0])+x
                try:
                    if x < 0 or x > self.fild_size[1]:
                        raise
                    if y < 0 or y > self.fild_size[0]:
                        raise
                    self.fild[y,x] = color
                except:
                    pass

    def Update(self):
        
        self.dt += self.frame_t
        self.fild = np.zeros([self.fild_size[0],self.fild_size[1],3])
        self.Set_List = self.List_r
        for A in self.Set_List:
            self.Pick(A[4],A[2],A[5])

    def Navi(self):
        os.system("cls")
        print("{}second ===============/\\".format(self.dt) )
        for A in self.Set_List:
            print("{} | Acc: {}".format(A[0],A[3]))


    def _Draw_(self,Axis,Seta,Acc,Lagrangu,J = 1) -> list:
        for i in range(round(Lagrangu)):
            x = int(i * math.sin(math.radians(Seta)) + self.rx + Axis[0])
            y = int(i * math.cos(math.radians(Seta)) + self.ry + Axis[1])
            
            try:                   
                if x < 0 or x > self.fild_size[0]-1:
                    # print("err60")
                    pass
                elif y < 0 or y > self.fild_size[1]-1:
                    pass
                else:
                    if J == 0:
                        self.fild[y,x] = [10,10,10]
                    elif J == 1:
                        
                        self.fld[y,x] = [0,0,10]
            except:
                pass
        xp = int(Axis[0])+self.rx
        yp = int(Axis[1])+self.ry

        if xp < 0 or xp > self.fild_size[0]-1:
            pass
        elif yp < 0 or yp > self.fild_size[1]-1:
            pass
        else:
            if J == 1:
                self.fild[yp,xp] = [0,10,0]
                self.cov[yp,xp] = [0,10,0]
        
        xs = (Acc * math.sin(math.radians(Seta)) + Axis[0])
        ys = (Acc * math.cos(math.radians(Seta)) + Axis[1])
                            
        return [xs,ys]
            

    def __A_to_B__(self,A,B):
        G =1.

        y = B[4][0] - A[4][0]
        x = B[4][1] - A[4][1]
        Squid = math.sqrt((x*x)+(y*y)) * self.unit
        
        if Squid <= 1:
            F = 0.
        else:
            F = G*((A[1]*B[1]) / Squid**2)
        
        Seta = math.atan2(y,x)*(180/math.pi) 

        return F,Seta


def rand_ty():
    a = np.random.randint(0,1000)
    b = np.random.randint(0,1000)
    #print(a," :: ",b)
    return[a-500,b-500] 

a = Gravity(D_acc=[0,0],frame_time=0.001)
a.set_fild()
# for i in range(1):
#     a.sets("aa",1,5,[0,9.8],rand_ty())
a.sets("ABC",50,5,[180.,14],[100,100],[0,0,255])
a.sets("ABC",50,5,[0.,14],[-100,-100],[0,0,255])
a.sets("ABC",25000,5,[0.,0.],[0,0],[0,0,255],"N")

for i in range(100000):
    a.Nuton()
    a.Navi()
    a.Update()
    
