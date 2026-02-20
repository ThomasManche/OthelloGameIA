#Hello world 

import numpy
import time
import copy


# Jeu d'Othello : Variable

plat = numpy.zeros((8,8),str)
PionBlanc = "B"
PionNoir = "N"




def InitialisePlateau():
    global plat
    plat=numpy.zeros((8,8),str)
    plat[3][3]=PionBlanc
    plat[4][4]=PionBlanc
    plat[3][4]=PionNoir
    plat[4][3]=PionNoir
    for i in range(0,8):
        for j in range(0,8):
            if plat[i][j]=='':
                plat[i][j]=' '

def checkCoup(x,y,incrementX, incrementY,plateau, joueur=None):
        if joueur is None:
            joueur = TourActuel

        if plateau[x+incrementX][y+incrementY]==("N" if joueur=="B" else "B"):
            if x+(incrementX*2)>-1 and x+(incrementX*2)<8 and y+(incrementY*2)<8 and y+(incrementY*2)>-1:
                if plateau[x+(incrementX*2)][y+(incrementY*2)]==joueur:
                    return True  
                return checkCoup(x+incrementX,y+incrementY,incrementX,incrementY, plateau, joueur)  
        return False


def CoupAutorise(i,j, plateau, joueur=None):
    if joueur is None:
        joueur = TourActuel

    #On doit check chaque diagonale & Chaque côté pour voir si le coup est autorisé
    if plateau[i][j]!=' ':
        return False
    if (i>1):
        #OOn prend le pion au dessus
        if checkCoup(i,j,-1,0,plateau,joueur):
            return True
        if (j>1):
            #Diagonale Gauche
            if checkCoup(i,j,-1,-1,plateau,joueur):
                return True
        if (j<6):
            #Diagonale droite
            if checkCoup(i,j,-1,1,plateau,joueur):
                return True
    if (i<6):
        #Pion en dessous
        if checkCoup(i,j,1,0,plateau,joueur):
            return True
        if (j>1):
            #Diagonale bas gauche
            if checkCoup(i,j,1,-1,plateau,joueur):
                return True
        if (j<6):
            #Diagonale bas droite
            if checkCoup(i,j,1,1,plateau,joueur):
                return True
    if (j>1):
        # Gauche
        if checkCoup(i,j,0,-1,plateau,joueur):
            return True
    if (j<6):
        # Droite
        if checkCoup(i,j,0,1,plateau,joueur):
            return True
    return False


def ChangeCaseCoupAutorise(x,y,incrementX,incrementY,plateau, joueur=None):
    if joueur is None:
        joueur = TourActuel
    case=plateau[x+incrementX][y+incrementY]
    while case!=TourActuel:
        ChangeCouleurCase(x+incrementX,y+incrementY,plateau)
        x=x+incrementX
        y=y+incrementY
        case=plateau[x+incrementX][y+incrementY]

def ChangeCouleurCase(i,j,plateau):
    if plateau[i][j]=="B":
        plateau[i][j]="N"
    elif plateau[i][j]=="N":
        plateau[i][j]="B"

def ChangeTour():
    global TourActuel
    TourActuel="N" if TourActuel=="B" else "B"

def PosePion(i,j,plateau, joueur=None):
    if joueur is None:
        joueur = TourActuel
    plateau[i][j]=joueur
    if (i>1):
        #On prend le pion au dessus
        if checkCoup(i,j,-1,0,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,-1,0,plateau,joueur)
        if (j>1):
            #Diagonale Gauche
            if checkCoup(i,j,-1,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,-1,-1,plateau,joueur)
        if (j<6):
            #Diagonale droite
            if checkCoup(i,j,-1,1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,-1,1,plateau,joueur)
    if (i<6):
        #Pion en dessous
        if checkCoup(i,j,1,0,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,1,0,plateau,joueur)
        if (j>1):
            #Diagonale bas gauche
            if checkCoup(i,j,1,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,1,-1,plateau,joueur)
        if (j<6):
            #Diagonale bas droite
            if checkCoup(i,j,1,1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,1,1,plateau,joueur)
    if (j>1):
        # Gauche
        if checkCoup(i,j,0,-1,plateau,joueur):
                ChangeCaseCoupAutorise(i,j,0,-1,plateau,joueur)
    if (j<6):
        # Droite
        if checkCoup(i,j,0,1,plateau,joueur):
            ChangeCaseCoupAutorise(i,j,0,1,plateau,joueur)

def CoupJoue(i,j,plateau):
    if CoupAutorise(i,j,plateau):
        PosePion(i,j,plateau)
        ChangeTour()

def isFinished(plateau):
    condRemplissage=True
    condCoupPossible=False
    for i in range(0,len(plateau)):
        for j in range(0,len(plateau[0])):
            if plateau[i][j]==' ':
                condRemplissage=False
                if CoupAutorise(i,j,plateau):
                    condCoupPossible=True
    if condCoupPossible==False and condRemplissage==False:
        for i in range(0,len(plateau)):
            for j in range(0,len(plateau[0])):
                if CoupAutorise(i,j,plateau,"B" if TourActuel=="N" else "N"):
                    #print("Le joueur "+TourActuel+ " ne peut pas jouer, on repasse directement au joueur "+"B" if TourActuel=="N" else "N")
                    ChangeTour()
                    return False
    if condRemplissage==True or condCoupPossible==False or nombrePion("N", plat)==0 or nombrePion("B",plat)==0:
        return True
        
    return False
    

    # Rajouter le fait que si un des deux joueurs ne peut pas jouer, ca skip juste le tour ;)

TourActuel=PionNoir

def TestFonction():
    global TourActuel
    InitialisePlateau()
    print(plat)
    print("JEU D'OTHELLO")
    TourActuel=PionNoir
    while True:

        #time.sleep(1)
        if TourActuel=="B":
            #(x,y),_=MinMaxMaximise(TourActuel, plat, 2,2)
            (x,y)=MinMaxV1meilleurCoup(TourActuel,plat,2)
        else:
            (x,y)=MinMaxV1meilleurCoup(TourActuel,plat,2)
        #x=int(input("x:"))
        #y=int(input("y:"))
        if CoupAutorise(x,y,plat):
            PosePion(x,y,plat)
            print(plat)
            ChangeTour()
            if isFinished(plat):
                print(plat)
                print("C'est fini !")
                print("Score du joueur B : "+str(nombrePion("B",plat))+"\n")
                print("Score du joueur N : " + str(nombrePion("N",plat))+"\n")
                break

        else:
            print("Coup non valable !")
           
            print(plat)
            

def getResultat():
    RecursiviteMax=2
    compteurTour=1
    with open('resultat.txt','w') as f:
        f.write("Jeu d'Othello - Résultats \n")
    global TourActuel
    for t in range(0,2):
        for i in range(0,2):
            #Fonction pour B
            for j in range(0,2):
                #Fonction pour N
                for k in range(1,3):
                    #Score pour B
                    for l in range(1,3):
                        #Score pour N
                        for m in range(1,RecursiviteMax+1):
                            if m==2 and i!=1:
                                break
                            for n in range(1,RecursiviteMax+1):
                                if n==2 and j!=1:
                                    break
                                InitialisePlateau()
                                pt=0
                                print("Tour "+str(compteurTour))
                                compteurTour+=1
                                if t==0:
                                    TourActuel="N"
                                else:
                                    TourActuel="B"
                                print(str(i) + ","+ str(j)+","+str(k)+","+str(l)+","+str(m)+","+str(n) + " pour le tour "+ TourActuel + "\n")
                                with open('resultat.txt','a') as f:
                                    f.write(str(i) + ","+ str(j)+","+str(k)+","+str(l)+","+str(m)+","+str(n) + " pour le tour "+ TourActuel + "\n")
                                while True:
                                    if TourActuel=="B":
                                        if i==0:
                                            (x,y)=MinMaxV1meilleurCoup(TourActuel,plat,k)
                                        else:
                                            (x,y),_=MinMaxMaximise(TourActuel,plat,m,k)
                                    else:
                                        if j==0:
                                            (x,y)=MinMaxV1meilleurCoup(TourActuel,plat,l)
                                        else:
                                            (x,y),_=MinMaxMaximise(TourActuel,plat,n,l)      
                                    if CoupAutorise(x,y,plat):
                                        pt+=1
                                        PosePion(x,y,plat)
                                        ChangeTour()
                                        if isFinished(plat):
                                            #print(plat)
                                            with open('resultat.txt','a') as f:
                                                f.write("Coup joué :"+str(pt)+ "\n")
                                                f.write("Score du joueur B : "+str(nombrePion("B",plat))+"\n")
                                                f.write("Score du joueur N : " + str(nombrePion("N",plat))+"\n")
                                            break    



############################################################################################################
#==========================================================================================================#
#=========================== V1 : Min-max inversé de profondeur 1 =========================================#
#==========================================================================================================#
############################################################################################################
#Premiere version de l algorithme avec les min max inversés. 
# Le joueur choisit le coup qui minimise le meilleur score de l adversaire après que le joueur ait joué son coup.   
  
def MinMaxV1meilleurScoreAdversaire(joueur, plateauTemp,versionScore):
    # Cette fonction doit retourner le meilleur coup pour l'adversaire donné "N" ou "B"
    platTemp = copy.deepcopy(plateauTemp)
    scoreTemp = 0
    scoreMeilleur = float("-inf")
    coupPossible=False

    for i in range ( 0, len(platTemp)):
        for j in range ( 0, len(platTemp[i])):
            if CoupAutorise(i,j,platTemp):
                coupPossible=True
                PosePion(i,j,platTemp) # fonction plaçant le pion de l'adversaire sur le plateau temporaire
                if versionScore==1:
                    scoreTemp = score(joueur , platTemp)
                elif versionScore==2:
                    scoreTemp=scorePoidsCase(joueur, platTemp)
                if scoreTemp > scoreMeilleur:
                    scoreMeilleur = scoreTemp
                platTemp = copy.deepcopy(plateauTemp)
    if coupPossible==False:
        if versionScore == 1:
            return score(joueur, plateauTemp)
        else:
            return scorePoidsCase(joueur, plateauTemp)
    return scoreMeilleur    
                

def MinMaxV1meilleurCoup(joueur, plateau,versionScore=1 ):
    # Cette fonction doit retourner le meilleur coup pour le joueur donné "N" ou "B"
    #le meilleure coup est déterminé comme le coup qui minimise le meillescore de l'adversaire après que le joueur ait joué son coup
    plateauTemp = copy.deepcopy(plateau)
    coupMeilleurs = None
    scoreTemp = 0
    scoreAdver = 999999999
    
    for i in range ( 0, len(plateauTemp)):
        for j in range ( 0, len(plateauTemp[i])):
            if CoupAutorise(i,j,plateauTemp):
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauCoupSimule=copy.deepcopy(plateauTemp)
                PosePion(i,j,plateauCoupSimule) # fonction plaçant le pion du joueur sur le plateau temporaire
                scoreTemp =  MinMaxV1meilleurScoreAdversaire("N" if joueur=="B" else "B", plateauCoupSimule, versionScore)
                if scoreTemp <= scoreAdver:
                    scoreAdver = scoreTemp
                    coupMeilleurs = (i,j)
    
    return coupMeilleurs
    
############################################################################################################
#==========================================================================================================#
#================================== V2 : Min-max de profondeur n  =========================================#
#==========================================================================================================#
############################################################################################################

def MinMaxMinimise(joueur, plateau,profondeur,versionScore):
    # Cette fonction doit retourner le meilleur coup pour l'adversaire donné "N" ou "B"
    platTemp = copy.deepcopy(plateau)
    scoreTemp = 0
    scoreMeilleur = float("inf")
    coupPossible = False
    for i in range ( 0, len(platTemp)):
        for j in range ( 0, len(platTemp[i])):
            if CoupAutorise(i,j,platTemp,"B" if joueur=="N" else "N"):
                coupPossible=True
                PosePion(i,j,platTemp,"B" if joueur=="N" else "N") 
                _,scoreTemp = MinMaxMaximise(joueur , platTemp, profondeur-1,versionScore) 
                if scoreTemp < scoreMeilleur:
                    scoreMeilleur = scoreTemp
                platTemp = copy.deepcopy(plateau)
    if coupPossible==False:
        if versionScore == 1:
            return score(joueur, plateau)
        else:
            return scorePoidsCase(joueur, plateau)
    return scoreMeilleur    
                

def MinMaxMaximise(joueur, plateau,profondeur, versionScore=1 ):
    # Cette fonction doit retourner le meilleur coup pour le joueur donné "N" ou "B"
    #le meilleure coup est déterminé comme le coup qui minimise le meillescore de l'adversaire après que le joueur ait joué son coup
    plateauTemp = None
    bestCoup = None
    scoreTemp = 0
    bestscore = float("-inf")
    if profondeur==0:
        if versionScore==1:
            return bestCoup,score(joueur,plateau)
        elif versionScore==2:
            return bestCoup,scorePoidsCase(joueur,plateau)
    for i in range ( 0, len(plateau)):
        for j in range ( 0, len(plateau[i])):
            if CoupAutorise(i,j,plateau):
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauTemp=copy.deepcopy(plateau)
                PosePion(i,j,plateauTemp) # fonction plaçant le pion du joueur sur le plateau temporaire
                scoreTemp =  MinMaxMinimise(joueur, plateauTemp, profondeur, versionScore)
                if scoreTemp >= bestscore:
                    bestscore = scoreTemp
                    bestCoup = (i,j)
        
    return bestCoup, bestscore



############################################################################################################
#==========================================================================================================#
#================================== V3: Score au poids des cases  =========================================#
#==========================================================================================================#
############################################################################################################

tableauPoids = [
[500,-150,30,10,10,30,-150,500],
[-150,-250,0,0,0,0,-250,-150],
[30,0,1,2,2,1,0,30],
[10,0,2,16,16,2,0,10],
[10,0,2,16,16,2,0,10],
[30,0,1,2,2,1,0,30],
[-150,-250,0,0,0,0,-250,-150],
[500,-150,30,10,10,30,-150,500]]

def nombrePion (joueur,plat):
    score=0
    scoreAdversaire=0
    for i in range(0,len(plat)):
        for j in range(0,len(plat[i])):
            if plat[i][j]==joueur:
                score+=1
            elif plat[i][j]==("B" if joueur=="N" else "N"):
                scoreAdversaire+=1
    if scoreAdversaire==0:
        score=64
    return score


def score(joueur, plat):
    # Cette fonction doit retourner le score du joueur donné "N" ou "B"
    # Le score est défini comme le nombre de pions du joueur sur le plateau - le nombre de pions de l'adversaire

    score = 0
    scoreAdversaire=0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if (plat[i][j] == joueur):
                score+=1
            elif (plat[i][j] == ("B" if joueur=="N" else "N")):
                scoreAdversaire+=1
    if scoreAdversaire==0:
        score=64
    return score - scoreAdversaire


def scorePoidsCase(joueur, plat):
    # Cette fonction doit retourner le score du joueur donné "N" ou "B"
    # Le score est défini comme le nombre de pions du joueur sur le plateau - le nombre de pions de l'adversaire, suivant le poids actif
    score = 0
    scoreAdversaire=0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if (plat[i][j] == joueur):
                score+=tableauPoids[i][j]
            elif (plat[i][j] == ("B" if joueur=="N" else "N")):
                scoreAdversaire+=tableauPoids[i][j]
    if scoreAdversaire==0:
        score=0
        for i in range(0, len(plat)):
            for j in range(0,len(plat[i])):
                score+=tableauPoids[i][j]
    return score - scoreAdversaire


    

    
    


    
#TestFonction()
getResultat()