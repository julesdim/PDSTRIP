import csv
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt
Lpp=135
def conversion_coordinate_to_pdstrip(coord,midship_section):
    return (coord[0]-midship_section,coord[1],coord[2])

def calculation_coord(filename):
    fichier=open(filename,"r",encoding="utf-8")
    les_lignes=csv.reader(fichier)
    compt_ligne=0
    debut_frame=True
    x=0
    y=0
    z=0
    coord=[]
    for ligne in les_lignes:
        new=ligne[0].strip().split()
        #print(new)
        if compt_ligne==0:
            nb_f_tot=float(new[0])
        if compt_ligne!=0 and len (new)==1 and debut_frame:
            x=(float(new[0]))
            debut_frame=False
        if compt_ligne!=0 and len (new)==3 :
            y=(float(new[0]))
            z=(float(new[1]))
            coord_act=(x,y,z)

            coord.append((x,y,z))
            debut_frame=True
        compt_ligne+=1
    return coord

def calcul_rx2(coord,yg,zg):
    sum=0
    for i in range (len(coord)):
        y=coord[i][1]
        z = coord[i][2]
        sum+=(y-yg)**2+(z-zg)**2
    for i in range (len(coord)):
        y = -coord[i][1]
        z = coord[i][2]
        sum+=(y-yg)**2+(z-zg)**2
    return sum/2*len(coord)


def calcul_ry2(coord,xg,zg):
    sum = 0
    for i in range(len(coord)):
        x = coord[i][0]
        z = coord[i][2]
        sum += (x - xg) ** 2 + (z - zg) ** 2
    return sum / len(coord)

def calcul_rz2(coord,xg,yg):
    sum = 0
    for i in range(len(coord)):
        x = coord[i][0]
        y = coord[i][1]
        sum += (x - xg) ** 2 + (y - yg) ** 2
    for i in range(len(coord)):
        x = coord[i][0]
        y = -coord[i][1]
        sum += (x - xg) ** 2 + (y - yg) ** 2
    return sum / 2 * len(coord)

def calcule_xy(coord,xg,yg):
    sum=0
    for i in range(len(coord)):
        x = coord[i][0]
        y = coord[i][1]
        sum += (x - xg)*(y - yg)
    for i in range(len(coord)):
        x = coord[i][0]
        y = -coord[i][1]
        sum += (x - xg) * (y - yg)
    return sum/2*len(coord)

def calcul_yz(coord,yg,zg):
    sum = 0
    for i in range(len(coord)):
        z = coord[i][2]
        y = coord[i][1]
        sum += (z - zg) * (y - yg)
    for i in range(len(coord)):
        z = coord[i][2]
        y = -coord[i][1]
        sum += (z - zg) * (y - yg)
    return sum / 2 * len(coord)

def calcul_xz(coord,xg,zg):
    sum = 0
    for i in range(len(coord)):
        z = coord[i][2]
        x = coord[i][0]
        sum += (z - zg) * (x - xg)
    return sum / len(coord)

def mass_list (masses):
    fichier=open(masses,"rt")
    liste_masses=[]
    les_lignes=fichier.readlines()
    for ligne in les_lignes:
        ligne=ligne.strip("\n").split(";")
        m=float(ligne[0])
        xb = float(ligne[1])
        xe = float(ligne[2])
        xg = float(ligne[3])
        yr = float(ligne[4])
        z = float(ligne[5])
        liste_masses.append((m,xb,xe,xg,yr,z))
    return liste_masses

list_of_masses=mass_list("masses.csv")

def mass_calculation (masses,xb,xe):
    n=len(masses)
    tm=0
    for i in range (n):
        m=masses[i][0]
        xbm = masses[i][1]
        xem= masses[i][2]
        if xbm<xe and xem>xb:
            rb=np.max([xb,xbm])
            re=np.min([xe,xem])
            tm+=m*(re-rb)/(xem-xbm)
            #print(m*(re-rb)/(xem-xbm))
    return tm

def calcul_center_of_gravity(masses,xb,xe):
    """"calculationof the center of gravity with a list of masses
     warning the origine is the Pias origin of the report, a conversion is needed
     if we want to use the coordinates relative to the midship, for the PD Strip Theory """
    tm=mass_calculation(masses,xb,xe)
    n=len(masses)
    xg=0
    zg=0
    for i in range (n):
        m = masses[i][0]
        xbm = masses[i][1]
        xem = masses[i][2]
        if xbm < xe and xem > xb:
            rb = np.max([xb, xbm])
            re = np.min([xe, xem])
            rm = m * (re - rb) / (xem - xbm)
            xg+=rm*(re+rb)/2
            zg+=rm*masses[i][5]
            #print(masses[i][5])
    xg=xg/tm
    zg=zg/tm
    return (xg,0,zg)

def PD_strip_info_from_for_to_aft(masses,coord):
    all_coord=calculation_coord(coord)
    mass=mass_list(masses)
    list_x=[]
    f=open("data_pdstrip.csv","w")
    for coord in all_coord:
        if coord[0] not in list_x:
            list_x.append(coord[0])
    list_x.sort()
    print (list_x)
    n_x=len(list_x)
    for i in range (n_x-1):
        back=list_x[n_x-i-2]
        forw=list_x[n_x-i-1]
        list_coord=[]
        for coord in all_coord:
            if coord[0]==back or coord[0]==forw:
                list_coord.append(coord)
        m=mass_calculation(mass,back,forw)
        xg,yg,zg=calcul_center_of_gravity(mass,back,forw)
        xg,yg,zg=conversion_coordinate_to_pdstrip((xg,yg,zg),Lpp/2)
        rx2=calcul_rx2(list_coord,yg, zg)
        ry2=calcul_ry2(list_coord,xg,zg)
        rz2=calcul_rz2(list_coord,xg, yg)
        xy=calcule_xy(list_coord,xg, yg)
        yz=calcul_yz(list_coord,yg, zg)
        xz=calcul_xz(list_coord,xg, zg)
        data=[m,xg,yg,zg,rx2,ry2,rz2,xy,yz,xz]
        for inf in data:
            f.write(str(inf)+" ")
        f.write("\n")
    f.close()
    return
def PD_strip_info_from_aft_to_for(masses,coord):
    all_coord=calculation_coord(coord)
    mass=mass_list(masses)
    list_x=[]
    f=open("data_pdstrip.csv","w")
    for coord in all_coord:
        if coord[0] not in list_x:
            list_x.append(coord[0])
    list_x.sort()
    print (list_x)
    n_x=len(list_x)
    for i in range (n_x-1):
        back=list_x[i]
        forw=list_x[i+1]
        list_coord=[]
        for coord in all_coord:
            if coord[0]==back or coord[0]==forw:
                list_coord.append(coord)
        m=mass_calculation(mass,back,forw)
        xg,yg,zg=calcul_center_of_gravity(mass,back,forw)
        xg,yg,zg=conversion_coordinate_to_pdstrip((xg,yg,zg),Lpp/2)
        rx2=calcul_rx2(list_coord,yg, zg)
        ry2=calcul_ry2(list_coord,xg,zg)
        rz2=calcul_rz2(list_coord,xg, yg)
        xy=calcule_xy(list_coord,xg, yg)
        yz=calcul_yz(list_coord,yg, zg)
        xz=calcul_xz(list_coord,xg, zg)
        data=[m,xg,yg,zg,rx2,ry2,rz2,xy,yz,xz]
        for inf in data:
            f.write(str(inf)+" ")
        f.write("\n")
    f.close()
    return

#print (mass_calculation(list_of_masses,70,80))
#print(calcul_center_of_gravity(list_of_masses,70,80))
coord=calculation_coord("frame_try.asc")
#print(coord)
zg=3.372587
yg=0
xg=90.01621
rx2=calcul_rx2(coord,yg,zg)
ry2=calcul_ry2(coord,xg,zg)
rz2=calcul_rz2(coord,xg,yg)
xy=calcule_xy(coord,xg,yg)
yz=calcul_yz(coord,yg,zg)
xz=calcul_xz(coord,xg, zg)
PD_strip_info_from_for_to_aft("masses.csv","correct_frames_of_oural.asc")