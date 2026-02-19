#Hello world 

import numpy
import time



# Jeu d'Othello : Variable

plat = numpy.zeros((8,8),str)
PionBlanc = "B"
PionNoir = "N"

TourActuel=PionNoir


def InitialisePlateau(plateau):
    plateau[3][3]=PionBlanc
    plateau[4][4]=PionBlanc
    plateau[3][4]=PionNoir
    plateau[4][3]=PionNoir
    for i in range(0,8):
        for j in range(0,8):
            if plateau[i][j]=='':
                plateau[i][j]=' '

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
                    print("Le joueur "+TourActuel+ " ne peut pas jouer, on repasse directement au joueur "+"B" if TourActuel=="N" else "N")
                    ChangeTour()
                    return False
    if condRemplissage==True or condCoupPossible==False:
        print("Fin de la partie : Aucun coup n'est jouable")
        print("Score du joueur B : "+str(score("B",plat)))
        print("Score du joueur N : " + str(score("N",plat)))
        return True
        
    return False
    

    # Rajouter le fait que si un des deux joueurs ne peut pas jouer, ca skip juste le tour ;)


def TestFonction():
    InitialisePlateau(plat)
    print(plat)
    print("JEU D'OTHELLO")
    while True:
        time.sleep(1)
        print("Joueur "+TourActuel)
        (x,y),_=MinMaxMaximise(TourActuel, plat, 3)
        print(x,y)
        #x=int(input("x:"))
        #y=int(input("y:"))
        if CoupAutorise(x,y,plat):
            print("Coup autorisé ! Coup autorisé !")
            PosePion(x,y,plat)
            print(plat)
            ChangeTour()
            if isFinished(plat):
                print("C'est fini !")
                break

        else:
            print("Coup non valable !")
           
            print(plat)
            


def score(joueur, plat):
    # Cette fonction doit retourner le score du joueur donné "N" ou "B"
    # Le score est défini comme le nombre de pions du joueur sur le plateau

    score = 0
    
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if (plat[i][j] == joueur):
                score+=1
    return score

############################################################################################################
#==========================================================================================================#
#=========================== V1 : Min-max inversé de profondeur 1 =========================================#
#==========================================================================================================#
############################################################################################################
#Premiere version de l algorithme avec les min max inversés. 
# Le joueur choisit le coup qui minimise le meilleur score de l adversaire après que le joueur ait joué son coup.   
  
def MinMaxV1meilleurScoreAdversaire(joueur, plateauTemp):
    # Cette fonction doit retourner le meilleur coup pour l'adversaire donné "N" ou "B"
    platTemp = plateauTemp.copy()
    scoreTemp = 0
    scoreMeilleur = 0
    
    for i in range ( 0, len(platTemp)):
        for j in range ( 0, len(platTemp[i])):
            if CoupAutorise(i,j,platTemp):
                PosePion(i,j,platTemp) # fonction plaçant le pion de l'adversaire sur le plateau temporaire
                scoreTemp = score(joueur , platTemp)
                if scoreTemp > scoreMeilleur:
                    scoreMeilleur = scoreTemp
                platTemp = plateauTemp.copy()
    return scoreMeilleur    
                

def MinMaxV1meilleurCoup(joueur, plateau ):
    # Cette fonction doit retourner le meilleur coup pour le joueur donné "N" ou "B"
    #le meilleure coup est déterminé comme le coup qui minimise le meillescore de l'adversaire après que le joueur ait joué son coup
    plateauTemp = plateau.copy()
    coupMeilleurs = None
    scoreTemp = 0
    scoreAdver = -1
    
    for i in range ( 0, len(plateauTemp)):
        for j in range ( 0, len(plateauTemp[i])):
            if CoupAutorise(i,j,plateauTemp):
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauCoupSimule=plateauTemp.copy()
                PosePion(i,j,plateauCoupSimule) # fonction plaçant le pion du joueur sur le plateau temporaire
                scoreTemp =  MinMaxV1meilleurScoreAdversaire("N" if joueur=="B" else "B", plateauCoupSimule)
                if scoreAdver == -1:
                    scoreAdver = scoreTemp
                if scoreTemp <= scoreAdver:
                    scoreAdver = scoreTemp
                    coupMeilleurs = (i,j)
    return coupMeilleurs
    
############################################################################################################
#==========================================================================================================#
#================================== V2 : Min-max de profondeur n  =========================================#
#==========================================================================================================#
############################################################################################################

def MinMaxMinimise(joueur, plateau,profondeur):
    # Cette fonction doit retourner le meilleur coup pour l'adversaire donné "N" ou "B"
    platTemp = plateau.copy()
    scoreTemp = 0
    scoreMeilleur = 999999
    
    for i in range ( 0, len(platTemp)):
        for j in range ( 0, len(platTemp[i])):
            if CoupAutorise(i,j,platTemp,"B" if joueur=="N" else "N"):
                PosePion(i,j,platTemp,"B" if joueur=="N" else "N") 
                _,scoreTemp = MinMaxMaximise(joueur , platTemp, profondeur-1) 
                if scoreTemp < scoreMeilleur:
                    scoreMeilleur = scoreTemp
                platTemp = plateau.copy()
    return scoreMeilleur    
                

def MinMaxMaximise(joueur, plateau,profondeur ):
    # Cette fonction doit retourner le meilleur coup pour le joueur donné "N" ou "B"
    #le meilleure coup est déterminé comme le coup qui minimise le meillescore de l'adversaire après que le joueur ait joué son coup
    plateauTemp = None
    bestCoup = None
    scoreTemp = 0
    bestscore = -99999999
    if profondeur==0:
        return bestCoup,score(joueur,plateau)
    for i in range ( 0, len(plateau)):
        for j in range ( 0, len(plateau[i])):
            if CoupAutorise(i,j,plateau):
                #print("Coup autorisé pour i:"+str(i) + "et j : "+ str(j))
                plateauTemp=plateau.copy()
                PosePion(i,j,plateauTemp) # fonction plaçant le pion du joueur sur le plateau temporaire
                scoreTemp =  MinMaxMinimise(joueur, plateauTemp, profondeur)
                if bestscore == -1:
                    bestscore = scoreTemp
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
    
def scorePoidsCase(joueur, plat):
    # Cette fonction doit retourner le score du joueur donné "N" ou "B"
    # Le score est défini comme le nombre de pions du joueur sur le plateau
    score = 0
    for i in range ( 0, len(plat)):
        for j in range ( 0, len(plat[i])):
            if (plat[i][j] == joueur):
                score+=tableauPoids[i][j]
    return score


    

    
    


    

TestFonction()