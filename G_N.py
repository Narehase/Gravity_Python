import numpy as np
import cv2
import math
import os
import time
st = time.time()
def IntToAlpabet(Wa):
    if Wa > 23:
        Wa = 23
        
    al = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return str(al[Wa])

class Gravity:
    def __init__(self,Rx = 500 ,Ry = 500,D_acc = [0,0.0]) -> None:
        self.numd = 0
        self.Lit = []
        self.Gra = []   
        self.rx = Rx
        self.ry = Ry
        self.D_ac = D_acc
        self.rSeta = 0

    def Gravity(self,m1,m2,r,G = 6.673 ):
        try:
            Gp = G*((m1*m2)/(r**2))
        except:
            Gp = 0
        return Gp

    def sets(self,name,m,r,acc,axis = [0,0],color=[0,255,100],Move = "Y"): # m = kg, Acc = [Seta,m/s]
        for i in self.Lit:
            if i[0] == name:
                print("같은 이름의 객체가 존재 합니다.")
                raise
        self.Lit.append([name,m,acc,axis,r,color,Move])
        self.Pick(axis,r,color)
    def Pick(self,axis, r, color = [0,0,255]):
        for i in range(r-1):
            i += 1
            for ip in range(360):
                rad = math.radians(ip)
                x = int(i*math.cos(rad)) + self.rx
                y = int(i*math.sin(rad)) + self.ry
                
                y = int(axis[1])+y
                x = int(axis[0])+x
                #print([axis[0]+y,axis[1]+x])
                try:
                    if x < 0 or x > 999:
                        # print("err60")
                        raise
                    if y < 0 or y > 999:
                        # print("err40")
                        raise
                    self.Fild[y, x] = color
                except:
                    pass
                    # print("err")
    def updata(self):
        self.Fild = self.cov.copy()
        for n in self.Lit:
            self.Pick(n[3],n[4],n[5])
    def All_Nuton(self):
        G = 1.
        Pik = []
        for A in self.Lit:
            L1 = []
            cv2.putText(self.Fild, str(A[0]),(int(A[3][0])+self.ry,int(A[3][1])+self.rx), cv2.FONT_HERSHEY_PLAIN,2,(0, 0,10),2,cv2.LINE_AA )
            for B in self.Lit:
                if A[0] != B[0]:            
            
                    y = B[3][0] - A[3][0]
                    x = B[3][1] - A[3][1]
                    Squid = math.sqrt((x*x)+(y*y))
                    
                    if Squid**2 > 0:
                        F = G*(A[1]*B[1]) / Squid**2
                    else:
                        F = 0.

                    Seta = math.atan2(y,x)*(180/math.pi) 
                    # self.Drow(A,Seta, 50)
                    L1.append([Seta, F])

            
            x = 0
            y = 0
            for L2 in L1:
                x += L2[1]*math.cos(math.radians(L2[0])) 
                y += L2[1]*math.sin(math.radians(L2[0]))
            
            x += A[2][1]*A[1]*math.cos(math.radians(A[2][0]))
            y += A[2][1]*A[1]*math.sin(math.radians(A[2][0]))
            
            x += self.D_ac[1]*A[1]*math.cos(math.radians(self.D_ac[0]))
            y += self.D_ac[1]*A[1]*math.sin(math.radians(self.D_ac[0]))


            Seta = math.atan2(y,x)*(180/math.pi)
            F = math.sqrt((x**2)+(y**2))
            if A[1] == 0:
                Ac = 0.
            else:
                Ac = F/A[1]
            
            # x = Ac*math.cos(math.radians(Seta))
            # y = Ac*math.sin(math.radians(Seta))
            # Seta = math.atan2(y,x)*(180/math.pi)
            # F = math.sqrt((x**2)+(y**2))
            
            # print(Ac)
            Ax = self.Drow(A, Seta,100, 1, Ac*10)
            if A[6] == "Y":
                Pik.append([A[0],A[1],[Seta,Ac],Ax,A[4],A[5],A[6]])
            else:
                Pik.append([A[0],A[1],[Seta,Ac],A[3],A[4],A[5],A[6]])
            # self.Lit.append([name,m,acc,axis])

        self.Lit = Pik
        pili = cv2.resize(self.Fild,[1000,1000])
        cv2.imshow("ll", pili)
        keys = cv2.waitKey(1)
        if keys == ord("a"):
            cv2.imshow("ll", pili)
            cv2.waitKey()
        if keys == ord("s"):
            cv2.imwrite("web.png",self.Fild*255)
            cv2.imwrite("web_Raw.png",self.cov*255)
    def Drow(self,A, Seta, Lagrangu , J = 0, tik = 0.):
        # print(Lagrangu)
        
        for i in range(round(Lagrangu)):
            coss = int(i * math.sin(math.radians(Seta)) + self.rx + A[3][0])
            sins = int(i * math.cos(math.radians(Seta)) + self.ry + A[3][1])
            
            try:                   
                if coss < 0 or coss > self.size[0]-1:
                    # print("err60")
                    pass
                elif sins < 0 or sins > self.size[1]-1:
                    pass
                else:
                    if J == 0:
                        self.Fild[sins,coss] = [10,10,10]
                    elif J == 1:
                        
                        self.Fild[sins,coss] = [0,0,10]
            except:
                pass
            xp = int(A[3][0])+self.rx
            yp = int(A[3][1])+self.ry

            if xp < 0 or xp > self.size[0]-1:
                # print("err60")
                pass
            elif yp < 0 or yp > self.size[1]-1:
                pass
            else:
                if J == 1:
                    self.Fild[yp,xp] = [0,10,0]
                    self.cov[yp,xp] = [0,10,0]
                            
        c = (tik * math.sin(math.radians(Seta)) + A[3][0])
        s = (tik * math.cos(math.radians(Seta)) + A[3][1])
        return [c,s]
    
    def Navi(self):
        os.system("cls")
        for i in self.Lit:
            name = str(i[0])
            if len(name) > 6:
                name = name[0:5] + "-"  
            Acc = i[2][1]
            if len(str(Acc)) > 14:
                Acc = str(Acc)[0:13] + "-"
            else:
                Pik = "                     "
                Pik = (str(Acc) + Pik)
                Acc = str(Pik)[0:14] 
            print(name,"| Accel :", Acc, "|")
    
    # def Accel(self):
    #     S = V* t + 0.5*a*t**2
    #     if t != 0 :
    #         SV = S/t
    #     else :
    #         SV = 0.
    #     return S, SV 
    
    def Base_(self, Size = [1000,1000]):
        self.size = Size
        self.Fild = np.zeros([Size[0],Size[1],3])
        self.cov = self.Fild.copy()


def rand_ty():
    a = np.random.randint(0,1000)
    b = np.random.randint(0,1000)
    #print(a," :: ",b)
    return[a-500,b-500] 

a = Gravity(1000,1000,[0,0.])
a.Base_([2000,2000])


a.sets("Dokdo",10,10,axis=[-200,-500],acc=[0,0.518])
a.sets("Dokdo1",10,10,axis=[-200,0],acc=[0,0.68])
a.sets("Dokdo2",500,10,axis=[0,0],acc=[0,0.],Move="N")
a.sets("Dokdo3",10,10,axis=[500,0],acc=[0,0.25])


for i in range(1000):
    a.All_Nuton()
    a.updata()
    a.Navi()
print(time.time() - st)
#지구 자전
#a.sets("Dokdo",10,10,axis=[-200,-500],acc=[0,0.518])
# a.sets("Dokdo1",10,10,axis=[-200,0],acc=[0,0.68])
# a.sets("Dokdo2",500,10,axis=[0,0],acc=[0,0.],Move="N")
# a.sets("Dokdo3",10,10,axis=[500,0],acc=[0,0.25])

# a.sets("Dokdo",-100,10,axis=[-200,-500],acc=[-27,0.25])
# a.sets("Navi",0.,0,axis=[0,0],acc=[0,0])
# # a.sets("Dokdo1",10,10,axis=[-200,0],acc=[0,0.68])
# a.sets("Dokdo2",500,10,axis=[0,0],acc=[0,0.],Move="Y")
# a.sets("Dokdo3",10,10,axis=[500,0],acc=[-55,0.3])

#마이너스 질량
# a.sets("Dokdo",-500,10,axis=[-200,-200],acc=[0,0.],Move="N")
# a.sets("Dokdo2",-500,10,axis=[-200,200],acc=[0,0.],Move="N")
# a.sets("Dokdo3",-500,10,axis=[200,-200],acc=[0,0.],Move="N")
# a.sets("Dokdo4",-500,10,axis=[200,200],acc=[0,0.],Move="N")
# a.sets("Dokdo5",-500,10,axis=[0,200],acc=[0,0.],Move="N")
# a.sets("Dokdo6",-500,10,axis=[200,0],acc=[0,0.],Move="N")
# a.sets("Dokdo7",-500,10,axis=[0,-200],acc=[0,0.],Move="N")
# a.sets("Dokdo8",-500,10,axis=[-200,0],acc=[0,0.],Move="N")
# a.sets("Dokd09",1000,10,axis=[0,0],acc=[10,0.5])

#신기한 공전
# a.sets("Dokdo",500,10,axis=[0,0],acc=[0,0.3],Move="Y")
# # a.sets("Dokdo1",100,10,axis=[-200,-200],acc=[10,0.5],Move="Y")
# a.sets("Dokdo2",500,10,axis=[-200,-200],acc=[180,0.3],Move="Y")
# # a.sets("Dokdo3",150,10,axis=[200,-200],acc=[-98,0.25],Move="Y")
# a.sets("Dokdo4",50,10,axis=[200,200],acc=[100,0.35],Move="Y")

#ART
# a.sets("Dokdo",700,10,axis=[0,0],acc=[180,0.2],Move="Y")
# a.sets("Dokdo2",700,10,axis=[-200,-200],acc=[0,0.2],Move="Y")
# # a.sets("Dokdo4",10,10,axis=[200,0],acc=[-90,0.2],Move="Y")

#큰 궤도
# a.sets("Dokdo0",800,10,axis=[0,0],acc=[0,0.],Move="N")
# # a.sets("Dokdo1",700,10,axis=[200,200],acc=[180,0.6],Move="Y",color=[255,0,0])
# a.sets("Dokdo2",700,10,axis=[200,-200],acc=[0,0.6],Move="Y",color=[255,0,0])
# # a.sets("Dokdo3",700,10,axis=[200,-200],acc=[-90,0.6],Move="Y",color=[255,0,0])
# # a.sets("Dokdo4",700,10,axis=[-200,200],acc=[90,0.6],Move="Y",color=[255,0,0])
# # a.sets("Dokdo3",150,10,axis=[200,-200],acc=[-98,0.25],Move="Y")
# # a.sets("Dokdo4",10,10,axis=[200,0],acc=[-90,0.2],Move="Y")
# a.sets("1Dokdo",500,10,axis=[0,0],acc=[0,0.3],Move="Y")
# # a.sets("Dokdo1",100,10,axis=[-200,-200],acc=[10,0.5],Move="Y")
# a.sets("2Dokdo2",500,10,axis=[-200,-200],acc=[180,0.3],Move="Y")
# # a.sets("Dokdo3",150,10,axis=[200,-200],acc=[-98,0.25],Move="Y")
# a.sets("3Dokdo4",50,10,axis=[200,200],acc=[100,0.35],Move="Y")
