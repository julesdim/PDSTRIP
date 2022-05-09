import numpy as np

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
            print(m*(re-rb)/(xem-xbm))
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
            print(masses[i][5])
    xg=xg/tm
    zg=zg/tm
    return (xg,0,zg)

print (mass_calculation(list_of_masses,70,80))
print(calcul_center_of_gravity(list_of_masses,70,80))